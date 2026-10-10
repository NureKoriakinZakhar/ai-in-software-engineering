# 01 Input Pack v1.1 — G1

Учасники: Корякін З. П.; Кириченко К. В. Група: ПЗПІ-23-8. Дата підготовки: 10.10.2026. Статус: SOURCE VERIFIED; контроль A — APPROVED. Редакція: v1.1, 10.10.2026.

## Джерела та типи тверджень

Вихідна специфікація, 13 сторінок, доступні §0–§9; §9 порожній і заповнюється цією роботою. Методичні рекомендації, 29 сторінок. Оригінали збережено без змін. SOURCE — вихідна вимога; DERIVED — логічний висновок; DESIGN — UX-пропозиція навчального варіанта; статус у 00; UNRESOLVED — технічне питання.

## Product purpose — SOURCE

Mini Issue Tracker — внутрішня вебсистема для реєстрації та відстеження проблем невеликої команди розробників. Вона координує відповідальних, пріоритети, поточні статуси й обговорення заявок. Мета — скоротити час від реєстрації проблеми до її призначення та вирішення. [S1 §1–§2]

## Actors і scope

SOURCE: Team Member та Team Lead; усі користувачі — члени однієї команди; у MVP два Member і один Lead. Current assignee — відношення конкретного користувача до конкретної заявки, а не нова роль. Product Owner та System Administrator є secondary stakeholders, без окремих продуктових сценаріїв MVP. [S1 §1, §3 BR-01]

Release MVP: **US-01–US-08** [S1 §8, с.13]. Candidate MVP з §4 не визначає остаточний scope. Deferred: **US-09 Attach files to an issue**, включно з AC-09.1–AC-09.6. Future: **SR-10 Automatic issue categorization; SR-11 Automatic priority recommendation**. BR-12 стосується майбутніх рекомендацій, тому не породжує control у MVP.

SOURCE out of scope: Customer support portal; Billing; Source-code hosting; CI/CD; Time tracking; Full project management; Mobile application; інтеграції GitHub, GitLab, Jira та інших issue trackers [S1 §1 KC-05; §2]. BR-10 забороняє delete; BR-11 виключає окрему історію змін. Design exclusions методичного варіанта: пошук, сортування, pagination, analytics, dashboard, notifications, bulk actions, row-selection, user administration, редагування Title/Description після створення, нові поля, ролі та значення. Це обмеження brief, а не приписування відсутніх AC джерелу.

## Included stories — SOURCE

|US|Actor|Назва|Мета|
|---|---|---|---|
|US-01|Team Member / Team Lead|Create Issue|Створити issue з назвою й описом, щоб проблема була зареєстрована та відстежувалась.|
|US-02|Team Member / Team Lead|View Issues|Переглянути зареєстровані проблеми та їхні поточні деталі.|
|US-03|Team Lead|Assign Issue to the responsible team member|Призначити заявку члену команди, щоб було зрозуміло, хто відповідає за її виконання.|
|US-04|Team Lead|Set Issue Priority|Встановити пріоритет заявки, щоб команда могла визначити порядок роботи.|
|US-05|Team Member / Team Lead|Track Issue Progress|Побачити поточний стан заявки, щоб розуміти прогрес роботи.|
|US-06|Team Member / Team Lead|Add Comment|Додати коментар до заявки для обговорення проблеми.|
|US-07|Current assignee, незалежно від ролі|Update Issue Status|Змінити статус відповідальної заявки, щоб команда бачила поточний стан роботи.|
|US-08|Team Member / Team Lead|View Important Open Issues|Швидко побачити важливі незакриті заявки для зосередження на першочергових проблемах.|


## Повний реєстр 33 AC — SOURCE

Формулювання збережено за змістом і мовою джерела; списки полів розгорнуто в один рядок без втрат. Повний дослівний текст — у вихідному PDF S1. US-03 не має вихідних нумерованих AC; посилання на пункти не є новими AC-ID. Gherkin на с.7–8 ілюструє вже враховані AC, а не додає критерії.

