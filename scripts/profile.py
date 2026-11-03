#!/usr/bin/env python
"""profile.py: the per-writer learning store for the prose skill.

The profile lives outside the skill (default ~/.claude/prose-profile, override with
PROSE_PROFILE_DIR) so each writer keeps their own rules, glossary, venue cards and
exemplar cards. Files are plain Markdown that the writer can read and edit.

Commands:
    init                                  create the profile from the bundled template
    context --genre G [--venue V] [--section S] [--lang zh|en]
                                          print what applies before drafting
    observe --scope G/V/S --lang L --src SRC --pref TEXT [--example TEXT]
    observe --same O7 [--example TEXT]    record one more occurrence of an observation
    promote O7 [--pref TEXT]              turn an observation into a rule
    retire R3 --reason TEXT               stop applying a rule, keep it for history
    diff DRAFT FINAL                      sentence pairs the writer changed
    stats FILE [FILE ...]                 measurable habits of the writer's own text
    list                                  counts and pending promotions

Scope is genre/venue/section; use * for "any". SRC is one of
user-edit, explicit, advisor, reviewer, exemplar.
"""
import argparse
import datetime
import difflib
import os
import re
import shutil
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "profile-template"
ROOT = Path(os.environ.get("PROSE_PROFILE_DIR") or Path.home() / ".claude" / "prose-profile")
RULE_RX = re.compile(r"^- \[(R\d+)\] scope=(\S+) lang=(\S+) \| (.+?) \| 依据 (.+?) \| (\d{4}-\d{2}-\d{2})\s*$")
OBS_RX = re.compile(r"^- \[(O\d+)\] scope=(\S+) lang=(\S+) n=(\d+) src=(\S+) \| (.+?) \| 例：(.*?) \| (\d{4}-\d{2}-\d{2})\s*$")
SOURCES = ("user-edit", "explicit", "advisor", "reviewer", "exemplar")
PROMOTE_AT = 2


def today():
    return datetime.date.today().isoformat()


def need_root():
    if not (ROOT / "rules.md").is_file():
        sys.exit(f"档案不存在：{ROOT}。先运行 `python {Path(__file__).name} init`。")


def read_lines(name):
    return (ROOT / name).read_text(encoding="utf-8").splitlines()


def write_lines(name, lines):
    path = ROOT / name
    shutil.copyfile(path, path.with_suffix(".md.bak"))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def next_id(lines, prefix):
    nums = [int(m.group(1)) for m in (re.search(rf"\[{prefix}(\d+)\]", l) for l in lines) if m]
    return f"{prefix}{max(nums, default=0) + 1}"


def norm_scope(scope):
    parts = (scope.split("/") + ["*", "*", "*"])[:3]
    return "/".join(p.strip() or "*" for p in parts)


def matches(scope, genre, venue, section):
    want = (genre or "*", venue or "*", section or "*")
    have = norm_scope(scope).split("/")
    return all(h == "*" or w == "*" or h.lower() == w.lower() for h, w in zip(have, want))


def specificity(scope):
    return sum(p != "*" for p in norm_scope(scope).split("/"))


def ready(m):
    return int(m.group(4)) >= PROMOTE_AT or m.group(5) == "explicit"


def one_line(text):
    return re.sub(r"\s+", " ", text.replace("|", "／")).strip()


def cmd_init(_):
    if (ROOT / "rules.md").is_file():
        print(f"档案已存在：{ROOT}（未改动）")
        return
    shutil.copytree(TEMPLATE, ROOT, dirs_exist_ok=True)
    print(f"已创建档案：{ROOT}")


