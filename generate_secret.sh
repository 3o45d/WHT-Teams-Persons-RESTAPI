#!/bin/bash
echo "Запуск скрипта..."

# Вывод текущей директории
pwd

# Вывод списка файлов в текущей директории
ls -la

if [ ! -f .env ]; then
    echo "Файл .env не найден, генерируем ключ..."
    SECRET_KEY=$(openssl rand -hex 32)
    echo "Сгенерированный ключ: $SECRET_KEY"
    echo "SECRET_KEY=$SECRET_KEY" > .env
else
    echo "Файл .env уже существует"
fi

# Проверка содержимого .env файла
echo "Содержимое .env файла:"
cat .env