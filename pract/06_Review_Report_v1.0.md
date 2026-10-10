# Review Report v1.1 — підсумкова редакція

Учасники: Корякін З. П.; Кириченко К. В.; ПЗПІ-23-8. Перевірка: 10.10.2026. Версія Figma: **P1 expanded routes — 10.10.2026**, page UX/UI v1.0. [Figma](https://www.figma.com/design/WR2MU9NL1NdQj6LQJYAB7N); [Prototype і test record](07_Prototype_P1.md).

## Джерела й метод

S1: SD_Spec.docx.pdf, 13 сторінок, §1/3/5/8. M: методичні рекомендації, 29 сторінок, с.7–18/20–28. Обидва оригінали повторно прочитано. Документальна traceability: 8 включених US, 33 AC; excluded US-09, future SR-10/SR-11.

Початковий статичний огляд семи наданих JPG дав 21 PASS (UI), 12 PARTIAL, 0 FAIL. Актуальне джерело макета — Figma. Нижче збережено датовані результати цього огляду, а подальші native/Present перевірки наведено окремо. Різниця UI/PARTIAL відображає межі доказу функціональних вимог, а не кількість UI-дефектів.

## Контроль C

Оператор: Корякін З. П. Version: 05, поточна редакція. Документальна звірка: VERIFIED. Дата підтвердження: 10.10.2026. Accepted: фінальний brief; Rejected: немає. Контроль C: APPROVED за підтвердженням Корякіна З. П.

Brief самодостатній, UTF-8 Markdown, містить всі source fields, sample data, permissions, transitions, errors, exclusions і navigation intent. D-01–D-08 відокремлено від S1. Документальну перевірку виконано 10.10.2026; журнал — 09.

## Part A — усі 33 AC

|Source|Expected|Screen/state|Observed evidence|Result|Remaining test|
|---|---|---|---|---|---|
|AC-01.1|Користувач може ввести: Title; Description.|M-01 і REF-01/Create|Title та multiline Description; editable-looking fields; лише два input labels.|PASS (UI)|Перевірити native editability у Figma; T-01.|
|AC-01.2|Title є обов'язковим.|M-01 і REF-01/Create missing-title|Title *; Title is required; empty Title і заповнений Description; both-missing теж є.|PASS (UI)|T-02: invalid submit не навігує в success.|
|AC-01.3|Description є обов'язковим.|M-01 і REF-01/Create missing-description|Description *; Description is required; empty Description; both-missing теж є.|PASS (UI)|T-02: invalid submit не навігує в success.|
|AC-01.4|Після створення заявка отримує: ID; status = Open; created_at; author.|REF-01/Create prepared ISS-009|ISS-009; Open; Member A; 10.10.2026 10:20; поля пояснені як automatic/prepared.|PARTIAL|T-01 prepared navigation; IMPL unique ID/current author/time generation.|
|AC-01.5|Після створення issue його priority не встановлено.|REF-01/Create prepared ISS-009|Priority: Not Set; не Normal; Unassigned окремо.|PASS (UI)|T-01 prepared result; IMPL actual creation.|
|AC-02.1|Авторизований член команди може переглянути список зареєстрованих issues.|S-02-A; S-01|8 rows видимі; S-01 neutral authentication boundary, форма login відсутня.|PARTIAL|T-09 navigation; IMPL authentication не доведено.|
|AC-02.2|Для кожного issue у списку відображаються щонайменше: ID; Title; Status; Priority; Assignee, якщо він призначений.|S-02-A/B|Кожний row має ID/Title/Status/Priority/Assignee; Unassigned показано у 005/006.|PASS (UI)|T-08/09; звірити Figma layers.|
|AC-02.3|Користувач може вибрати issue зі списку та відкрити сторінку його деталей.|S-02-A/B; S-03|Titles підкреслено; S-03 показує той самий ISS-003. Це intent, не пройдений connection.|PARTIAL|T-09 Present: Title -> details.|
|AC-02.4|На сторінці issue відображаються: ID; Title; Description; Status; Priority; Assignee, якщо він призначений; Author; Created at.|S-03|ISS-003; повні Title/Description; Resolved; High; Member A; Member B; 10.10.2026 09:20.|PASS (UI)|T-09 details інших ID і same fixture.|
|AC-02.5|Якщо зареєстрованих issues немає, система відображає порожній список або повідомлення про відсутність issues.|S-02-C|All active; No issues yet; 0 rows; Create Issue доступний.|PASS (UI)|T-09 empty fixture і Cancel.|
|US-03, AC, пункт 1|можна вибрати одного assignee;|S-03; REF-01/permissions/choices|Single-value Assignee control; Member A, Member B, Lead перелічені окремо; вибір не відкрито.|PARTIAL|T-03 відкрити options; single assign/reassign -> Apply.|
|US-03, AC, пункт 2|assignee повинен бути членом команди;|REF-01/choices|Склад команди показано як Member A, Member B, Lead; інших assignee names немає.|PARTIAL|T-03 actual options; IMPL membership validation.|
|US-03, AC, пункт 3|призначати заявку може лише Team Lead;|REF-01/4 contexts; S-03|Member controls сірі/disabled; Lead controls enabled; current assignee не дає Member assignment right.|PASS (UI)|T-03 no denied hotspot; IMPL server authorization.|
|US-03, AC, пункт 4|поточний assignee відображається у заявці.|S-03; S-02-A/B|Поточний assignee ISS-003 = Member A однаковий у details і lists.|PASS (UI)|T-03 after-Apply state.|
|AC-04.1|Допустимі значення встановленого Priority: Low, Normal, High, Critical;|REF-01/choices; S-03|Low, Normal, High, Critical перелічені; Not Set пояснено absence. Реальний dropdown закритий.|PARTIAL|T-04 actual dropdown exactly four levels, no reset.|
|AC-04.2|Встановлювати та змінювати priority може лише Team Lead.|REF-01/4 contexts; S-03|Priority disabled для Member, enabled для Lead; adjacent Apply.|PASS (UI)|T-04 actual role options/hotspot; IMPL server rights.|
|AC-05.1|Поточний status відображається для кожного issue.|S-02-A/B; S-03; REF-01 fixture|Усі 8 rows мають status; details current Resolved і reference examples.|PASS (UI)|T-05/09 after-change consistency.|
|AC-05.2|Status відображається на сторінці issue.|S-03|Status Resolved показано читабельно, control grey/disabled для canonical context.|PASS (UI)|T-05 prepared result.|
|AC-05.3|Status відображається у списку issues.|S-02-A/B|Status column показано; values збігаються з еталоном.|PASS (UI)|T-08 after-close list state.|
|AC-06.1|Comment text cannot be empty.|REF-01/comments validation|Empty Comment; Comment text is required; лише baseline saved entry.|PASS (UI)|T-07 Present invalid branch; IMPL validation.|
|AC-06.2|Added comment is stored and shown for the issue.|REF-01/comments success|Два saved entries: baseline плюс новий text; збереження не доведено.|PARTIAL|T-07 success branch; IMPL persistence.|
|AC-06.3|Comment author is stored and displayed.|S-03; REF-01/comments success|Baseline Member B; новий entry Member A; labels читабельні.|PARTIAL|IMPL stored author association; T-07.|
|AC-06.4|Creation date/time is stored and displayed.|S-03; REF-01/comments success|Baseline 10.10.2026 10:15; новий 10.10.2026 10:25; labels читабельні.|PARTIAL|IMPL stored creation time; T-07.|
|AC-06.5|Failed save does not create a comment and produces an error.|REF-01/comments save failure|Comment could not be saved; тільки 1 baseline entry; submitted text лишається в input.|PASS (UI)|T-07 failure branch; IMPL atomic save failure.|
|AC-07.1|Нова заявка створюється зі статусом Open.|REF-01/Create prepared ISS-009|Prepared new issue status = Open.|PASS (UI)|T-01 Present; IMPL actual initial status.|
|AC-07.2|Допустимі статуси: Open, In Progress, Resolved, Closed.|S-02-A; REF-01/status matrix|У fixture/matrix є лише Open, In Progress, Resolved, Closed. Actual destination menus не відкриті.|PARTIAL|T-05 allowed options і current value не destination.|
|AC-07.3|Після зміни статусу система зберігає нове значення та відображає його при наступному перегляді заявки.|REF-01/prepared change ISS-003|After-change ISS-003 Closed/High/Member A; same identity; return/reopen не виконано.|PARTIAL|T-05/T-09 prepared next view; IMPL save/retrieval.|
|AC-07.4|Користувач, який не є виконавцем заявки, не може змінити її статус.|S-03; REF-01/4 contexts|Lead non-assignee Status/Apply disabled; Member non-assignee теж disabled; assignee contexts enabled.|PASS (UI)|T-06 no denied hotspot; IMPL server authorization.|
|AC-07.5|Система не дозволяє встановити значення статусу, якого немає у визначеному переліку.|REF-01/matrix/choices|Невідомих statuses немає у matrix; це не доказ actual dropdown чи server rejection.|PARTIAL|T-05 actual menus; IMPL unknown status rejection.|
|AC-08.1|Заявка з priority = High і статусом, відмінним від Closed, відображається у списку Important Issues.|S-02-B|ISS-002 In Progress/High та ISS-003 Resolved/High присутні; values як в All.|PASS (UI)|T-08 navigation/filter simulation; IMPL query.|
|AC-08.2|Заявка з priority = Critical і статусом, відмінним від Closed, відображається у списку Important Issues.|S-02-B|ISS-001 Open/Critical та ISS-007 Resolved/Critical присутні.|PASS (UI)|T-08; IMPL query.|
|AC-08.3|Заявки з priority = Low або Normal не відображаються у списку Important Issues.|S-02-A/B|ISS-005 Normal та ISS-008 Low є в All і відсутні в Important; ISS-006 Not Set також excluded за predicate.|PASS (UI)|T-08 actual tab connection.|
|AC-08.4|Заявки зі status = Closed не відображаються незалежно від priority.|S-02-A/B|ISS-004 Closed/Critical є в All і відсутня в Important. REF after-close також виключає 003.|PASS (UI)|T-08 prepared after-close navigation.|


**Підсумок: 21 PASS (UI), 12 PARTIAL, 0 FAIL.** Усі 33 criteria мають видимий UI-доказ відповідної статичної частини; functional/backend частини не підтверджено. Це не твердження «всі AC виконано».

## Повторний огляд native Figma

- На одній сторінці присутні S-01, S-02-A/B/C, M-01, S-03; REF-01 окремо від продукту. Section P1 states містить додаткові демонстраційні копії.
- F1 response повідомляє 14 local component definitions і 113 instances; P1-STATES response — 51 full frames, 6 menus та 432 instances. Загальні числа reported, а не незалежний повний підрахунок. Representative instance → main component та редагування тексту → Undo перевірені.
- Повторно оглянуто всі шість menus: Assignee = Member A/Member B/Lead; Priority = Low/Normal/High/Critical; Status Open → In Progress, In Progress → Resolved, Resolved → In Progress/Closed; Closed → no available transitions.
- Повторно оглянуто Member non-assignee ISS-003, Member assignee chosen-In Progress ISS-001, Lead assignee ISS-007 та Closed ISS-003. Lead non-assignee canonical ISS-003 раніше перевірено у Present. Вигаданої ролі Reviewer або role switcher немає у цих surfaces.
- Comment validation/saved/save-error: entries 1/2/1; success input очищено, new Member A entry 10:25; failure input збережено, нового entry немає.
- assigned-Member-B ISS-005 має одного assignee; after-close Important містить 001/002/007 і виключає Closed 003.
- У Present прочитано 18 стартів: Flow 1–17 і P1 — Zero issues; пояснення та прямі посилання у 07.

## UX і дефекти

У перевірених поверхнях нових доказових UI-дефектів не виявлено. F2 correction не запускалась; додаткові тестові стани розширюють демонстраційне покриття. Статичні приклади читабельні на відповідному масштабі; матриці й actor annotations розміщено поза product frames. Це не accessibility certification і не доказ універсальної usability.

## Контроль D — рекомендації та особисте рішення

Дата: 10.10.2026. Версія: **P1 expanded routes — 10.10.2026**. Рекомендація аудиту: **ACCEPT WITH LIMITS** для базового навчального UI-макета. Рішення Кириченка К. В. — **ACCEPT WITH LIMITS**; підтвердження передано Корякіним З. П. 10.10.2026. Підстава — звірка вимог, огляд редагованих елементів Figma та протокол Present. Спосіб проведення перевірки записано у 09.

Зауваження EVID-01–04 прийняті Кириченком К. В.; підстави:

- **EVID-01 — ACCEPTED; базовий доказ отримано.** Native text edit → Undo та representative instance → main component перевірені. Початкова відсутність native evidence усунена для цих перевірок. Повний незалежний підрахунок усіх компонентів/instances не заявлено.
- **EVID-02 — ACCEPTED; базові й розширені маршрути підтверджено.** У 07 є 37 PASS для prepared UI, включно з P-29–P-44, та повтор трьох контрольних сценаріїв. Apply/status/comments пройдено у Present. Методичка с.18 допускає показ прав/статусів через REF-01 і prepared examples.
- **EVID-03 — ACCEPTED; оформлено підсумкове рішення.** Робоча версія названа, Figma/Present links наведено, рішення й обмеження записано. Share збережено як Anyone can view.
- **EVID-04 — ACCEPTED; відповідь Figma Agent записано в 09.** Відомості про frames/components відокремлено від незалежних перевірок. У журналі зазначено GPT-6 ASTRA / High для текстової частини; модель Figma Agent, тарифний план і кредити не зафіксовані.
- **Нові UX-дефекти — відсутні у перевірених сценаріях.** F2-виправлення не призначається без доказового дефекту. Спільне проходження з Кирилом описано у 07: за повідомленням оператора, затруднень не було. Незалежний формат без підказок не підтверджено.

Висновок: базовий навчальний макет рекомендовано прийняти у межах наявних UI-доказів і prepared simulation. Загальне виконання всіх функціональних AC, usability, backend та всього DoD не заявляється. Додано й перевірено 16 розширених connections; збережено версію P1 expanded routes — 10.10.2026. Залишок для здавання: незалежний мінітест без підказок, передання комплекту та захист; організаційні умови здавання перевіряються окремо.

## Підсумок готовності

- **Вимоги й дизайн: COMPLETE COVERAGE.** Усі 33 AC мають місце в Traceability та видимі приклади UI-частини. Таблиця Part A зберігає результат первинного статичного огляду: 21 PASS (UI), 12 PARTIAL, 0 FAIL. PARTIAL у ній стосується непідтвердженої функціональної частини; межі реалізації наведено окремо.
- **Базовий прототип: VERIFIED у межах prepared simulation.** Маршрути Present описано у 07. P-29–P-44 — 16/16 PASS у Present: assignment, priority, status, after-close navigation, comments. Загалом 37/44 PASS; сім базових Title connections мають CONFIGURED, їхні detail/Back перевірено зі списку after-create.
- **Реалізація: OUT OF DESIGN SCOPE.** Authentication, server authorization, actual input validation, unique ID/time generation, persistence, atomic failed save, <1 s, HTTPS та backup/restore потребують реалізації; не є підставою вимагати backend у low-fi макеті.
- **Погодження рецензента: CONFIRMED.** Кириченко К. В. прийняв поточний план, D-01–D-08, EVID-01–04 і результати прототипу; підтвердження передано Корякіним З. П. 10.10.2026. Корякін З. П. підтвердив контроль A/C; спільне проходження з Кирилом описано у 07; незалежний мінітест без підказок не підтверджено.
- **Доступ: CONFIGURED.** Share збережено як Anyone can view; Kyrylo — can view. Зовнішній перегляд за посиланням відкритий. Особисте відкриття викладачем не перевірялося.

**Загальний DoD дизайну: PARTIAL за процедурними умовами** — потрібен незалежний мінітест без підказок; backend поза обсягом.

## Поля особистого контролю D

Reviewer: Кириченко К. В. Version: P1 expanded routes — 10.10.2026. Date запису підтвердження: 10.10.2026. Accepted: EVID-01–04; Rejected: немає. Рішення: ACCEPT WITH LIMITS. Підтвердження передано Корякіним З. П.; рішення другого учасника у цьому записі не засвідчується.

## Актуалізація Prototype — 10.10.2026

Після первинного статичного огляду виконано розширене проходження P-29–P-44: 16/16 PASS (prepared simulation), докази та node IDs — у 07. Assignment і чотири priority values показано після Apply; усі чотири дозволені зміни status і повторний перегляд Closed підтверджено. Add Comment має три різні результати: порожній текст → error, успіх → другий entry та очищений input, failure → error без нового entry зі збереженим draft.

Таблиця Part A вище зберігає первинний результат, а цей розділ фіксує новий доказ. PARTIAL функціональних вимог про автентифікацію, membership і stored data не змінено на повне PASS: UI-прототип не виконує серверної реалізації. Видимі частини всіх 33 AC представлені, інтерактивні перевірки розширено.

## Висновок Кириченка К. В.

Результати перевірки макета й прототипу приймаю. Погоджую розмежування прав Lead/assignee, чотири значення priority, дозволені переходи status, виключення Closed з Important та три результати Add Comment. Приймаю EVID-01–04. Макет приймаю як навчальний UX/UI-прототип із підготовленими станами; серверна реалізація не входить до цієї оцінки.

Дата запису підтвердження: 10.10.2026. Підстава: підтвердження рецензента, передане Корякіним З. П.

## Підсумкова перевірка UI-релевантних BR і D-рішень

Джерело правил і Traceability — 03; фактичні маршрути та state evidence — 07. PASS (UI/SIM) стосується видимого макета або підготовленої симуляції; серверні перевірки лишаються окремими.

|Source|Expected|Screen/state|Observed evidence|Result|Remaining test / межа|
|---|---|---|---|---|---|
|BR-01|Доступ лише authenticated team members|S-01 boundary; три fixture users|UI boundary представлена; authentication не реалізовано|PARTIAL|T-09; IMPL authentication|
|BR-02|Будь-який член команди створює issue|S-02-A/B/C → M-01|Create/Cancel і prepared success пройдені|PASS (UI/SIM)|T-01/T-09; IMPL rights|
|BR-03|Нова issue Open|S-03 / ISS-009|Після Create показано Open|PASS (UI/SIM)|T-01|
|BR-04|Нова issue без priority|S-03 / ISS-009|Після Create Not Set|PASS (UI/SIM)|T-01|
|BR-05|Priority лише Low/Normal/High/Critical|Menu / Priority; ISS-006 results|Чотири options і P-31–P-34 відповідають переліку|PASS (UI/SIM)|T-04; IMPL validation|
|BR-06|Priority змінює лише Lead|REF-01 contexts; S-03|Member disabled, Lead enabled; Apply results перевірені|PASS (UI/SIM)|T-04; IMPL authorization|
|BR-07|Чотири допустимі status|REF-01; status menus/results|Open/In Progress/Resolved/Closed представлені|PASS (UI)|T-05; IMPL validation|
|BR-08|Status змінює поточний assignee|REF-01 contexts; canonical ISS-003|Lead non-assignee disabled; assignee Apply routes пройдені|PASS (UI/SIM)|T-05/T-06; IMPL authorization|
|BR-08.1|Чотири дозволені directed transitions|REF-01 matrix; P-35–P-38|Усі чотири Apply routes пройдені; Closed без destinations|PASS (UI/SIM)|T-05; IMPL enforcement|
|BR-09|Important за High/Critical|S-02-B / baseline|001/002/003/007, без Low/Normal/Not Set|PASS (UI/SIM)|T-08; IMPL query|
|BR-09.1|Resolved залишається active до Closed|S-02-B baseline / after-close|003/007 Resolved включені; після Closed 003 виключено|PASS (UI/SIM)|T-05/T-08|
|BR-10|Issues не видаляються|Product frames|Delete control відсутній|PASS (UI)|T-10; IMPL deletion policy|
|BR-11|Немає користувацької історії змін|Product frames|History surface/control відсутні|PASS (UI)|T-10|
|D-01|Desktop grayscale; tabs; modal|S-02/M-01|Low-fi native frames; tabs і overlay пройдені|PASS (UI/SIM)|T-01/T-08/T-10|
|D-02|Нейтральна authentication boundary|S-01; Flow 1|Механізм TBD; старт на authenticated list|PASS (UI)|T-09|
|D-03|Not Set як absence, без reset|S-03; priority menu|Лише чотири встановлювані рівні; reset відсутній|PASS (UI)|T-04|
|D-04|Новий Unassigned; reassign одного|ISS-009; P-29/P-30|Unassigned після Create; один Member A/B після Apply|PASS (UI/SIM)|T-01/T-03|
|D-05|Заборонені controls disabled|REF-01; canonical ISS-003|Рольові examples оглянуті; non-assignee Status не реагує|PASS (UI/SIM)|T-03/T-04/T-06|
|D-06|Вибір → adjacent Apply|P-29–P-38|Assignment/priority/status results відкрито через Apply|PASS (UI/SIM)|T-03/T-04/T-05|
|D-07|Return зберігає calling tab|S-03 Return; All/Important|Обидва Return routes відновили відповідний list state|PASS (SIM)|T-09|
|D-08|Фіктивні дані й prepared outcomes|P1 states; протокол 07|Фіксовані fields/results; межі input/backend явно описані|PASS (SIM scope)|T-01–T-10|
