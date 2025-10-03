# style_improvements.py - Улучшенные стили для всех элементов интерфейса

def get_modern_card_style(border_color="#FF2B43", shadow_color="rgba(0,0,0,0.3)"):
    """Возвращает современный стиль карточки с градиентами и тенями"""
    return f"""
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2D2D2D, stop:1 #3D3D3D);
        border: 2px solid {border_color};
        border-radius: 12px;
        padding: 20px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 14px;
        color: #CCCCCC;
        selection-background-color: {border_color};
        box-shadow: 0 4px 12px {shadow_color};
    """

def get_stat_card_html(title, value, color, emoji, progress_value, progress_label, motivation):
    """Генерирует HTML для статистической карточки в едином стиле"""
    return f"""
    <div style='background: linear-gradient(135deg, #2D2D2D, #3D3D3D); padding: 25px; border-radius: 12px; text-align: center; border: 1px solid {color}40; box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
        <h3 style='color: {color}; margin: 0; font-size: 14px;'>{emoji} {title}</h3>
        <h1 style='margin: 15px 0; font-family: "Courier New", monospace; color: {color}; font-size: 32px; text-shadow: 0 0 10px {color}50; letter-spacing: 2px;'>{value}</h1>
        
        <!-- Прогресс-бар -->
        <div style='margin: 15px 0; background: #1A1A1A; border-radius: 10px; height: 8px; overflow: hidden;'>
            <div style='background: linear-gradient(90deg, {color}, {color}80); height: 100%; width: {progress_value:.1f}%; border-radius: 10px; transition: width 0.3s ease;'></div>
        </div>
        <p style='color: {color}; margin: 5px 0; font-size: 11px; font-weight: bold;'>{progress_label}: {progress_value:.0f}%</p>
        
        <!-- Мотивационное сообщение -->
        <p style='color: #FFD700; margin: 10px 0; font-size: 11px; font-style: italic; opacity: 0.9;'>{motivation}</p>
    </div>
    """

def get_modern_textedit_style(border_color="#FF2B43"):
    """Возвращает современный стиль для QTextEdit"""
    return f"""
        QTextEdit {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2D2D2D, stop:1 #3D3D3D);
            border: 2px solid {border_color};
            border-radius: 12px;
            padding: 20px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            color: #CCCCCC;
            selection-background-color: {border_color};
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
    """

def get_modern_button_style():
    """Возвращает современный стиль для кнопок"""
    return """
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #FF2B43, stop:1 #E01E37);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 14px;
            border-radius: 10px;
            font-weight: bold;
            min-width: 140px;
            min-height: 45px;
            box-shadow: 0 6px 15px rgba(255, 43, 67, 0.3);
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #FF4A5F, stop:1 #FF2B43);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(255, 43, 67, 0.4);
        }
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #E01E37, stop:1 #C01A31);
            transform: translateY(0px);
            box-shadow: 0 4px 10px rgba(255, 43, 67, 0.2);
        }
    """

def get_modern_label_style():
    """Возвращает современный стиль для заголовков"""
    return """
        QLabel {
            margin: 10px;
            font-weight: 600;
            color: #FFFFFF;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
    """

# Примеры использования для разных элементов
STYLE_EXAMPLES = {
    "tasks_card": {
        "color": "#FF2B43",
        "emoji": "📋",
        "title": "Задачи сегодня"
    },
    "completed_card": {
        "color": "#4CAF50", 
        "emoji": "✅",
        "title": "Выполнено"
    },
    "time_card": {
        "color": "#2196F3",
        "emoji": "🕐", 
        "title": "Текущее время"
    },
    "chart_widget": {
        "border_color": "#FF2B43"
    },
    "stats_widget": {
        "border_color": "#4CAF50"
    }
}

print("Модуль улучшенных стилей загружен! 🎨")
print("Доступные функции:")
print("- get_modern_card_style()")
print("- get_stat_card_html()")
print("- get_modern_textedit_style()")
print("- get_modern_button_style()")
print("- get_modern_label_style()")
