from app import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    due_date = db.Column(db.DateTime, nullable=True)
    category_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, data):
        """
        新增一筆任務記錄
        :param data: dict，包含 title, due_date 等欄位
        :return: 新增的 Task 實例或 None
        """
        try:
            task = cls(**data)
            db.session.add(task)
            db.session.commit()
            return task
        except Exception as e:
            db.session.rollback()
            print(f"Error creating task: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有任務記錄
        :return: Task 實例列表
        """
        try:
            return cls.query.order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"Error getting all tasks: {e}")
            return []

    @classmethod
    def get_by_id(cls, task_id):
        """
        取得單筆任務記錄
        :param task_id: 任務 ID
        :return: Task 實例或 None
        """
        try:
            return cls.query.get(task_id)
        except Exception as e:
            print(f"Error getting task by id: {e}")
            return None

    @classmethod
    def update(cls, task_id, data):
        """
        更新任務記錄
        :param task_id: 任務 ID
        :param data: dict，要更新的欄位與值
        :return: 更新後的 Task 實例或 None
        """
        try:
            task = cls.query.get(task_id)
            if task:
                for key, value in data.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                db.session.commit()
            return task
        except Exception as e:
            db.session.rollback()
            print(f"Error updating task: {e}")
            return None

    @classmethod
    def delete(cls, task_id):
        """
        刪除任務記錄
        :param task_id: 任務 ID
        :return: 布林值表示是否成功
        """
        try:
            task = cls.query.get(task_id)
            if task:
                db.session.delete(task)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting task: {e}")
            return False
