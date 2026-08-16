# INSTALL — grep-recall

> **這份是寫給 agent 照做的，不是寫給人讀的。** 你（agent）照著跑，人負責在第 3 步點頭。
> 契約規矩見 [`organs/README.md`](../../README.md) §第二級器官、§改別人的 `settings.json` 的規矩。

## 前置檢查（不通過就停，不要裝一半）

```bash
command -v python3 && python3 -c "import json,re,glob,math; print('ok')"
```

**印不出 `ok` ⇒ 這台機器裝不了這顆器官。** 跟使用者說清楚「你的機器上沒有 python3，這顆裝不起來」，**然後就停在這裡**——不要註冊 hook、不要留下任何半殘的東西。

（只用標準函式庫，不需要 pip install 任何東西。）

⚠️ 你**自己**在下面第 2 步要合併 JSON。用你手邊任何可靠的方式都行，只是別把那個工具變成這顆器官的依賴。**不管用什麼方式，都要保留原檔的排版**：縮排、鍵的順序、**還有檔尾那個換行**——整個檔重新序列化會讓它在 `git diff` 裡整段變動，而且卸載之後回不到裝之前的樣子。

## 安裝

### 步驟 0 — 確認器官在正確位置，並準備卡庫

```bash
ls organs/grep-recall/grep-recall.py
```

看不到 ⇒ 它可能還在 `organs/available/grep-recall/`。**先把資料夾搬進 `organs/`**，再回來繼續。

```bash
chmod +x organs/grep-recall/grep-recall.py
mkdir -p memory/cards
```

⚠️ 沒有執行權限是**安靜失敗**的典型來源：hook 註冊得好好的，就是什麼都不發生。

ℹ️ **卡庫預設在 `memory/cards/`**，空的也沒關係——沒有卡的時候這顆器官什麼都不做，那是正常狀態。要換位置就改 `grep-recall.py` 頂端的 `CARDS_SUBDIR`，或設環境變數 `GREP_RECALL_CARDS`。

### 步驟 1 — 讀現有的 `.claude/settings.json`

```bash
cat .claude/settings.json
```

三種情況，全部都要能處理：

| 你看到什麼 | 怎麼辦 |
|---|---|
| 檔案不存在 | 新建，內容就是下面那塊 |
| 有檔案，但**沒有 `hooks` 這個 key** | 新增 `hooks` key（一顆全新的種子就是這種） |
| 有 `hooks`，甚至已經有 `UserPromptSubmit` | **加進去，不是取代** —— 見下面 ⚠️ |

### 步驟 1.5 — 冪等檢查（已經裝過就停在這裡）

```bash
grep -c "grep-recall.py" .claude/settings.json
```

**不是 0 ⇒ 已經註冊過了。跟使用者說一聲「已經裝好了」，然後跳到〈驗證〉。**
⛔ 不要再加一條。重複註冊不會報錯，它只會讓同一批卡片被推兩次。

### 步驟 2 — 產生合併後的內容

要加的是這一條：

```json
{
  "type": "command",
  "command": "python3 \"$CLAUDE_PROJECT_DIR/organs/grep-recall/grep-recall.py\"",
  "timeout": 10
}
```

放進 `hooks.UserPromptSubmit[].hooks[]` 陣列裡。完整長相（假設原本什麼都沒有）：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/organs/grep-recall/grep-recall.py\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

⚠️⚠️ **使用者原本就有 `UserPromptSubmit` hook 的話，是把上面那一條 append 進既有的 `hooks` 陣列，不是把整個陣列換掉。**

**被蓋掉的東西不會報錯**——它只是從此不再發生，而使用者要等到某天發現「咦我那個怎麼沒作用了」才知道。

`$CLAUDE_PROJECT_DIR` 要照抄，不要換成你當下的絕對路徑。

### 步驟 3 — 給人看過，他點頭才寫

**把合併後的完整 `settings.json` 印出來給使用者看，等他同意，才寫進去。**

