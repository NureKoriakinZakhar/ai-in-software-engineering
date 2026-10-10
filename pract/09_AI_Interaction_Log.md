# Журнал AI-взаємодій v1.1

Корякін З. П.; Кириченко К. В.; ПЗПІ-23-8. Дата: 10.10.2026.

## Інструменти та спосіб роботи

Текстову частину завдання підготовлено за допомогою GPT-6 ASTRA з рівнем міркування High; wireframes — засобами Figma Design і Figma Agent. Документальна звірка, налаштування базових connections та контрольне проходження Present виконані з автоматизованою допомогою. Прийняття поточних результатів Кириченком К. В. підтверджено через Корякіна З. П. 10.10.2026; запис рішення — у 00/04/06/07/08. Протокол мінітесту — у 07.

Модель текстового AI-асистента — GPT-6 ASTRA; рівень міркування — High. Модель Figma Agent, тарифний план і баланс кредитів не зафіксовані.

## Формат журналу — Додаток B2

Для кожного етапу наведено контекст, режим, запит, результат, рішення, перевірку та обмеження. Формулювання G1–G6 наведені з методички для відтворення етапів, а не як дослівна стенограма сесії. Результати описують наявні артефакти. Запити Figma збережені в чаті Create editable frames.

## G1 — Input Pack і вихідні вимоги

**Контекст.** SD Spec (S1, 13 сторінок), методичні рекомендації (M, 29 сторінок). Режим: GPT-6 ASTRA / High, аналіз документів і підготовка Markdown.

**Методичний запит (M с.6).**

> Ти — аналітик вимог. Створи UX/UI Design Input Pack лише з прикріпленої актуальної специфікації Mini
> Issue Tracker. Екрани ще не проєктуй.
> Спочатку назви прочитаний файл та підтвердь, які його розділи доступні. Якщо матеріал неповний, не
> роби вигляд, що прочитано все.
> Визнач Release MVP за остаточним Release Scope, а не за Candidate MVP. Не трактуй пізніший розділ
> як автоматичне скасування суперечливих бізнес-правил: суперечності винеси окремо.
> Сформуй:
> 1. Product purpose — до 3 речень; actors та межі першого релізу.
> 2. Included US; Deferred; Future; explicitly out of scope.
> 3. Для кожної включеної US — ID, actor, мета, усі AC зі збереженням змісту та вихідних
> ідентифікаторів.
> 4. UI-релевантні BR: права, початкові значення, переходи, Important Issues, comments, заборонені дії.
> 5. Relevant NFR; окремо вимоги, які не перевіряються макетом.
> 6. Q-ID: конфлікти, прогалини та питання, що потребують рішення людини.
> Для кожного твердження вкажи Source: розділ + US/AC/BR або точний пункт. Познач тип: SOURCE /
> DERIVED / PROPOSED / UNRESOLVED. Висновки DERIVED обґрунтуй джерелами; PROPOSED не
> включай до обов’язкових вимог.
> Не додавай нові функції, поля, ролі, екрани, способи автентифікації чи механізми збереження. Не
> перетворюй припущення на погоджені рішення. Не вигадуй ID для ненумерованих вихідних критеріїв.
> Збережи всі негативні умови: відсутні права, недопустимі переходи, помилка збереження comment,
> виключення з Important Issues. Розрізняй Not Set як відсутність priority і встановлений рівень priority. Не
> прирівнюй Resolved до Closed.
> Закінчи Source Check: кожна included US → усі її AC → місце у Pack; перелік excluded вимог із
> причиною; список unresolved питань. Не оголошуй Pack погодженим. Виведи текст, придатний до
> копіювання в документ.

**Результат.** Підготовлено 01_Input_Pack_v1.0.md: US-01–08, реєстр 33 AC, бізнес-правила, обмеження й відкриті питання.

**Рішення.** Прийнято структуру Input Pack і збереження вихідних AC-ID. US-09 та майбутні SR-10/SR-11 не включено до дизайну релізу. Пункти US-03 позначено посиланнями на вихідний текст, без вигаданих AC-ID.

