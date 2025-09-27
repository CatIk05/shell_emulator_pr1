#!/usr/bin/env python3
"""
Интерактивная демонстрация эмулятора командной строки (Этап 1)
"""

import subprocess
import sys
import os

def interactive_demo():
    """Интерактивная демонстрация работы эмулятора"""
    print("=" * 60)
    print("ИНТЕРАКТИВНАЯ ДЕМОНСТРАЦИЯ ЭМУЛЯТОРА КОМАНДНОЙ СТРОКИ")
    print("=" * 60)
    print()
    print("Демонстрируемые возможности:")
    print("1. Приглашение в формате username@hostname:directory$")
    print("2. Команды-заглушки: ls, cd, echo, exit")
    print("3. Раскрытие переменных окружения: $VAR, ${VAR}")
    print("4. Обработка ошибок")
    print("5. Поддержка кавычек и пробелов")
    print()
    print("Примеры команд для тестирования:")
    print("- ls")
    print("- ls /home /tmp")
    print("- cd /tmp")
    print("- cd")
    print("- echo Hello World")
    print("- echo $HOME")
    print("- echo ${USER}")
    print("- echo 'file with spaces'")
    print("- nonexistent_command")
    print("- exit")
    print()
    print("Запуск эмулятора...")
    print("-" * 60)
    
    try:
        # Запускаем эмулятор в интерактивном режиме
        subprocess.run([sys.executable, 'shell.py'], cwd=os.path.dirname(os.path.abspath(__file__)))
    except KeyboardInterrupt:
        print("\nДемонстрация прервана пользователем")
    except Exception as e:
        print(f"Ошибка при запуске демонстрации: {e}")

if __name__ == "__main__":
    interactive_demo()
