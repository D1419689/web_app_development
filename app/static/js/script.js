// 切換任務完成狀態
async function toggleTask(taskId, isCompleted) {
    try {
        const response = await fetch(`/tasks/${taskId}/update`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ is_completed: isCompleted })
        });
        
        if (response.ok) {
            const result = await response.json();
            const taskElement = document.querySelector(`.task-item[data-id="${taskId}"]`);
            
            if (result.is_completed) {
                taskElement.classList.add('completed');
            } else {
                taskElement.classList.remove('completed');
            }
        } else {
            // 如果失敗，回復 checkbox 的狀態
            const checkbox = document.getElementById(`task-${taskId}`);
            checkbox.checked = !isCompleted;
            alert('更新狀態失敗，請稍後再試。');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('網路錯誤，請稍後再試。');
    }
}

// 刪除任務
async function deleteTask(taskId) {
    if (!confirm('確定要刪除這個任務嗎？')) {
        return;
    }
    
    try {
        const response = await fetch(`/tasks/${taskId}/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const taskElement = document.querySelector(`.task-item[data-id="${taskId}"]`);
            // 觸發移除動畫
            taskElement.classList.add('removing');
            
            // 等待動畫結束後從 DOM 移除
            setTimeout(() => {
                taskElement.remove();
                
                // 如果是最後一個任務，可能需要重新整理來顯示 empty state
                const remainingTasks = document.querySelectorAll('.task-item');
                if (remainingTasks.length === 0) {
                    window.location.reload();
                }
            }, 300);
        } else {
            alert('刪除失敗，請稍後再試。');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('網路錯誤，請稍後再試。');
    }
}

// 自動關閉 Flash 訊息
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            setTimeout(() => alert.remove(), 500);
        }, 3000);
    });
});