這是他的設定檔，而合併這個動作是有可能出錯的。唯一有能力看出「這不是我原本那條」的人是他。

## 驗證（二進位讀數 —— 不做這步就不算裝完）

⚠️ **先講一件會害你誤判的事：這顆器官注入的東西，人看不到。**

hook 把卡片標題注進的是 **agent 的 context**，不是使用者的畫面。**在 Claude Code 裡，人不會在訊息裡看到那段「🧠 召回」——沒看到是正常的，不代表沒裝好。**

⇒ 讀數有兩個版本，看你是誰：

### 你是人：先放一張卡，再去問 agent

```bash
cp organs/grep-recall/example-cards/*.md memory/cards/
```

（`example-cards/` 裡有一中一英兩張現成的。你自己已經有卡的話，跳過這步。）

**開一個新的 session，問一句跟那張卡有關的話**，例如「我想買一個新的鍵盤」，然後問 agent：

> 「你這則訊息有收到召回的卡片嗎？有的話標題是什麼？」

- **它答得出那張卡的標題** → **裝好了。**
- **它說沒收到** → 沒裝好，往下看排錯。

### 你是 agent（甦醒時自檢用）

直接看你自己的 context：**這一則訊息裡有沒有那段「🧠 召回」開頭的東西。**

⚠️ **注意一個陷阱**：卡庫是空的、或這句話跟所有卡都沾不上邊時，**它本來就不會注入任何東西**——那是它正常運作，不是壞掉。所以自檢要用**一句你確定會命中的話**來測，不能拿隨便一句沒命中的來判它死了。

### 沒過的話，依序查

① 手動跑一次，看它有沒有吐出 JSON：

```bash
echo '{"prompt":"我想買一個新的鍵盤"}' | python3 organs/grep-recall/grep-recall.py
```

（什麼都沒印 ⇒ 可能是卡庫空的、或這句話沒過門檻，先確認 `memory/cards/` 裡真的有相關的卡。）

② 腳本有沒有執行權限 ③ 路徑對不對 ④ 註冊有沒有寫進 `hooks.UserPromptSubmit`（不是別的事件）⑤ 卡庫路徑對不對（預設 `memory/cards/`）。

⚠️ **必須是新 session。** 已經開著的 session 不會重讀設定檔。

ℹ️ 「人看不到那段」是在 **Claude Code** 上觀察到的行為。別的 harness 可能會顯示注入的 context——你那邊看得到的話，那也是一個有效的讀數，不衝突。

## 卸載

> ⚠️ **這一段假設你可能已經把資料夾刪掉了。** 拆器官的人通常照第一級的直覺「把資料夾搬走」就當拆完了，結果留下一個**指向不存在腳本的孤兒 hook**，每一則訊息都踩一次。
> **先清註冊，再處理資料夾。**

### 1. 清掉註冊（最重要，別跳過）

```bash
grep -n "grep-recall.py" .claude/settings.json
```

有命中 ⇒ 把那一條從 `hooks.UserPromptSubmit[].hooks[]` 陣列裡移除。**只移除這一條，使用者其他的 hook 一個都不能動。**

移除之後如果某個容器變成空的，把空殼一起清掉：`{"hooks": []}` 的物件 → 移除；`UserPromptSubmit` 陣列變空 → 移除這個 key；`hooks` 物件變空 → 移除 `hooks` key（回到裝之前的樣子）。

同樣**寫進去之前給使用者看一眼**。

### 2. 處理資料夾

留著以後再裝：`mv organs/grep-recall organs/available/`
不留了：刪掉 `organs/grep-recall/`

⚠️ **`memory/cards/` 不要動。** 那是使用者自己寫的東西，不是這顆器官的資產——器官走了，卡要留著。

### 3. 確認沒留孤兒

```bash
grep -c "grep-recall" .claude/settings.json
```

**要是 0。** 然後開一個新 session 說句話 —— **不再有召回，而且沒有任何錯誤訊息**。

有錯誤訊息 ⇒ 註冊還在但腳本沒了，回第 1 步。
