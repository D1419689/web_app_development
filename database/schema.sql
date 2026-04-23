-- 任務資料表
CREATE TABLE task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT 0,
    due_date DATETIME,
    category_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
