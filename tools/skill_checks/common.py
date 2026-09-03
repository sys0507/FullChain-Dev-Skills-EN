"""检查器共用工具。

本模块的存在理由是本项目的一段真实经历：自检误报了 5 次，**全部是检查器自身的问题**，
零次真实文档缺陷。四类成因各不相同：

  1. 作用域过宽    —— 全文搜「模糊词」，命中的是规则里写的禁令本身
  2. 字节区间      —— 用字节范围判中文，把 — 和 → 也算了进去
  3. 字面量含标记  —— 匹配「只能通过显式变更记录发生」，原文是「...记录**发生」
  4. 静默失败      —— 字符串替换没匹配上，脚本照常返回成功

对策集中在这里，各检查一律复用，不要各写一套。
"""
from __future__ import annotations

import re
from pathlib import Path

# 成因 2 的对策：Unicode 码点区间，不是字节区间
CJK = re.compile(r"[一-鿿]")

FENCE = re.compile(r"^\s*```")


def strip_fences(text: str) -> str:
    """成因 1 的对策之一：剔除围栏代码块。

    提示词正文常含 ## 开头的行；不剔除会把它们当成标题。
    """
    out, inside = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            inside = not inside
            continue
        if not inside:
            out.append(line)
    return "\n".join(out)


def normalize(text: str) -> str:
    """成因 3 的对策：剥离行内标记后再比对。

    注意不要过度归一化——`test_normalize_keeps_real_difference` 是它的负样本。
    """
    return re.sub(r"[*`_]", "", text)


def headings(text: str) -> list[str]:
    """标题列表，已剔除围栏内容。"""
    return [l.strip() for l in strip_fences(text).splitlines() if l.startswith("#")]


def section(text: str, title: str) -> str:
    """成因 1 的对策之二：按章节切片，只在切片内匹配。

    找不到该章节返回空串——调用方据此判定「章节缺失」，而不是误判「内容不合格」。
    """
    body = strip_fences(text)
    if title not in body:
        return ""
    tail = body.split(title, 1)[1]
    m = re.search(r"\n#{1,3} ", tail)
    return tail[: m.start()] if m else tail


def frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    parts = text.split("---", 2)
    return parts[1] if len(parts) >= 3 else ""


def description(fm: str) -> str:
    """折叠式 description: >- 跨多行；只取首行会漏判（005 曾因此误报 5 个 Skill）。"""
    if "description:" not in fm:
        return ""
    tail = fm.split("description:", 1)[1]
    m = re.search(r"^(license|allowed-tools|metadata|name):", tail, re.M)
    return tail[: m.start()] if m else tail


def logical_skills(skills_root: Path) -> list[Path]:
    """中文版目录（en 版是其配对）。"""
    return sorted(d for d in skills_root.iterdir()
                  if d.is_dir() and not d.name.endswith("-en"))


class Finding:
    """一条发现。

    携带**语言无关的 key** 与渲染参数，而不是成品文案：

    - 文案按当前语言在读取 `detail` 时才渲染，所以一份检查器能服务两个语言的库
    - 测试断言 `key` 而不是散文。断言在会被翻译的文案上本来就脆——
      改一个字就红一片，而那种红不指向任何真实缺陷
    """

    __slots__ = ("check", "path", "key", "args")

    # check/path/key 声明为位置参数：否则 `path=` 这样的渲染参数会撞上字段名。
    # 结构上堵死，比加一条运行期校验可靠。
    def __init__(self, check: str, path: str, key: str, /, **args):
        self.check, self.path, self.key, self.args = check, path, key, args

    @property
    def detail(self) -> str:
        from messages import t
        return t(self.key, **self.args)

    def __str__(self) -> str:
        return f"[{self.check}] {self.path}: {self.detail}"


class Check:
    """所有检查的基类。

    `positive_sample` / `negative_sample` 不是可选的——
    没有负样本时，一次全绿无法区分「真的没问题」与「检查器坏了」。
    """

    name = "unnamed"
    #: 规则说明的消息 key（如 "c1.rule"），不是成品文案——它要按当前语言渲染。
    rule_key = ""
    #: 本检查从哪一期起应当全绿。跨语言类检查在英文版复刻前不可能通过，
    #: 标 3 让它在 Phase 1 报「分期推迟」而非「未通过」——
    #: 否则一个永远红的检查会让人习惯性忽略整个报告。
    phase = 1

    @property
    def rule(self) -> str:
        from messages import t
        return t(self.rule_key)

    def run(self, skills_root: Path) -> list[Finding]:
        raise NotImplementedError
