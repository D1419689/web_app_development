# 系統與使用者流程圖 (Flowchart)：任務管理系統

## 1. 使用者流程圖 (User Flow)

這張圖展示了使用者進入系統後，所能進行的所有操作。為確保互動流暢（參考我們在架構設計中決定使用 JS Vanilla 輔助），許多操作（如打勾完成、刪除）將在畫面上立即回饋，不須重新載入整個頁面。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Home[首頁 - 任務儀表板]
    
    Home --> Action{要執行什麼操作？}
    
    %% 新增功能
    Action -->|新增任務| AddInput[輸入名稱與截止日]
    AddInput --> AddSubmit([點擊「新增」按鈕])
    AddSubmit --> Home
    
    %% 切換完成
    Action -->|切換狀態| ToggleCheck([點擊任務前的 Checkbox])
    ToggleCheck -.->|JS Fetch 更新後台| ToggleMark[UI 加上或移除完成刪除線]
    ToggleMark --> Home
    
    %% 刪除功能
    Action -->|刪除任務| ClickDelete([點擊任務旁的「垃圾桶按鈕」])
    ClickDelete -.->|JS Fetch 更新後台| RemoveItem[UI 動態移除該列]
    RemoveItem --> Home
    
    %% 搜尋過濾功能
    Action -->|搜尋任務| TypeSearch[在搜尋欄輸入關鍵字]
    TypeSearch --> SearchUI[列出標題符合的任務]
    SearchUI --> Home
    
    %% 分類與篩選
    Action -->|篩選視圖| FilterClick([點選「全部/未完成/已完成」])
    FilterClick --> FilterUI[切換清單內容]
    FilterUI --> Home
```

---

## 2. 系統序列圖 (Sequence Diagram)

以下以「**使用者新增任務**」這個較完整的操作為例，展示前端瀏覽器、Flask 路由、SQLAlchemy Model 與 SQLite 資料庫之間的資料流向。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 使用者瀏覽器 (JS/HTML)
    participant Flask as Flask Route
    participant Model as SQLAlchemy Model
    participant DB as SQLite
    
    User->>Browser: 填寫表單並點擊「新增」
    Browser->>Flask: POST /api/tasks (帶有 JSON 資料)
    Flask->>Flask: 檢查欄位 (如標題是否為空)
    
    alt 資料不合法
        Flask-->>Browser: 400 Bad Request (回傳錯誤訊息)
        Browser-->>User: 畫面顯示「任務名稱未填寫」警告
    else 資料合法
        Flask->>Model: 建立 Task 實例 (title, due_date...)
        Model->>DB: INSERT INTO tasks (...)
        DB-->>Model: 寫入成功
        Model-->>Flask: 回傳存檔的 Task 資訊
        Flask-->>Browser: 201 Created (回報成功與任務 JSON)
        Browser->>Browser: JavaScript 操作 DOM 插入新任務
        Browser-->>User: 畫面即時浮現剛新增的任務清單
    end
```

---

## 3. 功能清單與路由對照表

以下表格定義了主要功能會對應到的後端路由 (URL Paths) 與 HTTP Methods。

| 系統功能 | HTTP 方法 | URL 路徑 | 功能說明 | 前置動作 (觸發條件) |
| --- | --- | --- | --- | --- |
| 初始載入 | GET | `/` | 由 Jinja2 渲染完整的 HTML 首頁，包含目前的任務與統計進度。 | 首次進入網站 或 畫面重整 |
| 新增任務 | POST | `/api/tasks` | 接收表單資料，並存入資料庫。 | 點擊新增按鈕送出 |
| 切換完成狀態 | PATCH | `/api/tasks/<id>/status` | 根據任務 `<id>`，將其設定為已完成或未完成狀態。 | 點擊 Checkbox |
| 刪除指定任務 | DELETE | `/api/tasks/<id>` | 根據任務 `<id>`，從資料庫中刪除該筆資料。 | 點擊刪除按鈕 |
| 篩選任務列表 | GET | `/api/tasks?status=...&q=...` | (可選)若資料龐大時交由後端篩選，回傳符合條件的資料；若資料少也可由前端原生 JS 隱藏。 | 輸入文字或切換頁籤 |

備註：利用 `/api/` 作為前綴能清楚區分「回傳靜態 HTML」與「回傳 JSON 供 JS 非同步操作」的路由職責。
