# Mini Issue Tracker — low-fidelity design brief v1.1

## Purpose and scope

Internal desktop web issue tracker for one small team. Include US-01–US-08 only: create, view, assign, prioritize, track status, comment and view important non-closed issues. Release scope comes from S1 §8, not the earlier Candidate MVP. Deferred: US-09. Future: SR-10 and SR-11. The source has no US-10 or US-11. Use three fictional users: Member A, Member B and Lead. Member A and Member B are Team Members; Lead is Team Lead. Assignee is an issue-specific relationship, not a separate system role.

## Design basis

Decision Log records the design choices used in the mockup separately from source requirements. Document verification is complete. The current D-01–D-08 decisions and plan are approved by the reviewer; see Decision Log and Plan Review.

Design contract v1.0, 10 October 2026. Source: S1 sections 1, 3, 5 and 8. D-01–D-08 follow the methodological guide, section 6: desktop grayscale low-fi; tabs and modal Create; neutral authentication boundary; absent priority; initial unassignment/reassignment; disabled controls; adjacent Apply; restored list context; static prepared outcomes. These are recorded design decisions, separate from source acceptance criteria.

## Design and output constraints

Create editable native Figma layers on one page. Grayscale, low-fidelity, readable hierarchy, meaningful layer names, reusable local controls and rows, Auto Layout where practical. Preserve Screen IDs in frame names. Create six canonical frames: S-01, S-02-A, S-02-B, S-02-C, M-01, S-03. M-01 is an overlay surface. S-02-A/B/C are states of one list screen. Add one service Section REF-01 outside all product frames, with compact state examples. This is not a request for sixteen complete detail screens. Additional prepared state frames may be created later manually for testing without adding product screens.

Reviewer notes, actor labels and source references stay OUTSIDE product frames in REF-01. No decorative page icons or empty square placeholders. Do not duplicate editable and read-only representations of the same field unnecessarily. A long issue Title must be fully readable in details even if the list presentation is compact. Use the control IDs below in layer names. Prototype navigation is annotated only: do not wire interactions or implement an application.

## S-01 — Authentication boundary [BR-01; NFR-02; D-02]

A neutral boundary block with the application name and the exact label “Authentication entry — mechanism TBD”. No login method, password fields, SSO buttons or social-login controls. This is not working authentication. The demo starts from S-02 as an already authenticated user. Do not provide an interaction that claims to authenticate a user.

## S-02 — Issues List [US-02; US-05; US-08; D-01]

Header: Issues List and Create Issue action C-03. Tabs: All Issues C-01 / Important Issues C-02. Rows C-04 show ID, Title, Status, Priority and Assignee if assigned. Unassigned is an empty-value display label. Title opens the corresponding issue details. No row-selection checkboxes.

Show S-02-A All Issues, S-02-B Important Issues and S-02-C Empty All Issues. They are states of ONE product screen and may use separate frames. S-02-A has all eight baseline rows below. S-02-B has only ISS-001, ISS-002, ISS-003 and ISS-007. S-02-C has zero registered issues, no rows, “No issues yet”, the tabs and Create Issue. Empty Important on a nonempty collection is a different situation and does not replace S-02-C.

Important = (priority is High or Critical) AND status != Closed. Resolved High/Critical issues stay included. Low, Normal, unset priority and every Closed issue are excluded. Reuse the same issue IDs and values across list states. After the prepared ISS-003 Resolved -> Closed demonstration, Important contains ISS-001, ISS-002 and ISS-007 only; All still contains ISS-003 with Closed status.

### Baseline sample data

Status, priority and assignee follow the methodological fixture. Titles, descriptions, authors and times are fictional display data. Times use Europe/Kyiv, 10 October 2026. Keep the same values in list and details for each ID.

