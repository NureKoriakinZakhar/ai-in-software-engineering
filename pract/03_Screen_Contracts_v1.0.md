# 03 Screen Contracts v1.1 — G3

Автори навчального пакета: Корякін З. П., Кириченко К. В.; ПЗПІ-23-8. Дата: 10.10.2026. Статус: DOCUMENT VERIFIED; поточний контракт — APPROVED рецензентом (04). SOURCE і DESIGN пропозиції розділено у 01/00. Робочий Figma-файл і результати перевірки наведено у 06/07.

## Рівні верифікації

- UI: видимі поля, тексти, states, options, disabled controls, consistency — лише після отримання макета.
- SIM: ручне проходження підготовлених prototype connections, без реального обчислення умов і збереження.
- IMPL: authentication, server permissions, validation запитів, унікальність ID, persistence, atomic failed save, actual timing, HTTPS, backup/restore. Не доводяться wireframe або Figma prototype.

У Traceability coverage означає наявність контракту, а не PASS. Фактичні результати T-01–T-10 наведено у 07; контракти описують очікувану поведінку.

## Контракти поверхонь

### S-01 Authentication boundary

Purpose/actor/entry: зовнішня межа authentication для відвідувача. Visible data: назва Mini Issue Tracker та «Authentication entry — mechanism TBD»; обидва read-only. Inputs і controls відсутні; error/empty states не вигадуються. Вихід demo не є перевіреним login; T-09 стартує окремо з S-02. UI доказ — нейтральна boundary; NFR-02 перевіряється лише реалізацією. Source: BR-01; NFR-02; D-02/08.

### S-02-A All Issues

Entry: authenticated Member/Lead, demo baseline або Return із All. Visible data: title Issues List; All active; Important tab; Create Issue; 8 rows зі зразків еталонних даних M с.21. Кожний row має ID, Title, Status, Priority; Assignee якщо призначений; для відсутності показано Unassigned (DESIGN display). Priority absence показано Not Set. Controls C-01–C-04. Inputs відсутні. Outgoing: T-01 Create; T-08 Important; T-09 Title. Incoming: T-09 Return або Cancel. Default: fixture із 8 issue; zero collection — S-02-C, а не loading error. UI показує поля; SIM показує navigation; auth/persistence — IMPL. Source: AC-02.1/2/3; AC-05.1/3; D-01/07/08.

### S-02-B Important Issues

Entry: C-02 або Return із Important. Visible data та row structure ідентичні S-02-A; active Important. Default rows: ISS-001, ISS-002, ISS-003, ISS-007. Inputs відсутні; controls C-01–C-04. Predicate — лише High/Critical AND non-Closed. Після prepared close ISS-003 показано 001/002/007; після Create ISS-009 Not Set не додається в Important. Incoming/outgoing: T-08 tabs; T-09 Title/Return/Cancel; T-01 Create. За zero dataset може використовувати empty component, але це не заміна AC-02.5 All-empty. Помилка завантаження не описана S1 і не додається. UI показує точну вибірку; SIM navigation; actual filter query — IMPL. Source: US-08; BR-09/09.1; D-01/07/08.

### S-02-C Empty All Issues

Entry: окремий start point zero fixture, authenticated actor. Visible data: Issues List; tabs; Create Issue; «No issues yet»; 0 rows. Controls C-01/02/03 та A-EMPTY; inputs відсутні. Default/empty: zero registered issues; не label «No important issues» при непорожній колекції. T-09 inspection; T-01 -> M-01. Cancel залишає zero fixture. Success Create показує ISS-009 і Return -> prepared All із одним row. Source: AC-02.5; D-01/08.

### M-01 Create modal

Entry: C-03 з A/B/C. Visible data: Create Issue, labels Title/Description, Create/Cancel. Controls C-05–C-08. Title і Description обов’язкові; Description multiline. Немає inputs ID, author, created time, priority, status або assignee. Default: пусті editable fields. Missing Title: «Title is required» [S1 US-01 Gherkin]; Missing Description: «Description is required» [DESIGN copy]. Обидва empty: показати обидві помилки; не створювати issue і не закривати modal. Підготовлений valid state: title/description ISS-009. Valid Create -> S-03 ISS-009 з auto defaults; Cancel -> calling list без мутації. T-01/T-02/T-09. UI не доводить генерацію унікального ID/часу чи save. Source: AC-01.1–AC-01.5; BR-02/03/04; D-01/04/08.

