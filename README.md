# Malyutki_Shutova

## Event ticketing system

## Description
Система управляет жизненным циклом билетов: от просмотра и бронировки до оплаты, генерации QR-кодов и личного кабинета пользователя.

Factory Pattern для централизованного создания билетов и списания мест
Strategy Pattern для гибкой замены алгоритма оплаты
Decorator Pattern для маршрутизации во Flask
SOLID-архитектура и чистый OOP, отдельные слои для моделей, сервисов и контроллеров

Система подходит для любого небольшого или среднего проекта по продаже билетов.

## Features
* Просмотр каталога событий с иллюстрациями и детальной информацией
* Карусель «Ближайших событий» на главной странице
* Бронирование билета с таймером (по умолчанию 15 минут)
* Оплата через Strategy (имитация успешной/неуспешной транзакции)
* Генерация QR-кода и вывод его в личном кабинете и в письме
* Личный кабинет: профиль пользователя, список купленных билетов, возможность дозавершить оплату в пределах таймера
* Email-уведомления об успешной покупке билета и сам билет


## Repository content
```
ticket_complete_project/
├─ event_ticketing/
│  ├─ db.py                   # DB engine, сессии, Base
│  ├─ qr.py                   # функция generate_qr_png
│  ├─ notify.py               # stub send_mail
│  ├─ settings.py             # SMTP
│  ├─ models/
│  │  ├─ user.py              # UserDB
│  │  ├─ event.py             # EventDB
│  │  └─ ticket.py            # TicketDB
│  └─ services/
│     ├─ factory.py           # TicketFactory
│     └─ strategy.py          # PaymentStrategy
├─ web/
│  ├─ app.py                  # Flask-приложения, маршруты
│  ├─ static/
│     └─...                   # Изображения для сайта                   
│  └─ templates/
│     ├─ base.html
│     ├─ index.html
│     ├─ event.html
│     ├─ pay.html
│     ├─ ticket.html
│     ├─ cabinet.html
│     ├─ login.html
│     └─ register.html
├─ apply_sql.py
├─ init_events.sql
├─ requirements.txt
└─ tickets.db                 # SQLite-файл (генерируется автоматически)
```

## Installation
1. Установите Python 3.10+
2. Скачайте архив ticket_complete_project.zip
3. Распакуйте его в удобную папку.
4. В командной строке перейдите в корень проекта: 
```
cd <Ваш адрес корневой папки>/ticket_complete_project
```
5. Создайте и активируйте визуальное окружение: 
```
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```
6. Установите зависимости: pip install -r requirements.txt    

## Usage
1. Находясь в корневой папке проекта, запустить сервер: 
```
python -m web.app
```
2. Открыть в браузере http://127.0.0.1:5000
3. Вуаля! Сайт в вашем распоряжении, зарегистрируйтесь и можете использовать все возможности!

## Support
Бог вам в помощь...

## Roadmap
Мотивацию надо поднять!

1. Реализовать различные способы оплаты через интерфейс PaymentStrategy
2. Добавить возможность регистрации для организаторов мероприятий и реализовать им специальный интерфейс работы на сайте.

## Authors and acknowledgment
Проект создан этими прекрасными жещинами:
* Гришанова Мария Алексеевна - teamlead, UML, тестировщик, жоский подгоняла-кэп
* Данилова Алика Павловна - frontend-разработчик, дизайнер, тестировщик
* Иванова Василиса Ивановна - backend-разработчик, тестировщик
