# Сервіс студентських звернень — ЛР2

Локальний REST-сервіс за специфікацією ЛР1 ([docs/requirements.md](docs/requirements.md),
[docs/api-contract.md](docs/api-contract.md), [docs/architecture.md](docs/architecture.md)).
Бригада ПЗПІ-23-8: Кириченко Кирило, Корякін Захар.

## Вимоги

- Python 3.12 (погоджена в бригаді версія; специфікація допускає 3.11+). Перевірено на 3.12.14, macOS.
- Залежності зафіксовано в [requirements-lock.txt](requirements-lock.txt).

## Чисте встановлення

```sh
python3.12 -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows cmd: .venv\Scripts\activate.bat
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-lock.txt
```

Якщо PowerShell забороняє активацію, викликайте `.venv\Scripts\python.exe -m ...` без зміни політики.

## Запуск

Застосунок створюється фабрикою `create_app()`, тому uvicorn запускається з `--factory`:

```sh
python -m uvicorn app.main:create_app --factory --host 127.0.0.1 --port 8000
```

- Swagger UI: http://127.0.0.1:8000/docs — для кожного маршруту є іменовані приклади запитів
  (успішні сценарії й типові помилки) у списку «Examples».
- Робоча БД: `data/student_requests.sqlite3` (створюється автоматично, у Git не потрапляє).
  Інший шлях: `APP_DB_PATH=/шлях/до/файлу.sqlite3`.
- Сервіс прив'язано лише до 127.0.0.1.

## Тести та статичний аналіз

```sh
python -m pytest -q
python -m ruff check app tests --select E4,E7,E9,F,I
```

Кожен тест отримує окремий файл SQLite у `tmp_path` і керований годинник (`tests/conftest.py`);
робоча БД тестами не використовується.

## Маршрути (10)

| Метод | Шлях | Призначення |
|---|---|---|
| GET | /health | Перевірка процесу |
| GET | /staff | Довідник співробітників 1 — Agent A, 2 — Agent B |
| POST | /requests | Створення звернення (OPEN) |
| GET | /requests | Список; фільтри `status`, `urgency`, `request_type` (AND) |
| GET | /requests/{id} | Деталі звернення з completeness і resolution |
| PATCH | /requests/{id} | Часткове редагування, підтвердження типу, призначення |
| PATCH | /requests/{id}/status | Зміна статусу за матрицею 3×3 |
| POST | /requests/{id}/close | Закриття з резолюцією |
| POST | /requests/{id}/comments | Додавання коментаря |
| GET | /requests/{id}/comments | Коментарі звернення |

## Приклад сценарію

```sh
B=http://127.0.0.1:8000
H="Content-Type: application/json"
curl -s -X POST $B/requests -H "$H" -d '{"student_id":"S-2308001","full_name":"Тестовий Студент","title":"Довідка про навчання","urgency":"high","certificate_details":{"language":"uk","purpose":"За місцем вимоги","delivery_method":"digital"}}'
curl -s -X PATCH $B/requests/1 -H "$H" -d '{"request_type":"ENROLLMENT_CERTIFICATE","type_confirmed_by":1,"assignee_id":2}'
curl -s -X POST $B/requests/1/comments -H "$H" -d '{"author_id":2,"text":"Довідку підготовлено."}'
curl -s -X PATCH $B/requests/1/status -H "$H" -d '{"status":"IN_PROGRESS"}'
curl -s -X POST $B/requests/1/close -H "$H" -d '{"resolution":{"resolution_code":"COMPLETED","result_details":{"certificate_number":"CERT-2026-001","issued_on":"2026-11-17"},"resolved_by":1}}'
curl -s -X PATCH $B/requests/1/status -H "$H" -d '{"status":"OPEN"}'   # 409 INVALID_TRANSITION
curl -s "$B/requests?status=CLOSED&urgency=high"
```

`issued_on` має бути не раніше дати створення і не пізніше поточної дати UTC (D-12).
Тіло запиту передається з `Content-Type: application/json`.

## Skill для AI-агента

Skill `tracker-slice` розміщено в [.claude/skills/tracker-slice/](.claude/skills/tracker-slice/)
і використовується з Claude Code. Агента потрібно запускати з теки `lab2/`, щоб Skill
і шляхи `docs/`, `app/`, `tests/` визначалися від кореня проєкту. Каталог `.agents/skills/`
для інших агентів не створювався: бригада працювала лише з Claude Code.

## Навчальні обмеження

- Автентифікації немає: `author_id`, `assignee_id`, `type_confirmed_by`, `resolved_by` — лише
  синтетичні номери тестових співробітників 1/2, а не доказ особи.
- Усі дані синтетичні; видалення звернень, пагінація, GUI, Docker і хмара поза обсягом.
- Час зберігається з точністю до секунди (UTC, `YYYY-MM-DDTHH:MM:SSZ`).
