#!/usr/bin/env python3
# apply_styles.py - Скрипт для применения современных стилей

import re

def apply_modern_styles_to_file(filename):
    """Применяет современные стили к файлу"""
    
    # Читаем файл
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Паттерны для замены старых стилей на новые
    replacements = [
        # Обновляем стили QTextEdit для графиков
        (
            r'QTextEdit \{\s*background: #2D2D2D;\s*border: 2px solid #FF2B43;\s*border-radius: 8px;\s*padding: 15px;\s*font-family: \'Consolas\', monospace;\s*color: #CCCCCC;\s*\}',
            '''QTextEdit {
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
        ),
        
        # Обновляем стили для статистики
        (
            r'QTextEdit \{\s*background: #2D2D2D;\s*border: 2px solid #4CAF50;\s*border-radius: 8px;\s*padding: 15px;\s*color: #CCCCCC;\s*\}',
            '''QTextEdit {
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
        )
    ]
    
    # Применяем замены
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
    
    # Сохраняем обновленный файл
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Стили применены к файлу: {filename}")

if __name__ == "__main__":
    # Применяем стили к основному файлу
    try:
        apply_modern_styles_to_file("hybrid_app.py")
        print("🎨 Все стили успешно обновлены!")
    except Exception as e:
        print(f"❌ Ошибка при применении стилей: {e}")