**Перевірка й обмеження.** Зіставлено записи з S1 §1/3/5/8; 33/33 AC збережені. Це перевірка повноти документів, а не реалізації системи. Доказ: 01, розділ Source Check.

## G2 — Decision Log і Screen Map

**Контекст.** Input Pack, методичні рекомендації та UX-рішення D-01–D-08. Режим: GPT-6 ASTRA / High.

**Методичний запит (M с.8).**

> Ти — UX architect. Використовуй останній погоджений Input Pack і Decision Log. Не відновлюй
> Deferred/Future функції з ранньої історії чату.
> Побудуй мінімальну систему екранів для Release MVP. Одна User Story не означає один screen:
> related controls можна розмістити у спільних деталях issue.
> Для кожної surface/state запиши:
> Screen/State ID | Name | Purpose | Actors | Entry | Visible data | Inputs | Actions | Role/state conditions |
> Errors/empty states | Exit | Source/D-ID.
> Розрізняй screen, state того самого screen, modal/overlay, component state та службову annotation.
> Визнач також, скільки Figma frames потрібно для демонстрації, не плутаючи це з кількістю
> продуктових екранів.
> Для погодженого варіанта використай: S-01 Authentication boundary; S-02 Issues List зі станами S-02-A
> All, S-02-B Important, S-02-C Empty; M-01 Create modal; S-03 Issue Details. Не додавати самостійні
> сторінки Assignment, Priority, Status або Comments.
> Зроби таблицю переходів:
> T-ID | From | Actor | Trigger | Preconditions | To | Visible result | Requirement/D-ID.
> Покрий сценарії: створення та перегляд issue; призначення і priority для Team Lead; дозволені статусні
> переходи; повернення Resolved у роботу; comment success/error; перегляд Important; заборонена дія
> для неуповноваженого користувача; порожній список.
> Врахуй повернення на попередній list state, якщо це погоджено. Недопустима дія не створює перехід.
> S-01 залишається placeholder, а не вигаданим login screen.
> Дай текстовий user flow для кожного сценарію з ID екранів та очікуваними станами. Наведи 3
> приклади того, що НЕ слід додавати, навіть якщо це типово для issue trackers.
> Наприкінці: мінімальний Screen Inventory; unresolved рішення; критерії, які план ще не покриває. Не
> створюй зображення, код чи Figma-файл. Не оголошуй свій план затвердженим.

**Результат.** Підготовлено 00_Decision_Log_v1.0.md і 02_Screen_Map_v1.0.md. Визначено чотири продуктові поверхні: S-01, S-02, M-01, S-03; шість канонічних frames з урахуванням станів списку; окрему REF-01. Сценарії T-01–T-10 прив’язано до поверхонь.

**Рішення.** Прийнято All/Important tabs, modal Create, disabled controls для заборонених дій, повернення до попередньої вкладки та підготовлені результати прототипу. Не включено окремі продуктові сторінки для призначення, пріоритету, статусу й коментарів; role switcher та додаткову роль Reviewer.

**Перевірка й обмеження.** Перевірено відповідність карти included US/AC і методичним рекомендаціям с.7–9. Механізм автентифікації не визначався довільно: S-01 позначає межу доступу, демонстрація починається з автентифікованого стану. Доказ: 00/02.

## G3 — Screen Contracts і Traceability

**Контекст.** Input Pack, Decision Log, Screen Map, права ролей та правила статусів. Режим: GPT-6 ASTRA / High.

**Методичний запит (M с.10).**

