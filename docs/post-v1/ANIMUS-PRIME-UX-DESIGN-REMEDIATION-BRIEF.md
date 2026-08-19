# ANIMUS PRIME Post-V1 UX Design Remediation Brief

## Status and authority

- Directive: `D-PRIME-POSTV1-UX-REMEDIATION-BRIEF-001`
- Classification: post-V1 design analysis; implementation not authorized
- Frozen V1 posture preserved: `PRIME-SPEC-V1.0.0`, 81/81, Phase 15 complete
- Governed baseline: `a4ef39ef3353ac2c560e9a6a5e79bc9c707f6859`
- Qualified implementation/runtime: `d067a247dbeea47eb8b061111db04e7cd95bebe2`
- Public deployment and Phase 16: not authorized

This brief defines a future UX convergence initiative. It does not reopen, weaken, or reinterpret any frozen V1 acceptance result. PRIME is functionally qualified for its approved private production posture; the gap addressed here is product presentation, information architecture, and interaction quality.

## Executive finding

The current PRIME UI is functionally broad but structurally flat. Its single-page shell renders most setup, status, project, integration, lifecycle, diagnostic, and qualification controls in one continuous document. Nearly every surface uses the same bordered-panel weight, explanatory copy is frequently visible by default, and the navigation exposes the complete product taxonomy at once. The result is accurate but cognitively expensive: operators must read and scroll before they can establish project identity, health, current activity, or the next useful action.

ANIMUS ONE provides the stronger product language. Its source demonstrates compact project identity, image/icon-led recognition, contextual tabs, one active workspace surface, short status summaries, progressive disclosure, drawers/modals for secondary work, and restrained neon accents over a near-black foundation. PRIME should converge on that system without copying ANIMUS ONE blindly or hiding PRIME's essential provenance, authority, security, degraded-state, and destructive-action semantics.

The target is not a cosmetic reskin. It is a controlled information-architecture refactor:

1. reduce the global shell to product-level destinations;
2. make the selected project the dominant workspace context;
3. show one primary surface at a time;
4. summarize state with metrics, chips, short calls to action, and exception-first panels;
5. move detail into drill-downs, drawers, accordions, and evidence inspectors;
6. retain complete accessible labels, provenance, warnings, confirmations, and truthful degraded behavior.

## Source provenance

### ANIMUS PRIME

- Repository: `SketchOTP/ANIMUS_PRIME`
- Atlas checkout: `/home/sketch/Projects/ANIMUS_PRIME`
- Audited governed revision: `a4ef39ef3353ac2c560e9a6a5e79bc9c707f6859`
- Primary web source: `apps/web/index.html`
- Runtime observed: qualified private URL `https://atlas-2.tail1a5964.ts.net/`
- Browser evidence: live desktop, tablet, and narrow mobile captures from the existing private runtime

### ANIMUS ONE

- Authoritative checkout located: `/home/sketch/Projects/animus_directive`
- Git remote: `git@github.com:SketchOTP/animus-mimir.git`
- Branch at inspection: `feature/animus-one-006-cold-start`
- Git-backed baseline: `550b303221f8c6386488023fc39078a5556478d8` (`release: qualify unified Animus product experience`)
- Design lineage inspected: workspace/chat consolidation, first-use navigation, status-summary, library, and unified-product commits from `7548a4a` through `550b303`
- Current working tree: dirty before inspection; it was read-only and was not modified

The design extraction uses committed ANIMUS ONE behavior at `550b303…` and explicitly observed current working-tree refinements. The dirty working tree is not represented as a published revision. No claim in this brief depends on it being committed.

Key source files inspected:

- `apps/web/app/globals.css`
- `apps/web/components/ProjectCard.tsx`
- `apps/web/components/ProjectListClient.tsx`
- `apps/web/components/ProjectWorkspaceShell.tsx`
- `apps/web/components/ProjectLibraryClient.tsx`
- `apps/web/components/ProjectCreateForm.tsx`
- `apps/web/components/ProjectAvatarCrop.tsx`
- `apps/web/components/WorkspaceGlyph.tsx`

## Current PRIME UI architecture

PRIME's web shell is a single HTML application with a fixed 17rem desktop sidebar, anchor-based navigation, and one long main document. The live surface exposes global navigation and project navigation together:

