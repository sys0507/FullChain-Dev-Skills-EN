#!/usr/bin/env python3
"""本地一条命令跑全部 10 项检查。

    python tools/skill_checks/run_all.py
    python tools/skill_checks/run_all.py --scope all --phase 3
    python tools/skill_checks/run_all.py --check C6 C7 C8

必须能在本地手动执行 —— 只存在于自动化平台的检查，开发期无法自查，
问题会积压到最后一刻。

两个维度的过滤，作用不同：

  --scope  语言作用域。Phase 1 只做中文版，英文版的发现不该淹没中文版的真实问题。
  --phase  分期门控。跨语言类检查在英文版复刻前不可能通过；
           标为「分期推迟」而非「未通过」，否则一个永远红的检查
           会让人习惯性忽略整个报告。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from checks import ALL_CHECKS  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Skill 资产结构检查（10 项）")
    ap.add_argument("--skills-root", default="Assets/skills")
    ap.add_argument("--en-root", default=None,
                    help="英文版 Skill 根目录。中英文拆成两个目录后，"
                         "C2 靠它跨目录比对——不给就退回同目录找 <name>-en")
    ap.add_argument("--check", nargs="*", default=None,
                    help="只跑指定检查，如 C1 C6；缺省跑全部")
    ap.add_argument("--scope", choices=("zh", "en", "all"), default="zh",
                    help="语言作用域，默认 zh（Phase 1 只做中文版）")
    ap.add_argument("--phase", type=int, default=1,
                    help="当前所处的期，默认 1。高于本期的检查报为分期推迟")
    ap.add_argument("--quiet", action="store_true", help="只输出未通过项")
    args = ap.parse_args(argv)

    root = Path(args.skills_root)
    en_root = Path(args.en_root) if args.en_root else None
    if en_root is not None and not en_root.is_dir():
        print(f"✗ 找不到英文版根目录 {en_root}", file=sys.stderr)
        return 2
    if not root.is_dir():
        print(f"✗ 找不到 {root}", file=sys.stderr)
        return 2

    selected = ALL_CHECKS
    if args.check:
        want = {c.upper() for c in args.check}
        selected = [c for c in ALL_CHECKS if c.name.split("-")[0].upper() in want]
        if not selected:
            print(f"✗ 没有匹配的检查：{args.check}", file=sys.stderr)
            return 2

    def in_scope(f) -> bool:
        is_en = "-en/" in f.path or f.path.endswith("-en")
        return {"zh": not is_en, "en": is_en, "all": True}[args.scope]

    blocking = 0
    out_of_scope = 0
    lines: list[str] = []
    postponed: list[str] = []

    for chk in selected:
        # C2 是唯一的 zh/en 漂移探测器，它需要知道英文版在哪
        raw = chk.run(root, en_root) if chk.name.startswith("C2") else chk.run(root)
        found = [f for f in raw if in_scope(f)]
        out_of_scope += len(raw) - len(found)
        chk_phase = getattr(chk, "phase", 1)

        if chk_phase > args.phase:
            if found:
                postponed.append(
                    f"⏳ {chk.name}：{len(found)} 项 —— 须到 Phase {chk_phase} 才应全绿")
                if not args.quiet:
                    postponed += [f"      {f}" for f in found[:3]]
                    if len(found) > 3:
                        postponed.append(f"      …… 另 {len(found) - 3} 项")
            elif not args.quiet:
                lines.append(f"✅ {chk.name}（提前达标）")
            continue

        blocking += len(found)
        if found:
            lines.append(f"\n❌ {chk.name} —— {chk.rule}")
            lines += [f"   {f}" for f in found]
        elif not args.quiet:
            lines.append(f"✅ {chk.name}")

    if lines:
        print("\n".join(lines))
    print("\n" + "─" * 62)
    if blocking:
        print(f"未通过：{blocking} 项（作用域 {args.scope}，Phase {args.phase}）")
    else:
        print(f"全部通过：{len(selected)} 项检查，0 项阻塞"
              f"（作用域 {args.scope}，Phase {args.phase}）")

    if postponed:
        print("\n分期推迟（不计入未通过）：")
        for line in postponed:
            print("  " + line)
    if out_of_scope:
        print(f"\n另有 {out_of_scope} 项在语言作用域之外，未计入。用 --scope all 查看。")

    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
