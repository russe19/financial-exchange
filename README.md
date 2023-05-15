# Биржа
Проект биржи.
1. [Описание](#introduction)
2. [Что реализовано](#paragraph1)
    1. [Backend на Fast-API](#subparagraph1)
    2. [База данных](#subparagraph2)
    3. [Frontend на React](#subparagraph3)
    4. [Состояние на данный момент](#subparagraph4)
3. [Запуск проекта](#paragraph2)

## Описание <a name="introduction"></a>
В проекте реализована биржа по торговле различными валютами между пользователями, обмен валюты реализуется с помощью операций, первый пользователь создает операцию и назначает свою цену, а любой другой пользователь может ее приобрести. Курсы валют и операции хранятся в базе данных, и информация о нынешнем курсе постоянно обновляется. 
Структура проекта:
<img src="https://github.com/russe19/financial-exchange/assets/116742525/03e43cb5-0d5e-4dae-846a-79da0604343e" width="500" />
## Что реализовано <a name="paragraph1"></a>
### Backend на Fast-API<a name="subparagraph1"></a>
Проект состоин из 3-х основных приложений, с пользователями, операциями и валютами. 
Реализация API:
<img src="https://github.com/russe19/financial-exchange/assets/116742525/e4c79f02-78f9-4ffe-a4d3-f5468ae2ea6c" width="500" />
В проекте реализован функционал для работы с пользователями с помощью библиотеки fast-api-users. Данные о текущем пользователе хранятся в cookie, а для создания токена используется стандарт JWT. Реализованы операции по получению информации о пользователе, получению и пополнению баланса, просмотр всех операций и фильтрация по типу (продажа или покупка). Так же можно сосздать операцию. Посимо этого реализованы различные операции с валютами.
### База данных<a name="subparagraph2"></a>
В проекте используется база данных PostgreSQL.
Основные таблицы.
<img src="https://github.com/russe19/financial-exchange/assets/116742525/1fa05eaf-075e-4324-8d77-ff153f1e30e9" width="500" />
Получение всех элементов из таблицы currency:
<img src="https://github.com/russe19/financial-exchange/assets/116742525/1a6ea05c-3c6b-42d0-9ed9-f4873b4df2ba" width="500" />
### Frontend на React<a name="subparagraph3"></a>
Фронтенд реализуется с использованием JS и библиотеки React, с использованием функциональных компонентов и хуков. На данный момент реализованы только некоторые страницы, реализованы часто переиспользуемые компоненты такие как кнопки, инпуты, селекты и т.д.
Пример реализации страницы с элементами из таблицы currency:



Процесс оформления заказа состоит из 5 этапов, на первом этапе необходимо ввести необходимые данные о пользователе, если пользователь авторизован, то основные данные подставляются автоматически. Если пользователь не авторизован, то имеется возможность зарегистрироваться или авторизироваться. Зарегистрироваться можно прямо со страницы оформления заказа, для этого требуется ввести оригинальный e-mail пользователя, а так же два раза ввести пароль, во втором поле пароль должен быть продублирован. Вводимые данные в полях должны удовлетворять требованиям валидации.
![image](https://user-images.githubusercontent.com/116742525/233165193-3aca37e7-c310-44e5-b2b9-195a60a2e966.png)

Так же имеется возможность авторизироваться на сайте, если у вас уже есть аккаунт. Для этого необходимо нажать на кнопку "Авторизироваться".
![image](https://user-images.githubusercontent.com/116742525/233178242-74a1f8a6-019e-49a9-a9fd-4c46d20f343e.png)

На втором этапе оформляется способ доставки и конечный адрес, от способа доставки зависит конечная стоимость заказа. В settings задаются переменные, которые в дальнейшем применяются в расчете конечной стоимости в представлении.
![image](https://user-images.githubusercontent.com/116742525/233165271-20b35524-8f0a-4671-a784-bb67d52e06d8.png)

На третьем этапе выбирается способ оплаты.
![image](https://user-images.githubusercontent.com/116742525/233165327-52cc33b3-16f3-422b-9ea4-1426a7b8fd2b.png)

На четвертом этапе происходит подтверждение введенных данных, так же можно увидеть содержимое корзины и добавить комментарий к заказу. В момент подтверждения заказа все данные подставляются из кэша, и создается соответствующая запись в таблице с заказами.
![image](https://user-images.githubusercontent.com/116742525/233165529-61849ea4-307f-4a34-9de4-ae7f6593d344.png)

На последнем этапе требуется ввести код от карты и подтвердить заказ. После подтверждения мы переходим на страницу ожидания подтверждения оплаты. 
Происходит транзакция об оплате и ожидание ответа. С помощью Celery и Redis, был реализован микросервис, который позволяет во время выполнения оплаты перейти на сайт и выполнять различные действия.
![image](https://user-images.githubusercontent.com/116742525/233177901-abf0cbe2-7669-481e-873a-9f07ead40c2d.png)

### Разработка страницы «История заказов» и детальной страницы истории заказов<a name="subparagraph2"></a>
Была реализована страница страница, на которой отображаюся все заказы сделанные пользователем, отображается краткая информация о заказе и его статус.
![image](https://user-images.githubusercontent.com/116742525/233166180-aac29eac-2897-41ad-b503-0ccaa0f7f0d6.png)
На детальной странице отображается более подробная информация, можно посмотреть какие товары присутствуют в заказе и перейти к их детальным страницам.
![image](https://user-images.githubusercontent.com/116742525/233166354-2843a227-e64b-449c-b035-31c382dea2c3.png)

### Создание модели и детальной страницы продавца<a name="subparagraph3"></a>
На детальной странице продавца отображается вся подробная информация, выводится логотип продавца. Эти данные мы получаем из соответствующих моделей. Так же на этой странице формируется рейтинг самых популярных товаров, рейтинг мы строим на основании данных, полученных из всех сделанных на сайте заказов.
![image](https://user-images.githubusercontent.com/116742525/233162926-4b068b4a-0473-4ca9-99c6-3d574f23617b.png)

### Создание модели и детальной страницы товара<a name="subparagraph4"></a>
В процессе разработки проекта было принято решение разделить страницы товара и продукта, товар является связующей таблицей для продуктов и продавцов, между которыми реализуется связь многие ко многим. 
На странице продукта имеется возможность добавить к сравнению, 
<img src="https://user-images.githubusercontent.com/116742525/233164100-bad26a0a-4836-430f-8f56-df5d59ad9d87.png" width="700">
посмотреть описание и характеристики, 
![image](https://user-images.githubusercontent.com/116742525/233164163-05cc7da1-2339-44a9-9617-63cb9b3eb869.png)
а так же перейти на детальные страницы товара и продавца.
![image](https://user-images.githubusercontent.com/116742525/233164333-c6d18f5f-916e-48ed-8635-ce215060ad4d.png)
На странице товара имеется возможность добавить в корзину, оставить отзыв или посмотреть существующие, а так же посмотреть описание товара. 
![image](https://user-images.githubusercontent.com/116742525/233165086-15aa602f-569d-4fb4-b624-2ca103b66c66.png)


### Локализация сайта в админке, бэкенде и верстке<a name="subparagraph5"></a>
Была выполнена полная локализация сайта, основной язык на сайте является русский, в качестве дополнительного языка используется английский.
![image](https://user-images.githubusercontent.com/116742525/233164749-021e0200-94ff-4fa8-80e8-2050745eb854.png)


### Разработка верхнего меню и футера (верстка)<a name="subparagraph6"></a>
В проекте использовалась сторонняя верстка, много были переработаны и адаптированы верхнее меню и футор, и многие другие части кода.


## Запуск проекта в docker-compose <a name="paragraph2"></a>
> Запуск проекта производится с хостовой операционной системы в режиме "Продакшн" 

В файле .env расположены "секреты" для доступа к базе данных. В переменной *POSTGRES_PORT* указывает порт проброса из контейнера в хостовую операционную систему.
Запуск осуществляется через nginx и gunicorn. Приложение должно быть доступно на порту 8181.  
**Сборка проекта**
```commandline
docker-compose build
```
**Запуск проекта**
```commandline
docker-compose up -d
```