- Global: Home, Projects, Needs Attention, Recently Active, System Health, Settings.
- Project: Overview, Ask PRIME, Search, Goal, Progress, Repository, Authority, Memory, Warm Start, Project Brain, Time Lens, Knowledge, Evidence, Activity, AI Connections, Settings.

The same document also mounts authentication/recovery, bootstrap/onboarding, Node enrollment, Notion, Nodes, Hindsight, remote access, backup, usage, project lifecycle, fork controls, diagnostics, and qualification-era controls. Responsive rules stack the content, but do not materially reduce it: the desktop page becomes an even longer tablet/mobile page, while the complete navigation remains exposed.

Current visual tokens are coherent but generic: blue-black background, blue-gray panels, Inter/system text, uniform 1px borders, and state expressed largely through copy plus colored left borders. The problem is not token quality in isolation; it is equal visual weight and simultaneous exposure across too many surfaces.

## ANIMUS ONE design language to adopt

### Verified tokens

These values are present in the inspected ANIMUS ONE source and should be the historical baseline for convergence:

| Role | ANIMUS ONE value | Intended PRIME use |
|---|---|---|
| Canvas | `#050505` | application background |
| Elevated canvas | `#0d0d0f` | sidebar, header, drawers |
| Panel | `#111116` | cards and primary modules |
| Border | `#1f1f28` | quiet structural separation |
| Text | `#e8e8ef` | primary text |
| Muted text | `#8b8b9a` | metadata and secondary labels |
| Cyan | `#00f5ff` | primary accent/focus |
| Pink | `#ff2a6d` | destructive/error |
| Green | `#39ff14` | healthy/success |
| Yellow | `#faff00` | warning/attention |
| Purple | `#bf00ff` | brand/project accent |
| Radius | `10px` | standard card radius |
| Glow | restrained 12px accent mix | selected/active/important surfaces only |

Additional verified palette colors—orange, blue, mint, magenta, teal, and coral—support project identity and categorization. They must not become an uncontrolled rainbow status system.

ANIMUS ONE currently uses `Segoe UI`, system UI, and platform sans-serif fallbacks. Any future font change is a proposal requiring separate accessibility, performance, and licensing review; it is not part of the extracted historical system.

### Verified component and interaction patterns

- Branded wordmark: uppercase, high weight, wide tracking, purple/cyan/magenta neon treatment. Motion/glitch effects are disabled under reduced-motion preferences.
- Project identity: avatar or glyph, per-project accent, concise name/summary, status chip, progress signal, and compact primary entry action.
- Workspace shell: selected project identity remains visible; a contextual tablist mounts only one primary workspace surface at a time.
- Cards: near-black panels, quiet border, 10px radius, optional restrained accent glow.
- Status: compact pills/chips backed by text labels; color is supplementary.
- Actions: concise icon buttons with accessible names; destructive operations retain explicit confirmation.
- Secondary work: drawers, dialogs, and expandable detail rather than permanently mounted forms.
- Library/data browsing: compact search, category tabs/chips, visual objects, and detail modals.
- Creation: staged form sections, visible validation, project appearance, and clear completion state.

### Rules for PRIME adoption

1. Preserve semantic labels. An icon may shorten the visual footprint, but never replace accessible text or an unambiguous tooltip/name.
2. Use glow only for current context, focus, primary action, or exceptional status. Do not glow every card or divider.
3. Never encode health, authority, freshness, or destructive risk by color alone.
4. Keep full evidence, source revision/hash, authority, and degraded-state detail available within one deliberate interaction.
5. Keep all security-negative, confirmation, step-up, refusal, and audit behaviors intact.
6. Do not merge distinct PRIME concepts merely because ANIMUS ONE has fewer destinations.

## Structural drift audit