> Підготуй Developer-Verifiable Screen Contracts за погодженим планом. Не додавай продуктових вимог.
> Нові UX-рішення познач PROPOSED D-ID, а не SOURCE.
> Для кожного screen/state запиши:
> 1. ID, призначення, actors, entry conditions.
> 2. Visible data: назва поля, обов’язковість, вигляд відсутнього значення.
> 3. Controls: C-ID, label, type, visible/enabled conditions, trigger, результат, Source/D-ID.
> 4. Default, empty, validation та error states.
> 5. Incoming/outgoing transitions з T-ID.
> 6. Що саме перевіряється в макеті, у прототипі та лише в реалізації.
> Окремо сформуй permission matrix для Team Member non-assignee; Team Member assignee; Team Lead
> non-assignee; Team Lead assignee. Дії: view, create, comment, assign, change priority, change status.
> Assignee — відношення користувача до issue, не нова глобальна роль. Team Lead не отримує
> автоматично права на status.
> Побудуй повну матрицю status transitions. Поточний status — не новий перехід; Closed не має вихідних
> переходів. Дозволені лише переходи BR-08.1.
> Запиши Important predicate точно: priority у {High, Critical} AND status != Closed. Додай приклади
> High+Resolved, Critical+Closed та відсутній priority.
> Для Create відокрем користувацькі поля від автоматично заданих. Для priority розрізни відсутнє
> значення та доступні для встановлення значення. Для comments збережи author, time і невдале
> збереження без створеного comment.
> Зроби Traceability:
> Source ID/пункт | UIR-ID | Screen/State | C-ID або annotation | Test ID | Verification level.
> Покрий усі AC включених US. Для US-03 зберігай посилання на вихідні ненумеровані пункти.
> Для кожного тесту: actor/context, precondition, action, expected visible result, що не можна довести цим
> тестом. Не став PASS за майбутній макет. Перелік потрібних бізнес-рішень виведи окремо.

**Результат.** Підготовлено 03_Screen_Contracts_v1.0.md: 33 записи простежуваності, матриці прав і переходів, тестові дані та очікувані результати.

**Рішення.** Прийнято чотири дозволені переходи статусу; Closed — кінцевий стан. Lead без призначення на заявку не отримує права змінювати її статус. До Important включаються High/Critical зі статусом, відмінним від Closed; Resolved не виключається. Not Set означає відсутній пріоритет і не є пунктом вибору.

**Перевірка й обмеження.** Матриці зіставлено з BR-08/08.1, BR-09/09.1 та AC. Для кожного критерію розділено видимий UI, підготовлену симуляцію та перевірку реалізації. Серверні права й збереження даних прототипом не доведені. Доказ: 03.

## G4 — Plan Review

**Контекст.** Комплект 00–03, S1 і методичні рекомендації. Режим: GPT-6 ASTRA / High, документальна перевірка.

**Методичний запит (M с.12).**

> Перевір план як критичний рецензент. Не захищай попередні відповіді. Зістав вихідну специфікацію,
> погоджені D-рішення, Input Pack, Screen Contracts і Traceability.
> Якщо вихідної специфікації немає у доступному контексті, назви обмеження: не стверджуй, що
> перевірив відповідність S1.
> Пройди кожну included US і кожен AC. Шукай: пропуски; зайві функції; підміну вимог UX-рішеннями;
> неправильні права; незаконні status transitions; неправильне трактування Resolved або Not Set;
> неможливі маршрути; невизначені результати дій; дублювання екранів; непотрібні product controls;
> непокриті empty/error states.
> Особливо перевір: Team Lead non-assignee не змінює status; у Create тільки Title/Description; Important
> включає High/Critical Resolved; Closed не має status transitions; усі джерельні ID реальні;
> backup/HTTPS не перетворено на екрани.
> Вихід 1 — матриця coverage для всіх AC: COVERED / MISSING / AMBIGUOUS із доказом у плані.
> Вихід 2 — DEF-ID | severity | source | plan location | проблема | мінімальне виправлення. Відокрем
> вимоговий дефект від необов’язкової UX-пропозиції.
> Вихід 3 — Q-ID, які блокують генерацію, та питання, які можна відкласти.
> Вихід 4 — PLAN READY / NOT READY з поясненням. READY — тільки рекомендація; остаточне
> рішення приймає розробник.
> Не додавай «покращення» без виявленої проблеми. Не змінюй джерело. Після виправлень дай
> перелік змінених пунктів, без повного переписування непорушених розділів.

**Результат.** Підготовлено 04_Plan_Review_v1.0.md. Покриття — 33/33; результат документальної перевірки — PLAN READY. Поточний план прийнятий Кириченком К. В.; запис — у 04.

