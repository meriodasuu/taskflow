import tkinter as tk
from tkinter import ttk, messagebox
from task_manager import TaskManager

class ModernTaskManagerGUI:
    """Современный интерфейс системы управления задачами"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("TaskFlow • Современный менеджер задач")
        self.root.geometry("1200x750")
        
        # Улучшенная цветовая палитра с лучшим контрастом
        self.colors = {
            'primary': '#6366F1',
            'primary_dark': '#4F46E5',
            'primary_light': '#8B5CF6',
            'bg_primary': '#0F0F0F',
            'bg_secondary': '#1A1A1A',
            'bg_surface': '#262626',
            'bg_card': '#2D2D2D',
            'bg_input': '#3A3A3A',  # Новый цвет для полей ввода
            'text_primary': '#FFFFFF',
            'text_secondary': '#E5E5E5',  # Более светлый для лучшей читаемости
            'text_muted': '#A0A0A0',
            'accent_green': '#10B981',
            'accent_red': '#EF4444',
            'accent_blue': '#3B82F6',
            'border': '#404040',
            'border_light': '#555555',
            'hover_light': '#363636'
        }
        
        # Настройка стиля окна
        self.root.configure(bg=self.colors['bg_primary'])
        self.setup_styles()
        
        self.manager = TaskManager()
        self.setup_ui()
        self.refresh_projects()
        self.refresh_all_tasks()
        
        # Адаптивность
        self.root.bind('<Configure>', self.on_resize)
    
    def setup_styles(self):
        """Настройка современных стилей с улучшенной видимостью"""
        style = ttk.Style()
        
        # Современная тема
        style.theme_use('clam')
        
        # Настройка вкладок
        style.configure('Modern.TNotebook',
                       background=self.colors['bg_primary'],
                       borderwidth=0)
        style.configure('Modern.TNotebook.Tab',
                       padding=[20, 10],
                       background=self.colors['bg_card'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0,
                       focuscolor='none')
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.colors['primary'])],
                 foreground=[('selected', 'white')])
        
        # Улучшенная настройка деревьев с лучшим контрастом
        style.configure('Modern.Treeview',
                       background=self.colors['bg_surface'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['bg_surface'],
                       borderwidth=0,
                       font=('Segoe UI', 10),
                       rowheight=25)
        style.configure('Modern.Treeview.Heading',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0,
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat')
        style.map('Modern.Treeview.Heading',
                 background=[('active', self.colors['primary_light'])])
        
        # Стиль для полей ввода
        style.configure('Modern.TCombobox',
                       fieldbackground=self.colors['bg_input'],
                       background=self.colors['bg_input'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       relief='flat')
        style.map('Modern.TCombobox',
                 fieldbackground=[('readonly', self.colors['bg_input'])],
                 background=[('readonly', self.colors['bg_input'])])
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Главный контейнер
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Заголовок
        self.setup_header(main_container)
        
        # Вкладки
        self.setup_tabs(main_container)
    
    def setup_header(self, parent):
        """Верхняя панель с улучшенным дизайном"""
        header = tk.Frame(parent, bg=self.colors['bg_secondary'], height=80)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)
        
        # Заголовок приложения
        title_frame = tk.Frame(header, bg=self.colors['bg_secondary'])
        title_frame.pack(side='left', padx=30, pady=20)
        
        # Основной заголовок с градиентным эффектом
        tk.Label(
            title_frame,
            text="TASKFLOW",
            font=('Segoe UI', 24, 'bold'),
            fg=self.colors['primary_light'],
            bg=self.colors['bg_secondary']
        ).pack(side='left')
        
        tk.Label(
            title_frame,
            text="• Современный менеджер задач",
            font=('Segoe UI', 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary']
        ).pack(side='left', padx=(15, 0), pady=4)
        
        # Кнопки действий
        action_frame = tk.Frame(header, bg=self.colors['bg_secondary'])
        action_frame.pack(side='right', padx=30, pady=20)
        
        self.create_modern_button(
            action_frame, "🔄 Обновить", 
            self.refresh_all_data, self.colors['primary']
        ).pack(side='left', padx=5)
        
        self.create_modern_button(
            action_frame, "➕ Проект", 
            self.show_create_project, self.colors['accent_green']
        ).pack(side='left', padx=5)
    
    def setup_tabs(self, parent):
        """Настройка системы вкладок"""
        self.notebook = ttk.Notebook(parent, style='Modern.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Вкладка проектов
        self.projects_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(self.projects_frame, text="📁 Проекты")
        self.setup_projects_tab()
        
        # Вкладка задач
        self.tasks_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(self.tasks_frame, text="✅ Задачи")
        self.setup_tasks_tab()
        
        # Вкладка комментариев
        self.comments_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(self.comments_frame, text="💬 Комментарии")
        self.setup_comments_tab()
    
    def setup_projects_tab(self):
        """Вкладка управления проектами с улучшенной видимостью"""
        # Сетка 2 колонки
        main_grid = tk.Frame(self.projects_frame, bg=self.colors['bg_primary'])
        main_grid.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Левая колонка - создание проекта
        left_frame = tk.Frame(main_grid, bg=self.colors['bg_primary'])
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        # Правая колонка - список проектов
        right_frame = tk.Frame(main_grid, bg=self.colors['bg_primary'])
        right_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
        
        main_grid.columnconfigure(0, weight=1)
        main_grid.columnconfigure(1, weight=1)
        main_grid.rowconfigure(0, weight=1)
        
        # Карточка создания проекта
        create_card = self.create_modern_card(left_frame, "Создать проект", "Добавление нового проекта")
        create_card.pack(fill='both', expand=True)
        
        # Форма создания проекта с улучшенными полями
        tk.Label(create_card, text="Название проекта:", 
                font=('Segoe UI', 10, 'bold'), fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).pack(anchor='w', pady=(0, 8))
        
        self.project_name_entry = self.create_modern_entry(create_card, "Введите название проекта")
        self.project_name_entry.pack(fill='x', pady=(0, 15))
        
        tk.Label(create_card, text="Описание проекта:", 
                font=('Segoe UI', 10, 'bold'), fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).pack(anchor='w', pady=(0, 8))
        
        self.project_desc_entry = self.create_modern_entry(create_card, "Необязательное описание")
        self.project_desc_entry.pack(fill='x', pady=(0, 25))
        
        self.create_modern_button(
            create_card, "🚀 Создать проект", 
            self.create_project, self.colors['accent_green']
        ).pack()
        
        # Карточка списка проектов
        list_card = self.create_modern_card(right_frame, "Мои проекты", "Список всех проектов")
        list_card.pack(fill='both', expand=True)
        
        # Таблица проектов с улучшенной видимостью
        tree_frame = tk.Frame(list_card, bg=self.colors['bg_card'])
        tree_frame.pack(fill='both', expand=True, pady=(15, 0))
        
        self.projects_tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Name', 'Description'),
            show='headings',
            height=12
        )
        
        self.projects_tree.config(style='Modern.Treeview')
        
        # Улучшенные заголовки колонок
        columns_config = [
            ('ID', 'ID', 80),
            ('Name', 'НАЗВАНИЕ ПРОЕКТА', 200),
            ('Description', 'ОПИСАНИЕ', 250)
        ]
        
        for col, text, width in columns_config:
            self.projects_tree.heading(col, text=text)
            self.projects_tree.column(col, width=width, anchor='center' if col == 'ID' else 'w')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.projects_tree.yview)
        self.projects_tree.configure(yscrollcommand=scrollbar.set)
        
        self.projects_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Кнопка удаления
        self.create_modern_button(
            list_card, "🗑️ Удалить проект", 
            self.delete_project, self.colors['accent_red']
        ).pack(pady=(15, 0))
    
    def setup_tasks_tab(self):
        """Вкладка управления задачами с улучшенным дизайном"""
        main_grid = tk.Frame(self.tasks_frame, bg=self.colors['bg_primary'])
        main_grid.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Левая колонка
        left_frame = tk.Frame(main_grid, bg=self.colors['bg_primary'])
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        # Правая колонка
        right_frame = tk.Frame(main_grid, bg=self.colors['bg_primary'])
        right_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
        
        main_grid.columnconfigure(0, weight=1)
        main_grid.columnconfigure(1, weight=1)
        main_grid.rowconfigure(0, weight=1)
        
        # Карточка создания задачи
        create_card = self.create_modern_card(left_frame, "Новая задача", "Создание задачи в проекте")
        create_card.pack(fill='both', expand=True)
        
        # Форма создания задачи с улучшенными полями
        fields = [
            ("Проект", "project_combo", "combobox"),
            ("Название задачи", "task_title", "entry"),
            ("Исполнитель", "task_assignee", "entry"),
            ("Приоритет", "task_priority", "combobox"),
        ]
        
        for label, attr, field_type in fields:
            tk.Label(create_card, text=label + ":", 
                    font=('Segoe UI', 10, 'bold'), fg=self.colors['text_primary'],
                    bg=self.colors['bg_card']).pack(anchor='w', pady=(0, 8))
            
            if field_type == 'entry':
                widget = self.create_modern_entry(create_card, f"Введите {label.lower()}")
            else:
                widget = ttk.Combobox(create_card, font=('Segoe UI', 10), style='Modern.TCombobox')
                if attr == 'project_combo':
                    widget.set("Выберите проект")
                elif attr == 'task_priority':
                    widget['values'] = ['низкий', 'средний', 'высокий']
                    widget.set('средний')
            
            setattr(self, attr, widget)
            widget.pack(fill='x', pady=(0, 15))
        
        self.create_modern_button(
            create_card, "🎯 Создать задачу", 
            self.create_task, self.colors['accent_green']
        ).pack()
        
        # Карточка управления задачами
        manage_card = self.create_modern_card(right_frame, "Управление задачами", "Список задач проекта")
        manage_card.pack(fill='both', expand=True)
        
        # Таблица задач с улучшенной видимостью
        tree_frame = tk.Frame(manage_card, bg=self.colors['bg_card'])
        tree_frame.pack(fill='both', expand=True, pady=(15, 0))
        
        self.tasks_tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Title', 'Status', 'Assignee', 'Priority'),
            show='headings',
            height=10
        )
        
        self.tasks_tree.config(style='Modern.Treeview')
        
        # Улучшенные заголовки колонок
        task_columns = [
            ('ID', 'ID', 80),
            ('Title', 'ЗАДАЧА', 200),
            ('Status', 'СТАТУС', 120),
            ('Assignee', 'ИСПОЛНИТЕЛЬ', 120),
            ('Priority', 'ПРИОРИТЕТ', 100)
        ]
        
        for col, text, width in task_columns:
            self.tasks_tree.heading(col, text=text)
            self.tasks_tree.column(col, width=width, anchor='center' if col == 'ID' else 'w')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tasks_tree.yview)
        self.tasks_tree.configure(yscrollcommand=scrollbar.set)
        
        self.tasks_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Панель управления с улучшенным дизайном
        control_frame = tk.Frame(manage_card, bg=self.colors['bg_card'])
        control_frame.pack(fill='x', pady=(15, 0))
        
        tk.Label(control_frame, text="Изменение статуса:", 
                font=('Segoe UI', 10, 'bold'), fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).pack(side='left', padx=(0, 10))
        
        self.status_combo = ttk.Combobox(control_frame, 
                                       values=['к выполнению', 'в работе', 'на проверке', 'выполнено'],
                                       width=18,
                                       font=('Segoe UI', 10),
                                       style='Modern.TCombobox')
        self.status_combo.pack(side='left', padx=(0, 20))
        
        self.create_modern_button(
            control_frame, "🔄 Обновить", 
            self.update_task_status, self.colors['primary']
        ).pack(side='left', padx=(0, 10))
        
        self.create_modern_button(
            control_frame, "🗑️ Удалить", 
            self.delete_task, self.colors['accent_red']
        ).pack(side='left')
        
        # Привязка событий
        self.project_combo.bind('<<ComboboxSelected>>', self.on_project_selected)
    
    def setup_comments_tab(self):
        """Вкладка комментариев с улучшенным дизайном"""
        main_grid = tk.Frame(self.comments_frame, bg=self.colors['bg_primary'])
        main_grid.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Левая колонка - список задач
        left_frame = tk.Frame(main_grid, bg=self.colors['bg_primary'])
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        # Правая колонка - комментарии
        right_frame = tk.Frame(main_grid, bg=self.colors['bg_primary'])
        right_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
        
        main_grid.columnconfigure(0, weight=1)
        main_grid.columnconfigure(1, weight=2)
        main_grid.rowconfigure(0, weight=1)
        
        # Карточка списка задач
        tasks_card = self.create_modern_card(left_frame, "Список задач", "Выберите задачу для комментариев")
        tasks_card.pack(fill='both', expand=True)
        
        # Список задач для комментариев
        tree_frame = tk.Frame(tasks_card, bg=self.colors['bg_card'])
        tree_frame.pack(fill='both', expand=True, pady=(15, 0))
        
        self.comments_tasks_tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Title', 'Project'),
            show='headings',
            height=15
        )
        
        self.comments_tasks_tree.config(style='Modern.Treeview')
        
        columns_config = [
            ('ID', 'ID', 80),
            ('Title', 'ЗАДАЧА', 150),
            ('Project', 'ПРОЕКТ', 100)
        ]
        
        for col, text, width in columns_config:
            self.comments_tasks_tree.heading(col, text=text)
            self.comments_tasks_tree.column(col, width=width, anchor='center' if col == 'ID' else 'w')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.comments_tasks_tree.yview)
        self.comments_tasks_tree.configure(yscrollcommand=scrollbar.set)
        
        self.comments_tasks_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Карточка комментариев
        comments_card = self.create_modern_card(right_frame, "Комментарии", "Комментарии к выбранной задаче")
        comments_card.pack(fill='both', expand=True)
        
        # Поле для нового комментария с улучшенным дизайном
        tk.Label(comments_card, text="Новый комментарий:", 
                font=('Segoe UI', 11, 'bold'), fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).pack(anchor='w', pady=(0, 10))
        
        # Поле автора
        author_frame = tk.Frame(comments_card, bg=self.colors['bg_card'])
        author_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(author_frame, text="Автор:", 
                font=('Segoe UI', 10), fg=self.colors['text_secondary'],
                bg=self.colors['bg_card']).pack(side='left', padx=(0, 10))
        
        self.comment_author_entry = self.create_modern_entry(author_frame, "Ваше имя")
        self.comment_author_entry.pack(side='left', fill='x', expand=True)
        
        # Поле текста комментария
        tk.Label(comments_card, text="Текст комментария:", 
                font=('Segoe UI', 10), fg=self.colors['text_secondary'],
                bg=self.colors['bg_card']).pack(anchor='w')
        
        text_frame = tk.Frame(comments_card, bg=self.colors['bg_input'], relief='flat', borderwidth=1)
        text_frame.pack(fill='x', pady=(5, 10))
        
        self.comment_text = tk.Text(
            text_frame,
            height=4,
            bg=self.colors['bg_input'],
            fg=self.colors['text_primary'],
            font=('Segoe UI', 10),
            relief='flat',
            borderwidth=0,
            padx=12,
            pady=12,
            wrap='word'
        )
        self.comment_text.pack(fill='both', expand=True, padx=1, pady=1)
        
        self.create_modern_button(
            comments_card, "💬 Добавить комментарий", 
            self.add_comment, self.colors['accent_green']
        ).pack(pady=(0, 20))
        
        # Список комментариев
        tk.Label(comments_card, text="История комментариев:", 
                font=('Segoe UI', 11, 'bold'), fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).pack(anchor='w')
        
        comments_list_frame = tk.Frame(comments_card, bg=self.colors['bg_card'])
        comments_list_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        self.comments_tree = ttk.Treeview(
            comments_list_frame,
            columns=('ID', 'Author', 'Text', 'Date'),
            show='headings',
            height=8
        )
        
        self.comments_tree.config(style='Modern.Treeview')
        
        comment_columns = [
            ('ID', 'ID', 60),
            ('Author', 'АВТОР', 100),
            ('Text', 'ТЕКСТ', 250),
            ('Date', 'ДАТА', 120)
        ]
        
        for col, text, width in comment_columns:
            self.comments_tree.heading(col, text=text)
            self.comments_tree.column(col, width=width, anchor='center' if col == 'ID' else 'w')
        
        scrollbar = ttk.Scrollbar(comments_list_frame, orient="vertical", command=self.comments_tree.yview)
        self.comments_tree.configure(yscrollcommand=scrollbar.set)
        
        self.comments_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Кнопка удаления комментария
        self.create_modern_button(
            comments_card, "🗑️ Удалить комментарий", 
            self.delete_comment, self.colors['accent_red']
        ).pack(pady=(10, 0))
        
        # Привязка события выбора задачи
        self.comments_tasks_tree.bind('<<TreeviewSelect>>', self.on_task_selected_for_comments)
    
    def create_modern_card(self, parent, title, subtitle):
        """Создание современной карточки со сглаженным дизайном"""
        card = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat', borderwidth=0)
        
        # Заголовок с улучшенным шрифтом
        tk.Label(card, text=title, 
                font=('Segoe UI', 13, 'bold'), fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).pack(anchor='w', padx=20, pady=(20, 5))
        
        # Подзаголовок
        if subtitle:
            tk.Label(card, text=subtitle, 
                    font=('Segoe UI', 9), fg=self.colors['text_muted'],
                    bg=self.colors['bg_card']).pack(anchor='w', padx=20, pady=(0, 15))
        
        return card
    
    def create_modern_entry(self, parent, placeholder=""):
        """Создание современного поля ввода с улучшенной видимостью"""
        frame = tk.Frame(parent, bg=self.colors['bg_card'])
        
        entry = tk.Entry(
            frame,
            bg=self.colors['bg_input'],
            fg=self.colors['text_primary'],
            font=('Segoe UI', 10),
            relief='flat',
            borderwidth=1,
            insertbackground=self.colors['text_primary']
        )
        entry.pack(fill='x', padx=1, pady=1)
        
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg=self.colors['text_muted'])
            
            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, 'end')
                    entry.config(fg=self.colors['text_primary'])
            
            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg=self.colors['text_muted'])
            
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
        
        return frame
    
    def create_modern_button(self, parent, text, command, color):
        """Создание современной кнопки со сглаженным дизайном"""
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            padx=20,
            pady=12,
            activebackground=self.colors['primary_light'],
            activeforeground='white'
        )
        
        # Плавный hover эффект
        def on_enter(e):
            if color == self.colors['primary']:
                button.config(bg=self.colors['primary_light'])
            elif color == self.colors['accent_green']:
                button.config(bg='#0DA271')
            elif color == self.colors['accent_red']:
                button.config(bg='#DC2626')
        
        def on_leave(e):
            button.config(bg=color)
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
        return button
    
    def on_resize(self, event):
        """Обработчик изменения размера окна для адаптивности"""
        # Можно добавить логику пересчета размеров при необходимости
        pass
    
    # Бизнес-логика (остается без изменений)
    def refresh_projects(self):
        """Обновление списка проектов"""
        projects = self.manager.get_all_projects()
        self.project_combo['values'] = [f"{p['id']}: {p['name']}" for p in projects]
        
        self.projects_tree.delete(*self.projects_tree.get_children())
        for project in projects:
            self.projects_tree.insert('', 'end', values=(
                project['id'], project['name'], project['description']
            ))
    
    def refresh_all_tasks(self):
        """Обновление всех задач для комментариев"""
        tasks = self.manager.get_all_tasks()
        self.comments_tasks_tree.delete(*self.comments_tasks_tree.get_children())
        for task in tasks:
            self.comments_tasks_tree.insert('', 'end', values=(
                task[0], task[1], task[8]  # ID, Title, Project Name
            ))
    
    def on_project_selected(self, event):
        """Обработчик выбора проекта"""
        selected = self.project_combo.get()
        if selected and selected != "Выберите проект":
            project_id = int(selected.split(':')[0])
            self.refresh_tasks(project_id)
    
    def refresh_tasks(self, project_id):
        """Обновление задач проекта"""
        tasks = self.manager.get_tasks_by_project(project_id)
        self.tasks_tree.delete(*self.tasks_tree.get_children())
        for task in tasks:
            self.tasks_tree.insert('', 'end', values=(
                task['id'], task['title'], task['status'], 
                task['assignee'], task['priority']
            ))
    
    def on_task_selected_for_comments(self, event):
        """Обработчик выбора задачи для комментариев"""
        selected = self.comments_tasks_tree.selection()
        if selected:
            task_id = self.comments_tasks_tree.item(selected[0])['values'][0]
            self.refresh_comments(task_id)
            self.selected_task_id = task_id
    
    def refresh_comments(self, task_id):
        """Обновление комментариев задачи"""
        comments = self.manager.get_comments(task_id)
        self.comments_tree.delete(*self.comments_tree.get_children())
        for comment in comments:
            # Обрезаем длинный текст для отображения
            text = comment['text']
            if len(text) > 50:
                text = text[:50] + '...'
            
            self.comments_tree.insert('', 'end', values=(
                comment['id'], comment['author'], text, comment['created_date']
            ))
    
    def refresh_all_data(self):
        """Полное обновление данных"""
        self.refresh_projects()
        self.refresh_all_tasks()
        messagebox.showinfo("Обновлено", "Все данные успешно обновлены!")
    
    def create_project(self):
        """Создание нового проекта"""
        name = self.project_name_entry.winfo_children()[0].get().strip()
        desc = self.project_desc_entry.winfo_children()[0].get().strip()
        
        if not name or name == "Введите название проекта":
            messagebox.showerror("Ошибка", "Введите название проекта")
            return
        
        success = self.manager.create_project(name, desc)
        if success:
            messagebox.showinfo("Успех", "Проект создан успешно!")
            self.project_name_entry.winfo_children()[0].delete(0, 'end')
            self.project_desc_entry.winfo_children()[0].delete(0, 'end')
            self.refresh_projects()
            self.refresh_all_tasks()
        else:
            messagebox.showerror("Ошибка", "Проект с таким названием уже существует!")
    
    def delete_project(self):
        """Удаление проекта"""
        selected = self.projects_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите проект для удаления")
            return
        
        project_id = self.projects_tree.item(selected[0])['values'][0]
        self.manager.delete_project(project_id)
        messagebox.showinfo("Успех", "Проект удален!")
        self.refresh_projects()
        self.refresh_all_tasks()
    
    def create_task(self):
        """Создание новой задачи"""
        selected_project = self.project_combo.get()
        if not selected_project or selected_project == "Выберите проект":
            messagebox.showerror("Ошибка", "Выберите проект")
            return
        
        project_id = int(selected_project.split(':')[0])
        title = self.task_title.winfo_children()[0].get().strip()
        
        if not title or title == "Введите название задачи":
            messagebox.showerror("Ошибка", "Введите название задачи")
            return
        
        if self.manager.task_exists(title, project_id):
            messagebox.showerror("Ошибка", "Задача с таким названием уже существует в этом проекте!")
            return
        
        assignee = self.task_assignee.winfo_children()[0].get().strip()
        priority = self.task_priority.get()
        
        success = self.manager.create_task(title, project_id, "", assignee, priority, "")
        if success:
            messagebox.showinfo("Успех", "Задача создана успешно!")
            self.task_title.winfo_children()[0].delete(0, 'end')
            self.task_assignee.winfo_children()[0].delete(0, 'end')
            self.refresh_tasks(project_id)
            self.refresh_all_tasks()
        else:
            messagebox.showerror("Ошибка", "Ошибка при создании задачи!")
    
    def update_task_status(self):
        """Обновление статуса задачи"""
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите задачу")
            return
        
        new_status = self.status_combo.get()
        if not new_status:
            messagebox.showerror("Ошибка", "Выберите новый статус")
            return
        
        task_id = self.tasks_tree.item(selected[0])['values'][0]
        self.manager.update_task_status(task_id, new_status)
        messagebox.showinfo("Успех", "Статус задачи обновлен!")
        
        selected_project = self.project_combo.get()
        if selected_project and selected_project != "Выберите проект":
            project_id = int(selected_project.split(':')[0])
            self.refresh_tasks(project_id)
    
    def delete_task(self):
        """Удаление задачи"""
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите задачу для удаления")
            return
        
        task_id = self.tasks_tree.item(selected[0])['values'][0]
        self.manager.delete_task(task_id)
        messagebox.showinfo("Успех", "Задача удалена!")
        
        selected_project = self.project_combo.get()
        if selected_project and selected_project != "Выберите проект":
            project_id = int(selected_project.split(':')[0])
            self.refresh_tasks(project_id)
            self.refresh_all_tasks()
    
    def add_comment(self):
        """Добавление комментария"""
        if not hasattr(self, 'selected_task_id'):
            messagebox.showerror("Ошибка", "Выберите задачу для комментария")
            return
        
        author = self.comment_author_entry.winfo_children()[0].get().strip()
        text = self.comment_text.get('1.0', 'end-1c').strip()
        
        if not author or author == "Ваше имя" or not text:
            messagebox.showerror("Ошибка", "Заполните автора и текст комментария")
            return
        
        success = self.manager.add_comment(self.selected_task_id, author, text)
        if success:
            messagebox.showinfo("Успех", "Комментарий добавлен!")
            self.comment_author_entry.winfo_children()[0].delete(0, 'end')
            self.comment_text.delete('1.0', 'end')
            self.refresh_comments(self.selected_task_id)
        else:
            messagebox.showerror("Ошибка", "Ошибка при добавлении комментария")
    
    def delete_comment(self):
        """Удаление комментария"""
        selected = self.comments_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите комментарий для удаления")
            return
        
        comment_id = self.comments_tree.item(selected[0])['values'][0]
        self.manager.delete_comment(comment_id)
        messagebox.showinfo("Успех", "Комментарий удален!")
        
        if hasattr(self, 'selected_task_id'):
            self.refresh_comments(self.selected_task_id)
    
    def show_create_project(self):
        """Показ диалога создания проекта"""
        self.create_project()

def main():
    """Запуск приложения"""
    root = tk.Tk()
    app = ModernTaskManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()