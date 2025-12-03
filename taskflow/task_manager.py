import sqlite3
from datetime import datetime

class Database:
    """Класс для работы с базой данных"""
    
    def __init__(self, db_name='tasks.db'):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Таблица проектов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица задач
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'к выполнению',
                priority TEXT DEFAULT 'средний',
                project_id INTEGER,
                assignee TEXT,
                due_date TEXT,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id),
                UNIQUE(title, project_id)
            )
        ''')
        
        # Таблица комментариев
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                author TEXT,
                text TEXT,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (task_id) REFERENCES tasks (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query, params=()):
        """Выполнение запроса"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Database error: {e}")
            return False
    
    def fetch_all(self, query, params=()):
        """Получение всех записей"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.close()
        return result
    
    def fetch_one(self, query, params=()):
        """Получение одной записи"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return result

class TaskManager:
    """Основной класс для управления задачами"""
    
    def __init__(self):
        self.db = Database()
    
    # Проекты
    def create_project(self, name, description=""):
        """Создание нового проекта"""
        query = "INSERT INTO projects (name, description) VALUES (?, ?)"
        return self.db.execute_query(query, (name, description))
    
    def get_all_projects(self):
        """Получение всех проектов"""
        query = "SELECT * FROM projects ORDER BY created_date DESC"
        results = self.db.fetch_all(query)
        projects = []
        for row in results:
            projects.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'created_date': row[3]
            })
        return projects
    
    def delete_project(self, project_id):
        """Удаление проекта"""
        # Сначала удаляем все задачи проекта
        self.db.execute_query("DELETE FROM tasks WHERE project_id = ?", (project_id,))
        # Затем удаляем проект
        self.db.execute_query("DELETE FROM projects WHERE id = ?", (project_id,))
    
    # Задачи
    def create_task(self, title, project_id, description="", assignee="", priority="средний", due_date=None):
        """Создание новой задачи"""
        # Проверка на дубликаты
        check_query = "SELECT id FROM tasks WHERE title = ? AND project_id = ?"
        existing_task = self.db.fetch_one(check_query, (title, project_id))
        
        if existing_task:
            return False
        
        query = """INSERT INTO tasks (title, description, project_id, assignee, priority, due_date) 
                   VALUES (?, ?, ?, ?, ?, ?)"""
        return self.db.execute_query(query, (title, description, project_id, assignee, priority, due_date))
    
    def get_tasks_by_project(self, project_id):
        """Получение задач по проекту"""
        query = "SELECT * FROM tasks WHERE project_id = ? ORDER BY created_date DESC"
        results = self.db.fetch_all(query, (project_id,))
        tasks = []
        for row in results:
            tasks.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'status': row[3],
                'priority': row[4],
                'project_id': row[5],
                'assignee': row[6],
                'due_date': row[7],
                'created_date': row[8]
            })
        return tasks
    
    def get_all_tasks(self):
        """Получение всех задач"""
        query = """SELECT t.*, p.name as project_name 
                   FROM tasks t 
                   LEFT JOIN projects p ON t.project_id = p.id 
                   ORDER BY t.created_date DESC"""
        return self.db.fetch_all(query)
    
    def update_task_status(self, task_id, new_status):
        """Обновление статуса задачи"""
        query = "UPDATE tasks SET status = ? WHERE id = ?"
        self.db.execute_query(query, (new_status, task_id))
    
    def delete_task(self, task_id):
        """Удаление задачи"""
        # Сначала удаляем комментарии задачи
        self.db.execute_query("DELETE FROM comments WHERE task_id = ?", (task_id,))
        # Затем удаляем задачу
        self.db.execute_query("DELETE FROM tasks WHERE id = ?", (task_id,))
    
    def task_exists(self, title, project_id):
        """Проверка существования задачи"""
        query = "SELECT id FROM tasks WHERE title = ? AND project_id = ?"
        result = self.db.fetch_one(query, (title, project_id))
        return result is not None
    
    # Комментарии
    def add_comment(self, task_id, author, text):
        """Добавление комментария к задаче"""
        query = "INSERT INTO comments (task_id, author, text) VALUES (?, ?, ?)"
        return self.db.execute_query(query, (task_id, author, text))
    
    def get_comments(self, task_id):
        """Получение комментариев задачи"""
        query = "SELECT * FROM comments WHERE task_id = ? ORDER BY created_date DESC"
        results = self.db.fetch_all(query, (task_id,))
        comments = []
        for row in results:
            comments.append({
                'id': row[0],
                'task_id': row[1],
                'author': row[2],
                'text': row[3],
                'created_date': row[4]
            })
        return comments
    
    def delete_comment(self, comment_id):
        """Удаление комментария"""
        self.db.execute_query("DELETE FROM comments WHERE id = ?", (comment_id,))