| ID | Title | Status | Priority | Assignee | Author | Created at |
|---|---|---|---|---|---|---|
| ISS-001 | Помилка входу після оновлення | Open | Critical | Member A | Member B | 10.10.2026 09:00 |
| ISS-002 | Зависання під час відкриття звіту | In Progress | High | Member B | Member A | 10.10.2026 09:10 |
| ISS-003 | Некоректне відображення дати | Resolved | High | Member A | Member B | 10.10.2026 09:20 |
| ISS-004 | Недоступність експорту | Closed | Critical | Member B | Lead | 10.10.2026 09:30 |
| ISS-005 | Відступи у повідомленні | Open | Normal | Unassigned | Member A | 10.10.2026 09:40 |
| ISS-006 | Нечіткий текст підказки | Open | Not Set | Unassigned | Member B | 10.10.2026 09:50 |
| ISS-007 | Помилка завантаження документа | Resolved | Critical | Lead | Member A | 10.10.2026 10:00 |
| ISS-008 | Обрізаний текст кнопки | In Progress | Low | Member A | Lead | 10.10.2026 10:10 |

Descriptions for details:

- ISS-001: Після введення коректних даних користувач не потрапляє до застосунку.
- ISS-002: Відкриття звіту зупиняє взаємодію з інтерфейсом.
- ISS-003: У деталях документа дата відображалась у неправильному форматі.
- ISS-004: Експорт документа був недоступний; виправлення закрито.
- ISS-005: Текст повідомлення має нерівномірні відступи.
- ISS-006: Підказка у формі містить незрозуміле формулювання.
- ISS-007: Завантаження документа завершувалось помилкою; виправлення очікує закриття.
- ISS-008: Назва кнопки обрізається на десктопному екрані.

## M-01 — Create Issue overlay [US-01; D-01/04]

Inputs: Title C-05, required; Description C-06, required multiline. Actions: Create C-07 and Cancel C-08. Only these two issue fields are editable here.

After success: generated ID, Open status, absent priority shown as Not Set, unassigned assignee, current authenticated author and generated creation time. Do not expose these defaults as inputs. Show default, prepared valid input, missing-Title, missing-Description and both-missing examples. Invalid submission does not create an issue or navigate to success. Preserve the source example “Title is required”. Working design copy for Description: “Description is required”. This copy is a design choice, not an additional source criterion.

Prepared Create result: ISS-009; Title “Помилка збереження налаштувань”; Description “Після підтвердження налаштування не відображаються повторно.”; Open; Not Set; Unassigned; Author Member A; Created at 10.10.2026 10:20. The prepared ID and time represent automatic fields; they are not actual generated or stored values.

## S-03 — Issue Details [US-02–US-07]

Show ID, Title, Description, Status, Priority, Assignee, Author and Created at. Unassigned/Not Set are empty-value display states, not extra metadata. Read-only identity and metadata: C-09. Return to Issues List: C-19.

Keep Assignee C-10, Priority C-11 and Status C-12 controls together without a decorative “Control Actions Area” heading. Apply buttons: C-13 adjacent to Assignee, C-14 adjacent to Priority, C-15 adjacent to Status. Canonical example: Lead viewing ISS-003 assigned to Member A; assignment and priority enabled, status disabled.

Only Lead can assign/reassign one team member and set/change priority [US-03; AC-04.2; BR-06; D-04]. Assignee choices: Member A, Member B and Lead. Member controls are disabled [D-05]. Unassigned is an initial absence display, not a new team member or an unassignment action. Selection is applied with the adjacent Apply; visible success remains on S-03 [D-06].

Priority display states: Not Set, Low, Normal, High, Critical. Selectable levels: Low, Normal, High, Critical ONLY. Not Set represents absence; it is not a selectable level or reset action [BR-04/05; D-03].

Only the current assignee can change status, including for Lead [AC-07.4; BR-08]. Allowed destinations only:

- Open -> In Progress.
- In Progress -> Resolved.
- Resolved -> In Progress.
- Resolved -> Closed.

In Closed there is no next-status action. Show current status but do not offer it as a new transition. No assignee means nobody can change status before assignment. Resolved is resolved but not closed [BR-09.1]. Do not infer that Closed disables comments, assignment or priority changes.

