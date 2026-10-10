# 02 Screen Map v1.1 — G2

Design basis: D-01–D-08 з M с.7, застосовані в макеті; APPROVED у журналі 00. Джерела: S1 §1/3/5/8; M с.8–9. Метод перевірки описано у журналі 09.

## Screen Inventory

Чотири продуктові поверхні: S-01, S-02, M-01, S-03. S-02-A/B/C — три стани одного списку. REF-01 — службова Section за межами продуктового UI. Базова збірка: **6 canonical frames** (S-01, S-02-A, S-02-B, S-02-C, M-01, S-03) + 1 службова Section REF-01. Overlay frame не є самостійною сторінкою. Кількість compact state examples і копій станів для P1 може збільшити кількість Figma frames, але не кількість продуктових поверхонь.

## S-01 — Authentication boundary

|Field|Contract|
|---|---|
|ID|S-01|
|Name|Authentication boundary|
|Purpose|Позначити обов’язковість автентифікації без вигаданого механізму.|
|Actors|Неавтентифікований відвідувач; лише boundary.|
|Entry|Зовнішня межа входу до продукту.|
|Visible Data|Mini Issue Tracker; Authentication entry — mechanism TBD.|
|Inputs|Немає.|
|Actions|Немає робочої login-дії.|
|Conditions|До MVP допускається лише authenticated user; ця surface не виконує перевірку.|
|Errors|Не моделювати password/SSO errors.|
|Exit|Демонстрація окремо стартує на S-02, не через фіктивний login.|
|Source|S1 BR-01; NFR-02; D-02/08|


## S-02-A — All Issues

|Field|Contract|
|---|---|
|ID|S-02-A|
|Name|All Issues|
|Purpose|Показати всі зареєстровані issues.|
|Actors|Authenticated Member або Lead.|
|Entry|Початок demo; All tab; Return із деталей, відкритих з All.|
|Visible Data|8 issue rows: ID, Title, Status, Priority, Assignee; header; All/Important tabs.|
|Inputs|Немає текстових inputs.|
|Actions|Create Issue; Important tab; issue Title.|
|Conditions|All active; незалежно від статусу і priority показано всі 8 записів.|
|Errors|Не є error state; для zero records використовувати S-02-C.|
|Exit|M-01; S-02-B; S-03 потрібного ID.|
|Source|S1 AC-02.1/2/3; AC-05.1/3; D-01/07|


## S-02-B — Important Issues

|Field|Contract|
|---|---|
|ID|S-02-B|
|Name|Important Issues|
|Purpose|Показати High/Critical non-Closed із тієї самої колекції.|
|Actors|Authenticated Member або Lead.|
|Entry|Important tab; Return із деталей, відкритих з Important.|
|Visible Data|ISS-001, ISS-002, ISS-003, ISS-007; ті самі поля, що в All; Important active.|
|Inputs|Немає.|
|Actions|All tab; Create Issue; issue Title.|
|Conditions|(priority in {High,Critical}) AND (status != Closed); Resolved включено.|
|Errors|Empty Important не тотожний zero registered issues і не замінює S-02-C.|
|Exit|S-02-A; M-01; S-03; повернення відновлює Important.|
|Source|S1 AC-08.1–AC-08.4; BR-09.1; D-01/07|


## S-02-C — Empty All Issues

|Field|Contract|
|---|---|
|ID|S-02-C|
|Name|Empty All Issues|
|Purpose|Показати відсутність будь-яких зареєстрованих issues.|
|Actors|Authenticated Member або Lead.|
|Entry|Окремий dataset zero records; start point test T-09.|
|Visible Data|Issues List; tabs; Create Issue; No issues yet; жодного issue row.|
|Inputs|Немає.|
|Actions|Create Issue; таби того самого списку.|
|Conditions|Zero registered issues; All active.|
|Errors|Це empty state, не failure loading.|
|Exit|M-01; підготовлений Important empty може використовувати той самий компонент.|
|Source|S1 AC-02.5; D-01/08|


## M-01 — Create Issue modal