|№|Source ID / пункт|Повний зміст|Source|
|---|---|---|---|
|1|AC-01.1|Користувач може ввести: Title; Description.|S1 §5, с.7|
|2|AC-01.2|Title є обов'язковим.|S1 §5, с.7|
|3|AC-01.3|Description є обов'язковим.|S1 §5, с.7|
|4|AC-01.4|Після створення заявка отримує: ID; status = Open; created_at; author.|S1 §5, с.7|
|5|AC-01.5|Після створення issue його priority не встановлено.|S1 §5, с.7|
|6|AC-02.1|Авторизований член команди може переглянути список зареєстрованих issues.|S1 §5, с.8|
|7|AC-02.2|Для кожного issue у списку відображаються щонайменше: ID; Title; Status; Priority; Assignee, якщо він призначений.|S1 §5, с.8|
|8|AC-02.3|Користувач може вибрати issue зі списку та відкрити сторінку його деталей.|S1 §5, с.8|
|9|AC-02.4|На сторінці issue відображаються: ID; Title; Description; Status; Priority; Assignee, якщо він призначений; Author; Created at.|S1 §5, с.8|
|10|AC-02.5|Якщо зареєстрованих issues немає, система відображає порожній список або повідомлення про відсутність issues.|S1 §5, с.9|
|11|US-03, AC, пункт 1|можна вибрати одного assignee;|S1 §5, с.9|
|12|US-03, AC, пункт 2|assignee повинен бути членом команди;|S1 §5, с.9|
|13|US-03, AC, пункт 3|призначати заявку може лише Team Lead;|S1 §5, с.9|
|14|US-03, AC, пункт 4|поточний assignee відображається у заявці.|S1 §5, с.9|
|15|AC-04.1|Допустимі значення встановленого Priority: Low, Normal, High, Critical;|S1 §5, с.9|
|16|AC-04.2|Встановлювати та змінювати priority може лише Team Lead.|S1 §5, с.9|
|17|AC-05.1|Поточний status відображається для кожного issue.|S1 §5, с.9|
|18|AC-05.2|Status відображається на сторінці issue.|S1 §5, с.9|
|19|AC-05.3|Status відображається у списку issues.|S1 §5, с.10|
|20|AC-06.1|Comment text cannot be empty.|S1 §5, с.10|
|21|AC-06.2|Added comment is stored and shown for the issue.|S1 §5, с.10|
|22|AC-06.3|Comment author is stored and displayed.|S1 §5, с.10|
|23|AC-06.4|Creation date/time is stored and displayed.|S1 §5, с.10|
|24|AC-06.5|Failed save does not create a comment and produces an error.|S1 §5, с.10|
|25|AC-07.1|Нова заявка створюється зі статусом Open.|S1 §5, с.10|
|26|AC-07.2|Допустимі статуси: Open, In Progress, Resolved, Closed.|S1 §5, с.10|
|27|AC-07.3|Після зміни статусу система зберігає нове значення та відображає його при наступному перегляді заявки.|S1 §5, с.10|
|28|AC-07.4|Користувач, який не є виконавцем заявки, не може змінити її статус.|S1 §5, с.10|
|29|AC-07.5|Система не дозволяє встановити значення статусу, якого немає у визначеному переліку.|S1 §5, с.10|
|30|AC-08.1|Заявка з priority = High і статусом, відмінним від Closed, відображається у списку Important Issues.|S1 §5, с.10|
|31|AC-08.2|Заявка з priority = Critical і статусом, відмінним від Closed, відображається у списку Important Issues.|S1 §5, с.11|
|32|AC-08.3|Заявки з priority = Low або Normal не відображаються у списку Important Issues.|S1 §5, с.11|
|33|AC-08.4|Заявки зі status = Closed не відображаються незалежно від priority.|S1 §5, с.11|


## UI-релевантні business rules — SOURCE

