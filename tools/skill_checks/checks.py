"""8 项检查。

前 5 项守存量结构（各自曾抓出过真实缺陷），后 3 项守独立可用性（对应硬规则 R1/R2/R3）。

每项都用 common.py 的工具，不各写一套匹配逻辑——
本项目 5 次自检误报的成因全部集中在匹配方式上。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from common import (
    CJK,
    Check,
    Finding,
    description,
    frontmatter,
    headings,
    logical_skills,
    section,
    strip_fences,
)

# 刻意保留的双语触发词白名单：标注为参考用途的中文触发词
BILINGUAL_MARKERS = ("(for reference)", "Chinese (for reference)", "（参考）")


class C1References(Check):
    """references 链接可解析且无孤儿。抓出过：3 处断链、1 个空 evals 目录。"""

    name = "C1-references"
    rule_key = "c1.rule"

    def run(self, root: Path) -> list[Finding]:
        out = []
        for d in sorted(p for p in root.iterdir() if p.is_dir()):
            sp = d / "SKILL.md"
            if not sp.is_file():
                continue
            text = sp.read_text(encoding="utf-8")
            cited = set(re.findall(r"references/([A-Za-z0-9._-]+\.md)", text))
            rd = d / "references"
            actual = {f.name for f in rd.iterdir() if f.is_file()} if rd.is_dir() else set()
            for miss in sorted(cited - actual):
                out.append(Finding(self.name, f"{d.name}/SKILL.md", "c1.broken_link", name=miss))
            for orphan in sorted(actual - cited):
                out.append(Finding(self.name, f"{d.name}/references/{orphan}", "c1.orphan"))
            if rd.is_dir():
                for sub in rd.iterdir():
                    if sub.is_dir():
                        out.append(Finding(self.name, f"{d.name}/references/{sub.name}",
                                           "c1.subdir"))
        return out


class C2Pairing(Check):
    """zh/en 配对一致。抓出过：一个英文版比中文版多 5 节的结构漂移。

    标题统计必须剔除围栏 —— 未剔除时曾把提示词正文里的 ## 误计为标题。
    """

    name = "C2-pairing"
    rule_key = "c2.rule"
    phase = 3  # 中文版已补三节，英文版复刻属 Phase 3；此前必然不等

    def run(self, root: Path, en_root: Path | None = None) -> list[Finding]:
        """`en_root` 缺省时在同目录找 `<name>-en`；给定时去那个目录找。

        Phase 3 把英文版搬到同级新目录后，同级关系消失。C2 是**唯一**的
        zh/en 漂移探测器，同级关系一断它就静默失效——而那恰好是漂移
        风险变大的时刻。跨目录能力是拆分布局的前置条件，不是可选项。
        """
        out = []
        base = en_root if en_root is not None else root
        for d in logical_skills(root):
            en = base / (d.name + "-en")
            # 目录在但 SKILL.md 还没写，属尚未落地——与目录不存在同等对待。
            # 只判 is_dir() 会在半成品目录上抛 FileNotFoundError，
            # 而一个崩溃的检查器比一个会报错的更糟：它让后面的发现全看不到。
            if not (en / "SKILL.md").is_file() or not (d / "SKILL.md").is_file():
                continue
            hz = headings((d / "SKILL.md").read_text(encoding="utf-8"))
            he = headings((en / "SKILL.md").read_text(encoding="utf-8"))
            if len(hz) != len(he):
                out.append(Finding(self.name, d.name, "c2.heading_count",
                                   zh=len(hz), en=len(he)))
            rz = {f.name for f in (d / "references").iterdir()} if (d / "references").is_dir() else set()
            re_ = {f.name for f in (en / "references").iterdir()} if (en / "references").is_dir() else set()
            if rz != re_:
                out.append(Finding(self.name, d.name, "c2.refs_mismatch",
                                   only_zh=sorted(rz - re_), only_en=sorted(re_ - rz)))
        return out


class C3EnPurity(Check):
    """英文版正文无中文残留。抓出过：英文版引用中文文件名。

    必须用 Unicode 码点区间 —— 字节区间会把 — 和 → 也算成中文。
    """

    name = "C3-en-purity"
    rule_key = "c3.rule"

    def run(self, root: Path) -> list[Finding]:
        out = []
        for d in sorted(p for p in root.iterdir() if p.is_dir() and p.name.endswith("-en")):
            for f in sorted(d.rglob("*.md")):
                text = f.read_text(encoding="utf-8")
                for i, line in enumerate(text.splitlines(), 1):
                    if CJK.search(line) and not any(m in line for m in BILINGUAL_MARKERS):
                        # 白名单：紧邻上一行标注了参考用途
                        prev = text.splitlines()[i - 2] if i >= 2 else ""
                        if any(m in prev for m in BILINGUAL_MARKERS):
                            continue
                        out.append(Finding(self.name,
                                           f"{d.name}/{f.relative_to(d)}:{i}",
                                           "c3.residue", line=line.strip()[:50]))
        return out


class C4EnEvals(Check):
    """英文版 evals 标识正确且 prompt 无中文。抓出过：英文版 evals 是中文版逐字节副本。

    这项最容易漏 —— evals 不在 SKILL.md 里，人工 review 看不见。
    """

    name = "C4-en-evals"
    rule_key = "c4.rule"

    def run(self, root: Path) -> list[Finding]:
        out = []
        for d in sorted(p for p in root.iterdir() if p.is_dir() and p.name.endswith("-en")):
            ep = d / "evals" / "evals.json"
            if not ep.is_file():
                continue
            data = json.loads(ep.read_text(encoding="utf-8"))
            if not str(data.get("skill_name", "")).endswith("-en"):
                out.append(Finding(self.name, f"{d.name}/evals/evals.json",
                                   "c4.name_missing_en", actual=repr(data.get("skill_name"))))
            for item in data.get("evals", []):
                if CJK.search(str(item.get("prompt", ""))):
                    out.append(Finding(self.name, f"{d.name}/evals/evals.json",
                                       "c4.prompt_cjk", id=item.get("id")))
        return out


class C5ScriptsNeedTests(Check):
    """带 scripts 的 Skill 必须有 tests。抓出过：一个带 15 个脚本却无测试的 Skill。"""

    name = "C5-scripts-tests"
    rule_key = "c5.rule"

    def run(self, root: Path) -> list[Finding]:
        out = []
        for d in sorted(p for p in root.iterdir() if p.is_dir()):
            if (d / "scripts").is_dir() and not (d / "tests").is_dir():
                out.append(Finding(self.name, d.name, "c5.no_tests"))
        return out


class C6SelfContained(Check):
    """R1 目录自包含。现状零违规，本项是防退化。

    按名软引用不违反 R1 —— 它不产生文件系统耦合。
    """

    name = "C6-self-contained"
    rule_key = "c6.rule"

    PAT = re.compile(r"(\.\./[A-Za-z0-9_-]+/|Assets/skills/|~/Assets/skills)")

    def run(self, root: Path) -> list[Finding]:
        out = []
        for d in sorted(p for p in root.iterdir() if p.is_dir()):
            for f in sorted(list(d.rglob("*.md")) + list(d.rglob("*.json"))):
                text = f.read_text(encoding="utf-8")
                for m in self.PAT.finditer(text):
                    out.append(Finding(self.name, f"{d.name}/{f.relative_to(d)}",
                                       "c6.cross_ref",
                                       snippet=repr(text[m.start():m.start() + 40])))
        return out


class C7StandaloneSection(Check):
    """R2 输入可替代。三节齐全，且「独立使用」含三问。"""

    name = "C7-standalone"
    rule_key = "c7.rule"

    #: 双语词汇表的唯一定义处是 docs/skill-metadata-standard.md §5.0。
    #: 英文版沿用中文节名会被 C3 判为中文残留；各自发挥则 C7 查不了——
    #: 规则一旦不可枚举，CI 就守不住。故两套都认，按目录后缀选。
    SECTIONS = ("## 上游产物", "## 下游消费者", "## 独立使用")
    QUESTIONS = ("要你提供什么", "能得到什么", "得不到什么")
    SECTIONS_EN = ("## Upstream Artifacts", "## Downstream Consumers", "## Standalone Use")
    QUESTIONS_EN = ("What you provide", "What you get", "What you don't get")

    def run(self, root: Path) -> list[Finding]:
        out = []
        for d in sorted(p for p in root.iterdir() if p.is_dir()):
            sp = d / "SKILL.md"
            if not sp.is_file():
                continue
            en = d.name.endswith("-en")
            sections = self.SECTIONS_EN if en else self.SECTIONS
            questions = self.QUESTIONS_EN if en else self.QUESTIONS
            text = sp.read_text(encoding="utf-8")
            body = strip_fences(text)
            for sec in sections:
                if sec not in body:
                    out.append(Finding(self.name, f"{d.name}/SKILL.md", "c7.missing_section", section=sec))
            # 切片后再找三问，避免命中别处
            standalone = section(text, sections[2])
            if standalone:
                for q in questions:
                    if q not in standalone:
                        out.append(Finding(self.name, f"{d.name}/SKILL.md", "c7.missing_question",
                                           section=sections[2], question=q))
        return out


class C8Requires(Check):
    """R3 依赖显式分级。级别取值封闭，非必需项必须有 fallback。"""

    name = "C8-requires"
    rule_key = "c8.rule"

    #: 双语枚举，定义处见 docs/skill-metadata-standard.md §5.0
    LEVELS = {"必需", "可选增强", "编排级"}
    LEVELS_EN = {"required", "optional", "orchestration"}
    REQUIRED = {"必需", "required"}
    ANTI = ("不用于", "不负责", "不做")
    ANTI_EN = ("do not use", "not for", "does not")

    def run(self, root: Path) -> list[Finding]:
        out = []
        for d in sorted(p for p in root.iterdir() if p.is_dir()):
            sp = d / "SKILL.md"
            if not sp.is_file():
                continue
            levels = self.LEVELS_EN if d.name.endswith("-en") else self.LEVELS
            fm = frontmatter(sp.read_text(encoding="utf-8"))
            if not fm:
                out.append(Finding(self.name, f"{d.name}/SKILL.md", "c8.no_frontmatter"))
                continue
            if not re.search(r"^\s*lang:\s*\S+", fm, re.M):
                out.append(Finding(self.name, f"{d.name}/SKILL.md", "c8.no_lang"))
            if "requires:" not in fm:
                out.append(Finding(self.name, f"{d.name}/SKILL.md", "c8.no_requires"))
                continue
            block = fm.split("requires:", 1)[1]
            entries = re.split(r"\n\s*- name:", block)[1:]
            for e in entries:
                lv = re.search(r"level:\s*(\S+)", e)
                if not lv:
                    out.append(Finding(self.name, f"{d.name}/SKILL.md", "c8.no_level"))
                    continue
                if lv.group(1) not in levels:
                    out.append(Finding(self.name, f"{d.name}/SKILL.md",
                                       "c8.bad_level", value=repr(lv.group(1))))
                elif lv.group(1) not in self.REQUIRED and "fallback:" not in e:
                    out.append(Finding(self.name, f"{d.name}/SKILL.md",
                                       "c8.no_fallback", level=lv.group(1)))
            desc = description(fm)
            anti = self.ANTI_EN if d.name.endswith("-en") else self.ANTI
            if not any(k in desc.lower() if d.name.endswith("-en") else k in desc
                       for k in anti):
                out.append(Finding(self.name, f"{d.name}/SKILL.md", "c8.no_anti_trigger"))
        return out


class C9SizeBudget(Check):
    """体量上限**只计内容行**，双模式契约三节不计入（宪法 1.1.0）。

    OQ-M5：两个 Skill 长期红灯，追查后是度量口径错，不是写得太长。
    上限保护的是「判定点与指路」那份预算；三节是固定格式的契约样板，
    不消耗那份预算，把它们计进去等于量错了对象。

    `metadata.kind` 缺省时按宽松上限（350）判。没有声明 kind 的 Skill，
    检查器无从知道它该守 200 还是 350——只能守外沿，不臆测。
    """

    name = "C9-size-budget"
    rule_key = "c9.rule"

    CEILINGS = {"行为约束型": 200, "流程执行器型": 350}
    DEFAULT_CEILING = 350
    CONTRACT_START = "## 上游产物"
    REFERENCE_CEILING = 400

    def run(self, root: Path) -> list[Finding]:
        out = []
        for d in sorted(p for p in root.iterdir() if p.is_dir()):
            sp = d / "SKILL.md"
            if not sp.is_file():
                continue
            text = sp.read_text(encoding="utf-8")
            head, _, _ = text.partition(self.CONTRACT_START)
            content = len(head.splitlines())
            kind = re.search(r"^\s*kind:\s*(\S+)", frontmatter(text), re.M)
            ceiling = self.CEILINGS.get(kind.group(1) if kind else "", self.DEFAULT_CEILING)
            if content > ceiling:
                out.append(Finding(self.name, f"{d.name}/SKILL.md",
                                   "c9.over_ceiling", lines=content, ceiling=ceiling))
            for ref in sorted((d / "references").glob("*.md")) if (d / "references").is_dir() else []:
                n = len(ref.read_text(encoding="utf-8").splitlines())
                if n > self.REFERENCE_CEILING:
                    out.append(Finding(self.name, f"{d.name}/references/{ref.name}", "c9.ref_over_ceiling",
                                       lines=n, ceiling=self.REFERENCE_CEILING))
        return out


class C10MatrixPathsInSkill(Check):
    """矩阵钉死的精确路径，必须出现在真正产出它的那个 SKILL.md 里。

    验证 E 查出：矩阵钉了 8 个精确文件名作为唯一真相源，只有 5 个出现在
    对应 SKILL.md 中；其余是通配符（`02-*.md`）或自由文本（「MVP 收敛结果」）。

    **执行期 Agent 读的是 SKILL.md，不是矩阵。** 缺的那几个里，
    有两个正好被真实运行改了名——它按自己的理解取名，没做错任何事。
    宪法原则 VII 说矩阵是唯一定义处，但**没有机制把定义传导进执行路径**。
    这个检查就是那个机制。

    含 `<占位符>` 的路径无法逐字比对，跳过；矩阵有行但 Skill 目录不存在
    （Phase 预留）也跳过。
    """

    name = "C10-matrix-paths"
    rule_key = "c10.rule"
    DEFAULT_MATRIX = Path("docs/stage-artifact-contract.md")
    #: 只查写入列里的精确文件路径
    CELL = re.compile(r"`([^`<>*]+?\.(?:md|json|yml|yaml))`")

    def run(self, root: Path, matrix: Path | None = None) -> list[Finding]:
        mp = matrix or self.DEFAULT_MATRIX
        if not mp.is_file():
            return []
        out = []
        for line in mp.read_text(encoding="utf-8").splitlines():
            if not line.startswith("| `"):
                continue
            cells = [c.strip() for c in line.split("|")]
            if len(cells) < 5:
                continue
            name = cells[1].strip("` ")
            skill = root / name
            sp = skill / "SKILL.md"
            if not sp.is_file():
                continue  # Phase 预留行，或英文版未复刻
            text = sp.read_text(encoding="utf-8")
            written = cells[3] if len(cells) > 3 else ""
            for path in self.CELL.findall(written):
                if path.rsplit("/", 1)[-1] in text:
                    continue
                out.append(Finding(self.name, f"{name}/SKILL.md", "c10.path_missing", path=path))
        return out


ALL_CHECKS: list[Check] = [
    C1References(), C2Pairing(), C3EnPurity(), C4EnEvals(),
    C5ScriptsNeedTests(), C6SelfContained(), C7StandaloneSection(), C8Requires(),
    C9SizeBudget(), C10MatrixPathsInSkill(),
]