|Field|Contract|
|---|---|
|ID|M-01|
|Name|Create Issue modal|
|Purpose|Створити issue з двома користувацькими полями.|
|Actors|Authenticated Member або Lead.|
|Entry|Create Issue на будь-якому стані S-02.|
|Visible Data|Modal Create Issue; Title; Description; Create; Cancel; field errors.|
|Inputs|Title required; Description required multiline.|
|Actions|Create; Cancel.|
|Conditions|ID, status, priority, author, created_at та assignee не є editable inputs.|
|Errors|Missing Title: Title is required; missing Description: Description is required; invalid submit створює 0 issues.|
|Exit|Cancel closes overlay до calling list state; valid success -> S-03 new issue.|
|Source|S1 AC-01.1–AC-01.5; US-01 Gherkin; BR-02/03/04; D-01/04/08|


## S-03 — Issue Details

|Field|Contract|
|---|---|
|ID|S-03|
|Name|Issue Details|
|Purpose|Деталі, assignment/priority/status та comments на одній поверхні.|
|Actors|Authenticated Member/Lead; enabled залежить від current assignee.|
|Entry|Issue Title зі списку; результат Create.|
|Visible Data|ID; Title; Description; Status; Priority; Assignee; Author; Created at; saved comments with text/author/time.|
|Inputs|Assignee single team member; Priority four levels; Status valid destinations; Comment text.|
|Actions|Apply біля Assignee; Apply біля Priority; Apply біля Status; Add Comment; Return to Issues List.|
|Conditions|Lead-only assignment/priority; current-assignee-only status; Closed no status destination; Comment доступний усім authenticated.|
|Errors|Comment empty validation; comment-save-error без нового saved entry; compact permission/status examples у REF-01.|
|Exit|Успішні зміни лишаються на S-03; Return restores prior tab.|
|Source|S1 US-02–US-07; BR-05/06/07/08/08.1; D-03–D-08|


## REF-01 — Review notes

|Field|Contract|
|---|---|
|ID|REF-01|
|Name|Review notes|
|Purpose|Службові матриці та компактні state examples для review.|
|Actors|Студенти, розробник і викладач; не користувач продукту.|
|Entry|Огляд canvas поза product frames.|
|Visible Data|4 contexts; 4 status examples; validation/error snippets; Source IDs; actor/issue/status annotations.|
|Inputs|Немає продуктових inputs.|
|Actions|Немає product navigation; examples лише доказові.|
|Conditions|Поза продуктовими frames; не створює роль Reviewer або role switcher.|
|Errors|Містить missing title/description, empty comment, failed save; Closed без destination.|
|Exit|Огляд документа/макета, не новий маршрут застосунку.|
|Source|M с.9–11,25–26; S1 AC-06.1/5; AC-07.4; BR-08.1; D-05/08|


## Таблиця переходів / контрольних сценаріїв

T-ID збережено таким самим, як у тестах методички с.22. T-10 — inspection, а не навігаційна дія користувача. T-05 і T-07 розгортаються на підвипадки без нових продуктових правил.

|T-ID|From|Actor|Trigger|Preconditions|To|Visible Result|Requirement/D-ID|
|---|---|---|---|---|---|---|---|
|T-01|S-02 -> M-01|Member або Lead|Create Issue; заповнити Title/Description; Create|Authenticated; два required поля непорожні|S-03 / new-issue|ISS-009; Open; Not Set; Unassigned; author/time; invalid input не має success|AC-01.1/4/5; AC-07.1; D-01/04/08|
|T-02|M-01 / missing-title; missing-description|Member або Lead|Create на підготовленій неповній формі|Title або Description відсутнє|M-01 / validation|Помилка відповідного поля; жодного нового ID чи success|AC-01.2/3; US-01 Gherkin; D-08|
|T-03|S-03 / assignment-ready|Lead; Member negative example|Assignee -> один team member -> Apply|Lead; один assignee; для Member disabled|S-03 / assignment-result|Поточний assignee оновлено; Member action не відбувається|US-03, AC, пункти 1–4; D-04/05/06|
|T-04|S-03 / priority-ready|Lead; Member negative example|Low/Normal/High/Critical -> Apply|Lead; Not Set є display absence, не option|S-03 / priority-result|Встановлений priority; Member disabled; reset немає|AC-04.1/2; BR-04/05/06; D-03/05/06|
|T-05|S-03 / Open, In Progress, Resolved, Closed|Current assignee|Allowed Status -> Apply|Current user=current assignee; destination за BR-08.1|S-03 / status-result; matching S-02 updated on Return|4 allowed transitions; інших 8 між різними статусами немає; Closed terminal|AC-07.2/3/4/5; BR-08.1; D-06/08|
|T-06|S-03 / Lead viewing ISS-003|Lead non-assignee|Спроба Status/Apply|ISS-003 assigned to Member A|Той самий S-03|Status/Apply disabled, hotspot відсутній; Resolved не змінюється|AC-07.4; BR-08; D-05|
|T-07|S-03 / comment-ready|Member або Lead|Add Comment: empty / prepared success / prepared failure|Authenticated; scenarios розділені, error injection тільки симуляція|S-03 / validation, saved, save-error|Empty -> error; success -> text/author/time; failure -> error без нового entry|AC-06.1–AC-06.5; D-08|
|T-08|S-02-A|Member або Lead|Important tab|Еталонні ISS-001..008 до мутацій|S-02-B|Тільки 001/002/003/007; ті самі values; після закриття 003 -> тільки 001/002/007|AC-08.1–AC-08.4; BR-09.1; D-01/08|
|T-09|S-02-A/B/C; M-01; S-03|Member або Lead|Title -> Details -> Return; Create -> Cancel; Empty start|Попередній tab збережено; zero dataset для C|Попередній S-02; S-02-C для empty test|ID збігається; Return зберігає tab; Cancel не створює; Empty має 0 rows|AC-02.1–AC-02.5; AC-05.1/3; D-07/08|
|T-10|Увесь комплект frames/layers/connections|Кириченко К. В. як рецензент|Огляд усіх поверхонь, controls, Layers та Prototype|Доступний увесь комплект робочої версії|Review verdict поза UI|Відсутні unsupported features; native editable layers; службові notes поза продуктом|S1 §8; BR-10/11; D-01/08; brief exclusions|