| Surface | Current PRIME behavior | ANIMUS ONE reference | Operator impact | Target direction | Priority |
|---|---|---|---|---|---|
| Application shell | Global and project destinations appear together; most surfaces share one scroll | Compact shell plus contextual workspace tabs | Location and task hierarchy are unclear | Persistent global rail/header; selected-project subnav; one route/surface at a time | P0 |
| Home | Explanatory, setup, status, and operational blocks compete | Short focus/status summaries | Slow five-second comprehension | Health, needs attention, recent activity, and resume action above fold | P0 |
| Projects | Record-like text containers | Avatar-led compact project cards/list | Projects are difficult to recognize quickly | Visual identity, one-line summary, status, activity, two key signals, primary open action | P0 |
| Needs Attention | Embedded among many panels | Exception-first focus list | Urgency diluted by surrounding content | Ranked actionable exceptions with owner/source/age and direct resolution action | P1 |
| Recently Active | Verbose event presentation | Compact status/history summaries | Activity scanning is slow | Timeline rows with actor, verb, object, source class, relative time; expand for evidence | P1 |
| System Health | Mixed with setup/integration controls | Status chips and focused modules | Health and configuration are conflated | Health overview cards; drill into Diagnostics; setup shown only when required | P1 |
| Project Overview | Many equal-weight boxes | Persistent project identity and concise overview | No dominant project state | Project header, health, Goal alignment, progress, next action, recent evidence | P0 |
| Ask PRIME | Shares page with unrelated controls | Dedicated conversational workspace | Question/answer flow lacks focus | Dedicated Ask surface; evidence rail/drawer; concise epistemic label and citations | P1 |
| Search | Dense grouped results in long shell | Compact search and category filters | Search context is hard to scan | Full-width search, source-class chips, grouped result cards, detail drawer | P1 |
| Goal | Goal content and management controls coexist | Focused content with secondary controls hidden | Authoritative state competes with editing mechanics | Read-first Goal card; revision/approval metadata; edit/review in controlled drawer | P1 |
| Progress | Narrative status and correction controls compete | Visual status/progress signals | Alignment and next action are not glanceable | Milestone strip, alignment status, evidence freshness, challenge/correction as secondary workflow | P0 |
| Repository | Binding, status, tree/actions, diagnostics share weight | Compact object identity and staged actions | Routine reads feel administrative | Repository identity/status header; browse primary; binding/admin under manage panel | P1 |
| Authority | Dense policy text and controls | Progressive disclosure | Operators must read policy before seeing authority state | Current authority summary, grants/limits chips, provenance; editing behind review action | P1 |
| Memory | Long metadata and provider states | Library-like browse pattern | Durable knowledge feels like records | Search/filter, memory cards, provenance/freshness chips, detail inspector | P1 |
| Warm Start | Inputs, explanation, and output compete | Staged focused flow | Resume context is visually buried | Single resume card; selected sources; generated brief; provenance in expandable panel | P1 |
| Project Brain | Multiple data/status panels | Visual library/workspace pattern | Relationships are difficult to parse | Summary metrics, artifact groups, focused inspector; reserve visual graph for useful relationships | P2 |
| Time Lens | Selector and descriptive material share long page | Dedicated contextual workspace | Temporal comparison loses focus | Prominent time selector, comparison summary, changed-evidence list, details on demand | P2 |
| Knowledge | Source lifecycle and knowledge content coexist | Library tabs, shelves, detail modal | Content and source administration blur | Browse/search default; source freshness chips; manage sources in drawer | P1 |
| Evidence | Provenance-rich but visually dense | Focused object/detail pattern | Important evidence is hard to rank | Evidence list with source class, freshness, revision, confidence; immutable detail inspector | P1 |
| Activity | Long operational feed | Compact history summary | Change history requires excess reading | Filterable timeline; default concise; expandable payload/provenance | P1 |
| AI Connections | Provider state, credentials, and policy explanation visible together | Setup as deliberate secondary work | Routine workspace is exposed to configuration complexity | Provider health summary; connection/setup in protected settings flow | P2 |
| Project Settings | Multiple unrelated control families | Grouped settings and dialogs | High-risk and routine settings appear equivalent | Identity, integrations, lifecycle, danger zone; destructive actions isolated | P1 |
| Global Settings | Diagnostics/setup/usage/backup intermixed | Contextual grouped settings | Product feels like an admin console | Account/security, runtime, integrations, usage, backup, diagnostics groups | P1 |
| Authentication/setup | Recovery, bootstrap, enrollment, and normal entry share shell | Staged cold-start navigation | Setup complexity persists after onboarding | State-driven entry: login, first-use, recovery, or product; never all simultaneously | P0 |
| Narrow viewport | Same content/nav stacked into a very long page | Responsive focused surfaces | Mobile reading load expands sharply | Drawer/compact rail, sticky project header, one surface, preserved 44px targets | P0 |

