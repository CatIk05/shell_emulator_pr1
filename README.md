# Эмулятор командной строки UNIX

## Описание

Этот проект представляет собой эмулятор командной строки UNIX-подобной ОС, реализованный на Python. Проект разрабатывается поэтапно, каждый этап добавляет новую функциональность.

## Этапы разработки

### ✅ Этап 1: REPL (Завершен)
### ✅ Этап 2: Конфигурация (Завершен)
### ✅ Этап 3: VFS (Завершен)
### ⏳ Этап 4: Основные команды (Планируется)
### ⏳ Этап 5: Дополнительные команды (Планируется)

## Реализованная функциональность

### Этап 1: REPL

### 1. Консольный интерфейс (CLI)
- Приложение работает в форме консольного интерфейса
- Поддерживает интерактивный ввод команд

### 2. Приглашение к вводу
- Формируется на основе реальных данных ОС
- Формат: `username@hostname:directory$`
- Поддерживает отображение домашней директории как `~`
- Пример: `ivanblazhko@MacBook-Pro-VanechKa.local:~/Desktop/Учеба/КУ/pr1$`

### 3. Парсер команд
- Поддерживает раскрытие переменных окружения в форматах:
  - `$VAR` - простая переменная
  - `${VAR}` - переменная в фигурных скобках
- Поддерживает кавычки (одинарные и двойные)
- Корректно обрабатывает пробелы в аргументах

### 4. Команды-заглушки
- **ls** - выводит информацию о том, что бы было выведено
- **cd** - показывает, в какую директорию был бы выполнен переход
- **echo** - выводит переданные аргументы (с поддержкой переменных окружения)
- **exit** - завершает работу эмулятора (с поддержкой кода возврата)

### 5. Обработка ошибок
- Обработка несуществующих команд
- Обработка некорректных аргументов
- Обработка прерывания (Ctrl+C)
- Обработка EOF (Ctrl+D)

### Этап 2: Конфигурация

### 1. Параметры командной строки
- `--vfs-path` - путь к физическому расположению VFS (XML файл)
- `--startup-script` - путь к стартовому скрипту для выполнения команд
- `--debug` - включить отладочный вывод параметров при запуске
- `--help` - справка по параметрам

