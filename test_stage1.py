
import subprocess
import sys
import os

def run_shell_command(command):
    """Выполняет команду в эмуляторе и возвращает результат"""
    try:
        process = subprocess.Popen(
            [sys.executable, 'shell.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        stdout, stderr = process.communicate(input=command + '\nexit\n', timeout=10)
        return stdout, stderr, process.returncode
    except subprocess.TimeoutExpired:
        process.kill()
        return "", "Timeout", 1
    except Exception as e:
        return "", str(e), 1

def test_basic_commands():
    """Тестирует базовые команды"""
    print("=== Тестирование базовых команд ===")
    
    # Тест команды ls
    print("\n1. Тест команды ls:")
    stdout, stderr, code = run_shell_command("ls")
    print("Вывод:", stdout)
    
    # Тест команды ls с аргументами
    print("\n2. Тест команды ls с аргументами:")
    stdout, stderr, code = run_shell_command("ls /home /tmp")
    print("Вывод:", stdout)
    
    # Тест команды cd
    print("\n3. Тест команды cd:")
    stdout, stderr, code = run_shell_command("cd /tmp")
    print("Вывод:", stdout)
    
    # Тест команды cd без аргументов
    print("\n4. Тест команды cd без аргументов:")
    stdout, stderr, code = run_shell_command("cd")
    print("Вывод:", stdout)
    
    # Тест команды cd с множественными аргументами
    print("\n5. Тест команды cd с множественными аргументами:")
    stdout, stderr, code = run_shell_command("cd /tmp /home")
    print("Вывод:", stdout)

def test_environment_variables():
    """Тестирует переменные окружения"""
    print("\n=== Тестирование переменных окружения ===")
    
    # Тест $HOME
    print("\n1. Тест переменной $HOME:")
    stdout, stderr, code = run_shell_command("echo $HOME")
    print("Вывод:", stdout)
    
    # Тест ${HOME}
    print("\n2. Тест переменной ${HOME}:")
    stdout, stderr, code = run_shell_command("echo ${HOME}")
    print("Вывод:", stdout)
    
    # Тест $USER
    print("\n3. Тест переменной $USER:")
    stdout, stderr, code = run_shell_command("echo $USER")
    print("Вывод:", stdout)
    
    # Тест несуществующей переменной
    print("\n4. Тест несуществующей переменной:")
    stdout, stderr, code = run_shell_command("echo $NONEXISTENT")
    print("Вывод:", stdout)

def test_error_handling():
    """Тестирует обработку ошибок"""
    print("\n=== Тестирование обработки ошибок ===")
    
    # Тест несуществующей команды
    print("\n1. Тест несуществующей команды:")
    stdout, stderr, code = run_shell_command("nonexistent_command")
    print("Вывод:", stdout)
    
    # Тест пустой команды
    print("\n2. Тест пустой команды:")
    stdout, stderr, code = run_shell_command("")
    print("Вывод:", stdout)
    
    # Тест команды exit с кодом
    print("\n3. Тест команды exit с кодом:")
    stdout, stderr, code = run_shell_command("exit 42")
    print("Код возврата:", code)
    print("Вывод:", stdout)

def test_quotes_and_spaces():
    """Тестирует обработку кавычек и пробелов"""
    print("\n=== Тестирование кавычек и пробелов ===")
    
    # Тест с кавычками
    print("\n1. Тест с кавычками:")
    stdout, stderr, code = run_shell_command('ls "file with spaces"')
    print("Вывод:", stdout)
    
    # Тест с одинарными кавычками
    print("\n2. Тест с одинарными кавычками:")
    stdout, stderr, code = run_shell_command("ls 'file with spaces'")
    print("Вывод:", stdout)

if __name__ == "__main__":
    print("Демонстрация работы эмулятора командной строки (Этап 1)")
    print("=" * 60)
    
    test_basic_commands()
    test_environment_variables()
    test_error_handling()
    test_quotes_and_spaces()
    
    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