**Рішення.** Прийнято поточну структуру плану як основу генерації. Невизначений механізм автентифікації залишено відкритим технічним питанням; вигадану форму login не включено.

**Перевірка й обмеження.** Перевірено права, переходи, Important, required fields, початкові значення та граничні випадки. Цей запис підтверджує AI-перевірку матеріалів; подальше прийняття рецензентом записано у 04. Доказ: 04/08.

## G5 — Figma Brief

**Контекст.** Перевірені 00–04, тестові дані й вимоги до low-fi макета. Режим: GPT-6 ASTRA / High, підготовка англомовного brief.

**Методичний запит (M с.13).**

> Скомпілюй один self-contained англомовний Figma Design implementation brief з погоджених Screen
> Contracts. Це не новий UX-дизайн і не переказ усієї специфікації.
> Обов’язкові секції: purpose and scope; design constraints; canonical screens/states with exact IDs;
> required labels/data; controls and permissions; status transitions; Important predicate; required empty/error
> examples; navigation intent; sample data; exclusions; acceptance checklist.
> Кожне правило визнач один раз. Збережи Source/D-ID у коротких посиланнях. Не включай Candidate
> MVP, історію дискусії, backend design і деталізацію Deferred/Future. Заборонені функції переліч один
> раз.
> Попроси: editable Figma-native layers; reusable local components; Auto Layout де доречно; grayscale
> low-fidelity; meaningful names; одна робоча сторінка; примітки поза продуктовими frames; жодних page
> icon placeholders, декоративних квадратів, row-selection або bulk controls.
> Створи canonical screens і компактні control/state examples; не вимагай повних сторінок для всіх role ×
> status combinations. У state reference повинні бути всі 4 statuses і всі 4 role/assignee contexts.
> Для prototype на цьому кроці лише анотації переходів. Не проси Agent експортувати файли чи
> реалізувати backend, authentication, conditional logic або перевірку прав у коді.
> Усі введені UX-рішення повинні вже мати APPROVED D-ID. Якщо рішення необхідне, але не
> погоджене, не приховуй його у brief — поверни BLOCKER.
> Виведи лише текст файла Markdown, без вступу і без зовнішньої рамки коду. Не урізай важливі
> правила заради заданої кількості символів: обмеження поля запуску вирішується вкладенням файла.

**Результат.** Підготовлено 05_Figma_Brief_v1.0.md для генерації шести основних frames та REF-01.

**Рішення.** Прийнято grayscale low-fi, native editable layers, локальні компоненти й Auto Layout там, де доречно. Не включено unsupported features: видалення, attachments, пошук, сортування, bulk actions, історію, dashboards та додаткові metadata.

**Перевірка й обмеження.** Brief зіставлено з 00–03; він містить дані та правила, потрібні без звернення до інших документів. Генерація макета не замінює backend і тестування реалізації. Доказ: 05/06.

## A/B/C — документальна перевірка

Перевірено повноту джерела, права, allowed transitions, Important predicate, початкові значення та error states. Документальний результат: VERIFIED / PLAN READY для D-01–D-08 і плану генерації. Метод: AI-перевірка матеріалів; прийняття поточного плану рецензентом записано у 00/04. Докази: 00/01/04/05/06.

## F1 — запит до Figma Agent

**Контекст і режим.** Вкладений 05_Figma_Brief_v1.0.md, сторінка UX/UI v1.0. Інструмент: Figma Agent; модель і рівень міркування цього інструмента не зафіксовані.

**Збережений продуктовий фрагмент запиту F1.** Організаційну преамбулу опущено; повний текст доступний у чаті Create editable frames, 10.10.2026:

