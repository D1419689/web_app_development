# 路由設計文件：任務管理系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 任務列表 | GET | / | templates/index.html | 顯示所有任務，可透過查詢參數篩選 (如 `/?status=completed`) |
| 建立任務 | POST | /tasks | — | 接收表單（標題、到期日），存入 DB 後重導向回首頁 |
| 更新任務狀態 | POST | /tasks/<int:id>/update | — | 透過 Fetch API 接收狀態變更，更新 DB 後回傳 JSON 或重導向 |
| 刪除任務 | POST | /tasks/<int:id>/delete | — | 刪除指定任務，刪除後重導向回首頁 |
| 數據總覽 | GET | /dashboard | templates/dashboard.html | 顯示進度統計、未完成/已完成任務比例 |

## 2. 每個路由的詳細說明

### `GET /` (任務列表)
- **輸入**：可選的 URL 查詢參數 `status` (all, active, completed)
- **處理邏輯**：從資料庫查詢對應狀態的任務列表，並根據建立時間或到期日排序。
- **輸出**：渲染 `index.html`，傳遞 `tasks` 變數與目前 `status`。
- **錯誤處理**：無。

### `POST /tasks` (建立任務)
- **輸入**：表單欄位 `title` (任務名稱)、`due_date` (到期日)、`category_id` (分類，可選)。
- **處理邏輯**：驗證 `title` 是否空白。建立新的 Task Model 實例並寫入資料庫。
- **輸出**：成功後重導向至 `/`。
- **錯誤處理**：如果標題為空，重導向回 `/` 並帶有錯誤訊息（使用 flash 訊息）。

### `POST /tasks/<int:id>/update` (更新任務狀態)
- **輸入**：表單或 JSON 包含 `is_completed` 布林值。
- **處理邏輯**：在資料庫尋找對應的 Task，更新 `is_completed` 欄位並儲存。
- **輸出**：為了配合前端的 Fetch API 動態更新，可回傳 JSON 成功訊息；如果是一般表單提交則重導向 `/`。
- **錯誤處理**：找不到任務則回傳 404。

### `POST /tasks/<int:id>/delete` (刪除任務)
- **輸入**：無。
- **處理邏輯**：從資料庫刪除指定的 Task。
- **輸出**：回傳 JSON 成功訊息或重導向 `/`。
- **錯誤處理**：找不到任務則回傳 404。

### `GET /dashboard` (數據總覽)
- **輸入**：無。
- **處理邏輯**：統計今日新增、總任務數、已完成任務數等指標。
- **輸出**：渲染 `dashboard.html`，傳遞統計數據變數。
- **錯誤處理**：無。

## 3. Jinja2 模板清單

需要建立以下 HTML 模板，均放在 `app/templates/` 目錄中：

1. **`base.html`**
   - 包含共用頭部 (HTML head)、導覽列 (Navigation Bar)、以及引入靜態資源 (`style.css`, `script.js`)。
   - 所有其他頁面將透過 `{% extends "base.html" %}` 繼承此模板。
2. **`index.html`**
   - 繼承 `base.html`。
   - 包含新增任務的表單、任務列表區塊、以及狀態篩選按鈕。
3. **`dashboard.html`**
   - 繼承 `base.html`。
   - 顯示任務完成率與統計圖表的視覺化介面。
