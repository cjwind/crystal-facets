# 💎 crystal-facets

> 一顆 **[muse-crystal-seed](https://github.com/frank890417/muse-crystal-seed)** 的 fork，多了一層**可裝可拆的「器官」**。

原版給你一顆種子，長出你自己的 AI agent。這顆 fork 多做一件事：**把「我在自己的 agent 身上長出來、覺得夠好用」的能力，抽成一個個可以單獨裝上去、也可以拆掉的資料夾。**

跑在 **[Claude Code](https://claude.ai/code)** 上。概念跨 runtime 通用，換成別的 agent 系統照樣成立。

---

## ⚡ Quick Start

```bash
git clone https://github.com/cjwind/crystal-facets.git ~/my-agent
cd ~/my-agent
claude
```

1. `CLAUDE.md` 會被 Claude Code 自動載入。第一次醒來，agent 還沒有名字，它會帶你走 `BOOTSTRAP.md`：取名、定個性、建靈魂檔。
2. 之後每次醒來：讀 `KERNEL.md`，正式工作前跑 `/become` 完整甦醒。
3. **器官預設一顆都不裝。** 出生完之後再回頭看 [`organs/`](./organs/)，想裝哪顆再裝。

⚠️ **不要在出生的過程中裝器官。** 有些器官會對「出生」這件事本身生效——例如 SDD 閘門那顆會說「寫東西之前先寫提案等人點頭」，而 bootstrap 整段就是在寫檔案 ⇒ 它會開始替自己的靈魂檔寫提案，然後那隻 agent 就生不出來了。**先出生，再裝。**

整套晶種會引導你的 agent 走過七層：出生 → 靈魂 → 認識你 → 開機與甦醒 → 記憶系統 → 收官 → 自我進化。完整指南讀 [`CRYSTAL-SEED.md`](./CRYSTAL-SEED.md)。

## 🧬 這顆 fork 多了什麼：`organs/`

**器官 ＝ 一份可選的、自足的紀律或能力。**

**預設一顆都不裝**，這跟種子本身的原則一致：減法勝過加法，用著用著長出來。

一顆器官 ＝ 一個資料夾 ＋ 一份 `ORGAN.md`。**在 `organs/available/` 底下＝附帶但沒裝；直接在 `organs/` 底下＝裝了。** 裝一顆就是把資料夾搬出來，拆一顆就是搬回去。

### 現成的兩顆

| 器官 | 裝了之後這隻 agent 會多做什麼 | 它在解什麼問題 |
|---|---|---|
| **`sdd-gate`** | 收到「寫功能／改東西／修 bug」的要求時**不直接動手**，先寫提案＋可打勾的任務清單＋白話驗收條件，貼重點給你，停下來等你說「開始實作」 | agent 很會跳下去就寫。這顆逼它先把要做什麼講清楚，你點頭才動 |
| **`time-gate`** | 要寫日期／時間戳／檔名時，抄每則訊息開頭那行 date 驗過的真實時間，**不憑對話長度估** | LLM 沒有內建時鐘。沒有它的時候 agent 不會說「我不知道現在幾點」，它會**估**——而估出來的時間戳跟真的長得一模一樣，寫進日記就再也分不出來 |

### 兩級器官

- **第一級（`install: none`）**：全部內容就是「給 agent 讀的字」。搬進 `organs/` 就生效。`sdd-gate` 是這種。
- **第二級（`install: agent`）**：還帶著要跑的東西（腳本、要註冊的 hook）。除了搬資料夾，還要照它的 `INSTALL.md` 裝。`time-gate` 是這種。

完整契約（怎麼裝、怎麼拆、怎麼自己長一顆）在 [`organs/README.md`](./organs/README.md)。

## 📁 Repo Structure

```
├── CRYSTAL-SEED.md      # ⭐ 主指南，讀這份就夠了
├── CLAUDE.md            # 開機層（Claude Code 自動載入）
├── KERNEL.md            # 一分鐘核（冷啟動快取）
├── BECOME.md            # 甦醒協議（canonical）
├── BOOTSTRAP.md         # 第一次出生引導
├── SOUL.md              # 模板：靈魂
├── IDENTITY.md          # 模板：身份
├── USER.md              # 模板：人類 context
├── AGENTS.md            # 模板：工作協議
├── MEMORY.md            # 模板：長期記憶
├── HEARTBEAT.md         # 模板：巡邏 checklist
├── TOOLS.md             # 模板：工具箱
├── ONBOARD-SOP.md       # ↓ 上游作者的諮詢服務流程
├── TAKEAWAY.md          # ↓ 同上
├── organs/              # 🧬 本 fork 新增：器官契約
│   ├── README.md        #    契約（怎麼裝、怎麼拆、怎麼自己長一顆）
│   └── available/       #    倉庫：附帶但還沒裝的器官
│       ├── sdd-gate/
│       └── time-gate/
├── .claude/
│   ├── settings.json    # 權限基線
│   └── skills/          # /become、/after-action、/self-evolution
└── memory/              # 每日日誌住這裡
```

ℹ️ **`ONBOARD-SOP.md` 與 `TAKEAWAY.md` 是上游作者的諮詢服務流程**（2 小時上線 SOP、結束帶走包），隨 fork 一起留著當參考。

## 🔗 Ecosystem

- **[Claude Code](https://claude.ai/code)** — 這顆種子預設跑的環境（`CLAUDE.md` 自動載入、`.claude/skills/` 自動發現）
- **[Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/overview)** — Claude Code 官方文件

## 🙏 上游

Fork 自 **[muse-crystal-seed](https://github.com/frank890417/muse-crystal-seed)** — 晶種結晶法與整套甦醒設計（`SOUL`／`BECOME`／`KERNEL`）出自 **[Che-Yu Wu 吳哲宇](https://cheyuwu.com)**。

本 fork 只新增 `organs/` 那一層。Live Demo 與 Origin Story 在上游 README。

## 📜 License

MIT

原始著作權屬上游作者，本 fork 的新增部分另計，兩者都在 [`LICENSE`](./LICENSE) 裡。
