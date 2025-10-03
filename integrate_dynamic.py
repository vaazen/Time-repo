#!/usr/bin/env python3
# integrate_dynamic.py - Интеграция динамической системы в основное приложение

def integrate_dynamic_system():
    """Интегрирует динамическую систему в hybrid_app.py"""
    
    try:
        # Читаем основной файл
        with open("hybrid_app.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Добавляем импорт динамической системы
        if "from dynamic_interface import" not in content:
            import_line = "from dynamic_interface import setup_dynamic_interface, register_dynamic_element\n"
            
            # Находим место для вставки импорта
            import_section = content.find("from localization_system import")
            if import_section != -1:
                # Вставляем после импорта локализации
                end_of_line = content.find('\n', import_section) + 1
                content = content[:end_of_line] + import_line + content[end_of_line:]
                print("Импорт динамической системы добавлен")
        
        # Добавляем инициализацию динамической системы в __init__
        init_addition = """
        # Инициализация динамической системы
        self.dynamic_manager = setup_dynamic_interface(self)
        print("Динамическая система активирована!")"""
        
        if "self.dynamic_manager = setup_dynamic_interface(self)" not in content:
            # Находим место в __init__ после setup_timers
            setup_timers_pos = content.find("self.setup_timers()")
            if setup_timers_pos != -1:
                end_of_line = content.find('\n', setup_timers_pos) + 1
                content = content[:end_of_line] + init_addition + content[end_of_line:]
                print("Инициализация динамической системы добавлена")
        
        # Модифицируем создание карточек для поддержки динамического обновления
        # Заменяем создание карточки задач
        old_tasks_card = '''tasks_card = QLabel(f"""
        <div style='background: linear-gradient(135deg, #2D2D2D, #3D3D3D); padding: 25px; border-radius: 12px; text-align: center; border: 1px solid #FF2B4340; box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
            <h3 style='color: #FF2B43; margin: 0; font-size: 14px;'>📋 {_("tasks_today")}</h3>
            <h1 style='margin: 15px 0; font-family: "Courier New", monospace; color: #FF2B43; font-size: 32px; text-shadow: 0 0 10px #FF2B4350; letter-spacing: 2px;'>{total_tasks}</h1>
            
            <!-- Прогресс-бар для задач -->
            <div style='margin: 15px 0; background: #1A1A1A; border-radius: 10px; height: 8px; overflow: hidden;'>
                <div style='background: linear-gradient(90deg, #FF2B43, #FF2B4380); height: 100%; width: {min(total_tasks * 10, 100)}%; border-radius: 10px; transition: width 0.3s ease;'></div>
            </div>
            <p style='color: #FF2B43; margin: 5px 0; font-size: 11px; font-weight: bold;'>Активность: {min(total_tasks * 10, 100):.0f}%</p>
            
            <!-- Мотивационное сообщение -->
            <p style='color: #FFD700; margin: 10px 0; font-size: 11px; font-style: italic; opacity: 0.9;'>{'Отличный старт!' if total_tasks > 3 else 'Добавьте задачи! 📝'}</p>
        </div>
        """)
        stats_layout.addWidget(tasks_card)'''
        
        new_tasks_card = '''self.tasks_card_element = QLabel(f"""
        <div style='background: linear-gradient(135deg, #2D2D2D, #3D3D3D); padding: 25px; border-radius: 12px; text-align: center; border: 1px solid #FF2B4340; box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
            <h3 style='color: #FF2B43; margin: 0; font-size: 14px;'>📋 {_("tasks_today")}</h3>
            <h1 style='margin: 15px 0; font-family: "Courier New", monospace; color: #FF2B43; font-size: 32px; text-shadow: 0 0 10px #FF2B4350; letter-spacing: 2px;'>{total_tasks}</h1>
            
            <!-- Прогресс-бар для задач -->
            <div style='margin: 15px 0; background: #1A1A1A; border-radius: 10px; height: 8px; overflow: hidden;'>
                <div style='background: linear-gradient(90deg, #FF2B43, #FF2B4380); height: 100%; width: {min(total_tasks * 10, 100)}%; border-radius: 10px; transition: width 0.3s ease;'></div>
            </div>
            <p style='color: #FF2B43; margin: 5px 0; font-size: 11px; font-weight: bold;'>Активность: {min(total_tasks * 10, 100):.0f}%</p>
            
            <!-- Мотивационное сообщение -->
            <p style='color: #FFD700; margin: 10px 0; font-size: 11px; font-style: italic; opacity: 0.9;'>{'Отличный старт!' if total_tasks > 3 else 'Добавьте задачи! 📝'}</p>
        </div>
        """)
        register_dynamic_element(self, "tasks_card", self.tasks_card_element, "stats")
        stats_layout.addWidget(self.tasks_card_element)'''
        
        if old_tasks_card in content:
            content = content.replace(old_tasks_card, new_tasks_card)
            print("Карточка задач обновлена для динамического режима")
        
        # Аналогично для карточки выполненных задач
        old_completed_card = '''completed_card = QLabel(f"""
        <div style='background: linear-gradient(135deg, #2D2D2D, #3D3D3D); padding: 25px; border-radius: 12px; text-align: center; border: 1px solid #4CAF5040; box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
            <h3 style='color: #4CAF50; margin: 0; font-size: 14px;'>✅ {_("completed_tasks")}</h3>
            <h1 style='margin: 15px 0; font-family: "Courier New", monospace; color: #4CAF50; font-size: 32px; text-shadow: 0 0 10px #4CAF5050; letter-spacing: 2px;'>{completed_count}</h1>
            
            <!-- Прогресс-бар выполнения -->
            <div style='margin: 15px 0; background: #1A1A1A; border-radius: 10px; height: 8px; overflow: hidden;'>
                <div style='background: linear-gradient(90deg, #4CAF50, #4CAF5080); height: 100%; width: {completion_rate:.1f}%; border-radius: 10px; transition: width 0.3s ease;'></div>
            </div>
            <p style='color: #4CAF50; margin: 5px 0; font-size: 11px; font-weight: bold;'>Выполнено: {completion_rate:.0f}%</p>
            
            <!-- Мотивационное сообщение -->
            <p style='color: #FFD700; margin: 10px 0; font-size: 11px; font-style: italic; opacity: 0.9;'>{'Превосходно! 🎉' if completion_rate > 70 else 'Продолжайте! 💪' if completion_rate > 30 else 'Начните выполнять! 🚀'}</p>
        </div>
        """)
        stats_layout.addWidget(completed_card)'''
        
        new_completed_card = '''self.completed_card_element = QLabel(f"""
        <div style='background: linear-gradient(135deg, #2D2D2D, #3D3D3D); padding: 25px; border-radius: 12px; text-align: center; border: 1px solid #4CAF5040; box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
            <h3 style='color: #4CAF50; margin: 0; font-size: 14px;'>✅ {_("completed_tasks")}</h3>
            <h1 style='margin: 15px 0; font-family: "Courier New", monospace; color: #4CAF50; font-size: 32px; text-shadow: 0 0 10px #4CAF5050; letter-spacing: 2px;'>{completed_count}</h1>
            
            <!-- Прогресс-бар выполнения -->
            <div style='margin: 15px 0; background: #1A1A1A; border-radius: 10px; height: 8px; overflow: hidden;'>
                <div style='background: linear-gradient(90deg, #4CAF50, #4CAF5080); height: 100%; width: {completion_rate:.1f}%; border-radius: 10px; transition: width 0.3s ease;'></div>
            </div>
            <p style='color: #4CAF50; margin: 5px 0; font-size: 11px; font-weight: bold;'>Выполнено: {completion_rate:.0f}%</p>
            
            <!-- Мотивационное сообщение -->
            <p style='color: #FFD700; margin: 10px 0; font-size: 11px; font-style: italic; opacity: 0.9;'>{'Превосходно! 🎉' if completion_rate > 70 else 'Продолжайте! 💪' if completion_rate > 30 else 'Начните выполнять! 🚀'}</p>
        </div>
        """)
        register_dynamic_element(self, "completed_card", self.completed_card_element, "stats")
        stats_layout.addWidget(self.completed_card_element)'''
        
        if old_completed_card in content:
            content = content.replace(old_completed_card, new_completed_card)
            print("Карточка выполненных задач обновлена для динамического режима")
        
        # Сохраняем обновленный файл
        with open("hybrid_app.py", 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Динамическая система успешно интегрирована!")
        
    except Exception as e:
        print(f"Ошибка интеграции: {e}")

if __name__ == "__main__":
    integrate_dynamic_system()
