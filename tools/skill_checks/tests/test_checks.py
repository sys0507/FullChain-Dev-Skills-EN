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
import sys
import tempfile
import unittest
from pathlib import Path

NL = chr(10)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

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
from common import headings, normalize, section, strip_fences  # noqa: E402

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
        self.assertTrue(any("断链" in f.detail for f in found))

    def test_positive_orphan_file(self):
        make(self.root, "a", refs={"unused.md": "x"})
        found = C1References().run(self.root)
        self.assertTrue(any("孤儿" in f.detail for f in found))

    def test_positive_subdir_under_references(self):
        """真实缺陷：evals 被放进了 references/ 下。"""
        d = make(self.root, "a", refs={"used.md": "x"})
        (d / "references" / "evals").mkdir()
        (d / "SKILL.md").write_text((d / "SKILL.md").read_text(encoding="utf-8")
                                    + "\n见 `references/used.md`\n", encoding="utf-8")
        found = C1References().run(self.root)
        self.assertTrue(any("子目录" in f.detail for f in found))

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
        self.assertTrue(any("标题数不等" in f.detail for f in found))

    def test_positive_references_mismatch(self):
        make(self.root, "a", body=GOOD_SECTIONS + "\n见 `references/x.md`\n",
             refs={"x.md": "1"})
        make(self.root, "a-en")
        found = C2Pairing().run(self.root)
        self.assertTrue(any("references 集合不等" in f.detail for f in found))

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

    def test_negative_no_en_version(self):
        """英文版尚未复刻属预期，不报。"""
        make(self.root, "a")
        self.assertEqual(C2Pairing().run(self.root), [])


# ---------------------------------------------------------------- C3

class TestC3EnPurity(Base):
    """正样本取自真实缺陷：英文版正文引用了中文文件名。"""

    def test_positive_chinese_in_en(self):
        make(self.root, "a-en", fm=EN_FM,
             body=EN_SECTIONS + "\nSee `specs/research/00-项目输入与假设.md`\n")
        found = C3EnPurity().run(self.root)
        self.assertTrue(any("中文残留" in f.detail for f in found))

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
        self.assertTrue(any("skill_name" in f.detail for f in found))

    def test_positive_chinese_prompt(self):
        make(self.root, "a-en",
             evals={"skill_name": "a-en", "evals": [{"id": 1, "prompt": "帮我生成"}]})
        found = C4EnEvals().run(self.root)
        self.assertTrue(any("prompt 含中文" in f.detail for f in found))

    def test_negative_clean_en_evals(self):
        make(self.root, "a-en",
             evals={"skill_name": "a-en", "evals": [{"id": 1, "prompt": "Generate it"}]})
        self.assertEqual(C4EnEvals().run(self.root), [])

    def test_negative_no_evals_dir(self):
        make(self.root, "a-en")
        self.assertEqual(C4EnEvals().run(self.root), [])


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
        self.assertTrue(any("缺章节 ## 独立使用" in f.detail for f in found))

    def test_positive_missing_question(self):
        body = GOOD_SECTIONS.replace("**得不到什么**：不做上游的事。", "")
        make(self.root, "a", body=body)
        found = C7StandaloneSection().run(self.root)
        self.assertTrue(any("得不到什么" in f.detail for f in found))

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
        self.assertTrue(any("取值非法" in f.detail for f in found))

    def test_positive_optional_without_fallback(self):
        fm = GOOD_FM.replace('      fallback: "请用户直接提供"\n', "")
        make(self.root, "a", fm=fm)
        found = C8Requires().run(self.root)
        self.assertTrue(any("缺 fallback" in f.detail for f in found))

    def test_positive_missing_lang(self):
        fm = GOOD_FM.replace("  lang: zh\n", "")
        make(self.root, "a", fm=fm)
        found = C8Requires().run(self.root)
        self.assertTrue(any("缺 lang" in f.detail for f in found))

    def test_positive_no_anti_trigger(self):
        fm = GOOD_FM.replace("不用于：别的事情。", "")
        make(self.root, "a", fm=fm)
        found = C8Requires().run(self.root)
        self.assertTrue(any("反触发" in f.detail for f in found))

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
        self.assertTrue(any("references" in f.detail or "x.md" in f.path for f in found),
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

    C2 是**唯一**的 zh/en 漂移探测器，靠比较同级 `foo` 与 `foo-en` 工作。
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
        self.assertIn("标题数不等", found[0].detail)

    def test_reference_drift_across_roots_is_caught(self):
        self._write(self.zh, "foo", 3, ("a.md", "b.md"))
        self._write(self.en, "foo-en", 3, ("a.md",))
        found = C2Pairing().run(self.zh, en_root=self.en)
        self.assertTrue(any("references" in f.detail for f in found))

    def test_missing_en_twin_is_still_skipped(self):
        """负样本：英文版尚未复刻属预期，跨目录时同样不报。"""
        self._write(self.zh, "foo", 3)
        self.assertEqual(C2Pairing().run(self.zh, en_root=self.en), [])

    def test_same_root_behaviour_unchanged(self):
        """负样本：不传 en_root 时，行为与从前完全一致。"""
        self._write(self.zh, "foo", 8)
        self._write(self.zh, "foo-en", 5)
        found = C2Pairing().run(self.zh)
        self.assertEqual(len(found), 1, "同目录模式不得被跨目录改动搞坏")

if __name__ == "__main__":
    unittest.main(verbosity=2)
