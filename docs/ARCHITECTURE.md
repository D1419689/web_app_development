# 系統架構設計：任務管理系統

## 1. 技術架構說明

根據本專案的 PRD 需求，我們採用輕量、穩定且開發迅速的技術棧，確保能在掌控效能的同時打造具備現代美感的操作介面。

- **後端框架**：**Python + Flask**
  - **原因**：Flask 是輕量級的 Web 框架，適合中小型應用程式或 API 服務。具有簡單明瞭的結構，開發迅速且容易修改。
- **模板引擎**：**Jinja2**
  - **原因**：Flask 的預設模板引擎，可以在 HTML 中嵌入 Python 語法進行渲染。因為我們不採用複雜的前後端分離框架，所以透過 Jinja2 將後端資料在伺服器端直接組裝成 HTML 頁面回傳，大幅簡化實作難度。
- **資料庫**：**SQLite (透過 SQLAlchemy ORM)**
  - **原因**：SQLite 無須額外安裝伺服器軟體，所有資料存放於單一檔案 (`.db`) 中，極度適合 MVP (最小可行性產品) 和個人用途。搭配 SQLAlchemy 作為 ORM (物件關聯對映)，可以用 Python 語法操作資料庫，提升安全性與程式可讀性。
- **前端呈現**：**Vanilla CSS & Vanilla JavaScript**
  - **原因**：為了實現高質感、獨具特色的 UI 設計與動態微動畫（Micro-animations），我們決定不仰賴 Bootstrap 或 Tailwind 等現成框架，而是透過原生的 CSS 自行佈署 Design System。同時，引入輕量的原生 JavaScript 搭配 Fetch API 來處理按鍵點擊、任務打勾等互動，使用戶不需一直刷新頁面。

### MVC 模式說明
本專案的程式結構對應了經典的 MVC (Model-View-Controller) 概念：
- **Model (資料庫模型)**：`models/` 資料夾下的程式碼，負責定義諸如 `Task`, `Category` 等資料表的結構與邏輯。
- **View (視圖)**：`templates/` 資料夾下的 Jinja2 HTML 檔案，結合 `static/` 下的樣式表負責最終要呈現給使用者的視覺呈現。
- **Controller (控制器)**：`routes/` 資料夾下的 Flask 路由。負責接收瀏覽器的請求 (如新增任務)，呼叫 Model 更新資料庫，然後再請 View 負責渲染更新後的畫面回傳。

---

## 2. 專案資料夾結構

為保持專案的可維護性，同時遵循 Flask 開發的最佳實踐，檔案將以此目錄結構進行切割：

```text
web_app_development-1/
│
├── app/                      # 應用程式主目錄
│   ├── __init__.py           # Flask 初始化檔案 (建立 app 實例與資料庫連線)
│   ├── models/               # Model：定義 DB Schema 與關聯
│   │   ├── __init__.py
│   │   └── task.py           # 負責任務、分類等資料表實體設計
│   │
│   ├── routes/               # Controller：定義應用程式的進入點與邏輯
│   │   ├── __init__.py
│   │   └── main.py           # 主要頁面的 HTTP 請求處理 (GET/POST)
│   │
│   ├── templates/            # View：Jinja2 所需的 HTML 模板
│   │   ├── base.html         # 母版 (定義共用排版、Navigation bar)
│   │   ├── index.html        # 任務首頁
│   │   └── dashboard.html    # (可選) 視覺化圖表與數據總覽頁面
│   │
│   └── static/               # 前端靜態資源
│       ├── css/
│       │   └── style.css     # 客製化層疊樣式表 (色彩、動畫、排版)
│       └── js/
│           └── script.js     # JavaScript (負責處理刪除互動、非同步更新與視圖效果)
│
├── instance/                 # 預設建立的執行個體目錄
│   └── database.db           # SQLite 資料庫檔案本身 (應設定 .gitignore 排除)
│
├── docs/                     # 專案系統設計文件庫
│   ├── PRD.md                # 產品需求文件
│   └── ARCHITECTURE.md       # 本文件
│
├── requirements.txt          # Python 第三方套件依賴清單
└── run.py                    # 啟動應用程式的主進入點
```

---

## 3. 元件關係圖

以下展示使用者透過瀏覽器發送請求時，後端各層級與資料庫系統之間的互動順序：

```mermaid
flowchart TD
    Client[Browser (User Interface)]
    
    subgraph 伺服器端
        Router(Flask App Router)
        Controller[Routes - Controllers]
        Model[SQLAlchemy Models]
        View[Jinja2 Templates]
        Database[(SQLite)]
    end
    
    Client -- "1. 發送請求 (如: 點擊完成)" --> Router
    Router -- "2. 轉交對應邏輯" --> Controller
    Controller -- "3. 更新或查詢" --> Model
    Model <--> "4. SQL 交互" Database
    Model -- "5. 回傳 Python 物件" --> Controller
    Controller -- "6. 傳遞變數" --> View
    View -- "7. 生成完整 HTML" --> Controller
    Controller -- "8. 回應網頁或 JSON" --> Client
```

---

## 4. 關鍵設計決策

1. **使用 Jinja2 搭配輕量 AJAX (Fetch API) 漸進式增強**
   - **原因**：為了在追求快速原型開發的同時，仍然給予使用者優良的無縫體驗。頁面初始化與複雜資料仍由 Jinja2 渲染，但諸如「標記任務完成」或「刪除任務」等頻繁且輕量的單一互動，我們會透過 JS 的 Fetch API 呼叫後端路由，並直接在網頁畫面上用 JavaScript 加入動態刪除的效果，避免不必要的重新整理帶給用戶鈍挫感。
2. **集中式的靜態資產與 Vanilla CSS**
   - **原因**：為確保達到設計上高彈性且高品質視覺效果的追求，決定不導入像 Bootstrap 這類排版制式化的套件。取而代之的是，我們會設計一個專注於留白比例、簡潔字體及過渡動畫的 Modern Web 原生 CSS 庫，令產品質感大幅提升。
3. **App Factory 架構模式**
   - **原因**：利用 `app/__init__.py` 來實作工廠模式（App Factory）生成 Flask 實例，而不是把所有啟動邏輯都塞在其餘檔案中。這樣能讓資料庫擴充 (SQLAlchemy 初始化) 與其他擴充模組更為獨立，日後要為這個專案寫測試也會簡單許多。
4. **模組化的 Models 與 Routes 分離**
   - **原因**：將 `routes` 與 `models` 各立為資料夾，目的是隨著需求變大（即使現階段只是開發單人用的 MVP 任務系統），能避免所有的邏輯代碼纏繞在同一個超巨型檔案裡，達到關注點分離。
