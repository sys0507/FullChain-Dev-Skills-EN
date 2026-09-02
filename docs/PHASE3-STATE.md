# Phase 3 断点状态

> 更新：2026-09-02。**七个并行执行者全部因会话速率上限中断**，重置在 3am America/New_York。

## 一、已完成并提交

| # | 内容 | 提交 |
|:-:|---|---|
| 1 | 重命名对齐 21 处，全库 0 断链 | `c0132ec` |
| 2 | 宪法升 1.2.0（原则 I 加窄例外 + 审计锚点哈希） | `c0132ec` |
| 3 | C2 跨目录能力 | `24de569` |
| 4 | 12 个英文版搬出中文树 | `c252aa6` / EN `d4b0e41` |
| 5 | 双语词汇表 §5.0 + C7/C8/反触发词双语化 | 中文树已提交 |

## 二、本轮查出的真实债务（不是执行者造成的）

**迁移过来的英文版，references 大面积仍是中文——931 行，8 个 Skill。**

| Skill | 中文行 | 文件数 |
|---|---:|---:|
| `test-routing-advisor-en` | 552 | 7 |
| `frontend-testing-en` | 125 | 1 |
| `testing-system-blueprint-en` | 72 | 2 |
| `claude-md-bootstrap-en` | 71 | 1 |
| `backend-testing-en` | 65 | 1 |
| `full-chain-testing-en` | 43 | 5 |
| `speckit-design-injection-universal-en` | 2 | 2 |
| `product-research-kickoff-universal-en` | 1 | 1 |

**git 证实这些中文在 HEAD 里就有**——是 Phase 3 之前就存在的债，随迁移带过来的。

### 为什么之前没发现

早先跑分项检查时读到「C3 全部通过」，那是**测量错误**：
`grep -oE '未通过：[0-9]+ 项|全部通过' | head -1` 抓到的「全部通过」
出现在某条发现所引用的中文原文里，不是汇总行。

**同类错误（匹配口径不当导致误读）在本项目第三次发生。**

## 三、当前各 Skill 状态

### 已完整（三节 + metadata + 零中文）

- `platform-design-kickoff-en`（含 3 references + evals，手写）
- `adversarial-architecture-selection-universal-en`（refs 5/6，缺 1 份）
- `prd-writer-universal-en`（refs 5/7，缺 2 份）
- `project-context-ledger-en`（refs 2/3，缺 1 份）
- `implementation-runway-setup-en`（refs 0/3，全缺）

### 三节已补但有中文残留

`backend-testing-en` `claude-md-bootstrap-en` `frontend-testing-en`
`product-research-kickoff-universal-en` `test-routing-advisor-en`
`testing-system-blueprint-en`

### 只有空壳或未开始

| Skill | 状态 |
|---|---|
| `full-chain-testing-en` | 三节 0/3，refs 1/2 |
| `fullstack-slice-testing-en` | 三节 0/3 |
| `run-feature-en` | 三节 0/3，refs 0/2 |
| `speckit-design-injection-universal-en` | 三节 0/3 |
| `fullchain-toolchain-setup-en` | **无 SKILL.md** |
| `learnings-retrospective-en` | **无 SKILL.md** |
| `mvp-convergence-brainstorming-en` | **无 SKILL.md** |
| `release-packaging-router-en` | **无 SKILL.md** |
| `speckit-feature-pipeline-en` | **无 SKILL.md** |

### 两份模板译文

| 文件 | 状态 |
|---|---|
| `Full-Chain-Development-Prompt-Template-Skills-Edition.md` | 57057 字节，**完成度未核验** |
| `Full-Chain-Development-Prompt-Template.md` | **未产出** |

`fullchain-dev-workflow-en` 刻意不做——宪法「中文先行」，等英文版端到端验证时一并补。

## 四、剩余工作

| # | 内容 | 量 |
|:-:|---|---|
| 1 | 清 931 行中文残留（8 个 Skill 的 references） | 最大一块 |
| 2 | 5 个 Skill 从零建 | SKILL.md + refs + evals |
| 3 | 4 个 Skill 补三节 + metadata | — |
| 4 | 补齐缺失的 references（adversarial 1 / prd-writer 2 / ledger 1 / runway 3） | 7 份 |
| 5 | 翻译纯提示词模板 | 1278 行 |
| 6 | 核验 skills 版模板译文 | 57KB |
| 7 | 英文版 CLAUDE.md / 薄索引 / README | 3 份 |
| 8 | 三个带 scripts 的英文版：脚本与测试移植（C5 会查） | — |

## 五、出口标准

```
python tools/skill_checks/run_all.py --scope en --phase 3
python tools/skill_checks/run_all.py --check C2 --phase 3 \
  --skills-root ../全链路开发汇总/Assets/skills --en-root Assets/skills
```

C1–C10 全绿。**C2 全绿是 Phase 3 真正的出口**——它一直被标「分期推迟」，等的就是这一期。

## 六、恢复时怎么接

1. 先读本文件
2. 跑上面两条命令拿到当前真实缺口，**不要相信本文件的数字是最新的**
3. 读汇总行要看 `─────` 之后那一行，**不要用 grep 从全文抓关键词**——
   发现条目里会引用原文，原文可能正好含有你在找的词
4. 派执行者时**必须交代**：大文件用 Write 工具，不要用 heredoc——
   七个执行者里有四个明确报告 heredoc 解析失败
