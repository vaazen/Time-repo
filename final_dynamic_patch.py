#!/usr/bin/env python3
# final_dynamic_patch.py - Финальная интеграция всех динамических элементов

def apply_final_dynamic_patch():
    """Применяет финальный патч для полной динамизации интерфейса"""
    
    try:
        # Читаем файл
        with open("hybrid_app.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Добавляем импорт динамических элементов
        if "from dynamic_elements import" not in content:
            import_line = "from dynamic_elements import dynamic_task_list, dynamic_chart, dynamic_stats\n"
            
            # Находим место после импорта dynamic_interface
            dynamic_import_pos = content.find("from dynamic_interface import")
            if dynamic_import_pos != -1:
                end_of_line = content.find('\n', dynamic_import_pos) + 1
                content = content[:end_of_line] + import_line + content[end_of_line:]
                print("Импорт динамических элементов добавлен")
        
        # Добавляем метод обновления всех динамических элементов
        update_method = '''
    def update_all_dynamic_elements(self):
        """Обновление всех динамических элементов интерфейса"""
        try:
            # Обновляем список задач
            if hasattr(self, 'upcoming_tasks') and self.upcoming_tasks:
                new_text = dynamic_task_list.get_dynamic_task_text()
                self.upcoming_tasks.setPlainText(new_text)
            
            # Обновляем график
            if hasattr(self, 'chart_widget') and self.chart_widget:
                new_chart = dynamic_chart.get_dynamic_chart_text()
                self.chart_widget.setPlainText(new_chart)
            
            # Обновляем статистику
            if hasattr(self, 'stats_widget') and self.stats_widget:
                new_stats = dynamic_stats.get_dynamic_stats_text()
                self.stats_widget.setPlainText(new_stats)
                
        except Exception as e:
            print(f"Ошибка обновления динамических элементов: {e}")'''
        
        if "def update_all_dynamic_elements(self):" not in content:
            # Вставляем метод перед update_time_display
            update_time_pos = content.find("def update_time_display(self):")
            if update_time_pos != -1:
                content = content[:update_time_pos] + update_method + "\n    " + content[update_time_pos:]
                print("Метод обновления динамических элементов добавлен")
        
        # Добавляем таймер для обновления всех элементов в setup_timers
        timer_addition = '''
        # Таймер для обновления всех динамических элементов (каждые 3 секунды)
        self.all_elements_timer = QTimer()
        self.all_elements_timer.timeout.connect(self.update_all_dynamic_elements)
        self.all_elements_timer.start(3000)'''
        
        if "self.all_elements_timer = QTimer()" not in content:
            # Находим конец метода setup_timers
            setup_timers_start = content.find("def setup_timers(self):")
            if setup_timers_start != -1:
                # Находим следующий метод
                next_method = content.find("\n    def ", setup_timers_start + 1)
                if next_method != -1:
                    content = content[:next_method] + timer_addition + content[next_method:]
                    print("Таймер для всех элементов добавлен")
        
        # Модифицируем создание upcoming_tasks для сохранения ссылки
        old_upcoming = "upcoming_tasks = QTextEdit()"
        new_upcoming = "self.upcoming_tasks = QTextEdit()"
        
        if old_upcoming in content:
            content = content.replace(old_upcoming, new_upcoming)
            print("Список задач сделан динамическим")
        
        # Модифицируем создание chart_widget для сохранения ссылки
        old_chart = "chart_widget = QTextEdit()"
        new_chart = "self.chart_widget = QTextEdit()"
        
        if old_chart in content:
            content = content.replace(old_chart, new_chart)
            print("График сделан динамическим")
        
        # Модифицируем создание stats_widget для сохранения ссылки
        old_stats = "stats_widget = QTextEdit()"
        new_stats = "self.stats_widget = QTextEdit()"
        
        if old_stats in content:
            content = content.replace(old_stats, new_stats)
            print("Статистика сделана динамической")
        
        # Обновляем все ссылки на локальные переменные
        replacements = [
            ("upcoming_tasks.setReadOnly(True)", "self.upcoming_tasks.setReadOnly(True)"),
            ("upcoming_tasks.setMaximumHeight(150)", "self.upcoming_tasks.setMaximumHeight(150)"),
            ("upcoming_tasks.setPlainText(tasks_text)", "self.upcoming_tasks.setPlainText(dynamic_task_list.get_dynamic_task_text())"),
            ("upcoming_tasks.setStyleSheet(", "self.upcoming_tasks.setStyleSheet("),
            ("layout.addWidget(upcoming_tasks)", "layout.addWidget(self.upcoming_tasks)"),
            
            ("chart_widget.setReadOnly(True)", "self.chart_widget.setReadOnly(True)"),
            ("chart_widget.setMaximumHeight(200)", "self.chart_widget.setMaximumHeight(200)"),
            ("chart_widget.setPlainText(chart_text)", "self.chart_widget.setPlainText(dynamic_chart.get_dynamic_chart_text())"),
            ("chart_widget.setStyleSheet(", "self.chart_widget.setStyleSheet("),
            ("layout.addWidget(chart_widget)", "layout.addWidget(self.chart_widget)"),
            
            ("stats_widget.setReadOnly(True)", "self.stats_widget.setReadOnly(True)"),
            ("stats_widget.setMaximumHeight(150)", "self.stats_widget.setMaximumHeight(150)"),
            ("stats_widget.setPlainText(stats_text)", "self.stats_widget.setPlainText(dynamic_stats.get_dynamic_stats_text())"),
            ("stats_widget.setStyleSheet(", "self.stats_widget.setStyleSheet("),
            ("layout.addWidget(stats_widget)", "layout.addWidget(self.stats_widget)")
        ]
        
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
        
        print("Все ссылки обновлены для динамического режима")
        
        # Сохраняем обновленный файл
        with open("hybrid_app.py", 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Финальный динамический патч применен успешно!")
        print("Теперь весь интерфейс работает в динамическом режиме!")
        
    except Exception as e:
        print(f"Ошибка применения патча: {e}")

if __name__ == "__main__":
    apply_final_dynamic_patch()