def cmd_context(a):
    need_root()
    active = []
    for line in read_lines("rules.md"):
        if line.startswith("## 已停用"):
            break
        m = RULE_RX.match(line)
        if m and matches(m.group(2), a.genre, a.venue, a.section) and m.group(3) in ("*", a.lang or "*"):
            active.append((specificity(m.group(2)), m.group(6), line))
    print(f"# 写作档案：{ROOT}\n")
    print("## 适用规则（越具体越优先；同等具体时日期新的优先）")
    for _, _, line in sorted(active, key=lambda x: (x[0], x[1]), reverse=True):
        print(line)
    if not active:
        print("（无）")
    pending = [l for l in read_lines("observations.md")
               if (m := OBS_RX.match(l)) and ready(m) and matches(m.group(2), a.genre, a.venue, a.section)]
    if pending:
        print("\n## 待确认（出现两次以上或作者明确要求过，问作者是否升为规则）")
        print("\n".join(pending))
    if a.venue:
        card = ROOT / "venues" / f"{a.venue}.md"
        print(f"\n## 期刊卡片：{card if card.is_file() else '（尚无，可按 learning.md 第 4 节建立）'}")
    ex_dirs = [ROOT / "exemplars" / (a.genre or "")]
    cards = sorted(p for d in ex_dirs if d.is_dir() for p in d.glob("*.md"))
    if a.venue:
        cards = [p for p in cards if a.venue.lower() in p.read_text(encoding="utf-8").lower()] or cards
    print("\n## 范文结构卡片")
    print("\n".join(f"- {p}" for p in cards[:5]) or "（无）")
    samples = sorted(p for p in (ROOT / "samples").glob(f"{a.genre or ''}*") if p.name != "README.md")         if (ROOT / "samples").is_dir() else []
    print("\n## 作者样稿（起草时取 2–3 段作风格样本）")
    print("\n".join(f"- {p}" for p in samples[:5]) or "（无）")
    print(f"\n## 术语表：{ROOT / 'glossary.md'}")


def cmd_observe(a):
    need_root()
    lines = read_lines("observations.md")
    if a.same:
        for i, line in enumerate(lines):
            m = OBS_RX.match(line)
            if m and m.group(1) == a.same:
                n = int(m.group(4)) + 1
                ex = m.group(7) if not a.example else one_line(a.example)
                lines[i] = (f"- [{a.same}] scope={m.group(2)} lang={m.group(3)} n={n} src={m.group(5)} | "
                            f"{m.group(6)} | 例：{ex} | {today()}")
                write_lines("observations.md", lines)
                print(lines[i] + ("\n→ 已出现 %d 次，可问作者是否升为规则（promote %s）" % (n, a.same) if n >= PROMOTE_AT else ""))
                return
        sys.exit(f"找不到 {a.same}")
    if not (a.scope and a.pref and a.src):
        sys.exit("新观察需要 --scope、--src 和 --pref")
    if a.src not in SOURCES:
        sys.exit(f"--src 只能是 {', '.join(SOURCES)}")
    oid = next_id(lines, "O")
    line = (f"- [{oid}] scope={norm_scope(a.scope)} lang={a.lang or '*'} n=1 src={a.src} | "
            f"{one_line(a.pref)} | 例：{one_line(a.example or '')} | {today()}")
    lines.append(line)
    write_lines("observations.md", lines)
    print(line)
    if a.src == "explicit":
        print(f"→ 作者明确要求，可直接升为规则（promote {oid}）")


def cmd_promote(a):
    need_root()
    obs = read_lines("observations.md")
    for i, line in enumerate(obs):
        m = OBS_RX.match(line)
        if m and m.group(1) == a.oid:
            rules = read_lines("rules.md")
            rid = next_id(rules, "R")
            pref = one_line(a.pref) if a.pref else m.group(6)
            rule = f"- [{rid}] scope={m.group(2)} lang={m.group(3)} | {pref} | 依据 {m.group(5)}×{m.group(4)}（{a.oid}） | {today()}"
            cut = next((j for j, l in enumerate(rules) if l.startswith("## 已停用")), len(rules))
            rules.insert(cut, rule)
            write_lines("rules.md", rules)
            del obs[i]
            write_lines("observations.md", obs)
            print(rule)
            return
    sys.exit(f"找不到 {a.oid}")


def cmd_retire(a):
    need_root()
    rules = read_lines("rules.md")
    for i, line in enumerate(rules):
        m = RULE_RX.match(line)
        if m and m.group(1) == a.rid:
            del rules[i]
            if not any(l.startswith("## 已停用") for l in rules):
                rules += ["", "## 已停用"]
            rules.append(f"{line}  〔停用 {today()}：{one_line(a.reason)}〕")
            write_lines("rules.md", rules)
            print(f"已停用 {a.rid}")
            return
    sys.exit(f"找不到 {a.rid}")


def split_sentences(text):
    text = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"(?<=[。！？；])\s*|(?<=[.!?;])\s+", text) if len(s.strip()) > 1]


def cmd_diff(a):
    old = split_sentences(Path(a.draft).read_text(encoding="utf-8", errors="replace"))
    new = split_sentences(Path(a.final).read_text(encoding="utf-8", errors="replace"))
    sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
    k = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        k += 1
        print(f"\n[{k}] {tag}")
        for s in old[i1:i2]:
            print(f"  - {s}")
        for s in new[j1:j2]:
            print(f"  + {s}")
    kept = sum(i2 - i1 for t, i1, i2, _, _ in sm.get_opcodes() if t == "equal")
    print(f"\n共 {k} 处改动；原稿 {len(old)} 句中原样保留 {kept} 句。")
    print("逐处归纳作者的偏好（为什么这样改），只记录在别处也会成立的那几条。")


