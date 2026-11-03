#!/usr/bin/env python
"""check_prose.py: flag AI-style tells, AI-writing failures, structure and readability issues (Chinese and English).

Usage:
    python check_prose.py FILE [--genre academic-en|academic-zh|patent|report|technical|letter|essay]

Reads .md / .txt / .tex, and .docx when python-docx is installed. Every hit is a place to
inspect, not proof of AI authorship; judge each one in context. Exit code is always 0.
Hits are grouped as: 内容 (unsupported claims, sycophancy, residue), 结构 (headings, sections,
list and dimension skeletons), AI 痕迹 (patterns measured or widely documented as over-used by
models), 文体 (genre rules), 排版 (punctuation and typesetting), 可读性 (not AI evidence).
"""
import argparse
import re
import sys
from pathlib import Path

ZH_PHRASES = [
    "值得注意的是", "需要指出的是", "值得一提的是", "综上所述", "总而言之", "总的来说", "总体而言",
    "综观", "众所周知", "不难看出", "显而易见", "可以清晰地", "不可否认", "扮演着", "扮演了",
    "至关重要", "不可或缺", "具有重要意义", "具有重要的意义", "具有深远的意义", "典型代表", "广泛应用", "深入研究",
    "长足发展", "日益重要", "高度一致", "各有侧重", "在一定程度上", "某种程度上", "开辟了新的",
    "奠定了坚实的基础", "赋能", "底层逻辑", "抓手", "说白了", "说穿了", "先说结论",
    "不得不说", "有一说一", "很多人不知道", "真正的关键在于", "未来可期", "拭目以待", "值得我们深思",
    "让我们携手", "让我们一起", "崭新篇章", "新篇章", "双刃剑", "护城河", "降维打击",
]
ZH_TONE = ["说实话", "我完全理解", "接住你", "接住了", "好问题", "很高兴地", "我必须承认"]
ZH_PATTERNS = [
    (r"不是[^，。\n]{1,20}[，,]\s*(而是|而在于|本质是)", "先否后立『不是…而是』"),
    (r"不仅[^，。\n]{1,30}(而且|更是|还)", "对仗堆叠『不仅…而且/更是』"),
    (r"回答的是[^。\n]{0,40}的问题", "对称收尾『回答的是…的问题』"),
    (r"标志着[^。\n]{0,30}(转变|里程碑|跃迁|起点|新时代)", "拔高收尾『标志着…』"),
    (r"为[^，。\n]{0,20}提供[^，。\n]{0,12}(支持|支撑|基础|保障)", "空泛因果『为…提供…支撑』"),
    (r"旨在[^，。；\n]{0,12}", "空泛目的『旨在…』"),
    (r"(对于|对)[^，。\n]{1,15}(来说|而言)", "译文句式『对于…来说』"),
    (r"当[^，。\n]{2,25}(时|的时候)[，,]", "译文句式『当…时』"),
    (r"(^|[。！？\n])\s*然而[，,]", "译文句式：句首『然而，』"),
    (r"这意味着", "译文句式『这意味着』复述"),
    (r"(相关|有关)(规定|材料|方面|问题|内容|工作|部门)", "虚指『相关/有关』：写出具体对象"),
    (r"(数据|结果|实验)(告诉|揭示|讲述)(了|我们)", "拟人化主语『数据告诉我们』"),
    (r"尽管[^。\n]{0,20}(挑战|困难|不足)[^。\n]{0,30}(前景|潜力|广阔)", "挑战—展望套路"),
    (r"如同一[座盏把块道]?(灯塔|基石|桥梁|钥匙|引擎)|注入[^，。\n]{0,6}(引擎|动力|活力)|彰显了", "现成喻体 / 拔高动词"),
    (r"(逻辑|问题|原因|结论|答案)很(清晰|直接|简单|明确)[：:]", "形容词加冒号开头"),
    (r"((从|可以从|主要从|分)(以下)?|以下)[两三四五六七八九十几多]+个?(方面|层面|维度|角度|方向)", "预告式维度枚举"),
]
ZH_VAGUE = [
    (r"(大量|诸多|众多|许多)(研究|文献|实验|学者)(表明|显示|证明|认为)", "无出处的权威『大量研究表明』"),
    (r"(专家|学者|业内)(普遍)?(认为|表示|指出)", "无出处的权威『专家认为』"),
    (r"(^|[，。；])研究(表明|显示)", "无出处的『研究表明』：写出作者、年份"),
]
ZH_LINE_PATTERNS = [
    (r"^\s*第[一二三四五六七八九十]+[，、,]", "序数词充当小标题『第一，』"),
    (r"^[^。！？\n]{2,18}[：:]\s*$", "空转句 + 冒号引出"),
    (r"^\s*(这一点|这很|这正是|这也|这种做法|这无疑|这不仅)", "段首无指代的评论句"),
]
ZH_OPENING = r"^\s*(随着[^，。]{0,30}(发展|进步|普及|兴起)|近年来|在当今|当今[^，。]{0,8}(时代|社会)|在[^，。]{1,20}(时代|背景下)[，,])"
ZH_DIM = r"(从|在|就|站在)[^，。；：\n]{1,12}?(层面|维度|方向|角度|视角|方面|层次)(来看|来说|而言|上|看|讲)?"

