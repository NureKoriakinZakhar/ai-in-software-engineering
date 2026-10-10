# 04 Plan Review v1.1 — G4 / контроль B

Дата: 10.10.2026. Метод: звірка S1, методичних рекомендацій та документів 00–03. Використані інструменти — у 09. Документальний висновок: PLAN READY. Рішення рецензента B: APPROVED; підтвердження передано Корякіним З. П. 10.10.2026.

## Coverage Matrix — 33 AC

COVERED означає, що вимога повністю описана планом; це не доказ виконання дизайну чи реалізації.

|Source AC / пункт|Status|Доказ у плані|Тест|
|---|---|---|---|
|AC-01.1|COVERED|03: UIR-001; M-01; C-05, C-06|T-01|
|AC-01.2|COVERED|03: UIR-002; M-01 / missing-title; C-05, C-07|T-02|
|AC-01.3|COVERED|03: UIR-003; M-01 / missing-description; C-06, C-07|T-02|
|AC-01.4|COVERED|03: UIR-004; S-03 / new-issue; C-09|T-01|
|AC-01.5|COVERED|03: UIR-005; S-03 / new-issue; C-11|T-01|
|AC-02.1|COVERED|03: UIR-006; S-02-A; C-01, C-04|T-09|
|AC-02.2|COVERED|03: UIR-007; S-02-A, S-02-B; C-04|T-08, T-09|
|AC-02.3|COVERED|03: UIR-008; S-02 -> S-03; C-04|T-09|
|AC-02.4|COVERED|03: UIR-009; S-03; C-09, C-10, C-11, C-12|T-09|
|AC-02.5|COVERED|03: UIR-010; S-02-C; A-EMPTY|T-09|
|US-03, AC, пункт 1|COVERED|03: UIR-011; S-03; C-10, C-13|T-03|
|US-03, AC, пункт 2|COVERED|03: UIR-012; S-03; C-10|T-03|
|US-03, AC, пункт 3|COVERED|03: UIR-013; S-03, REF-01 / permissions; C-10, C-13|T-03|
|US-03, AC, пункт 4|COVERED|03: UIR-014; S-03; C-10|T-03|
|AC-04.1|COVERED|03: UIR-015; S-03; C-11|T-04|
|AC-04.2|COVERED|03: UIR-016; S-03, REF-01 / permissions; C-11, C-14|T-04|
|AC-05.1|COVERED|03: UIR-017; S-02, S-03; C-04, C-12|T-05, T-09|
|AC-05.2|COVERED|03: UIR-018; S-03; C-12|T-05|
|AC-05.3|COVERED|03: UIR-019; S-02-A, S-02-B; C-04|T-08|
|AC-06.1|COVERED|03: UIR-020; S-03 / comment-validation; REF-01; C-16, C-17|T-07|
|AC-06.2|COVERED|03: UIR-021; S-03 / comment-saved; C-18|T-07|
|AC-06.3|COVERED|03: UIR-022; S-03 / comment-saved; C-18|T-07|
|AC-06.4|COVERED|03: UIR-023; S-03 / comment-saved; C-18|T-07|
|AC-06.5|COVERED|03: UIR-024; S-03 / comment-save-error; REF-01; C-17, A-COMMENT-ERROR|T-07|
|AC-07.1|COVERED|03: UIR-025; S-03 / new-issue; C-12|T-01|
|AC-07.2|COVERED|03: UIR-026; S-03, REF-01 / transitions; C-12|T-05|
|AC-07.3|COVERED|03: UIR-027; S-03 / status-result; S-02 / updated; C-12, C-04|T-05, T-09|
|AC-07.4|COVERED|03: UIR-028; S-03, REF-01 / permissions; C-12, C-15|T-05, T-06|
|AC-07.5|COVERED|03: UIR-029; S-03, REF-01 / transitions; C-12|T-05|
|AC-08.1|COVERED|03: UIR-030; S-02-B / ISS-002, ISS-003; C-02, C-04|T-08|
|AC-08.2|COVERED|03: UIR-031; S-02-B / ISS-001, ISS-007; C-02, C-04|T-08|
|AC-08.3|COVERED|03: UIR-032; S-02-B / exclusion ISS-005, ISS-008; C-02, C-04|T-08|
|AC-08.4|COVERED|03: UIR-033; S-02-B / exclusion ISS-004; C-02, C-04|T-08|


