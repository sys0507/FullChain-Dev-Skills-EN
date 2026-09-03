"""检查器自身的测试。

**每项检查都有正样本（应报错）与负样本（不应报错）。**
这不是完备性追求，是本项目付出代价换来的硬要求：
自检误报过 6 次，全部是检查器自身的问题，零次真实文档缺陷。
没有负样本时，一次全绿无法区分「真的没问题」与「检查器坏了」。

正样本取自本仓库真实发生过的缺陷，不是构造的——真实缺陷比构造样本更能反映实际形态。
夹具自建，不依赖仓库当前状态，否则测试结果会随资产演进而漂移。
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

NL = chr(10)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from messages import LANGS, MESSAGES, current_language, set_language, t  # noqa: E402

from checks import (  # noqa: E402
    C1References,
    C2Pairing,
    C3EnPurity,
    C4EnEvals,
    C5ScriptsNeedTests,
    C6SelfContained,
    C7StandaloneSection,
    C8Requires,
    C9SizeBudget,
    C10MatrixPathsInSkill,
)
from common import CJK, headings, normalize, section, strip_fences  # noqa: E402

GOOD_FM = """---
name: demo
description: 一个示例 Skill。不用于：别的事情。
metadata:
  version: "1.0"
  lang: zh
  standalone: true
  requires:
    - name: "上游文件"
      level: 编排级
      fallback: "请用户直接提供"
---
"""

EN_SECTIONS = """
## Upstream artefacts

The upstream file, orchestration-level.

## Downstream consumers

Downstream skills read the output.

## Standalone use

What you supply, what you get, what you do not get.
"""

EN_FM = """---
name: demo-en
description: A demo skill. Do not use for other things.
metadata:
  version: "1.0"
  lang: en
  standalone: true
  requires:
    - name: "upstream file"
      level: orchestration
      fallback: "ask the user to supply it directly"
---
"""

GOOD_SECTIONS = """
## 上游产物

| 产物 | 级别 | 缺失时 |
|---|---|---|
| 上游文件 | 编排级 | 请用户直接提供 |

## 下游消费者

下游 Skill 读产出。

## 独立使用

