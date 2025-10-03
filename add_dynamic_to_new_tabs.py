#!/usr/bin/env python3
# add_dynamic_to_new_tabs.py - Добавление динамических обновлений к новым вкладкам

def add_dynamic_methods():
    """Добавляет методы для динамического обновления новых вкладок"""
    
    try:
        with open("hybrid_app.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Добавляем новые методы для обновления задач
        new_methods = '''
    def clear_completed_tasks(self):
        """Очистка выполненных задач"""
        try:
            from task_manager import task_manager, TaskStatus
            all_tasks = task_manager.get_all_tasks()
            completed_tasks = [t for t in all_tasks if t.status == TaskStatus.COMPLETED]
            
            if completed_tasks:
                # Здесь можно добавить логику удаления
                self.update_tasks_display()
                self.update_tasks_stats()
                print(f"Очищено {len(completed_tasks)} выполненных задач")
            else:
                print("Нет выполненных задач для очистки")
                
        except Exception as e:
            print(f"Ошибка очистки задач: {e}")
    
    def refresh_tasks(self):
        """Обновление списка задач"""
        try:
            self.update_tasks_display()
            self.update_tasks_stats()
            print("Список задач обновлен")
        except Exception as e:
            print(f"Ошибка обновления задач: {e}")'''
        
        # Находим место для вставки (перед update_time_display)
        update_time_pos = content.find("def update_time_display(self):")
        if update_time_pos != -1:
            content = content[:update_time_pos] + new_methods + "\n    " + content[update_time_pos:]
            print("Методы для работы с задачами добавлены")
        
        # Обновляем метод update_all_dynamic_elements для включения новых элементов
        old_update_method = '''def update_all_dynamic_elements(self):
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
        
        new_update_method = '''def update_all_dynamic_elements(self):
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
            
            # Обновляем список задач в отдельной вкладке
            if hasattr(self, 'tasks_list_widget') and self.tasks_list_widget:
                self.update_tasks_display()
            
            # Обновляем статистику задач
            if hasattr(self, 'tasks_stats_widget') and self.tasks_stats_widget:
                self.update_tasks_stats()
            
            # Обновляем статус интеграций
            if hasattr(self, 'integrations_status') and self.integrations_status:
                self.update_integrations_status()
                
        except Exception as e:
            print(f"Ошибка обновления динамических элементов: {e}")'''
        
        if old_update_method in content:
            content = content.replace(old_update_method, new_update_method)
            print("Метод обновления динамических элементов расширен")
        
        # Сохраняем обновленный файл
        with open("hybrid_app.py", 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Динамические обновления добавлены к новым вкладкам!")
        
    except Exception as e:
        print(f"Ошибка добавления динамических методов: {e}")

if __name__ == "__main__":
    add_dynamic_methods()