## Content-density policy

### Default-visible content

Every major surface should answer, without scrolling or opening detail:

- Where am I?
- Which project or system context is active?
- Is it healthy/current?
- What changed recently?
- What needs attention?
- What is the single best next action?

Use one-line summaries, metrics, status chips, short event rows, and compact calls to action. A project card should normally contain no more than a name, one-line summary, status, last activity, one or two high-value signals, and the primary action.

### Detail on demand

Move these behind expanders, drawers, dialogs, or inspectors:

- raw identifiers and hashes;
- long descriptions and help copy;
- source/provenance payloads;
- diagnostics and configuration mechanics;
- recovery and enrollment procedures;
- secondary actions;
- advanced filters;
- completed workflow history.

### Never hide

The following must remain directly visible when relevant:

- unavailable/degraded/blocked state;
- stale/retracted source state;
- pending destructive consequence;
- current authority/permission limitation;
- missing authentication or step-up requirement;
- active project identity;
- irreversible action confirmation;
- safety refusal and recovery instruction.

## Target information architecture

```text
ANIMUS PRIME
├── Home
├── Projects
├── Attention
├── Activity
└── System
    ├── Health
    └── Settings

Selected Project
├── Overview
├── Ask
├── Work
│   ├── Goal
│   ├── Progress
│   ├── Repository
│   └── Authority
├── Knowledge
│   ├── Search
│   ├── Memory
│   ├── Knowledge Sources
│   ├── Evidence
│   ├── Brain
│   └── Time Lens
├── History
│   ├── Activity
│   └── Warm Start
└── Manage
    ├── AI Connections
    ├── Integrations
    ├── Backup
    └── Project Settings
```

This grouping changes navigation presentation, not domain semantics or authorization boundaries. Deep links must remain stable or receive explicit compatibility redirects. The global shell must never imply that system configuration belongs to the selected project's evidence state.

### Target shell

```text
┌──────────────┬────────────────────────────────────────────────────────┐
│ ANIMUS PRIME │ Project icon + name    health   activity   user       │
│              ├────────────────────────────────────────────────────────┤
│ Home         │ Overview  Ask  Work  Knowledge  History  Manage       │
│ Projects     ├────────────────────────────────────────────────────────┤
│ Attention    │                                                        │
│ Activity     │              ONE ACTIVE PRIMARY SURFACE                │
│ System       │                                                        │
│              │                                    optional inspector  │
└──────────────┴────────────────────────────────────────────────────────┘
```

Desktop uses a compact rail or collapsible sidebar. Tablet converts secondary project navigation to a scrollable tab row. Mobile uses a concise app bar and navigation drawer; the selected project and active surface remain visible. Inspectors become bottom sheets or full-screen dialogs where necessary.

## Five-second Home contract

Within five seconds, a returning operator should be able to identify:

1. current system health;
2. highest-priority attention item;
3. most recently active project;
4. that project's current Goal/progress state;
5. the primary resume/open action.

The default Home view should contain:

- a compact health strip;
- Needs Attention count and top three actionable items;
- recent project cards;
- one Resume Work card;
- recent activity preview.

Setup, enrollment, integration, backup, provider, and diagnostic forms appear only when state requires them or when the operator enters the relevant management surface.

## Projects contract

Each project card/list row should prioritize:

- recognizable avatar/glyph and project accent;
- project name;
- one-line summary;
- status/health chip;
- last meaningful activity;
- Goal alignment or progress signal;
- attention count when nonzero;
- primary Open/Resume action;
- compact overflow menu for edit, refresh, fork, lifecycle, and other secondary actions.

Project identity is functional, not decoration: colors and glyphs improve recognition but never replace the project name or ID in confirmations and authority-sensitive contexts.

## State and semantics preservation

The redesign must preserve every qualified state, including:

- loading, empty, unavailable, degraded, offline, stale, retracted, conflict, blocked, unauthorized, and error;
- source class, revision, content hash, freshness, citation, and authority classification;
- Node identity and repository binding;
- Notion managed/user-content boundaries;
- Hindsight derived/non-authoritative classification;
- provider availability and truthful cost limitations;
- durable workflow interruption/resume and idempotency;
- project lifecycle, fork, rebind, delete, and purge distinctions;
- step-up authentication, CSRF protection, preflight freshness, target identity, confirmation, audit, and no-mutation guarantees.