### 2. Стартовые скрипты
- Выполнение команд последовательно из файла
- Пропуск пустых строк и комментариев (начинающихся с #)
- Обработка ошибок - ошибочные строки пропускаются
- Отображение ввода и вывода, имитируя диалог с пользователем

### 3. Команда conf-dump
- Выводит конфигурацию эмулятора в формате ключ-значение
- Показывает все параметры: vfs_path, startup_script, username, hostname, current_dir, home_dir

### 4. Отладочный вывод
- При запуске с флагом --debug отображаются все заданные параметры
- Помогает в отладке и проверке конфигурации

### Этап 3: VFS (Виртуальная файловая система)

### 1. Класс VFS
- Полная виртуальная файловая система, работающая в памяти
- Загрузка структуры из XML файлов
- Поддержка директорий и файлов с содержимым
- Все операции выполняются только в памяти

### 2. XML формат VFS
- Структурированное описание файловой системы в XML
- Поддержка вложенных директорий любой глубины
- Атрибуты для файлов и директорий
- Поддержка base64 кодирования для двоичных данных

### 3. Команды VFS
- **ls** - список содержимого директории (реальная логика)
- **cd** - смена директории с поддержкой относительных путей, `..`, `/`
- **pwd** - вывод текущей директории в VFS
- **cat** - вывод содержимого файлов
- **echo** - вывод текста с поддержкой переменных окружения

### 4. Навигация по VFS
- Абсолютные пути (начинающиеся с `/`)
- Относительные пути
- Переход в родительскую директорию (`..`)
- Переход в корень (`/`)
- Автоматическое обновление приглашения

### 5. Base64 поддержка
- Декодирование base64 содержимого файлов
- Атрибут `encoding="base64"` в XML
- Автоматическое определение и декодирование

### 6. Обработка ошибок VFS
- Корректные сообщения об ошибках для несуществующих файлов/директорий
- Продолжение работы при ошибках в стартовых скриптах
- Валидация путей и структуры VFS

## Файлы проекта

### Основные файлы
- `shell.py` - основной файл эмулятора (все этапы)

### VFS файлы (Этап 3)
- `vfs_minimal.xml` - минимальная VFS с одним файлом
- `vfs_files.xml` - VFS с несколькими файлами и директориями
- `vfs_deep.xml` - VFS с 3+ уровнями вложенности
- `vfs_base64.xml` - VFS с base64 кодированием

### Тестовые файлы
- `test_stage1.py` - автоматические тесты функциональности (Этап 1)
- `demo_stage1.py` - интерактивная демонстрация (Этап 1)
- `test_script.txt` - тестовый стартовый скрипт (Этап 2)
- `test_all_commands.txt` - стартовый скрипт для всех команд (Этап 3)

### Скрипты реальной ОС
- `test_basic.sh` - базовое тестирование всех параметров
- `test_startup_script.sh` - тестирование стартовых скриптов
- `test_vfs_minimal.sh` - тестирование минимальной VFS
- `test_vfs_files.sh` - тестирование VFS с файлами
- `test_vfs_deep.sh` - тестирование глубокой VFS
- `test_vfs_base64.sh` - тестирование VFS с base64

### Документация
- `README_stage1.md` - данный файл с описанием всех этапов

## Запуск

### Интерактивный режим
```bash
python3 shell.py
```

### С параметрами командной строки
```bash
# С отладочным выводом
python3 shell.py --debug

# Со стартовым скриптом
python3 shell.py --startup-script test_script.txt

# С VFS (реальная функциональность)
python3 shell.py --vfs-path vfs_files.xml

# Со всеми параметрами
python3 shell.py --debug --vfs-path vfs_files.xml --startup-script test_all_commands.txt

# Справка
python3 shell.py --help
```

### Работа с VFS
```bash
# Минимальная VFS
python3 shell.py --vfs-path vfs_minimal.xml

# VFS с несколькими файлами
python3 shell.py --vfs-path vfs_files.xml

# Глубокая VFS (3+ уровня)
python3 shell.py --vfs-path vfs_deep.xml

# VFS с base64 кодированием
python3 shell.py --vfs-path vfs_base64.xml

# VFS со стартовым скриптом
python3 shell.py --vfs-path vfs_files.xml --startup-script test_all_commands.txt
```

### Тестирование
```bash
# Автоматические тесты (Этап 1)
python3 test_stage1.py

# Интерактивная демонстрация (Этап 1)
python3 demo_stage1.py

# Скрипты реальной ОС (Этапы 2-3)
./test_basic.sh
./test_startup_script.sh

# Тестирование VFS (Этап 3)
./test_vfs_minimal.sh
./test_vfs_files.sh
./test_vfs_deep.sh
./test_vfs_base64.sh
```

## Примеры использования

### Базовые команды
```bash
$ ls
ls: command called with arguments: []
ls: would list contents of current directory

$ ls /home /tmp
ls: command called with arguments: ['/home', '/tmp']
ls: would list contents of: ['/home', '/tmp']

$ cd /tmp
cd: would change to directory: /tmp

$ cd
cd: would change to home directory: /Users/ivanblazhko
```

### Переменные окружения
```bash
$ echo $HOME
/Users/ivanblazhko

$ echo ${USER}
ivanblazhko

$ echo $NONEXISTENT
$NONEXISTENT
```

### Обработка ошибок
```bash
$ nonexistent_command
Command not found: nonexistent_command

$ cd /tmp /home
cd: too many arguments
Usage: cd [directory]

$ exit 42
Exiting with code: 42
```

### Кавычки и пробелы
```bash
$ echo "Hello World"
Hello World

$ ls 'file with spaces'
ls: command called with arguments: ["'file with spaces'"]
ls: would list contents of: ["'file with spaces'"]
```

### Конфигурация (Этап 2)
```bash
$ conf-dump
Конфигурация эмулятора:
==============================
vfs_path: не задано
startup_script: не задано
username: ivanblazhko
hostname: MacBook-Pro-VanechKa.local
current_dir: /Users/ivanblazhko/Desktop/Учеба/КУ/pr1
home_dir: /Users/ivanblazhko
==============================

$ python3 shell.py --debug
Отладочный вывод параметров эмулятора:
========================================
vfs_path: None
startup_script: None
debug: True
========================================

$ python3 shell.py --startup-script test_script.txt
Выполнение стартового скрипта: test_script.txt
--------------------------------------------------
root@MacBook-Pro-VanechKa.local:~/Desktop/Учеба/КУ/pr1$ echo "Добро пожаловать в тестовый скрипт!"
"Добро пожаловать в тестовый скрипт!"
...
```

### VFS (Этап 3)
```bash
$ python3 shell.py --vfs-path vfs_files.xml
VFS загружена из vfs_files.xml
Добро пожаловать в эмулятор командной строки!
Доступные команды: ls, cd, echo, cat, pwd, conf-dump, exit
--------------------------------------------------
root@MacBook-Pro-VanechKa.local:/$ ls
root/
root@MacBook-Pro-VanechKa.local:/$ cd root
root@MacBook-Pro-VanechKa.local:/root$ ls
logs/
temp/
README.txt
config.txt
data.txt
root@MacBook-Pro-VanechKa.local:/root$ cat README.txt
Добро пожаловать в VFS с несколькими файлами!
root@MacBook-Pro-VanechKa.local:/root$ cd logs
root@MacBook-Pro-VanechKa.local:/root/logs$ ls
app.log
error.log
root@MacBook-Pro-VanechKa.local:/root/logs$ cat app.log
Лог приложения
root@MacBook-Pro-VanechKa.local:/root/logs$ cd ..
root@MacBook-Pro-VanechKa.local:/root$ pwd
/root
root@MacBook-Pro-VanechKa.local:/root$ cd /
root@MacBook-Pro-VanechKa.local:/$ pwd
/
```

### Base64 кодирование
```bash
$ python3 shell.py --vfs-path vfs_base64.xml
VFS загружена из vfs_base64.xml
root@MacBook-Pro-VanechKa.local:/$ cd root
root@MacBook-Pro-VanechKa.local:/root$ cat binary.txt
Hello World! This is a base64 encoded file.
root@MacBook-Pro-VanechKa.local:/root$ cat config.txt
ServerName=myserver
Port=8080
Debug=true
```

## Технические детали

### Архитектура
- Класс `Shell` - основной класс эмулятора
- Класс `VFS` - виртуальная файловая система
- Словарь `commands` - регистр доступных команд
- Метод `parse_command()` - парсер команд с поддержкой переменных
- Метод `execute()` - выполнение команд с обработкой ошибок

### VFS архитектура
- `VFS.__init__()` - инициализация и загрузка из XML
- `VFS.load_from_xml()` - парсинг XML структуры
- `VFS._parse_xml_element()` - рекурсивный парсинг элементов
- `VFS.list_directory()` - получение списка содержимого
- `VFS.get_file_content()` - чтение содержимого файлов
- `VFS.get_node()` - получение узла по пути
- Поддержка base64 декодирования

### Парсинг переменных окружения
- Использует регулярные выражения для поиска переменных
- Поддерживает форматы `$VAR` и `${VAR}`
- Несуществующие переменные остаются в исходном виде
- Переменные в кавычках не раскрываются

### Обработка ошибок
- Try-catch блоки на всех уровнях
- Информативные сообщения об ошибках
- Корректное завершение при прерывании

## Соответствие требованиям

### Этап 1: REPL
✅ **Приложение реализовано в форме консольного интерфейса (CLI)**  
✅ **Приглашение формируется на основе реальных данных ОС**  
✅ **Парсер поддерживает раскрытие переменных окружения**  
✅ **Реализованы команды-заглушки ls, cd**  
✅ **Реализована команда exit**  
✅ **Демонстрация работы в интерактивном режиме**  
✅ **Показаны примеры обработки ошибок**

### Этап 2: Конфигурация
✅ **Параметры командной строки: --vfs-path, --startup-script**  
✅ **Стартовый скрипт выполняет команды последовательно**  
✅ **Ошибочные строки в скрипте пропускаются**  
✅ **Отображается ввод и вывод, имитируя диалог**  
✅ **Команда conf-dump выводит параметры в формате ключ-значение**  
✅ **Созданы скрипты реальной ОС для тестирования**  
✅ **Отладочный вывод всех заданных параметров при запуске**

### Этап 3: VFS
✅ **Все операции выполняются в памяти**  
✅ **Источником VFS является XML-файл**  
✅ **Для двоичных данных используется base64**  
✅ **Созданы скрипты для тестирования различных вариантов VFS**  
✅ **Создан стартовый скрипт для тестирования всех команд**  
✅ **Реализована работа с VFS и обработка ошибок**

## Формат XML VFS

### Структура XML файла:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<vfs>
    <directory name="root">
        <file name="README.txt">Содержимое файла</file>
        <file name="config.txt" encoding="base64">U2VydmVyTmFtZT1teXNlcnZlcg==</file>
        <directory name="logs">
            <file name="app.log">Лог приложения</file>
            <file name="error.log">Лог ошибок</file>
        </directory>
    </directory>
</vfs>
```

### Элементы XML:
- **`<vfs>`** - корневой элемент
- **`<directory name="...">`** - директория с именем
- **`<file name="...">`** - файл с содержимым
- **`encoding="base64"`** - атрибут для base64 кодирования

### Примеры VFS файлов:
- **Минимальная**: `vfs_minimal.xml` - один файл в корне
- **С файлами**: `vfs_files.xml` - несколько файлов и директорий
- **Глубокая**: `vfs_deep.xml` - 3+ уровня вложенности
- **Base64**: `vfs_base64.xml` - файлы с base64 кодированием

## Следующие этапы

- **Этап 4**: Основные команды (реальная логика для ls, cd, date, whoami)
- **Этап 5**: Дополнительные команды (mkdir, cp)
