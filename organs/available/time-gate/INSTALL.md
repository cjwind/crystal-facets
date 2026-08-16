# INSTALL — time-gate

> **這份是寫給 agent 照做的，不是寫給人讀的。** 你（agent）照著跑，人負責在第 3 步點頭。
> 契約規矩見 [`organs/README.md`](../../README.md) §第二級器官、§改別人的 `settings.json` 的規矩。

## 前置檢查（不通過就停，不要裝一半）

```bash
command -v bash date printf
```

三個都在就可以裝。**這顆器官不需要 python3、不需要 jq。**

⚠️ 但你**自己**在下面第 2 步要合併 JSON。用你手邊任何可靠的方式都行（直接編輯檔案也行），只是別把「合併 JSON 的工具」變成這顆器官的依賴——**使用者的機器上有沒有那個工具，跟這顆器官裝不裝得起來無關。**

## 安裝

### 步驟 0 — 確認器官在正確位置

```bash
ls organs/time-gate/time-gate.sh
```

看不到 ⇒ 它可能還在 `organs/available/time-gate/`。**先把資料夾搬進 `organs/`**（那是第一級的動作，contract 規定的），再回來繼續。

```bash
chmod +x organs/time-gate/time-gate.sh
```

⚠️ 沒有執行權限是**安靜失敗**的典型來源：hook 註冊得好好的，就是什麼都不發生。

### 步驟 1 — 讀現有的 `.claude/settings.json`

```bash
cat .claude/settings.json
```

三種情況，全部都要能處理：

| 你看到什麼 | 怎麼辦 |
|---|---|
| 檔案不存在 | 新建，內容就是下面那塊「要加的東西」 |
| 有檔案，但**沒有 `hooks` 這個 key** | 新增 `hooks` key（一顆全新的種子就是這種） |
| 有 `hooks`，甚至已經有 `UserPromptSubmit` | **加進去，不是取代** —— 見下面 ⚠️ |

### 步驟 1.5 — 冪等檢查（已經裝過就停在這裡）

```bash
grep -c "time-gate.sh" .claude/settings.json
```

**不是 0 ⇒ 已經註冊過了。跟使用者說一聲「已經裝好了」，然後跳到〈驗證〉。**
⛔ 不要再加一條。重複註冊不會報錯，它只是讓 hook 每則訊息跑兩次、輸出重複兩行。

### 步驟 2 — 產生合併後的內容

要加的東西是這一條：

```json
{
  "type": "command",
  "command": "bash \"$CLAUDE_PROJECT_DIR/organs/time-gate/time-gate.sh\"",
  "timeout": 10
}
```

它要放進 `hooks.UserPromptSubmit[].hooks[]` 陣列裡。完整長相（假設原本什麼都沒有）：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR/organs/time-gate/time-gate.sh\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

⚠️⚠️ **使用者原本就有 `UserPromptSubmit` hook 的話，是把上面那一條 append 進既有的 `hooks` 陣列，不是把整個陣列換掉。**

這是這整份文件最容易犯、後果最嚴重的錯，因為**被蓋掉的東西不會報錯**——它只是從此不再發生，而使用者要等到某天發現「咦我那個怎麼沒作用了」才知道。

`$CLAUDE_PROJECT_DIR` 要照抄，**不要換成你當下的絕對路徑**——它會跟著專案走，而 hook 的執行目錄不見得是你以為的那個。

### 步驟 3 — 給人看過，他點頭才寫

**把合併後的完整 `settings.json` 印出來給使用者看，等他同意，才寫進去。**

不是形式主義：這是他的設定檔，而合併這個動作是有可能出錯的（步驟 2 那個 ⚠️ 就是這樣來的）。**唯一有能力看出「這不是我原本那條」的人是他。**

## 驗證（二進位讀數 —— 不做這步就不算裝完）

**開一個新的 session，隨便說一句話。下一則訊息的開頭應該出現：**

```
🕐 現在（date 驗）：2026-08-16 (週日) 12:19 CST　←要寫日期／時間戳就抄這一行…
```

- **看得到那行** → 裝好了。
- **看不到** → 就是沒裝好，不要當成「可能有生效」。依序查：① 腳本有沒有執行權限 ② 路徑對不對（`ls` 一下 `organs/time-gate/time-gate.sh`）③ 註冊有沒有寫進 `hooks.UserPromptSubmit`（不是別的事件）④ 手動跑 `echo '{}' | bash organs/time-gate/time-gate.sh` 看有沒有吐出 JSON。

⚠️ **必須是新 session。** 已經開著的 session 不會重讀設定檔——在舊 session 裡看不到那行，不代表沒裝好。

## 卸載

> ⚠️ **這一段假設你可能已經把資料夾刪掉了。** 拆器官的人通常照第一級的直覺「把資料夾搬走」就當拆完了，結果留下一個**指向不存在腳本的孤兒 hook**，每一則訊息都踩一次。
> **先清註冊，再處理資料夾。** 順序反了也救得回來，照這段做就是。

### 1. 清掉註冊（最重要，別跳過）

```bash
grep -n "time-gate.sh" .claude/settings.json
```

有命中 ⇒ 把那一條 `{"type": "command", "command": "...time-gate.sh...", ...}` 從 `hooks.UserPromptSubmit[].hooks[]` 陣列裡移除。

**⚠️ 只移除這一條，使用者其他的 hook 一個都不能動。**

移除之後如果某個容器變成空的，把空殼一起清掉，不要留骨架：

- 某個 `{"hooks": []}` 變空 → 移除這個物件
- `UserPromptSubmit` 陣列變空 → 移除這個 key
- `hooks` 物件變空 → 移除 `hooks` key（回到裝之前的樣子）

同樣**寫進去之前給使用者看一眼**。

### 2. 處理資料夾

留著以後再裝：`mv organs/time-gate organs/available/`
不留了：刪掉 `organs/time-gate/`

### 3. 確認沒留孤兒

```bash
grep -c "time-gate" .claude/settings.json
```

**要是 0。** 然後開一個新 session 說句話 —— **那行時間不再出現，而且沒有任何錯誤訊息**。

有錯誤訊息 ⇒ 註冊還在但腳本沒了，回第 1 步。