Compact presentation must not turn truthful degraded behavior into ambiguous absence. A collapsed panel that contains an active blocker must surface that blocker in its parent summary.

## Accessibility and motion requirements

- Preserve logical heading structure, landmarks, form labels, descriptions, and error associations.
- Every icon-only control requires an accessible name and visible tooltip or equivalent discoverability.
- Critical flows must remain keyboard-complete with clearly visible focus.
- Maintain minimum 44px touch targets on narrow viewports.
- Do not rely on hover for essential information or action discovery.
- Maintain WCAG AA contrast for text and meaningful non-text UI; test neon colors on actual dark surfaces rather than assuming contrast.
- Respect `prefers-reduced-motion`; disable glitch, flicker, animated glow, parallax, and nonessential transitions.
- Preserve zoom/reflow at 200% and a usable 320px-wide layout without horizontal content loss.
- Announce asynchronous state and validation changes appropriately; avoid excessive live-region chatter.
- Charts, progress rings, and color-coded status require textual equivalents.

## What must not be copied from ANIMUS ONE

- Fewer conceptual destinations do not justify collapsing PRIME's distinct security, authority, source, or lifecycle contracts.
- Decorative glitch effects must not impair reading, focus, or reduced-motion users.
- Icon-led navigation must not become icon-only ambiguity.
- Project avatars and neon accents must not obscure exact identity in destructive or authority-sensitive operations.
- ANIMUS ONE's current working-tree changes are reference evidence, not an unreviewed dependency or code source.
- PRIME must not acquire a shared runtime dependency on ANIMUS ONE merely to share visual language. Any future shared package requires separate architectural authority.

## Implementation waves

No wave below is authorized by this brief. Each requires an explicit post-V1 implementation directive, bounded acceptance, qualified runtime provenance, regression, browser evidence, and publication.

### Wave A — foundation and route-safe shell (P0, medium-high)

Scope:

- introduce design tokens and reusable primitives inside PRIME;
- build global shell, selected-project header, contextual project navigation, drawers/dialogs, status chips, icon buttons, and responsive navigation;
- render one primary surface at a time while preserving existing API behavior and deep-link compatibility;
- state-drive authentication, first-use, recovery, and normal product entry.

Dependencies: route/state inventory, stable surface IDs, accessibility baseline, screenshot baselines.

Risks: hidden qualified controls, broken anchor/deep links, state loss during navigation, reduced diagnostic visibility.

Browser validation: protected entry, login/logout, refresh, invalid route, desktop/tablet/mobile navigation, keyboard traversal, focus restoration, reduced motion, existing project persistence.

### Wave B — Home and Projects convergence (P0, medium)

Scope:

- implement five-second Home contract;
- convert project presentation to avatar/glyph-led cards/list rows;
- surface health, attention, activity, Goal alignment, and Resume action;
- move setup and secondary project actions behind state-driven panels/menus.

Dependencies: Wave A primitives; reliable project summaries and attention counts.

Risks: oversimplified status, hidden degraded conditions, project identity ambiguity.

Browser validation: empty/single/many projects, long names, missing avatar, degraded project, attention state, recent activity, narrow viewport, keyboard/card action semantics.

### Wave C — core project workspaces (P0/P1, high)

Scope:

- Overview, Progress, Goal, Repository, Authority, Ask, and Search;
- evidence/freshness inspector shared by grounded surfaces;
- correction/challenge and managed actions as focused secondary workflows.

Dependencies: Waves A-B; shared provenance component; stable status vocabulary.

Risks: loss of citation detail, misleading summarized progress, accidental authority-edit affordance, Ask/Search epistemic dilution.

Browser validation: current/stale/retracted sources, UNKNOWN Ask, citations and source classes, Progress correction challenge, Goal approval/reversal, repository online/offline, authority review, isolation.

### Wave D — knowledge, history, and resume surfaces (P1/P2, high)

Scope:

- Memory, Knowledge Sources, Evidence, Brain, Time Lens, Activity, and Warm Start;
- library/timeline patterns; filter chips; visual object identity; detail inspector;
- preserve derived/non-authoritative and historical/current distinctions.

Dependencies: Wave C provenance inspector; representative data states.