### S-03 Issue Details

Entry: issue title C-04 або valid Create. Canonical example: **Lead non-assignee, ISS-003, Resolved, High, Member A**. Visible data: ID, повні Title/Description, current Status, current Priority, Assignee, Author, Created at; коментарі text/author/time. C-09 read-only; C-10/11/12 показують поточні значення та відповідні edit choices без зайвого дублювання. Absence: Unassigned і Not Set як display text. Controls C-10–C-19; C-13/14/15 Apply біля відповідного control. Shared control area без декоративного heading.

Canonical permissions: assignment/priority enabled; status disabled. Member contexts: assignment/priority disabled. Member assignee або Lead assignee: тільки allowed next Status; Closed і Unassigned не мають executable Status action. Вибір призначення/priority/status не вважається applied до Apply; це UX intent, а в P1 підготовлена симуляція. Source не вводить length limits, mandatory comment count, reset priority чи можливість редагувати Title/Description.

Default comment state: baseline entry + empty input. Empty submission: «Comment text is required» [DESIGN copy], baseline count незмінний. Success: text «Підтверджую виправлення у деталях документа.», Member A, 10.10.2026 10:25; додано рівно один prepared entry. Failed save: «Comment could not be saved» [DESIGN copy]; нового entry немає, baseline залишається. Це окремі states; не один суперечливий success/error screen. Closed не блокує comments чи Lead assignment/priority. T-03/04/05/06/07 залишаються S-03; T-09 Return зберігає tab. Persistence та actual server access — IMPL.

### REF-01 Review notes

Entry: огляд поза продуктовими frames, не перехід з UI. Visible data: 4 permission contexts, 4 status examples, Actor/Issue/Current status annotations, compact M-01 validation і S-03 comment validation/save-error examples. A-REF і A-COMMENT-ERROR. Показати Open, In Progress, Resolved, Closed; не 16 повних detail screens. До P1 за потреби окремі компактні приклади перетворюються на prepared detail-state copies, а notes лишаються поза UI. Матриці — документаційний доказ правил, а не evidence серверної авторизації. T-02/03/04/05/06/07/10.

## Реєстр controls