**要你提供什么**：一段描述。
**能得到什么**：完整产出。
**得不到什么**：不做上游的事。
"""


def make(root: Path, name: str, *, fm: str = GOOD_FM, body: str = GOOD_SECTIONS,
         refs: dict[str, str] | None = None, scripts: bool = False,
         tests: bool = False, evals: dict | None = None) -> Path:
    d = root / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(fm + "\n# " + name + "\n" + body, encoding="utf-8")
    if refs:
        (d / "references").mkdir()
        for fn, content in refs.items():
            (d / "references" / fn).write_text(content, encoding="utf-8")
    if scripts:
        (d / "scripts").mkdir()
        (d / "scripts" / "x.py").write_text("# x\n", encoding="utf-8")
    if tests:
        (d / "tests").mkdir()
        (d / "tests" / "t.py").write_text("# t\n", encoding="utf-8")
    if evals is not None:
        (d / "evals").mkdir()
        (d / "evals" / "evals.json").write_text(json.dumps(evals, ensure_ascii=False),
                                                encoding="utf-8")
    return d


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)


# ---------------------------------------------------------------- C1

class TestC1References(Base):
    """正样本取自真实缺陷：一个英文版引用了 3 个不存在的 references。"""

    def test_positive_broken_link(self):
        make(self.root, "a", body=GOOD_SECTIONS + "\n见 `references/missing.md`\n")
        found = C1References().run(self.root)
        self.assertTrue(any(f.key == "c1.broken_link" for f in found))

    def test_positive_orphan_file(self):
        make(self.root, "a", refs={"unused.md": "x"})
        found = C1References().run(self.root)
        self.assertTrue(any(f.key == "c1.orphan" for f in found))

    def test_positive_subdir_under_references(self):
        """真实缺陷：evals 被放进了 references/ 下。"""
        d = make(self.root, "a", refs={"used.md": "x"})
        (d / "references" / "evals").mkdir()
        (d / "SKILL.md").write_text((d / "SKILL.md").read_text(encoding="utf-8")
                                    + "\n见 `references/used.md`\n", encoding="utf-8")
        found = C1References().run(self.root)
        self.assertTrue(any(f.key == "c1.subdir" for f in found))

    def test_negative_clean(self):
        make(self.root, "a", body=GOOD_SECTIONS + "\n见 `references/used.md`\n",
             refs={"used.md": "x"})
        self.assertEqual(C1References().run(self.root), [])


# ---------------------------------------------------------------- C2

class TestC2Pairing(Base):
    """正样本取自真实缺陷：英文版比中文版多了几节的结构漂移。"""

    def test_positive_heading_drift(self):
        make(self.root, "a")
        make(self.root, "a-en", body=GOOD_SECTIONS + "\n## 多出来的一节\n\n内容\n")
        found = C2Pairing().run(self.root)
        self.assertTrue(any(f.key == "c2.heading_count" for f in found))

    def test_positive_references_mismatch(self):
        make(self.root, "a", body=GOOD_SECTIONS + "\n见 `references/x.md`\n",
             refs={"x.md": "1"})
        make(self.root, "a-en")
        found = C2Pairing().run(self.root)
        self.assertTrue(any(f.key == "c2.refs_mismatch" for f in found))

    def test_negative_matched_pair(self):
        make(self.root, "a")
        make(self.root, "a-en")
        self.assertEqual(C2Pairing().run(self.root), [])

    def test_negative_fenced_headings_not_counted(self):
        """关键负样本：围栏内的 ## 不得被计为标题。

        真实教训：未剔除围栏时，把提示词正文里的 ## 误计为标题，
        误报某个英文版有 5 节漂移，实际只有 1 节。
        """
        fenced = GOOD_SECTIONS + "\n```\n## 这是代码块里的假标题\n## 又一个\n```\n"
        make(self.root, "a", body=fenced)
        make(self.root, "a-en")
        self.assertEqual(C2Pairing().run(self.root), [],
                         "围栏内的 ## 被误计为标题")

    def test_negative_missing_en_without_en_root_is_out_of_scope(self):
        """单语树未显式给 en_root 时，不猜测另一棵树的位置。"""
        make(self.root, "a")
        self.assertEqual(C2Pairing().run(self.root), [])

    def test_positive_orchestrator_is_not_exempt(self):
        """英文编排器落地后不再保留任何配对豁免。"""
        make(self.root, "fullchain-dev-workflow")
        en = self.root / "en"
        en.mkdir()
        found = C2Pairing().run(self.root, en_root=en)
        self.assertTrue(any(f.key == "c2.missing_en_skill" for f in found))

    def test_positive_assets_mismatch(self):
        zh = make(self.root, "a")
        make(self.root, "a-en")
        (zh / "assets").mkdir()
        (zh / "assets" / "template.md").write_text("x\n", encoding="utf-8")
        found = C2Pairing().run(self.root)
        self.assertTrue(any(f.key == "c2.assets_mismatch" for f in found))

    def test_positive_produces_count_drift(self):
        zh_fm = GOOD_FM.replace(
            "  requires:\n", '  produces:\n    - "one"\n    - "two"\n  requires:\n')
        en_fm = EN_FM.replace(
            "  requires:\n", '  produces:\n    - "one"\n  requires:\n')
        make(self.root, "a", fm=zh_fm)
        make(self.root, "a-en", fm=en_fm)
        found = C2Pairing().run(self.root)
        self.assertTrue(any(f.key == "c2.produces_count" for f in found))


# ---------------------------------------------------------------- C3

class TestC3EnPurity(Base):
    """正样本取自真实缺陷：英文版正文引用了中文文件名。"""

    def test_positive_chinese_in_en(self):
        make(self.root, "a-en", fm=EN_FM,
             body=EN_SECTIONS + "\nSee `specs/research/00-项目输入与假设.md`\n")
        found = C3EnPurity().run(self.root)
        self.assertTrue(any(f.key == "c3.residue" for f in found))

    def test_positive_chinese_in_non_markdown_text(self):
        """HTML、脚本和 JSON 中的中文同样会进入英文 Skill 的运行产物。"""
        d = make(self.root, "a-en", fm=EN_FM, body=EN_SECTIONS)
        samples = {
            "scripts/viewer.html": "<button>下单</button>\n",
            "scripts/run.py": 'print("执行")\n',
            "assets/example.json": '{"label": "结果"}\n',
        }
        for relative, content in samples.items():
            path = d / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        found = C3EnPurity().run(self.root)
        paths = {f.path.replace("\\", "/") for f in found}
        for relative in samples:
            self.assertTrue(any(relative in path for path in paths), relative)

    def test_negative_pure_english(self):
        make(self.root, "a-en", fm=EN_FM, body=EN_SECTIONS)
        self.assertEqual(C3EnPurity().run(self.root), [])

    def test_negative_bilingual_marker_whitelisted(self):
        """刻意保留的双语触发词不报。"""
        make(self.root, "a-en", fm=EN_FM,
             body=EN_SECTIONS + "\n**Chinese (for reference)**: 新项目立项 / 产品调研\n")
        self.assertEqual(C3EnPurity().run(self.root), [])

    def test_negative_em_dash_and_arrow_not_chinese(self):
        """关键负样本：— 与 → 是多字节但不是中文。

        真实教训：用字节区间判定时把它们算成了中文，导致占比统计虚高。
        """
        make(self.root, "a-en", fm=EN_FM, body=EN_SECTIONS + "\nRed — Green → Refactor\n")
        self.assertEqual(C3EnPurity().run(self.root), [],
                         "破折号与箭头被误判为中文")


# ---------------------------------------------------------------- C4

class TestC4EnEvals(Base):
    """正样本取自真实缺陷：英文版 evals 是中文版的逐字节副本。"""

    def test_positive_skill_name_without_en(self):
        make(self.root, "a-en", evals={"skill_name": "a", "evals": []})
        found = C4EnEvals().run(self.root)
        self.assertTrue(any(f.key == "c4.name_missing_en" for f in found))

    def test_positive_chinese_prompt(self):
        make(self.root, "a-en",
             evals={"skill_name": "a-en", "evals": [{"id": 1, "prompt": "帮我生成"}]})
        found = C4EnEvals().run(self.root)
        self.assertTrue(any(f.key == "c4.prompt_cjk" for f in found))

    def test_negative_clean_en_evals(self):
        make(self.root, "a-en",
             evals={"skill_name": "a-en", "evals": [{"id": 1, "prompt": "Generate it"}]})
        self.assertEqual(C4EnEvals().run(self.root), [])

    def test_negative_no_evals_dir(self):
        make(self.root, "a-en")
        self.assertEqual(C4EnEvals().run(self.root), [])

    def test_positive_paired_evals_file_missing(self):
        zh = self.root / "zh"
        en = self.root / "en"
        zh.mkdir()
        en.mkdir()
        make(zh, "a", evals={"skill_name": "a", "evals": []})
        make(en, "a-en")
        found = C4EnEvals().run(zh, en_root=en)
        self.assertTrue(any(f.key == "c4.files_mismatch" for f in found))

    def test_positive_paired_baseline_missing(self):
        zh = self.root / "zh"
        en = self.root / "en"
        zh.mkdir()
        en.mkdir()
        zd = make(zh, "a", evals={"skill_name": "a", "evals": []})
        make(en, "a-en", evals={"skill_name": "a-en", "evals": []})
        (zd / "evals" / "baseline.md").write_text("baseline\n", encoding="utf-8")
        found = C4EnEvals().run(zh, en_root=en)
        self.assertTrue(any(f.key == "c4.files_mismatch" for f in found))

    def test_positive_paired_eval_sequence_mismatch(self):
        zh = self.root / "zh"
        en = self.root / "en"
        zh.mkdir()
        en.mkdir()
        make(zh, "a", evals={"skill_name": "a", "evals": [
            {"id": 1, "name": "first", "prompt": "甲", "assertions": []},
            {"id": 2, "name": "second", "prompt": "乙", "assertions": []},
        ]})
        make(en, "a-en", evals={"skill_name": "a-en", "evals": [
            {"id": 1, "name": "first", "prompt": "A", "assertions": []},
        ]})
        found = C4EnEvals().run(zh, en_root=en)
        self.assertTrue(any(f.key == "c4.eval_sequence" for f in found))

    def test_positive_paired_assertion_count_mismatch(self):
        zh = self.root / "zh"
        en = self.root / "en"
        zh.mkdir()
        en.mkdir()
        make(zh, "a", evals={"skill_name": "a", "evals": [
            {"id": 1, "name": "first", "prompt": "甲", "assertions": [{"id": "x"}, {"id": "y"}]},
        ]})
        make(en, "a-en", evals={"skill_name": "a-en", "evals": [
            {"id": 1, "name": "first", "prompt": "A", "assertions": [{"id": "x"}]},
        ]})
        found = C4EnEvals().run(zh, en_root=en)
        self.assertTrue(any(f.key == "c4.assertion_count" for f in found))


# ---------------------------------------------------------------- C5

class TestC5ScriptsNeedTests(Base):

    def test_positive_scripts_without_tests(self):
        make(self.root, "a", scripts=True, tests=False)
        self.assertEqual(len(C5ScriptsNeedTests().run(self.root)), 1)

    def test_negative_scripts_with_tests(self):
        make(self.root, "a", scripts=True, tests=True)
        self.assertEqual(C5ScriptsNeedTests().run(self.root), [])

    def test_negative_no_scripts_at_all(self):
        make(self.root, "a")
        self.assertEqual(C5ScriptsNeedTests().run(self.root), [])

    def test_positive_paired_script_and_test_files_missing(self):
        zh = self.root / "zh"
        en = self.root / "en"
        zh.mkdir()
        en.mkdir()
        make(zh, "a", scripts=True, tests=True)
        make(en, "a-en")
        found = C5ScriptsNeedTests().run(zh, en_root=en)
        self.assertTrue(any(f.key == "c5.bundle_mismatch" for f in found))

    def test_negative_generated_python_cache_is_ignored(self):
        zh = self.root / "zh"
        en = self.root / "en"
        zh.mkdir()
        en.mkdir()
        zd = make(zh, "a", scripts=True, tests=True)
        make(en, "a-en", scripts=True, tests=True)
        cache = zd / "scripts" / "__pycache__"
        cache.mkdir()
        (cache / "tool.cpython-313.pyc").write_bytes(b"generated")
        self.assertEqual(C5ScriptsNeedTests().run(zh, en_root=en), [])


# ---------------------------------------------------------------- C6

class TestC6SelfContained(Base):

    def test_positive_relative_cross_skill_path(self):
        make(self.root, "a", body=GOOD_SECTIONS + "\n见 `../other-skill/references/x.md`\n")
        self.assertTrue(C6SelfContained().run(self.root))

    def test_positive_assets_skills_path(self):
        make(self.root, "a", body=GOOD_SECTIONS + "\n源在 `~/Assets/skills/other/`\n")
        self.assertTrue(C6SelfContained().run(self.root))

    def test_negative_soft_reference_by_name(self):
        """关键负样本：按名软引用不违反 R1。

        它不产生文件系统耦合，单独下载后只是该能力不可用，Skill 本身仍完整。
        """
        make(self.root, "a",
             body=GOOD_SECTIONS + "\n遵循 `testing-system-blueprint` 蓝本（按名引用即可）\n")
        self.assertEqual(C6SelfContained().run(self.root), [],
                         "按名软引用被误判为跨目录耦合")

    def test_negative_own_references(self):
        make(self.root, "a", body=GOOD_SECTIONS + "\n见 `references/x.md`\n",
             refs={"x.md": "1"})
        self.assertEqual(C6SelfContained().run(self.root), [])


# ---------------------------------------------------------------- C7

class TestC7StandaloneSection(Base):

    def test_positive_missing_section(self):
        make(self.root, "a", body="\n## 上游产物\n\nx\n")
        found = C7StandaloneSection().run(self.root)
        self.assertTrue(any(f.key == "c7.missing_section" and f.args["section"] == "## 独立使用"
                            for f in found))

    def test_positive_missing_question(self):
        body = GOOD_SECTIONS.replace("**得不到什么**：不做上游的事。", "")
        make(self.root, "a", body=body)
        found = C7StandaloneSection().run(self.root)
        self.assertTrue(any(f.key == "c7.missing_question" and f.args["question"] == "得不到什么"
                            for f in found))

    def test_negative_all_present(self):
        make(self.root, "a")
        self.assertEqual(C7StandaloneSection().run(self.root), [])

    def test_negative_questions_matched_within_section_only(self):
        """关键负样本：三问必须在「独立使用」切片内找到，别处出现不算。

        真实教训：全文匹配会命中规则说明或反模式列表里的同名词。
        """
        body = ("\n## 上游产物\n\n这里提到 要你提供什么 能得到什么 得不到什么\n"
                "\n## 下游消费者\n\nx\n\n## 独立使用\n\n"
                "**要你提供什么**：a\n**能得到什么**：b\n**得不到什么**：c\n")
        make(self.root, "a", body=body)
        self.assertEqual(C7StandaloneSection().run(self.root), [])


# ---------------------------------------------------------------- C8

class TestC8Requires(Base):

    def test_positive_illegal_level(self):
        fm = GOOD_FM.replace("level: 编排级", "level: 大概需要")
        make(self.root, "a", fm=fm)
        found = C8Requires().run(self.root)
        self.assertTrue(any(f.key == "c8.bad_level" for f in found))

    def test_positive_optional_without_fallback(self):
        fm = GOOD_FM.replace('      fallback: "请用户直接提供"\n', "")
        make(self.root, "a", fm=fm)
        found = C8Requires().run(self.root)
        self.assertTrue(any(f.key == "c8.no_fallback" for f in found))

    def test_positive_missing_lang(self):
        fm = GOOD_FM.replace("  lang: zh\n", "")
        make(self.root, "a", fm=fm)
        found = C8Requires().run(self.root)
        self.assertTrue(any(f.key == "c8.no_lang" for f in found))

    def test_positive_no_anti_trigger(self):
        fm = GOOD_FM.replace("不用于：别的事情。", "")
        make(self.root, "a", fm=fm)
        found = C8Requires().run(self.root)
        self.assertTrue(any(f.key == "c8.no_anti_trigger" for f in found))

    def test_negative_required_needs_no_fallback(self):
        """负样本：必需级依赖可以没有 fallback，不该报错。"""
        fm = GOOD_FM.replace('      level: 编排级\n      fallback: "请用户直接提供"\n',
                             "      level: 必需\n")
        make(self.root, "a", fm=fm)
        self.assertEqual(C8Requires().run(self.root), [])

    def test_negative_folded_description(self):
        """关键负样本：折叠式 description 跨多行，只取首行会漏判反触发。

        真实教训：005 曾因此误报 5 个 Skill 缺反触发，实际都写了。
        """
        fm = GOOD_FM.replace(
            "description: 一个示例 Skill。不用于：别的事情。",
            "description: >-\n  一个示例 Skill，说明很长很长。\n  不用于：别的事情。")
        make(self.root, "a", fm=fm)
        self.assertEqual(C8Requires().run(self.root), [],
                         "折叠式 description 中的反触发被漏判")

    def test_negative_clean(self):
        make(self.root, "a")
        self.assertEqual(C8Requires().run(self.root), [])


# ---------------------------------------------------------------- common

class TestCommonHelpers(unittest.TestCase):
    """共用工具的负样本 —— 归一化过度比不归一化更危险。"""

    def test_strip_fences(self):
        self.assertNotIn("假标题", strip_fences("a\n```\n## 假标题\n```\nb"))
        self.assertIn("真标题", strip_fences("## 真标题\n"))

    def test_normalize_ignores_emphasis(self):
        self.assertEqual(normalize("**只能**这样"), normalize("只能这样"))

    def test_normalize_keeps_real_difference(self):
        """负样本：语义不同的文本归一化后仍须不同。"""
        self.assertNotEqual(normalize("必须读宪法"), normalize("不必读宪法"))

    def test_section_returns_empty_when_absent(self):
        """章节缺失返回空串，让调用方判「缺章节」而非误判「内容不合格」。"""
        self.assertEqual(section("## 甲\nx\n", "## 乙"), "")

    def test_section_stops_at_next_heading(self):
        s = section("## 甲\n内容甲\n## 乙\n内容乙\n", "## 甲")
        self.assertIn("内容甲", s)
        self.assertNotIn("内容乙", s)

    def test_headings_skips_fences(self):
        self.assertEqual(len(headings("# 一\n```\n## 假\n```\n## 二\n")), 2)


class TestC9SizeBudget(unittest.TestCase):
    """体量上限只计内容行，双模式契约三节不计入（宪法 1.1.0 · OQ-M5 裁决）。

    真实缺陷：按总行数量，`testing-system-blueprint` 204/200 长期红灯。
    追查后确认是度量口径错，不是写得太长——三节是固定格式的契约样板，
    不消耗「判定点与指路」那份预算。
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def _skill(self, name, content_lines, kind="行为约束型"):
        d = self.root / name
        d.mkdir()
        head = ["---", "name: " + name, "metadata:", "  kind: " + kind, "---", ""]
        body = ["内容第 %d 行" % i for i in range(content_lines)]
        tail = ["## 上游产物", "表格", "## 下游消费者", "表格",
                "## 独立使用", "要你提供什么 / 能得到什么 / 得不到什么"]
        (d / "SKILL.md").write_text(NL.join(head + body + tail) + NL, encoding="utf-8")
        return d

    def test_content_over_ceiling_is_reported(self):
        self._skill("too-long", 210)
        found = C9SizeBudget().run(self.root)
        self.assertEqual(len(found), 1, "内容行真的超限时必须报")

    def test_contract_sections_do_not_count(self):
        """核心：内容在线内、加上三节后总行数超限——不得报错。

        这正是 OQ-M5 的形态：内容 196 行 ≤ 200，但整份文件 202 行，
        按总行数量就是红灯。frontmatter 仍计入内容——它不是契约样板。
        """
        d = self._skill("at-ceiling", 190)
        total = len((d / "SKILL.md").read_text(encoding="utf-8").splitlines())
        self.assertGreater(total, 200, "夹具必须真的按旧口径超限，否则测了个寂寞")
        self.assertEqual(C9SizeBudget().run(self.root), [],
                         "三节被计入了内容预算——正是 OQ-M5 那个口径错误")

    def test_executor_gets_higher_ceiling(self):
        self._skill("executor", 300, kind="流程执行器型")
        self.assertEqual(C9SizeBudget().run(self.root), [],
                         "流程执行器型上限是 350，不是 200")

    def test_reference_over_ceiling_is_reported(self):
        d = self._skill("big-ref", 10)
        (d / "references").mkdir()
        (d / "references" / "x.md").write_text(NL.join(["行"] * 410) + NL, encoding="utf-8")
        found = C9SizeBudget().run(self.root)
        self.assertTrue(any(f.key.startswith("c1.") or "x.md" in f.path for f in found),
                        "单个 references 超 400 行必须报")

    def test_normal_skill_is_silent(self):
        """负样本：正常体量的 Skill 不得被报。"""
        self._skill("normal", 120)
        self.assertEqual(C9SizeBudget().run(self.root), [])

