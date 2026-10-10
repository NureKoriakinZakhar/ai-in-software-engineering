# Prototype P1 — протокол перевірки

Корякін З. П.; Кириченко К. В.; ПЗПІ-23-8. Дата: 10.10.2026. Робоча версія: **P1 expanded routes — 10.10.2026**, page UX/UI v1.0. [Редагований макет](https://www.figma.com/design/WR2MU9NL1NdQj6LQJYAB7N).

Базові й розширені переходи перевірено у Present. Інструменти та спосіб роботи — у 09; мінітест наведено нижче. Дані фіктивні. Prototype симулює підготовлені стани, без backend і довільного введення.

## Усі стартові flow у Figma

У Present прочитано 18 стартових точок: Flow 1–17 і P1 — Zero issues. Flow — точка початку демонстрації, а не окрема функція продукту.

1. **[Flow 1 — основний список](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=12-2965&starting-point-node-id=12%3A2965&scaling=min-zoom&content-scaling=fixed)**, S-02-A, node 12:2965. All із вісьмома заявками → Important із 001/002/003/007 → Title → відповідні Details → Return. Create відкриває порожній overlay; кліки у поля підставляють fixture; Create показує ISS-009; Return — дев'ять заявок. Cancel закриває overlay. Порожні поля переводять у відповідні validation states. Це основний flow для захисту.
2. **[P1 — Zero issues](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=12-3073&starting-point-node-id=12%3A3073&scaling=min-zoom&content-scaling=fixed)**, S-02-C, node 12:3073. No issues yet → Create → підготовлена заповнена форма → ISS-009 → Return → список з однією заявкою. Cancel повертає до порожнього списку.
3. **[Flow 2 — заповнена форма з All](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=18-628&starting-point-node-id=18%3A628&scaling=min-zoom&content-scaling=fixed)**, M-01 / valid-from-All, node 18:628. Create → ISS-009 / from-All → Return → All із дев'ятьма записами. Це скорочений старт сценарію успіху; введення полів пропущене.
4. **[Flow 3 — заповнена форма з Important](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=18-645&starting-point-node-id=18%3A645&scaling=min-zoom&content-scaling=fixed)**, M-01 / valid-from-Important, node 18:645. Create → ISS-009 / from-Important → Return → Important із чотирма початковими записами. Нова ISS-009 не входить до Important, бо її priority = Not Set.
5. **[Flow 4 — заповнена форма з Empty](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=18-662&starting-point-node-id=18%3A662&scaling=min-zoom&content-scaling=fixed)**, M-01 / valid-from-Empty, node 18:662. Create → ISS-009 / from-Empty → Return → All з одним записом.

Flow 2–4 автоматично з'явилися під час налаштування transitions. Cancel у них має Close overlay і перевірений при відкритті форми зі списку; самостійний старт форми не має calling overlay/list. Для демонстрації Cancel використовується Flow 1 або P1 — Zero issues. Прямі старти Flow 2–4 окремо у Present не пройдено; відповідні success routes перевірено з calling lists.


Додаткові старти Flow 5–17 починаються з підготовленого вибору або коментаря; вони перевіряють Apply/Add Comment, а не довільне введення. Усі наведені маршрути пройдено у Present 10.10.2026:

- **[Flow 5](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=18-1178&starting-point-node-id=18%3A1178&scaling=min-zoom&content-scaling=fixed)** — Призначення Member A.
- **[Flow 6](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=18-1290&starting-point-node-id=18%3A1290&scaling=min-zoom&content-scaling=fixed)** — Перепризначення Member B.
- **[Flow 7](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=18-1403&starting-point-node-id=18%3A1403&scaling=min-zoom&content-scaling=fixed)** — Priority Low.
- **[Flow 8](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=18-1515&starting-point-node-id=18%3A1515&scaling=min-zoom&content-scaling=fixed)** — Priority Normal.
- **[Flow 9](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=18-1627&starting-point-node-id=18%3A1627&scaling=min-zoom&content-scaling=fixed)** — Priority High.
- **[Flow 10](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=18-1739&starting-point-node-id=18%3A1739&scaling=min-zoom&content-scaling=fixed)** — Priority Critical.
- **[Flow 11](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=18-1852&starting-point-node-id=18%3A1852&scaling=min-zoom&content-scaling=fixed)** — Open → In Progress.
- **[Flow 12](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=18-1981&starting-point-node-id=18%3A1981&scaling=min-zoom&content-scaling=fixed)** — In Progress → Resolved.
- **[Flow 13](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=18-2110&starting-point-node-id=18%3A2110&scaling=min-zoom&content-scaling=fixed)** — Resolved → In Progress.
- **[Flow 14](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=18-2239&starting-point-node-id=18%3A2239&scaling=min-zoom&content-scaling=fixed)** — Resolved → Closed → Important → All → повторний перегляд Closed.
- **[Flow 15](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=18-2669&starting-point-node-id=18%3A2669&scaling=min-zoom&content-scaling=fixed)** — Порожній коментар → validation.
- **[Flow 16](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=18-2801&starting-point-node-id=18%3A2801&scaling=min-zoom&content-scaling=fixed)** — Заповнений коментар → success.
- **[Flow 17](https://www.figma.com/proto/WR2MU9NL1NdQj6LQJYAB7N?node-id=18-2932&starting-point-node-id=18%3A2932&scaling=min-zoom&content-scaling=fixed)** — Заповнений коментар → save error.

## Підсумок виконання

37 connection tests мають фактичний PASS: P-01–08, P-11, P-17–44. Додатково перевірено сім карток ISS-001/002/004–008 зі списку after-create та Back; ISS-001 з Important; Cancel після Title error. Повний повтор кожного Title початкового All не заявляється. CONFIGURED означає оглянуту interaction у редакторі; NOT RUN — відсутність click-test, а не доведений дефект.

## Детальний протокол connections

44 рядки — розширений локальний план перевірки, не вимога методички щодо числа connections. P-01–P-28 описують базові маршрути; P-29–P-44 — додаткову інтерактивну симуляцію state examples. NOT RUN означає відсутність підтвердженого click-test, а не автоматичну відсутність відповідного UI-стану. Статичні результати окремо у 06.

|P-ID|Test|Hotspot|Trigger|Action|Target frame/state|Очікуваний видимий результат|Симуляція / межа|Фактичний клік-тест|
|---|---|---|---|---|---|---|---|---|
|P-01|T-08|S-02-A / C-02 Important|On click|Navigate to|S-02-B / baseline|001/002/003/007 visible; Important active|Navigation + prepared filtered data|PASS — Present, 10.10.2026|
|P-02|T-08|S-02-B / C-01 All|On click|Navigate to|S-02-A / baseline|All eight rows; All active|Navigation|PASS — Present, 10.10.2026|
|P-03|T-01/T-09|S-02-A / C-03|On click|Open overlay|M-01 / default|Modal over S-02-A; caller context preserved|Overlay navigation|PASS — Present, 10.10.2026|
|P-04|T-09|M-01 opened from S-02-A / C-08 Cancel|On click|Close overlay|Calling S-02-A|No created issue; original list state A|Overlay navigation; no persistence|PASS — Present, 10.10.2026|
|P-05|T-01/T-09|S-02-B / C-03|On click|Open overlay|M-01 / valid-from-Important|Modal over S-02-B; caller context preserved|Overlay navigation|PASS — Present, 10.10.2026|
|P-06|T-09|M-01 / valid-from-Important / C-08 Cancel|On click|Close overlay|Calling S-02-B|No created issue; original list state B|Overlay navigation; no persistence|PASS — Present, 10.10.2026|
|P-07|T-01/T-09|S-02-C / C-03|On click|Open overlay|M-01 / valid-from-Empty|Modal over S-02-C; caller context preserved|Overlay navigation|PASS — Present, 10.10.2026|
|P-08|T-09|M-01 / valid-from-Empty / C-08 Cancel|On click|Close overlay|Calling S-02-C|No created issue; original list state C|Overlay navigation; no persistence|PASS — Present, 10.10.2026|
|P-09|T-09|S-02-A / Title ISS-001|On click|Navigate to|S-03 / ISS-001|Same ID and all fields match fixture ISS-001|Prepared detail state, no data loading|CONFIGURED; detail/Back passed from after-create; full baseline retest not claimed|
|P-10|T-09|S-02-A / Title ISS-002|On click|Navigate to|S-03 / ISS-002|Same ID and all fields match fixture ISS-002|Prepared detail state, no data loading|CONFIGURED; detail/Back passed from after-create; full baseline retest not claimed|
|P-11|T-09|S-02-A / Title ISS-003|On click|Navigate to|S-03 / ISS-003 / shared baseline|Same ID and all fields match fixture ISS-003|Prepared detail state, no data loading|PASS — Present, 10.10.2026|
|P-12|T-09|S-02-A / Title ISS-004|On click|Navigate to|S-03 / ISS-004|Same ID and all fields match fixture ISS-004|Prepared detail state, no data loading|CONFIGURED; detail/Back passed from after-create; full baseline retest not claimed|
|P-13|T-09|S-02-A / Title ISS-005|On click|Navigate to|S-03 / ISS-005|Same ID and all fields match fixture ISS-005|Prepared detail state, no data loading|CONFIGURED; detail/Back passed from after-create; full baseline retest not claimed|
|P-14|T-09|S-02-A / Title ISS-006|On click|Navigate to|S-03 / ISS-006|Same ID and all fields match fixture ISS-006|Prepared detail state, no data loading|CONFIGURED; detail/Back passed from after-create; full baseline retest not claimed|
|P-15|T-09|S-02-A / Title ISS-007|On click|Navigate to|S-03 / ISS-007|Same ID and all fields match fixture ISS-007|Prepared detail state, no data loading|CONFIGURED; detail/Back passed from after-create; full baseline retest not claimed|
|P-16|T-09|S-02-A / Title ISS-008|On click|Navigate to|S-03 / ISS-008|Same ID and all fields match fixture ISS-008|Prepared detail state, no data loading|CONFIGURED; detail/Back passed from after-create; full baseline retest not claimed|
|P-17|T-09|S-02-B / Title ISS-003|On click|Navigate to|S-03 / ISS-003 / shared baseline|Resolved/High/Member A; prior tab Important|Prepared state simulation|PASS — Present, 10.10.2026|
|P-18|T-09|S-03 / ISS-003 / C-19|On click|Back|S-02-A / baseline|Return restores All|Prepared state simulation|PASS — Present, 10.10.2026|
|P-19|T-09|S-03 / ISS-003 / C-19|On click|Back|S-02-B / baseline|Return restores Important|Prepared state simulation|PASS — Present, 10.10.2026|
|P-20|T-01|M-01 / valid-from-All / C-07|On click|Navigate to|S-03 / ISS-009 / from-All|Open/Not Set/Unassigned; Member A; time 10:20; overlay dismissed|Prepared state simulation|PASS — Present, 10.10.2026|
|P-21|T-01/T-09|S-03 / ISS-009 / from-All / C-19|On click|Navigate to|S-02-A / after-create|All 9 rows, including ISS-009|Prepared state simulation|PASS — Present, 10.10.2026|
|P-22|T-01|M-01 / valid-from-Important / C-07|On click|Navigate to|S-03 / ISS-009 / from-Important|Same ISS-009 defaults; prior tab Important|Prepared state simulation|PASS — Present, 10.10.2026|
|P-23|T-01/T-09|S-03 / ISS-009 / from-Important / C-19|On click|Navigate to|S-02-B / baseline|ISS-009 excluded: Not Set; Important still 4 rows|Prepared state simulation|PASS — Present, 10.10.2026|
|P-24|T-01|M-01 / valid-from-Empty / C-07|On click|Navigate to|S-03 / ISS-009 / from-Empty|Prepared ISS-009; prior All zero fixture|Prepared state simulation|PASS — Present, 10.10.2026|
|P-25|T-01/T-09|S-03 / ISS-009 / from-Empty / C-19|On click|Navigate to|S-02-A / one-issue|Only ISS-009; collection has 1 record|Prepared state simulation|PASS — Present, 10.10.2026|
|P-26|T-02|M-01 / missing-title-before-submit / C-07|On click|Swap overlay|M-01 / missing-title-validation|Title is required; no new issue|Prepared overlay validation, no live text parsing|PASS — Present, 10.10.2026|
|P-27|T-02|M-01 / missing-description-before-submit / C-07|On click|Swap overlay|M-01 / missing-description-validation|Description is required; no new issue|Prepared overlay validation, no live text parsing|PASS — Present, 10.10.2026|
|P-28|T-02|M-01 / default / C-07|On click|Swap overlay|M-01 / both-missing-validation|Both field errors; no new issue|Prepared overlay validation, no live text parsing|PASS — Present, 10.10.2026|
|P-29|T-03|S-03 / ISS-005 / chosen-Member-A / C-13|On click|Navigate to|S-03 / ISS-005 / assigned-Member-A|One assignee Member A|Prepared state simulation|PASS — Present, prepared simulation, 10.10.2026|
|P-30|T-03|S-03 / ISS-005 / chosen-Member-B / C-13|On click|Navigate to|S-03 / ISS-005 / assigned-Member-B|One assignee Member B; previous assignee replaced|Prepared state simulation|PASS — Present, prepared simulation, 10.10.2026|
|P-31|T-04|S-03 / ISS-006 / chosen-Low / C-14|On click|Navigate to|S-03 / ISS-006 / priority-Low|Priority Low; Not Set not an option|Prepared state simulation|PASS — Present, prepared simulation, 10.10.2026|
|P-32|T-04|S-03 / ISS-006 / chosen-Normal / C-14|On click|Navigate to|S-03 / ISS-006 / priority-Normal|Priority Normal; Not Set not an option|Prepared state simulation|PASS — Present, prepared simulation, 10.10.2026|
|P-33|T-04|S-03 / ISS-006 / chosen-High / C-14|On click|Navigate to|S-03 / ISS-006 / priority-High|Priority High; Not Set not an option|Prepared state simulation|PASS — Present, prepared simulation, 10.10.2026|
|P-34|T-04|S-03 / ISS-006 / chosen-Critical / C-14|On click|Navigate to|S-03 / ISS-006 / priority-Critical|Priority Critical; Not Set not an option|Prepared state simulation|PASS — Present, prepared simulation, 10.10.2026|
|P-35|T-05|S-03 / ISS-001 / Open chosen-In Progress / C-15|On click|Navigate to|S-03 / ISS-001 / In Progress|Same issue now In Progress; allowed transition|Prepared state simulation|PASS — Present, prepared simulation, 10.10.2026|
|P-36|T-05|S-03 / ISS-002 / In Progress chosen-Resolved / C-15|On click|Navigate to|S-03 / ISS-002 / Resolved|Same issue now Resolved; allowed transition|Prepared state simulation|PASS — Present, prepared simulation, 10.10.2026|
|P-37|T-05|S-03 / ISS-003 / Resolved chosen-In Progress / C-15|On click|Navigate to|S-03 / ISS-003 / In Progress|Same issue now In Progress; allowed transition|Prepared state simulation|PASS — Present, prepared simulation, 10.10.2026|
|P-38|T-05|S-03 / ISS-003 / Resolved chosen-Closed / C-15|On click|Navigate to|S-03 / ISS-003 / Closed / from-Important|Same issue now Closed; allowed transition|Prepared state simulation|PASS — Present, prepared simulation, 10.10.2026|
|P-39|T-05/T-08|S-03 / ISS-003 / Closed / from-Important / C-19|On click|Navigate to|S-02-B / after-close-003|001/002/007 only; no ISS-003|Prepared state simulation|PASS — Present, prepared simulation, 10.10.2026|
|P-40|T-05/T-09|S-02-B / after-close-003 / C-01|On click|Navigate to|S-02-A / after-close-003|All 8 records; ISS-003 Closed/High/Member A|Prepared state simulation|PASS — Present, prepared simulation, 10.10.2026|
|P-41|T-05/T-09|S-02-A / after-close-003 / Title ISS-003|On click|Navigate to|S-03 / ISS-003 / Closed / from-All|Reopen shows Closed; prepared next-view result|Prepared state simulation|PASS — Present, prepared simulation, 10.10.2026|
|P-42|T-07|S-03 / comment-empty / C-17|On click|Navigate to|S-03 / comment-validation|Comment text is required; baseline entry only|Prepared state simulation|PASS — Present, prepared simulation, 10.10.2026|
|P-43|T-07|S-03 / comment-filled-success / C-17|On click|Navigate to|S-03 / comment-saved|2 entries: baseline + Member A text/time|Prepared state simulation|PASS — Present, prepared simulation, 10.10.2026|
|P-44|T-07|S-03 / comment-filled-failure / C-17|On click|Navigate to|S-03 / comment-save-error|Comment could not be saved; baseline only|Prepared state simulation|PASS — Present, prepared simulation, 10.10.2026|

## T-01–T-10: рівні доказів

- T-01 Create: PASS (prepared prototype), успіх із All/Important/Empty; значення нової заявки і повернення перевірені.
- T-02 required fields: PASS (prepared prototype), Title/Description/both missing, відповідні errors, без нового issue.
- T-03 assignment: PASS (prepared prototype), P-29/P-30: Apply відкриває assigned-Member-A/B; рівно один assignee, попередній замінений. Меню і рольові обмеження оглянуті окремо.
- T-04 priority: PASS (prepared prototype), P-31–P-34: Apply показує Low/Normal/High/Critical для тієї самої ISS-006; меню без Not Set/reset.
- T-05 statuses: PASS (prepared prototype), P-35–P-41: чотири дозволені переходи, Return після Closed, All та повторне відкриття ISS-003 зі статусом Closed. Closed не має переходів.
- T-06 Lead non-assignee: PASS (prepared prototype), Status/Apply disabled і кліки не змінюють Resolved.
- T-07 comments: PASS (prepared prototype), P-42–P-44: Add Comment показує validation/success/save-error; entries 1/2/1, автор і час; після success input порожній, після failure draft збережений.
- T-08 Important: PASS (prepared prototype): baseline 001/002/003/007; після Closed 003 — лише 001/002/007. У All лишається 8 записів, 003 має Closed/High/Member A.
- T-09 navigation: Return для ISS-003 з обох tabs, Cancel A/B/C та три Create returns PASS; повний title-by-title baseline retest не заявлено.
- T-10 scope/native: canonical surfaces і потрібні reference examples оглянуто; representative text edit/Undo та instance/main link перевірено. Повний незалежний підрахунок усіх instances не виконано.

## Мінітест з одногрупником і незалежний контроль

Учасник: Кирило (Кириченко К. В.). За повідомленням Корякіна З. П. від 10.10.2026, сценарії розглядали спільно під час виконання роботи. Затруднень у Кирила не було. Формат — спільний перегляд; незалежне проходження без підказок не підтверджено.

Нижче наведено результати контрольного проходження у Present від 10.10.2026; спосіб перевірки описано у 09:

1. **Створення — PASS (prepared UI).** S-02-A / All, node 12:2965 → Create Issue → M-01 → Title → Description → Create → ISS-009, node 18:798 → Return → All / after-create, node 18:985. Кліки в поля підставили «Помилка збереження налаштувань» і підготовлений опис. Картка показала Open / Not Set / Unassigned, Member A, 10.10.2026 10:20; список після повернення містив дев'ять заявок.
2. **Важлива Resolved-заявка — PASS (prepared UI).** Незалежний старт All → Important, node 12:3031: ISS-001/002/003/007. ISS-003 має Resolved / High, ISS-007 — Resolved / Critical. Title ISS-003 відкрив відповідну картку, node 12:3103.
3. **Заборонена зміна status — PASS (prepared UI).** У контексті Lead для ISS-003 assignee = Member A. Status та його Apply сірі/disabled; фактичні кліки не відкрили вибір і не змінили Resolved. Пояснення за контрактом: змінювати status може тільки поточний assignee; роль Lead сама по собі не дає цього права.

У трьох контрольних сценаріях нових дефектів не виявлено. Результати підтверджують відтворюваність підготовлених маршрутів; спостереження спільного проходження наведено окремо нижче. Довільне введення, backend та збереження даних поза межами цього проходження.

## Межі прототипу

All відкриває порожню форму. Клік у Title або Description підставляє фіксований текст через Swap overlay; порожній Create показує required errors. Important/Empty відкривають підготовлені заповнені форми. After-create та one-issue містять Title connections; не всі додаткові tabs/Create у цих копіях підключені. Повторне накопичення заявок, live input, авторизація та persistence не моделюються.

Розширені Apply/status/comment connections P-29–P-44 налаштовані й перевірені у Present. Кліки переходять між prepared frames; це демонстрація UI-поведінки без серверного збереження. Меню та права також представлені у REF-01.

## Спостереження спільного проходження з Кирилом

Учасник: Кириченко К. В. Оператор: Корякін З. П. Версія: P1 expanded routes — 10.10.2026. Джерело спостережень: повідомлення Корякіна З. П. від 10.10.2026. Роботу й перегляд сценаріїв виконували разом; затруднень у Кирила не було. Нижче наведено маршрути підтверджених сценаріїв прототипу; окремий хронометраж і дослівні репліки не фіксувалися.

|Завдання|Маршрут сценарію|Вагання та незрозумілі написи|Результат|
|---|---|---|---|
|Створити заявку|All Issues → Create Issue → Title/Description → Create → ISS-009 → Return to Issues List|За повідомленням оператора, затруднень не було; незрозумілі написи не повідомлені|Результат Open / Not Set / Unassigned і повернення до списку прийняті учасником|
|Знайти важливу Resolved-заявку|All Issues → Important Issues → ISS-003 → Issue Details|За повідомленням оператора, затруднень не було; незрозумілі написи не повідомлені|ISS-003 з High/Resolved входить до Important; результат прийнятий|
|Перевірити недоступний Status для Lead non-assignee|Important Issues → ISS-003 → disabled Status/Apply; assignee Member A|За повідомленням оператора, затруднень не було; незрозумілі написи не повідомлені|Зміна status недоступна; результат відповідає праву лише поточного assignee|

Висновок: під час спільного перегляду Кирило не мав затруднень і прийняв результати трьох сценаріїв. Це спостереження конкретного спільного перегляду; незалежний мінітест без підказок за M с.22 залишається непідтвердженим.

## Розширене проходження — 10.10.2026

Метод: клік саме по Apply, Return, All, Title та Add Comment у Present, зі звіркою кінцевого кадру й видимого результату. P-29/P-30: 18:1178 → 18:1234 і 18:1290 → 18:1346. P-31–P-34: 18:1403 → 18:1459; 18:1515 → 18:1571; 18:1627 → 18:1683; 18:1739 → 18:1795. P-35–P-38: 18:1852 → 18:1917; 18:1981 → 18:2046; 18:2110 → 18:2175; 18:2239 → 18:2304. P-39–P-41: 18:2304 → 18:2494 → 18:2554 → 18:2367. P-42–P-44: 18:2669 → 18:2733; 18:2801 → 18:2865; 18:2932 → 18:2996. Результат: 16/16 PASS (prepared simulation).

Share збережено як **Anyone can view**. Перегляд за посиланням відкритий; фактичне відкриття викладачем не засвідчується.

## Підсумковий відгук Кириченка К. В.

Результати трьох контрольних сценаріїв і переходів P-29–P-44 приймаю. Створення показує Open / Not Set / Unassigned; Important містить High/Critical, крім Closed; Lead non-assignee не може змінити status. Розширені Apply та Add Comment відповідають описаним підготовленим результатам.

Підтвердження прийняття передано Корякіним З. П. 10.10.2026. Детальні спостереження мінітесту наведено в окремому розділі.