EN_PHRASES = [
    "it is worth noting", "it's worth noting", "it should be noted that", "notably", "importantly",
    "crucially", "in conclusion", "at its core", "when it comes to", "in today's", "in an era of",
    "plays a crucial role", "plays a pivotal role", "serves as a testament", "stands as a testament",
    "testament to", "delve", "delves", "tapestry", "showcasing", "underscores", "underscore",
    "paves the way", "pave the way", "sheds light on", "opens new avenues", "holds promise",
    "groundbreaking", "cutting-edge", "seamless", "meticulous", "meticulously", "intricate", "interplay",
    "evolving landscape", "enduring legacy", "has the potential to revolutionize", "it goes without saying",
    "that being said", "let's dive in", "let's unpack", "here's the thing", "imagine a world",
    "the future looks bright", "only time will tell", "let that sink in", "beacon", "cornerstone",
    "game-changer", "paradigm shift", "watershed moment", "double-edged sword", "unlock the power",
    "unlock the potential", "here's a breakdown", "across multiple dimensions",
]
EN_PATTERNS = [
    (r"\bnot only\b[^.]{1,80}\bbut also\b", "AI 痕迹", "negative parallelism 'not only … but also'"),
    (r"\b(?:it'?s|this is|that is) not (?:just |merely |only )?[^.,;]{1,40}[,;—-]+\s*(?:it'?s|but)\b", "AI 痕迹", "'not X, it's Y' contrast"),
    (r",\s+(highlighting|underscoring|ensuring|reflecting|showcasing|emphasizing|fostering|paving the way)\b", "AI 痕迹", "trailing -ing clause adding significance"),
    (r"\b(serves|stands|functions|acts) as an?\b", "AI 痕迹", "copula avoidance 'serves as'"),
    (r"\bfrom [\w-]+(?: [\w-]+){0,3} to [\w-]+(?: [\w-]+){0,3},\s*from\b", "AI 痕迹", "false range 'from X to Y, from …'"),
    (r"\bin this (section|paper|article|essay),? we (will|shall)\b", "AI 痕迹", "meta-commentary 'In this section, we will'"),
    (r"\bcan be (?:understood|viewed|analy[sz]ed|examined) (?:on|from|in|across) (?:several|three|multiple|two|four) (?:levels|perspectives|dimensions|angles)\b", "结构", "preview of dimensions"),
    (r"\b(perform|conduct|make|carry out)(?:s|ed|ing)? (?:an? |the )?(analysis|comparison|evaluation|investigation|improvement)\b", "可读性", "nominalization: use the verb"),
    (r"\b(may|might|could) (?:potentially|possibly)\b", "内容", "stacked hedge"),
    (r"\b(very|really|truly|deeply|fundamentally|essentially|incredibly)\b", "可读性", "empty intensifier"),
    (r"\b(experts (?:say|argue|believe)|studies (?:show|suggest)|research (?:shows|suggests)|it is widely (?:believed|regarded)|numerous studies)\b", "内容", "vague attribution: name the source"),
    (r"\b(you'?re absolutely right|great question|i hope this helps|happy to help|let me know if)\b", "内容", "chat/sycophancy residue"),
    (r"(?:^|\W)(honestly,|i want to be upfront|i'?m (?:so )?(?:thrilled|excited) to\b|let'?s break (?:this|it) down|think of it (?:as|like)\b)", "AI 痕迹", "performed tone"),
    (r"\bdespite (?:these|the|its|such) challenges\b", "AI 痕迹", "challenges-then-optimism formula"),
    (r"\b(i hope this (?:e-?mail|message) finds you well|i wanted to reach out|(?:please )?(?:don'?t hesitate|feel free) to reach out)\b", "AI 痕迹", "stock email opener/closer"),
    (r"\b(as of my (?:last|knowledge)|based on available information|not widely documented)\b", "内容", "knowledge-boundary disclaimer"),
]
EN_DIM = r"\b(on the [\w-]+ (?:front|side)|from an? [\w-]+(?: [\w-]+)? (?:perspective|standpoint|point of view|lens)|in terms of|at the [\w-]+ level)\b"
EN_OPENING = r"^\s*(in today'?s|in the ever|in an era|in recent years|with the (?:rapid )?development of|imagine a world)"
EN_DENSITY_WORDS = ["crucial", "significant", "significantly", "comprehensive", "robust", "key", "novel",
                    "various", "effective", "innovative", "pivotal", "enhance", "leverage", "foster"]