|C-ID / annotation|Label / data|Type / location|Visible/enabled conditions|Trigger|Visible result|Source/D-ID|
|---|---|---|---|---|---|---|
|C-01|All Issues|Tab / S-02|Видимий всім authenticated; active на A/C|Click|S-02-A; на zero fixture — S-02-C|AC-02.1; D-01|
|C-02|Important Issues|Tab / S-02|Видимий всім authenticated; active на B|Click|S-02-B із filtered rows того самого fixture|AC-08.1–AC-08.4; D-01|
|C-03|Create Issue|Button / S-02|Enabled authenticated Member/Lead|Click|Open overlay M-01; caller context зберігається|BR-02; D-01|
|C-04|ID / Title / Status / Priority / Assignee|Row / S-02|Усі registered на A; filtered на B; відсутні на C|Title click|S-03 того самого issue ID|AC-02.2/3; AC-05.1/3|
|C-05|Title|Text field / M-01|Enabled; required; не success якщо empty|Prepared text state; Create|Валідація Title is required якщо empty|AC-01.1/2; US-01 Gherkin|
|C-06|Description|Multiline field / M-01|Enabled; required; не success якщо empty|Prepared text state; Create|Description is required якщо empty; текст — DESIGN copy|AC-01.1/3|
|C-07|Create|Button / M-01|Enabled для спроби submit; invalid branch не веде в success|Click|Valid -> S-03 ISS-009; invalid -> відповідний modal state|AC-01.2/3/4/5; D-08|
|C-08|Cancel|Button / M-01|Enabled незалежно від required inputs|Click|Close overlay; calling list state; новий issue не створено|D-01/07|
|C-09|Issue identity and metadata|Read-only block / S-03|ID, Title, Description, Author, Created at присутні|Немає editing trigger|Читабельні значення issue; довгий title доступний повністю|AC-02.4; AC-01.4|
|C-10|Assignee|Single select / S-03|Lead enabled; Member disabled; options Member A, Member B, Lead|Choose one; C-13|Selection draft; applied value після Apply; Unassigned — display absence|US-03, AC, пункти 1–4; D-04/05/06|
|C-11|Priority|Single select / S-03|Lead enabled; Member disabled; options Low, Normal, High, Critical|Choose one; C-14|Not Set display до вибору; встановлений рівень після Apply|AC-04.1/2; BR-04/05/06; D-03/05/06|
|C-12|Status|Current value + destination select / S-03|Enabled тільки current assignee та next(status) непорожній; інакше disabled|Choose valid destination; C-15|Поточне значення не destination; allow list за BR-08.1|AC-05.2; AC-07.1–AC-07.5; BR-08.1; D-05/06|
|C-13|Apply|Button adjacent to Assignee|Enabled для Lead з обраним destination assignee; Member disabled|Click|S-03 with updated Assignee; той самий issue|US-03; D-06|
|C-14|Apply|Button adjacent to Priority|Enabled для Lead з обраним встановлюваним рівнем; Member disabled|Click|S-03 with updated Priority; без reset|AC-04.1/2; D-03/06|
|C-15|Apply|Button adjacent to Status|Enabled current assignee з дозволеним destination; Closed disabled|Click|S-03 updated Status; matching list result на Return|AC-07.3/4/5; BR-08.1; D-06|
|C-16|Comment|Multiline field / S-03|Enabled authenticated users, включно з Closed|Prepared text state|Pending text; empty не створює saved entry|AC-06.1; US-06|
|C-17|Add Comment|Button / S-03|Enabled authenticated; дозволяє показати validation branch|Click|Empty -> validation; valid -> saved або simulated save error|AC-06.1/2/5|
|C-18|Saved comments|Read-only entries / S-03|Показати text, author, created time; на error лише baseline|Немає editing/deletion action|У success на один saved entry більше; error/empty count не змінюється|AC-06.2/3/4/5|
|C-19|Return to Issues List|Navigation button / S-03|Enabled authenticated|Click|Prior S-02 All/Important; актуальний fixture branch|AC-02.3; D-07|
|A-EMPTY|No issues yet|Empty-state text / S-02-C|Видимий лише zero registered issues|Немає|0 rows; Create доступний|AC-02.5|
|A-COMMENT-ERROR|Comment could not be saved|Error text / S-03 failure|Лише failed save prepared branch|Немає|Error видимий; submitted comment не saved|AC-06.5; DESIGN error copy|
|A-REF|Review notes|Annotation / REF-01|Тільки за межами продукту|Немає product actions|Actor, issue ID, current status, permissions, transitions|M с.9–11; D-08|


## Permission Matrix — 4 contexts × 6 actions

Усі contexts передбачають authenticated user. Assignee — issue-specific. Assignment право: S1 §1 Open Questions і US-03, AC, пункт 3; не BR-06. Priority право: BR-06/AC-04.2. Status право: BR-08 + AC-07.4. View/create/comment: US-02; BR-02; US-06.

|Context|View|Create|Comment|Assign / reassign|Change priority|Change status|
|---|---|---|---|---|---|---|
|Member non-assignee|Так|Так|Так|Ні|Ні|Ні|
|Member assignee|Так|Так|Так|Ні|Ні|Так, лише BR-08.1; Closed — Ні|
|Lead non-assignee|Так|Так|Так|Так|Так|**Ні**|
|Lead assignee|Так|Так|Так|Так|Так|Так, лише BR-08.1; Closed — Ні|


No assignee: status disabled для всіх. Disabled не означає backend enforcement. Closed не змінює permissions для інших п’яти actions.

## Status Transition Matrix — BR-08.1

|From / To|Open|In Progress|Resolved|Closed|
|---|---|---|---|---|
|Open|Поточний; не дія|Дозволено|Заборонено|Заборонено|
|In Progress|Заборонено|Поточний; не дія|Дозволено|Заборонено|
|Resolved|Заборонено|Дозволено|Поточний; не дія|Дозволено|
|Closed|Заборонено|Заборонено|Заборонено|Поточний; не дія|


Enabled status = current user == current assignee AND next(status) != empty. Current status показано як value, а не option для нового переходу.

## Important predicate і еталонні records

`Important(issue) = (issue.priority in {High, Critical}) AND (issue.status != Closed)`

