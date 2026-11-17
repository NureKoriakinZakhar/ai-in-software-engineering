# Зрізи «Сервісу студентських звернень»

Розділи вказано посиланнями на docs/; правила не копіюються.
Відповідність назв методички: issues → requests, users → staff, priority → urgency
(docs/requirements.md §2).

## A. Створення й читання
- Код (app/): schemas.py, models.py, service.py, repository.py, database.py, api.py, main.py
- Тести (tests/): conftest.py, test_health_staff.py, test_requests.py, test_persistence.py
- Читати: docs/api-contract.md — вступ, §1 (RequestCreate, Request, Completeness,
  StaffList, Health, Error), §2.1–2.5; docs/requirements.md — §6.1–6.4, §6.10–6.12, §9
- Критерії: FR-01, FR-02 (деталізація, порядок), FR-07 (збереження) —
  AC-01-01, AC-01-02, AC-01-03, AC-02-03, AC-02-05, AC-07-04
- Сценарії: T01, T02, T03, T13

## B. Редагування й підтвердження типу
- Код (app/): schemas.py, service.py, repository.py, api.py
- Тести (tests/): test_patch.py
- Читати: docs/api-contract.md — §1 RequestPatch, §2.6, §3 «Частково невалідний PATCH»;
  docs/requirements.md — D-01..D-04, D-11, §6.1, §6.11, §8
- Критерії: FR-03, FR-04 (підтвердження), FR-05 — AC-03-01..AC-03-08,
  AC-04-05..AC-04-08, AC-05-01..AC-05-03
- Сценарії: T07, T08, T14

## C. Статуси й закриття
- Код (app/): schemas.py, service.py, api.py
- Тести (tests/): test_status_close.py
- Читати: docs/api-contract.md — §1 StatusPatch, CloseInput, ResolutionInput, §2.7, §2.8,
  §3, §4; docs/requirements.md — D-05, D-06, D-12, §6.6, §6.8, §6.9, §6.11, §7
- Критерії: FR-04 (переходи), FR-07 (результат) — AC-04-01..AC-04-04, AC-04-09,
  AC-07-01..AC-07-03, AC-07-05..AC-07-07
- Сценарії: T09, T10
- Час у тестах: FakeClock із tests/conftest.py (START 2026-10-10T10:00:00Z, +1 с
  на кожен виклик). issued_on і corrected_at задавай не пізніше START, інакше D-12
  правильно поверне 422.

## D. Коментарі
- Код (app/): schemas.py, service.py, repository.py, api.py
- Тести (tests/): test_comments.py
- Читати: docs/api-contract.md — §1 CommentCreate, Comment, §2.9, §2.10;
  docs/requirements.md — §6.5, FR-06
- Критерії: FR-06 — AC-06-01..AC-06-05
- Сценарії: T11, T12

## E. Фільтри
- Код (app/): service.py, api.py
- Тести (tests/): test_filters.py
- Читати: docs/api-contract.md — §2.4 (query status, urgency, request_type);
  docs/requirements.md — FR-02
- Критерії: FR-02 — AC-02-01, AC-02-02, AC-02-04
- Сценарії: T04, T05, T06

## Сценарії T-xx методички → критерії ЛР1
| T | Критерії |
|---|---|
| T01 | AC-01-01 |
| T02 | AC-01-02, AC-01-03 |
| T03 | AC-02-03, AC-02-05 |
| T04 | AC-02-02 (status) |
| T05 | AC-02-04 |
| T06 | AC-02-01 |
| T07 | AC-03-01, AC-03-02, AC-03-04 |
| T08 | AC-05-01..AC-05-03 |
| T09 | AC-04-01, AC-04-04, AC-04-09 |
| T10 | AC-04-03 |
| T11 | AC-06-01, AC-06-02 |
| T12 | AC-06-01, AC-06-03 |
| T13 | AC-07-04 |
| T14 | AC-03-03 |