### Permission reference

All contexts below are already authenticated. This matrix belongs outside product UI.

| Context | View | Create | Comment | Assign | Change priority | Change status |
|---|---|---|---|---|---|---|
| Member non-assignee | Yes | Yes | Yes | No | No | No |
| Member assignee | Yes | Yes | Yes | No | No | Allowed destinations only; none in Closed |
| Lead non-assignee | Yes | Yes | Yes | Yes | Yes | No |
| Lead assignee | Yes | Yes | Yes | Yes | Yes | Allowed destinations only; none in Closed |

### Comments [AC-06.1–AC-06.5]

Comment input C-16; Add Comment C-17; saved entries C-18 with text, author and creation date/time. Baseline ISS-003 entry: “Перевірено формат дати на тестовому прикладі.”; Member B; 10.10.2026 10:15.

Include separate ready, empty-validation, saved-success and save-failure examples. Empty submission shows “Comment text is required” and creates nothing. Success adds “Підтверджую виправлення у деталях документа.”; Member A; 10.10.2026 10:25. Save failure shows “Comment could not be saved” and does not add the submitted comment; the baseline entry remains. Validation/error copy other than the specified Title example is working design copy. A rendered saved entry is not proof of persistence.

## REF-01 — state reference outside product frames

Show all four contexts: Member non-assignee; Member assignee; Lead non-assignee; Lead assignee. Represent assignment/priority/status availability for each. Also show all four current-status examples, including In Progress, with valid destinations only. Show Closed with no destination and an unassigned example with disabled status. Include the required Create validation and comment validation/failure examples.

Use compact components or annotated examples. Annotations specify the test actor, issue ID and current status; they are not product controls or a role-switcher feature. Show a complete 4x4 transition matrix: the four listed directed transitions are allowed; the eight other transitions between different statuses are forbidden; diagonal cells are the current value and are not actions.

## Navigation intent [D-01/02/07/08]

S-02 tabs switch list states; issue Title opens its S-03; Create Issue opens M-01; Cancel closes the overlay to the calling list state; successful Create shows the prepared new-issue S-03; Return restores the prior list tab. Assignment, priority, status and comments remain on S-03 after success. Invalid operations do not show a success state. These are design intentions and prepared outcomes, not working persistence. Annotate intended transitions outside product UI; students will connect them manually later.

## Exclusions

No title/description editing after creation, deletion, attachments, AI features, dashboards, analytics, notifications, search, sorting, pagination, user administration, user-visible history, extra issue metadata, multi-assignee, extra status/priority values or transitions, invented login method, row-selection, bulk actions, branding or decorative imagery. No separate product screens for assignment, priority, status, comments or Important Issues. Do not add a Reviewer role, an Approve action or a user-facing role switcher.

## Acceptance checklist

- Six canonical frames with exact IDs and a separate REF-01 section exist on one page.
- Native text, fields, buttons and rows are editable; reported reusable controls are actual local components.
- All baseline rows match across views; Important has exactly 001/002/003/007.
- Create has only Title/Description; required-field examples and automatic-result representation exist.
- Details shows all eight source fields; shared controls and adjacent Apply buttons are present.
- Four permission contexts and four current-status examples are represented; Lead non-assignee status is disabled.
- Only the four allowed directed status transitions are offered; Closed has none.
- Not Set is absent priority, not an option/reset; only four levels are selectable.
- Comment ready, validation, success and failed-save states show correct entries and counts.
- Notes stay outside product frames; unsupported functions and decorative square placeholders are absent.
- Navigation is annotated, with no Agent-built prototype or backend claims.

## Completion report instructions

In the same Agent response report actual created frames/state references, actual reusable local components, unrepresented rules/states and assumptions or limitations. List NOT REPRESENTED and UNRESOLVED explicitly, even if none were found. State uncertainty instead of claiming full compliance. A static wireframe does not prove authentication, server permissions, saved data, actual response time, HTTPS or backup. Do not export files or perform additional redesign after reporting.
