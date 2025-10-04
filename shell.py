import os
import sys
import readline
import re
import argparse
import xml.etree.ElementTree as ET
import base64
from pathlib import Path

class VFS:
    """Виртуальная файловая система"""
    
    def __init__(self, xml_path=None):
        self.root = {}
        self.current_path = "/"
        self.xml_path = xml_path
        
        if xml_path and os.path.exists(xml_path):
            self.load_from_xml(xml_path)
        elif xml_path:
            print(f"Предупреждение: VFS файл не найден: {xml_path}")
    
    def load_from_xml(self, xml_path):
        """Загружает VFS из XML файла"""
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            self.root = self._parse_xml_element(root)
            print(f"VFS загружена из {xml_path}")
        except Exception as e:
            print(f"Ошибка загрузки VFS: {e}")
            self.root = {}
    
    def _parse_xml_element(self, element):
        """Рекурсивно парсит XML элемент в структуру VFS"""
        result = {}
        
        for child in element:
            if child.tag == "directory":
                name = child.get("name", "")
                result[name] = {
                    "type": "directory",
                    "children": self._parse_xml_element(child)
                }
            elif child.tag == "file":
                name = child.get("name", "")
                content = child.text or ""
                
                # Проверяем, является ли содержимое base64
                if child.get("encoding") == "base64":
                    try:
                        content = base64.b64decode(content).decode('utf-8')
                    except:
                        content = child.text or ""
                
                result[name] = {
                    "type": "file",
                    "content": content
                }
        
        return result
    
    def get_path_parts(self, path):
        """Разбивает путь на части"""
        if path == "/":
            return []
        return [part for part in path.split("/") if part]
    
    def get_node(self, path):
        """Получает узел по пути"""
        if path == "/":
            return self.root
        
        parts = self.get_path_parts(path)
        current = self.root
        
        for part in parts:
            if part not in current or current[part]["type"] != "directory":
                return None
            current = current[part]["children"]
        
        return current
    
    def get_parent_node(self, path):
        """Получает родительский узел"""
        if path == "/":
            return None
        
        parts = self.get_path_parts(path)
        if len(parts) <= 1:
            return self.root
        
        parent_path = "/" + "/".join(parts[:-1])
        return self.get_node(parent_path)
    
    def list_directory(self, path="/"):
        """Список содержимого директории"""
        node = self.get_node(path)
        if not node:
            return None
        
        items = []
        for name, item in node.items():
            items.append({
                "name": name,
                "type": item["type"]
            })
        
        return sorted(items, key=lambda x: (x["type"], x["name"]))
    
    def get_file_content(self, path):
        """Получает содержимое файла"""
        parts = self.get_path_parts(path)
        if not parts:
            return None
        
        filename = parts[-1]
        parent_path = "/" + "/".join(parts[:-1]) if len(parts) > 1 else "/"
        
        parent_node = self.get_node(parent_path)
        if not parent_node or filename not in parent_node:
            return None
        
        file_node = parent_node[filename]
        if file_node["type"] != "file":
            return None
        
        return file_node["content"]
    
    def create_directory(self, path):
        """Создает директорию"""
        parts = self.get_path_parts(path)
        if not parts:
            return False
        
        dirname = parts[-1]
        parent_path = "/" + "/".join(parts[:-1]) if len(parts) > 1 else "/"
        
        parent_node = self.get_node(parent_path)
        if not parent_node:
            return False
        
        if dirname in parent_node:
            return False  # Уже существует
        
        parent_node[dirname] = {
            "type": "directory",
            "children": {}
        }
        return True
    
    def create_file(self, path, content=""):
        """Создает файл"""
        parts = self.get_path_parts(path)
        if not parts:
            return False
        
        filename = parts[-1]
        parent_path = "/" + "/".join(parts[:-1]) if len(parts) > 1 else "/"
        
        parent_node = self.get_node(parent_path)
        if not parent_node:
            return False
        
        if filename in parent_node:
            return False  # Уже существует
        
        parent_node[filename] = {
            "type": "file",
            "content": content
        }
        return True
    
    def copy_file(self, src_path, dst_path):
        """Копирует файл"""
        content = self.get_file_content(src_path)
        if content is None:
            return False
        
        return self.create_file(dst_path, content)

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
        
        # VFS
        self.vfs = VFS(vfs_path)
        self.vfs_current_path = "/"
        
        self.update_prompt()
        self.commands = {
            'ls': self.ls_command,
            'cd': self.cd_command,
            'echo': self.echo_command,
            'cat': self.cat_command,
            'pwd': self.pwd_command,
            'conf-dump': self.conf_dump_command,
            'exit': self.exit_command
        }
    
    def update_prompt(self):
        """Обновляет приглашение с учетом текущей директории"""
        if self.vfs_path:
            # Если используется VFS, показываем VFS путь
            vfs_display = self.vfs_current_path if self.vfs_current_path != "/" else "/"
            self.prompt = f"{self.username}@{self.hostname}:{vfs_display}$ "
        else:
            # Обычный режим - показываем реальную директорию
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
        if self.vfs_path:
            print("Доступные команды: ls, cd, echo, cat, pwd, conf-dump, exit")
        else:
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
        """Команда ls - список содержимого директории"""
        if self.vfs_path:
            # Режим VFS
            if args:
                target_path = args[0]
                # Нормализуем путь
                if not target_path.startswith("/"):
                    if self.vfs_current_path == "/":
                        target_path = "/" + target_path
                    else:
                        target_path = self.vfs_current_path + "/" + target_path
            else:
                target_path = self.vfs_current_path
            
            items = self.vfs.list_directory(target_path)
            if items is None:
                print(f"ls: {target_path}: No such file or directory")
                return
            
            if not items:
                return  # Пустая директория
            
            # Выводим содержимое
            for item in items:
                if item["type"] == "directory":
                    print(f"{item['name']}/")
                else:
                    print(item["name"])
        else:
            # Обычный режим - заглушка
            print(f"ls: command called with arguments: {args}")
            if args:
                print(f"ls: would list contents of: {args}")
            else:
                print("ls: would list contents of current directory")

    def cd_command(self, args):
        """Команда cd - смена директории"""
        if self.vfs_path:
            # Режим VFS
            if len(args) == 0:
                # cd без аргументов - переход в корень
                self.vfs_current_path = "/"
            elif len(args) == 1:
                target_dir = args[0]
                
                # Нормализуем путь
                if target_dir == "/":
                    new_path = "/"
                elif target_dir.startswith("/"):
                    new_path = target_dir
                elif target_dir == "..":
                    # Переход в родительскую директорию
                    if self.vfs_current_path == "/":
                        new_path = "/"  # Уже в корне
                    else:
                        parts = self.vfs_current_path.split("/")
                        if len(parts) <= 2:  # /root -> /
                            new_path = "/"
                        else:
                            new_path = "/" + "/".join(parts[1:-1])
                else:
                    # Относительный путь
                    if self.vfs_current_path == "/":
                        new_path = "/" + target_dir
                    else:
                        new_path = self.vfs_current_path + "/" + target_dir
                
                # Проверяем, существует ли директория
                if self.vfs.get_node(new_path) is not None:
                    self.vfs_current_path = new_path
                else:
                    print(f"cd: {target_dir}: No such file or directory")
            else:
                print("cd: too many arguments")
                print("Usage: cd [directory]")
            
            self.update_prompt()
        else:
            # Обычный режим - заглушка
            if len(args) == 0:
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

    def cat_command(self, args):
        """Команда cat - выводит содержимое файла"""
        if not args:
            print("cat: missing file operand")
            print("Usage: cat <file>")
            return
        
        if self.vfs_path:
            # Режим VFS
            for filename in args:
                # Нормализуем путь
                if not filename.startswith("/"):
                    if self.vfs_current_path == "/":
                        file_path = "/" + filename
                    else:
                        file_path = self.vfs_current_path + "/" + filename
                else:
                    file_path = filename
                
                content = self.vfs.get_file_content(file_path)
                if content is None:
                    print(f"cat: {filename}: No such file or directory")
                else:
                    print(content)
        else:
            # Обычный режим - заглушка
            print(f"cat: would display contents of: {args}")

    def pwd_command(self, args):
        """Команда pwd - выводит текущую директорию"""
        if self.vfs_path:
            # Режим VFS
            print(self.vfs_current_path)
        else:
            # Обычный режим
            print(self.current_dir)

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
