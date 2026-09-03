"""检查器的用户可见文案 —— 双语，一份实现。

## 为什么是消息表而不是两份检查器

宪法「单一实现优于双份脚本——双份必然漂移」。本项目亲眼见过这种漂移：
12 个英文 Skill 复制出去之后没人同步，攒下 931 行未翻译内容，
而 C2 只比对 Skill、不比对工具——**工具漂移没有任何东西会喊**。

所以两库共用**同一份**检查器，只把用户可见的那 48 条串抽成双语表。
注释、docstring 与测试内文案**刻意保持中文**：它们只在有人读源码时才起作用，
而当前英文库是「自己的英文工作副本」，没有外部贡献者。
若将来英文库面向社区开源，翻译它们是那一步的前置条件，不是现在的工作。

## 语言从哪来

**显式传入，不推断。** 与安装器的语言硬隔离同源：
不从目录位置、环境变量或区域设置猜。调用方用 `--messages` 指定，
缺省 `zh`（源语言）。英文库的 CLAUDE.md 与 README 里已写死带 `--messages en` 的命令。

## key 的作用不止于翻译

`Finding` 携带 key 而非成品文案，让测试能断言 **key** 而不是散文。
断言在会被翻译的文案上，本来就脆——改一个字就红一片，
而那种红不指向任何真实缺陷。
"""
from __future__ import annotations

LANGS = ("zh", "en")

