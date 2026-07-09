# Конвертер валют — backend (хакатон Яндекс.Практикум)

> Команда 2 · 3–28 декабря 2024 · Яндекс.Практикум  
> Задача: API + веб, курсы с внешнего API, чтобы пользователь узнал,  
> **насколько подешевел отдых**… или наоборот. Обычно наоборот.

Организатор: АНО ДПО «Образовательные технологии Яндекса».

---

## Ссылки

| Что | Куда |
|-----|------|
| Живой сайт | [currency-converter-team2.vercel.app](https://currency-converter-team2.vercel.app/) |
| Frontend | [currency-converter-frontend](https://github.com/r0meo-1/currency-converter-frontend) |
| Backend (этот репо) | вы здесь |
| Figma | [макет](https://www.figma.com/design/PHxF5BGFK2kv0NvCDQu1xE/) |

---

## Технологии

**Frontend:** HTML5, JS ES6, Sass/SCSS  

**Backend:** Python, Django REST Framework, drf-spectacular, Redis, Celery, Nginx, Docker, Gunicorn, GitHub Actions, corsheaders  

Да, Celery на хакатоне — это либо смелость, либо дедлайн заставил полюбить асинхронность.

---

## Локальный запуск

```bash
git clone https://github.com/r0meo-1/currency-converter-backend.git
cd currency-converter-backend
cp .env.example .env
```

В `.env` минимум:

```
APIKEY=...                 # https://freecurrencyapi.com/
DB_HOST=postgres_db        # как сервис в docker-compose
```

```bash
docker compose up --build
```

Дальше — Swagger/доки в проекте (drf-spectacular обычно не врёт… почти).

---

## Зачем в портфолио

- Командный хакатон end-to-end  
- Django REST + Docker + CI  
- Понимание, что «курсы валют» = чужой API + ваши нервы при rate limit  

---

## Контакты

**[r0meo1.ru](https://r0meo1.ru)** · [@r0meo1](https://t.me/r0meo1)
