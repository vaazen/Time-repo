# 🔧 Настройка C++ модуля для Windows

## 🎯 Проблема
C++ модуль не компилируется, потому что не установлен компилятор.

## 📋 Варианты решения

### Вариант 1: Установка MinGW-w64 (Рекомендуется)

#### Шаг 1: Скачать MinGW-w64
1. Перейдите на https://www.mingw-w64.org/downloads/
2. Скачайте MSYS2: https://www.msys2.org/
3. Установите MSYS2

#### Шаг 2: Установка компилятора
```bash
# В терминале MSYS2
pacman -S mingw-w64-x86_64-gcc
pacman -S mingw-w64-x86_64-make
```

#### Шаг 3: Добавить в PATH
Добавьте в системную переменную PATH:
```
C:\msys64\mingw64\bin
```

#### Шаг 4: Компиляция
```bash
g++ -shared -fPIC -O3 performance.cpp -o performance.dll
```

### Вариант 2: Visual Studio Build Tools

#### Шаг 1: Скачать Build Tools
1. Перейдите на https://visualstudio.microsoft.com/downloads/
2. Скачайте "Build Tools for Visual Studio 2022"
3. Установите с компонентом "C++ build tools"

#### Шаг 2: Компиляция
```cmd
# В Developer Command Prompt
cl /LD /O2 performance.cpp /Fe:performance.dll
```

### Вариант 3: Использование онлайн компилятора

#### Шаг 1: Подготовить код
Скопируйте содержимое `performance.cpp`

#### Шаг 2: Компиляция онлайн
1. Перейдите на https://godbolt.org/
2. Выберите компилятор x86-64 gcc
3. Добавьте флаги: `-shared -fPIC -O3`
4. Скачайте результат

## 🚀 Быстрое решение: Предкомпилированная DLL

Создадим упрощенную версию C++ модуля для демонстрации:
