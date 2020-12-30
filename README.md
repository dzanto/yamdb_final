![example workflow name](https://github.com/dzanto/yamdb_final/workflows/Yamdb-app%20workflow/badge.svg)
# REST API для сервиса YaMDb — базы отзывов о фильмах, книгах и музыке.
запросы к API начинаются с `/api/v1/`
##### Demo:
- http://84.201.150.162/redoc/
- http://84.201.150.162/api/v1/


## Описание

Проект **YaMDb** собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
- Добавление категорий (Музыка, фильмы, книги и т.д.)
- Добавление жанров (Классика, джаз, рок и т.д.)
- Поиск по категории и жанру
- Добавление произведений (Книга, фильм, песня)
- Добавление отзывов к произведениям

## Запуск с помощью Docker
- Склонировать репозитарий `git clone https://github.com/dzanto/yamdb_final.git`
- Собрать docker образ `docker build -t dzanto/yamdb`
- Запустить
`docker-compose up --detach`
- выполнить миграции:
```
docker-compose exec web python manage.py makemigrations user_management
docker-compose exec web python manage.py makemigrations api
docker-compose exec web python manage.py migrate
```
- создать суперпользователя
```
docker-compose exec web python manage.py migrate
```

## Алгоритм регистрации пользователей
1. Пользователь отправляет запрос с параметром `email` на `/auth/email/`.
2. **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес  `email` .
3. Пользователь отправляет запрос с параметрами `email` и `confirmation_code` на `/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на `/users/me/` и заполняет поля в своём профайле (описание полей — в документации).

## Пользовательские роли
- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь** — может, как и **Аноним**, читать всё, дополнительно он может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять **свои** отзывы и комментарии.
- **Модератор** — те же права, что и у **Аутентифицированного пользователя** плюс право удалять **любые** отзывы и комментарии.
- **Администратор** — полные права на управление проектом и всем его содержимым. Может создавать и удалять категории и произведения. Может назначать роли пользователям.
- **Администратор Django** — те же права, что и у роли **Администратор**.


Автор: Shishlin A.
https://vologda.hh.ru/resume/91066c72ff0876d5180039ed1f44796674474f

Проект выполнен командой из трех разработчиков