|ID|Status|Priority|Assignee|Important|Підстава|
|---|---|---|---|---|---|
|ISS-001|Open|Critical|Member A|Так|Critical і non-Closed|
|ISS-002|In Progress|High|Member B|Так|High і non-Closed|
|ISS-003|Resolved|High|Member A|**Так**|BR-09.1: Resolved ще не Closed|
|ISS-004|Closed|Critical|Member B|Ні|AC-08.4: Closed виключено|
|ISS-005|Open|Normal|Unassigned|Ні|AC-08.3: Normal виключено|
|ISS-006|Open|Not Set|Unassigned|Ні|DERIVED: absence не High/Critical|
|ISS-007|Resolved|Critical|Lead|**Так**|BR-09.1: Resolved ще не Closed|
|ISS-008|In Progress|Low|Member A|Ні|AC-08.3: Low виключено|


All = 8 issue. Important = 4 issue. After close ISS-003: All = 8, Important = 3. Create ISS-009 Not Set: All = 9, Important = 4 у baseline-create branch. Zero fixture success: All = 1, Important = 0. Не змішувати незалежні test branches.

## Traceability Matrix — усі 33 AC

UIR-001–UIR-033 — локальні derived requirement IDs для організації контракту. Вихідні AC-ID та посилання на ненумеровані пункти незмінні.

|Source ID / пункт|UIR-ID|Screen / State|Control / annotation|Test ID|Verification Level|
|---|---|---|---|---|---|
|AC-01.1|UIR-001|M-01|C-05, C-06|T-01|UI + SIM|
|AC-01.2|UIR-002|M-01 / missing-title|C-05, C-07|T-02|UI|
|AC-01.3|UIR-003|M-01 / missing-description|C-06, C-07|T-02|UI|
|AC-01.4|UIR-004|S-03 / new-issue|C-09|T-01|UI + SIM + IMPL|
|AC-01.5|UIR-005|S-03 / new-issue|C-11|T-01|UI + SIM|
|AC-02.1|UIR-006|S-02-A|C-01, C-04|T-09|UI + SIM + IMPL|
|AC-02.2|UIR-007|S-02-A, S-02-B|C-04|T-08, T-09|UI|
|AC-02.3|UIR-008|S-02 -> S-03|C-04|T-09|UI + SIM|
|AC-02.4|UIR-009|S-03|C-09, C-10, C-11, C-12|T-09|UI|
|AC-02.5|UIR-010|S-02-C|A-EMPTY|T-09|UI|
|US-03, AC, пункт 1|UIR-011|S-03|C-10, C-13|T-03|UI + SIM|
|US-03, AC, пункт 2|UIR-012|S-03|C-10|T-03|UI + IMPL|
|US-03, AC, пункт 3|UIR-013|S-03, REF-01 / permissions|C-10, C-13|T-03|UI + IMPL|
|US-03, AC, пункт 4|UIR-014|S-03|C-10|T-03|UI + SIM|
|AC-04.1|UIR-015|S-03|C-11|T-04|UI + IMPL|
|AC-04.2|UIR-016|S-03, REF-01 / permissions|C-11, C-14|T-04|UI + IMPL|
|AC-05.1|UIR-017|S-02, S-03|C-04, C-12|T-05, T-09|UI|
|AC-05.2|UIR-018|S-03|C-12|T-05|UI|
|AC-05.3|UIR-019|S-02-A, S-02-B|C-04|T-08|UI|
|AC-06.1|UIR-020|S-03 / comment-validation; REF-01|C-16, C-17|T-07|UI + SIM + IMPL|
|AC-06.2|UIR-021|S-03 / comment-saved|C-18|T-07|UI + SIM + IMPL|
|AC-06.3|UIR-022|S-03 / comment-saved|C-18|T-07|UI + IMPL|
|AC-06.4|UIR-023|S-03 / comment-saved|C-18|T-07|UI + IMPL|
|AC-06.5|UIR-024|S-03 / comment-save-error; REF-01|C-17, A-COMMENT-ERROR|T-07|UI + SIM + IMPL|
|AC-07.1|UIR-025|S-03 / new-issue|C-12|T-01|UI + SIM|
|AC-07.2|UIR-026|S-03, REF-01 / transitions|C-12|T-05|UI + IMPL|
|AC-07.3|UIR-027|S-03 / status-result; S-02 / updated|C-12, C-04|T-05, T-09|UI + SIM + IMPL|
|AC-07.4|UIR-028|S-03, REF-01 / permissions|C-12, C-15|T-05, T-06|UI + IMPL|
|AC-07.5|UIR-029|S-03, REF-01 / transitions|C-12|T-05|UI + IMPL|
|AC-08.1|UIR-030|S-02-B / ISS-002, ISS-003|C-02, C-04|T-08|UI + IMPL|
|AC-08.2|UIR-031|S-02-B / ISS-001, ISS-007|C-02, C-04|T-08|UI + IMPL|
|AC-08.3|UIR-032|S-02-B / exclusion ISS-005, ISS-008|C-02, C-04|T-08|UI + IMPL|
|AC-08.4|UIR-033|S-02-B / exclusion ISS-004|C-02, C-04|T-08|UI + IMPL|


