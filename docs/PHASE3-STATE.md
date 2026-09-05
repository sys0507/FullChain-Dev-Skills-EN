# Phase 3 状态

> Phase 3 出口已达成：英文库全部检查全绿，跨目录 C2/C4/C5 全绿。

## 一、出口标准

```
python tools/skill_checks/run_all.py --scope en --phase 3 --messages en \
  --matrix ../全链路开发汇总/docs/stage-artifact-contract.md
python tools/skill_checks/run_all.py --check C2 C4 C5 --phase 3 --messages en \
  --skills-root ../全链路开发汇总/Assets/skills --en-root Assets/skills \
  --matrix ../全链路开发汇总/docs/stage-artifact-contract.md
```

| 检查 | 结果 |
|---|:---:|
| 英文库 C1–C11 | ✅ 全绿 |
| 跨目录 C2/C4/C5 | ✅ 全绿 |

## 二、交付物

| 项 | 状态 |
|---|---|
| 21 个英文 Skill（含编排器） | ✅ |
| 两份模板译文 | ✅ 纯提示词版 + skills 版 |
| 薄索引英文版 | ✅ `Full-Chain-Development-Skill-Execution-Index.md` |
| `CLAUDE.md` / `README.md` | ✅ |
| 检查器（11 项 + 自测） | ✅ 与中文库同步 |
| 移植规格 | ✅ `docs/EN-PORT-SPEC.md` |

## 三、编排器验证

`fullchain-dev-workflow-en` 已在无人值守的干净环境跑通完整英文全链路，
产出全部落在契约矩阵定义的路径上。详见中文库 `docs/phase3-acceptance-report.md`。

## 四、C3 的已知盲区

C3 只扫 `.md`，`.py`/`.json` 里的中文残留看不见；扫描范围也只限
`Assets/skills/*-en/`，根目录文件与 `tools/` 在范围之外。

**刻意保留的中文**：

| 位置 | 为什么 |
|---|---|
| `knife4_merge.py` 的 `RISK_KEYWORDS` | 扫描目标代码库的匹配模式，不是工具自身的语言——目标代码库可能有中文标识符 |
| `docs/EN-PORT-SPEC.md` | 双语词汇对照表，中文列是它的用途 |
| `CLAUDE.md` / `README.md` | 指向同级目录 `全链路开发汇总/`，目录名本身是中文 |
| `product-research-kickoff-universal-en/SKILL.md` | 带 `Chinese (for reference)` 白名单标记的双语触发词 |
| 本文件 | 写给中文用户看的状态文件 |

## 五、检查器语言（OQ-M10）

`tools/skill_checks/` 按受众切分：用户可见文案（规则说明、发现详情、
CLI 输出）抽成双语表 `messages.py`，`--messages {zh,en}` 显式切换；
开发者可见内容（注释、docstring、测试文案）保持中文，两库共用同一份实现。

若英文库将来开源为面向社区的项目，翻译开发者可见的部分是 Phase 4 的前置条件。
