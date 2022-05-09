# Yatube 
#### Описание: 
Cоциальная сеть.Позволяет авторам создавать записи на различные темы,дает возможность комментировать их и подписываться/отписываться от авторов.Включает в себя администрирование, управление пользователями, работу с записями(создание, редактирование, удаление), объединение записей по сообществам, паджинацию, модель отправки электронных сообщений пользователям, основные шаблоны для страниц сайта.Для хранение данных используется SQLite.
#### Технологии:
- Python 3.7
- Django 2.2.19 
#### Запуск проекта в dev-режиме:
- Склонируйте репозиторий:  
``` git clone <название репозитория> ```    
- Установите и активируйте виртуальное окружение:  
``` python -m venv venv ```  
``` source venv/Scripts/activate ``` 
- Установите зависимости из файла requirements.txt:   
``` pip install -r requirements.txt ```
- Перейдите в папку hw05_final/yatube.
- Примените миграции:  
``` python manage.py makemigrations ```  
``` python manage.py migrate ```
- Выполните команду:   
``` python manage.py runserver ``` 
#### Автор:
Гут Владимир