## Traceability — BR, D і NFR (не додають AC)

|Source|UIR-ID|Screen / State|Control / annotation|Test|Level|
|---|---|---|---|---|---|
|BR-01|UIR-B01|S-01; authenticated S-02|A-REF|T-09|UI boundary; IMPL authentication|
|BR-02|UIR-B02|S-02 -> M-01|C-03|T-01|UI + SIM + IMPL|
|BR-03|UIR-B03|S-03 new-issue|C-12|T-01|UI + SIM|
|BR-04|UIR-B04|S-03 new-issue|C-11|T-01, T-04|UI + SIM|
|BR-05|UIR-B05|S-03 priority|C-11|T-04|UI + IMPL|
|BR-06|UIR-B06|S-03; REF-01|C-11, C-14|T-04|UI + IMPL|
|BR-07|UIR-B07|S-03; REF-01|C-12|T-05|UI + IMPL|
|BR-08|UIR-B08|S-03; REF-01|C-12, C-15|T-05, T-06|UI + IMPL|
|BR-08.1|UIR-B081|S-03; REF-01 transitions|C-12, C-15|T-05|UI + SIM + IMPL|
|BR-09|UIR-B09|S-02-B|C-02, C-04|T-08|UI + IMPL|
|BR-09.1|UIR-B091|S-02-B Resolved rows|C-04|T-08|UI + SIM|
|BR-10|UIR-B10|Усі product frames|A-REF: exclusions|T-10|UI inspection; IMPL deletion API|
|BR-11|UIR-B11|Усі product frames|A-REF: exclusions|T-10|UI inspection|


|Source|Evidence location|Tests / level|
|---|---|---|
|D-01|S-02 tabs; M-01; grayscale native layers|T-01/08/10; UI|
|D-02|S-01 neutral; demo start S-02|T-09; UI + SIM|
|D-03|S-03 Not Set absence; four options|T-04; UI|
|D-04|S-03 new Unassigned; reassign example|T-01/03; UI + SIM|
|D-05|REF-01 disabled contexts; no denied hotspot|T-03/04/06; UI + SIM|
|D-06|S-03 three adjacent Apply actions|T-03/04/05; UI + SIM|
|D-07|Return to calling All/Important|T-09; SIM|
|D-08|Sample data and prepared outcome annotation|T-01–T-10; SIM limits|
|NFR-01|No dedicated screen|IMPL timing <1 s|
|NFR-02|S-01 boundary only|IMPL authentication|
|NFR-03|No dedicated screen|IMPL HTTPS|
|NFR-04|No dedicated screen|IMPL backup + restore|


## Верифікаційні сценарії T-01–T-10

Це контракти тестів; стан перевірки нижче узагальнює докази 06/07. Детальні результати виконання наведено у протоколі P1. Усі Actor labels знаходяться у REF-01 або протоколі, а не є role switcher продукту.

### T-01 Create

- Precondition / actor: Member A; authenticated; calling S-02-A/B/C; fixture branch ізольовано.
- Action: Create Issue -> prepared valid Title/Description ISS-009 -> Create. Перевірити поля й auto values; Return у кожний calling context.
- Expected Visible Result: Лише 2 inputs у M-01. S-03 ISS-009: Open; Not Set; Unassigned; Member A; generated-time representation. All after-create включає ISS-009; Important не включає.
- Межі доказу: ID/time і save лише prepared; унікальність, реальний current user, persistence та authentication не доведені.
- Actual result / evidence: [протокол P1](07_Prototype_P1.md), відповідний T-ID; статичні докази — [Review Report](06_Review_Report_v1.0.md).
- Стан перевірки за 06/07: PASS (prepared prototype): Create з All/Important/Empty, поля ISS-009 і повернення; P-20–P-25. Backend — не перевірено.

