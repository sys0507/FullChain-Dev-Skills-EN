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

# 这些文本格式会直接参与 Skill 运行、示例或用户界面，均受英文纯度约束。
EN_TEXT_SUFFIXES = {
    ".css", ".html", ".js", ".json", ".md", ".py", ".sh", ".toml",
    ".ts", ".tsx", ".txt", ".yaml", ".yml",
}

# 当前无配对豁免。保留封闭集合，未来若有经书面批准的分期项，可显式登记。
PAIRING_EXEMPT_ZH: set[str] = set()


def _relative_files(directory: Path) -> set[str]:
    """返回目录内递归文件集合；目录不存在等价于空集合。"""
    if not directory.is_dir():
        return set()
    return {
        p.relative_to(directory).as_posix()
        for p in directory.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
    }


def _produces_count(text: str) -> int:
    """统计 frontmatter 中 metadata.produces 的列表项数量。"""
    fm = frontmatter(text)
    match = re.search(r"^  produces:\s*\n((?:    - .*(?:\n|$))*)", fm, re.M)
    return len(re.findall(r"^    - ", match.group(1), re.M)) if match else 0


def _frontmatter_keys(text: str) -> tuple[set[str], set[str]]:
    """Return top-level and metadata key sets from the constrained Skill schema."""
    top: set[str] = set()
    metadata: set[str] = set()
    in_metadata = False
    for line in frontmatter(text).splitlines():
        top_match = re.match(r"^([a-z][a-z0-9-]*):", line)
        if top_match:
            key = top_match.group(1)
            top.add(key)
            in_metadata = key == "metadata"
            continue
        if in_metadata:
            metadata_match = re.match(r"^  ([a-z][a-z0-9-]*):", line)
            if metadata_match:
                metadata.add(metadata_match.group(1))
    return top, metadata


