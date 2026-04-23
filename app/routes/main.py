from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.models.task import Task
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    任務列表頁面
    可透過 URL 查詢參數 ?status=xxx 來過濾任務 (all, active, completed)
    """
    status = request.args.get('status', 'all')
    tasks = Task.get_all()
    
    if status == 'active':
        tasks = [t for t in tasks if not t.is_completed]
    elif status == 'completed':
        tasks = [t for t in tasks if t.is_completed]
        
    return render_template('index.html', tasks=tasks, current_status=status)

@main_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    建立新任務
    接收表單資料 (title, due_date 等)，驗證後存入資料庫，並重導向回首頁
    """
    title = request.form.get('title')
    due_date_str = request.form.get('due_date')
    
    if not title or not title.strip():
        flash('任務名稱不能為空', 'error')
        return redirect(url_for('main.index'))
        
    data = {'title': title.strip()}
    
    if due_date_str:
        try:
            # 假設表單傳來的是 YYYY-MM-DD 格式
            data['due_date'] = datetime.strptime(due_date_str, '%Y-%m-%d')
        except ValueError:
            flash('日期格式錯誤', 'error')
            return redirect(url_for('main.index'))
            
    task = Task.create(data)
    if task:
        flash('任務建立成功', 'success')
    else:
        flash('任務建立失敗', 'error')
        
    return redirect(url_for('main.index'))

@main_bp.route('/tasks/<int:id>/update', methods=['POST'])
def update_task(id):
    """
    更新任務狀態
    接收表單或 JSON 請求來切換任務的完成狀態，並回傳結果或重導向
    """
    # 支援 fetch API (JSON) 與普通表單
    if request.is_json:
        data = request.get_json()
        is_completed = data.get('is_completed')
        
        updated_task = Task.update(id, {'is_completed': bool(is_completed)})
        if updated_task:
            return jsonify({'success': True, 'is_completed': updated_task.is_completed})
        return jsonify({'success': False, 'message': 'Task not found'}), 404
    else:
        # 傳統表單
        is_completed = request.form.get('is_completed') == 'on'
        updated_task = Task.update(id, {'is_completed': is_completed})
        if not updated_task:
            flash('找不到指定的任務', 'error')
        return redirect(url_for('main.index'))

@main_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """
    刪除特定任務
    自資料庫中移除任務後，回傳 JSON 成功訊息或重導向回首頁
    """
    success = Task.delete(id)
    
    if request.is_json:
        if success:
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Task not found'}), 404
    else:
        if success:
            flash('任務已刪除', 'success')
        else:
            flash('刪除失敗，找不到指定任務', 'error')
        return redirect(url_for('main.index'))

@main_bp.route('/dashboard')
def dashboard():
    """
    數據總覽頁面
    顯示任務完成進度、統計圖表等
    """
    tasks = Task.get_all()
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.is_completed)
    active_tasks = total_tasks - completed_tasks
    
    progress = 0
    if total_tasks > 0:
        progress = int((completed_tasks / total_tasks) * 100)
        
    stats = {
        'total': total_tasks,
        'completed': completed_tasks,
        'active': active_tasks,
        'progress': progress
    }
    
    return render_template('dashboard.html', stats=stats)