|ID|Зміст і межі|Source|
|---|---|---|
|BR-01|Системою можуть користуватися лише автентифіковані члени команди. У першій версії є три заздалегідь визначені користувачі: два Team Member та один Team Lead.|S1 §3, с.4|
|BR-02|Будь-який автентифікований член команди може створити issue.|S1 §3, с.5|
|BR-03|Під час створення нового issue система автоматично встановлює status = Open.|S1 §3, с.5|
|BR-04|Під час створення нового issue його priority не визначений: priority = Not Set.|S1 §3, с.5|
|BR-05|Після встановлення priority: Low, Normal, High, Critical. До встановлення допускається стан Не встановлено (пусте значення).|S1 §3, с.5|
|BR-06|Встановлювати та змінювати priority issue може тільки Team Lead.|S1 §3, с.5|
|BR-07|Status issue: Open, In Progress, Resolved, Closed.|S1 §3, с.5|
|BR-08|Член команди, відповідальний за виконання issue, повинен мати можливість змінювати його status. Заборону для інших прямо встановлює AC-07.4.|S1 §3, с.5; §5 AC-07.4|
|BR-08.1|Open -> In Progress; In Progress -> Resolved; Resolved -> Closed; Resolved -> In Progress. Інші переходи не дозволені.|S1 §3, с.5|
|BR-09|Issue важливий, якщо priority = High або Critical.|S1 §3, с.5|
|BR-09.1|Resolved означає вирішено, але ще не закрито. До переходу в Closed заявка активна та може відображатися в Important відповідно до priority. У PDF заголовок надруковано «BR-09 1.»; тут використано методичне посилання BR-09.1.|S1 §3, с.5|
|BR-10|Issues не видаляються із системи.|S1 §3, с.5|
|BR-11|У першій версії окрема користувацька історія змін issue не передбачається.|S1 §3, с.5|


## Похідні висновки — DERIVED

1. Important = `(priority in {High, Critical}) AND (status != Closed)` [BR-09; BR-09.1; AC-08.1–AC-08.4]. Невстановлений priority не відповідає High/Critical і виключається; це висновок за предикатом, а не дослівна частина AC-08.3.
2. Status enabled тільки коли current user = current assignee та є дозволений наступний стан [BR-08; BR-08.1; AC-07.4]. Lead non-assignee не має цього права.
3. Closed не має вихідних статусних переходів, але це не забороняє comment, assignment чи priority change [BR-08.1; US-03/04/06].
4. Без assignee жоден користувач не змінює status. Lead спочатку призначає виконавця [US-03; AC-07.4].

## NFR — актуальна редакція §8

|ID|SOURCE|Що видно в макеті|Що потребує реалізації|
|---|---|---|---|
|NFR-01|Response time < 1 s|NOT VERIFIABLE|Вимірювання часу операцій у реалізованій системі.|
|NFR-02|Authentication required|S-01 boundary; це лише позначення вимоги|Реальний login, session та перевірка неавтентифікованого доступу.|
|NFR-03|HTTPS only|NOT VERIFIABLE; окремого екрана немає|Deployment HTTPS, сертифікат і заборона незахищеного доступу.|
|NFR-04|Backup of all data|NOT VERIFIABLE; окремого екрана немає|Backup і restore усіх даних MVP. Attachments прибрано оновленим NFR у §8.|


## Реєстр питань Q-01–Q-05

|Q-ID|Питання / джерело|Підхід для дизайну|Статус / межа|
|---|---|---|---|
|Q-01|Який механізм authentication? S1 §1; R-01|D-02: нейтральна S-01, demo з S-02|UNRESOLVED для реалізації; не блокує статичний дизайн.|
|Q-02|Як відображати absent priority; чи можливий reset? BR-04/05|D-03: Not Set як absence; лише 4 options; reset немає|DESIGN PROPOSAL; Source: M с.7; null/enum не визначено.|
|Q-03|Початковий assignee; перепризначення? US-03|D-04: unassigned при створенні; Lead перепризначає|DESIGN PROPOSAL; Source: M с.7; записано 10.10.2026; рішення APPROVED у 00.|
|Q-04|Спосіб застосування змін і показ недоступних controls? AC-07.4; US-03/04|D-05/06: disabled; Apply біля контролу|DESIGN PROPOSAL; Source: M с.7; записано 10.10.2026; рішення APPROVED у 00.|
|Q-05|Повернення, симуляція збереження й error copy? US-01/06/07|D-07/08: попередній tab; prepared states; робочі error labels|DESIGN PROPOSAL; Source: M с.7; реальне збереження не доведено.|


## Source Check — контроль A

Source Check: зіставлено included US та AC з S1 §1/3/5/8. Покриття — 33/33; змістових втрат не виявлено. Результат документальної звірки: VERIFIED, 10.10.2026. Оператор Корякін З. П. підтвердив звірку та прийняв результат 10.10.2026.