Risks: collapsing history into current truth, hiding freshness, visual graph without operator value, heavy rendering on large datasets.

Browser validation: source lifecycle, detach/retract, durable memory provenance, activity persistence, historical comparison, restart, large result sets, no-result states, keyboard filters.

### Wave E — management, diagnostics, and full-product polish (P1/P2, high)

Scope:

- AI Connections, integrations, usage, backup, Node enrollment, remote access, global/project settings, Diagnostics, lifecycle, fork/rebind/delete/purge;
- consistent dialogs, danger zones, status summaries, recovery guidance, and final responsive polish.

Dependencies: all prior waves; qualified destructive fixtures/targets where needed.

Risks: weakened safety disclosure, hidden unavailable provider state, accidental public/network affordance, regression in complex durable workflows.

Browser validation: security-negative matrix, confirmation/cancel/focus, step-up, stale preflight, wrong target, CSRF, audit/no mutation, offline Node, private route, provider degradation, backup refusal/recovery, lifecycle/fork/rebind/destruction, service restart.

## Future implementation acceptance criteria

A future redesign is complete only when all of the following pass:

### Structure and hierarchy

- Only one primary product surface is mounted/visible at a time in normal operation.
- Global and selected-project navigation are visually and semantically distinct.
- Home satisfies the five-second contract in moderated or scripted evaluation.
- Project cards meet the concise identity/status/action contract.
- No default screen exposes setup or destructive controls unrelated to its current state/task.

### Visual system

- Extracted palette, border, radius, status, icon-button, and restrained-glow rules are consistently applied.
- Selected/active/exceptional states are visually distinct; ordinary containers remain quiet.
- No essential state uses color alone.
- Typography and spacing tokens are documented and mechanically reused rather than page-local values.

### Content density

- Default cards use concise summaries rather than paragraph explanations.
- Long help, identifiers, provenance payloads, diagnostics, and secondary controls use progressive disclosure.
- Active blockers, degraded states, stale/retracted evidence, and destructive consequences remain visible without hunting.

### Product behavior

- Existing protected routes, session behavior, deep links or redirects, project selection, and restart recovery pass.
- All 81 frozen V1 capabilities remain behaviorally intact; no redesign acceptance may be traded against a frozen requirement.
- Full supported regression remains green and skip changes are explained.
- Persistent runtime is rebuilt from the exact qualified implementation and retains database, Hindsight, Nodes, projects, and source state.

### Browser and accessibility

- Desktop, tablet, 320px mobile, 200% zoom, keyboard-only, visible focus, and reduced-motion checks pass.
- Critical flows have no inaccessible icon-only action, focus trap failure, hidden error, hover-only instruction, or horizontal-loss defect.
- Automated checks are supplemented by real browser review of hierarchy, clipping, state transitions, and destructive confirmations.

### Governance

- Each implementation wave names the exact design acceptance it closes.
- Product/runtime changes receive a qualified implementation SHA and runtime-build provenance.
- GitHub, `.agent`, evidence, and the main Notion SOT agree at each bounded closeout.
- No public exposure, Funnel, Phase 16, or unrelated architecture is inferred from UX authority.

## Recommended first implementation directive

Authorize only Wave A plus the minimum Home/Projects slice needed to prove the shell. The first implementation should not attempt all screens. Its bounded objective should be:

> Establish the ANIMUS ONE-derived PRIME design foundation and route-safe shell; separate global and selected-project navigation; mount one primary surface at a time; implement the five-second Home and concise Projects cards; preserve every existing backend/API contract, qualified state, accessibility behavior, deep link, and private runtime boundary.

Stop after that slice is rebuilt and qualified in the persistent private runtime. Use the result to refine—not automatically authorize—the remaining waves.

## Validation of this brief

- Current governed baseline and Git parity: verified before analysis.
- PRIME source architecture and current private UI: inspected read-only.
- Desktop/tablet/mobile current layout: captured and reviewed read-only.
- ANIMUS ONE source, Git provenance, component patterns, and design tokens: inspected read-only.
- PRIME application/runtime/database/network changes: none.
- ANIMUS ONE changes: none.
- Phase 16 / Continuation 097 / deployment / public exposure: none.

This document is the canonical post-V1 UX remediation brief. It authorizes no implementation by itself.