## User flows

### Створення заявки

S-02-A/B/C -> Create Issue -> M-01 -> Title і Description -> Create -> S-03 ISS-009 Open/Not Set/Unassigned. Return -> calling tab з актуалізованими prepared rows. Cancel -> calling list без нового issue. T-01/T-09.

### Перегляд заявки

S-02-A або S-02-B -> Title ISS-003 -> S-03 ISS-003 із такими самими Status/Priority/Assignee -> Return -> той самий tab. T-09.

### Призначення лідом

Lead відкриває S-03 ISS-005 Unassigned -> Assignee Member A -> Apply -> S-03 ISS-005 assigned Member A. Повторний вибір Member B -> Apply -> той самий ID assigned Member B. Member бачить disabled controls. T-03.

### Визначення priority

Lead відкриває ISS-006 Not Set -> обирає High -> Apply -> S-03 ISS-006 High. Not Set не є пунктом dropdown. Member бачить disabled. T-04.

### Переведення у Resolved

Member B є assignee ISS-002 In Progress -> Status Resolved -> Apply -> S-03 ISS-002 Resolved -> Return -> відповідний список ISS-002 Resolved/High. T-05.

### Повернення у роботу

Member A є assignee ISS-003 Resolved -> In Progress -> Apply -> S-03 ISS-003 In Progress. Альтернативний перехід Resolved -> Closed дозволений тому самому current assignee. T-05.

### Коментування

Authenticated user -> S-03 -> Comment text -> Add Comment -> prepared saved entry text/author/time. Empty submission -> validation без entry. Save failure branch -> error без нового entry. T-07.

### Неавторизована зміна статусу

Lead non-assignee відкриває ISS-003 assigned Member A -> Status/Apply disabled, hotspot не додається -> жодного переходу. Lead може assignment/priority, але не status цієї заявки. T-06.

### Порожній список

Start point S-02-C із zero dataset -> No issues yet і Create Issue -> M-01; це не empty Important на непорожній колекції. T-09.

### Important і закриття

S-02-A -> Important -> S-02-B із 001/002/003/007 -> ISS-003 Member A -> Closed -> Return -> S-02-B after-close із 001/002/007; у All after-close ISS-003 залишається, Status Closed. T-08/T-05.

## Три заборонені типові функції

1. Пошук і сортування відсутні в погодженому обсязі: пошукове поле та сортування за заголовками таблиці не передбачені.
2. Історія змін не показується в інтерфейсі відповідно до BR-11.
3. Масові операції не передбачені: прапорці вибору рядків і панель групових дій відсутні.

## Питання та coverage

Непокритих AC у плані немає: 33 записи простежуваності — у 03_Screen_Contracts_v1.0.md. Q-01 залишається технічним; D-01–D-08 наведено у Decision Log (00), спосіб перевірки — у журналі 09. Редагований макет і базовий P1 створені; докази та межі перевірки наведено у 06/07.