|№|AC / пункт|Місце у Pack|Результат звірки|Статус|
|---|---|---|---|---|
|1|AC-01.1|Реєстр 33 AC, рядок 1|PRESENT / зміст збережено|VERIFIED|
|2|AC-01.2|Реєстр 33 AC, рядок 2|PRESENT / зміст збережено|VERIFIED|
|3|AC-01.3|Реєстр 33 AC, рядок 3|PRESENT / зміст збережено|VERIFIED|
|4|AC-01.4|Реєстр 33 AC, рядок 4|PRESENT / зміст збережено|VERIFIED|
|5|AC-01.5|Реєстр 33 AC, рядок 5|PRESENT / зміст збережено|VERIFIED|
|6|AC-02.1|Реєстр 33 AC, рядок 6|PRESENT / зміст збережено|VERIFIED|
|7|AC-02.2|Реєстр 33 AC, рядок 7|PRESENT / зміст збережено|VERIFIED|
|8|AC-02.3|Реєстр 33 AC, рядок 8|PRESENT / зміст збережено|VERIFIED|
|9|AC-02.4|Реєстр 33 AC, рядок 9|PRESENT / зміст збережено|VERIFIED|
|10|AC-02.5|Реєстр 33 AC, рядок 10|PRESENT / зміст збережено|VERIFIED|
|11|US-03, AC, пункт 1|Реєстр 33 AC, рядок 11|PRESENT / зміст збережено|VERIFIED|
|12|US-03, AC, пункт 2|Реєстр 33 AC, рядок 12|PRESENT / зміст збережено|VERIFIED|
|13|US-03, AC, пункт 3|Реєстр 33 AC, рядок 13|PRESENT / зміст збережено|VERIFIED|
|14|US-03, AC, пункт 4|Реєстр 33 AC, рядок 14|PRESENT / зміст збережено|VERIFIED|
|15|AC-04.1|Реєстр 33 AC, рядок 15|PRESENT / зміст збережено|VERIFIED|
|16|AC-04.2|Реєстр 33 AC, рядок 16|PRESENT / зміст збережено|VERIFIED|
|17|AC-05.1|Реєстр 33 AC, рядок 17|PRESENT / зміст збережено|VERIFIED|
|18|AC-05.2|Реєстр 33 AC, рядок 18|PRESENT / зміст збережено|VERIFIED|
|19|AC-05.3|Реєстр 33 AC, рядок 19|PRESENT / зміст збережено|VERIFIED|
|20|AC-06.1|Реєстр 33 AC, рядок 20|PRESENT / зміст збережено|VERIFIED|
|21|AC-06.2|Реєстр 33 AC, рядок 21|PRESENT / зміст збережено|VERIFIED|
|22|AC-06.3|Реєстр 33 AC, рядок 22|PRESENT / зміст збережено|VERIFIED|
|23|AC-06.4|Реєстр 33 AC, рядок 23|PRESENT / зміст збережено|VERIFIED|
|24|AC-06.5|Реєстр 33 AC, рядок 24|PRESENT / зміст збережено|VERIFIED|
|25|AC-07.1|Реєстр 33 AC, рядок 25|PRESENT / зміст збережено|VERIFIED|
|26|AC-07.2|Реєстр 33 AC, рядок 26|PRESENT / зміст збережено|VERIFIED|
|27|AC-07.3|Реєстр 33 AC, рядок 27|PRESENT / зміст збережено|VERIFIED|
|28|AC-07.4|Реєстр 33 AC, рядок 28|PRESENT / зміст збережено|VERIFIED|
|29|AC-07.5|Реєстр 33 AC, рядок 29|PRESENT / зміст збережено|VERIFIED|
|30|AC-08.1|Реєстр 33 AC, рядок 30|PRESENT / зміст збережено|VERIFIED|
|31|AC-08.2|Реєстр 33 AC, рядок 31|PRESENT / зміст збережено|VERIFIED|
|32|AC-08.3|Реєстр 33 AC, рядок 32|PRESENT / зміст збережено|VERIFIED|
|33|AC-08.4|Реєстр 33 AC, рядок 33|PRESENT / зміст збережено|VERIFIED|


Контрольні суми AC за US: 5 + 5 + 4 + 2 + 3 + 5 + 5 + 4 = **33**. Контроль A: оператор Корякін З. П.; перевіряється 01 v1.1 проти S1. Дата підтвердження: 10.10.2026. Verdict: APPROVED. Усі 33 AC звірено зі специфікацією; змістових втрат і розбіжностей не виявлено.


## Оригінали джерел

- SD_Spec.docx.pdf: 13 сторінок; отримано 10.10.2026.
- Mini_Issue_Tracker_UX_UI_Methodological_Guide_UA.docx.pdf: 29 сторінок; отримано 10.10.2026.