Use the attached 05_Figma_Brief_v1.0.md as the approved design contract for Mini Issue Tracker.
Read the complete attachment. If missing, unreadable or blocked, stop and identify the problem.
Create its six canonical editable low-fidelity frames and separate compact REF-01 state reference on one page. Preserve exact screen/control IDs, fields, sample data, permissions, four status transitions and Important predicate. Use native editable layers, grayscale, actual local reusable components and Auto Layout where practical. Keep annotations outside product frames.
Do not add page icons, square placeholders, row-selection, bulk actions or unsupported features. Do not create sixteen full role/status screens. Do not wire a prototype or implement backend logic.
In THIS response report actual created frames/state references, reused components, NOT REPRESENTED requirements, UNRESOLVED issues and limitations. Do not claim persistence, authentication or server permissions were tested.

## F1 — результат генерації

[Figma Design](https://www.figma.com/design/WR2MU9NL1NdQj6LQJYAB7N), чат **Create editable frames**. Контекст: вкладений 05_Figma_Brief_v1.0.md. Оригінальний текст вкладення збережений у чаті; поточна редакція brief має те саме продуктове наповнення.

Відповідь Figma Agent: шість основних frames, окрема REF-01, п'ять Create examples, чотири контексти прав і чотири статуси, матриці, comments і after-close examples. Заявлено 14 локальних компонентів та 113 instances; тривалість 10 хв 48 с. NOT REPRESENTED — none; UNRESOLVED — none. Перевірка результату: огляд семи зображень, редагування тексту зі скасуванням, перехід instance → main component та огляд окремих станів. Повний підрахунок компонентів не проводився. Кредити й повідомлення про ліміт не зафіксовані.

**Рішення за результатом F1.** Генерацію прийнято як базовий low-fi макет після огляду. Числа components/instances з відповіді збережено як заявлені інструментом, а не як незалежно підтверджений підрахунок. Висновки про роботу backend, authentication чи persistence не прийнято як результати UI-перевірки.

## P1-STATES — підготовка демонстраційних станів

**Режим.** Figma Agent, розширення наявного макета; модель і параметри режиму не зафіксовані.

Контекст: готові основні екрани, тестові дані та базові connections. Запит: додати окрему Section P1 states на тій самій сторінці, 51 prepared frame і шість menus для тестових випадків; зберегти основні екрани й продуктову логіку. Повний текст запиту і відповіді збережено в чаті **Create editable frames**.

Відповідь Figma Agent: виконано за 14 хв 13 с; заявлено 51 frame, шість menus, 432 instances та 14 definitions. Ці числа взяті зі звіту генерації; незалежний повний підрахунок не проводився. Перевірені приклади прав, пріоритетів, статусів, comments і результати операцій. Генерація не створювала prototype interactions; connections налаштовано окремо з автоматизованою допомогою. Додаткові стани — підготовка тестів, а не F2 correction.

**Рішення.** Додаткові стани включено як демонстраційні приклади для тестів. Їх не зараховано як виконані інтерактивні дії або окремі продуктові сторінки. Перевірка: огляд menus, рольових обмежень і prepared result states; докази у 06/07.

## P1 — прототип і версії

**Дії за M с.18:** налаштування базових connections у Prototype та перевірка маршрутів у Present. Запит генерації interactions до Figma Agent на цьому етапі не відправлявся.

**Контекст і режим.** Готовий Figma-макет; автоматизоване налаштування Prototype та проходження Present. Текстовий супровід — GPT-6 ASTRA / High.

Базові transitions налаштовано у Prototype і перевірено у Present: 37 PASS та додаткові маршрути у 07. Збережені версії: **P1 baseline v1.0 — 10.10.2026**, **P1 basic routes — 10.10.2026**, **P1 expanded routes — 10.10.2026**. Резервна копія: [BACKUP P1 baseline](https://www.figma.com/design/QVA2xV9PJ7Ki88dAMXx538), без пізніших expanded states.

**Рішення.** Підтверджені базові маршрути включено до результатів PASS. P-29–P-44 налаштовано через редактор Prototype й перевірено у Present: 16/16 PASS (prepared simulation). Прямі старти Flow 2–4 не отримали окремого PASS; відповідні маршрути створення перевірені зі списків. Обмеження: фіксоване введення та prepared states, без накопичення даних і серверного збереження.

## Мінітест із одногрупником

За повідомленням Корякіна З. П., роботу й три сценарії розглядали разом із Кирилом; затруднень у Кирила не було. Маршрути підтверджених сценаріїв і спостереження спільного проходження наведено у 07. Незалежний формат без підказок за M с.22 не підтверджено. Окреме автоматизоване контрольне проходження трьох сценаріїв має 3/3 PASS prepared UI; його результати не є спостереженнями за учасником.

## G6 — фінальний аудит доказів

**Контекст / режим.** 03/05, зображення макета, поточні Figma states і протокол 07. GPT-6 ASTRA / High, аналіз тексту та UI-доказів; дата: 10.10.2026.

**Методичний запит (M с.20).**

> Перевір Mini Issue Tracker за погодженими вимогами і наданими доказами. Не вважай звіт Figma
> Agent доказом виконаної правки.
> Спочатку переліч видимі Screen/State IDs і скажи, чи читається текст. Якщо частини нечіткі або
> відсутні, назви їх. Не реконструюй екран із попереднього prompt.
> Частина A — вимоги. Для кожного included AC та UI-релевантного BR/D-рішення заповни:
> Source | Expected | Screen/State | Observed evidence | Result | Remaining test.
> Results: PASS — очікуваний UI-доказ видно; PARTIAL — видно лише частину; FAIL — видно
> суперечність; NOT VERIFIABLE — даних недостатньо або потрібна реалізація. Якщо обов’язковий
> state відсутній у повному заявленому комплекті, це дефект комплекту. Якщо надано лише частину
> export, не плутай це з доведеною відсутністю state у файлі.
> Окремо перевір права, current assignee, початкові значення, усі чотири переходи, Resolved != Closed,
> Important predicate, comments, validation/empty states та відсутність зайвих функцій і page icon
> placeholders.
> Статичний disabled control не доводить серверну авторизацію; намальований comment не доводить
> persistence. HTTPS, backup, actual response time і login не позначати PASS за картинкою. Ручні
> результати прототипу позначати як повідомлення студента, якщо не спостерігаєш їх сам.
> Частина B — UX. Дай до 5 доказових проблем навігації, читабельності, зрозумілості дій, consistency,
> error prevention або базової доступності. Не прирівнюй цей огляд до сертифікації accessibility чи тесту
> з реальними користувачами.
> Частина C — DEF-ID/UX-ID | Severity | Location | Source | Evidence | Minimal correction. Не пропонуй
> нові функції.
> Завершення: 1) UI design coverage — complete/partial/failed; 2) prototype evidence —
> verified/reported/not provided; 3) implementation tests outstanding. Не давай загального «всі AC
> виконано», якщо є NOT VERIFIABLE. Не виправляй макет; підготуй перелік для людини.