### T-02 Validation

- Precondition / actor: Member A; M-01 missing Title, missing Description, both missing — три prepared states.
- Action: Create у кожному error branch; перевірити error labels і відсутність connection на success.
- Expected Visible Result: Title is required; Description is required; при обох пустих обидві помилки; overlay не закривається, нового issue немає.
- Межі доказу: Підготовлені states не доводять runtime validation; whitespace normalization не визначена джерелом.
- Actual result / evidence: [протокол P1](07_Prototype_P1.md), відповідний T-ID; статичні докази — [Review Report](06_Review_Report_v1.0.md).
- Стан перевірки за 06/07: PASS (prepared prototype): missing Title, missing Description та both missing; P-26–P-28. Runtime validation — не перевірено.

### T-03 Assignment

- Precondition / actor: Lead, ISS-005 Unassigned; Member A non-assignee й assignee compact negative examples.
- Action: Lead choose Member A -> Apply; reassign Member B -> Apply; оглянути disabled Member controls, без hotspots.
- Expected Visible Result: Рівно один assignee зі складу Member A/Member B/Lead; current value змінено; Member призначення недоступне.
- Межі доказу: Figma не доводить server authorization або membership validation запиту.
- Actual result / evidence: [протокол P1](07_Prototype_P1.md), відповідний T-ID; статичні докази — [Review Report](06_Review_Report_v1.0.md).
- Стан перевірки за 06/07: PASS (prepared prototype): P-29/P-30 пройдено; Apply показує одного Member A/B, попереднього assignee замінено.

### T-04 Priority

- Precondition / actor: Lead, ISS-006 Not Set; Member disabled contexts.
- Action: Відкрити four options; prepared Apply для Low, Normal, High, Critical. Перевірити Not Set absence і відсутність reset.
- Expected Visible Result: У dropdown лише 4 установлені рівні; поточний Not Set як display; Lead Apply update; Member disabled.
- Межі доказу: Немає доказу збереження, API allow-list чи заборони підробленого Member request.
- Actual result / evidence: [протокол P1](07_Prototype_P1.md), відповідний T-ID; статичні докази — [Review Report](06_Review_Report_v1.0.md).
- Стан перевірки за 06/07: PASS (prepared prototype): P-31–P-34 пройдено для Low/Normal/High/Critical. Меню й рольові обмеження перевірено окремо.

### T-05 Status

- Precondition / actor: Member A для ISS-001/003; Member B для ISS-002/004; Lead assignee для ISS-007; separate prepared states.
- Action: Перевірити 4 allowed transitions, 8 disallowed between different statuses, 4 diagonal current-value cells. Показати In Progress; after-change Return та reopen same ID.
- Expected Visible Result: Open -> In Progress; In Progress -> Resolved; Resolved -> In Progress; Resolved -> Closed. Current value не option; Closed без destination; matching list value після повернення. Невідомий Archived не пропонується.
- Межі доказу: Reopen prepared state лише імітує next view; persistence, API rejection unknown values та concurrency перевіряються реалізацією.
- Actual result / evidence: [протокол P1](07_Prototype_P1.md), відповідний T-ID; статичні докази — [Review Report](06_Review_Report_v1.0.md).
- Стан перевірки за 06/07: PASS (prepared prototype): P-35–P-41 пройдено; чотири дозволені переходи, Closed → Return → All → повторний перегляд Closed.

### T-06 Lead restriction

- Precondition / actor: Lead non-assignee; ISS-003 Resolved assigned Member A. Також Member non-assignee й Unassigned example.
- Action: Спробувати Status/Apply у Present; оглянути controls та Prototype connections.
- Expected Visible Result: Status і Apply disabled; hotspot відсутній; Resolved не змінився. Assignment/Priority Lead лишаються enabled.
- Межі доказу: Візуальна заборона не є доказом server access control.
- Actual result / evidence: [протокол P1](07_Prototype_P1.md), відповідний T-ID; статичні докази — [Review Report](06_Review_Report_v1.0.md).
- Стан перевірки за 06/07: PASS (prepared prototype): Status/Apply для Lead non-assignee disabled; Present-кліки не змінили Resolved. Додаткові рольові приклади — статичні докази.

### T-07 Comments