class TestC10MatrixPathsInSkill(unittest.TestCase):
    """矩阵钉死的精确路径，必须出现在真正产出它的那个 SKILL.md 里。

    真实缺陷（验证 E）：矩阵钉了 8 个精确文件名作为唯一真相源，
    但只有 5 个出现在对应 SKILL.md 中。另外 3 个在 Skill 里是通配符
    （`02-*.md`）或自由文本（「MVP 收敛结果」）。

    **执行期 Agent 读的是 SKILL.md，不是矩阵。** 于是它按自己的理解取名，
    产出了 `02-核心机制.md`、`07-MVP收敛.md`——它没做错任何事。
    宪法原则 VII 说矩阵是唯一定义处，但没有机制把定义传导进执行路径。
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.matrix = self.root / "matrix.md"

    def _skill(self, name, produces_text):
        d = self.root / "skills" / name
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(
            NL.join(["---", "name: " + name, "metadata:",
                     "  produces:", "    - " + produces_text, "---", "",
                     "正文提到 " + produces_text]) + NL,
            encoding="utf-8")

    def _matrix(self, row):
        self.matrix.write_text(
            NL.join(["| Skill | 读取 | 写入 | 门禁 | 幂等 | 置信度 |",
                     "|---|---|---|---|---|---|", row]) + NL,
            encoding="utf-8")

    def test_wildcard_in_skill_is_reported(self):
        """正样本：矩阵钉死名字，Skill 只写通配符——必须报。"""
        self._skill("researcher", "specs/research/02-*.md")
        self._matrix("| `researcher` | x | `specs/research/02-关键资源与外部依赖.md`（新建） | 无 | 幂等 | 实测 |")
        found = C10MatrixPathsInSkill().run(self.root / "skills", self.matrix)
        self.assertEqual(len(found), 1)

    def test_exact_name_in_skill_is_clean(self):
        """负样本：Skill 写了精确名——不得报。"""
        self._skill("researcher", "specs/research/03-开源项目.md")
        self._matrix("| `researcher` | x | `specs/research/03-开源项目.md`（新建） | 无 | 幂等 | 实测 |")
        self.assertEqual(
            C10MatrixPathsInSkill().run(self.root / "skills", self.matrix), [])

    def test_free_text_in_skill_is_reported(self):
        self._skill("convergence", "MVP 收敛结果")
        self._matrix("| `convergence` | x | `specs/research/07-MVP收敛结果.md`（新建） | 无 | 幂等 | 实测 |")
        self.assertTrue(
            C10MatrixPathsInSkill().run(self.root / "skills", self.matrix))

    def test_placeholder_paths_are_skipped(self):
        """负样本：含 <占位符> 的路径无法逐字比对，不得报。"""
        self._skill("runner", "源码")
        self._matrix("| `runner` | x | `specs/<id>-<feature>/state.md`（覆盖） | 无 | 覆盖 | 实测 |")
        self.assertEqual(
            C10MatrixPathsInSkill().run(self.root / "skills", self.matrix), [])

    def test_missing_skill_dir_is_skipped(self):
        """负样本：矩阵里有行但 Skill 目录不存在（如 Phase 2 预留）——不得报。"""
        self._matrix("| `not-built-yet` | x | `specs/research/99-未来.md`（新建） | 无 | 幂等 | 推演 |")
        (self.root / "skills").mkdir()
        self.assertEqual(
            C10MatrixPathsInSkill().run(self.root / "skills", self.matrix), [])

class TestC2CrossRoot(unittest.TestCase):
    """C2 必须能跨目录比对——这是拆分中英文目录的前置条件。

    C2 是 Skill 结构的 zh/en 漂移探测器；C4/C5 分别守 evals 与 scripts/tests。
    Phase 3 把英文版搬到同级新目录后，同级关系消失，C2 会静默失效——
    而那恰好是漂移风险变大的时刻：两套目录、将来两个 repo、两条提交历史，
    改了一边忘了另一边**没有任何东西会喊**。

    所以先让它跨目录可用，再动布局。
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.zh = Path(self.tmp.name) / "zh" / "skills"
        self.en = Path(self.tmp.name) / "en" / "skills"
        self.zh.mkdir(parents=True)
        self.en.mkdir(parents=True)

    def _write(self, root, name, headings_n, refs=()):
        d = root / name
        d.mkdir()
        body = ["---", "name: " + name, "---"]
        body += ["## 节 %d" % i for i in range(headings_n)]
        (d / "SKILL.md").write_text(NL.join(body) + NL, encoding="utf-8")
        if refs:
            (d / "references").mkdir()
            for r in refs:
                (d / "references" / r).write_text("x" + NL, encoding="utf-8")

    def test_aligned_pair_across_roots_is_clean(self):
        """负样本：两边一致时，跨目录也不得报。"""
        self._write(self.zh, "foo", 5, ("a.md",))
        self._write(self.en, "foo-en", 5, ("a.md",))
        self.assertEqual(C2Pairing().run(self.zh, en_root=self.en), [])

    def test_heading_drift_across_roots_is_caught(self):
        self._write(self.zh, "foo", 8)
        self._write(self.en, "foo-en", 5)
        found = C2Pairing().run(self.zh, en_root=self.en)
        self.assertEqual(len(found), 1)
        self.assertEqual("c2.heading_count", found[0].key)

    def test_reference_drift_across_roots_is_caught(self):
        self._write(self.zh, "foo", 3, ("a.md", "b.md"))
        self._write(self.en, "foo-en", 3, ("a.md",))
        found = C2Pairing().run(self.zh, en_root=self.en)
        self.assertTrue(any(f.key == "c2.refs_mismatch" for f in found))

    def test_missing_en_twin_is_caught(self):
        """Phase 3 后，跨目录缺少整个配对 Skill 必须报错。"""
        self._write(self.zh, "foo", 3)
        found = C2Pairing().run(self.zh, en_root=self.en)
        self.assertTrue(any(f.key == "c2.missing_en_skill" for f in found))

    def test_same_root_behaviour_unchanged(self):
        """负样本：不传 en_root 时，行为与从前完全一致。"""
        self._write(self.zh, "foo", 8)
        self._write(self.zh, "foo-en", 5)
        found = C2Pairing().run(self.zh)
        self.assertEqual(len(found), 1, "同目录模式不得被跨目录改动搞坏")

