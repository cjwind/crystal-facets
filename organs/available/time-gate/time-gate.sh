#!/usr/bin/env bash
# time-gate — UserPromptSubmit hook：每則訊息把「date 驗過的真實時間」注進 agent 的 context。
#
# 為什麼：LLM 沒有內建時鐘。沒有這個東西的時候，它會憑「對話變長 ≈ 過了多久」估時間，
# 而估出來的時間戳長得跟真的一模一樣——寫進日記、檔名、紀錄裡就再也分不出來了。
# 這支 hook 不糾正那個習慣，它讓那個習慣沒有存在的理由：時間就在眼前，抄就好。
#
# 設計原則：
#   - 只「餵」事實，不「擋」。它不改寫 agent 寫的任何東西，時間戳仍然是 agent 自己寫的。
#   - 任何狀況都 exit 0。餵時間失敗頂多是沒推，絕不能害使用者發不出話。
#   - 零依賴：只用 bash + date + printf。不需要 python、jq 或任何第三方工具。

# ── 時區設定 ────────────────────────────────────────────────────────────
# 預設跟隨系統時區（不設定就是這樣，多數人要的就是這個）。
# 想釘死一個時區（例如你的 agent 會在雲端跑、那邊是 UTC，但你要看自己的當地時間）：
#   方法 A：設環境變數  export ORGAN_TIME_GATE_TZ='Asia/Taipei'
#   方法 B：改下面這一行  TZ_DEFAULT='Asia/Taipei'
# 兩個都沒設 → 系統時區。IANA 時區名清單：https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TZ_DEFAULT=''

# ── 以下不用改 ──────────────────────────────────────────────────────────

# UserPromptSubmit 會從 stdin 餵 JSON 進來。這支 hook 用不到，但要把管子讀掉，
# 否則寫入端可能吃到 SIGPIPE。
cat >/dev/null 2>&1

tz="${ORGAN_TIME_GATE_TZ:-$TZ_DEFAULT}"

if [ -n "$tz" ]; then
  now="$(TZ="$tz" date '+%Y-%m-%d (%A) %H:%M %Z' 2>/dev/null)"
else
  now="$(date '+%Y-%m-%d (%A) %H:%M %Z' 2>/dev/null)"
fi

# 時區名打錯時 date 不見得會失敗，它可能安靜地回 UTC。這裡只保證「拿不到就閉嘴」。
[ -z "$now" ] && exit 0

# 手寫 JSON：$now 來自 date 的格式字串，不含雙引號或反斜線，直接內插是安全的。
printf '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"🕐 現在（date 驗）：%s　←要寫日期／時間戳就抄這一行，不要憑對話長度估。需要秒級精度再自己跑 date。"}}\n' "$now"

exit 0
