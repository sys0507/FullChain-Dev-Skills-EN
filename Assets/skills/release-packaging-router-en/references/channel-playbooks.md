# The seven release channels: playbooks

## When to read this

**After the routing decision is made and the user has confirmed the channel** — then read
that one section.

**Do not read it end to end.** Each section applies only when routed to, which is exactly why
this skill exists.

---

## 1. Container

> **Applies only when routed to a container.** This section is demoted from the frozen
> template's original stage 11 prompt — the prompt itself is correct; **what was wrong was
> treating it as the whole of stage 11**.

What clarify must settle:

| # | Question |
|:-:|---|
| 1 | Base image selection |
| 2 | Multi-stage build strategy |
| 3 | Image size ceiling |
| 4 | Deployment target: self-hosted VPS or a PaaS |
| 5 | Whether to generate a CI build-and-push workflow |
| 6 | How production configuration is isolated from development |
| 7 | The health check endpoint convention |

Feature goal: every runtime service becomes a production-grade image; after
`docker compose up -d` every service is healthy, each exposes its port, and migration-style
startup hooks have run in order.

---

## 2. Package registry

npm, PyPI, crates.io, Maven Central, a private registry.

| # | What clarify must ask |
|:-:|---|
| 1 | Which registry (public or private) |
| 2 | Whether the package name is already taken |
| 3 | Versioning policy (semver? a prerelease channel?) |
| 4 | The supported runtime version range |
| 5 | Whether CI publishes automatically, or a human does |
| 6 | Whether the licence and author information are complete |

**Do not ask about containers.** A library needs no image.

---

## 3. App store

App Store, Google Play, Microsoft Store.

| # | What clarify must ask |
|:-:|---|
| 1 | Whether a developer account is already registered (**do not register on the user's behalf**) |
| 2 | Where the signing certificates and provisioning profiles come from |
| 3 | The minimum supported OS version |
| 4 | Who prepares the review assets (screenshots, privacy statement, age rating) |
| 5 | Staged rollout or full release |

**Layout units are size class and dp, not breakpoints.** If the upstream `DESIGN.md` uses web
breakpoints, report it back to the design stage; **do not convert it yourself**.

---

## 4. Installer

.msi / .dmg / .deb / .rpm / AppImage.

| # | What clarify must ask |
|:-:|---|
| 1 | The target operating system and architecture matrix |
| 2 | Whether code signing is needed (Windows signing, macOS notarisation) |
| 3 | Whether an auto-update mechanism is required |
| 4 | What happens to user data on uninstall |

---

## 5. Firmware

| # | What clarify must ask |
|:-:|---|
| 1 | The target chip and its flash ceiling |
| 2 | The flashing method (serial / OTA / production jig) |
| 3 | Whether a rollback partition is needed |
| 4 | Where the version identifier is written |

---

## 6. Hosting platform

Vercel, Netlify, Fly.io, Railway and similar.

| # | What clarify must ask |
|:-:|---|
| 1 | Whether the platform account and project already exist |
| 2 | Whether environment variables are managed on the platform side or in the repository (**secrets never enter version control**) |
| 3 | The build command and output directory |
| 4 | Custom domains and certificates |
| 5 | Whether preview environments are needed |

---

## 7. Private registry

Nexus, Artifactory, an internal registry, a shared directory.

| # | What clarify must ask |
|:-:|---|
| 1 | The registry address and authentication method (**credentials go only into ignored local files**) |
| 2 | The artifact naming and versioning convention |
| 3 | The retention policy (how long, how many versions) |
| 4 | How machines on the internal network pull from it |

---

## Common: after routing, take the existing chain

Once the release channel is settled, **still follow the existing chain**: spec -> clarify ->
plan -> tasks -> TDD -> review -> finish -> learnings. This skill only creates the directory
and the spec skeleton; the four steps go to `speckit-feature-pipeline-en`.

See `artifact-detection.md` for how the artifact shape is detected.
