Парсер вакансия с сайта HH.ru

Этот проект представляет собой веб-приложение на Flask для поиска и анализа вакансий с использованием API hh.ru. Приложение собирает вакансии по заданным критериям и отображает их в удобном для пользователя виде.


Предварительные требования:

- Установленный Docker и Docker Compose
- Python 3.8 (если запускать локально без Docker)


 Структура проекта:
- app.py - основной файл приложения Flask.
- templates/ - директория с HTML-шаблонами.
- requirements.txt - файл с зависимостями проекта.
- Dockerfile - конфигурация для сборки Docker-образа.
- docker-compose.yml - конфигурация для Docker Compose.

  
Использование: 

1) Перейдите на главную страницу приложения.
2) Введите название вакансии, город и опыт работы.
3) Нажмите кнопку поиска.
4) Вакансии будут отображены на странице результатов вместе с аналитикой по количеству вакансий.