## Реєстр перевірених ризиків плану

Перевірено три граничні випадки плану. Окремо наведено усунену невідповідність документації.

|ID / клас|Source|Місце|Ризик і перевірка|Мінімальна правка при виявленні|Фактичний результат|
|---|---|---|---|---|---|
|CHECK-P01|AC-07.4|03, права S-03|Lead non-assignee не має права змінювати status|Disabled Status/Apply; прибрати hotspot|PASS: матриця і приклад правильно блокують дію|
|CHECK-P02|AC-04.1; BR-04/05|03, Priority|Not Set не входить до selectable options|Залишити Low/Normal/High/Critical; Not Set лише absence|PASS: правило правильно описано|
|CHECK-P03|AC-01.3|03, M-01|Порожній Description не веде до success|Додати required/error state|PASS: missing-description state та маршрут є у 07|
|DEF-P04 / процедурний Major|M с.12/27|00/01/04/06/09|AI-рекомендація була позначена як людський APPROVED|Розділити VERIFIED/RECOMMENDED і особисте рішення; додати поля A–D|Документацію виправлено; прийняття поточної редакції згодом підтверджено|

## Результат звірки поточного плану

33 AC мають source/control/test; 13 UI-relevant BR мають traceability. Матриця прав правильно відокремлює Lead від assignee. Статусна матриця містить 4 дозволені transitions; Closed terminal. Important включає ISS-003 та ISS-007. Create тільки Title/Description; errors comments розділені; Scope не відновлює US-09/Future. NFR не перетворено на продуктові екрани.

## Q і умови переходу

Q-01 authentication mechanism unresolved для реалізації, не для статичного дизайну за D-02. Q-02–Q-05 врегульовано D-03–D-08 для дизайну; рішення зафіксовані у Decision Log. Змістових блокерів статичного дизайну не виявлено. Рецензент прийняв поточний план; підтвердження внесено 10.10.2026. Це дата прийняття поточної редакції, а не доказ погодження до першої генерації.

**Документальний вердикт: PLAN READY.** Остаточне рішення розробника — окремий контроль B; поточний статус APPROVED. Контроль C описано у 06.

## Поля фактичного контролю B

- Reviewer: Кириченко К. В.; прийняття поточного плану підтверджено через Корякіна З. П.
- Метод попередньої перевірки: звірка документів; інструменти описано у 09.
- Date документальної звірки: 10.10.2026; Date запису підтвердження: 10.10.2026.
- Versions для особистого review: 00/01 v1.1; 02/03 — поточна редакція з уточненим статусом.
- Рекомендовані decisions: D-01–D-08; Accepted: D-01–D-08; Rejected: немає.
- Open blockers: продуктових суперечностей у плані не виявлено.
- Verdict документальної звірки: PLAN READY; Verdict рецензента: APPROVED.
- Evidence: 33/33 Source Check; 33-row coverage; permissions/transitions/Important у 03; actual interaction record у 09.
- Limit: Цей документ стосується плану; результати перевірки Figma — у 06/07, реалізації — поза межами роботи.

## Перевірений чек-лист документації

1. Зіставлено 33 AC з S1 §5 і coverage.
2. Перевірено, що Lead non-assignee не змінює status.
3. Звірено 4 allowed/8 disallowed transitions та Closed.
4. Перевірено ISS-003/007 у Important, ISS-004/006 поза ним.
5. Перевірено missing-description та failed-comment state.
6. D-ID та спосіб погодження записано у 00/09.

## Висновок Кириченка К. В.

Поточний план приймаю. Покриття 33 AC, матриці прав і статусів, required Title/Description та склад Important Issues узгоджені. Приймаю рішення D-01–D-08 і результати перевірки граничних сценаріїв. Вердикт: PLAN APPROVED. Дата запису підтвердження: 10.10.2026; підтвердження передано Корякіним З. П.