**Результат.** Первинний статичний огляд: 21 PASS (UI), 12 PARTIAL, 0 FAIL для 33 AC. Подальший огляд підтвердив потрібні control/state examples і базові маршрути. UI design coverage — complete; базовий prototype evidence — verified у межах prepared simulation; реалізація не перевіряється wireframes.

**Рішення.** Рекомендація аудиту — ACCEPT WITH LIMITS. Підстави для EVID-01–04 і залишок перевірки наведено у 06. EVID-01–04 прийняті Кириченком К. В.; рішення — у 06.

**Перевірка.** Права current assignee, чотири переходи, Closed terminal, Important із Resolved, required/error/empty states, comments і scope. Докази: 06/07/08. 33/33 AC збережені, локальні посилання перевірені.

**Обмеження / резерв.** Контроль A/C підтверджено Корякіним З. П. Спостереження спільного проходження записано у 07; незалежний формат без підказок не підтверджено. Рішення рецензента B/D внесено у 04/06. P-29–P-44 — PASS у межах prepared simulation; Share — Anyone can view. Резерв — особисте review та спостереження трьох завдань без підказок.

## B2 — параметри сеансів і відповідальність

Дата записів: 10.10.2026. Оператор комплекту — Корякін З. П.; призначений рецензент — Кириченко К. В. Текстові записи G1–G6: GPT-6 ASTRA / High, додатковий номер версії й тариф не зафіксовані. F1/P1-STATES: Figma Design / Figma Agent; модель, plan і режим не показані у збережених відповідях.

