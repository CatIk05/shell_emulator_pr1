import os
import sys
import readline
import re
import argparse

class Shell:
    def __init__(self, vfs_path=None, startup_script=None):
        self.username = os.getlogin()
        self.hostname = os.uname().nodename
        self.current_dir = os.getcwd()
        self.home_dir = os.path.expanduser("~")
        
        # Конфигурация
        self.vfs_path = vfs_path
        self.startup_script = startup_script
        self.config = {
            'vfs_path': vfs_path,
            'startup_script': startup_script,
            'username': self.username,
            'hostname': self.hostname,
            'current_dir': self.current_dir,
            'home_dir': self.home_dir
        }
        
        self.update_prompt()
        self.commands = {
            'ls': self.ls_command,
            'cd': self.cd_command,
            'echo': self.echo_command,
            'conf-dump': self.conf_dump_command,
            'exit': self.exit_command
        }
    
    def update_prompt(self):
        """Обновляет приглашение с учетом текущей директории"""
        if self.current_dir == self.home_dir:
            dir_display = "~"
        elif self.current_dir.startswith(self.home_dir + "/"):
            dir_display = "~" + self.current_dir[len(self.home_dir):]
        else:
            dir_display = self.current_dir
        
        self.prompt = f"{self.username}@{self.hostname}:{dir_display}$ "

    def run(self):
        """Основной цикл REPL"""
        print("Добро пожаловать в эмулятор командной строки!")
        print("Доступные команды: ls, cd, echo, conf-dump, exit")
        print("Поддерживаются переменные окружения: $VAR, ${VAR}")
        print("Для выхода используйте команду 'exit' или Ctrl+C")
        print("-" * 50)
        
        # Выполнение стартового скрипта, если указан
        if self.startup_script:
            self.execute_startup_script()
        
        while True:
            try:
                user_input = input(self.prompt)
                self.execute(user_input)
            except (EOFError, KeyboardInterrupt):
                print("\nExiting shell")
                break
            except Exception as e:
                print(f"Ошибка: {e}")
    
    def execute_startup_script(self):
        """Выполняет стартовый скрипт"""
        if not os.path.exists(self.startup_script):
            print(f"Ошибка: стартовый скрипт не найден: {self.startup_script}")
            return
        
        print(f"Выполнение стартового скрипта: {self.startup_script}")
        print("-" * 50)
        
        try:
            with open(self.startup_script, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue  # Пропускаем пустые строки и комментарии
                
                print(f"{self.prompt}{line}")
                try:
                    self.execute(line)
                except Exception as e:
                    print(f"Ошибка в строке {line_num}: {e}")
                    continue  # Пропускаем ошибочные строки
            
            print("-" * 50)
            print("Стартовый скрипт выполнен")
            
        except Exception as e:
            print(f"Ошибка чтения стартового скрипта: {e}")

    def execute(self, command):
        """Выполняет команду"""
        # Парсинг команды
        try:
            parts = self.parse_command(command)
            if not parts:
                return

            cmd = parts[0]
            args = parts[1:]

            # Выполнение команды
            if cmd in self.commands:
                try:
                    self.commands[cmd](args)
                except Exception as e:
                    print(f"Ошибка выполнения команды '{cmd}': {e}")
            else:
                print(f"Command not found: {cmd}")
        except Exception as e:
            print(f"Ошибка парсинга команды: {e}")

    def parse_command(self, command):
        """Парсит команду с поддержкой переменных окружения"""
        if not command.strip():
            return []
        
        # Поддержка переменных окружения в формате $VAR или ${VAR}
        def expand_vars(text):
            # Обработка ${VAR} формата
            text = re.sub(r'\$\{([^}]+)\}', lambda m: os.getenv(m.group(1), f"${{{m.group(1)}}}"), text)
            # Обработка $VAR формата
            text = re.sub(r'\$([A-Za-z_][A-Za-z0-9_]*)', lambda m: os.getenv(m.group(1), f"${m.group(1)}"), text)
            return text
        
        # Разбиваем команду на части, сохраняя кавычки
        parts = []
        current_part = ""
        in_quotes = False
        quote_char = None
        
        for char in command:
            if char in ['"', "'"] and not in_quotes:
                in_quotes = True
                quote_char = char
                current_part += char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
                current_part += char
            elif char == ' ' and not in_quotes:
                if current_part.strip():
                    parts.append(expand_vars(current_part.strip()))
                current_part = ""
            else:
                current_part += char
        
        if current_part.strip():
            parts.append(expand_vars(current_part.strip()))
        
        return parts

    def ls_command(self, args):
        """Команда ls - заглушка"""
        print(f"ls: command called with arguments: {args}")
        if args:
            print(f"ls: would list contents of: {args}")
        else:
            print("ls: would list contents of current directory")

    def cd_command(self, args):
        """Команда cd - заглушка"""
        if len(args) == 0:
            # cd без аргументов - переход в домашнюю директорию
            print(f"cd: would change to home directory: {self.home_dir}")
            return
        elif len(args) == 1:
            target_dir = args[0]
            print(f"cd: would change to directory: {target_dir}")
        else:
            print("cd: too many arguments")
            print("Usage: cd [directory]")

    def echo_command(self, args):
        """Команда echo - выводит аргументы"""
        if args:
            # Объединяем все аргументы в одну строку
            output = ' '.join(args)
            print(output)
        else:
            # echo без аргументов выводит пустую строку
            print()

    def conf_dump_command(self, args):
        """Команда conf-dump - выводит конфигурацию эмулятора"""
        print("Конфигурация эмулятора:")
        print("=" * 30)
        for key, value in self.config.items():
            if value is None:
                value = "не задано"
            print(f"{key}: {value}")
        print("=" * 30)

    def exit_command(self, args):
        """Команда exit - завершение работы эмулятора"""
        if args:
            try:
                exit_code = int(args[0])
                print(f"Exiting with code: {exit_code}")
                sys.exit(exit_code)
            except ValueError:
                print("exit: numeric argument required")
                sys.exit(1)
        else:
            print("Exiting shell")
            sys.exit(0)

def parse_arguments():
    """Парсит аргументы командной строки"""
    parser = argparse.ArgumentParser(
        description='Эмулятор командной строки UNIX-подобной ОС',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python3 shell.py                                    # Интерактивный режим
  python3 shell.py --vfs-path /path/to/vfs.xml       # С VFS
  python3 shell.py --startup-script script.txt       # Со стартовым скриптом
  python3 shell.py --vfs-path vfs.xml --startup-script script.txt  # Оба параметра
        """
    )
    
    parser.add_argument(
        '--vfs-path',
        type=str,
        help='Путь к физическому расположению VFS (XML файл)'
    )
    
    parser.add_argument(
        '--startup-script',
        type=str,
        help='Путь к стартовому скрипту для выполнения команд эмулятора'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Включить отладочный вывод параметров при запуске'
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    # Отладочный вывод параметров
    if args.debug:
        print("Отладочный вывод параметров эмулятора:")
        print("=" * 40)
        print(f"vfs_path: {args.vfs_path}")
        print(f"startup_script: {args.startup_script}")
        print(f"debug: {args.debug}")
        print("=" * 40)
        print()
    
    # Создание и запуск эмулятора
    shell = Shell(vfs_path=args.vfs_path, startup_script=args.startup_script)
    shell.run()