- Precondition / actor: Member A, ISS-003 з одним baseline comment; три ізольовані prepared branches.
- Action: Empty -> Add Comment; valid prepared text -> success; valid prepared text -> forced save-error. Перевірити Closed comment-enabled example.
- Expected Visible Result: Empty error, baseline count 1; success count 2 з text/Member A/time; failure count 1 і error. Closed не блокує comments.
- Межі доказу: Actual failed transaction, author/time persistence і storage не доведені.
- Actual result / evidence: [протокол P1](07_Prototype_P1.md), відповідний T-ID; статичні докази — [Review Report](06_Review_Report_v1.0.md).
- Стан перевірки за 06/07: PASS (prepared prototype): P-42–P-44 пройдено; validation/success/failure, entries 1/2/1, author/time, очищення input після success і retained draft після failure.

### T-08 Important

- Precondition / actor: Member або Lead; baseline із усіма 8 records; окрема after-close branch.
- Action: All -> Important; звірити всі ID, values і виключення; Member A close ISS-003 -> Return Important.
- Expected Visible Result: Baseline 001/002/003/007; 003/007 Resolved включені. Closed 004; Normal 005; unset 006; Low 008 виключені. After-close тільки 001/002/007.
- Межі доказу: Prepared filtering не доводить query correctness для довільних даних.
- Actual result / evidence: [протокол P1](07_Prototype_P1.md), відповідний T-ID; статичні докази — [Review Report](06_Review_Report_v1.0.md).
- Стан перевірки за 06/07: PASS (prepared prototype): baseline Important 001/002/003/007; P-39 підтвердив після Closed лише 001/002/007, P-40/P-41 — All і повторний перегляд.

### T-09 Navigation / empty

- Precondition / actor: Authenticated actor; start All, Important, zero All окремо.
- Action: Title 003 -> S-03 -> Return з All і Important; Create -> Cancel із кожного A/B/C; огляд zero state; valid create із zero.
- Expected Visible Result: Same issue ID і fields; Return restores tab; Cancel нічого не створює; zero state 0 rows; zero-success All 1 row.
- Межі доказу: Connections мають бути фактично пройдені; намальовані arrows не доказ. Browser history і persistence не перевірені.
- Actual result / evidence: [протокол P1](07_Prototype_P1.md), відповідний T-ID; статичні докази — [Review Report](06_Review_Report_v1.0.md).
- Стан перевірки за 06/07: PASS для описаних базових маршрутів: Title ISS-003, Return з обох tabs, Cancel A/B/C, zero-success. Повний baseline title-by-title retest не заявляється.

### T-10 Scope / layers

- Precondition / actor: Кириченко К. В.; доступ до всіх working frames/layers/connections.
- Action: Оглянути 6 canonical frames, REF-01, states, native text/layers, actual main components and instances; unsupported UI/hotspots.
- Expected Visible Result: Немає delete/attachments/AI/history/search/sort/bulk/login form/new metadata. Notes поза UI; без decorative squares; frames IDs збережено; native edits можливі.
- Межі доказу: Не доводить відсутність backend функцій, глобальну accessibility або usability для всіх користувачів.
- Actual result / evidence: [протокол P1](07_Prototype_P1.md), відповідний T-ID; статичні докази — [Review Report](06_Review_Report_v1.0.md).
- Стан перевірки за 06/07: REPRESENTATIVE UI / NATIVE CHECK VERIFIED: канонічні поверхні, reference examples, text edit/Undo, instance/main component. Повний підрахунок усіх layers/instances не проводився; прийняття результатів рецензентом наведено у 06.

## Повний негативний status checklist

Заборонено: Open -> Resolved; Open -> Closed; In Progress -> Open; In Progress -> Closed; Resolved -> Open; Closed -> Open; Closed -> In Progress; Closed -> Resolved. Не є змінами: Open -> Open; In Progress -> In Progress; Resolved -> Resolved; Closed -> Closed. Невідомий status Archived не пропонується; серверне відхилення невідомого значення залишається IMPL.

## Бізнес-рішення до генерації

UX-рішення D-01–D-08 наведено у 00_Decision_Log_v1.0.md. Ролі продукту — Team Member та Team Lead; роль Reviewer, дія Approve та окремий перевіряльник Closed до scope не входять. За D-02 механізм автентифікації залишається питанням реалізації. Зміни UX-контракту потребують узгодження та нової версії Decision Log.
