"""Tests for the routing script.

The weight is on **resisting container inertia**: the frozen template's first paragraph warns
that containers MUST NOT be forced on mobile, desktop, SDK, library, plugin or embedded
projects, while its second paragraph is entirely about Docker. A warning does not stop
inertia; an assertion does.

Every class of assertion has a negative sample - with positive samples alone, an all-green
run cannot distinguish "genuinely fine" from "the checker is broken".
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from route_release import Channel, route  # noqa: E402

NL = chr(10)


class Fixture:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def write(self, name, text=""):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return self

    def close(self):
        self.tmp.cleanup()


class TestNoContainerInertia(unittest.TestCase):
    """Three non-container scenarios. A container appearing in any of them defeats this
    skill's reason for existing."""

    def _route(self, fx):
        self.addCleanup(fx.close)
        return route(fx.root)

    def test_python_cli_goes_to_package_registry(self):          # AC-012-1
        r = self._route(Fixture().write("pyproject.toml",
            '[project]' + NL + 'name = "csv2md"' + NL
            + '[project.scripts]' + NL + 'csv2md = "csv2md.cli:main"' + NL))
        self.assertIn(Channel.PACKAGE_REGISTRY, r.channels)
        self.assertNotIn(Channel.CONTAINER, r.channels,
                         "routing a CLI tool to a container is exactly what this skill blocks")

    def test_npm_library_goes_to_package_registry(self):         # AC-012-2
        r = self._route(Fixture().write("package.json",
            '{"name":"tinyparse","version":"1.0.0","main":"index.js"}'))
        self.assertIn(Channel.PACKAGE_REGISTRY, r.channels)
        self.assertNotIn(Channel.CONTAINER, r.channels)

    def test_ios_goes_to_app_store(self):                        # AC-012-4
        r = self._route(Fixture().write("TeamPulse.podspec", "Pod::Spec.new"))
        self.assertIn(Channel.APP_STORE, r.channels)
        self.assertNotIn(Channel.CONTAINER, r.channels,
                         "writing a Dockerfile for an iOS project is explicitly forbidden by the frozen template")


class TestPositiveRouting(unittest.TestCase):
    """The negative-sample direction: what should route to a container must actually do so."""

    def _route(self, fx):
        self.addCleanup(fx.close)
        return route(fx.root)

    def test_web_backend_goes_to_container(self):                # AC-012-3
        r = self._route(Fixture()
            .write("Dockerfile", "FROM python:3.12")
            .write("docker-compose.yml", "services:")
            .write("pyproject.toml", '[project]' + NL + 'name = "api"' + NL))
        self.assertIn(Channel.CONTAINER, r.channels)

    def test_multiple_artifacts_get_multiple_channels(self):     # AC-012-6
        r = self._route(Fixture()
            .write("Dockerfile", "FROM python:3.12")
            .write("pyproject.toml",
                   '[project]' + NL + 'name = "svc"' + NL
                   + '[project.scripts]' + NL + 'svc = "svc.cli:main"' + NL))
        self.assertIn(Channel.CONTAINER, r.channels)
        self.assertIn(Channel.PACKAGE_REGISTRY, r.channels)
        self.assertGreaterEqual(len(r.channels), 2,
                                "a service and a CLI MUST NOT be merged into one channel")


class TestConflictIsReportedNotDecided(unittest.TestCase):
    """The script reports; the user rules. A script that chooses turns a wrong judgement into
    an apparently objective conclusion."""

    def test_docker_plus_podspec_is_a_conflict(self):            # AC-012-10
        fx = Fixture().write("Dockerfile", "FROM x").write("A.podspec", "Pod::Spec.new")
        self.addCleanup(fx.close)
        r = route(fx.root)
        self.assertTrue(r.conflicts,
                        "hitting both container and app-store signals MUST report a conflict")

    def test_clean_project_has_no_conflict(self):
        """Negative sample: a project with a clear shape MUST NOT be reported as conflicting."""
        fx = Fixture().write("package.json", '{"name":"lib","main":"i.js"}')
        self.addCleanup(fx.close)
        self.assertEqual(route(fx.root).conflicts, [])


class TestUnknownAndEmpty(unittest.TestCase):
    def test_no_manifest_does_not_crash(self):                   # AC-012-8
        fx = Fixture()
        self.addCleanup(fx.close)
        r = route(fx.root)
        self.assertEqual(r.channels, [])
        self.assertTrue(r.unknown, "with no manifest it MUST report unknown rather than guess")

    def test_manifest_without_shape_signal_is_unknown(self):
        """go.mod exists but there is no main package - the shape is unclear, so mark it
        pending rather than guessing."""
        fx = Fixture().write("go.mod", "module example.com/x")
        self.addCleanup(fx.close)
        self.assertTrue(route(fx.root).unknown)


class TestDeterminism(unittest.TestCase):
    def test_same_input_same_output(self):                       # AC-012-9
        fx = Fixture().write("package.json", '{"name":"lib","main":"i.js"}')
        self.addCleanup(fx.close)
        a, b = route(fx.root), route(fx.root)
        self.assertEqual((a.channels, a.conflicts, a.unknown),
                         (b.channels, b.conflicts, b.unknown))

    def test_channels_are_sorted(self):
        """A stable order, without which 'byte-identical' means nothing."""
        fx = Fixture().write("Dockerfile", "FROM x").write(
            "pyproject.toml", '[project]' + NL + 'name="s"' + NL
            + '[project.scripts]' + NL + 's="s:m"' + NL)
        self.addCleanup(fx.close)
        self.assertEqual(route(fx.root).channels, sorted(route(fx.root).channels))


if __name__ == "__main__":
    unittest.main(verbosity=2)
