<h1 align="center">Telegram-bot | Hotel search and booking.
​
    
[![Telegram URL](https://www.dampftbeidir.de/mediafiles/tpl/icon-telegram.png)](https://t.me/searchhotels_sb_bot) 
</h1>

***

## Описание проекта

[Телеграмм бот](@searchhotels_sb_bot) ищет отели в заданном пользователем городе используя API сайта Hotels.com
Используя API сайта [Hotels.com](https://hotels.com/).
<br> Пользователь с помощью специальных команд бота может сделать следующее: 
<br/>
- Осуществить поиск бюджетных вариантов отелей в городе (**команда /low**). 
- Осуществить поиск дорогих отелей в городе (**команда /high**). 
- Осуществить поиск отелей, наиболее подходящих по цене и расположению от центра (**команда /custom**). 
- Узнать историю поиска отелей (**команда /history**).

### Запуск проекта (на примере Windows)

- Создайте на своем компьютере папку проекта
- Склонируйте этот репозиторий в папку проекта `https://gitlab.skillbox.ru/ilia_semynin/python_basic_diploma/-/tree/SemyninTGBot`
- Создайте файл `.env` и добавьте в него переменные окружения, следующего вида:
<br>
    BOT_TOKEN= "ваш бот токен"<br>
    RAPID_API_KEY= "ваш rapid_api key"<br>
<br>
- Активируйте виртуальное окружение `pipenv shell`
- Установите все зависимости `pipenv install --ignore-Pipfile`
- Запустите бота командой `pipenv run main.py` из Терминала из папки с проектом 

***

## Описание работы команд

### Команда /start

После ввода команды: 
1. Выводится приветствие с кратким описанием, что умеет бот;

### Команда /help

После ввода команды: 
1. Выводится список всех команд, с кратким описанием того, что делает каждая команда;


### Команда /low

После ввода команды у пользователя запрашивается: 
1. Город, где будет проводиться поиск;
2. Далее пользователю необходимо уточнить город выбрав его из списка в виде клавиатуры;
3. Выбор валюты для оплаты проживания (USD или EUR);
4. Выводится календарь с возможностью выбора даты заезда или выезда.
5. Количество вариантов отелей;
6. Нужны ли пользователю фото отеля;
7. При положительном ответе пользователь также вводит количество необходимых фотографий.

### Команда /high

После ввода команды у пользователя запрашивается: 
1. Город, где будет проводиться поиск;
2. Далее пользователю необходимо уточнить город выбрав его из списка в виде клавиатуры;
3. Выбор валюты для оплаты проживания (USD или EUR);
4. Выводится календарь с возможностью выбора даты заезда или выезда.
5. Количество вариантов отелей;
6. Нужны ли пользователю фото отеля;
7. При положительном ответе пользователь также вводит количество необходимых фотографий.

### Команда /custom

После ввода команды у пользователя запрашивается: 
1. Город, где будет проводиться поиск;
2. Далее пользователю необходимо уточнить город выбрав его из списка в виде клавиатуры; 
3. Запрашивается минимальная и максимальная стоимость отеля в выбранной ранее валюте;
4. Запрашивается минимальная и максимальная удалённость отеля от центра;
5. Выводится календарь с возможностью выбора даты заезда или выезда. 
6. Количество вариантов отелей;
7. Нужны ли пользователю фото отеля;
8. При положительном ответе пользователь также вводит количество необходимых фотографий.


### Команда /history

После ввода команды выводится краткая история запросов пользователя 


## Описание внешнего вида и UI
Окно Telegram-бота при запущенном Python-скрипте воспринимает следующие команды:
- /start - запуск бота
- /help — помощь по командам бота 
- /low — вывод самых дешёвых отелей в городе
- /high — вывод самых дорогих отелей в городе 
- /custom — вывод отелей, наиболее подходящих по цене и расположению от центра
- /history — вывод истории поиска отелей

Для команд low, high и custom сообщение с результатом содержит краткую информацию по каждому отелю. 
В эту информацию входит: 
- Название отеля;
- Рейтинг;
- Адрес;
- Расстояние до центра;
- Цена за период;
- Сайт;
- Фотографии отеля.



## В разработке использованы

pyTelegramBotAPI==4.9.0<br>
python-dotenv==0.21.1<br>
pip==22.0.4<br>
certifi==2023.7.22<br>
requests==2.31.0<br>
idna==3.4<br>
urllib3==2.0.4<br>
setuptools==58.1.0<br>
loguru==0.7.0<br>
sqlitedict==2.1.0
python-telegram-bot-calendar==1.0.5
python-dateutil==2.8.2
