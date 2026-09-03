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
from messages import LANGS, set_language, t  # noqa: E402


def _preselect_language(argv: list[str] | None) -> None:
    """`--messages` 必须在构造 parser **之前**生效——help 文案在构造时就渲染了。

    只认这一个参数，其余交给正式 parser。与安装器同源：
    语言显式传入，不从环境或区域设置推断。
    """
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--messages", choices=LANGS, default="zh")
    set_language(pre.parse_known_args(argv)[0].messages)


def main(argv: list[str] | None = None) -> int:
    _preselect_language(argv)
    ap = argparse.ArgumentParser(description=t("cli.desc"))
    ap.add_argument("--skills-root", default="Assets/skills")
    ap.add_argument("--en-root", default=None, help=t("cli.help.en_root"))
    ap.add_argument("--check", nargs="*", default=None, help=t("cli.help.check"))
    ap.add_argument("--scope", choices=("zh", "en", "all"), default="zh",
                    help=t("cli.help.scope"))
    ap.add_argument("--phase", type=int, default=1, help=t("cli.help.phase"))
    ap.add_argument("--quiet", action="store_true", help=t("cli.help.quiet"))
    ap.add_argument("--messages", choices=LANGS, default="zh",
                    help=t("cli.help.messages"))
    args = ap.parse_args(argv)

    root = Path(args.skills_root)
    en_root = Path(args.en_root) if args.en_root else None
    if en_root is not None and not en_root.is_dir():
        print(t("cli.no_en_root", path=en_root), file=sys.stderr)
        return 2
    if not root.is_dir():
        print(t("cli.no_root", path=root), file=sys.stderr)
        return 2

    selected = ALL_CHECKS
    if args.check:
        want = {c.upper() for c in args.check}
        selected = [c for c in ALL_CHECKS if c.name.split("-")[0].upper() in want]
        if not selected:
            print(t("cli.no_match", names=args.check), file=sys.stderr)
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
                postponed.append(t("cli.postponed_item", name=chk.name,
                                   count=len(found), phase=chk_phase))
                if not args.quiet:
                    postponed += [f"      {f}" for f in found[:3]]
                    if len(found) > 3:
                        postponed.append("      " + t("cli.postponed_more",
                                                      count=len(found) - 3))
            elif not args.quiet:
                lines.append(t("cli.early_pass", name=chk.name))
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
        print(t("cli.failed", count=blocking, scope=args.scope, phase=args.phase))
    else:
        print(t("cli.passed", count=len(selected), scope=args.scope,
                phase=args.phase))

    if postponed:
        print("\n" + t("cli.postponed_header"))
        for line in postponed:
            print("  " + line)
    if out_of_scope:
        print("\n" + t("cli.out_of_scope", count=out_of_scope))

    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