def _scalar(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", frontmatter(text), re.M)
    return match.group(1).strip("\"'") if match else None


def _metadata_list(text: str, key: str) -> list[str]:
    fm = frontmatter(text)
    match = re.search(
        rf"^  {re.escape(key)}:\s*\n((?:(?:    |      ).*(?:\n|$))*)", fm, re.M)
    if not match:
        return []
    return [
        item.strip().strip("\"'")
        for item in re.findall(r"^    -\s+(.*)$", match.group(1), re.M)
    ]


def _requires_shape(text: str) -> list[tuple[str | None, bool]]:
    """Return ordered (normalised level, has-fallback) entries, ignoring translated names."""
    levels = {"必需": "required", "可选增强": "optional", "编排级": "orchestration"}
    fm = frontmatter(text)
    match = re.search(r"^  requires:\s*\n((?:(?:    |      ).*(?:\n|$))*)", fm, re.M)
    if not match:
        return []
    blocks = re.split(r"(?=^    -\s+name:)", match.group(1), flags=re.M)
    shape = []
    for block in blocks:
        if not re.match(r"^    -\s+name:", block):
            continue
        level_match = re.search(r"^      level:\s*(.*?)\s*$", block, re.M)
        level = level_match.group(1).strip("\"'") if level_match else None
        shape.append((levels.get(level, level), bool(re.search(r"^      fallback:", block, re.M))))
    return shape


def _path_translation(matrix: Path | None) -> dict[str, str]:
    """Read the zh->en path map from the contract matrix, its sole definition site."""
    if matrix is None or not matrix.is_file():
        return {}
    text = matrix.read_text(encoding="utf-8")
    marker = "## 3.5 "
    if marker not in text:
        return {}
    section_text = text.split(marker, 1)[1]
    next_heading = re.search(r"\n## ", section_text)
    if next_heading:
        section_text = section_text[:next_heading.start()]
    return dict(re.findall(r"^\| `([^`]+)` \| `([^`]+)` \|$", section_text, re.M))


def _produces_paths(text: str) -> list[str]:
    """Keep machine-addressable outputs; translated prose outputs are covered by item count."""
    return [item for item in _metadata_list(text, "produces")
            if "/" in item or re.search(r"(?:^|[.])[A-Za-z0-9_-]+$", item)]


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

    def run(self, root: Path, en_root: Path | None = None,
            matrix: Path | None = None) -> list[Finding]:
        """`en_root` 缺省时在同目录找 `<name>-en`；给定时去那个目录找。

        Phase 3 把英文版搬到同级新目录后，同级关系消失。C2 守 Skill 结构，
        C4/C5 分别守 evals 与 scripts/tests；三者都必须显式接收第二个根目录，
        否则会在漂移风险变大时静默失效。
        """
        out = []
        base = en_root if en_root is not None else root
        translations = _path_translation(matrix)
        reverse_translations = {en: zh for zh, en in translations.items()}
        zh_dirs = logical_skills(root)
        for d in zh_dirs:
            if d.name in PAIRING_EXEMPT_ZH:
                continue
            en = base / (d.name + "-en")
            zh_skill = d / "SKILL.md"
            en_skill = en / "SKILL.md"
            if not zh_skill.is_file():
                out.append(Finding(self.name, d.name, "c2.missing_zh_skill"))
                continue
            if not en_skill.is_file():
                # 单语树不猜另一棵树的位置；显式跨树，或已经出现半成品配对目录时才报。
                if en_root is not None or en.exists():
                    out.append(Finding(self.name, d.name, "c2.missing_en_skill"))
                continue
            zh_text = zh_skill.read_text(encoding="utf-8")
            en_text = en_skill.read_text(encoding="utf-8")
            zh_top, zh_meta = _frontmatter_keys(zh_text)
            en_top, en_meta = _frontmatter_keys(en_text)
            # Names, descriptions, and language values must differ by design; their keys must exist.
            if zh_top != en_top:
                out.append(Finding(self.name, d.name, "c2.top_keys",
                                   only_zh=sorted(zh_top - en_top),
                                   only_en=sorted(en_top - zh_top)))
            if zh_meta != en_meta:
                out.append(Finding(self.name, d.name, "c2.metadata_keys",
                                   only_zh=sorted(zh_meta - en_meta),
                                   only_en=sorted(en_meta - zh_meta)))
            zh_tools, en_tools = _scalar(zh_text, "allowed-tools"), _scalar(en_text, "allowed-tools")
            if zh_tools != en_tools:
                out.append(Finding(self.name, d.name, "c2.allowed_tools",
                                   zh=zh_tools, en=en_tools))
            zh_requires, en_requires = _requires_shape(zh_text), _requires_shape(en_text)
            if len(zh_requires) != len(en_requires):
                out.append(Finding(self.name, d.name, "c2.requires_count",
                                   zh=len(zh_requires), en=len(en_requires)))
            elif zh_requires != en_requires:
                out.append(Finding(self.name, d.name, "c2.requires_structure",
                                   zh=zh_requires, en=en_requires))
            hz = headings(zh_text)
            he = headings(en_text)
            if len(hz) != len(he):
                out.append(Finding(self.name, d.name, "c2.heading_count",
                                   zh=len(hz), en=len(he)))
            rz = {f.name for f in (d / "references").iterdir()} if (d / "references").is_dir() else set()
            re_ = {f.name for f in (en / "references").iterdir()} if (en / "references").is_dir() else set()
            if rz != re_:
                out.append(Finding(self.name, d.name, "c2.refs_mismatch",
                                   only_zh=sorted(rz - re_), only_en=sorted(re_ - rz)))
            az = _relative_files(d / "assets")
            ae = _relative_files(en / "assets")
            if az != ae:
                out.append(Finding(self.name, d.name, "c2.assets_mismatch",
                                   only_zh=sorted(az - ae), only_en=sorted(ae - az)))
            pz, pe = _produces_count(zh_text), _produces_count(en_text)
            if pz != pe:
                out.append(Finding(self.name, d.name, "c2.produces_count", zh=pz, en=pe))
            zh_paths = _produces_paths(zh_text)
            en_paths = [reverse_translations.get(path, path) for path in _produces_paths(en_text)]
            if zh_paths != en_paths:
                out.append(Finding(self.name, d.name, "c2.produces_paths",
                                   zh=zh_paths, en=_produces_paths(en_text)))

        # 反向守门：英文树多出 Skill，或中文半成品目录缺 SKILL.md，也不能静默跳过。
        en_dirs = sorted(p for p in base.iterdir() if p.is_dir() and p.name.endswith("-en"))
        for en in en_dirs if (en_root is not None or zh_dirs) else []:
            zh_name = en.name[:-3]
            if zh_name in PAIRING_EXEMPT_ZH:
                continue
            zh = root / zh_name
            if not (zh / "SKILL.md").is_file() and not any(
                    f.path == zh_name and f.key == "c2.missing_zh_skill" for f in out):
                out.append(Finding(self.name, zh_name, "c2.missing_zh_skill"))
        return out


class C3EnPurity(Check):
    """英文版文本产物无中文残留。抓出过：英文版引用中文文件名。

    必须用 Unicode 码点区间 —— 字节区间会把 — 和 → 也算成中文。
    """

    name = "C3-en-purity"
    rule_key = "c3.rule"

    def run(self, root: Path) -> list[Finding]:
        out = []
        for d in sorted(p for p in root.iterdir() if p.is_dir() and p.name.endswith("-en")):
            for f in sorted(p for p in d.rglob("*")
                            if p.is_file() and p.suffix.lower() in EN_TEXT_SUFFIXES):
                text = f.read_text(encoding="utf-8")
                lines = text.splitlines()
                for i, line in enumerate(lines, 1):
                    if CJK.search(line) and not any(m in line for m in BILINGUAL_MARKERS):
                        # 白名单：紧邻上一行标注了参考用途
                        prev = lines[i - 2] if i >= 2 else ""
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

    def run(self, root: Path, en_root: Path | None = None) -> list[Finding]:
        out = []
        english_root = en_root if en_root is not None else root
        if en_root is not None:
            for zh in logical_skills(root):
                if zh.name in PAIRING_EXEMPT_ZH:
                    continue
                en = english_root / (zh.name + "-en")
                if not (zh / "SKILL.md").is_file() or not (en / "SKILL.md").is_file():
                    continue  # C2 负责报告整项 Skill 缺失。
                zf = _relative_files(zh / "evals")
                ef = _relative_files(en / "evals")
                if zf != ef:
                    out.append(Finding(self.name, zh.name, "c4.files_mismatch",
                                       only_zh=sorted(zf - ef), only_en=sorted(ef - zf)))
                    continue
                zh_evals = zh / "evals" / "evals.json"
                en_evals = en / "evals" / "evals.json"
                if zh_evals.is_file() and en_evals.is_file():
                    zh_items = json.loads(zh_evals.read_text(encoding="utf-8")).get("evals", [])
                    en_items = json.loads(en_evals.read_text(encoding="utf-8")).get("evals", [])
                    zh_sequence = [(item.get("id"), item.get("name")) for item in zh_items]
                    en_sequence = [(item.get("id"), item.get("name")) for item in en_items]
                    if zh_sequence != en_sequence:
                        out.append(Finding(self.name, zh.name, "c4.eval_sequence",
                                           zh=zh_sequence, en=en_sequence))
                        continue
                    for zh_item, en_item in zip(zh_items, en_items):
                        zh_count = len(zh_item.get("assertions", []))
                        en_count = len(en_item.get("assertions", []))
                        if zh_count != en_count:
                            out.append(Finding(self.name, zh.name, "c4.assertion_count",
                                               id=zh_item.get("id"), zh=zh_count, en=en_count))
        for d in sorted(p for p in english_root.iterdir()
                        if p.is_dir() and p.name.endswith("-en")):
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

    def run(self, root: Path, en_root: Path | None = None) -> list[Finding]:
        out = []
        roots = [root] + ([en_root] if en_root is not None else [])
        for current in roots:
            for d in sorted(p for p in current.iterdir() if p.is_dir()):
                if (d / "scripts").is_dir() and not (d / "tests").is_dir():
                    out.append(Finding(self.name, d.name, "c5.no_tests"))
        if en_root is not None:
            for zh in logical_skills(root):
                if zh.name in PAIRING_EXEMPT_ZH:
                    continue
                en = en_root / (zh.name + "-en")
                if not (zh / "SKILL.md").is_file() or not (en / "SKILL.md").is_file():
                    continue  # C2 负责报告整项 Skill 缺失。
                for bundle in ("scripts", "tests"):
                    zf = _relative_files(zh / bundle)
                    ef = _relative_files(en / bundle)
                    if zf != ef:
                        out.append(Finding(self.name, zh.name, "c5.bundle_mismatch",
                                           bundle=bundle, only_zh=sorted(zf - ef),
                                           only_en=sorted(ef - zf)))
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
            # 静默返回空等于「本项通过」——而它其实一次都没跑。
            # 英文库没有矩阵副本，这个分支让 C10 在那边空绿了整个 Phase 3。
            # 宪法原则 IV：走了兜底路径必须显式标注，不得静默降级。
            return [Finding(self.name, str(mp), "c10.no_matrix", path=mp)]
        text_all = mp.read_text(encoding="utf-8")
        #: §3.5 的中→英路径映射，矩阵是它的唯一定义处（宪法 VII）
        _pairs = re.findall(r"^\| `(specs/[^`]+)` \| `(specs/[^`]+)` \|$", text_all, re.M)
        # 同时按完整路径和裸文件名建键——矩阵的写入列两种写法都有，
        # 只按完整路径建键会漏掉裸文件名那几行，而漏掉的表现是「报中文名找不到」，
        # 看起来像英文版缺了产出，其实是映射没命中。
        xlate = {}
        for zh_path, en_path in _pairs:
            xlate[zh_path] = en_path
            xlate[zh_path.rsplit("/", 1)[-1]] = en_path.rsplit("/", 1)[-1]
        out = []
        for line in text_all.splitlines():
            if not line.startswith("| `"):
                continue
            cells = [c.strip() for c in line.split("|")]
            if len(cells) < 5:
                continue
            zh_name = cells[1].strip("` ")
            # 英文树里 Skill 叫 <name>-en，产出也是 §3.5 右列的英文名。
            # 不做这两步映射，每一行都会因「目录不存在」而 continue——
            # C10 就在英文树里空绿了整个 Phase 3，看起来和真通过一模一样。
            for name, translate in ((zh_name, False), (zh_name + "-en", True)):
                sp = root / name / "SKILL.md"
                if not sp.is_file():
                    continue  # Phase 预留行，或该语言未复刻
                text = sp.read_text(encoding="utf-8")
                written = cells[3] if len(cells) > 3 else ""
                for path in self.CELL.findall(written):
                    if translate:
                        path = xlate.get(path, path)
                    if path.rsplit("/", 1)[-1] in text:
                        continue
                    out.append(Finding(self.name, f"{name}/SKILL.md",
                                       "c10.path_missing", path=path))
        return out


def _matches(template: str, path: str) -> bool:
    """`specs/<id>-<feature>/x.md` 认得出 `specs/001-foo/x.md`。"""
    if template == path:
        return True
    if "<" not in template:
        return False
    pat = "".join("[^/]+" if part.startswith("<") else re.escape(part)
                  for part in re.split(r"(<[^>]+>)", template))
    return re.fullmatch(pat, path) is not None


class C11MatrixMappingComplete(Check):
    """矩阵钉死的中文路径，§3.5 必须都给出英文映射。

    真实缺陷（英文版全链路首跑）：§3.4 裁定「报告型产物 MUST 落盘并在本表登记」，
    登记了 7 条——**但 §3.5 只映射了其中 3 条**。两节从来没有对接过：
    §3.4 管「要登记」，§3.5 管「英文叫什么」，中间没有任何东西把它们接起来。

    后果是英文链路跑到那几步时**无名可用**，于是现场编：环境准备报告丢了 `09-` 前缀，
    测试报告从 `specs/` 挪进了 `specs/research/` 还占了别人的序号。
    执行者没做错任何事——**没有定义的路径，用到时就会被编出来**。

    这是同一物种的第四次（OQ-M7、`debate/00`、`chain-state.md`、本次）。
    前三次都是补完了事；这一次它终于是**可枚举**的，所以做成检查。

    C10 守「矩阵钉了 → SKILL.md 要有」，本项守「矩阵钉了 → §3.5 要有映射」。
    两项合起来才让「矩阵是唯一真相源」这句话在英文链路上真正成立。
    """

    name = "C11-matrix-mapping"
    rule_key = "c11.rule"
    phase = 3  # 跨语言映射，英文版复刻前不适用
    DEFAULT_MATRIX = Path("docs/stage-artifact-contract.md")
    #: 表格单元里的反引号路径
    CELL = re.compile(r"`((?:specs|docs)/[^`]+?)`")

    def run(self, skills_root: Path, matrix: Path | None = None) -> list[Finding]:
        mp = matrix or self.DEFAULT_MATRIX
        if not mp.is_file():
            return [Finding(self.name, str(mp), "c11.no_matrix", path=mp)]
        text = mp.read_text(encoding="utf-8")
        mapped = {zh for zh, _ in re.findall(
            r"^\| `((?:specs|docs)/[^`]+)` \| `((?:specs|docs)/[^`]+)` \|$", text, re.M)}
        out, seen = [], set()
        for line in text.splitlines():
            # 只看表格行——正文与引用块里提到的路径不构成「钉死」
            if not line.startswith("| "):
                continue
            for path in self.CELL.findall(line):
                # 文件名不含中文的，两版共用，无需映射
                if not CJK.search(path.rsplit("/", 1)[-1]):
                    continue
                # 占位符模板实例化后仍算已映射：§2.3 的验证覆盖明细写的是
                # `specs/001-csv-to-markdown/测试路由判定.md` 这样的具体实例，
                # 映射表登记的却是 `specs/<id>-<feature>/测试路由判定.md`。
                # 不做这一步，每条实测记录都会被误报成未映射。
                if path in seen or any(_matches(k, path) for k in mapped):
                    continue
                seen.add(path)
                out.append(Finding(self.name, str(mp), "c11.unmapped", path=path))
        return out


ALL_CHECKS: list[Check] = [
    C1References(), C2Pairing(), C3EnPurity(), C4EnEvals(),
    C5ScriptsNeedTests(), C6SelfContained(), C7StandaloneSection(), C8Requires(),
    C9SizeBudget(), C10MatrixPathsInSkill(), C11MatrixMappingComplete(),
]
