#!/usr/bin/env python3
"""grep-recall — UserPromptSubmit hook：每則訊息把「可能相關的記憶卡標題」注進 agent 的 context。

零依賴（只用 Python 3 標準函式庫）。沒有模型、沒有向量、沒有快取、沒有狀態。

它做的事：把你打的那句話切成詞，去卡庫裡找哪幾張卡沾得上邊，把那幾張的**標題那一行**
注進 agent 的 context。就這樣——不注入整張卡（context 是每則訊息都在付的稅）。

⚠️ 它的效力等於你自己的卡庫。沒寫卡就什麼都不會發生，而且那是正常的。

防呆鐵則：任何狀況都 exit 0。召回失敗頂多是沒推，絕不能害使用者發不出話。
"""

import json
import os
import re
import sys
import glob
import math

# ── 可以調的三個東西，全部在這裡 ──────────────────────────────────────

# 卡庫在哪（相對於專案根目錄）。環境變數 GREP_RECALL_CARDS 可覆寫成絕對路徑。
CARDS_SUBDIR = os.path.join('memory', 'cards')

# 門檻：最高分低於這個數字 → 一張都不出。
# ⚠️ 4.0 是對「某一個人的卡庫」調出來的，不是普世常數。怎麼看出該不該調：
#   一直什麼都沒出來 → 太緊，調低（3.0 試試）
#   一直冒出不相關的 → 太鬆，調高（5.0 試試）
MIN_TOP_SCORE = 4.0

# 一次最多注入幾張。超過會明講「還有 N 張沒列」，不做沉默截斷。
MAX_CARDS = 5

# 停用詞：太常見、沒有鑑別度的詞。
# ⚠️ 這份是對中文＋英文混用的卡庫調出來的，**不是普世清單**。
#    你的卡庫如果總是被某個常見詞拉出一堆不相關的卡，就把那個詞加進來。
STOP = {
    '今天', '明天', '昨天', '天天', '現在', '目前', '今年', '最近', '剛剛',
    '然後', '因為', '所以', '可是', '但是', '還有', '還是', '而且', '或是',
    '一個', '這個', '那個', '什麼', '怎麼', '為什', '自己', '我們', '你們',
    '他們', '可以', '想要', '覺得', '知道', '一下', '一直', '有點', '比較',
    '幫我', '看一', '一樣', '一些', '一點', '這樣', '那樣', '這些', '那些',
    '一起', '一定', '需要', '應該',
    '我看', '你看', '這是', '那是', '個嗎', '以幫', '下這',
    'the', 'and', 'for', 'you', 'are', 'with', 'this', 'that', 'have',
}

# ── 以下不用改 ────────────────────────────────────────────────────────

CJK = r'一-鿿'


def cjk_bigrams(s):
    """中文沒有空白可以切詞。bigram（相鄰兩字）是繞開斷詞器的辦法：
    「風浪板」→「風浪」「浪板」。查詢與卡片用同一套切法，就對得起來。"""
    out = []
    for run in re.findall(f'[{CJK}]+', s):
        if len(run) == 1:
            out.append(run)
        else:
            out += [run[i:i + 2] for i in range(len(run) - 1)]
    return out


def terms(q):
    """ascii 單字（2 字以上）＋ CJK bigram － 停用詞。"""
    ascii_words = [w.lower() for w in re.findall(r'[A-Za-z0-9]{2,}', q)]
    return {t for t in set(ascii_words + cjk_bigrams(q)) if t not in STOP}


def cards_dir():
    override = os.environ.get('GREP_RECALL_CARDS')
    if override:
        return override
    root = (os.environ.get('CLAUDE_PROJECT_DIR')
            or os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))))
    return os.path.join(root, CARDS_SUBDIR)


def strip_frontmatter(text):
    """卡片可以有 YAML frontmatter，也可以沒有。有的話跳過再取標題。"""
    if text.startswith('---'):
        m = re.match(r'^---\n.*?\n---[ \t]*\n', text, re.S)
        if m:
            return text[m.end():].lstrip('\n')
    return text


def load_cards():
    """一張卡 ＝ 一個 .md 檔，第一行是標題。讀不到就當沒有這張，不吵。"""
    out = []
    for path in sorted(glob.glob(os.path.join(cards_dir(), '*.md'))):
        try:
            with open(path, encoding='utf-8') as f:
                text = strip_frontmatter(f.read())
        except OSError:
            continue
        title = (text.splitlines()[0].lstrip('# ').strip()
                 if text.strip() else os.path.basename(path))
        out.append((os.path.basename(path)[:-3], title, title.lower(),
                    text.lower()))
    return out


def idf(qterms, cards):
    """一個詞出現在越多張卡 → 越沒有鑑別度 → 權重越低。壓掉共詞噪音。"""
    n = len(cards) or 1
    return {t: math.log((n + 1) / (sum(1 for _, _, _, b in cards if t in b) + 1)) + 1.0
            for t in qterms}


def score(qterms, weights, title_l, body_l):
    """單卡的分數：命中標題算 3 分、命中內文算 1 分、沒命中 0 分，各乘 IDF 加總。
    標題權重高，是因為卡的標題本來就該是那張卡的 claim 本身。"""
    return sum(weights[t] * (3 if t in title_l else (1 if t in body_l else 0))
               for t in qterms)


def search(query):
    qterms = terms(query)
    if not qterms:
        return [], 0
    cards = load_cards()
    if not cards:
        return [], 0
    weights = idf(qterms, cards)
    scored = [(s, title, name)
              for name, title, title_l, body_l in cards
              for s in (score(qterms, weights, title_l, body_l),) if s > 0]
    scored.sort(key=lambda x: (-x[0], x[1]))
    # 門檻看的是「最高分」：整組都不夠相關的話，一張都不出。
    # 寧可安靜，也不要端半相關的東西上來——那比沒有更糟，它會污染判斷。
    if not scored or scored[0][0] < MIN_TOP_SCORE:
        return [], 0
    return scored[:MAX_CARDS], len(scored)


def main():
    try:
        payload = json.load(sys.stdin)
        query = payload.get('prompt', '')
    except Exception:
        return 0
    if not query.strip():
        return 0

    try:
        hits, total = search(query)
    except Exception:
        return 0
    if not hits:
        return 0

    lines = [f'[{s:.1f}] {title}  «{name}»' for s, title, name in hits]
    if total > len(hits):
        lines.append(f'（還有 {total - len(hits)} 張也命中了，沒列出來）')

    ctx = ('🧠 召回（可能相關的記憶卡。**這是線索不是事實**——'
           '卡記的是寫當下為真，用之前先開原檔驗；不相關就忽略）：\n'
           + '\n'.join(lines))

    print(json.dumps({'hookSpecificOutput': {
        'hookEventName': 'UserPromptSubmit',
        'additionalContext': ctx,
    }}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