|Step|Context / version|Prompt / response|Decision / evidence|Limit / fallback|
|---|---|---|---|---|
|G1–G3|S1, M; 00–03|Методичні запити та результати наведено вище|33/33; правила, матриці та fixtures звірені; контроль A APPROVED|Параметри сесії крім моделі/High не збережені; резерв — звірка S1 вручну|
|G4 / B|S1, M; 00/01 v1.1, 02/03|Методичний запит вище; результат — 04|PLAN APPROVED; прийняття рецензентом у 04|AI-review не незалежне; резерв — Кириченко К. В. перевіряє джерело й граничні сценарії|
|G5 / C|00–04; 05|Brief та запис G5|Самодостатній brief VERIFIED; контроль C APPROVED|Прийняття фінального brief підтверджено оператором 10.10.2026|
|F1|05 у чаті Create editable frames|Дословний launcher вище; відповідь у Figma|Базові frames/state examples оглянуто, native editability перевірено|Кредити до/після та exhaustion не зафіксовані; резерв — ручні Layers/компоненти|
|P1-STATES|Робочий файл; P1 states|Повний запит/відповідь у Figma chat|Додаткові states представлені; reported totals не є незалежним підрахунком|Plan/model/credits невідомі; резерв — ручні prepared examples|
|F2|Поточний макет і контрольні випадки|Запит не відправлявся; F2 не виконувався|Доказового дефекту для корекції не зафіксовано|F2 не проводилась; резерв — локальна правка після виявленого дефекту|
|P1|P1 expanded routes — 10.10.2026|Запис connections і node IDs у 07|37 PASS, включно з P-29–P-44; 7 CONFIGURED|Фіксовані дані; довільний input і persistence не моделюються|
|G6 / D|06/07/08; поточний макет|Методичний запит G6; результат — 06/08|ACCEPT WITH LIMITS; EVID-01–04 прийняті рецензентом|Спільне проходження без затруднень; незалежний мінітест не підтверджено; Share Anyone can view; резерв — особистий review і нове спостереження|

## Розширення P1 — фактична взаємодія, 10.10.2026

Контекст: готові P1 states, контракти T-03/04/05/07/08 і перевірки за M с.18/22. Режим: налаштування connections у Figma Prototype та UI-кліки в Present з автоматизованою допомогою; текстовий супровід — GPT-6 ASTRA / High. Окремий запит генерації до Figma Agent не відправлявся. Прийняте: зв’язати Apply з assignment/priority/status results, Return/All/Title з after-close frames, Add Comment з validation/success/failure.

Результат і перевірка: 16 connections P-29–P-44 створені; кожний hotspot пройдено у Present, результат та node ID звірено. 16/16 PASS; повний протокол і прямі flow links у 07. Share settings збережено як Anyone can view. Версія P1 expanded routes — 10.10.2026 збережена в історії Figma. Фактичні обмеження: prepared states без backend, довільного введення й накопичення записів. Ліміти або використання AI-кредитів цим UI-налаштуванням не підтверджуються.

## Прийняття результатів рецензентом — 10.10.2026

Контекст: поточний план, рішення D-01–D-08, звіт 06 і протокол P1. Рішення Кириченка К. В.: поточний план і D-01–D-08 — APPROVED; EVID-01–04 та результати прототипу — ACCEPTED WITH LIMITS. Підтвердження передано Корякіним З. П. Записи узгоджено у 00/04/06/07/08. Спостереження спільного проходження з Кирилом — у 07; незалежний формат без підказок не підтверджено.

## Підтвердження контролю A/C — 10.10.2026

Оператор Корякін З. П. підтвердив звірку всіх 33 AC з вихідною специфікацією та перевірку фінального Figma brief. Результат A: повна вибірка без змістових втрат, APPROVED. Результат C: brief прийнято, APPROVED. Записи — у 01/06.