class TestBilingualVocabulary(unittest.TestCase):
    """C7 / C8 按目录名后缀选用中文或英文词汇表（元数据标准 §5.0）。

    英文版若沿用中文节名，C3（中文残留）会报错；若各自发挥，C7/C8 就查不了。
    **规则一旦不可枚举，CI 就守不住**——所以词汇表必须双语定死，检查器认两套。
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def _skill(self, name, sections, questions, level="required", fallback=True):
        d = self.root / name
        d.mkdir()
        fb = ('      fallback: "degrade gracefully"' + NL) if fallback else ""
        fm = ["---", "name: " + name, "description: does a thing; do not use for other things",
              "metadata:", "  lang: en", "  requires:", '    - name: "upstream"',
              "      level: " + level]
        body = NL.join(fm) + NL + fb + "---" + NL + NL
        for s in sections:
            body += s + NL + "content" + NL
        body += NL.join(questions) + NL
        (d / "SKILL.md").write_text(body, encoding="utf-8")
        return d

    EN_SECTIONS = ("## Upstream Artifacts", "## Downstream Consumers", "## Standalone Use")
    EN_QUESTIONS = ("What you provide: a thing",
                    "What you get: another thing",
                    "What you don't get: the other thing")

    def test_english_sections_accepted_for_en_skill(self):
        """负样本：英文版用英文节名，不得被报缺章节。"""
        self._skill("foo-en", self.EN_SECTIONS, self.EN_QUESTIONS)
        self.assertEqual(C7StandaloneSection().run(self.root), [])

    def test_chinese_sections_rejected_for_en_skill(self):
        """英文版用中文节名——按英文词汇表就是缺章节。"""
        self._skill("foo-en", ("## 上游产物", "## 下游消费者", "## 独立使用"),
                    ("要你提供什么：x", "能得到什么：y", "得不到什么：z"))
        self.assertTrue(C7StandaloneSection().run(self.root))

    def test_chinese_sections_still_accepted_for_zh_skill(self):
        """负样本：中文版行为不得被这次改动搞坏。"""
        self._skill("foo", ("## 上游产物", "## 下游消费者", "## 独立使用"),
                    ("要你提供什么：x", "能得到什么：y", "得不到什么：z"))
        self.assertEqual(C7StandaloneSection().run(self.root), [])

    def test_english_questions_required_in_standalone(self):
        self._skill("foo-en", self.EN_SECTIONS, ("nothing useful here",))
        found = C7StandaloneSection().run(self.root)
        self.assertEqual(len(found), 3, "三问缺失应各报一条")

    def test_english_level_enum_accepted(self):
        """负样本：required / optional / orchestration 是合法英文取值。"""
        for lv in ("required", "optional", "orchestration"):
            with self.subTest(level=lv):
                import shutil
                if (self.root / "bar-en").exists():
                    shutil.rmtree(self.root / "bar-en")
                self._skill("bar-en", self.EN_SECTIONS, self.EN_QUESTIONS, level=lv)
                self.assertEqual(C8Requires().run(self.root), [])

    def test_chinese_level_rejected_for_en_skill(self):
        self._skill("foo-en", self.EN_SECTIONS, self.EN_QUESTIONS, level="必需")
        self.assertTrue(any(f.key == "c8.bad_level" for f in C8Requires().run(self.root)))

    def test_non_required_without_fallback_still_caught_in_english(self):
        self._skill("foo-en", self.EN_SECTIONS, self.EN_QUESTIONS,
                    level="optional", fallback=False)
        self.assertTrue(any(f.key == "c8.no_fallback" for f in C8Requires().run(self.root)))

class TestC2ReportsIncompleteDirs(unittest.TestCase):
    """英文版目录存在但没有 SKILL.md 时，C2 必须报告而不是崩溃。

    真实缺陷：并行执行者中途被会话上限打断，留下 5 个只有目录没有 SKILL.md 的
    半成品。C2 只判了 `is_dir()` 就去读文件，直接抛 FileNotFoundError——
    **一个崩溃的检查器比一个会报错的更糟**：它让整条检查链停在这里，
    后面的发现全都看不到了。
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def _zh(self, name, n=3):
        d = self.root / name
        d.mkdir()
        (d / "SKILL.md").write_text(
            NL.join(["## 节 %d" % i for i in range(n)]) + NL, encoding="utf-8")

    def test_en_dir_without_skill_md_is_reported(self):
        self._zh("foo")
        (self.root / "foo-en").mkdir()          # 空目录，无 SKILL.md
        found = C2Pairing().run(self.root)
        self.assertTrue(any(f.key == "c2.missing_en_skill" for f in found),
                        "半成品英文目录必须报告，而不是跳过或崩溃")

    def test_zh_dir_without_skill_md_is_reported(self):
        """反向：中文版侧缺 SKILL.md 必须报告且不得崩溃。"""
        (self.root / "bar").mkdir()
        (self.root / "bar-en").mkdir()
        (self.root / "bar-en" / "SKILL.md").write_text("## x" + NL, encoding="utf-8")
        found = C2Pairing().run(self.root)
        self.assertTrue(any(f.key == "c2.missing_zh_skill" for f in found))

    def test_complete_pair_still_compared(self):
        """负样本：两侧齐全时照常比对，不得被这次容错顺手放过。"""
        self._zh("baz", 5)
        d = self.root / "baz-en"
        d.mkdir()
        (d / "SKILL.md").write_text("## only one" + NL, encoding="utf-8")
        self.assertEqual(len(C2Pairing().run(self.root)), 1)