ARTIFACTS = r"(contentReference\[oaicite|oaicite:\d|turn\d+search\d+|\[cite:\s*\d+\]|\[span_\d+\]\(start_span\)|【\d+†L?\d|\[attached_file:\d+\]|grok_card)"
PATENT_SUBJECTIVE = ["所特有", "现有技术均未", "完美", "彻底解决", "显著优于", "首创", "独有", "实测", "热力图显示"]
REPORT_ZH = ["本周主要开展了", "主要开展了以下工作", "取得了阶段性进展", "取得了阶段性成果", "有序推进", "下一步将继续",
             "进一步优化", "存在的问题及解决措施", "取得了较好的效果"]
TECH_EN = ["blazing fast", "blazing-fast", "powerful", "out of the box", "contributions are welcome", "enterprise-grade",
           "lightning fast", "effortless", "effortlessly"]
ACAD_EN = ["a novel", "towards", "unlocking", "extensive experiments", "state-of-the-art", "paving the way",
           "superiority", "comprehensive experiments"]
ACAD_ZH = ["新颖的", "大量实验表明", "充分证明", "优越性", "提供了新思路", "具有重要的理论意义和应用价值"]
# 单个破折号；数字之间的连接号（GB/T 7713.2—2022、2019—2024）不算
SINGLE_DASH = r"(?<!—)(?<!\d)—(?!—)|(?<=\d)—(?![\d—])"
SYMBOLS = r"[→✅✔✨🚀⚡🔥💡📌👉•]"
HEAD_RX = [
    (r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$", None),
    (r"^\s*\\((?:sub){0,2})section\*?\{(.+?)\}", None),
    (r"^\s*([一二三四五六七八九十]+、)\s*([^。；]{1,30})$", 1),
    (r"^\s*(（[一二三四五六七八九十]+）)\s*([^。；]{1,30})$", 2),
]


def read_text(path):
    p = Path(path)
    if p.suffix.lower() == ".docx":
        try:
            import docx  # python-docx
        except ImportError:
            sys.exit("python-docx is not installed; export the .docx to .txt or .md first.")
        return "\n".join(par.text for par in docx.Document(str(p)).paragraphs)
    return p.read_text(encoding="utf-8", errors="replace")


def is_zh(text):
    return len(re.findall(r"[\u4e00-\u9fff]", text)) >= len(re.findall(r"[A-Za-z]", text)) / 3


def strip_markup(line):
    line = re.sub(r"`[^`]*`", "", line)
    line = re.sub(r"\$[^$]*\$", "", line)
    return re.sub(r"\\cite\{[^}]*\}|\[[^\]]*\]\([^)]*\)", "", line)


def sentences(text, zh):
    parts = re.split(r"(?<=[。！？；])" if zh else r"(?<=[.!?])\s+", text)
    return [s.strip() for s in parts if len(s.strip()) > 1]


def slen(s, zh):
    return len(re.findall(r"[\u4e00-\u9fff]", s)) if zh else len(s.split())


def units(text):
    return len(re.findall(r"[\u4e00-\u9fff]", text)) + len(re.findall(r"[A-Za-z]+", text))


def heading(line):
    for rx, level in HEAD_RX:
        m = re.match(rx, line)
        if m:
            if level is None:
                g = m.group(1) or ""
                level = len(g) if g.startswith("#") else g.count("sub") + 1
            return level, m.group(2).strip()
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--genre", default="", choices=["", "academic-en", "academic-zh", "patent", "report",
                                                    "technical", "letter", "essay"])
    args = ap.parse_args()
    raw = read_text(args.file)
    hits = []  # (line, group, label, detail)
    add = lambda n, g, label, d="": hits.append((n, g, label, d))

    for m in re.finditer(ARTIFACTS, raw):
        add(raw[:m.start()].count("\n") + 1, "内容", "工具标记残留", m.group(0)[:20])
    for m in re.finditer("[\u202f\u00a0\u200b]", raw):
        add(raw[:m.start()].count("\n") + 1, "排版", "不可见字符（U+202F / U+00A0 / U+200B）：换成普通空格")
        break

    in_code, paragraphs, buf, en_words = False, [], [], []
    heads, bullets, label_lines, dashes = [], [], [], []  # heads: (line, level, title, body_text)
    for n, line in enumerate(raw.splitlines(), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or line.strip().startswith(("|", "<!--", "---")):
            continue
        h = heading(line)
        if h:
            if buf:
                paragraphs.append(buf)
                buf = []
            heads.append([n, h[0], h[1], ""])
            if re.search(SYMBOLS, h[1]):
                add(n, "结构", "标题里有 emoji / 符号", h[1][:20])
            words = re.findall(r"[A-Za-z][\w'-]*", h[1])
            if len(words) >= 4 and not is_zh(h[1]) and all(w[0].isupper() for w in words if len(w) > 3):
                add(n, "结构", "英文标题全部首字母大写（按期刊模板判断）", h[1][:30])
            continue
        text = strip_markup(line)
        if not text.strip():
            if buf:
                paragraphs.append(buf)
                buf = []
            continue
        text_first = not buf
        buf.append((n, text))
        if heads:
            heads[-1][3] += text + "\n"
        if re.match(r"^\s*([-*+]|\d+[.)])\s+", line):
            bullets.append(n)
        if re.match(r"^\s*([-*+]|\d+[.)])?\s*\*\*[^*]+\*\*\s*[:：]", line):
            label_lines.append(n)
        zh = is_zh(text)
        low = text.lower()
        if zh:
            for ph in ZH_PHRASES:
                if ph in text:
                    add(n, "AI 痕迹", "套话 / AI 高频词", ph)
            for ph in ZH_TONE:
                if ph in text:
                    add(n, "AI 痕迹", "表演式语气 / 客服腔", ph)
            for rx, label in ZH_PATTERNS:
                for m in re.finditer(rx, text):
                    add(n, "结构" if "维度" in label else "AI 痕迹", label, m.group(0)[:24])
            for rx, label in ZH_VAGUE:
                for m in re.finditer(rx, text):
                    add(n, "内容", label, m.group(0)[:16])
            for rx, label in ZH_LINE_PATTERNS:
                if (label != "段首无指代的评论句" or text_first) and re.search(rx, text):
                    add(n, "AI 痕迹", label)
            if text.count("的") >= 4 and len(text) < 120:
                add(n, "可读性", "『的』过多", f"{text.count('的')} 个")
            if len(re.findall(r"、", text)) >= 5:
                add(n, "AI 痕迹", "顿号并列过密", f"{text.count('、')} 个")
            if re.search(r"[\u4e00-\u9fff][,;:?!]|[,;:?!][\u4e00-\u9fff]|[\u4e00-\u9fff]\([\u4e00-\u9fff]", text):
                add(n, "排版", "中文句子里用了半角标点")
            if re.search(SINGLE_DASH + r"|[\u4e00-\u9fff]\s?--\s?[\u4e00-\u9fff]", text):
                add(n, "排版", "中文破折号应写作两字宽『——』")
            if re.search(r"……\s*等|\.\.\.\s*等", text):
                add(n, "排版", "省略号不和『等』连用")
            if re.search(r"[！!]{2,}|[？?][！!][？?]", text):
                add(n, "排版", "标点重复")
        else:
            en_words.extend(re.findall(r"[a-z']+", low))
            for ph in EN_PHRASES:
                if re.search(r"\b" + re.escape(ph) + r"\b", low):
                    add(n, "AI 痕迹", "AI-frequent phrase", ph)
            for rx, group, label in EN_PATTERNS:
                for m in re.finditer(rx, low):
                    add(n, group, label, m.group(0)[:30])
        if "——" in text or "—" in text:
            dashes.extend([n] * (text.count("——") + len(re.findall(SINGLE_DASH, text))))
        if text.count("**") >= 4:
            add(n, "AI 痕迹", "加粗过多")
        if re.search(SYMBOLS, text) and not re.match(r"^\s*[-*+]\s", line):
            add(n, "排版", "符号代替文字（→ ✅ • emoji）")
        if args.genre == "academic-en" and not zh:
            if re.search(r";\s+[a-z]", text):
                add(n, "文体", "IEEE: prose semicolon")
            if re.search(r"\b\w+n't\b|\b(it's|we're|they're|that's)\b", low):
                add(n, "文体", "contraction")
            for m in re.finditer(r"\b(proves?|guarantees?|clearly demonstrates?|establishes that)\b", low):
                add(n, "内容", "claim stronger than evidence?", m.group(0))
            for w in ACAD_EN:
                if re.search(r"\b" + re.escape(w) + r"\b", low):
                    add(n, "文体", "advertising word in title/abstract/caption?", w)
            if re.match(r"^\s*(fig\.|figure|table)\s*[\dIVX]+", low) and re.search(r"clearly|superior|demonstrat|showcas|comprehensive|crucial|outperform", low):
                add(n, "文体", "caption interprets instead of describing")
        if args.genre == "academic-zh" and zh:
            for w in ACAD_ZH:
                if w in text:
                    add(n, "文体", "论文套话 / 无度量修饰", w)
            if re.match(r"^\s*(图|表)\s*\d", text) and re.search(r"证明|优越|显著|充分", text):
                add(n, "文体", "图表题在下结论，改为描述内容")
        if args.genre == "report":
            for w in REPORT_ZH:
                if w in text:
                    add(n, "文体", "周报套话：换成对象 + 数字 + 日期", w)
            if re.match(r"^\s*(谢谢|谢谢聆听|感谢聆听|Q\s*&\s*A|Thank you!?|Questions\??|敬请指正)[。.!！]?\s*$", text, re.I):
                add(n, "文体", "以致谢 / 提问页收尾：换成请求和待决事项")
        if args.genre == "technical" and not zh:
            for w in TECH_EN:
                if w in low:
                    add(n, "文体", "README hype：换成数字、命令或限制", w)
            if re.match(r"^\s*(update|fix|change|modify)\s+[\w./-]+\s*$", low):
                add(n, "文体", "提交信息只说了改了哪个文件")
        if args.genre == "patent":
            if re.search(r"(按|根据|由|如)?式\s*[（(]\s*\d+[a-z]?\s*[）)]", text):
                add(n, "文体", "专利：『式（n）』远引，改为就地『如下式所示』")
            for w in PATENT_SUBJECTIVE:
                if w in text:
                    add(n, "内容", "专利：主观或绝对化断言", w)
            if re.search(r"(我们|我)", text):
                add(n, "文体", "专利：第一人称")
    if buf:
        paragraphs.append(buf)

    body_all = "\n".join(t for p in paragraphs for _, t in p)
    total = max(units(body_all), 1)

    # 结构：标题
    for i, (n, level, title, body) in enumerate(heads):
        nxt = heads[i + 1] if i + 1 < len(heads) else None
        if nxt and nxt[1] > level and not body.strip():
            continue  # 父标题直接接子标题
        zh = is_zh(body or title)
        sc = len(sentences(re.sub(r"^\s*([-*+]|\d+[.)])\s+", "", body, flags=re.M), zh)) if body.strip() else 0
        if args.genre != "technical" and sc < 2 and (nxt or body.strip()):
            add(n, "结构", "小节正文不足两句：并入相邻段落或删去标题", title[:20])
        kids = []
        for m in heads[i + 1:]:
            if m[1] <= level:
                break
            kids.append(m[1])
        if kids and kids.count(min(kids)) == 1:
            add(n, "结构", "这一级只有一个子标题：不分，或补齐", title[:20])
    if len(heads) >= 4 and total / len(heads) < 75:
        add(0, "结构", "标题过密", f"{len(heads)} 个标题 / 约 {total} 字词")
    dim_heads = [h for h in heads if re.search(r"层面|维度|方面|角度|视角|篇$|perspective|dimension|front$", h[2], re.I)]
    if len(dim_heads) >= 2:
        add(dim_heads[0][0], "结构", "标题按维度切片（技术层面 / 应用层面…）", f"{len(dim_heads)} 个")

    # 结构：列表、标签、破折号
    min_labels = 6 if args.genre == "technical" else 3
    if len(label_lines) >= min_labels:
        add(label_lines[0], "结构", "『**标签**：内容』式行过多", f"{len(label_lines)} 行")
    if len(bullets) >= 8 and total / len(bullets) < 25 and args.genre not in ("technical", "report"):
        add(bullets[0], "结构", "要点过密：论证、取舍写成段落", f"{len(bullets)} 条 / 约 {total} 字词")
    if dashes:
        rate = len(dashes) * 1000 / total
        if len(dashes) >= 3 or (len(dashes) >= 2 and rate >= 3):
            add(dashes[0], "AI 痕迹", "破折号 / em dash 偏多",
                f"{len(dashes)} 处，约每千字词 {rate:.1f}；行 {', '.join(map(str, sorted(set(dashes))[:6]))}")

    if en_words:
        per_k = 1000 / max(len(en_words), 1)
        for w in EN_DENSITY_WORDS:
            c = en_words.count(w)
            if c >= 3 and c * per_k >= 3:
                add(0, "AI 痕迹", "high density of a common word", f"{w} ×{c}")

    # 中英间空格是否统一
    tight = len(re.findall(r"[\u4e00-\u9fff][A-Za-z0-9]|[A-Za-z0-9][\u4e00-\u9fff]", body_all))
    spaced = len(re.findall(r"[\u4e00-\u9fff] [A-Za-z0-9]|[A-Za-z0-9] [\u4e00-\u9fff]", body_all))
    if tight >= 3 and spaced >= 3:
        add(0, "排版", "中英文之间的空格不统一", f"有空格 {spaced} 处，无空格 {tight} 处")

    prose = [p for p in paragraphs if units("".join(t for _, t in p)) >= 15]
    if prose:
        first_text = prose[0][0][1]
        if re.search(ZH_OPENING, first_text) or re.search(EN_OPENING, first_text.lower()):
            add(prose[0][0][0], "AI 痕迹", "背景式开头：换成造成问题的具体事实（专利、开题按惯例保留一句）")

    for para in paragraphs:
        body = "".join(t for _, t in para)
        zh = is_zh(body)
        first = para[0][0]
        dims = re.findall(ZH_DIM, body) if zh else re.findall(EN_DIM, body.lower())
        if len(dims) >= 3:
            add(first, "结构", "维度切片：『从 A 层面…从 B 层面…』，改成按因果和主次组织", f"{len(dims)} 处")
        sl = [slen(s, zh) for s in sentences(body, zh)]
        hedges = (sum(body.count(h) for h in ["可能", "也许", "或许", "似乎", "在一定程度上"]) if zh else
                  len(re.findall(r"\b(may|might|could|possibly|perhaps|somewhat|arguably|relatively)\b", body.lower())))
        if sl and hedges >= max(3, len(sl) // 2):
            add(first, "内容", "限定语堆叠 / stacked hedges", f"{hedges} 处")
        if any(x > (60 if zh else 40) for x in sl):
            add(first, "可读性", "超长句 / very long sentence", f"最长 {max(sl)}")

    if not hits:
        print("未发现常见问题。脚本只看表面模式；内容层（立场、证据、虚假平衡）仍需人工通读。")
        return
    order = {"内容": 0, "结构": 1, "AI 痕迹": 2, "文体": 3, "排版": 4, "可读性": 5}
    print(f"{args.file}: {len(hits)} 处提示（逐条判断，不必全改；命中不代表是 AI 写的）")
    for g in sorted({h[1] for h in hits}, key=lambda x: order.get(x, 9)):
        print(f"\n[{g}]")
        for n, _, label, detail in sorted((h for h in hits if h[1] == g), key=lambda h: h[0]):
            loc = f"L{n}" if n else "全文"
            print(f"  {loc:>6}  {label}" + (f"  [{detail}]" if detail else ""))


if __name__ == "__main__":
    main()
