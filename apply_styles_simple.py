#!/usr/bin/env python3
# apply_styles_simple.py - Упрощенный скрипт для применения стилей

def apply_modern_styles():
    """Применяет современные стили к файлу"""
    
    try:
        # Читаем файл
        with open("hybrid_app.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Простые замены для улучшения стилей
        old_style_1 = '''QTextEdit {
                background: #2D2D2D;
                border: 2px solid #FF2B43;
                border-radius: 8px;
                padding: 15px;
                font-family: 'Consolas', monospace;
                color: #CCCCCC;
            }'''
        
        new_style_1 = '''QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2D2D2D, stop:1 #3D3D3D);
                border: 2px solid #FF2B43;
                border-radius: 12px;
                padding: 20px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
                color: #CCCCCC;
                selection-background-color: #FF2B43;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }'''
        
        # Применяем замену
        if old_style_1 in content:
            content = content.replace(old_style_1, new_style_1)
            print("Стиль 1 обновлен")
        
        # Вторая замена для статистики
        old_style_2 = '''QTextEdit {
                background: #2D2D2D;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 15px;
                color: #CCCCCC;
            }'''
        
        new_style_2 = '''QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2D2D2D, stop:1 #3D3D3D);
                border: 2px solid #4CAF50;
                border-radius: 12px;
                padding: 20px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
                color: #CCCCCC;
                selection-background-color: #4CAF50;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }'''
        
        if old_style_2 in content:
            content = content.replace(old_style_2, new_style_2)
            print("Стиль 2 обновлен")
        
        # Сохраняем файл
        with open("hybrid_app.py", 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Стили успешно применены!")
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    apply_modern_styles()
