# 💎 crystal-facets

> 一顆 **[muse-crystal-seed](https://github.com/frank890417/muse-crystal-seed)** 的 fork，多了一層**可裝可拆的「器官」**。

原版給你一顆種子，長出你自己的 AI agent。這顆 fork 多做一件事：**把「我在自己的 agent 身上長出來、覺得夠好用」的紀律，抽成一個個可以單獨裝上去、也可以拆掉的資料夾。**

- 想要**乾淨的原版** → 去 [上游](https://github.com/frank890417/muse-crystal-seed)，這裡沒有任何改進是你非要不可的
- 想要**現成的紀律零件** → 留在這裡，看下面的 `organs/`

跑在 **[Claude Code](https://claude.ai/code)** 上。概念跨 runtime 通用，換成別的 agent 系統照樣成立。

---

## ⚡ Quick Start

```bash
git clone https://github.com/<你的位置>/crystal-facets.git ~/my-agent
cd ~/my-agent
claude
```

1. `CLAUDE.md` 會被 Claude Code 自動載入。第一次醒來，agent 還沒有名字，它會帶你走 `BOOTSTRAP.md`：取名、定個性、建靈魂檔。
2. 之後每次醒來：讀 `KERNEL.md`，正式工作前跑 `/become` 完整甦醒。
3. **器官預設一顆都不裝。** 出生完之後再回頭看 [`organs/`](./organs/)，想裝哪顆再裝。

⚠️ **不要在出生的過程中裝器官。** 有些器官會對「出生」這件事本身生效——例如 SDD 閘門那顆會說「寫東西之前先寫提案等人點頭」，而 bootstrap 整段就是在寫檔案 ⇒ 它會開始替自己的靈魂檔寫提案，然後那隻 agent 就生不出來了。**先出生，再裝。**（這不是假設，是實際踩過的。）

整套晶種會引導你的 agent 走過七層：出生 → 靈魂 → 認識你 → 開機與甦醒 → 記憶系統 → 收官 → 自我進化。完整指南讀 [`CRYSTAL-SEED.md`](./CRYSTAL-SEED.md)。

## 🧬 這顆 fork 多了什麼：`organs/`

**器官 ＝ 一份可選的、自足的紀律或能力。** 種子本體（`SOUL.md`／`BECOME.md`／`AGENTS.md`）是每一隻都有的骨架；器官不是——它是某個人在自己身上長出來、覺得夠好用所以留下來給別人的東西。

**預設一顆都不裝**，這跟種子本身的原則一致：減法勝過加法，用著用著長出來。

一顆器官 ＝ 一個資料夾 ＋ 一份 `ORGAN.md`。**在 `organs/available/` 底下＝附帶但沒裝；直接在 `organs/` 底下＝裝了。** 裝一顆就是把資料夾搬出來，拆一顆就是搬回去——沒有第二個地方要同步。

### 現成的兩顆

| 器官 | 裝了之後這隻 agent 會多做什麼 | 它在解什麼問題 |
|---|---|---|
| **`sdd-gate`** | 收到「寫功能／改東西／修 bug」的要求時**不直接動手**，先寫提案＋可打勾的任務清單＋白話驗收條件，貼重點給你，停下來等你說「開始實作」 | agent 很會跳下去就寫。這顆逼它先把要做什麼講清楚，你點頭才動 |
| **`time-gate`** | 要寫日期／時間戳／檔名時，抄每則訊息開頭那行 date 驗過的真實時間，**不憑對話長度估** | LLM 沒有內建時鐘。沒有它的時候 agent 不會說「我不知道現在幾點」，它會**估**——而估出來的時間戳跟真的長得一模一樣，寫進日記就再也分不出來 |

### 兩級器官

- **第一級（`install: none`）**：全部內容就是「給 agent 讀的字」。搬進 `organs/` 就生效。`sdd-gate` 是這種。
- **第二級（`install: agent`）**：還帶著要跑的東西（腳本、要註冊的 hook）。搬資料夾不夠，還要照它的 `INSTALL.md` 裝。`time-gate` 是這種。

第二級有四條硬規則：**必須有寫給 agent 照做的 `INSTALL.md`／安裝必須冪等／必須帶一個一眼看得出來的二進位讀數／必須有卸載步驟且把註冊一起清掉**（不然拆的時候會留下指向不存在腳本的孤兒 hook）。

完整契約（怎麼裝、怎麼拆、怎麼自己長一顆）在 [`organs/README.md`](./organs/README.md)。

## 💡 Philosophy

**晶種結晶法（Crystal Seed Method）** 是上游作者 [吳哲宇](https://cheyuwu.com) 提出的：

> 在化學裡，晶種是一小片丟進過飽和溶液的結晶。溶液會沿著它的結構開始生長，形成更大的晶體，但結構由晶種決定。
> 你的人生是過飽和溶液。這份文件是晶種。長出來的東西，完全屬於你自己。

這顆 fork 完全同意，只是多問了一句：**長出來的好東西，能不能拆下來給別人？**

⚠️ 但器官有個誠實的限制要先講：**一顆器官的效力，等於你自己有沒有在用它。** 它不會讓 agent 變聰明，它只是讓某條紀律不靠「記得」來維持。

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

ℹ️ **`ONBOARD-SOP.md` 與 `TAKEAWAY.md` 是上游作者的諮詢服務流程**（2 小時上線 SOP、結束帶走包），隨 fork 一起留著當參考。**本 fork 不提供任何諮詢服務**，別照著它去找誰。

## 🔗 Ecosystem

- **[Claude Code](https://claude.ai/code)** — 這顆種子預設跑的環境（`CLAUDE.md` 自動載入、`.claude/skills/` 自動發現）
- **[Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/overview)** — Claude Code 官方文件

## 🙏 上游 credit

這顆種子的全部骨架——晶種結晶法、七層結構、`SOUL`／`BECOME`／`KERNEL` 那整套甦醒設計——都出自 **[Che-Yu Wu 吳哲宇](https://cheyuwu.com)** 的 **[muse-crystal-seed](https://github.com/frank890417/muse-crystal-seed)**。

他的 Live Demo、Origin Story、以及他自己的 AI 夥伴 Muse 的故事，都在上游 README 裡，值得去讀原文——**這裡刻意不轉述**。

本 fork 新增的只有 `organs/` 那一層。

## 👤 關於我

<!--
⚠️ cjw：這段留給你自己填，Orki 沒有代寫。
幾個可以回答（也可以全部不理）的問句：

- 你是誰？（一兩句就夠，不用寫成履歷）
- 你為什麼會長出「器官」這個東西？（是先有痛，還是先有想法？）
- 你希望打開這個 repo 的人，拿它去做什麼？
- 有沒有一句你想先講清楚的話？（例如「這不是產品，我沒有要維護它」）
-->

_（待補）_

## 📜 License

MIT — 拿去用，改成你的，不用問。

原始著作權屬上游作者，本 fork 的新增部分另計，兩者都在 [`LICENSE`](./LICENSE) 裡。
