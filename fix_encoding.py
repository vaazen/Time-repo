#!/usr/bin/env python3
# fix_encoding.py - Исправление проблем с кодировкой

def fix_encoding_issues():
    """Исправляет проблемы с кодировкой в файлах"""
    
    files_to_fix = ["dynamic_interface.py", "dynamic_elements.py"]
    
    for filename in files_to_fix:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Заменяем проблемные print с эмодзи
            content = content.replace('print("Система динамического интерфейса загружена! 🔄")', 'print("Система динамического интерфейса загружена!")')
            content = content.replace('print("Динамические элементы загружены! 🔄")', 'print("Динамические элементы загружены!")')
            content = content.replace('print("Динамическая система активирована!")', 'print("Динамическая система активирована!")')
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Исправлен файл: {filename}")
            
        except Exception as e:
            print(f"Ошибка исправления {filename}: {e}")

if __name__ == "__main__":
    fix_encoding_issues()