class TestMessageTable(unittest.TestCase):
    """用户可见文案双语，**一份实现**。

    宪法「单一实现优于双份脚本——双份必然漂移」。本项目亲眼见过：
    12 个英文 Skill 复制出去没人同步，攒下 931 行未翻译内容。
    而 C2 只比对 Skill、不比对工具——**工具漂移没有任何东西会喊**。
    所以检查器只有一份，把用户可见的串抽成表。
    """

    def setUp(self):
        self.addCleanup(set_language, "zh")

    def test_every_key_has_both_languages(self):
        missing = [k for k, v in MESSAGES.items() if set(v) != set(LANGS)]
        self.assertEqual(missing, [], "每条消息都必须两种语言齐全")

    def test_every_message_actually_renders(self):
        """光比对占位符集合不够——它只认 {word} 这种形状。

        `c8.rule` 的中文里有 `{必需, 可选增强, 编排级}`，是**字面**花括号，
        `\\w+` 匹配不到，于是两语言的占位符集合都是空集、比对通过；
        而 `.format()` 一渲染就 KeyError。它只在「有发现要输出」时才炸，
        全绿的跑法永远碰不到——**一个崩溃的检查器比会报错的更糟**。
        所以这条测试真的去渲染每一条。
        """
        for key, v in MESSAGES.items():
            names = set(re.findall(r"\{(\w+)\}", v["zh"]))
            for lang, s in v.items():
                with self.subTest(key=key, lang=lang):
                    s.format(**{n: "x" for n in names})

    def test_placeholders_match_across_languages(self):
        """占位符必须一致，否则切语言时会 KeyError —— 那是运行期才炸的错。"""
        bad = []
        for k, v in MESSAGES.items():
            names = {lang: set(re.findall(r"\{(\w+)\}", s)) for lang, s in v.items()}
            if len(set(map(frozenset, names.values()))) != 1:
                bad.append((k, names))
        self.assertEqual(bad, [], "同一 key 的各语言占位符必须完全一致")

    def test_no_cjk_in_english_messages(self):
        """负样本方向：英文文案里不得残留中文。"""
        bad = [k for k, v in MESSAGES.items() if CJK.search(v["en"])]
        self.assertEqual(bad, [])

    def test_language_switches_output(self):
        set_language("en")
        self.assertNotIn("断链", t("c1.broken_link", name="x.md"))
        self.assertIn("broken link", t("c1.broken_link", name="x.md"))
        set_language("zh")
        self.assertIn("断链", t("c1.broken_link", name="x.md"))

    def test_unknown_language_raises(self):
        """非法语言报错，不静默回退 —— 静默回退会让人以为设置生效了。"""
        with self.assertRaises(ValueError):
            set_language("de")
        self.assertEqual(current_language(), "zh", "报错后不得改变当前语言")

    def test_unknown_key_returns_the_key(self):
        """缺登记的 key 原样返回，不抛错 —— 检查器不该因一条文案没登记就跑不动。"""
        self.assertEqual(t("no.such.key"), "no.such.key")

    def test_language_is_never_inferred(self):
        """默认永远是 zh，不看环境变量 —— 与安装器的语言硬隔离同源。"""
        import os
        os.environ["LANG"] = "en_US.UTF-8"
        self.addCleanup(os.environ.pop, "LANG", None)
        import importlib
        import messages as m
        importlib.reload(m)
        self.assertEqual(m.current_language(), "zh")


class TestFindingCarriesKey(unittest.TestCase):
    """Finding 携带语言无关的 key，测试断言 key 而不是散文。

    断言在会被翻译的文案上本来就脆：改一个字就红一片，
    而那种红不指向任何真实缺陷。
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(set_language, "zh")
        self.root = Path(self.tmp.name)

    def test_finding_has_stable_key(self):
        d = self.root / "s"
        (d / "references").mkdir(parents=True)
        (d / "SKILL.md").write_text("see references/gone.md" + NL, encoding="utf-8")
        found = C1References().run(self.root)
        self.assertTrue(any(f.key == "c1.broken_link" for f in found),
                        "Finding 必须携带稳定的 key")

    def test_detail_follows_the_language(self):
        d = self.root / "s"
        (d / "references").mkdir(parents=True)
        (d / "SKILL.md").write_text("see references/gone.md" + NL, encoding="utf-8")
        set_language("en")
        found = C1References().run(self.root)
        self.assertIn("broken link", found[0].detail)
        self.assertEqual(found[0].key, "c1.broken_link", "key 不随语言变化")

if __name__ == "__main__":
    unittest.main(verbosity=2)
