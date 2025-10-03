#!/usr/bin/env python3
# modernize_all_tabs.py - Модернизация всех вкладок приложения

def modernize_tasks_tab():
    """Модернизирует вкладку задач"""
    
    try:
        with open("hybrid_app.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Находим метод create_tasks_tab и заменяем его на современную версию
        old_tasks_tab_start = content.find("def create_tasks_tab(self):")
        if old_tasks_tab_start == -1:
            print("Метод create_tasks_tab не найден")
            return content
        
        # Находим конец метода
        next_method = content.find("\n    def ", old_tasks_tab_start + 1)
        if next_method == -1:
            next_method = len(content)
        
        # Новая современная версия вкладки задач
        new_tasks_tab = '''def create_tasks_tab(self):
        """Создание современной вкладки управления задачами"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Современный заголовок с градиентом
        title = QLabel("📋 Управление задачами")
        title.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            padding: 15px; 
            text-align: center;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FF2B43, stop:1 #FF6B35);
            border-radius: 10px;
            color: white;
            margin: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Современные кнопки управления
        buttons_layout = QHBoxLayout()
        
        # Кнопка добавления задачи
        self.add_task_btn = QPushButton("➕ Добавить задачу")
        self.add_task_btn.clicked.connect(self.add_task)
        self.add_task_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4CAF50, stop:1 #45A049);
                color: white;
                border: none;
                padding: 15px 25px;
                font-size: 14px;
                border-radius: 10px;
                font-weight: bold;
                min-width: 150px;
                min-height: 45px;
                box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5CBF60, stop:1 #4CAF50);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #45A049, stop:1 #3D8B40);
            }
        """)
        buttons_layout.addWidget(self.add_task_btn)
        
        # Кнопка обновления
        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.clicked.connect(self.refresh_tasks)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2196F3, stop:1 #1976D2);
                color: white;
                border: none;
                padding: 15px 25px;
                font-size: 14px;
                border-radius: 10px;
                font-weight: bold;
                min-width: 150px;
                min-height: 45px;
                box-shadow: 0 4px 8px rgba(33, 150, 243, 0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #42A5F5, stop:1 #2196F3);
                transform: translateY(-2px);
            }
        """)
        buttons_layout.addWidget(refresh_btn)
        
        # Кнопка очистки
        clear_btn = QPushButton("🗑️ Очистить")
        clear_btn.clicked.connect(self.clear_completed_tasks)
        clear_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FF5722, stop:1 #E64A19);
                color: white;
                border: none;
                padding: 15px 25px;
                font-size: 14px;
                border-radius: 10px;
                font-weight: bold;
                min-width: 150px;
                min-height: 45px;
                box-shadow: 0 4px 8px rgba(255, 87, 34, 0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FF7043, stop:1 #FF5722);
                transform: translateY(-2px);
            }
        """)
        buttons_layout.addWidget(clear_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # Современный список задач с прокруткой
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Динамический список задач
        self.tasks_list_widget = QTextEdit()
        self.tasks_list_widget.setReadOnly(True)
        self.tasks_list_widget.setMinimumHeight(300)
        self.tasks_list_widget.setStyleSheet("""
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2D2D2D, stop:1 #3D3D3D);
                border: 2px solid #FF2B43;
                border-radius: 12px;
                padding: 20px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
                color: #CCCCCC;
                selection-background-color: #FF2B43;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }
        """)
        
        # Инициализируем список задач
        self.update_tasks_display()
        
        scroll_layout.addWidget(self.tasks_list_widget)
        
        # Статистика задач
        self.tasks_stats_widget = QLabel()
        self.tasks_stats_widget.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2D2D2D, stop:1 #3D3D3D);
                border: 2px solid #4CAF50;
                border-radius: 12px;
                padding: 20px;
                font-size: 14px;
                color: #CCCCCC;
                margin: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }
        """)
        self.update_tasks_stats()
        scroll_layout.addWidget(self.tasks_stats_widget)
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        widget.setLayout(layout)
        return widget
    
    def update_tasks_display(self):
        """Обновление отображения списка задач"""
        try:
            from task_manager import task_manager, TaskStatus
            from datetime import datetime
            
            all_tasks = task_manager.get_all_tasks()
            
            if not all_tasks:
                self.tasks_list_widget.setPlainText("📝 Нет задач. Добавьте первую задачу!")
                return
            
            tasks_text = "📋 Список всех задач:\\n\\n"
            
            # Группируем задачи по статусу
            status_groups = {
                "in_progress": "🔄 В процессе:",
                "planned": "⏰ Запланированы:",
                "completed": "✅ Выполнены:"
            }
            
            for status, title in status_groups.items():
                status_tasks = [t for t in all_tasks if t.status.name.lower() == status]
                if status_tasks:
                    tasks_text += f"\\n{title}\\n"
                    for task in status_tasks[:10]:  # Показываем до 10 задач каждого типа
                        time_str = task.start_time.strftime('%H:%M') if hasattr(task, 'start_time') else "00:00"
                        priority_icon = "🔴" if hasattr(task, 'priority') and task.priority == "high" else "🟡" if hasattr(task, 'priority') and task.priority == "medium" else "🟢"
                        tasks_text += f"  {priority_icon} {task.title} ({time_str})\\n"
            
            current_time = datetime.now().strftime('%H:%M:%S')
            tasks_text += f"\\n🕐 Обновлено: {current_time}"
            
            self.tasks_list_widget.setPlainText(tasks_text)
            
        except Exception as e:
            self.tasks_list_widget.setPlainText(f"Ошибка загрузки задач: {e}")
    
    def update_tasks_stats(self):
        """Обновление статистики задач"""
        try:
            from task_manager import task_manager, TaskStatus
            
            all_tasks = task_manager.get_all_tasks()
            completed = len([t for t in all_tasks if t.status == TaskStatus.COMPLETED])
            in_progress = len([t for t in all_tasks if t.status == TaskStatus.IN_PROGRESS])
            planned = len([t for t in all_tasks if t.status == TaskStatus.PLANNED])
            
            completion_rate = (completed / len(all_tasks) * 100) if all_tasks else 0
            
            stats_html = f"""
            <div style='text-align: center;'>
                <h3 style='color: #4CAF50; margin: 0;'>📊 Статистика задач</h3>
                <p style='margin: 10px 0;'>
                    <span style='color: #FFD700;'>Всего: {len(all_tasks)}</span> | 
                    <span style='color: #4CAF50;'>Выполнено: {completed}</span> | 
                    <span style='color: #FF9800;'>В работе: {in_progress}</span> | 
                    <span style='color: #2196F3;'>Запланировано: {planned}</span>
                </p>
                <p style='color: #FF2B43; font-weight: bold;'>Прогресс: {completion_rate:.1f}%</p>
            </div>
            """
            
            self.tasks_stats_widget.setText(stats_html)
            
        except Exception as e:
            self.tasks_stats_widget.setText(f"Ошибка статистики: {e}")'''
        
        # Заменяем старый метод на новый
        content = content[:old_tasks_tab_start] + new_tasks_tab + content[next_method:]
        
        print("Вкладка задач модернизирована!")
        return content
        
    except Exception as e:
        print(f"Ошибка модернизации вкладки задач: {e}")
        return None

def modernize_ai_tab():
    """Модернизирует вкладку ИИ"""
    
    try:
        with open("hybrid_app.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Находим и заменяем create_ai_tab
        old_ai_start = content.find("def create_ai_tab(self):")
        if old_ai_start == -1:
            print("Метод create_ai_tab не найден")
            return content
        
        next_method = content.find("\n    def ", old_ai_start + 1)
        if next_method == -1:
            next_method = len(content)
        
        new_ai_tab = '''def create_ai_tab(self):
        """Создание современной вкладки ИИ-помощника"""
        ai_widget = QWidget()
        layout = QVBoxLayout()
        
        # Современный заголовок
        title = QLabel("🤖 ИИ-Помощник для продуктивности")
        title.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            padding: 15px; 
            text-align: center;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #9C27B0, stop:1 #673AB7);
            border-radius: 10px;
            color: white;
            margin: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Область ввода запроса
        input_layout = QHBoxLayout()
        
        self.ai_input = QLineEdit()
        self.ai_input.setPlaceholderText("Введите ваш запрос к ИИ-помощнику...")
        self.ai_input.setStyleSheet("""
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2D2D2D, stop:1 #3D3D3D);
                border: 2px solid #9C27B0;
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
                color: #CCCCCC;
                min-height: 20px;
            }
            QLineEdit:focus {
                border: 2px solid #BA68C8;
                box-shadow: 0 0 10px rgba(156, 39, 176, 0.3);
            }
        """)
        input_layout.addWidget(self.ai_input)
        
        # Кнопка отправки
        send_btn = QPushButton("🚀 Спросить ИИ")
        send_btn.clicked.connect(self.process_ai_request)
        send_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #9C27B0, stop:1 #7B1FA2);
                color: white;
                border: none;
                padding: 15px 25px;
                font-size: 14px;
                border-radius: 10px;
                font-weight: bold;
                min-width: 150px;
                box-shadow: 0 4px 8px rgba(156, 39, 176, 0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #BA68C8, stop:1 #9C27B0);
                transform: translateY(-2px);
            }
        """)
        input_layout.addWidget(send_btn)
        
        layout.addLayout(input_layout)
        
        # Область результатов ИИ
        self.ai_results = QTextEdit()
        self.ai_results.setReadOnly(True)
        self.ai_results.setStyleSheet("""
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2D2D2D, stop:1 #3D3D3D);
                border: 2px solid #9C27B0;
                border-radius: 12px;
                padding: 20px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
                color: #CCCCCC;
                selection-background-color: #9C27B0;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }
        """)
        
        # Инициализируем с приветствием
        welcome_text = """🤖 Добро пожаловать в ИИ-Помощник!

Я могу помочь вам с:
• 📋 Планированием задач и расписания
• ⏰ Оптимизацией времени
• 🎯 Постановкой целей
• 📊 Анализом продуктивности
• 💡 Советами по эффективности

Просто введите ваш вопрос выше и нажмите "Спросить ИИ"!

Примеры запросов:
- "Как лучше спланировать день?"
- "Посоветуй техники концентрации"
- "Как повысить продуктивность?"
"""
        self.ai_results.setPlainText(welcome_text)
        layout.addWidget(self.ai_results)
        
        # Быстрые кнопки
        quick_buttons_layout = QHBoxLayout()
        
        quick_buttons = [
            ("📋 План дня", "Создай план продуктивного дня"),
            ("⏰ Тайм-менеджмент", "Дай советы по управлению временем"),
            ("🎯 Цели", "Помоги поставить SMART цели"),
            ("💪 Мотивация", "Дай мотивационный совет")
        ]
        
        for btn_text, prompt in quick_buttons:
            btn = QPushButton(btn_text)
            btn.clicked.connect(lambda checked, p=prompt: self.quick_ai_request(p))
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #673AB7, stop:1 #512DA8);
                    color: white;
                    border: none;
                    padding: 10px 15px;
                    font-size: 12px;
                    border-radius: 8px;
                    font-weight: bold;
                    min-width: 120px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7986CB, stop:1 #673AB7);
                }
            """)
            quick_buttons_layout.addWidget(btn)
        
        layout.addLayout(quick_buttons_layout)
        
        ai_widget.setLayout(layout)
        return ai_widget
    
    def process_ai_request(self):
        """Обработка запроса к ИИ"""
        query = self.ai_input.text().strip()
        if not query:
            return
        
        # Симуляция ответа ИИ
        import random
        from datetime import datetime
        
        responses = {
            "план": [
                "📋 Рекомендуемый план дня:\\n\\n1. 🌅 Утро (6:00-9:00): Планирование и важные задачи\\n2. ☀️ День (9:00-13:00): Основная работа\\n3. 🍽️ Обед (13:00-14:00): Отдых и восстановление\\n4. 🌆 Вечер (14:00-18:00): Завершение дел\\n5. 🌙 Ночь: Подведение итогов",
                "🎯 Эффективный день начинается с:\\n\\n• Четкого списка приоритетов\\n• Блокировки времени для важных задач\\n• Регулярных перерывов\\n• Анализа результатов"
            ],
            "время": [
                "⏰ Техники управления временем:\\n\\n🍅 Pomodoro: 25 мин работы + 5 мин отдыха\\n📊 Time blocking: Блокировка времени для задач\\n🎯 Eisenhower Matrix: Важное vs Срочное\\n⚡ GTD: Getting Things Done система",
                "💡 Секреты продуктивности:\\n\\n• Начинайте с самого сложного\\n• Используйте правило 2 минут\\n• Группируйте похожие задачи\\n• Избегайте многозадачности"
            ],
            "цели": [
                "🎯 SMART цели:\\n\\nS - Specific (Конкретные)\\nM - Measurable (Измеримые)\\nA - Achievable (Достижимые)\\nR - Relevant (Релевантные)\\nT - Time-bound (Ограниченные по времени)\\n\\nПример: 'Изучить Python за 3 месяца, уделяя 1 час в день'",
                "🚀 Стратегия достижения целей:\\n\\n1. Разбейте большую цель на маленькие шаги\\n2. Отслеживайте прогресс ежедневно\\n3. Празднуйте маленькие победы\\n4. Корректируйте план при необходимости"
            ],
            "мотивация": [
                "💪 Мотивационный заряд:\\n\\n'Успех - это сумма маленьких усилий, повторяемых день за днем.'\\n\\n🌟 Помните: каждая выполненная задача приближает вас к цели!\\n⚡ Вы уже на правильном пути!",
                "🔥 Источники мотивации:\\n\\n• Визуализируйте свой успех\\n• Ведите дневник достижений\\n• Окружайте себя вдохновляющими людьми\\n• Помните свое 'Зачем'"
            ]
        }
        
        # Определяем тип запроса
        query_lower = query.lower()
        response_type = "общий"
        
        for key in responses.keys():
            if key in query_lower:
                response_type = key
                break
        
        if response_type in responses:
            response = random.choice(responses[response_type])
        else:
            response = f"🤖 Анализирую ваш запрос: '{query}'\\n\\n💡 Это интересный вопрос! Вот что я думаю:\\n\\n• Начните с определения конкретной цели\\n• Разбейте задачу на маленькие шаги\\n• Используйте техники тайм-менеджмента\\n• Отслеживайте прогресс\\n\\n⚡ Помните: постоянство важнее совершенства!"
        
        current_time = datetime.now().strftime('%H:%M:%S')
        full_response = f"❓ Ваш вопрос: {query}\\n\\n{response}\\n\\n🕐 Время ответа: {current_time}"
        
        self.ai_results.setPlainText(full_response)
        self.ai_input.clear()
    
    def quick_ai_request(self, prompt):
        """Быстрый запрос к ИИ"""
        self.ai_input.setText(prompt)
        self.process_ai_request()'''
        
        content = content[:old_ai_start] + new_ai_tab + content[next_method:]
        print("Вкладка ИИ модернизирована!")
        return content
        
    except Exception as e:
        print(f"Ошибка модернизации вкладки ИИ: {e}")
        return None

def apply_all_modernizations():
    """Применяет все модернизации"""
    
    try:
        with open("hybrid_app.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Применяем модернизацию задач
        content = modernize_tasks_tab()
        if content is None:
            return
        
        # Применяем модернизацию ИИ
        content = modernize_ai_tab()
        if content is None:
            return
        
        # Сохраняем обновленный файл
        with open("hybrid_app.py", 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Все вкладки успешно модернизированы!")
        
    except Exception as e:
        print(f"Ошибка применения модернизации: {e}")

if __name__ == "__main__":
    apply_all_modernizations()