#: key -> {lang: format string}。占位符用 str.format 的具名参数。
MESSAGES: dict[str, dict[str, str]] = {
    # ---- 各检查的规则说明（报告抬头） ----
    "c1.rule": {
        "zh": "SKILL.md 引用的 references 必须存在；references 下的文件必须被引用",
        "en": "references cited by SKILL.md must exist; files under references must be cited",
    },
    "c2.rule": {
        "zh": "zh 与 en 版的标题数与 references 集合必须一致",
        "en": "the zh and en versions must agree on heading count and reference set",
    },
    "c3.rule": {
        "zh": "英文版正文不得含中文（标注为参考用途的双语触发词除外）",
        "en": "English versions must contain no Chinese (bilingual trigger words marked for reference excepted)",
    },
    "c4.rule": {
        "zh": "英文版 evals 的 skill_name 必须带 -en，且 prompt 不得含中文",
        "en": "an English version's evals skill_name must end in -en, and its prompts must contain no Chinese",
    },
    "c5.rule": {
        "zh": "存在 scripts/ 时必须存在 tests/",
        "en": "where scripts/ exists, tests/ must exist",
    },
    "c6.rule": {
        "zh": "Skill 目录内不得出现跨 Skill 的文件路径引用（按名引用不受限）",
        "en": "a skill directory must contain no cross-skill file path (by-name references are unrestricted)",
    },
    "c7.rule": {
        "zh": "SKILL.md 必须含三节，且 ## 独立使用 须回答三问",
        "en": "SKILL.md must contain the three sections, and Standalone Use must answer the three questions",
    },
    "c8.rule": {
        # 字面花括号必须双写——单写会被 str.format 当占位符，渲染时 KeyError
        "zh": "依赖级别 ∈ {{必需, 可选增强, 编排级}}；非必需项必须有 fallback；lang 必填",
        "en": "dependency level must be one of required / optional / orchestration; non-required entries must carry a fallback; lang is mandatory",
    },
    "c9.rule": {
        "zh": "SKILL.md 内容行不超上限（三节不计），单个 references ≤ 400 行",
        "en": "SKILL.md content lines stay under the ceiling (the three sections excluded); each reference is at most 400 lines",
    },
    "c10.rule": {
        "zh": "矩阵中的精确写入路径必须出现在对应 SKILL.md",
        "en": "an exact write path in the matrix must appear in the corresponding SKILL.md",
    },

    # ---- C1 ----
    "c1.broken_link": {
        "zh": "断链：references/{name}",
        "en": "broken link: references/{name}",
    },
    "c1.orphan": {
        "zh": "孤儿：未被引用",
        "en": "orphan: never cited",
    },
    "c1.subdir": {
        "zh": "references 下不应有子目录（evals 应放 skill 根目录）",
        "en": "references must contain no subdirectory (evals belongs at the skill root)",
    },

    # ---- C2 ----
    "c2.heading_count": {
        "zh": "标题数不等：zh={zh} en={en}",
        "en": "heading counts differ: zh={zh} en={en}",
    },
    "c2.refs_mismatch": {
        "zh": "references 集合不等：仅 zh={only_zh} 仅 en={only_en}",
        "en": "reference sets differ: zh only={only_zh} en only={only_en}",
    },

    # ---- C3 ----
    "c3.residue": {
        "zh": "中文残留：{line}",
        "en": "Chinese residue: {line}",
    },

    # ---- C4 ----
    "c4.name_missing_en": {
        "zh": "skill_name 未带 -en：{actual}",
        "en": "skill_name does not end in -en: {actual}",
    },
    "c4.prompt_cjk": {
        "zh": "用例 {id} 的 prompt 含中文",
        "en": "case {id}'s prompt contains Chinese",
    },

    # ---- C5 ----
    "c5.no_tests": {
        "zh": "有 scripts/ 但无 tests/",
        "en": "has scripts/ but no tests/",
    },

    # ---- C6 ----
    "c6.cross_ref": {
        "zh": "跨 Skill 路径引用：{snippet}",
        "en": "cross-skill path reference: {snippet}",
    },

    # ---- C7 ----
    "c7.missing_section": {
        "zh": "缺章节 {section}",
        "en": "missing section {section}",
    },
    "c7.missing_question": {
        "zh": "{section} 缺「{question}」",
        "en": "{section} is missing \"{question}\"",
    },

    # ---- C8 ----
    "c8.no_frontmatter": {
        "zh": "无 frontmatter",
        "en": "no frontmatter",
    },
    "c8.no_lang": {
        "zh": "metadata 缺 lang",
        "en": "metadata is missing lang",
    },
    "c8.no_requires": {
        "zh": "缺 metadata.requires",
        "en": "missing metadata.requires",
    },
    "c8.no_level": {
        "zh": "某依赖缺 level",
        "en": "a dependency is missing its level",
    },
    "c8.bad_level": {
        "zh": "level 取值非法：{value}",
        "en": "illegal level value: {value}",
    },
    "c8.no_fallback": {
        "zh": "非必需依赖缺 fallback（level={level}）",
        "en": "a non-required dependency is missing its fallback (level={level})",
    },
    "c8.no_anti_trigger": {
        "zh": "description 缺反触发场景",
        "en": "description does not state what it is not for",
    },

    # ---- C9 ----
    "c9.over_ceiling": {
        "zh": "内容 {lines} 行 > 上限 {ceiling}（三节已排除）",
        "en": "content is {lines} lines, over the ceiling of {ceiling} (the three sections excluded)",
    },
    "c9.ref_over_ceiling": {
        "zh": "{lines} 行 > 上限 {ceiling}",
        "en": "{lines} lines, over the ceiling of {ceiling}",
    },

    # ---- C10 ----
    "c10.path_missing": {
        "zh": "矩阵钉死 {path}，但 SKILL.md 未出现该文件名",
        "en": "the matrix pins {path}, but SKILL.md never mentions that filename",
    },

    # ---- CLI：参数说明 ----
    "cli.desc": {
        "zh": "Skill 资产结构检查（10 项）",
        "en": "Skill asset structure checks (10 of them)",
    },
    "cli.help.en_root": {
        "zh": "英文版 Skill 根目录。中英文拆成两个目录后，C2 靠它跨目录比对——不给就退回同目录找 <name>-en",
        "en": "the English skill root. Once the two languages live in separate trees, C2 compares across them via this; without it, it falls back to looking for <name>-en alongside",
    },
    "cli.help.check": {
        "zh": "只跑指定检查，如 C1 C6；缺省跑全部",
        "en": "run only the named checks, such as C1 C6; runs all of them by default",
    },
    "cli.help.scope": {
        "zh": "语言作用域，默认 zh（Phase 1 只做中文版）",
        "en": "language scope, zh by default (Phase 1 covers the Chinese edition only)",
    },
    "cli.help.phase": {
        "zh": "当前所处的期，默认 1。高于本期的检查报为分期推迟",
        "en": "the current phase, 1 by default; checks belonging to a later phase are reported as deferred",
    },
    "cli.help.quiet": {
        "zh": "只输出未通过项",
        "en": "print only what did not pass",
    },
    "cli.help.messages": {
        "zh": "输出文案语言，默认 zh。显式传入，不从环境推断",
        "en": "the language of the output text, zh by default; passed explicitly, never inferred from the environment",
    },

    # ---- CLI：报错与报告 ----
    "cli.no_en_root": {
        "zh": "✗ 找不到英文版根目录 {path}",
        "en": "✗ English root not found: {path}",
    },
    "cli.no_root": {
        "zh": "✗ 找不到 {path}",
        "en": "✗ not found: {path}",
    },
    "cli.no_match": {
        "zh": "✗ 没有匹配的检查：{names}",
        "en": "✗ no check matches: {names}",
    },
    "cli.postponed_item": {
        "zh": "⏳ {name}：{count} 项 —— 须到 Phase {phase} 才应全绿",
        "en": "⏳ {name}: {count} findings - not expected to be clean until Phase {phase}",
    },
    "cli.postponed_more": {
        "zh": "…… 另 {count} 项",
        "en": "... and {count} more",
    },
    "cli.early_pass": {
        "zh": "✅ {name}（提前达标）",
        "en": "✅ {name} (clean ahead of its phase)",
    },
    "cli.failed": {
        "zh": "未通过：{count} 项（作用域 {scope}，Phase {phase}）",
        "en": "Not passed: {count} findings (scope {scope}, phase {phase})",
    },
    "cli.passed": {
        "zh": "全部通过：{count} 项检查，0 项阻塞（作用域 {scope}，Phase {phase}）",
        "en": "All passed: {count} checks, 0 blocking (scope {scope}, phase {phase})",
    },
    "cli.postponed_header": {
        "zh": "分期推迟（不计入未通过）：",
        "en": "Deferred by phase (not counted as failures):",
    },
    "cli.out_of_scope": {
        "zh": "另有 {count} 项在语言作用域之外，未计入。用 --scope all 查看。",
        "en": "A further {count} findings fall outside the language scope and were not counted. Use --scope all to see them.",
    },
}

#: 当前输出语言。**只由调用方显式设置**，绝不从环境推断。
_lang = "zh"


def set_language(lang: str) -> None:
    """设置输出语言。非法取值报错，不静默回退——静默回退会让人以为设置生效了。"""
    if lang not in LANGS:
        raise ValueError(f"unknown message language {lang!r}; valid values: {sorted(LANGS)}")
    global _lang
    _lang = lang


def current_language() -> str:
    return _lang


def t(key: str, **kwargs) -> str:
    """渲染一条消息。

    key 不存在时**返回 key 本身**而不是抛错——检查器的职责是报告发现，
    不该因为一条文案没登记就整个跑不动。缺失会以 key 原样出现在输出里，
    足够显眼到被发现。
    """
    entry = MESSAGES.get(key)
    if entry is None:
        return key
    return entry.get(_lang, entry["zh"]).format(**kwargs)
