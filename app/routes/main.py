from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    任務列表頁面
    可透過 URL 查詢參數 ?status=xxx 來過濾任務 (all, active, completed)
    """
    pass

@main_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    建立新任務
    接收表單資料 (title, due_date 等)，驗證後存入資料庫，並重導向回首頁
    """
    pass

@main_bp.route('/tasks/<int:id>/update', methods=['POST'])
def update_task(id):
    """
    更新任務狀態
    接收表單或 JSON 請求來切換任務的完成狀態，並回傳結果或重導向
    """
    pass

@main_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """
    刪除特定任務
    自資料庫中移除任務後，回傳 JSON 成功訊息或重導向回首頁
    """
    pass

@main_bp.route('/dashboard')
def dashboard():
    """
    數據總覽頁面
    顯示任務完成進度、統計圖表等
    """
    pass