def zh_ratio(text):
    return len(re.findall(r"[一-鿿]", text)) >= len(re.findall(r"[A-Za-z]", text)) / 3


def cmd_stats(a):
    text = "\n".join(Path(f).read_text(encoding="utf-8", errors="replace") for f in a.files)
    zh = zh_ratio(text)
    sents = split_sentences(text)
    lens = [len(re.findall(r"[一-鿿]", s)) if zh else len(s.split()) for s in sents]
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    unit = "字" if zh else "词"
    total = sum(lens) or 1
    print(f"样本：{len(a.files)} 个文件，{len(sents)} 句，{len(paras)} 段，约 {total} {unit}")
    if len(lens) >= 4:
        q = statistics.quantiles(lens, n=4)
        print(f"句长（{unit}）：中位 {statistics.median(lens):.0f}，四分位 {q[0]:.0f}–{q[2]:.0f}，最长 {max(lens)}")
    plen = [len(split_sentences(p)) for p in paras]
    if plen:
        print(f"段长（句）：中位 {statistics.median(plen):.0f}，最长 {max(plen)}")
    per_k = 1000 / total
    if zh:
        for label, rx in [("『的』", "的"), ("『进行』", "进行"), ("『被』", "被"), ("限定语（可能/或许/在一定程度上）", "可能|或许|也许|在一定程度上"),
                          ("第一人称（我们/本文/笔者）", "我们|本文|笔者"), ("破折号", "——")]:
            print(f"{label}：每千字 {len(re.findall(rx, text)) * per_k:.1f}")
    else:
        low = text.lower()
        for label, rx in [("we/our", r"\b(we|our|us)\b"), ("passive (be + -ed)", r"\b(is|are|was|were|be|been|being)\s+\w+ed\b"),
                          ("hedges", r"\b(may|might|could|suggests?|likely|possibly|appears?)\b"),
                          ("boosters", r"\b(clearly|significantly|demonstrates?|substantially|strongly)\b"),
                          ("em dash", "—"), ("semicolon", ";")]:
            print(f"{label}: {len(re.findall(rx, low)) * per_k:.1f} per 1000 words")
    print("这些数字描述作者本人的习惯，用来校准改写（别把作者的写法改成另一个人的），不是好坏标准。")


def cmd_list(_):
    need_root()
    rules = [l for l in read_lines("rules.md") if RULE_RX.match(l)]
    obs = [OBS_RX.match(l) for l in read_lines("observations.md")]
    obs = [m for m in obs if m]
    print(f"档案：{ROOT}")
    print(f"规则 {len(rules)} 条；观察 {len(obs)} 条，其中可升级 {sum(ready(m) for m in obs)} 条")
    for sub in ("venues", "exemplars", "samples"):
        d = ROOT / sub
        n = sum(1 for f in d.rglob("*.md") if not f.name.startswith("_") and f.name != "README.md") if d.is_dir() else 0
        print(f"{sub}: {n} 个")
    if len(rules) > 40:
        print("规则超过 40 条：按 learning.md 第 6 节合并重复、停用过时的。")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    c = sub.add_parser("context")
    c.add_argument("--genre", default="")
    c.add_argument("--venue", default="")
    c.add_argument("--section", default="")
    c.add_argument("--lang", default="")
    o = sub.add_parser("observe")
    o.add_argument("--same")
    o.add_argument("--scope")
    o.add_argument("--lang", default="*")
    o.add_argument("--src")
    o.add_argument("--pref")
    o.add_argument("--example")
    p = sub.add_parser("promote")
    p.add_argument("oid")
    p.add_argument("--pref")
    r = sub.add_parser("retire")
    r.add_argument("rid")
    r.add_argument("--reason", required=True)
    d = sub.add_parser("diff")
    d.add_argument("draft")
    d.add_argument("final")
    s = sub.add_parser("stats")
    s.add_argument("files", nargs="+")
    sub.add_parser("list")
    a = ap.parse_args()
    {"init": cmd_init, "context": cmd_context, "observe": cmd_observe, "promote": cmd_promote,
     "retire": cmd_retire, "diff": cmd_diff, "stats": cmd_stats, "list": cmd_list}[a.cmd](a)


if __name__ == "__main__":
    main()
