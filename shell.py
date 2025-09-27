import os
import sys
import readline
import re

class Shell:
    def __init__(self):
        self.username = os.getlogin()
        self.hostname = os.uname().nodename
        self.current_dir = os.getcwd()
        self.home_dir = os.path.expanduser("~")
        self.update_prompt()
        self.commands = {
            'ls': self.ls_command,
            'cd': self.cd_command,
            'echo': self.echo_command,
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
        print("Доступные команды: ls, cd, echo, exit")
        print("Поддерживаются переменные окружения: $VAR, ${VAR}")
        print("Для выхода используйте команду 'exit' или Ctrl+C")
        print("-" * 50)
        
        while True:
            try:
                user_input = input(self.prompt)
                self.execute(user_input)
            except (EOFError, KeyboardInterrupt):
                print("\nExiting shell")
                break
            except Exception as e:
                print(f"Ошибка: {e}")

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

if __name__ == "__main__":
    shell = Shell()
    shell.run()
