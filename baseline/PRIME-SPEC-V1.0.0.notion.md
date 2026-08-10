Here is the result of "view" for the Page with URL https://app.notion.com/p/3b8833cb27ff81aa8ba4c4e1dde0f273 as of 2026-08-10T15:47:00.625Z:
<page url="https://app.notion.com/p/3b8833cb27ff81aa8ba4c4e1dde0f273" icon="⚡">
<ancestor-path>
<parent-page url="https://app.notion.com/p/3b3833cb27ff8098932bfb1ffe9b49c5" title="Animus Machinae"/>
</ancestor-path>
<properties>
{"title":"ANIMUS PRIME"}
</properties>
<content>
<callout icon="🔒" color="purple_bg">
	**ANIMUS PRIME — PLANNING COMPLETE / IMPLEMENTATION AUTHORIZED**
	The operator froze the ANIMUS PRIME product and engineering plan on August 10, 2026 at 11:41 AM America/New_York (`2026-08-10T15:41:00Z`). The approved implementation baseline revision is **`PRIME-SPEC-V1.0.0`**. Phase 0 is authorized to materialize and hash the immutable specification export and `authority-template/v1` artifact, qualify exact dependency pins, establish the implementation Git baseline, and then proceed through §24A only after Phase 0 passes. Normative changes now require the SpecChangeRecord/new-baseline process.
</callout>
**Document status:** PLANNING COMPLETE — implementation authorized through §24A Phase 0–15  
**Approved spec revision:** `PRIME-SPEC-V1.0.0`  
**Freeze timestamp:** `2026-08-10T11:41:00-04:00` / `2026-08-10T15:41:00Z`  
**Implementation handoff:** <mention-page url="https://app.notion.com/p/3b8833cb27ff81d89229d461867ca547">ANIMUS PRIME — Implementation Handoff Record — PRIME-SPEC-V1.0.0</mention-page>  
**Product:** ANIMUS PRIME  
**Architecture posture:** Clean-sheet implementation  
**Primary user:** Exactly one trusted operator; local access plus private Tailscale tailnet remote access  
**Core principle:** **The AI coder does the engineering. PRIME preserves the project.**
<table_of_contents/>
---
# 1. Product Definition
## 1.1 What ANIMUS PRIME is
ANIMUS PRIME is a **local-first, integrated, visual project continuity and intelligence layer for repository-backed AI-assisted software and technical engineering projects**. Every managed PRIME project has exactly one primary Git repository as its required project container; repo-less project mode is intentionally unsupported.
It gives every managed project:
- a permanent identity, name, image, machine, and repository path;
- standardized `.agent` authority files and a complete `PROJECT_GOAL.md`;
- a read-only view of the repository and project authority state;
- an explainable, evidence-backed estimate of progress toward the project goal;
- a dedicated human-readable Notion project record that PRIME maintains automatically while preserving user-authored content;
- durable, project-isolated long-term agent memory;
- an MCP interface that an AI coding agent such as Codex can call to store, retrieve, and compile relevant project memory and context;
- an interactive, project-scoped 3D Project Brain visualization that renders repository structure and relationships as an explorable neural-style graph without influencing memory or reasoning;
- event-driven monitoring so the project can remain understandable across days, months, AI sessions, and different coding agents;
- a project-specific **Ask PRIME** experience for source-grounded questions about the current project;
- a daily operator experience built around **Since You Were Here**, **Needs Attention**, project integrity, alignment, milestones, progress history, and completion review;
- unified project search across repository, `.agent`, Git, Notion knowledge, memory, and activity;
- explicit AI-coder connection management, project-context export, and branch/worktree awareness so PRIME remains useful across coding tools and parallel agent work;
- secure remote operator access through a supported **Tailscale-only private tailnet path**, without publicly exposing PRIME;
- a read-only **Time Lens** that reconstructs the project as it was at a selected commit/time/assessment and can replay historical Project Brain structure where evidence exists;
- a protected **Fork / Clone Project** workflow that creates a fully isolated new project from a selected canonical Git revision without sharing live memory, authority, credentials, progress, or Notion state.
ANIMUS PRIME is **not the coding agent**. Codex or another AI coding system remains responsible for reasoning about implementation, editing code, running tests, fixing defects, and performing engineering work.
PRIME exists because coding sessions are temporary while projects are persistent.
## 1.2 The problem PRIME solves
Modern AI coding agents are very capable at reading a repository and doing work in the current session. The persistent problems are different:
- project setup and authority are repeatedly recreated by hand;
- repository location and identity are fragmented across machines;
- project goals and rules can become inconsistent or difficult to inspect;
- an AI agent may need to reconstruct months of history to understand *why* the code is the way it is;
- failed approaches, decisions, operator observations, environment quirks, and validation lessons are easy to lose;
- human-readable documentation drifts away from the live project;
- progress toward the actual project goal is difficult to see at a glance;
- context disappears when sessions, agents, or models change.
PRIME solves **continuity, observability, provisioning, documentation, and durable memory**. It does not duplicate the coding agent.
## 1.3 North Star
> **Every managed project should remain understandable, inspectable, and resumable regardless of which AI coding agent is currently working on it. PRIME preserves the project's identity, authority, history, documentation, progress evidence, and durable memory while the coding agent performs the actual engineering.**
## 1.4 Product boundary
### PRIME may
- create/register a project;
- register an existing repository;
- create a new repository when explicitly requested during onboarding;
- store project name, image, description, machine, and repository path;
- provision the approved `.agent` authority template during initial project setup;
- guide the user through creation of a complete `.agent/PROJECT_GOAL.md`;
- read all `.agent` files;
- read all repository files allowed by policy;
- read Git metadata and history;
- watch repository and `.agent` changes;
- assess progress toward the project goal;
- create and maintain a dedicated Notion page for each project;
- read user-authored knowledge from connected Notion content;
- write/update PRIME-managed project documentation in Notion;
- maintain durable project memory;
- expose project memory and bounded project context through MCP;
- archive/remove projects from PRIME;
- delete/archive repository data only after an explicit destructive user command and safety workflow.
### PRIME may not
- autonomously edit normal application/source files;
- act as an autonomous coding loop;
- replace Codex or another coding agent;
- autonomously choose product direction;
- create new engineering goals without user/agent authority;
- silently rewrite `.agent` authority after bootstrap;
- silently change `PROJECT_GOAL.md`;
- mix project memories;
- expose another project's memory to a project-scoped coding agent;
- treat an LLM inference as authoritative truth;
- silently convert Notion brainstorming into project authority;
- autonomously dispatch coding agents in V1;
- perform cross-project reasoning in V1.
## 1.5 Read-only means read-only project observation, not zero lifecycle control
The normal project dashboard is **read-only with respect to repository truth and engineering authority**.
Lifecycle actions are separate, explicit management operations:
- bootstrap project;
- register project;
- remove project from PRIME;
- archive project;
- delete project/repository through a protected destructive workflow.
Normal monitoring, progress evaluation, memory, and documentation must never mutate application source code.
---
# 2. Foundational Architecture Rules
## 2.1 Codex is the worker; PRIME is continuity infrastructure
PRIME must never grow into a second coding-agent product.
Conceptually:
```plain text
        HUMAN
          │
┌─────────▼─────────┐
│   ANIMUS PRIME    │
│ project continuity│
└─────────┬─────────┘
          │
project memory/context
          │ MCP
   ┌──────▼──────┐
   │ CODEX / AI  │
   │ CODING AGENT│
   └──────┬──────┘
          │
    edits/tests/code
          │
   PROJECT REPO
```
## 2.2 Hard project isolation
Every project has a unique `project_id` and isolated:
- repository binding;
- `.agent` authority;
- Notion bindings;
- memory namespace;
- retrieval namespace;
- Hindsight bank;
- MCP access scope;
- progress assessments;
- event stream.
A coding agent attached to Project A must not be able to request Project B by supplying a different `project_id`. Project scope must be bound below the model at authentication/session level.
## 2.3 No cross-project reasoning in V1
PRIME does not compare, merge, or synthesize projects globally.
Cross-project reasoning creates unacceptable contamination risk for project-specific coding agents.
A future separate component named **Oracle** may be considered only as an explicit, read-only research system. Oracle would be unable to write repository files, `.agent`, Notion, memory, decisions, or project state and would not automatically feed conclusions into project agents. Oracle is **out of scope for V1**.
## 2.4 Authority is mapped, not centralized into one physical database
Different information types have different legitimate authorities.
<table fit-page-width="true" header-row="true">
<tr>
<td>Information</td>
<td>Authoritative source</td>
</tr>
<tr>
<td>Current source code</td>
<td>Repository filesystem</td>
</tr>
<tr>
<td>Git history</td>
<td>Git repository</td>
</tr>
<tr>
<td>Project goal</td>
<td>`.agent/PROJECT_GOAL.md`</td>
</tr>
<tr>
<td>Agent operating authority/rules</td>
<td>Approved `.agent` authority files</td>
</tr>
<tr>
<td>Project identity/configuration</td>
<td>PRIME canonical database</td>
</tr>
<tr>
<td>Machine/repository binding</td>
<td>PRIME canonical database</td>
</tr>
<tr>
<td>User-written Notion knowledge</td>
<td>Original Notion blocks/page</td>
</tr>
<tr>
<td>PRIME-generated project documentation</td>
<td>PRIME canonical projection state + rendered Notion section</td>
</tr>
<tr>
<td>Durable memories</td>
<td>PRIME memory service with source provenance</td>
</tr>
<tr>
<td>Knowledge-graph relationships</td>
<td>Derived memory unless explicitly user-confirmed</td>
</tr>
<tr>
<td>Progress percentage</td>
<td>Derived assessment, never authority</td>
</tr>
</table>
## 2.5 Evidence before inference
Every machine-generated conclusion must be distinguishable from its evidence.
Conceptual states:
```plain text
SOURCE OBSERVATION
      ↓
EXPLICIT USER/PROJECT FACT
      ↓
DERIVED INTERPRETATION
      ↓
MEMORY / SUMMARY / PROGRESS ASSESSMENT
```
A derived conclusion must retain provenance and may be superseded when source truth changes.
## 2.6 Event-driven over constant rereading
PRIME should avoid repeatedly scanning entire repositories or databases.
Repository changes, `.agent` changes, Notion revisions, Git commits, memory writes, and relevant system events should mark derived views stale and trigger bounded reprocessing.
Periodic reconciliation exists only as a safety net.
## 2.7 Implementation baseline and change control
During planning, this live Notion page is the editable source of truth. **When the operator declares planning complete, PRIME planning must be frozen into a versioned implementation baseline rather than leaving the coding agent dependent on a silently mutable page.**
The handoff baseline contains at minimum:
- an exported/snapshotted copy of this specification;
- a `spec_revision` / content hash and freeze timestamp;
- the approved `authority-template/v1` artifact plus manifest/hash;
- the approved foundational dependency/architecture decisions required by Phase 0.
The implementation baseline is immutable. Later product/spec changes require an operator-approved **SpecChangeRecord** identifying the reason, affected requirements, old/new baseline revision, and effective time. The coding agent must not treat an unreviewed live-page edit as permission to change implementation scope. Before implementation begins or resumes after a specification update, PRIME/build tooling must be able to identify which approved baseline revision is in force.
---
# 3. System Overview
```plain text
┌────────────────────────────────────────────────────────────┐
│                      ANIMUS PRIME UI                       │
│ Home • Ask • Search • Progress • Repo • Authority • Memory • Brain │
└──────────────────────────┬─────────────────────────────────┘
                           │
                 ┌─────────▼──────────┐
                 │    PRIME CORE      │
                 │ project registry   │
                 │ lifecycle          │
                 │ events/jobs        │
                 │ progress           │
                 │ documentation      │
                 └───┬─────────┬──────┘
                     │         │
           ┌─────────▼───┐   ┌─▼────────────────┐
           │ PRIME MEMORY│   │ NOTION CONNECTOR │
           │ ledger      │   │ read/write docs  │
           │ Hindsight    │   │ user knowledge   │
           │ retrieval   │   └──────────────────┘
           └──────┬──────┘
                  │
           ┌──────▼──────┐
           │  PRIME MCP  │
           │project-bound│
           └──────┬──────┘
                  │
           CODEX / AI CODER

PRIME CORE
    │ authenticated private Node control plane (LAN / tailnet)
    ├───────────────┬────────────────┐
    ▼               ▼                ▼
PRIME NODE       PRIME NODE       PRIME NODE
Linux PC         Windows PC       Laptop
    │               │                │
 Repo A           Repo B           Repo C
```
---
# 4. Major Components
## 4.1 PRIME Web UI
A modern, minimal, responsive local web application.
Responsibilities:
- project cards/list plus Needs Attention, Recently Active, and System Health;
- add-project and first-run setup wizards;
- project Overview with Since You Were Here, Integrity, Alignment, milestones, and completion review;
- project-scoped Ask PRIME and unified project Search;
- goal rendering;
- progress visualization, history, explanation, and correction workflows;
- repository read-only browser/search;
- `.agent` read-only browser;
- memory browser/search;
- interactive 3D Project Brain visualization of repository topology and optional memory overlays;
- Notion connection status and links;
- activity/history;
- project settings;
- remove/archive/delete workflows;
- node/machine health display.
The UI must not resemble an IDE. Coding remains in Codex or the user's chosen coding environment.
## 4.2 PRIME Core
The central trusted service.
Responsibilities:
- canonical project registry;
- node registry;
- repository bindings;
- project lifecycle orchestration;
- bootstrap orchestration;
- event ingestion;
- job scheduling/debouncing;
- progress assessment orchestration;
- documentation synchronization;
- memory orchestration and automatic authority-event ingestion;
- Ask/search/recap/attention/integrity/alignment services;
- canonical Git/worktree tracking and repository rebind orchestration;
- AI-connection/MCP session issuance and project scoping;
- usage/cost, notifications, backup/restore, upgrade/preflight state;
- health and diagnostics;
- audit logging.
## 4.3 PRIME Node
A small headless service installed on any LAN machine that hosts managed repositories.
It is **not an AI service** and has no independent project intelligence.
Required responsibilities:
- identify the machine with a stable node ID;
- advertise health/capabilities to PRIME Core;
- validate configured repository paths;
- safely list directories;
- read files within an approved repository root;
- read Git status/history/branch metadata;
- watch filesystem changes;
- create a repository when instructed by an explicit onboarding operation;
- create/copy the `.agent` bootstrap package during onboarding;
- perform explicit archive/remove/delete filesystem operations through protected lifecycle APIs;
- reject paths outside configured roots;
- enforce read-only operation for normal project monitoring.
The node must not:
- run arbitrary shell commands supplied by an LLM;
- edit application files;
- permit unrestricted filesystem traversal;
- expose other repositories without explicit registration.
## 4.4 Project Bootstrapper
Responsible for creating a consistent AI-ready project envelope.
Inputs:
- project identity;
- machine/node;
- repository path or new repository path;
- project-goal interview answers;
- optional project image;
- Notion destination/configuration.
Outputs:
- registered project;
- complete `.agent/PROJECT_GOAL.md`;
- versioned `.agent` authority structure;
- project Notion page;
- isolated Hindsight bank binding plus project-scoped repository search/index binding;
- optional attached Notion Knowledge Source bindings;
- initial source/index snapshot;
- initial progress assessment;
- project-scoped MCP configuration/credentials.
## 4.5 Progress Assessment Service
A bounded LLM-backed assessment pipeline that compares the actual project evidence with the declared project goal.
It does **not** edit anything.
It produces structured, explainable progress estimates with confidence, goal-item breakdown, blockers, and source references.
## 4.6 Project Documentation Agent and Notion Documentation Service
The human-readable Notion project record must **not depend on the coding agent maintaining it**. Codex or another AI coding agent is responsible for engineering work and for updating the authoritative `.agent` files required by the project protocol. A separate, narrowly scoped **Project Documentation Agent** is responsible for observing authoritative project changes and maintaining the PRIME-managed portions of the project's Notion page.
This separation is mandatory because documentation quality must not depend on which coding agent is active, whether that agent remembers to call Notion, or how it chooses to summarize its own work.
### 4.6.1 Responsibilities by actor
**AI coding agent / Codex**
- edits source code and tests;
- performs engineering work;
- follows the project's `.agent` authority;
- updates authoritative project files such as directives, outcomes, learnings, decisions, risks, state, and other files required by the approved authority template;
- records durable machine context through PRIME MCP when appropriate;
- does **not** maintain the human-readable Notion project record directly.
**Project Documentation Agent**
- runs independently from the coding agent;
- is triggered by specific project events rather than continuously polling or rewriting the full document;
- reads the authoritative `.agent` change that caused the event;
- reads additional repository, Git, memory, or existing Notion context only when needed to accurately explain the change;
- updates only the corresponding PRIME-managed Notion sections;
- preserves provenance back to authoritative source material;
- never edits source code, Git history, `.agent`, project memory, or user-authored Notion content.
**PRIME Memory**
- preserves durable machine-facing context for future AI coding sessions;
- is independent from the Documentation Agent;
- is not a substitute for the human-readable Notion record.
The intended separation is:
```plain text
                PROJECT
                   │
       ┌───────────┼───────────┐
       │           │           │
       ▼           ▼           ▼
  AI CODER     PRIME MEMORY   DOC AGENT
    Codex          MCP
       │             │           │
       ▼             ▼           ▼
code + .agent   store/recall   Notion record
       │             │           │
       └─────────────┼───────────┘
                     │
                     ▼
               PRIME DASHBOARD
```
### 4.6.2 Notion page creation
A dedicated Notion project page is created during project onboarding. Project provisioning is not complete until the page exists and the initial Documentation Agent run succeeds or enters a clearly reported degraded state because Notion is unavailable.
The onboarding sequence includes:
```plain text
Project identity
      ↓
Repository binding
      ↓
PROJECT_GOAL.md approval
      ↓
.agent bootstrap
      ↓
Memory namespace initialization
      ↓
Create Notion project page
      ↓
Initial Documentation Agent run
      ↓
GoalModel / Progress Baseline Review
      ↓
Initial progress assessment
      ↓
Project READY
```
The initial Documentation Agent run produces the first human-readable representation of the project from the approved goal, `.agent` state, repository structure, and other authorized sources.
### 4.6.3 Notion ownership zones
Every managed project page must distinguish content ownership so automated updates cannot destroy operator knowledge.
**PRIME-managed content** may include:
- Executive Summary;
- Project Goal;
- Current Status;
- Current Directive / Active Work;
- Progress Summary;
- Architecture / How It Works;
- Completed Work;
- Outcomes;
- Important Decisions;
- Learnings;
- Risks / Blockers;
- Validation / Evidence;
- Major Milestones;
- Recent Activity.
**User-managed content** may include:
- free-form notes;
- ideas;
- observations;
- research;
- images;
- links;
- references;
- additional project knowledge the operator wants available to AI systems.
The Documentation Agent may read authorized user-managed content for context but **must never overwrite, move, delete, reformat, or silently absorb ownership of it**. PRIME must use explicit block/section ownership markers or durable Notion block IDs so managed updates remain bounded.
### 4.6.4 Event-driven documentation triggers
The PRIME Node watches the approved authority files inside `.agent`. A raw filesystem write does not immediately invoke an LLM. PRIME first computes a diff, determines whether semantic content changed, classifies the change, debounces related saves, and emits a structured project event.
The exact filenames are defined by the finalized authority template. Conceptually, events include:
```plain text
DIRECTIVE_ADDED
DIRECTIVE_UPDATED
DIRECTIVE_REMOVED
OUTCOME_ADDED
OUTCOME_RETRACTED
LEARNING_ADDED
LEARNING_RETRACTED
DECISION_ADDED
DECISION_RETRACTED
RISK_ADDED
RISK_UPDATED
RISK_REMOVED
GOAL_CHANGED
STATE_CHANGED
VALIDATION_ADDED
VALIDATION_RETRACTED
MILESTONE_REACHED
```
Example flow:
```plain text
.agent/DIRECTIVES.md changes
        ↓
Node computes bounded diff
        ↓
new directive detected
        ↓
DIRECTIVE_ADDED event
        ↓
Documentation Agent job queued
        ↓
reads changed directive + relevant context
        ↓
updates Current Directive / Status / Recent Activity
```
A new outcome should similarly update the relevant human-readable sections without requiring the coding agent to perform a second documentation workflow.
### 4.6.5 Targeted updates, not full-document rewrites
The Documentation Agent must not regenerate the full Notion page whenever one source file changes.
Each event maps to likely affected sections. For example:
<table fit-page-width="true" header-row="true">
<tr>
<td>Event</td>
<td>Typical Notion sections affected</td>
</tr>
<tr>
<td>`DIRECTIVE_ADDED`</td>
<td>Current Directive, Current Status, Recent Activity</td>
</tr>
<tr>
<td>`OUTCOME_ADDED`</td>
<td>Completed Work, Outcomes, Recent Activity, possibly Executive Summary</td>
</tr>
<tr>
<td>`LEARNING_ADDED`</td>
<td>Learnings, possibly Architecture or Executive Summary if materially important</td>
</tr>
<tr>
<td>`DECISION_ADDED`</td>
<td>Important Decisions, Architecture/How It Works when applicable, Recent Activity</td>
</tr>
<tr>
<td>`RISK_ADDED` / `RISK_UPDATED`</td>
<td>Risks / Blockers, Current Status</td>
</tr>
<tr>
<td>`GOAL_CHANGED`</td>
<td>Project Goal, Executive Summary, Progress Summary</td>
</tr>
<tr>
<td>`VALIDATION_ADDED`</td>
<td>Validation / Evidence, Progress Summary, Recent Activity</td>
</tr>
</table>
The agent receives only the event, changed content, relevant surrounding authority, current target Notion section, and any additional bounded context required to write accurately.
### 4.6.6 Event structure
Documentation-triggering events should carry enough data to support deterministic processing and retries. Recommended fields:
```plain text
event_id
project_id
event_type
source_file
source_revision
source_content_hash
change_range / diff reference
created_at
node_id
related_authority_ids[]
processing_status
```
The event itself is not an LLM interpretation. It is a mechanically produced record that an authoritative project source changed.
### 4.6.7 Debouncing and semantic change detection
Editors and coding agents may save the same authority file several times while composing one logical update. PRIME must avoid firing multiple Documentation Agent runs for one logical change.
Required behavior:
1. detect filesystem write;
2. calculate content hash/diff;
3. ignore unchanged or formatting-only changes when safe to do so;
4. debounce closely grouped writes;
5. identify the resulting logical event(s);
6. enqueue one documentation job per meaningful event or coalesced event group.
### 4.6.8 Idempotency and retries
Documentation updates must be safe under at-least-once job delivery.
PRIME must persist processing metadata such as:
```plain text
event_id
project_id
source_revision
source_content_hash
target_notion_page_id
target_section_id / block_id
notion_revision_after_write
processed_at
status
retry_count
last_error
```
If PRIME crashes after writing to Notion but before acknowledging the job, replaying the event must detect that the source revision was already projected and must not duplicate directives, outcomes, learnings, or other entries.
### 4.6.9 Periodic reconciliation
Events are the primary synchronization mechanism, but correctness must not depend entirely on uninterrupted event delivery.
PRIME must run a bounded reconciliation:
- on PRIME startup after an unclean shutdown;
- when a node reconnects after being offline;
- after Notion recovers from an outage;
- periodically at a low frequency as a safety net.
Reconciliation compares authoritative `.agent` state with PRIME's recorded projection state and the PRIME-managed Notion sections. Missing or stale projections are repaired without touching user-managed content.
**Events provide immediacy. Reconciliation provides eventual correctness.**
### 4.6.10 Documentation Agent access policy
The Documentation Agent has narrow capability boundaries.
**May read:**
- the current project's `.agent` files;
- the current project's repository files when needed for explanation;
- current-project Git metadata/history;
- current-project PRIME memory when needed for historical context;
- current PRIME-managed Notion sections;
- authorized user-managed Notion knowledge.
**May write:**
- only PRIME-managed sections/blocks of the current project's Notion page;
- internal documentation-job status/audit records.
**May not write:**
- source code;
- Git;
- `.agent` files;
- project goal;
- project memory;
- progress evidence;
- user-managed Notion content;
- another project's Notion page.
Project scoping must be enforced below the model exactly as it is for PRIME MCP.
### 4.6.11 Relationship to progress assessment
Documentation events and progress assessment events may originate from the same authoritative changes, but they remain separate jobs.
For example, `OUTCOME_ADDED`, `GOAL_CHANGED`, or `VALIDATION_ADDED` may:
- enqueue a targeted Documentation Agent update; and
- mark the project's progress assessment stale and enqueue a progress reassessment.
The Documentation Agent does not calculate the canonical progress percentage itself. It renders the latest approved derived assessment produced by the Progress Assessment Service.
### 4.6.12 Failure behavior
If the Documentation Agent or Notion API fails:
- project engineering must continue;
- source code and `.agent` remain authoritative;
- the failed documentation event remains durably queued;
- the UI shows documentation as stale/degraded;
- retries use backoff;
- recovery triggers reconciliation;
- no authority file is modified to compensate for a Notion failure.
A Notion outage must never block Codex from doing project work or PRIME Memory from serving project-scoped context.
### 4.6.13 Core design rule
> **The AI coder records authoritative project outcomes as part of doing the work. A separate observer turns those authoritative changes into the durable human-readable project record.**
This prevents the coding agent from being responsible for documenting itself and keeps machine continuity, human documentation, and engineering authority as separate concerns.
## 4.7 PRIME Memory — Hindsight
PRIME Memory is the durable, project-specific memory service used by AI coding agents across sessions. **Hindsight is the selected V1 memory engine.** PRIME must integrate Hindsight behind a PRIME-owned adapter and MCP contract rather than exposing Hindsight directly to coding agents.
The purpose of PRIME Memory is not to duplicate the repository. It preserves information whose meaning would otherwise be expensive or impossible to reconstruct from current code alone: rationale, failures, lessons, procedures, environment quirks, operator observations, invalidated approaches, historical context, and important changes in understanding.
### 4.7.1 Architectural boundary
```plain text
CODEX / AI CODER
       │
       ▼
PRIME MEMORY MCP
       │
       ▼
PRIME MEMORY SERVICE
scope • policy • provenance • filtering • budgets
       │
       ▼
HINDSIGHT ADAPTER
       │
       ▼
HINDSIGHT BANK — exactly one bank per project
       │
       ▼
PostgreSQL + pgvector
```
PRIME owns:
- project authentication and isolation;
- the coding-agent-facing MCP schema;
- memory retention policy;
- salience/noise filtering;
- provenance enrichment;
- secret/sensitive-content filtering;
- token/output budgets;
- source classification;
- health checking and durability verification;
- adapter compatibility with the selected Hindsight version.
Hindsight owns the memory-engine internals, including its world facts, experiences, observations, entity/relationship extraction, temporal organization, retrieval, reflection capabilities, and mental-model machinery.
The Hindsight dependency must remain replaceable behind the PRIME adapter. Coding agents must never depend on Hindsight-specific bank IDs or raw Hindsight MCP schemas.
### 4.7.2 One Hindsight bank per project
Every PRIME project maps to exactly one isolated Hindsight memory bank.
```plain text
Project A → Hindsight Bank A
Project B → Hindsight Bank B
Project C → Hindsight Bank C
```
A project-scoped MCP session is bound to its project before model execution. The coding agent cannot select a different project or bank by passing another ID. Bank identifiers are internal PRIME implementation details.
No cross-bank recall is allowed in normal project operation. Oracle, if ever implemented, is a separate read-only system and is not part of this memory path.
### 4.7.3 Memory model retained from Hindsight
PRIME intentionally preserves Hindsight's richer memory concepts rather than flattening everything into generic vector records.
**World facts** represent information believed about the project or environment.
**Experiences** represent things that happened to or were done by an agent during project work.
**Observations** are derived, evidence-linked conclusions synthesized from accumulated memories. Observations are valuable and must be retained, but they are always labeled as **derived** rather than authoritative fact.
PRIME must preserve source relationships so an observation can be traced back to the memories/facts from which it was derived.
### 4.7.4 Memory categories used by coding agents
The PRIME MCP should require a small semantic reason when storing durable memory. Initial categories:
- `learning`;
- `decision_rationale`;
- `failure`;
- `procedure`;
- `environment`;
- `constraint`;
- `observation`.
These categories are PRIME policy/tags layered over Hindsight rather than separate storage systems.
Good memory examples:
- why an architecture was chosen;
- why an approach was abandoned;
- a failure that consumed meaningful debugging effort;
- an experiment result that affects future work;
- a non-obvious environment or deployment condition;
- a reliable repair/build/release procedure;
- a user/operator observation that materially affects the project;
- a constraint that is not obvious from current code;
- a lesson likely to matter in future sessions.
Do not use durable memory for trivial facts that are cheap to rediscover from current repository state, such as ordinary file edits, routine passing tests, line counts, or obvious framework usage.
### 4.7.5 Memory write path
```plain text
Coding agent learns something durable
            ↓
prime_memory_store(...)
            ↓
PRIME binds project/session identity
            ↓
validate category + salience
            ↓
secret/sensitive-content filter
            ↓
attach provenance automatically
            ↓
Hindsight retain
            ↓
verify durable completion
            ↓
return confirmed memory reference
```
PRIME should automatically attach provenance where available, including:
- `project_id`;
- agent identity;
- session/run identity;
- active directive/work reference;
- Git commit/revision;
- source file or `.agent` reference;
- timestamp;
- memory category;
- user/agent/source attribution.
The coding agent should provide the durable content and category, not manually reconstruct metadata PRIME already knows.
A memory write is not considered successful merely because the backend accepted a request. PRIME must verify the Hindsight operation reached a durable successful state before reporting the memory as stored.
### 4.7.6 Memory recall path
Normal recall must be bounded and task-relevant.
```plain text
Codex asks:
"What should I know before changing persistence?"
            ↓
PRIME Memory MCP
            ↓
Hindsight recall
            ↓
PRIME applies project scope + result budget
            ↓
returns ranked memories with provenance/type
```
Recall output should distinguish at minimum:
- source/world facts;
- agent experiences;
- derived observations.
Derived observations must never be presented indistinguishably from source-backed facts.
PRIME should return a compact result set rather than dumping a project's memory history into the model. Normal context should be token-budgeted and optimized for relevance.
### 4.7.7 PRIME Memory MCP contract
Coding agents interact with PRIME, not Hindsight directly.
Minimum V1 tool surface:
```plain text
prime_memory_store
prime_memory_recall
prime_memory_timeline
prime_memory_get
prime_memory_report_problem
prime_memory_context
```
`prime_memory_context` is the convenience retrieval operation for task startup. It returns a bounded package of relevant durable memory and associated project authority/context references while leaving the coding agent responsible for reading current repository files directly.
The MCP must not expose dangerous administrative Hindsight operations to normal coding sessions, including bank deletion, unrestricted memory clearing, bank mutation, or arbitrary cross-bank access.
### 4.7.8 Observations are enabled
Hindsight observations are intentionally part of PRIME, not disabled.
They provide a mechanism for the memory system to form evidence-linked, evolving lessons from accumulated project experience. Because these are inferred, PRIME must:
- label them `DERIVED OBSERVATION`;
- retain links to source facts/experiences;
- allow later evidence to supersede or weaken them;
- never allow an observation by itself to rewrite `.agent`, repository state, decisions, or project authority.
Coding agents may recall observations as useful context, but must be able to inspect supporting provenance.
### 4.7.9 Reflect is retained as an advanced capability
Hindsight's reflection capability is intentionally preserved behind the PRIME Memory Service.
Normal coding-agent workflows should not automatically call Reflect on every task. Reflect is an advanced reasoning operation over project memory and therefore has a different epistemic status than ordinary recall.
Outputs from Reflect must be stored or surfaced as derived analysis with provenance. They are never authoritative project truth and cannot directly mutate source code, `.agent`, decisions, Notion user content, or progress state.
### 4.7.10 Mental Models are retained
Hindsight Mental Models are also intentionally retained.
They may provide persistent, refreshable higher-level representations of recurring project knowledge, patterns, constraints, and learned structure. Mental Models are derived artifacts, not authority.
PRIME should support viewing their state/health in the Memory UI when the backend exposes useful metadata, while keeping them separate from user-authored/project-authoritative records.
### 4.7.11 Reserved future capability — Dreaming Loop
ANIMUS PRIME intentionally reserves **Observations + Reflect + Mental Models** for a future project-scoped **Dreaming Loop**.
The purpose of the Dreaming Loop is to let a separate, bounded agent periodically reason over accumulated project memory to discover opportunities to improve how the project or PRIME's supporting processes operate.
Conceptual future flow:
```plain text
Project memory accumulated
        ↓
quiet/explicitly scheduled dream cycle
        ↓
Dreaming Agent reads:
• facts
• experiences
• observations
• mental models
        ↓
uses Reflect and other bounded analysis
        ↓
produces candidate insights / improvement hypotheses
        ↓
stored as derived dream outputs
        ↓
review / validation required before any authoritative action
```
The Dreaming Loop is **not part of normal autonomous coding** and must never directly modify repository code, `.agent`, project authority, or decisions. Its outputs are proposals/derived knowledge until explicitly validated through a future governed process.
The V1 architecture must avoid design choices that prevent this future capability, but implementation of an autonomous Dreaming Agent is not required for initial V1 unless explicitly promoted into scope later.
### 4.7.12 Memory backend deployment
Production deployment must use a **pinned, compatibility-tested Hindsight version** behind the PRIME adapter with durable PostgreSQL + pgvector storage. Never deploy a floating `latest` image in production; pin an immutable release/tag and preferably image digest. Phase 0 must record the exact supported Hindsight version/image, required PostgreSQL/pgvector versions, extraction LLM/embedding/reranker requirements, bank-level configuration behavior, document/delete/reprocess semantics, async operation behavior, bank lifecycle API behavior, retain/recall durability semantics, portable export/import and database backup/restore methods, migration expectations, and adapter compatibility tests. Upgrading Hindsight or any embedding/reranking model is a controlled dependency migration with pre-upgrade backup and AI retrieval/regression tests, not an automatic floating-version update.
PRIME must include:
- health checks;
- schema/version compatibility checks;
- migration strategy;
- backup/restore integration;
- project-bank creation during onboarding;
- project-bank archival/deletion only through protected lifecycle operations;
- degraded-state reporting when Hindsight is unavailable;
- retry/recovery for transient failures;
- explicit validation that a retained memory actually persisted.
Failure of Hindsight must not corrupt project authority or prevent the repository from being worked on manually. PRIME should surface memory as degraded/unavailable while preserving the rest of the project dashboard.
## 4.8 PRIME MCP
The coding-agent interface to project memory and bounded project context.
Each MCP session/token is bound to exactly one project namespace.
---
# 5. Project Lifecycle
## 5.1 Project states
Project state must be modeled on **separate axes** so lifecycle, connectivity, freshness, and work condition are never conflated.
### Lifecycle state
```plain text
DRAFT
PROVISIONING
READY
ACTIVE
PAUSED
COMPLETION_REVIEW
COMPLETED
ARCHIVED
REMOVED
DELETION_PENDING
DELETED
```
`ACTIVE` does not mean PRIME is autonomously coding. It means the project is an active managed project. `PAUSED` means the project remains managed and inspectable but ordinary watchers/automations may be reduced. `COMPLETION_REVIEW` means PRIME estimates the declared goal is satisfied and is waiting for operator review. `COMPLETED` is operator-confirmed and must never be inferred solely from a model score.
### Connectivity state
```plain text
ONLINE
DEGRADED
OFFLINE
```
This describes the bound PRIME Node/repository reachability and supporting-service availability, not lifecycle.
### Derived-data freshness
```plain text
CURRENT
STALE
UNKNOWN
```
Progress, documentation, indexes, and other projections track freshness independently.
### Work / authority condition
```plain text
NORMAL
BLOCKED
CONFLICT
INVALID_AUTHORITY
REVIEW_REQUIRED
```
This describes conditions surfaced from project evidence. A project may therefore be `ACTIVE + ONLINE + STALE + BLOCKED` without corrupting lifecycle semantics.
## 5.2 Add Project wizard
The onboarding workflow is a first-class product feature and must feel deliberate rather than administrative.
### Provisioning gate policy
Project readiness distinguishes **hard safety/authority prerequisites** from **degradable continuity features**.
Hard prerequisites that must block `READY` until resolved:
- valid project identity and unique `project_id`;
- approved/bound repository path inside an allowed root;
- repository identity/canonical Git target established where Git is expected;
- operator-approved `PROJECT_GOAL.md`;
- `.agent` bootstrap/adoption conflict resolved and authority package structurally valid;
- no unresolved path/security condition that would make monitoring unsafe.
Capabilities that may enter `DEGRADED`/`PENDING` state without making the repository unusable:
- Notion page creation/synchronization;
- Hindsight bank availability or initial memory warm start;
- AI provider needed for Documentation/Ask/Progress;
- proposed Progress Baseline generation/approval;
- initial repository semantic index/Project Brain generation;
- optional remote-development provider;
- optional Evidence parser/indexing.
If a degradable dependency is unavailable, the wizard clearly shows what is missing and offers retry or **Continue Degraded** where doing so does not violate a privacy/security/authority rule. The project can become `READY` with subsystem health flags such as `memory: degraded`, `documentation: pending`, or `progress: baseline_pending`; no unavailable derived feature may fabricate a successful/current result. Recovery jobs reconcile and complete initialization when dependencies return.
### Step 1 — Identity
Collect:
- project name;
- optional short description;
- project image/icon;
- optional tags.
### Step 2 — Repository host
Show registered PRIME Nodes and health.
User chooses the machine containing or receiving the project.
The UI must display human-friendly node information:
- node name;
- operating system;
- online/offline state;
- last seen;
- allowed repository roots.
### Step 3 — Repository
Choose one:
- **Attach existing repository**;
- **Create new repository**.
For existing repositories:
- browse only within node-approved roots;
- validate path;
- verify directory existence;
- detect Git repository;
- display current branch/remotes/status;
- warn if repository has unexpected or unsupported conditions.
For new repositories:
- choose approved parent path;
- create directory;
- **initialize Git as a required step** and establish the configured canonical branch/ref;
- do not generate application code unless a separate external coding-agent workflow does so.
If a newly initialized repository has no commit yet, PRIME must explicitly support the Git **unborn branch** state. The current working tree remains current source truth, but commit-dependent features such as Fork/Clone and exact historical code reconstruction remain unavailable until a canonical commit exists. PRIME must not create an implicit Git commit unless the operator explicitly chooses a bootstrap-commit option.
### Step 4 — Project goal interview
The user should not be forced to hand-author `PROJECT_GOAL.md` from scratch.
A guided AI-assisted interview should collect enough information to generate a complete goal document.
At minimum capture:
- what is being built/researched;
- why it exists;
- target user/operator;
- desired end state;
- core functional requirements;
- non-functional requirements;
- hard constraints;
- explicit non-goals;
- success criteria;
- validation/evidence expectations;
- supported environments/platforms;
- important known dependencies;
- unacceptable outcomes;
- any required stopping/failure rules.
The generated goal must be shown to the user for review.
**No project becomes READY until the user explicitly approves the generated ****`PROJECT_GOAL.md`****.** After onboarding, the approved goal revision remains operator-controlled product authority. A coding agent may propose a goal change or edit it only when the operator explicitly instructs that scope/product goal be changed; routine implementation work must not rewrite the target it is being measured against. PRIME records the last operator-approved goal hash/revision. If filesystem monitoring detects a different `PROJECT_GOAL.md` without a corresponding approval record, PRIME marks **Goal Approval Required**, freezes the previous GoalModel/progress baseline as the last approved target, surfaces the mutation in Integrity/Needs Attention, and requires operator accept/reject/revert resolution before the new goal becomes the scoring/documentation baseline.
### Step 5 — Bootstrap authority
PRIME creates `.agent/` from its bundled, versioned authority template.
The source template must be based on the finalized authority package derived from `/home/sketch/Projects/authority`, but production PRIME must not depend on that absolute source path at runtime.
The template lives inside PRIME and has an explicit version.
Each project stores:
```plain text
authority_template_version
bootstrap_timestamp
bootstrap_hash
```
`PROJECT_GOAL.md` generated for the project is inserted into the correct authority location.
After bootstrap, normal PRIME monitoring treats `.agent` as read-only source authority. Changes are made by the user/coding agent through the project's normal engineering workflow, not silently by PRIME.
### Step 6 — Notion page
Create a dedicated project page using the project name and image when supported.
Record the resulting Notion page ID/URL in the project binding.
### Step 7 — Memory and retrieval bindings
Create the isolated project continuity bindings:
- exactly one Hindsight bank for durable agent memory;
- PRIME project↔Hindsight-bank binding and adapter metadata;
- project-scoped repository search/index namespace, explicitly **not** a second memory store;
- normalized PRIME event/audit stream used for provenance and product timelines;
- project-scoped MCP identity/capability binding.
Do not create a parallel custom semantic/episodic/graph/vector memory database during onboarding.
### Step 8 — Initial scan
Read:
- repository tree;
- relevant repository text/source files;
- `.agent`;
- Git metadata;
- initial Notion page content.
The scan must respect ignore rules, file-size limits, binary exclusions, secret filtering, and supported file types.
### Step 9 — Initial documentation
Generate the first PRIME-managed human-readable Notion record.
### Step 10 — Initial progress baseline and assessment
Generate the proposed GoalModel, show the Progress Baseline Review, and require operator approval/adjustment before persisting the first official percentage. Once approved, create the first structured goal-coverage assessment against that frozen baseline.
### Step 11 — Ready screen
Show:
- repository binding;
- node status;
- Notion page;
- `.agent` health;
- memory health;
- MCP status;
- initial progress;
- any onboarding warnings.
Only then transition `PROVISIONING → READY`.
---
# 6. Repository and Node Model
## 6.1 Repository identity
A physical repository may be bound to **only one active PRIME project**. Registration/rebind preflight must detect the same canonical path, Git common directory/worktree relationship, or repository identity fingerprint already owned by another active project and reject accidental duplicate registration. Additional Git worktrees of the same repository belong to the same PRIME project rather than becoming separate projects. Fork/Clone is the supported way to create a distinct project and requires a distinct repository copy/binding.
A project repository binding must include at least:
```plain text
project_id
node_id
canonical_path
repository_type
is_git_repository
git_root
current_branch
remote_metadata
registered_at
last_seen_at
last_scan_at
last_event_at
```
## 6.2 Path safety
A PRIME Node must have administrator-configured allowed roots.
Every file operation must:
1. resolve canonical path;
2. verify it is inside an allowed root;
3. verify it is inside the bound project repository when project-scoped;
4. reject symlink/path traversal escapes;
5. apply file policy before returning content.
Cross-platform identity must not depend on OS-native path spelling. PRIME stores canonical **repository-relative logical paths** separately from machine-local absolute paths, normalizes path separators for internal IDs, preserves original display casing, and detects case-folding or Unicode-normalization collisions that may be legal on Linux but ambiguous on Windows/macOS filesystems. Rebinding a repository across machines must not create duplicate file identities merely because separators, drive letters, casing, or Unicode normalization differ. Rename/move detection should preserve historical provenance and Project Brain continuity where Git/content evidence makes the mapping reliable.
## 6.3 Read policy
Default ingestion exclusions:
- `.git` object database contents;
- dependency/vendor trees such as `node_modules` unless specifically required;
- build output;
- caches;
- binary blobs;
- large generated files;
- secrets and credential files;
- user-configured ignore patterns.
PRIME should honor repository-native ignore mechanisms where appropriate and support a PRIME-specific ignore file for additional exclusions. Ignore rules apply to ordinary repository indexing/search, **not to required project authority**: the approved `.agent` authority files and coding-agent bridge/Integrity metadata must still be observed and validated even if `.gitignore` or a PRIME index-ignore pattern would otherwise hide them. An operator cannot accidentally disable authority monitoring by ignoring `.agent`.
### Repository edge-case policy
The repository reader/indexer must explicitly handle rather than accidentally traverse:
- bare Git repositories: unsupported as a managed PRIME project because PRIME requires a working tree for current repository/authority truth; reject with a clear onboarding error or require the operator to create/attach a working clone;
- Git submodules: represent the submodule entry and commit pointer in the parent project; do not recursively ingest the external repository unless it is separately/explicitly approved as part of the project policy;
- Git LFS: index pointer metadata by default and avoid automatically downloading large LFS objects merely for indexing;
- nested Git repositories: treat them as boundaries and require explicit operator choice before indexing the nested repository;
- generated/vendor/package-manager directories: exclude by default even when not ignored by Git, with visible diagnostics when they dominate repository size;
- sparse checkouts and partial clones: mark missing/non-present content as unavailable rather than assuming deletion;
- symlinks/junctions: never follow them outside the approved repository root; internal links may be represented without creating duplicate indexing paths;
- very large text files: apply configurable size/chunk limits and surface partial-index status;
- non-UTF-8/unknown encodings: preserve file metadata and mark textual indexing unavailable unless a safe decoder is configured;
- binary assets: represent metadata/path in repository and Project Brain views without sending binary content to LLM/index pipelines unless a specific parser is enabled.
V1 uses **one primary Git repository per PRIME project**. A monorepo is one project and may expose internal package/subsystem clusters. Multiple independent repositories must not be silently merged into one project; if multi-repository projects are added later they require an explicit project-level repository-set contract so isolation, Git truth, progress, memory provenance, and deletion semantics remain unambiguous.
## 6.4 Git usage
Normal monitoring may read:
- branch;
- HEAD commit;
- commit metadata/history;
- changed file list;
- diff metadata;
- dirty/clean status;
- tags/remotes when useful.
Normal monitoring must not:
- commit;
- checkout;
- merge;
- reset;
- rebase;
- push;
- pull;
- modify working-tree files.
## 6.5 Filesystem watching
Node watchers should emit normalized events such as:
```plain text
repo.file.created
repo.file.modified
repo.file.deleted
agent.file.modified
git.head.changed
repo.bulk_change
```
Events should contain metadata and hashes where useful, not automatically transmit every full file.
PRIME Core decides what must be reread.
## 6.6 Offline nodes
If a node becomes unavailable:
- project remains visible;
- last known status remains available with timestamp;
- UI clearly marks repository data stale/offline;
- memory remains queryable;
- Notion remains linkable/queryable if available;
- progress assessment must not claim freshness beyond the last synchronized repository state.
When the node returns, reconcile changes before declaring current state fresh.
---
# 7. `.agent` Authority and `PROJECT_GOAL.md`
## 7.1 Purpose
The `.agent` folder is the repository-local authority package used by AI coding agents and human operators.
PRIME must **read and visualize** this authority, not replace it with hidden database state.
## 7.2 Bootstrap template
The approved authority source currently originates from `/home/sketch/Projects/authority`, but the cold-start implementation must **not depend on that absolute planning-machine path being available**.
### Planning-completion handoff prerequisite
Before the operator declares ANIMUS PRIME planning complete and hands this specification to the coding agent, the approved authority package must be audited and snapshotted as a versioned implementation input accessible alongside the PRIME project (for example a bundled `authority-template/v1` directory or equivalent retained artifact) with a manifest/hash. This snapshot—not the historical absolute path—is the implementation source the coder receives. The path `/home/sketch/Projects/authority` is provenance for how the snapshot was derived, not a runtime or cold-start dependency.
If the approved snapshot has not been produced at implementation handoff, Phase 0 must stop with an explicit **MISSING_AUTHORITY_TEMPLATE** prerequisite rather than inventing authority file contents.
Requirements:
- preserve intentional authority semantics;
- remove assumptions that only made sense for retired systems;
- document every generated file;
- test bootstrap output byte/semantic structure where appropriate;
- version the template;
- never silently mutate existing projects when the template version advances.
## 7.3 Goal document
`PROJECT_GOAL.md` is the canonical declaration of project intent.
It must be:
- human-readable;
- AI-readable;
- sufficiently concrete to evaluate progress;
- stable unless intentionally changed;
- traceable through Git history when the project is version controlled.
PRIME may assist in generating it only during explicit user flows.
## 7.4 Authority health
PRIME should detect and display:
- missing required authority files;
- malformed files;
- template-version drift;
- duplicate/contradictory authority declarations when detectable;
- modified `PROJECT_GOAL.md` since last assessment;
- stale derived progress after authority changes.
It should not silently fix these after onboarding.
---
# 8. Progress and Goal-Completion Assessment
## 8.1 Purpose
The project-card progress bar is an **estimated evidence-backed measure of how much of the declared project goal appears achieved**.
It is not a project-management task-completion percentage and not an LLM vibe score.
## 8.2 Required inputs
At minimum the assessor receives:
- current `PROJECT_GOAL.md`;
- relevant `.agent` files;
- completed/accepted work records available in `.agent`;
- validation/evidence records;
- current repository structure and selectively retrieved source evidence;
- relevant Git state/history;
- relevant project memories only when their provenance is adequate.
The evaluator should retrieve only necessary repository evidence rather than always stuffing the entire repo into one prompt.
## 8.3 Goal decomposition
The evaluator transforms the goal into stable `GoalItem` objects.
Conceptual schema:
```json
{
  "goal_item_id": "...",
  "title": "Persistent project memory",
  "description": "...",
  "weight": 0.20,
  "required": true,
  "acceptance_evidence": ["..."],
  "status": "partial",
  "completion": 0.60,
  "confidence": 0.82,
  "evidence_refs": ["..."],
  "missing_evidence": ["..."],
  "blockers": ["..."]
}
```
Goal-item identities should remain stable across reassessments unless the **operator-approved** project goal itself changes materially.
### Progress Baseline Review
The first GoalModel generated for an approved `PROJECT_GOAL.md` revision is a proposal, not silently accepted scoring authority. PRIME must present the derived GoalItems, descriptions, required/optional status, acceptance expectations, and weights in a lightweight **Progress Baseline Review**. The operator may accept the proposal or adjust the decomposition/weights before the first official percentage is displayed. Until approved, the project shows **Progress baseline pending** rather than a definitive percentage.
The approved GoalModel is stored with its goal revision and model/prompt/schema metadata. Routine reassessment may change evidence, completion, blockers, and confidence but **not** GoalItem identities/weights. Re-baselining requires either an operator-approved `PROJECT_GOAL.md` revision or an explicit operator **Rebuild Progress Baseline** action, and all previous assessments remain historically associated with the old baseline.
## 8.4 Scoring
Overall progress is the normalized weighted completion of goal items.
Required constraints:
- weights sum to 1.0;
- required goals cannot be hidden by many trivial completed goals;
- confidence is stored separately from completion;
- missing evidence lowers confidence and/or completion according to explicit rules;
- a failed validation can reduce previous completion;
- progress may move backward;
- material goal changes invalidate/rebase the assessment history rather than pretending the same percentage is directly comparable.
Recommended status vocabulary:
```plain text
not_started
in_progress
partial
implemented_unverified
verified
blocked
failed
not_applicable
unknown
```
## 8.5 Assessor output
```json
{
  "project_id": "...",
  "assessment_id": "...",
  "goal_revision_hash": "...",
  "repository_revision": "...",
  "progress_percent": 67,
  "confidence": 0.84,
  "summary": "...",
  "goal_items": [],
  "blockers": [],
  "uncertainties": [],
  "evidence_refs": [],
  "created_at": "..."
}
```
The UI must never display a percentage without making the underlying assessment accessible.
## 8.6 Triggering reassessment
Mark progress stale after material events such as:
- `PROJECT_GOAL.md` change;
- relevant `.agent` state/evidence change;
- Git HEAD change;
- validation evidence change;
- substantial repository change;
- explicit user request.
Use debounce/coalescing so a large coding operation causes one assessment after the repository settles rather than hundreds of calls.
A periodic reconciliation may reassess stale projects as a safety net.
## 8.7 Project card semantics
Display:
- progress bar;
- percentage;
- confidence indicator;
- freshness timestamp;
- project state such as Active / Offline / Blocked / Stale;
- optionally a short current blocker/status line.
Do not conflate progress with health. A project may be 90% complete and currently blocked.
## 8.8 Progress history
PRIME must retain progress-assessment history and show change over time rather than only the current percentage. The Progress surface should support a timeline/chart with assessment points and markers for major explanatory events such as goal revisions, failed validations, major milestones, and operator-confirmed completion. Selecting a historical point must reveal the exact GoalModel revision, evidence, confidence, and explanation that produced that score.
**Percentages produced under different GoalModel revisions are not directly comparable.** The chart must visually segment approved baselines/goal revisions and label the boundary. A new or expanded goal may legitimately create a very different percentage because the denominator changed; PRIME must not present that as ordinary project regression. `Since You Were Here`, notifications, and Needs Attention use phrases such as **Progress baseline changed: 80% on GoalModel A → 55% initial score on GoalModel B** rather than claiming `-25% regression`. Regression/delta calculations are valid only between assessments that share the same approved GoalModel revision.
## 8.9 Stable GoalModel
A `GoalModel` is generated once for each approved `PROJECT_GOAL.md` revision. Goal-item identities, weights, required flags, and acceptance expectations are frozen for that goal revision. Ordinary reassessment may update evidence, completion, blockers, and confidence but must not silently restructure the scoring model. A materially changed `PROJECT_GOAL.md` creates a new GoalModel revision. The operator may explicitly request a GoalModel rebuild if decomposition is wrong.
## 8.10 Goal alignment / drift
PRIME must provide a separate read-only **Goal Alignment** assessment answering whether current work still maps to the declared project goal. It may flag substantial directives or repository changes with no clear goal relationship, contradictory authority, implicitly abandoned requirements, or significant implementation areas unsupported by the goal. Alignment is derived advisory information only and cannot stop work or create directives.
## 8.11 Milestones
PRIME may derive human-scale milestones from stable GoalModel groupings so the operator can understand broad phases such as Foundation, Memory, MCP, UI, or Hardening without introducing a second task-management system. Milestones are projections over GoalItems and evidence, not new project authority.
## 8.12 Human challenge and correction
Every AI-derived assessment must expose a **Challenge / This is wrong** workflow. The operator can report missed evidence, incorrect goal interpretation, wrong status, or stale inputs. A challenge does not directly overwrite source truth; it creates a reviewed correction/reassessment event with provenance and may trigger a new assessment.
## 8.13 Completion semantics
A high progress score never automatically completes a project. When the evidence-backed estimate reaches the completion threshold, PRIME moves the project into `COMPLETION_REVIEW`, produces a final goal-evidence review, surfaces unresolved uncertainty, and asks the operator to confirm. Operator confirmation creates the `COMPLETED` lifecycle state, triggers a final Documentation Agent update, final project summary, final memory consolidation/reconciliation, and optional archive. Completion may be reversed only by an explicit operator action or a new approved goal revision.
---
# 9. Notion Project Record
## 9.1 Purpose
Every PRIME project receives a human-readable Notion page automatically.
The page is useful independently of PRIME and gives the operator a readable project history without opening the repository or interpreting `.agent` internals.
## 9.2 Page structure
Recommended structure:
```plain text
Project Name

PRIME MANAGED
- Overview
- Project Goal
- Current State
- Progress
- Architecture / System Shape
- Current Work
- Completed Work
- Important Decisions
- Risks / Blockers
- Validation / Evidence
- Important Memory / Lessons
- Recent History

USER KNOWLEDGE
- User Notes
- Research
- Ideas
- Free-form project knowledge
```
The precise formatting can evolve, but the managed/user ownership boundary must remain explicit.
### Long-running documentation rollover
The dedicated Project Record must remain useful after years of activity. PRIME keeps the root page focused on current state, durable summaries, major decisions/lessons, recent history, and navigation. When append-only managed history exceeds configurable size/age thresholds, the Documentation Service rolls older PRIME-managed chronological detail into **PRIME-owned linked history subpages** grouped by period or milestone while preserving source references and Time Lens revision links. User-owned content is never moved automatically. Rollover is deterministic/idempotent and must not summarize away the underlying authoritative evidence; it is a human-readable presentation compaction, not deletion of project history.
## 9.3 Managed-content protection
PRIME must never replace the entire Notion page on routine synchronization.
Use identifiable managed regions/blocks and update only those regions.
User content outside managed regions is immutable to automated refresh.
If managed markers are missing or ambiguous, fail safely and ask for repair rather than overwriting the page.
## 9.4 User knowledge ingestion
Authorized user-written Notion content may be ingested as source observations with provenance:
```plain text
source_type: notion
page_id
block_id / location when available
author when available
observed_at
content_hash
text
```
Notion text becomes project **knowledge-source input**, **not automatic ****`.agent`**** authority and not automatic Hindsight memory**. Attached/user-authored Notion content is indexed/retrieved through the project Knowledge/Search layer with its original page/block provenance. PRIME may admit a specific Notion statement into durable Hindsight memory only when an explicit operator action, authoritative project event, or salience policy designed for user-authored facts selects it. PRIME-generated Documentation Agent blocks are excluded from Hindsight admission and user-knowledge ingestion by default to prevent self-referential feedback loops and duplicate memory.
## 9.4A External knowledge connector boundary
**Notion is the only external human-knowledge connector in the ANIMUS PRIME product plan.** A project may bind its dedicated PRIME-managed Notion Project Record plus operator-selected additional Notion pages as read-only Knowledge Sources. PRIME must not implement a generic connector framework for Google Drive, Slack, OneDrive, Dropbox, generic websites, arbitrary SaaS knowledge bases, or other document systems unless this specification is intentionally revised.
This boundary does not prohibit:
- repository/Git/remote-provider status adapters, because they are engineering-state/evidence integrations rather than human knowledge connectors;
- PRIME Evidence uploads or explicit external Evidence references, because those are project artifacts with provenance rather than a generic knowledge-ingestion connector;
- Notion pages shared by explicit operator choice across more than one isolated PRIME project, provided each project has its own binding/index/provenance and no memory is automatically shared.
Ask, Search, Documentation and memory-admission logic must preserve this distinction. No service should silently turn an unsupported external source into project knowledge merely because a URL or file is reachable.
## 9.5 Documentation refresh
Documentation should update on meaningful project changes, not every file save.
Potential triggers:
- new progress assessment;
- material `.agent` change;
- significant memory/decision/lesson event;
- project state change;
- explicit refresh;
- periodic reconciliation.
## 9.6 Documentation generator inputs
The documentation agent may read:
- project goal;
- `.agent` state/history/evidence;
- current progress assessment;
- selected repository architecture/index data;
- Git activity;
- selected durable memories;
- existing managed Notion sections.
It should generate a concise, coherent project record rather than dump logs.
## 9.7 Notion failure behavior
If Notion is unavailable:
- project operation continues;
- documentation job becomes retryable;
- UI reports stale Notion synchronization;
- no project state or memory is lost;
- later sync resumes idempotently.
## 9.8 Additional Notion Knowledge Sources
Each project has exactly one dedicated **Project Record** created and maintained by PRIME plus zero or more additional operator-attached Notion knowledge pages.
**Dedicated Project Record**
- PRIME Documentation Agent may read it;
- PRIME may write only explicitly managed regions;
- user-managed regions remain protected;
- it is the canonical human-readable projection of project state.
**Additional Knowledge Sources**
- existing Notion pages may be attached to the project;
- they are read-only from PRIME's automated-documentation perspective;
- PRIME indexes their authorized user-authored content into the project-scoped Knowledge/Search layer with block/page provenance; a specific statement reaches Hindsight only through the explicit memory-admission rules in §9.4/§10, never merely because the page is attached;
- the Documentation Agent must never rewrite arbitrary attached research/knowledge pages;
- sources can be enabled, disabled, detached, and re-synchronized independently;
- disabling/detaching a source immediately removes it from current project retrieval/Ask context and emits a source-retraction event; cached/indexed copies are purged according to policy, and any memory previously promoted from that source is marked for provenance review/tombstone rather than remaining silently current;
- retained historical ingestion revisions may remain available to Time Lens/audit when policy permits, but the operator may choose a **local privacy purge** that removes PRIME-retained historical content/caches for the detached source while preserving only minimal non-content audit tombstones. PRIME cannot claim to delete the original Notion page it does not own.
A `KnowledgeSource` binding stores source type, external identifier/URL, access mode, last sync, content hashes/revisions where available, status, and project scope.
## 9.9 Notion loop and conflict prevention
PRIME-managed Notion writes must be excluded from user-knowledge ingestion so the system cannot learn its own generated prose and recursively amplify it. Managed block IDs/revisions/hashes are persisted. Self-generated Notion change events are suppressed or recognized idempotently.
If the operator manually edits a PRIME-managed block, PRIME must not silently overwrite it. The page enters a **managed-content conflict** state showing the changed block, PRIME's expected projection, and repair options. User-authored regions are never treated as conflicts merely because their content changes.
---
# 10. PRIME Memory — Product Requirements
## 10.1 Purpose
Memory exists so an AI coding agent can recover important project history and rationale without reconstructing the entire codebase or rereading months of artifacts.
The memory system must be **high-signal, project-isolated, provenance-rich, temporal, searchable, and replaceable at the backend layer**.
## 10.2 What should become memory
High-value examples:
- architectural decisions and rationale;
- why an approach was rejected;
- failed experiments and failure causes;
- validation outcomes;
- important operator observations;
- environment-specific quirks;
- deployment lessons;
- recurring defects;
- important constraints discovered during work;
- successful procedures;
- unresolved questions;
- changes in assumptions;
- important design intent not obvious from code;
- consequential agent discoveries;
- lessons that would otherwise need reconstruction.
## 10.3 What should not become durable memory by default
Avoid low-value noise such as:
- every file edit;
- routine test invocations;
- trivial refactors evident from Git;
- temporary chain-of-thought;
- duplicate observations;
- secrets;
- raw dependency/vendor content;
- whole source files when the live repository is authoritative.
## 10.4 Memory types
### Source Event Ledger
Immutable observations/events used as provenance.
Examples:
- user supplied a statement;
- Notion block changed;
- Git commit observed;
- agent explicitly recorded a result;
- validation failed;
- `.agent` state changed.
### Episodic memory
Things that happened in project history.
Example: an attempted architecture, what happened, why it failed, and what followed.
### Semantic memory
Durable facts/knowledge believed about the project, with provenance and temporal validity.
### Procedural memory
How to successfully perform recurring project-specific operations.
### Decision memory
Important accepted decisions with rationale, alternatives, consequences, and supersession.
### Failure/lesson memory
High-value failed approaches, causes, diagnostic signatures, and resolutions.
### Hypothesis/prediction memory
Explicitly non-factual derived expectations with confidence and validation status.
Predictions must never be promoted to semantic fact merely because a model generated them.
## 10.5 Hindsight
Hindsight is the **selected V1 memory engine** behind the PRIME-owned adapter. One PRIME project maps to exactly one Hindsight bank. Hindsight owns its supported world facts, experiences, observations, entities/relationships, temporal organization, retrieval, Reflect capability, and Mental Models. PRIME must not build a parallel custom episodic/semantic/vector/graph memory platform around it. PRIME's canonical database stores project↔bank binding, policy/audit/provenance metadata needed by PRIME, and adapter/job state rather than duplicating Hindsight's memory corpus. Hindsight is used for:
- entities;
- relationships;
- temporal evolution;
- episode ingestion;
- semantic/graph retrieval.
However, Hindsight is an implementation dependency behind a PRIME-owned memory interface.
PRIME must own:
- project isolation;
- memory IDs;
- provenance contract;
- source ledger;
- access control;
- API/MCP contract;
- retention/supersession policy.
If Hindsight is replaced later, agent-facing behavior should remain stable.
## 10.6 Memory storage architecture
Conceptual design:
```plain text
             PRIME MEMORY API
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
Source/Event DB   Hindsight    Retrieval Index
provenance        temporal     semantic/vector
immutable-ish     graph        acceleration
       └────────────┼────────────┘
                    ▼
              Context Compiler
                    │
                    ▼
                 PRIME MCP
```
Hindsight is the single durable agent-memory engine for V1. Repository indexes/search, PRIME canonical metadata, event/audit records, and Notion projections remain separate because they are **not memory backends**. Do not add another vector database, graph database, or custom episodic/semantic memory store unless a measured Hindsight limitation is documented and this specification is intentionally revised.
## 10.7 Salience and memory admission
Agent-submitted memory should include an explicit type and rationale.
Automatic memory admission must evaluate:
- durability;
- novelty;
- future usefulness;
- evidence quality;
- duplication;
- project relevance;
- sensitivity.
Low-value observations may remain in short-lived/event history without being promoted to durable memory.
## 10.8 Supersession, correction, and Hindsight invalidation
Memory must support:
- current;
- superseded;
- contradicted;
- uncertain;
- archived;
- rejected/incorrect.
New information should normally supersede rather than destructively erase historical knowledge.
PRIME must not assume that Hindsight exposes arbitrary in-place editing of every extracted memory unit. Every PRIME-originated retain operation must therefore use a stable, unique Hindsight `document_id` and store that binding in PRIME's canonical source ledger. The ledger preserves the operator/agent submission or authoritative source event needed to reconstruct the retained document, while Hindsight remains responsible for extraction, observations, entity/temporal relationships, recall, Reflect, and Mental Models.
Correction behavior is mandatory:
- PRIME recall/context results are filtered through PRIME's canonical memory status so superseded, rejected, archived, branch-abandoned, or otherwise invalid records do not silently resurface as current guidance;
- when an exact retained source document must be removed or replaced, the Hindsight adapter uses supported document-level delete/reprocess behavior rather than depending on opaque extracted-memory IDs;
- corrected replacement content receives a new PRIME memory/source revision and explicit supersession link;
- observations derived from corrected/deleted evidence must be invalidated/reconsolidated using supported Hindsight behavior where available;
- if backend invalidation semantics are insufficient or version-dependent, PRIME must be capable of rebuilding the project's Hindsight bank from the canonical retained-source ledger and current correction/tombstone state.
The Memory Inspector must clearly distinguish 'hidden from normal recall by PRIME policy' from 'physically removed from Hindsight'. Destructive backend deletion remains an operator/admin lifecycle action, not a normal coding-agent capability.
## 10.9 Provenance
Every durable memory must be traceable to one or more source references whenever possible.
Examples:
- Git commit/hash;
- file/path + content hash;
- `.agent` file + revision;
- Notion page/block;
- agent observation event;
- validation artifact;
- user statement.
## 10.10 Secret and sensitive-data handling
Do not ingest recognized secrets into memory or external model prompts.
Provide configurable redaction/filtering for:
- tokens;
- API keys;
- credentials;
- `.env` files;
- private keys;
- known secret patterns.
## 10.11 Automatic authoritative-event memory ingestion
Durable memory must not depend exclusively on a coding agent remembering to call MCP. The authority event pipeline should automatically retain consequential project events into the project's Hindsight bank when the approved AuthorityFileContract classifies them as memory-worthy.
Typical automatic inputs include:
- accepted outcomes;
- new learnings;
- decisions and rationale;
- recorded failures and resolutions;
- consequential validation failures/successes;
- explicit changes in assumptions or constraints.
The memory record must preserve the exact `.agent` source reference, revision/hash, directive/outcome/learning identifier when available, Git/branch/worktree context, event ID, and ingestion timestamp. Automatic ingestion must still apply secret filtering, deduplication, salience, and project isolation.
Codex explicit memory writes remain important for durable context that is **not already represented by authoritative project files**, such as debugging discoveries, environment quirks, reasoning rationale, or knowledge that should survive before it becomes formal project authority.
## 10.12 Existing-project warm start
When an established repository is added to PRIME, its memory bank should not begin artificially empty. Initial memory seeding may ingest high-value historical `.agent` authority records and operator-selected Notion knowledge with provenance. Do not indiscriminately convert the entire Git history or every source file into memories. Git and repository content remain searchable current evidence rather than memory by default.
## 10.13 Memory Inspector and Memory Activity
The Memory UI is a first-class operator surface, not an opaque backend. It must support browsing/searching by memory class, status, time, source, directive, branch/worktree, and related entities. Each record exposes content, epistemic class, status, creation/update time, provenance, source facts where applicable, relationships, and whether it is source-grounded or derived.
Operator actions include **view source**, **mark incorrect**, **mark duplicate**, **supersede**, **archive**, **report problem**, and **+ Remember / Add Project Observation**. Direct operator capture creates a project-scoped, provenance-labeled operator memory/observation without pretending it came from repository authority. The capture flow requires an explicit epistemic class (for example observation, constraint, lesson, environment fact, hypothesis) and makes clear that durable memory is not the same thing as changing `.agent` authority. These actions preserve history rather than destructively rewriting evidence.
The project also exposes **AI Memory Activity**, showing when a coding agent requested context/recall, which memory records were returned, approximate token budget, and when it stored or reported memory. This audit trail is project-scoped and is intended to answer questions such as why an agent may have acted on particular historical context.
---
# 11. PRIME MCP — Coding-Agent Contract
## 11.1 Core rule
A PRIME MCP connection is **project-bound**.
The server derives project scope from the authenticated MCP identity/session. The model must not be able to override project scope with an arbitrary parameter.
## 11.2 Capability mapping and canonical public surface
> **Do not implement a second/expanded MCP surface from descriptive capability names in this section. The canonical V1 public MCP contains only the six tools defined in §4.7.7 and §11.6.** Any older/descriptive operation below is an internal capability that must be mapped behind those six tools.
### Project context
**Project-summary capability**
- concise current project identity/state;
- progress/freshness;
- goal revision;
- important blockers;
- memory status.
**Project-goal capability**
- returns current authoritative `PROJECT_GOAL.md` or structured rendering.
**Project-status capability**
- returns current derived/project health metadata without editing anything.
**Context-compiler capability** (public form: `prime_memory_context`)
- accepts a bounded objective/question;
- retrieves relevant authority, memory, history, and source references;
- returns a compact context package rather than dumping the entire project.
### Memory retrieval
**Memory-search capability** (public form: `prime_memory_recall`)
- semantic/structured search over durable memory in the bound project.
`prime_memory_get`
- retrieve full memory record and provenance.
`prime_memory_timeline`
- retrieve relevant chronological memories/events for a subject.
**Decision/rationale filter** through `prime_memory_recall`
- find prior decisions and rationale.
**Failure/lesson filter** through `prime_memory_recall`
- find prior failures/lessons matching a problem.
**Procedure filter** through `prime_memory_recall`
- find project-specific procedures.
**Evidence/provenance filter** through `prime_memory_recall`
- locate validation/evidence-related memory records.
### Memory write
`prime_memory_store`
- explicitly propose/store a durable memory with type, summary, details, source references, salience, and confidence where relevant.
Supersession is performed through `prime_memory_store` using `supersedes_id` plus a reason, preserving the prior record and history.
Observations are stored through `prime_memory_store` with `kind=observation` and derived/source provenance fields.
## 11.3 `prime_memory_context` behavior
Example request:
```json
{
  "objective": "Fix intermittent persistence failure",
  "max_tokens": 6000
}
```
Example conceptual response:
```plain text
PROJECT AUTHORITY
- relevant goal constraints
- relevant .agent authority references

RELEVANT MEMORY
- previous SQLite locking incident
- earlier failed retry implementation
- persistence architecture decision

CURRENT PROJECT STATE
- relevant goal items/status
- current blocker/evidence

SUGGESTED REPOSITORY LOCATIONS
- src/storage/
- tests/persistence/

PROVENANCE
- source references for every important claim
```
The MCP does not need to send whole repository files because the coding agent already has repository access in its normal environment.
## 11.4 Agent memory-use expectations
The project's bootstrapped agent instructions should tell compatible coding agents to:
- query PRIME when historical context/rationale is relevant;
- store consequential lessons, decisions, failures, discoveries, and important operational knowledge;
- avoid storing trivial changes already obvious from Git;
- preserve provenance;
- correct/supersede stale memory when discovered;
- never assume memory is more authoritative than current repository/`.agent` truth.
## 11.5 MCP degraded mode
If memory/MCP is unavailable:
- coding must remain possible from repository + `.agent`;
- PRIME should clearly report memory unavailable;
- agents should fail gracefully rather than invent retrieved context;
- pending memory writes may be retried if safely journaled.
## 11.6 Canonical V1 PRIME Memory MCP schemas
The public MCP exposes exactly these six project-bound tools. The authenticated MCP session supplies `project_id`, client identity, and session identity; none of these can be overridden by model arguments.
### `prime_memory_store`
Purpose: store consequential durable context or supersede an existing memory.
Request semantics:
```json
{
  "kind": "learning | decision_rationale | failure | procedure | environment | constraint | observation | experience | world_fact | hypothesis",
  "summary": "short human-readable title",
  "content": "durable context",
  "source_refs": ["optional explicit refs already known to the agent"],
  "working_context": {
    "git_ref": "optional branch/ref hint",
    "git_commit": "optional HEAD hint",
    "worktree_path_or_id": "optional working-tree hint"
  },
  "salience": "normal | high | critical",
  "confidence": 0.0,
  "supersedes_id": "optional memory id",
  "supersession_reason": "required when supersedes_id is supplied"
}
```
The MCP session always supplies project/client/session identity. `working_context` is optional because not every MCP client exposes cwd/worktree metadata. PRIME validates any supplied ref/commit/worktree hint against the bound project's observed Git/worktree state when possible and records whether the context is `verified`, `client_claimed`, or `unknown`. A model/client can never use this field to switch projects or access another repository. If multiple active worktrees exist and PRIME cannot reliably identify the caller's worktree, it must record **unknown/ambiguous working context rather than guess**.
Server automatically enriches provenance with project/client/session, timestamp, verified canonical/working Git ref and commit when available, worktree identity, current directive/outcome context when deterministically known, and event correlation. Secret/privacy filters run before persistence.
Response semantics:
```json
{
  "status": "stored | queued | duplicate | rejected | degraded",
  "memory_id": "PRIME id when accepted",
  "hindsight_document_id": "internal source-document binding when accepted",
  "operation_id": "backend async operation when applicable",
  "duplicate_of": "id when deduplicated",
  "durability_verified": true,
  "provenance_refs": [],
  "reason": "optional rejection/degraded explanation"
}
```
`stored` means PRIME has verified durable Hindsight persistence sufficiently for the configured backend/version. `queued` means the source record is durably journaled by PRIME but Hindsight extraction/indexing is still pending; `durability_verified` is false until completion. The adapter must track Hindsight async operations where used and must never report an unverified queued/failed retain as durably stored. This explicitly protects against silent backend/indexing failures.
PRIME must not return `stored` unless durable persistence has been verified according to the Hindsight adapter contract.
### `prime_memory_recall`
Purpose: bounded high-signal historical recall.
```json
{
  "query": "what the agent needs to know",
  "kinds": ["optional filters"],
  "time_from": "optional ISO timestamp",
  "time_to": "optional ISO timestamp",
  "max_results": 8,
  "max_tokens": 4000,
  "include_derived": true
}
```
Hard limits must be enforced server-side. Results include memory ID, kind/epistemic class, summary/content excerpt, current/superseded/contradicted status, relevance/ranking information when useful, source/provenance refs, and supporting source facts for derived observations when available.
### `prime_memory_timeline`
Purpose: chronological memory/history retrieval.
```json
{
  "time_from": "optional ISO timestamp",
  "time_to": "optional ISO timestamp",
  "kinds": ["optional filters"],
  "max_results": 50
}
```
Return ordered bounded records with IDs, type/status, timestamp, summary, and provenance links.
### `prime_memory_get`
Purpose: inspect one exact memory.
```json
{"memory_id":"..."}
```
Return full operator-safe record, epistemic status, provenance, source facts/relationships when available, supersession/contradiction history, and branch/worktree context.
### `prime_memory_report_problem`
Purpose: let an agent report that a memory may be wrong/stale/duplicate/misleading without granting destructive memory authority.
```json
{
  "memory_id": "...",
  "problem": "incorrect | stale | duplicate | bad_provenance | misleading | other",
  "note": "why"
}
```
This creates an auditable correction/review signal. It does not silently delete or rewrite the underlying record.
### `prime_memory_context`
Purpose: task-startup context compilation.
```json
{
  "objective": "current engineering objective",
  "max_tokens": 6000,
  "include_recent_activity": true,
  "include_authority_refs": true
}
```
Return a bounded package containing relevant memory, important authority/goal references, current project/progress/work context, known failures/lessons, and suggested repository locations/references. It does **not** return entire source files; the coding agent reads current repository files directly. Derived claims are labeled and provenance is included.
### Common MCP errors
At minimum normalize:
```plain text
INVALID_INPUT
PROJECT_SCOPE_VIOLATION
MEMORY_BACKEND_UNAVAILABLE
DURABILITY_UNVERIFIED
PRIVACY_POLICY_BLOCKED
SOURCE_UNAVAILABLE
RESULT_BUDGET_EXCEEDED
RATE_LIMITED
INTERNAL_ERROR
```
Errors must never be converted into invented memory results.
Memory improves continuity; it must not become a single point that makes the repository unusable.
---
# 12. Repository Index and Retrieval
## 12.1 Purpose
PRIME needs enough repository understanding to support progress assessment, documentation, memory provenance, and context compilation.
This is not a replacement code-intelligence IDE.
## 12.2 Incremental indexing
Initial scan builds:
- file manifest;
- language/type metadata;
- content hashes;
- selectively generated summaries/embeddings where useful;
- Git revision linkage.
Subsequent updates process changed files only.
## 12.3 File content policy
Store metadata and derived retrieval data where possible rather than duplicating entire repositories in PRIME storage.
The live repository remains authoritative.
## 12.4 Retrieval
Repository retrieval may combine:
- filename/path search;
- text search;
- semantic search over approved chunks/summaries;
- Git metadata;
- optional structural symbol indexing.
This retrieval is available internally to progress/documentation/context services. Direct source editing is not.
## 12.5 Canonical branch and worktree awareness
PRIME must distinguish **canonical project truth** from parallel or experimental Git work. Each project stores a canonical Git target, normally a configured branch/ref such as `main`, plus repository identity/fingerprint data.
Progress scoring, living Notion documentation, accepted project state, and automatic authoritative memory ingestion must use the canonical target unless the approved authority explicitly defines another rule.
PRIME may discover and display active branches/worktrees as **Active Work**, including branch/ref, worktree path, HEAD, dirty state, related directive when deterministically known, and merge status. Unmerged experimental work must not silently become canonical project history.
Memories created while working on a branch/worktree should retain branch, commit, worktree/session identity, and later merge/acceptance state where determinable. PRIME should be able to mark such memories as branch-scoped, merged into canonical, abandoned, or unknown without erasing their historical value.
## 12.6 Repository relocation / rebinding
A managed project can move to another path or machine without becoming a new project. PRIME provides a protected **Move / Rebind Repository** workflow that verifies the new repository identity using Git root/remotes/history/fingerprint evidence, rebinds the same `project_id` to the new node/path, restarts watchers/indexes, and preserves Notion, Hindsight bank, progress history, activity, AI connections, and project identity. Accidental binding to an unrelated directory must fail safely.
---
# 13. Event and Job System
## 13.1 Normalized event envelope
```json
{
  "event_id": "...",
  "project_id": "...",
  "node_id": "...",
  "type": "repo.file.modified",
  "occurred_at": "...",
  "observed_at": "...",
  "project_sequence": 123,
  "source_revision": "...",
  "source_ref": "...",
  "payload": {},
  "dedupe_key": "..."
}
```
### Time and ordering semantics
All server-generated timestamps are stored as UTC instants and rendered in the operator's configured/local timezone. `occurred_at` represents best-known source/event time and may originate from filesystem/Git/node metadata; it is **not trusted as the sole ordering authority** because node clocks can drift and Git author dates can be arbitrary. `observed_at` is PRIME Core receipt/observation time. Causal ordering for projections uses project sequence/source revision/Git evidence plus idempotency rules, not wall-clock sorting alone. PRIME monitors material Node clock skew and surfaces it in Diagnostics. Historical Git author/committer timestamps remain evidence metadata rather than authoritative event sequence.
## 13.2 Important event types
**Removal/retraction is a first-class event, not absence of data.** The `AuthorityFileContract` must provide stable record identity where an authority file contains logical records and define add/update/remove/retract semantics. If a directive, outcome, learning, decision, risk, validation, Evidence item, Notion knowledge item, or other previously observed source is deleted/retracted, PRIME emits an explicit removal/retraction event containing the prior source identity/hash where available. Current projections/search stop presenting the item as current; dependent progress/documentation is invalidated; automatically derived memory is tombstoned/superseded according to policy; and historical/Time Lens evidence remains available unless the operator performs a privacy purge.
Project events must also distinguish `goal.change_detected` from `goal.revision_approved`/`goal.revision_rejected`; detection of a file change is not itself approval of a new product goal.
```plain text
project.created
project.ready
project.archived
project.removed
project.deletion.requested
project.deleted

node.online
node.offline

repo.file.created
repo.file.modified
repo.file.deleted
repo.bulk_change
git.head.changed

agent.authority.changed
agent.goal.changed

memory.created
memory.superseded

notion.user_content.changed
notion.sync.requested
notion.sync.completed
notion.sync.failed

progress.stale
progress.assessment.requested
progress.assessment.completed
progress.assessment.failed
```
## 13.3 Jobs
Background jobs must be:
- idempotent where possible;
- retryable with bounded exponential backoff;
- observable;
- project-scoped;
- cancellable when safe;
- deduplicated/coalesced for bursty repository activity.
Recommended job types:
- repository reconciliation;
- changed-file ingestion;
- progress assessment;
- Notion refresh;
- memory extraction/admission;
- graph/index update;
- cleanup/retention.
## 13.4 Durable multi-system workflow orchestration
Provisioning, Fork/Clone, archive/delete/purge, repository rebind, backup/restore, authority migration, Notion creation/rebind, and Hindsight-bank lifecycle span systems that cannot participate in one database transaction. PRIME must therefore implement these as **durable resumable workflows/sagas**, not fragile request handlers.
Requirements:
- persist workflow ID, type, project, requested actor, current step, completed steps, retry state, and terminal result;
- make each step idempotent and safe to retry after process/machine restart;
- use explicit compensating cleanup where reversal is safe, and otherwise preserve the partial resource with a visible repair state rather than pretending rollback occurred;
- never leave hidden orphan Notion pages, Hindsight banks, repo directories, credentials, or project registrations after a failed workflow without surfacing them;
- serialize mutually exclusive lifecycle workflows for the same project;
- support operator-visible resume/retry/repair/cancel where safe;
- use reconciliation to discover orphan/partial external resources after crashes.
A workflow is successful only when its durable completion state and required postconditions are verified. HTTP success from one external service is not equivalent to completion of the overall lifecycle operation.
---
# 14. Canonical Data Model
This is a conceptual minimum. The implementation may normalize further, but must preserve these semantics.
## 14.1 Project
```plain text
id
name
description
image_ref
lifecycle_state
connectivity_state
freshness_state
work_condition
node_id
repository_path
repository_git_root
repository_identity_fingerprint
canonical_git_ref
notion_page_id
notion_page_url
authority_template_version
created_at
updated_at
last_activity_at
last_repo_sync_at
last_notion_sync_at
last_progress_assessment_id
hindsight_bank_id
repository_index_namespace_id
last_operator_visit_checkpoint
completed_at
archived_at
```
## 14.2 Node
```plain text
id
name
os
version
capabilities
allowed_roots
public_key / auth identity
status
last_seen_at
created_at
```
## 14.3 RepositoryFile
Metadata only unless content retention is explicitly necessary.
```plain text
project_id
relative_path
kind
size
content_hash
modified_at
last_indexed_at
index_status
```
## 14.4 GoalRevision
```plain text
id
project_id
content_hash
content_snapshot_or_ref
observed_at
source_revision
```
## 14.5 GoalItem
```plain text
id
project_id
goal_revision_id
stable_key
title
description
weight
required
acceptance_expectations
```
## 14.6 ProgressAssessment
```plain text
id
project_id
goal_revision_id
repository_revision
progress_percent
confidence
summary
blockers
uncertainties
model/provider metadata
prompt/schema version
created_at
```
## 14.7 ProgressGoalItemResult
```plain text
assessment_id
goal_item_id
status
completion
confidence
explanation
evidence_refs
missing_evidence
blockers
```
## 14.8 MemoryRecord
```plain text
id
project_id
type
status
title
summary
body
confidence
salience
valid_from
valid_to
supersedes_id
created_by
created_at
updated_at
```
## 14.9 SourceReference
```plain text
id
project_id
source_type
uri/path/page/block/commit identifier
source_revision / commit / external revision when available
content_hash
observed_at
bounded_evidence_excerpt_or_snapshot_ref when policy permits
metadata
```
### Citation durability contract
A citation is a reference to **the evidence PRIME actually used**, not merely a convenient path to whatever exists now. Ask, Progress, Documentation, Memory Inspector, Alignment, Time Lens and other evidence-backed surfaces must attach a `SourceReference` with sufficient revision/hash identity to detect drift.
When the operator opens a citation:
- if the current source still matches the referenced hash/revision, open the current source at the referenced location;
- if the source changed but the exact historical Git/Authority/Notion-projection/Evidence revision is retained, open that historical revision and clearly label it historical;
- if the exact content is no longer retained, show the bounded captured evidence excerpt/metadata when available and mark the source **CHANGED / HISTORICAL CONTENT UNAVAILABLE** rather than silently opening different text as proof;
- external sources whose revision cannot be proven are labeled with their observed time/hash and current availability.
Citation resolution never substitutes a newer source for an older cited source without warning. Secret/redaction policy applies to stored excerpts and citation rendering.
## 14.10 MemorySourceLink
Many-to-many relation between MemoryRecord and SourceReference.
## 14.11 Event
Normalized append-oriented project/system event record.
## 14.12 Job
```plain text
id
project_id optional
type
status
attempts
dedupe_key
payload
scheduled_at
started_at
finished_at
last_error
```
## 14.13 AuditEvent
Security/lifecycle audit record for sensitive actions, especially:
- project creation;
- project removal;
- repository archive/delete;
- authority bootstrap;
- credential rotation;
- MCP token issuance;
- Notion binding changes.
## 14.14 Additional product entities
Implementation must also preserve the following semantics, whether normalized into dedicated tables or equivalent typed records:
### KnowledgeSource
```plain text
id
project_id
source_type
external_id / url
access_mode
status
last_synced_at
source_revision / content_hash
created_at
```
### ProjectVisit
Tracks operator project-open/last-seen checkpoints used to generate **Since You Were Here** without relying on guesswork.
### AttentionItem
```plain text
id
project_id
type
severity
status
source_ref
message
created_at
resolved_at
```
Attention items are deterministic/project-derived conditions, not cross-project strategic reasoning.
### GoalAlignmentAssessment
Stores alignment status, explanation, evidence refs, model/schema revision, and created time separately from progress percentage.
### MilestoneProjection
Derived grouping of GoalItems; never a second task authority.
### GitWorkContext
Represents canonical ref plus discovered branch/worktree state and merge/acceptance metadata.
### AIConnection
```plain text
id
project_id
client_type
credential_ref
capabilities
status
last_seen_at
created_at
revoked_at
```
Secrets are stored through secure credential storage, never in repository content.
### MemoryAccessEvent
Audit record of recall/context/store/report operations including agent/session, query/objective, returned memory IDs, token/result budgets, timestamp, and status.
### OperatorCorrection
Project-scoped reviewed correction/challenge linked to the derived artifact being disputed.
### UsageRecord
Tracks model/service usage and estimated cost by project/function/provider/model where available.
### Notification
High-signal operator notification with source condition and lifecycle.
### BackupRecord
Backup/export/restore metadata, verification status, manifest, and created/restored timestamps.
### AuthorityRevision
Compact retained history of meaningful `.agent` authority changes used for audit/Time Lens reconstruction. Includes project, authority file/path, revision ID, full authority text where policy permits, content hash, source event, observed time, optional canonical commit/ref, and gap/integrity metadata. Historical copies are evidence of what PRIME observed and never replace the live `.agent` authority.
### NotionProjectionRevision
Versioned history of PRIME-managed Notion projection sections. Includes project, managed-section identity, rendered content/hash or reversible delta strategy, source revision set, managed block mapping, generated/synced times, and model/prompt version where applicable. User-authored Notion history is not guaranteed by this record.
### ProjectForkRecord
Auditable lineage record containing parent project ID, child project ID, source canonical commit/tag, target repository identity/path, creation time, remote-retention choice, explicitly inherited memory/knowledge references, and result/status. This record provides provenance only; it does not permit runtime cross-project retrieval.
### RemoteAccessState
Non-secret Tailscale/remote-access status including enabled/disabled, Core host identity, Serve URL/health, MagicDNS/HTTPS state where observable, private-vs-Funnel safety result, last verification time, and actionable error state. Authentication keys/tokens are never stored in this status record.
### WorkflowRun
Durable lifecycle/saga record containing workflow ID/type, project where applicable, actor, requested time, current step, completed-step ledger, resource references created during the workflow, retry/compensation state, last error, and terminal status.
---
# 15. Core API Boundaries
Exact URL design may evolve, but these capability boundaries are required.
## 15.1 Projects
```plain text
GET    /projects
POST   /projects
GET    /projects/{id}
PATCH  /projects/{id}/metadata
POST   /projects/{id}/archive
POST   /projects/{id}/fork/preflight
POST   /projects/{id}/fork
POST   /projects/{id}/remove
POST   /projects/{id}/delete-request
POST   /projects/{id}/delete-confirm
```
Metadata updates may change PRIME-owned identity/configuration only, not repository source.
## 15.2 Nodes
```plain text
GET    /nodes
POST   /nodes/enroll
GET    /nodes/{id}
GET    /nodes/{id}/roots
POST   /nodes/{id}/validate-path
```
## 15.3 Repository read model
```plain text
GET /projects/{id}/repo/tree
GET /projects/{id}/repo/file
GET /projects/{id}/repo/git
GET /projects/{id}/repo/search
```
## 15.4 Authority
```plain text
GET  /projects/{id}/authority
GET  /projects/{id}/authority/file
POST /projects/{id}/bootstrap
```
Bootstrap write capability is lifecycle-scoped and unavailable as an ordinary monitoring endpoint after provisioning.
## 15.5 Progress
```plain text
GET  /projects/{id}/progress
GET  /projects/{id}/progress/history
POST /projects/{id}/progress/reassess
```
## 15.6 Memory
Internal API mirrors project-scoped MCP capabilities with stronger service authentication.
## 15.7 Notion
```plain text
GET  /projects/{id}/notion/status
POST /projects/{id}/notion/refresh
POST /projects/{id}/notion/rebind
```
## 15.8 Ask, search, recap, attention, and integrity
```plain text
POST /projects/{id}/ask
GET  /projects/{id}/search
GET  /projects/{id}/since-last-visit
GET  /projects/{id}/attention
GET  /projects/{id}/integrity
GET  /projects/{id}/alignment
GET  /projects/{id}/milestones
```
Ask is project-bound and read-only. Search returns source-grouped deterministic results where possible. Derived answers return citations and epistemic/source labels.
## 15.9 Git work context and repository rebinding
```plain text
GET  /projects/{id}/git/worktrees
GET  /projects/{id}/git/branches
GET  /projects/{id}/git/canonical
POST /projects/{id}/repository/rebind-validate
POST /projects/{id}/repository/rebind-confirm
```
## 15.10 Knowledge sources
```plain text
GET    /projects/{id}/knowledge
POST   /projects/{id}/knowledge/notion
PATCH  /projects/{id}/knowledge/{source_id}
DELETE /projects/{id}/knowledge/{source_id}
POST   /projects/{id}/knowledge/{source_id}/refresh
```
## 15.11 AI connections and context export
```plain text
GET    /projects/{id}/ai-connections
POST   /projects/{id}/ai-connections
POST   /projects/{id}/ai-connections/{connection_id}/rotate
DELETE /projects/{id}/ai-connections/{connection_id}
POST   /projects/{id}/context-export
```
The UI may generate client-specific MCP configuration snippets, but secrets must never be committed into the managed repository.
## 15.12 Completion, corrections, notifications, backup
```plain text
POST /projects/{id}/completion/review
POST /projects/{id}/completion/confirm
POST /projects/{id}/pause
POST /projects/{id}/resume
POST /projects/{id}/corrections
GET  /notifications
POST /notifications/{id}/dismiss
POST /backups
GET  /backups
POST /backups/{id}/restore
```
## 15.13 Time Lens
```plain text
GET  /projects/{id}/time-lens/checkpoints
GET  /projects/{id}/time-lens/state
GET  /projects/{id}/time-lens/brain
POST /projects/{id}/time-lens/ask
```
All Time Lens APIs require an explicit historical selector (`as_of`, commit/ref, assessment ID or equivalent) and return per-source reconstruction status. They are read-only.
## 15.14 Remote access
```plain text
GET  /system/remote-access
POST /system/remote-access/tailscale/configure
POST /system/remote-access/tailscale/verify
POST /system/remote-access/tailscale/disable
```
Remote-access configuration operations are fixed allowlisted system operations, not arbitrary shell execution. Any implementation that invokes the local Tailscale CLI must construct known-safe arguments internally and never accept raw command text from the browser/model.
---
# 16. UI/UX Specification
## 16.1 Visual direction
The interface should be:
- modern;
- clean;
- minimal;
- dark/light capable;
- visually rich enough to make projects feel tangible;
- uncluttered;
- fast;
- responsive;
- usable on desktop and tablet, with reasonable mobile read access.
Avoid enterprise-dashboard density unless information genuinely requires it.
## 16.2 Home / Projects screen
Primary content is a card grid/list.
Each card should show:
- image;
- project name;
- progress health bar;
- percentage;
- confidence/freshness cue;
- project state;
- machine/node;
- last meaningful activity;
- optional blocker indicator.
Example:
```plain text
┌──────────────────────────────┐
│        [PROJECT IMAGE]       │
│                              │
│ GHOST                        │
│ ████████████████░░░ 82%      │
│ High confidence • 14m old    │
│ Active                       │
│ atlas-linux • /Projects/...  │
└──────────────────────────────┘
```
The screen includes a prominent **+ Add Project** action.
## 16.3 Project screen navigation
Recommended sections:
### Overview
- image/name;
- repository host/path;
- Git branch/HEAD/status;
- progress;
- confidence/freshness;
- project goal summary;
- current state;
- blockers;
- recent meaningful activity;
- Notion and MCP health.
### Goal
- full human-readable `PROJECT_GOAL.md`;
- goal revision/hash/time;
- goal-item decomposition;
- no silent edit control.
### Progress
- large health/progress bar;
- overall score;
- confidence;
- assessment age;
- goal-item list with weights and statuses;
- blocker list;
- uncertainties;
- evidence drilldown;
- assessment history.
### Repository
- read-only tree;
- file viewer;
- path/text search;
- Git metadata;
- clear read-only indicator.
### Authority
- `.agent` tree;
- file viewer;
- authority health;
- template version;
- warnings/drift.
### Memory
- semantic search;
- filters by memory type/status;
- timeline;
- provenance view;
- supersession chain;
- manual operator add/correct/supersede capability may be supported because memory is PRIME-owned, not repository code.
### Knowledge
- linked Notion page;
- synchronization status;
- last sync;
- link to open Notion;
- managed/user content health.
### Ask
Project-specific, read-only **Ask PRIME** interface grounded only in the current project's repository, `.agent`, Git, attached Notion knowledge, Hindsight memory, progress evidence, and activity. Answers must distinguish current source evidence, historical evidence, durable memory, derived interpretation, and unknowns, with clickable citations.
### Search
Unified project search across repository, `.agent`, Git, Notion knowledge, memory, and activity. Results are grouped by source rather than flattened into an opaque semantic ranking.
### Activity
Human-readable important chronology, not raw debug logs. Support filters for Code, Authority, Memory, Progress, Documentation, Git, and System, and show events such as directives/outcomes, repository changes, validation, memory use, progress changes, and Notion updates.
### AI Connections
Show connected coding agents/MCP clients, connection health, capabilities, last activity, credential rotation/revocation, and copyable configuration guidance. Support future MCP-compatible clients without making PRIME dependent on Codex.
### Settings
- name/image/description;
- node/path binding controls;
- Notion binding;
- memory/MCP status;
- refresh/reconciliation;
- archive/remove/delete controls.
## 16.4 Empty/loading/error states
Every surface must distinguish:
- no data yet;
- loading;
- stale;
- node offline;
- Notion offline;
- memory unavailable;
- assessment failed;
- permission error;
- malformed authority.
Never render stale data as silently current.
---
# 16A. Complete Operator Product Experience
This section defines the full user-facing product layer that makes PRIME useful even when the coding agent itself is functioning perfectly. PRIME is the place the operator goes to **understand a project without having to become the coding agent**.
The product must answer, at a glance or through grounded inquiry:
- What is this project?
- What changed while I was away?
- What is happening now?
- How close are we to the declared goal?
- Are we still aligned with that goal?
- What is blocked, stale, conflicted, or unhealthy?
- What does the project remember and why?
- What context has the AI coder been receiving from PRIME?
- What has been tried before?
- What requires my attention or judgment?
PRIME may explain, summarize, search, visualize, and surface conditions. It must not use these product features as a back door to autonomously direct engineering work.
## 16A.1 Global Home
The home screen is more than a project-card grid. It contains four primary operator surfaces:
### Projects
All active/paused/completed projects as cards or list rows showing image, name, progress, confidence/freshness, lifecycle, connectivity, important condition, node/path summary, and recent activity. The global project collection must remain manageable at scale: support name search plus deterministic filters/sorts for lifecycle, attention state, node/machine, recent activity, tags/labels, and archived/completed visibility. Allow operator-owned pin/favorite and lightweight tags/groups for organization; these are PRIME metadata only and do not create cross-project reasoning or coding-agent context.
### Needs Attention
A deterministic aggregation of project-scoped conditions requiring operator awareness. This is **not cross-project strategic reasoning**. PRIME simply surfaces independently detected conditions such as:
- progress assessment failure or significant regression;
- `PROJECT_GOAL.md` changed and progress is stale;
- invalid/incomplete authority;
- node/repository offline beyond configured threshold;
- Notion managed-content conflict or prolonged sync failure;
- Hindsight/MCP degraded;
- backup failure;
- project appears complete and requires completion review;
- unresolved project-knowledge conflict;
- repository rebind required.
Each attention item links directly to its source project and evidence. Attention items have severity, first-seen time, current status, and deterministic resolution rules where possible.
### Recently Active
Projects ordered by meaningful project activity, not filesystem noise. Activity may include accepted authority changes, outcomes, validation, canonical Git changes, progress changes, memory operations, or operator interaction.
### System Health
Concise global status for PRIME Core, Hindsight, Notion, registered Nodes, backups, AI provider, event/job queues, and current degraded conditions. Detailed diagnostics remain in Settings/Diagnostics.
## 16A.2 Since You Were Here
Every project tracks the operator's last meaningful project visit/checkpoint. On reopening, Overview presents a deterministic **Since You Were Here** summary built from the project event stream between the prior checkpoint and now.
The structured summary should include when applicable:
- directives added/completed/changed;
- outcomes recorded;
- new learnings/decisions/failures;
- canonical repository changes and affected areas;
- validation results;
- progress movement and confidence change;
- new blockers/conflicts;
- Notion documentation status;
- number/type of durable memories added;
- major AI Memory Activity;
- branch/worktree activity that has not reached canonical state.
An LLM may turn the bounded event set into readable prose, but the underlying counts/events remain directly inspectable. The operator controls when the checkpoint is advanced; simply loading a page must not accidentally erase unread-change context before it can be reviewed.
## 16A.3 Ask PRIME — project-specific Q&A
Each project has a dedicated **Ask** surface. Ask is always bound to exactly one project and is distinct from future Oracle.
Ask may retrieve from:
- current canonical repository/index;
- `.agent` authority;
- canonical Git history/state;
- attached Notion knowledge sources;
- dedicated project Notion record;
- Hindsight memory;
- progress/alignment evidence;
- project activity/event history.
Example questions include:
- Why was this architecture chosen?
- What is blocking the project?
- Where is authentication implemented?
- What did we try before this?
- What evidence supports this requirement being complete?
- What changed last week?
- Why did progress drop?
- What does the project goal require for offline behavior?
Every substantive answer must distinguish epistemic/source class:
```plain text
CURRENT SOURCE
HISTORICAL EVIDENCE
DURABLE MEMORY
DERIVED INTERPRETATION
UNKNOWN / INSUFFICIENT EVIDENCE
```
Important claims include clickable source references. Ask must state uncertainty rather than fabricate missing context. It has no write tools and cannot modify project state.
Ask conversation history is an operator convenience, **not durable project memory or authority by default**. Questions/answers may be retained as short-lived UI history under configurable retention, but they are excluded from Hindsight and Documentation Agent ingestion unless the operator explicitly chooses **Remember this / Save insight**. Saving an Ask result stores the operator-selected proposition with links to the answer's underlying evidence, not the model's hidden reasoning.
Operator feedback includes **This is wrong / stale / missed evidence**, which creates a correction record and may improve derived systems but never silently rewrites authority.
## 16A.4 Unified Project Search
Search is deterministic retrieval, not the same product as Ask. One query searches across source classes and groups results visibly by:
- Repository;
- `.agent` Authority;
- Git;
- Notion Knowledge;
- Memory;
- Activity.
Search supports exact/path/text queries and semantic assistance where configured, while preserving source grouping, project isolation, source links, and freshness. Searching for `sqlite`, for example, may return a source file, a learning, a failure memory, a Notion research note, and a validation event as separate clearly labeled results.
## 16A.5 Project Overview
Overview is an operator dashboard, not a generic status page. It should prioritize:
- project identity/image;
- canonical node/path/ref;
- lifecycle/connectivity/freshness/condition;
- current progress and confidence;
- Goal Alignment;
- derived milestones;
- current directive/current work when represented by authority;
- blockers/attention;
- **Since You Were Here**;
- integrity summary;
- Notion/MCP/memory health;
- last meaningful activity.
The screen should make the project understandable in seconds and provide drill-down rather than dense permanent panels.
## 16A.6 Project Integrity
Each project exposes an **Integrity** readout comparable to a project check-engine light. It validates structural continuity rather than software correctness.
Checks include when applicable:
- repository reachable and identity matches binding;
- canonical Git target resolvable;
- `.agent` authority package complete and valid;
- required coding-agent bridge such as root `AGENTS.md` present/recognized and still points to the current authority contract where applicable;
- `PROJECT_GOAL.md` valid/approved;
- no prolonged **authority-protocol lag** where material canonical repository activity continues without the directive/outcome/learning/validation updates required by the `AuthorityFileContract`; this is an advisory `AUTHORITY_STALE_SUSPECTED` condition until reviewed, not automatic proof that engineering work is invalid;
- authority template version known;
- no detected authority conflicts;
- repository index current or explicitly stale;
- progress assessment current;
- Notion projection current/no managed-content conflict;
- knowledge sources reachable;
- Hindsight bank healthy/project mapping valid;
- MCP scope/config healthy;
- recent backup verified;
- source references used by important memories still resolvable where feasible.
Integrity findings become AttentionItems when severity warrants. PRIME may recommend repair but does not silently modify authority after onboarding.
## 16A.7 Progress, alignment, milestones, and completion
The Progress experience combines four deliberately separate concepts:
**Progress** — evidence-backed estimate toward the approved goal.
**Alignment** — derived assessment of whether current work remains mapped to that goal.
**Milestones** — human-readable grouping of stable GoalItems.
**Completion** — operator-confirmed lifecycle decision after final evidence review.
Progress history is visualized over time with markers for goal revisions, failed validation, significant regressions, milestones, and completion. Every plotted value is inspectable. A project can regress legitimately when evidence fails **within the same approved baseline**. An approved goal/GoalModel change begins a new progress segment and must not be mislabeled as a like-for-like regression.
## 16A.8 Human correction system
PRIME must assume derived AI output can be wrong. All important derived surfaces provide bounded correction paths.
Examples:
- Memory: incorrect, duplicate, superseded, no longer relevant, bad provenance;
- Progress: missed evidence, wrong interpretation, stale source, bad GoalModel;
- Documentation: regenerate managed section, factual error, managed-content conflict;
- Ask: wrong/stale/missing evidence;
- Observation/Mental Model/Reflection/Dream: reject, question, supersede, keep as derived insight.
Corrections are audit/provenance events. They do not rewrite raw source evidence or hide historical mistakes.
## 16A.9 Memory product experience
Memory has three operator experiences:
### Memory Inspector
Browse/search world facts, experiences, decisions/rationale, failures, procedures, observations, mental models, reflections, and future dream outputs. Each item exposes status, epistemic class, provenance, related artifacts/entities, timestamps, and source evidence.
### Memory Timeline
Chronological view of significant memory creation, supersession, contradiction, observation, reflection, and model evolution.
### AI Memory Activity
Audit what coding agents actually asked PRIME Memory for and what PRIME returned, including objective/query, returned memory IDs, source types, approximate token/result budget, session/client, time, status, and agent memory stores/reports. The UI must not expose hidden model chain-of-thought; it shows tool requests/results and persisted records.
## 16A.10 Automatic memory capture and warm start
Consequential authority events are automatically admitted to Hindsight according to the AuthorityFileContract so continuity does not depend on agent discipline. Existing projects receive a bounded initial import from high-value `.agent` history and operator-selected Notion knowledge. The repository and complete Git history are not bulk-converted into memories.
## 16A.11 Knowledge
The Knowledge surface shows:
- the dedicated PRIME-managed Project Record;
- attached Notion Knowledge Sources;
- sync/access status;
- last ingestion time;
- read/write ownership boundary;
- source-specific refresh/detach controls;
- knowledge conflicts or unavailable sources.
Additional knowledge sources are read-only from the Documentation Agent's perspective. User content remains original evidence and can be recalled by Ask/memory with provenance.
## 16A.12 Project knowledge conflicts
PRIME may detect when high-value knowledge appears inconsistent, for example current code/authority says SQLite while an old memory says Postgres or a user Notion note proposes another architecture. PRIME must not silently decide the winner beyond applying the explicit authority hierarchy.
The UI can surface **Conflicting Project Knowledge** with:
- conflicting statements;
- source class/revision/date;
- authority rank where defined;
- current-source evidence;
- actions to inspect, mark a memory stale/superseded, or dismiss the conflict.
Brainstorming/proposals are not errors merely because they differ from current authority; conflict detection should focus on records represented as current/factual or otherwise likely to mislead retrieval.
## 16A.13 Repository, branches, and worktrees
Repository view includes file browsing/search plus canonical Git state and **Active Work**. PRIME must display discovered branches/worktrees separately from canonical project truth, including branch/ref, worktree path, HEAD, dirty state, related directive if deterministically known, and merged/accepted/abandoned/unknown status where possible.
Experimental/unmerged work cannot update living human documentation or goal completion as though accepted unless authority explicitly says otherwise.
## 16A.14 AI Connections
Each project has an **AI Connections** page supporting Codex and future MCP-compatible coding tools.
For every connection display:
- client type/name;
- connected/degraded/revoked state;
- last activity;
- allowed project-scoped capabilities;
- credential created/rotated time;
- rotate/revoke controls;
- generated configuration guidance/snippet.
Normal clients receive only their bound project. No global project-list or arbitrary project-ID switching is exposed. Credentials/config secrets are never written into Git or `.agent`.
During bootstrap PRIME must create or validate a minimal coding-agent bridge such as root `AGENTS.md` for Codex-compatible projects. Codex automatically discovers an instruction chain from `AGENTS.override.md` / `AGENTS.md` files from project root toward the active working directory, with more specific downstream guidance taking precedence; it does **not** automatically treat the arbitrary `.agent/` directory as the instruction source. The bridge is therefore the explicit handoff into PRIME authority, but PRIME must not assume a root bridge is the only Codex instruction file.
Before declaring a project AI-ready, PRIME inventories applicable root and nested Codex instruction files (`AGENTS.md`, `AGENTS.override.md`, and configured fallback names where known). Existing files are never silently overwritten. If a root file already exists, PRIME either validates that it already contains the required bridge semantics or presents an explicit operator-reviewed managed insertion/merge. Nested/more-specific instruction files remain user/repository-owned; PRIME surfaces their scope and flags instructions that appear to conflict with `.agent` authority, project isolation, goal protection, or other hard PRIME boundaries. Such a conflict is an Integrity/Needs Attention condition rather than something PRIME resolves by silently rewriting the file.
The bridge must:
- point to the approved `.agent` authority location and source-precedence rules;
- require the coding agent to read `PROJECT_GOAL.md` and the authority files relevant to the current task before substantive work;
- require re-reading relevant `.agent` state after authority-changing events or when continuing a long-running session, because Codex instruction discovery occurs at run/session startup rather than continuously reloading arbitrary authority files;
- explain when to use PRIME Memory MCP and what consequential `.agent` updates the AuthorityFileContract requires;
- state that Notion documentation is maintained separately by PRIME;
- remain deliberately small and avoid duplicating the full authority package so it stays within coding-agent instruction-discovery limits and avoids conflicting copies of the same rule.
For Codex, AI Connections should generate a current-compatible MCP configuration using project-scoped authentication. Prefer secret values from environment variables/secure credential storage (for example a bearer-token environment variable) rather than static secrets in repo config. If project `.codex/config.toml` guidance is offered, PRIME must warn that Codex only loads project config for trusted projects and must never write the token itself into Git.
### MCP transport capability
PRIME must not assume every coding client can reach a private LAN/tailnet endpoint. AI Connections identifies the client transport:
- **local/tailnet-reachable client** — connect directly to PRIME's private project MCP endpoint;
- **supported OpenAI cloud surface** — optionally use OpenAI's Secure MCP Tunnel (or its verified successor) so the private PRIME MCP server remains non-public while an outbound tunnel client relays project-bound requests;
- **client with no approved private/tunnel path** — live MCP is unavailable and PRIME offers the bounded Context Export workflow instead.
Secure MCP Tunnel is an optional AI-client transport, **not operator remote access and not a public endpoint**. It must be explicitly enabled, use a project-bound PRIME MCP grant behind the tunnel, expose only the six allowed PRIME Memory MCP tools, be revocable, and comply with the project's effective cloud/model-egress policy. If project policy forbids the OpenAI cloud surface receiving project context, tunnel use is disabled rather than silently bypassing that policy.
## 16A.15 Portable Project Context Package
PRIME remains useful with coding environments that do not support MCP. **Export Context** creates a bounded Markdown and/or JSON package containing selected project identity, approved goal, authority summary/references, current progress/alignment, current state, recent outcomes, key failures/lessons, unresolved questions, and selected high-value memories with provenance.
Exports are snapshots with revision/freshness metadata and privacy/redaction policy. They do not become new authority. Support copy-to-clipboard and file export where practical.
## 16A.16 Activity timeline
Activity is a coherent project timeline based on normalized events, not raw debug logs. It may show:
- authority/directive/outcome changes;
- canonical Git/repository changes;
- validation events;
- progress/alignment movement;
- memory creation/recall where operator-relevant;
- Documentation Agent updates/conflicts;
- Notion/knowledge changes;
- node/rebind/lifecycle events;
- backup/restore;
- AI connection changes.
Filters include All, Code, Authority, Memory, Progress, Documentation, Git, and System. Events link to evidence where available.
## 16A.17 Project relocation
Move/Rebind Repository is a normal Settings workflow. The operator chooses a target Node/path, PRIME verifies repository identity, shows mismatches, pauses affected watchers during transition, rebinds the same project identity, rebuilds disposable indexes/Brain projection as necessary, and verifies canonical state before declaring the rebind healthy.
## 16A.18 First-run setup wizard
A clean PRIME installation must have a guided first-run experience:
```plain text
1. Create/configure the single operator authentication
2. Verify PRIME Core storage
3. Configure AI provider/model and privacy defaults
4. Connect Notion
5. Start/verify Hindsight + PostgreSQL/pgvector
6. Enroll first PRIME Node
7. Configure approved repository roots
8. Configure backup location/policy
9. Configure/verify Tailscale remote access or explicitly leave remote access disabled
10. Run system health check
11. Add the first project
```
The wizard supports retry/degraded states and does not leave hidden half-configured dependencies.
## 16A.19 AI/provider and privacy settings
Global Settings provides provider/model configuration, service health, usage/cost, cloud-vs-local policy defaults, excluded content/path rules, secret detection behavior, and per-project overrides. A project configured `LOCAL_ONLY` must never have protected source content silently sent to a cloud provider.
## 16A.20 Usage and cost
Model-backed automation must be observable financially. PRIME records and presents estimated usage/cost by function/project/provider/model where available, including Documentation, Progress, Ask, Memory Processing, Reflect, and future Dreaming. The operator may configure warning thresholds and hard/soft limits. Optional automation should pause/degrade explicitly when a limit prevents execution rather than repeatedly retrying and spending more.
## 16A.21 Notifications
Notifications are intentionally restrained and high-signal. In-app notifications are required for material conditions such as:
- project completion review ready;
- significant progress regression;
- prolonged node/repository outage;
- invalid authority;
- Notion managed-content conflict;
- memory/MCP prolonged failure;
- backup failure;
- privacy/provider configuration blocking required service;
- repository rebind/conflict requiring input.
Do not notify for ordinary file changes, routine successful jobs, or every memory event. Browser/desktop delivery may be optional, but all notifications remain visible in PRIME until resolved/dismissed.
## 16A.22 Backup, export, and restore
Backup/restore is a first-class product surface, not merely an ops cron job.
A PRIME backup includes as appropriate:
- canonical PRIME database/project identities;
- progress/alignment history and GoalModels;
- Hindsight durable memory and provenance required for restoration;
- event/activity history;
- Notion/knowledge bindings and managed-projection metadata;
- authority-template versions/bundled configuration;
- project images;
- Project Brain presentation state if retained;
- AI-connection metadata without exporting plaintext secrets;
- settings/configuration necessary for recovery.
Repositories remain separately authoritative through their own filesystem/Git backups and are not silently copied into PRIME backup bundles by default. Notion remains externally authoritative. Backups must have a manifest/version, integrity verification, visible last-success state, and tested restore workflow.
Support a **project continuity export** for moving PRIME metadata/memory between compatible installations when practical.
## 16A.23 Schema, protocol, and dependency upgrade UX
PRIME Core DB schema, Core↔Node protocol, authority-template versions, MCP contracts, Hindsight version, and client connections will evolve. Upgrades require compatibility/preflight checks, transactional migrations where possible, pre-upgrade backup, version reporting, safe restart/retry behavior, and a documented rollback or restore path when migration cannot be reversed.
The UI should surface incompatible/outdated Nodes and memory backend versions rather than failing mysteriously.
## 16A.24 Existing-repository authority adoption
Attaching an existing repository must support four explicit paths:
1. **No ****`.agent`**** exists** — generate/review goal and bootstrap current template.
2. **Compatible current ****`.agent`**** exists** — adopt without overwriting and verify health.
3. **Known older authority version exists** — produce a migration preview and require explicit approval before changing files.
4. **Unknown/conflicting authority exists** — enter review-required state; do not overwrite.
Existing `PROJECT_GOAL.md` is preserved and reviewed/adopted rather than regenerated automatically. All bootstrap/migration writes are explicit lifecycle operations.
## 16A.25 AuthorityFileContract
Phase 0 must turn the final bundled `.agent` template into a machine-readable/documented `AuthorityFileContract`. For every authority file define:
- canonical filename/path;
- purpose and precedence;
- expected structure/identifiers where relevant;
- append vs mutable/rewrite semantics;
- allowed producer(s);
- events emitted for meaningful changes;
- Documentation Agent section mapping;
- progress/alignment invalidation behavior;
- automatic memory-ingestion behavior;
- branch/canonical-state requirements;
- validation/health rules.
This contract prevents PRIME from guessing the semantics of filenames and allows authority evolution to be versioned.
## 16A.26 Event ordering and projection safety
Project events include monotonic/per-source revision information sufficient to prevent stale asynchronous jobs from overwriting newer projections. Derived project writes such as Documentation Agent updates, progress/alignment persistence, knowledge ingestion, and Project Brain updates must carry the source revisions they were based on.
Use per-project sequencing/serialization or optimistic compare-and-swap semantics where necessary. If a job finishes after its inputs are stale, it is rejected/requeued instead of overwriting newer state. Event delivery may be at-least-once, but projections must be idempotent.
## 16A.27 Dream Inbox — planned future product surface
The reserved Dreaming Loop will eventually have a human-facing **Dream Inbox**. Dream cycles are project-scoped and may analyze Hindsight facts, experiences, observations, mental models, reflections, failure patterns, and unresolved contradictions to produce derived candidates such as:
- recurring failure pattern;
- possible process/system simplification;
- mental-model contradiction;
- untested assumption;
- improvement hypothesis;
- opportunity worth investigating.
Every dream item carries supporting evidence/provenance and confidence/uncertainty. Operator actions may include **Inspect Evidence**, **Dismiss**, **Keep as Insight**, **Mark Incorrect**, and **Copy Recommendation**. There is deliberately no automatic **Implement**, **Create Directive**, or code-write action. A future explicit governance design would be required before dream output could influence authority.
## 16A.28 Oracle — planned future product surface
Oracle is a separately permissioned, manually invoked **cross-project read-only research interface**. It may search/answer across project read models, `.agent`, project Notion knowledge, repository indexes, and project memories while citing the originating projects.
Oracle may answer comparative/research questions such as which projects use a technology or whether a failure pattern has appeared elsewhere. It cannot:
- write memories;
- alter `.agent`;
- update Notion;
- modify repositories;
- create directives/tasks/decisions;
- dispatch agents;
- automatically inject cross-project conclusions into normal project Codex sessions.
Oracle is intentionally outside project cognition. Normal project Ask remains strictly single-project.
## 16A.29 Optional Remote Development Status adapters
PRIME's local repository remains authoritative, but local state alone cannot show whether remote integration/build/release systems are healthy. Define a provider-neutral, **read-only Remote Development Status adapter** interface, with GitHub as the first likely implementation when configured.
An attached remote provider may contribute source-labeled status for:
- remote repository/default-branch identity and divergence/freshness;
- pull requests and review/check state;
- CI/check/workflow results;
- tags/releases;
- optional deployment/environment status when a supported provider can map a deployed version back to a Git commit.
Remote status may appear in Activity, Search, Ask, Integrity, Needs Attention, and release/completion review. It must never automatically create directives, modify issues/PRs, merge/push code, change `.agent`, or turn remote text into authority. CI/check success may count as progress/validation evidence **only when the approved AuthorityFileContract/project validation policy explicitly maps that check to an acceptance expectation**; a green remote check is not automatically proof of goal completion.
Provider credentials live in PRIME Core, use least-privilege read-only scopes where possible, are never sent to Nodes/coding agents, and are independently revocable. Remote data carries provider/source IDs and freshness timestamps and degrades cleanly when disconnected. Repository/project operation must remain fully usable without any remote provider configured.
## 16A.30 Project Evidence & Artifacts
Each project includes a first-class **Evidence** surface for important validation/supporting material that does not naturally live in the repository or Notion. Examples include:
- screenshots and screen recordings;
- benchmark exports and performance reports;
- logs or diagnostic bundles intentionally captured as evidence;
- PDFs/specifications/test certificates;
- hardware-test photos/results;
- generated test reports;
- release/build artifacts or signed result manifests;
- external evidence URLs/provider records.
Evidence may be uploaded to PRIME-managed storage, referenced from an approved Node path, or linked to a supported external source. Every artifact carries provenance, content hash where practical, capture/observation time, privacy classification, and optional links to directives, GoalItems, validations, commits, or outcomes.
**Evidence is not automatically authority and not automatically Hindsight memory.** It becomes usable validation evidence for progress only when the project validation/AuthorityFileContract explicitly associates it with an acceptance expectation or the operator makes that association. Ask/Search/Documentation may retrieve evidence metadata/approved extracted text with citations. A selected artifact insight may be promoted into Hindsight through the normal memory-admission rules, preserving the artifact as its source.
Binary/model processing follows project privacy policy and explicit parser support. PRIME must not indiscriminately embed/OCR/transcribe every attachment. Large/sensitive artifacts use size limits, storage quotas, malware/content-type validation where applicable, and clear indexing status.
Evidence participates in backup/export/restore according to storage mode. External-only references are backed up as metadata but cannot be falsely represented as locally preserved content.
## 16A.31 Time Lens — historical project reconstruction
Each project includes a read-only **Time Lens** for exploring how the project looked and what PRIME knew at an earlier point in time. Time Lens exists because continuity is not only about remembering facts; the operator should be able to inspect the evolution of the project itself.
### Entry points
The operator may enter Time Lens by selecting:
- a canonical Git commit or tag;
- a timestamp;
- a historical ProgressAssessment / GoalModel revision;
- a major milestone or significant project event.
The selected point becomes an explicit `as_of` context. Every surface rendered in Time Lens must show that the operator is viewing history and provide a prominent **Return to Now** action.
### Reconstruction model
Time Lens is reconstructed from existing authoritative/versioned sources rather than full snapshots of every source file.
**Repository/code**
- reconstruct from the selected/nearest applicable canonical Git commit;
- display the exact commit/ref used;
- if the requested timestamp falls between commits, show that the code view represents the latest earlier canonical commit rather than pretending an exact timestamp snapshot exists;
- historical uncommitted application-source content is not guaranteed unless it was separately captured as Evidence; if PRIME was offline or no authoritative revision exists, mark it unavailable.
**`.agent`**** authority**
- retain compact `AuthorityRevision` history for meaningful authority-file changes because these files are small and central to project continuity;
- reconstruct the authority package as PRIME observed it at the selected point;
- when a revision is tied to a Git commit, expose that relationship;
- if PRIME missed a change while offline, show a reconstruction gap rather than guessing.
**Progress / GoalModel / milestones**
- use the exact persisted historical GoalModel, ProgressAssessment, confidence, evidence and milestone state;
- never rescore historical progress with a newer model/prompt and call it the original result;
- percentages from different GoalModel baselines remain visually segmented rather than presented as directly comparable deltas.
**Memory**
- historical membership/status is reconstructed from PRIME's retained-source ledger, memory lifecycle/tombstone events, recorded timestamps/revisions, and retained Hindsight history where explicitly available; **do not run an unconstrained recall against today's Hindsight bank and present the result as historical state**;
- show memories that existed by the selected point and their historical epistemic/status state;
- if a memory was later corrected, contradicted, superseded or archived, historical views may still show that it existed then, but must display a clear **later corrected/superseded** overlay so Time Lens cannot resurrect invalid guidance as current truth;
- if exact historical Hindsight extraction/observation state was not retained, mark memory reconstruction `PARTIAL` rather than regenerating it with today's model/configuration and calling it original;
- Reflect/Mental Model history is displayed only where Hindsight/PRIME retained sufficient provenance/revision information.
**Notion**
- PRIME retains versioned snapshots/diffs of its own **managed Notion projection** so the operator can inspect the human-readable record PRIME generated at earlier points;
- user-authored Notion historical text is only reconstructable to the extent PRIME captured an ingestion revision. PRIME must never display today's Notion text as if it were the exact historical content of an earlier date;
- missing Notion history is labeled partial/unavailable.
**Evidence and remote state**
- show artifacts/provider records known by the selected point, with original observed/captured timestamps and freshness;
- external systems are never assumed to preserve an old state if PRIME did not capture it.
### Reconstruction confidence
Every historical source class reports one of:
```plain text
EXACT
PARTIAL
UNAVAILABLE
```
The overall Time Lens header summarizes reconstruction coverage. Missing history is a normal explicit condition, not an invitation for an LLM to fill gaps.
### Historical Ask
Time Lens may provide **Ask at this point**. Historical Ask is bound to the selected `as_of` context and may use only evidence available/reconstructed for that historical point plus explicit later-correction annotations. Answers must state the selected time/revision and reconstruction limits. Historical Ask is read-only and its generated answer is not automatically stored as current project memory.
### Historical Project Brain
Project Brain gains a Time Lens mode/time slider:
- file/folder/import topology is rebuilt from the selected canonical commit;
- authority and memory overlays use the selected historical state;
- layout should remain visually stable enough across adjacent commits to make growth/change understandable;
- cached historical layouts are disposable presentation data and never authority.
Time Lens must not require permanent full working-tree snapshots. Use Git plus compact PRIME historical records and rebuildable caches.
### Historical Git checkpoint preservation
Git history can be rewritten, force-pushed, garbage-collected, or disappear with a remote. To keep meaningful Time Lens checkpoints durable without mutating the managed repository, PRIME maintains an optional/required-by-default **PRIME-owned Git history cache** for canonical commits referenced by approved GoalModel revisions, ProgressAssessments, milestones, completion, explicit Time Lens bookmarks, or other designated historical checkpoints. This may use Git bundles/object packs/bare cache storage outside the project repository and must preserve commit identity without creating branches/refs inside the working repository.
The cache is not a replacement for the user's source-code backup and does not automatically preserve uncommitted/untracked work or Git LFS payloads. It follows project privacy/storage quotas, participates in continuity backup when historical reconstruction is expected to survive host loss, and may be pruned only under an explicit retention policy that updates affected Time Lens coverage from `EXACT` to `PARTIAL/UNAVAILABLE` where necessary.
## 16A.32 Fork / Clone Project
PRIME provides a protected **Fork / Clone Project** workflow for creating a new experiment/project from an existing project's code without breaking project isolation.
### Core isolation rule
A fork is always a **new PRIME project**, with:
- new `project_id`;
- new repository binding/path;
- new Hindsight bank;
- new Notion Project Record;
- new event/activity stream;
- new Progress/GoalModel baseline;
- new MCP/AI Connection credentials;
- new Project Brain projection.
The child project never shares a live Hindsight bank, progress state, `.agent` authority, MCP credential, Notion managed blocks, or mutable project state with its source project.
### Source revision
V1 forks from an explicit **canonical committed Git revision/tag**. PRIME must not silently fork an ambiguous dirty worktree/uncommitted source state. If the operator wants uncommitted material preserved, it must first be committed or captured through a separately explicit snapshot/evidence workflow.
### Workflow
1. choose source project and canonical commit/tag;
2. choose target Node/path and new project name/image;
3. create the new repository/working copy while preserving selected Git history;
4. display parent remote configuration and require an explicit choice to retain or clear/remap remotes; default to clearing write-capable parent remotes when safety cannot be proven, to reduce accidental pushes to the source project;
5. create new project identity and isolated dependencies;
6. generate/adopt the current authority template rather than blindly treating the parent's historical `.agent` state as new authority;
7. the parent goal may be offered only as a **draft starting point**; the new `PROJECT_GOAL.md` requires normal operator approval;
8. create a new operator-approved Progress Baseline;
9. create a new Notion Project Record and new Hindsight bank;
10. issue new AI Connections/MCP credentials;
11. run normal indexing/documentation/progress initialization.
### Optional inherited context
By default, **no source-project memory is copied**. The operator may explicitly choose a small set of high-value memories or selected Notion Knowledge Source bindings to seed the fork. Copied memories become independent records in the child bank marked as `inherited_context` with provenance identifying the source project/memory and source revision. There is no live cross-project lookup after import.
Do not automatically copy:
- source project observations/mental models/reflections wholesale;
- source project activity history;
- progress assessments/baselines;
- credentials/secrets;
- managed Notion page content as if it were the child project's history;
- unresolved directives/outcomes as child authority.
The source project remains unchanged by a fork.
## 16A.33 Fixed product-boundary decisions
The following are intentional product decisions, not placeholders for future expansion:
**Exactly one human operator per PRIME installation.** PRIME will not become a team/multi-user/RBAC/collaboration product.
**One primary Git repository per PRIME project.** Monorepos are supported as one project. Multiple independent repositories are represented as separate PRIME projects rather than being aggregated into one project. Submodules remain linked repository artifacts under the repository policy and may be registered as separate PRIME projects if they need independent continuity/authority.
**Notion is the only external human-knowledge connector.** Do not build a generic connector/RAG marketplace. Evidence and remote engineering-status adapters remain separate source classes, not knowledge connectors.
**Tailscale is the supported remote-access mechanism.** Remote browser access remains private to the operator's tailnet and PRIME must not implement public hosting, its own Internet tunnel, or Tailscale Funnel exposure.
These decisions simplify project isolation and are requirements. During planning they may be changed by the operator on this page; after planning freeze they change implementation scope only through an operator-approved SpecChangeRecord/new implementation-baseline revision.
## 16A.34 Product navigation summary
Target project navigation:
```plain text
PROJECT
├── Overview
│   ├── Since You Were Here
│   ├── Progress
│   ├── Alignment
│   ├── Milestones
│   └── Integrity
├── Ask
├── Search
├── Progress
│   ├── Current Assessment
│   ├── Goal Items
│   └── History
├── Repository
│   ├── Files
│   ├── Git
│   ├── Branches / Worktrees
│   └── Repository Search
├── Authority
├── Memory
│   ├── Inspector / Search
│   ├── Timeline
│   ├── Facts / Experiences
│   ├── Decisions / Failures / Procedures
│   ├── Observations
│   ├── Mental Models / Reflection
│   └── AI Memory Activity
├── Brain
├── Time Lens
├── Knowledge
│   ├── Project Notion Record
│   └── Attached Knowledge Sources
├── Evidence
│   └── External / Uploaded Validation Artifacts
├── Activity
├── AI Connections
└── Settings
    ├── Identity
    ├── Repository / Canonical Git Target
    ├── Knowledge
    ├── Memory
    ├── Privacy
    ├── Context Export
    ├── Fork / Clone
    └── Lifecycle
```
Global Settings target:
```plain text
SETTINGS
├── Operator / Security
├── PRIME Nodes
├── Notion
├── AI Provider / Privacy
├── Hindsight
├── Remote Access / Tailscale
├── Authority Template
├── Backup / Restore
├── Usage / Cost
├── Notifications
├── Upgrades
└── Diagnostics
```
Future navigation may add **Dreams** and **Oracle** only under the authority boundaries above.
---
# 17. Project Removal, Archive, and Deletion
These are separate operations.
## 17.1 Remove from PRIME
Meaning:
- stop managing project;
- preserve repository untouched;
- preserve Notion page untouched;
- preserve or archive PRIME memory according to user choice;
- remove it from active dashboard.
This is the normal reversible offboarding action.
## 17.2 Archive
Meaning:
- project becomes read-only historical in PRIME;
- watchers/jobs disabled except explicitly allowed reconciliation;
- repository remains untouched;
- memory remains searchable;
- Notion remains available;
- project can be restored.
## 17.3 Delete Project
Destructive action with explicit confirmation.
Recommended workflow:
1. show exact node and repository path;
2. show whether repository has uncommitted changes;
3. show a **data disposition preview** covering repository, PRIME metadata/events, Hindsight bank, Evidence artifacts, Project Brain/index caches, AI connections/credentials, Notion Project Record/Knowledge bindings, remote-provider bindings, and existing backups;
4. create a final PRIME metadata/memory snapshot **only if the operator's chosen deletion mode permits preserving a recovery snapshot**;
5. perform final Notion update/archive where feasible and explicitly state that an external Notion page is not deleted unless the operator separately requests an action PRIME is authorized to perform;
6. default to moving repository into an OS/platform-specific quarantine/archive location rather than immediate permanent erasure;
7. revoke project-scoped AI/MCP credentials and stop watchers/jobs;
8. mark project deleted in PRIME;
9. expose permanent purge separately.
### Permanent purge
Permanent purge is a distinct high-friction operation. It must show exactly which locally controlled data will be erased and which external/backed-up copies may survive. When confirmed, purge should remove, as applicable:
- quarantined/local repository data when explicitly selected;
- Hindsight project bank and project-specific retained-source/correction state;
- PRIME project metadata not legally/operationally required for a minimal deletion audit tombstone;
- uploaded PRIME-managed Evidence artifacts;
- repository indexes/embeddings/Brain layouts/caches;
- revoked credential material and project integration secrets;
- project-specific model/job payloads that are not required audit records.
Backups require an explicit retention policy: purge marks the project deleted in backup manifests and either expires affected backups according to policy or warns the operator that historical encrypted backups still contain the data until their retention window ends. External systems such as Notion, remote Git providers, external Evidence URLs, and third-party model-provider logs are reported separately because PRIME must not claim to erase data it does not control.
Minimal audit tombstones may retain project ID, deletion time, actor, and disposition result without retaining project content. Permanent recursive filesystem deletion must require an additional confirmation containing the exact project name/path. No one-click trash icon should immediately `rm -rf` a project.
---
# 18. Security and Trust Model
## 18.1 Assumptions
V1 is intended for exactly one trusted operator using local/private LAN access plus the approved private Tailscale tailnet path, but it must not assume every process or device on either private network is trusted.
## 18.2 Node authentication
Nodes must use strong enrollment credentials and authenticated encrypted communication.
Prefer mutually authenticated identities or equivalent strong node credentials.
A compromised/unknown node must not be able to impersonate another node or request arbitrary project data.
### Node enrollment sequence
Node enrollment is an explicit operator-controlled workflow:
1. the operator starts **Add Node** in PRIME Core;
2. Core creates a short-lived, single-use enrollment secret/code or equivalent scoped bootstrap credential;
3. the Node presents that credential to the dedicated private Node control plane and proves its generated node identity;
4. Core displays the joining machine identity/capabilities for operator approval before trust is finalized;
5. Core issues/pins the long-lived node credential/certificate, invalidates the bootstrap credential, and records enrollment in audit history;
6. the operator configures allowed repository roots separately from node identity;
7. credential rotation/revocation and explicit re-enrollment are supported without changing existing `project_id` values.
Enrollment tokens must expire, be single-use, never grant repository access by themselves, and never be accepted over a public endpoint.
### Network exposure policy
V1 is a private-network product and must **never expose PRIME Core, Node control APIs, Hindsight, PostgreSQL, or project MCP endpoints directly to the public Internet**. Hindsight/PostgreSQL should remain private backend services reachable only by PRIME components that need them. The **operator Web/UI plane** binds to loopback by default and remote browser access uses the required Tailscale Serve design in §18.11. Do not expose the operator UI through a direct public or broad LAN listener merely to make Nodes or coding clients work.
Node and MCP communication use separate authenticated private service planes as defined in §18.12. Tailscale is already the supported built-in remote-access mechanism; do not retain or implement an obsolete generic "future remote access" path.
## 18.3 Project-scoped MCP credentials
MCP access tokens/identities must:
- bind to one project;
- have explicit capabilities;
- be revocable;
- be rotatable;
- support expiry/last-used visibility and explicit client identity;
- never expose a global project-list/search capability to a normal coding agent.
Each AI Connection also has enforceable **resource/abuse limits** independent of prompt instructions:
- maximum request/payload size;
- maximum `prime_memory_store` content size and bounded writes per time window;
- bounded recall/context result count and output/token budget;
- per-client request/concurrency limits;
- per-client/model-backed cost or usage limits where measurable;
- timeouts/cancellation for expensive retrieval/model operations;
- protection against repeated failed/retry loops;
- audit counters and clear throttled/quota-exceeded error semantics.
A compromised or malfunctioning coding client must not be able to flood Hindsight, exhaust model spend, monopolize background workers, or generate unbounded audit/history simply because its credential is valid. Rate/size limits are configurable globally with per-project/per-connection overrides. Audit logs should record operation metadata and result IDs while applying the same secret/privacy redaction rules as the rest of PRIME; do not create a second sensitive-content leak by logging raw MCP payloads indiscriminately.
## 18.4 Destructive operations
Archive/delete operations require:
- authenticated operator session;
- explicit confirmation;
- audit event;
- exact path display;
- node-side path revalidation;
- protection from symlink/path escape.
## 18.5 Notion credentials
Notion integration secrets remain server-side and are never sent to repo nodes or coding agents unless a specific architecture later requires a scoped credential.
## 18.6 Model provider credentials
LLM/provider keys used for progress/documentation/memory services remain server-side.
## 18.7 Untrusted content, prompt injection, and parser/fetch safety
Repository content, Notion content, Evidence/Artifacts, remote-development-provider text, commit/PR metadata, **Hindsight memories/observations/Mental Models/Reflect output, coding-agent-submitted memory, prior model output**, and external URLs are all **untrusted input/data**. Memory provenance and salience affect relevance; they do not grant instruction authority. LLM-backed services must not interpret text found in any project source as authorization to:
- reveal secrets;
- change project scope;
- perform filesystem writes;
- cross project boundaries;
- call destructive tools;
- change provider/privacy policy;
- mark goals/progress/validation authoritative.
Authorization is enforced by software boundaries, not prompts.
Evidence/import parsers must be isolated from the PRIME Core trust boundary where practical and must never execute macros, scripts, binaries, archive contents, or repository-provided code merely to extract text/metadata. Apply explicit MIME/content validation, decompression/size limits, timeouts, and resource limits. External URL ingestion must use SSRF-safe fetch rules: reject private/link-local/loopback destinations unless explicitly allowed for a trusted connector, revalidate redirects/DNS resolution, cap download size/time, and never forward PRIME/Notion/provider credentials to arbitrary URLs. HTML/active content is treated as data and sanitized/extracted rather than executed in the privileged application context.
The Web UI must also render repository files, Markdown, Notion-derived text, model output, commit/PR text, Evidence, SVG/HTML and links as **untrusted display content**. Escape/sanitize active markup, prohibit inline script execution, use an appropriate Content Security Policy and clickjacking/security headers, sandbox previews where needed, and never let merely viewing a project file execute repository-controlled JavaScript or privileged browser actions. External links must not inherit PRIME credentials/referrer-sensitive tokens.
## 18.8 Operator authentication and web-session security
Even in single-operator V1, PRIME's web UI and destructive APIs require an explicit operator authentication model. Use secure password/passkey/local identity appropriate to the implementation, secure session cookies, CSRF protection for state-changing web actions, origin checks, rate limiting on authentication, and secure credential storage. Do not equate "private LAN" with authenticated trust.
**PRIME is permanently a single-operator product.** Multi-user accounts, invitations, shared workspaces, team collaboration, per-user permissions, RBAC, and enterprise identity are not future product requirements and must not shape the implementation. A PRIME installation has exactly one human operator identity. If another person uses PRIME, they use a separate installation/instance rather than joining this one.
Durable records still carry explicit `actor_type`/`actor_id` where meaningful so provenance can distinguish the operator, individual coding-client/MCP identities, Documentation Agent/service, system jobs, remote providers, and other machine actors. These fields exist for auditability and client/service attribution, **not** to create a future human multi-user model.
### Single-operator recovery and step-up authentication
A permanently single-user product needs a deliberate break-glass path. Initial setup must generate/configure a **single-operator recovery mechanism** such as an offline recovery key/code or platform-secured local recovery secret. Recovery must not create a second human identity, depend on email/SaaS password reset, or be remotely exploitable as a bypass. Use of recovery revokes existing web sessions, invalidates/rotates relevant authentication secrets, is audit logged, and allows the operator to generate a replacement recovery credential.
High-risk operations require recent **step-up re-authentication** in addition to typed confirmations. At minimum this applies to permanent repository/project purge, destructive restore over existing state, operator credential/recovery reset, and revealing/exporting sensitive credentials where such export is supported.
### Browser and host data handling
Sensitive project APIs and rendered source/memory/Ask/Evidence content must use browser-cache controls appropriate to prevent persistent shared/proxy caching (`Cache-Control: no-store` or equivalent where applicable). Service workers/PWA caches may cache the application shell but must not silently persist protected project payloads for offline use. Logout/recovery revocation clears sensitive client-side session state.
PRIME must not invent custom database cryptography. Secrets belong in the OS/platform credential store or equivalent dedicated secret store; portable/off-machine backups containing sensitive data are encrypted. Setup/Diagnostics should recommend host full-disk encryption because PRIME's local databases, retained source ledger, Evidence, and indexes can contain proprietary project information even when no plaintext credentials are present.
## 18.9 Software supply-chain and dependency governance
PRIME depends on long-lived third-party infrastructure and must treat dependency changes as product changes. Phase 0 and release qualification maintain:
- a dependency/license inventory and SBOM for Core, Web, Node, Hindsight, PostgreSQL/pgvector, parsers, and shipped container images;
- confirmation that bundled/redistributed dependencies and optional provider integrations have licenses compatible with the intended PRIME distribution model;
- lockfiles/pinned runtime and container versions, with immutable image digests for production-critical containers where practical;
- vulnerability/advisory scanning and an explicit upgrade/remediation process;
- provenance/signature verification where upstream artifacts support it;
- a documented exception process for critical security updates that still requires compatibility/regression testing before normal deployment.
The currently selected Hindsight upstream declares an MIT license, but PRIME must preserve the license notice and re-check the exact pinned release plus bundled transitive/runtime components at implementation/release time rather than assuming licensing remains unchanged forever. Automatic dependency/container updates that bypass PRIME compatibility, privacy, backup, and AI behavior regression gates are prohibited.
## 18.10 Project privacy / model egress policy
PRIME must let the operator control whether project content may be sent to cloud-hosted model providers. Support at minimum a global default plus per-project override:
```plain text
CLOUD_MODELS_ALLOWED
LOCAL_ONLY
```
The policy governs the **entire inference and retrieval processing chain**, not only PRIME's top-level LLM calls. It applies to goal assistance, Ask, progress assessment, Documentation Agent, alignment/completion synthesis, memory salience, Hindsight Retain extraction, embeddings, reranking, Recall support components, Reflect, Mental Model refresh, and future Dreaming.
A project configured `LOCAL_ONLY` must use only locally approved model/embedding/reranking services for every component that may receive protected project content. Hindsight bank-level configuration must therefore be verified against the project's egress policy before retain/recall/reflect operations are enabled. PRIME must never silently fall back from a local provider to a cloud provider because the local provider is unavailable or low quality; the affected capability becomes explicitly degraded/disabled instead.
Hindsight bank mission/directive/disposition/configuration is **memory-engine configuration, not project authority**. PRIME owns and versions the Hindsight bank template/configuration used for project memory processing. Direct editing of Hindsight directives/mission through the Hindsight UI/API must not be able to silently redefine `.agent`, project goals, progress semantics, or coding-agent authority.
Repository paths/content categories may be excluded from all model/embedding prompts. The UI must show the effective provider/egress policy per project and flag any component whose configured backend violates or cannot prove compliance.
`LOCAL_ONLY` means **local-only model/inference processing**, not "no network egress whatsoever." The UI should label it unambiguously (for example **Local models only**) and separately show explicitly configured non-model external services such as Notion synchronization, Tailscale, remote Git/status providers, and optional Secure MCP Tunnel. Notion publication is deliberate external project-documentation egress and must be disclosed during project onboarding; generated Notion content applies secret/redaction rules and should prefer summaries/source references over unnecessary raw proprietary source-code excerpts.
### Telemetry / outbound-network policy
PRIME sends **no product analytics, usage telemetry, project content, crash dumps, or diagnostic bundles to a PRIME vendor/service by default**. Outbound network access is limited to operator-configured dependencies/integrations such as Notion, selected model/embedding/reranking providers, Tailscale, explicitly configured remote Git/status providers, and deliberate update/dependency checks. Diagnostic bundles remain local unless the operator explicitly exports them. Logs and usage records must not become a covert telemetry channel.
## 18.11 Tailscale remote access — supported private access path
Remote operator access is a required product capability, but PRIME must **not** become a public Internet-facing service. The supported remote-access design is Tailscale.
### Required topology
```plain text
Operator phone/laptop
      │
      │ authenticated Tailscale tailnet
      ▼
Tailscale Serve HTTPS
      │
      ▼
127.0.0.1:<PRIME web port>
      │
      ▼
PRIME Core / Web UI
```
PRIME's Web/Core HTTP service should bind to loopback by default. Cross-device browser access is provided through **Tailscale Serve**, which privately reverse-proxies the [localhost](http://localhost) service to an HTTPS tailnet URL. Tailscale MagicDNS provides the stable tailnet name when enabled. PRIME must not require a direct `0.0.0.0` public/LAN web bind merely to support remote use.
Current Tailscale configuration details must be verified against official Tailscale documentation at implementation time. The intended configuration uses the supported private **Serve** mechanism rather than **Funnel**. **Tailscale Funnel is prohibited for PRIME** because it exposes a service publicly to the Internet. PRIME-managed setup and diagnostics must detect/refuse a Funnel exposure for the PRIME endpoint and surface it as a critical security condition.
### Access controls
- Keep PRIME's own single-operator authentication and secure web session model even behind Tailscale. Tailscale is an outer network-access boundary, not the sole application authentication mechanism.
- Use current Tailscale **Grants** for new policy configurations where practical, restricted to the operator's approved identity/devices and the PRIME service endpoint/port. Do not rely on an allow-all tailnet policy when a narrower rule can be used.
- Tailscale device approval is strongly recommended and the setup/diagnostics UI should report whether the accessing devices are approved when that state can be determined.
- Tailscale Serve identity headers may be recorded as an additional audit signal when the backend is reachable only through the trusted [localhost](http://localhost) proxy path, but they must not create a second human-user model or replace PRIME operator authentication.
- PRIME Nodes are never exposed publicly. Nodes continue to communicate only through the authenticated Core↔Node protocol over trusted LAN/Tailscale-reachable networking as configured.
### Setup UX
The first-run and Settings **Remote Access** surface should:
1. detect whether Tailscale is installed/running on the Core host;
2. show tailnet/MagicDNS/Serve health without requiring a Tailscale cloud API token when local status is sufficient;
3. configure a fixed allowlisted `tailscale serve --bg` [localhost](http://localhost) reverse-proxy operation after explicit operator confirmation when the host permissions allow it, or provide exact current-compatible steps when automatic configuration is unavailable;
4. verify the resulting HTTPS URL from a tailnet client when practical;
5. show whether the endpoint is private Serve vs public Funnel;
6. support disabling/resetting PRIME's Serve configuration;
7. keep [localhost](http://localhost) access working if Tailscale is unavailable.
When enabling Tailscale HTTPS certificates, the UI must disclose any current Tailscale certificate-transparency/privacy implication (for example publication of the machine/tailnet DNS name in certificate transparency infrastructure) before changing that setting.
Remote-access failure is a connectivity degradation, not project corruption. If Tailscale is down, PRIME remains usable locally and project/node processing continues.
## 18.12 Network-plane separation
PRIME has distinct private network planes with different trust and exposure requirements.
**Operator Web/UI plane**
- Core Web/UI HTTP binds to loopback by default;
- remote browser access is Tailscale Serve → loopback only;
- PRIME authentication/session/CSRF/origin controls remain mandatory;
- browser routes are never exposed merely to support Nodes.
**Core↔Node control plane**
- uses a dedicated authenticated encrypted protocol/listener reachable only on explicitly configured private LAN/Tailscale interfaces;
- exposes only Node enrollment/health/repository-read/lifecycle operations, never the normal operator web application;
- uses node identity credentials/mTLS-equivalent authentication, allowed-root enforcement, firewall/private-interface binding, request limits, and revocation;
- may be Core-initiated, Node-initiated, or mutually connected according to implementation, but the security properties are invariant.
**Project MCP plane**
- uses project-bound application authentication independent of network location;
- may be loopback for co-located clients or an explicitly configured private LAN/tailnet HTTPS endpoint for remote coding clients;
- never exposes a global project switch/list capability and is never public Internet accessible;
- if routed through Tailscale Serve, its path remains separately authenticated by the PRIME MCP grant.
**Backend plane**
- PostgreSQL/Hindsight and internal service ports remain private to Core/supporting services and are never made browser/Tailscale-Serve/public endpoints.
Network configuration must not solve one plane's reachability by broadening another plane's attack surface.
---
# 19. Reliability and Failure Semantics
## 19.1 Source truth survives PRIME
A project must remain usable by a coding agent if PRIME is down because repository + `.agent` remain local authoritative artifacts.
## 19.2 Derived systems may be rebuilt
These are rebuildable from sources where practical:
- repository indexes;
- embeddings;
- progress assessments;
- Notion managed projection;
- graph-derived relationships.
Durable memory and source-event provenance require explicit backup because they contain history not necessarily reconstructible from current source files.
## 19.3 Idempotency
The following must be safe to retry:
- Notion refresh;
- progress assessment persistence;
- index updates;
- event ingestion using dedupe keys;
- node reconciliation;
- graph ingestion where duplicate detection is available.
## 19.4 Staleness
Derived data must carry source revision/freshness metadata.
Never show:
- old progress as current after goal change;
- old repo state as current while node is offline;
- old Notion sync as current after known failure.
## 19.5 Backup
At minimum back up:
- PRIME canonical DB;
- durable memory/source ledger and correction/tombstone state;
- Hindsight PostgreSQL/pgvector state required to restore each project bank;
- portable Hindsight document/bank-template exports where supported so recovery is not dependent solely on one internal database schema version;
- configuration/secret references appropriately;
- project images if locally stored.
Repositories and Notion have their own authoritative storage and are not duplicated as PRIME backups by default. The Backup UI must therefore state clearly that a PRIME continuity backup is **not automatically a source-code backup**. Integrity should surface repositories with no configured remote/protection signal or with known uncommitted/unpushed risk where PRIME can determine it without mutating the repository. An optional encrypted committed-history Git bundle may be offered as a continuity artifact, but it must state that uncommitted/untracked work and Git LFS payloads are not automatically protected unless explicitly included by a supported policy.
Backups may contain proprietary code-derived context, user notes, credentials references, and long-term memory, so backup encryption at rest is required when sensitive project data is present. The operator must be able to choose an off-machine/network/external backup target; a backup stored only beside the PRIME database is not sufficient disaster recovery.
A backup must also represent a **coherent recovery checkpoint**. The backup coordinator records high-water marks/revisions for the PRIME canonical DB, source/tombstone ledger, Hindsight bank state/export, Evidence manifest, and relevant configuration. It may briefly quiesce writers or use database-consistent snapshot mechanisms where required. A bundle assembled from mutually incompatible points in time must not be marked verified. Restore preflight validates component versions/manifests, and destructive in-place restore creates a safety backup/checkpoint first when feasible.
Restore is tested, not assumed: scheduled integrity checks must verify manifests and periodic recovery tests must demonstrate that project identities, Hindsight bank bindings/rebuilds, progress history, Notion bindings, and node trust/re-enrollment behavior are recoverable. A source-ledger rebuild of Hindsight is a continuity fallback, not necessarily a bit-identical restoration of previously derived observations/Mental Models; exact backend restore is preferred when historical derived-state fidelity matters.
## 19.6 Capacity, retention, and backpressure
PRIME must remain usable after years of project activity. Define configurable global/per-project limits and retention/compaction policies for:
- normalized event history;
- audit/security logs;
- repository index/chunk/embedding caches;
- Project Brain cached layouts;
- model-run traces and generated summaries;
- notification history;
- temporary job payloads/dead letters;
- retained-source ledger payloads where legal/operational policy permits compaction.
Retention is **reference-aware**. Compaction must not remove non-rebuildable evidence that is still pinned by an active durable memory's provenance, an approved ProgressAssessment/GoalModel, an operator correction, completion record, Time Lens checkpoint, audit requirement, or another retained artifact that promises resolvable evidence unless the operator explicitly chooses a retention/privacy action that accepts the resulting loss of reconstruction/citation coverage. Before pruning pinned history, PRIME calculates the affected references and shows the consequence.
Durable high-value Hindsight memory is not deleted merely to satisfy cache limits, but the UI must expose memory/storage growth and Hindsight/backend disk health. Automatic cleanup may remove **rebuildable derived caches** before non-rebuildable history. Burst changes and reconnects use bounded queues, coalescing, per-project concurrency limits, and backpressure so a mass checkout, dependency install, branch switch, or node reconnect cannot create thousands of simultaneous LLM/memory/documentation jobs. When a Node reconnects after missing activity, reconciliation compares Git/manifests/current authority rather than replaying an assumed complete sequence of filesystem watcher events.
---
# 20. Observability
Provide a technical diagnostics surface separate from the normal product UI.
Track:
- node connectivity;
- event ingest rate;
- watcher errors;
- indexing queue;
- progress jobs and failures;
- LLM/model usage/cost where available;
- Notion sync status;
- memory ingestion/search latency;
- Hindsight health;
- MCP request latency/error rate;
- job retries/dead letters;
- backup status.
Normal users should see simple health states; technical details may live in Diagnostics/Settings.
---
# 21. Implementation Architecture and Stack Guidance
The coding agent may adjust exact libraries after validating compatibility, but the architectural separation below is required.
## 21.1 Recommended repository organization
One monorepo:
```plain text
animus-prime/
├─ apps/
│  ├─ web/                 # modern web UI
│  ├─ core/                # central API/orchestration service
│  └─ node/                # cross-platform repository node service
├─ packages/
│  ├─ contracts/           # shared schemas/protocol contracts
│  ├─ authority-template/  # versioned .agent bootstrap assets
│  └─ ui/                  # reusable UI system if useful
├─ services/
│  └─ memory/              # memory/Hindsight integration if separate runtime needed
├─ infra/
├─ tests/
├─ docs/
└─ AGENTS.md
```
The exact split may use workspace tooling appropriate to the chosen languages.
## 21.2 Technology posture
Preferred shape:
- modern TypeScript/React web frontend;
- robust local API service;
- **one documented production deployment shape**: a versioned containerized Core/supporting-service stack (Docker Compose or equivalent) with Web/Core ports bound according to the network-plane policy, persistent named/host volumes, health checks, restart policy, pinned images/digests where practical, and explicit backup paths; native developer mode may differ but must not become a second undocumented production architecture;
- the containerized production stack must be qualified on the operator's selected Core-host environment before release; PRIME Nodes remain separately packaged native services for supported repository hosts;
- Python is acceptable/preferred where Hindsight ecosystem integration materially benefits from it;
- **PostgreSQL is the production V1 canonical database engine for PRIME Core** because Hindsight already requires PostgreSQL; use a PRIME-owned database/schema with migrations and ownership isolated from Hindsight tables;
- use PostgreSQL-backed durable job/workflow state for Core rather than introducing Redis/another queue service without a measured need;
- pinned Hindsight service backed by the same PostgreSQL installation/cluster where practical but a **separate Hindsight-owned database/schema**, with pgvector and independent migration ownership;
- sharing the PostgreSQL engine is an operational simplification, not permission for PRIME and Hindsight to read/write each other's private tables;
- repository text/semantic indexing may use a separate lightweight search/index technology because repository retrieval is not durable memory, but PRIME must not add a second agent-memory vector/graph store around Hindsight;
- containerized supporting services where practical;
- node service packaged for Linux and Windows at minimum.
Do not introduce distributed infrastructure merely for architectural fashion. This is a single-operator local system.
## 21.3 Canonical database recommendation
Use a transactional relational database suitable for concurrent background jobs and durable metadata. PostgreSQL is preferred for the central PRIME service unless implementation constraints establish a simpler equally reliable option.
Do not force Hindsight data, relational project metadata, filesystem content, and job queues into one database merely to claim simplicity.
## 21.4 API contracts
Use versioned typed schemas shared between UI/core/node where possible.
Breaking protocol changes require explicit version negotiation or coordinated upgrade behavior.
---
# 22. LLM Use Inside PRIME
PRIME is not an AI agent product, but specific bounded tasks legitimately require models.
Allowed model-backed functions:
- project-goal interview assistance/generation;
- progress assessment;
- human-readable Notion documentation synthesis;
- memory extraction/salience classification;
- memory/context retrieval synthesis where useful.
These must be bounded services with structured inputs/outputs.
They may not obtain unrestricted filesystem write tools.
Every critical model output should either:
- be derived/non-authoritative;
- require explicit user approval when becoming authority;
- or be stored with provenance/confidence as memory.
Additional bounded model-backed functions allowed by the product specification include project-specific Ask/synthesis, goal-alignment assessment, completion-review synthesis, and future explicitly enabled Reflect/Dreaming functions. These inherit the same project isolation, privacy/egress, provenance, and no-write-authority rules.
## 22.1 Provider configuration, usage, and cost
AI provider/model configuration is a first-class Settings surface. PRIME should expose **function-specific AI profiles** rather than assuming one model fits every job: at minimum Goal assistance, Ask, Progress/Alignment, Documentation, memory admission/processing, Hindsight extraction/embedding/reranking configuration, Reflect/Mental Models, and future Dreaming can have separate approved provider/model/settings with global defaults and per-project overrides. Every effective profile is checked against project privacy/egress policy and the relevant AI regression suite before production changes. Usage should be attributable by function/project/provider/model where available. Configurable soft/hard cost limits may suppress optional automatic model jobs rather than silently accumulating expense.
## 22.2 Model/prompt versioning and AI regression evaluation
Every model-backed PRIME function must be treated as versioned software behavior rather than an interchangeable prompt. Persist provider/model, model settings, prompt/template version, structured-output schema version, retrieval-policy version, and relevant source revisions for Progress, Alignment, Ask, Documentation, memory admission, completion review, Reflect/Dreaming, and any future model-backed projection.
PRIME must include a reproducible **AI behavior evaluation suite** with representative/golden project fixtures covering at minimum:
- progress scoring stability and evidence citation correctness;
- no false promotion of unsupported work to complete;
- regression when failed validation should reduce progress;
- Ask answer grounding, citation validity, uncertainty/no-answer behavior, and project isolation;
- Documentation Agent factual consistency and protection of user-owned blocks;
- alignment/drift false-positive and false-negative cases;
- memory admission quality, duplicate/noise rejection, and provenance preservation;
- prompt-injection resistance;
- local-only provider behavior and no cloud fallback;
- correction/supersession filtering so invalid memory does not reappear as current guidance.
Changing a production model, prompt, reranker, embedding model, Hindsight extraction configuration, or structured-output schema requires running the relevant regression suite first. A model upgrade must not silently change an existing project's GoalModel weights or reinterpret historical ProgressAssessments. Historical results remain tied to the model/prompt versions that produced them.
---
# 23. V1 Explicit Non-Goals
Do not build the following into V1:
- autonomous coding loops;
- internal architect/coder/auditor agent teams;
- project execution scheduler;
- automatic task/directive generation;
- portfolio prioritization;
- executive decision engine;
- global personal assistant;
- cross-project semantic retrieval;
- cross-project memory sharing;
- cross-project recommendations;
- automatic project-to-project knowledge transfer;
- Oracle;
- **any multi-user/team/RBAC/collaboration mode (permanent product non-goal)**;
- **generic external human-knowledge connectors beyond Notion (permanent product non-goal)**;
- **multi-repository aggregation inside one PRIME project; one primary Git repository remains the project boundary**;
- **public Internet exposure, custom public tunneling, or Tailscale Funnel for PRIME**;
- cloud SaaS productization;
- full IDE/editor;
- duplicate Git client;
- arbitrary remote shell execution;
- hidden competing project state outside repository/`.agent` authorities.
If a coding agent believes one of these is necessary, it must stop and raise the architectural conflict rather than quietly adding it.
---
# 24. Development Plan
Development proceeds in vertical slices. Each phase must produce a usable, testable increment.
## Phase 0 — Source lock and contracts
Deliver:
- repository created;
- verify the operator-approved immutable **implementation baseline** snapshot/manifest and record its `spec_revision`;
- verify the handed-off finalized `authority-template/v1` manifest/hash; `/home/sketch/Projects/authority` is provenance only and is not a cold-start implementation dependency;
- fail with an explicit prerequisite error rather than inventing missing baseline/authority artifacts;
- shared project/node/event contracts;
- threat model;
- production persistence posture confirmed: PostgreSQL for PRIME Core canonical state/jobs/workflows and a separately owned Hindsight database/schema in the supported PostgreSQL cluster; no SQLite/Redis/second durable queue introduced without a measured requirement;
- pinned Hindsight/PostgreSQL/pgvector compatibility contract documented and exercised;
- dependency/license inventory + SBOM established for shipped components, with Hindsight's pinned-release license/notice and redistribution requirements verified;
- Hindsight bank create/archive/delete, durable-retain verification, recall, observation provenance, Reflect, Mental Models, backup/restore, and degraded behavior tested through the PRIME adapter;
- test harness established;
- no feature coding before core contracts are explicit.
Exit gate:
- authority template validated;
- project isolation contract tested conceptually/with contract tests;
- lifecycle semantics frozen.
## Phase 1 — Core + Node + project registry
Deliver:
- PRIME Core service using the approved PostgreSQL canonical persistence/migration layer;
- durable workflow/saga runner backed by PRIME canonical persistence;
- node enrollment/health with short-lived single-use enrollment bootstrap and credential rotation/revocation;
- allowed roots/path validation;
- existing repo registration;
- create new repo;
- project name/image/path storage;
- read-only tree/file/Git access;
- filesystem watch events;
- minimal project-card UI.
Exit gate:
- project on Linux and project on Windows can both be registered/read from one PRIME Core;
- no normal endpoint can write source files;
- path traversal tests pass.
## Phase 2 — Bootstrapper
Deliver:
- goal interview;
- generated `PROJECT_GOAL.md` review/approval;
- `.agent` template deployment;
- authority health viewer;
- onboarding transaction/state machine;
- rollback/recovery from partial provisioning.
Exit gate:
- a brand-new repository can become a fully bootstrapped READY PRIME project without manual file copying.
## Phase 3 — Progress assessment
Deliver:
- goal decomposition;
- structured assessor schema;
- evidence retrieval;
- weighted progress calculation;
- confidence/freshness;
- project-card progress bar;
- detailed Progress screen;
- reassessment triggers/debounce;
- assessment history.
Exit gate:
- every displayed percentage can be explained by goal-item results and evidence;
- changing goal/evidence correctly marks prior score stale;
- failed validation can reduce progress.
## Phase 4 — Notion integration
Deliver:
- project page creation;
- managed section rendering;
- user-content protection;
- user knowledge ingestion;
- event-driven refresh;
- retry/degraded behavior;
- Notion status UI.
Exit gate:
- PRIME can repeatedly refresh a page without overwriting manually added user knowledge;
- page remains useful to a human without PRIME open.
## Phase 5 — Memory
Deliver:
- PRIME event/audit provenance integration;
- one isolated Hindsight bank per project behind the PRIME memory adapter;
- Hindsight world facts, experiences, and observations plus PRIME tags/classes for decisions/rationale, failures, procedures, environment, constraints, learnings, and hypotheses without creating separate memory stores;
- retained Reflect and Mental Models under derived/non-authoritative rules;
- provenance/source-fact resolution;
- salience/deduplication and verified durable writes;
- supersession/contradiction handling;
- automatic authority-event memory ingestion;
- existing-project bounded warm-start import;
- Memory Inspector/search/timeline and AI Memory Activity;
- project/branch/worktree isolation tests.
Exit gate:
- relevant historical decisions/failures can be retrieved without rereading entire repository;
- Project A retrieval cannot return Project B under adversarial tests;
- memory citations/provenance resolve to valid sources when available.
## Phase 6 — MCP
Deliver:
- project-bound MCP authentication;
- read/search/context tools;
- memory write/supersede tools;
- Codex integration documentation/configuration;
- degraded-mode behavior;
- audit logging.
Exit gate:
- Codex working in a project can retrieve useful historical context and write durable memory;
- Codex cannot switch project namespace;
- MCP outage does not make the repository unusable.
## Phase 7 — Complete operator product experience
Deliver:
- global Home with Projects, Needs Attention, Recently Active, and System Health;
- project Since You Were Here recap;
- Ask PRIME with project-scoped grounded citations;
- unified source-grouped project search;
- Goal Alignment, milestone projections, progress history, and operator correction flow;
- completion-review / operator-confirmed Completed lifecycle;
- Integrity surface and attention-item generation;
- Memory Inspector, timeline, and AI Memory Activity;
- automatic authority-event memory ingestion and existing-project warm-start import;
- attached Notion Knowledge Sources and managed-content conflict handling;
- branch/worktree/canonical-ref awareness;
- AI Connections and Codex/MCP configuration UX;
- portable Markdown/JSON context export;
- Time Lens historical reconstruction, historical Ask, and historical Project Brain mode;
- protected Fork / Clone Project workflow with fresh isolated project state;
- Tailscale private remote-access setup/status and Funnel safety detection;
- rich Activity timeline;
- repository relocation/rebinding;
- first-run setup wizard;
- provider/privacy configuration and usage/cost visibility;
- restrained notifications;
- user-facing backup/export/restore;
- schema/protocol/dependency upgrade preflight UX;
- Project Brain fully integrated into project navigation/API/test contracts;
- future Dream Inbox and Oracle interfaces documented but not autonomously enabled.
Exit gate:
- an operator can understand meaningful changes and project condition without opening the repository;
- Ask answers are project-isolated, source-labeled, and citation-backed;
- canonical Git truth is not polluted by unmerged worktrees;
- automatic memory capture cannot cross project or branch/canonical boundaries;
- additional Notion knowledge can be used without granting Documentation Agent write access to those pages;
- all correction/conflict flows preserve provenance;
- all new surfaces degrade explicitly when dependencies are unavailable.
## Phase 8 — Hardening and polished UI
Deliver:
- full project pages;
- responsive UI;
- archive/remove/delete workflows;
- diagnostics;
- backup/restore;
- installer/service packaging;
- node upgrade flow;
- reliability/performance testing;
- documentation.
Exit gate:
- system survives restart/offline node/Notion outage/memory outage without corrupting canonical project state;
- clean installation and recovery are documented and tested.
---
# 24A. AI Coder Execution Phase Plan — Normative End-to-End Build Order
This section converts the complete ANIMUS PRIME product specification into the **mandatory implementation sequence for the AI coding agent**. The higher-level Development Plan in §24 remains a summary. **This §24A plan is the execution-level phase contract.**
The coder must build from the operator-approved immutable implementation baseline described in §2.7 and §29. It must not begin from the mutable planning page, invent missing behavior, silently defer a requirement, or advance because a phase merely “mostly works.”
## 24A.1 Execution rules that apply to every phase
Every phase must follow the same closed-loop procedure.
### Before starting a phase
1. Verify the active `spec_revision`, authority-template manifest/hash, and previous phase qualification record.
2. Read every specification section referenced by the phase plus any upstream contracts those sections depend on.
3. Re-read §1–§2 product boundaries, §18 Security and Trust Model, §23 V1 Explicit Non-Goals, §27 AI Coding Agent Operating Rules, and the applicable parts of §25 Testing Requirements.
4. Inspect the current implementation rather than assuming the prior phase produced a particular internal design.
5. Update the implementation traceability artifact with the requirements owned by the phase and their current status.
6. Identify prerequisite failures before editing code. A missing required artifact, incompatible dependency, unresolved authority conflict, or failed previous gate is **BLOCKED**, not permission to improvise.
### While implementing a phase
The coder must continuously preserve these cross-cutting invariants:
- **Project isolation:** no project-scoped API, memory query, derived index, job, event, MCP grant, Notion binding, Evidence record, Time Lens reconstruction, or Project Brain projection may leak across `project_id` boundaries (§2.2, §18.3).
- **Authority separation:** repository/Git/`.agent` remain authoritative for their defined domains; PRIME-derived state must remain derived and source-referenced (§2.4–§2.5).
- **Read-only normal observation:** source writes are limited to explicit bootstrap/migration/lifecycle operations; normal monitoring and intelligence features cannot mutate engineering truth (§1.5, §17).
- **Provenance:** all derived outputs, model outputs, citations, memory admissions, progress evidence, Notion projections, historical reconstructions, and external-provider records preserve source identity/revision/freshness (§2.5, §14, §22).
- **Durable workflow safety:** multi-step cross-system operations use durable resumable workflow/saga semantics, idempotency, high-water marks, stale-job rejection, and explicit compensating/recovery states (§13, §16A.26, §19).
- **Privacy/egress:** the effective project privacy policy governs all model, embedding, reranking, Hindsight, Reflect, Mental Model, Ask, Documentation and future Dreaming processing (§18.10, §22).
- **Untrusted input:** repository text, Notion content, memory, Evidence, Git/PR metadata, remote-provider text, model output, URLs, HTML/SVG/Markdown, and imported documents are data—not instructions or authorization (§18.7).
- **Degraded truthfulness:** stale, offline, partial, unavailable, unknown, blocked, and degraded states are shown explicitly; PRIME never fabricates freshness or silently substitutes another source/model (§5, §19).
- **No hidden operational cost:** model-backed work participates in usage/cost attribution, rate limits, queue/backpressure policy, and optional-job suppression when limits are reached (§16A.20, §18.3, §19.6, §22.1).
- **Accessibility and responsive UI:** any user-facing surface added in a phase must be keyboard-accessible, responsive, and not depend solely on color, animation, or 3D spatial position (§16 and the Project Brain appendix).
- **Observability:** new services/jobs/endpoints expose health, structured redacted logs, actionable failure states, and audit events where required (§20).
- **Versionability:** schemas, protocols, prompts, AI profiles, adapters, parsers, authority contracts, and external-dependency behavior are versioned where later change could alter persisted meaning (§16A.23, §22.2).
### Before closing a phase
The coder must:
1. run all phase-specific unit/contract/integration/security/recovery/UX/AI-behavior tests identified below;
2. run the relevant regression subset from §25, not only tests created in the current phase;
3. verify no previously qualified phase regressed;
4. update the requirements traceability artifact from `PLANNED`/`IMPLEMENTING` to `IMPLEMENTED` and then `VERIFIED` only with evidence;
5. record unresolved items as `BLOCKED` with exact evidence—never silently mark them “later” unless the specification itself declares them future-only;
6. record the phase qualification result, implementation revision/commit, migrations/protocol versions, test evidence, known degraded behavior, and any operator decision required;
7. stop on a failed exit gate. The next phase must not begin merely to work around an unresolved failure.
## 24A.2 Requirements traceability contract
Phase 0 must create a version-controlled **Implementation Requirements Traceability** artifact. Its exact repository path is selected in Phase 0 and referenced by the implementation `AGENTS.md`; it is implementation governance and must not become competing project/product authority.
Each normative requirement receives a stable requirement ID and at minimum:
```plain text
requirement_id
spec_section
summary
owning_phase
validation_phases[]
status
implementation_refs[]
test_refs[]
evidence_refs[]
blocked_reason
last_verified_revision
```
Allowed status values:
```plain text
UNASSIGNED
PLANNED
IMPLEMENTING
IMPLEMENTED
VERIFIED
BLOCKED
FUTURE_ONLY_BY_SPEC
```
`UNASSIGNED` is forbidden after Phase 0. `FUTURE_ONLY_BY_SPEC` is allowed only for capabilities the approved specification explicitly places outside V1, such as Dreaming Loop/Dream Inbox execution and Oracle execution (§16A.27–§16A.28, §28). There is no generic `DEFERRED` state.
### Section ownership map
This map is the minimum coverage baseline; Phase 0 expands individual requirements beneath it.
<table fit-page-width="true" header-row="true">
<tr>
<td>Specification area</td>
<td>Primary owning phase(s)</td>
<td>Mandatory later validation</td>
</tr>
<tr>
<td>§1 Product Definition + §2 Foundational Rules</td>
<td>Phase 0</td>
<td>Every phase; final qualification</td>
</tr>
<tr>
<td>§3 System Overview + §4 Core component boundaries</td>
<td>Phases 1–7</td>
<td>Phases 13–15</td>
</tr>
<tr>
<td>§5 Project Lifecycle</td>
<td>Phases 1, 3, 12</td>
<td>Phases 13–15</td>
</tr>
<tr>
<td>§6 Repository and Node Model</td>
<td>Phase 2</td>
<td>Phases 4, 11, 12, 15</td>
</tr>
<tr>
<td>§7 `.agent` Authority / `PROJECT_GOAL.md`</td>
<td>Phases 0 and 3</td>
<td>Phases 7–9, 15</td>
</tr>
<tr>
<td>§8 Progress Assessment</td>
<td>Phase 8</td>
<td>Phases 9, 11, 15</td>
</tr>
<tr>
<td>§9 Notion Project Record</td>
<td>Phase 7</td>
<td>Phases 9, 11, 13, 15</td>
</tr>
<tr>
<td>§10 PRIME Memory</td>
<td>Phase 5</td>
<td>Phases 6, 9, 11, 15</td>
</tr>
<tr>
<td>§11 PRIME MCP</td>
<td>Phase 6</td>
<td>Phases 9, 12, 15</td>
</tr>
<tr>
<td>§12 Repository Index and Retrieval</td>
<td>Phase 4</td>
<td>Phases 8–11, 15</td>
</tr>
<tr>
<td>§13 Event and Job System</td>
<td>Phases 1 and 4</td>
<td>Every later event-driven phase</td>
</tr>
<tr>
<td>§14 Canonical Data Model</td>
<td>Phase 1 establishes; owning feature phase extends</td>
<td>Phase 15 schema/semantics audit</td>
</tr>
<tr>
<td>§15 Core API Boundaries</td>
<td>Implemented with each owning feature phase</td>
<td>Phase 15 complete API contract audit</td>
</tr>
<tr>
<td>§16 / §16A Operator Product Experience</td>
<td>Phases 7–14 according to feature</td>
<td>Phases 14–15 UX/end-to-end</td>
</tr>
<tr>
<td>§17 Lifecycle Management</td>
<td>Phase 12</td>
<td>Phases 13 and 15</td>
</tr>
<tr>
<td>§18 Security and Trust</td>
<td>Phase 0 threat model; implemented continuously; Phase 12 integration</td>
<td>Every phase + final adversarial suite</td>
</tr>
<tr>
<td>§19 Reliability / Backup / Capacity</td>
<td>Phase 13</td>
<td>Phase 15 recovery qualification</td>
</tr>
<tr>
<td>§20 Observability</td>
<td>Begins Phase 1; completed Phase 13</td>
<td>Phase 15</td>
</tr>
<tr>
<td>§21 Implementation Architecture</td>
<td>Phases 0–1</td>
<td>Every architecture review</td>
</tr>
<tr>
<td>§22 LLM Use / AI Evaluation</td>
<td>Phase 0 contract; implemented in Phases 5, 7–9; completed Phase 13</td>
<td>Phase 15 AI regression qualification</td>
</tr>
<tr>
<td>§23 V1 Explicit Non-Goals</td>
<td>Phase 0</td>
<td>Every phase + final scope audit</td>
</tr>
<tr>
<td>§25 Testing Requirements</td>
<td>Every phase</td>
<td>Phase 15 full suite</td>
</tr>
<tr>
<td>§26 Definition of Done</td>
<td>Mapped in Phase 0</td>
<td>Phase 15 closes every item</td>
</tr>
<tr>
<td>§27 AI Coding Agent Operating Rules</td>
<td>Every phase</td>
<td>Phase 15 compliance audit</td>
</tr>
<tr>
<td>§28 Future boundaries</td>
<td>Phase 0 interface/boundary planning only</td>
<td>Phase 15 proves no accidental V1 authority</td>
</tr>
<tr>
<td>Project Brain normative appendix</td>
<td>Phase 10</td>
<td>Phases 11 and 15</td>
</tr>
<tr>
<td>§29 Planning Freeze / Handoff</td>
<td>Pre-Phase-0 prerequisite</td>
<td>Phase 0 verifies immutable inputs</td>
</tr>
</table>
## 24A.3 Phase 0 — Handoff verification, source lock, contracts, and threat model
**Purpose:** prove the coder has complete immutable inputs and freeze the contracts that later phases must not guess.
**Read first:** §1–§2, §7.2 and AuthorityFileContract requirements, §18, §21–§23, §27, §29, and the complete V1 DoD in §26.
### Deliverables
- Verify immutable `spec_revision`, hash, operator approval, and implementation-baseline artifact.
- Verify `authority-template/v1` manifest/hash and audit every authority file; create the machine-readable/documented `AuthorityFileContract` required by §16A.25.
- Create the requirements traceability artifact and assign **every V1 requirement** an owning phase and validation phase(s).
- Create the implementation repository/monorepo skeleton, root implementation `AGENTS.md`, formatting/lint/type/test conventions, CI entry point, migration convention, and architecture-decision record mechanism.
- Freeze domain vocabulary and enum semantics for lifecycle/connectivity/freshness/work conditions (§5), epistemic classes, project scope, source classes, memory statuses, event/job states, Time Lens reconstruction statuses, and error semantics.
- Produce the V1 threat model covering operator UI, Node control plane, project MCP, Notion, Hindsight/PostgreSQL, model providers, Tailscale, optional Secure MCP Tunnel, Evidence parsers/fetchers, remote-development adapters, browser rendering, backups, and destructive workflows (§18).
- Select the Core host/deployment posture and production persistence baseline from §21.2: PostgreSQL for PRIME canonical state, separate ownership from Hindsight, migration tooling, container/runtime choices where applicable.
- Pin and qualify the exact Hindsight/PostgreSQL/pgvector release set and record license/SBOM inputs (§18.9).
- Define API/versioning/error conventions, actor/audit identity conventions, UTC timestamp/revision ordering rules, source-reference/citation semantics, and durable-workflow semantics.
- Define initial AI function profiles and privacy/egress defaults, but do not implement feature behavior yet (§18.10, §22).
- Build foundational test harnesses, fixtures, fake adapters, property/security-test infrastructure, and the initial AI golden-fixture framework.
### Required tests/evidence
- Baseline/hash verification and deliberate mismatch failure.
- Authority-template manifest mismatch/missing-artifact failure.
- Traceability report proves zero `UNASSIGNED` V1 requirements.
- Threat-model review has no unowned high-risk boundary.
- Hindsight compatibility smoke: create bank, retain, verify durability, recall, observation provenance, Reflect, Mental Model behavior, backup/export capability where supported, delete/archive semantics, and degraded behavior through a prototype adapter.
- PostgreSQL migration up/down/restore smoke in isolated test environment.
### Exit gate
No feature coding may begin until all source artifacts are verified, all V1 requirements are assigned, authority semantics are explicit, project isolation/security invariants are testable, and the selected foundational dependency set has passed compatibility smoke tests.
## 24A.4 Phase 1 — PRIME Core substrate, canonical persistence, workflow engine, and operator shell
**Purpose:** establish the trusted central service and durable control-plane substrate before connecting repositories or external systems.
**Read:** §3, §4.2, relevant §5 state semantics, §13, §14 core records, §15 core API conventions, §18.8, §19.1–§19.4, §20, §21.
### Deliverables
- PRIME Core service and configuration system.
- PostgreSQL canonical persistence with reproducible migrations, transaction boundaries, optimistic/concurrency controls, UTC time semantics, and schema-version reporting.
- Canonical core records: Project shell, actor/audit identity, durable Job/Workflow records, ProjectEvent envelope, SourceReference base, Notification/Usage primitives, settings and secret-reference metadata as required by §14.
- Durable job/workflow/saga runner with idempotency keys, bounded retries/backoff, cancellation rules, dead-letter/action-required state, source-revision gating, stale-result rejection, and crash recovery (§13, §16A.26).
- Single-operator authentication bootstrap, session management, CSRF/origin protections, secure cookies, authentication throttling, step-up-auth hooks, and offline recovery-credential mechanism (§18.8).
- Secret-storage abstraction using platform/host-secure storage appropriate to deployment; no plaintext project/provider secrets in repository or logs.
- Health/readiness endpoints and diagnostics skeleton for Core, DB, workflow queue, migrations, storage and configured dependencies.
- Structured redacted logging and AuditRecord service.
- Minimal authenticated web shell with global degraded/system-health placeholders; no fake project functionality.
### Required tests
- Migrations, restart during transaction/job, duplicate job delivery, stale job completion, auth/session/CSRF/origin/rate-limit tests, recovery credential use and session revocation, secret/log redaction, concurrency, DB outage/degraded behavior, UTC/order semantics.
- Security tests ensure no project-ID spoofing primitives are introduced in future-scoped service interfaces.
### Exit gate
Core restarts without losing durable workflows; authentication is enforceable; canonical DB migrations are reproducible; job/event primitives survive duplicate/reordered delivery; no feature service needs an ad-hoc persistence or background-work mechanism.
## 24A.5 Phase 2 — PRIME Nodes, repository identity, private Node control plane, and read-only Git/filesystem truth
**Purpose:** safely observe real repositories on Linux/Windows without granting PRIME an arbitrary remote shell.
**Read:** §4.3, §6, §12.5–§12.6, §15.2–§15.3, §18.2, §18.7, §25.9.
### Deliverables
- Cross-platform PRIME Node service for Linux and Windows.
- Dedicated authenticated/encrypted private Node control-plane endpoint distinct from the operator Web/UI listener.
- Explicit Node enrollment sequence with short-lived single-use bootstrap credential, generated long-lived node identity, operator approval, credential rotation/revocation, version/capability reporting, and separately configured allowed roots.
- Canonical path resolution, path traversal/symlink/junction escape protection, case/Unicode normalization policy, safe file reads, file-size/content-type limits, and directory browsing inside allowed roots only.
- Git repository validation and stable repository-identity fingerprinting.
- Prevent one physical Git repository/worktree set from being simultaneously registered as two active PRIME projects.
- Reject repo-less and bare-repository project onboarding; support new initialized repositories with unborn branch state while making commit-dependent functions explicitly unavailable.
- Read-only Git status, branch/ref, remotes, worktree, commit/history, submodule/LFS/sparse/partial/nested-repo awareness per §6.
- Repository rebind validation primitives that can later move a project between Node/path without changing project identity.
- Filesystem watcher emits raw bounded change observations only; no LLM or feature-specific interpretation at Node level.
- Core repository/project registration APIs and minimal repository/tree/Git UI.
### Required tests
- Full §25.9 repository compatibility matrix.
- Path traversal, symlink/junction escape, unauthorized Node, revoked Node, root escape, oversized file and binary handling.
- Same repo registered through alternate path/worktree/symlink cannot create duplicate project identity.
- Node disconnect/reconnect and Core restart without invented filesystem history.
- No normal Node API can edit source or execute arbitrary commands.
### Exit gate
A Linux-hosted and Windows-hosted Git working repository can be enrolled, uniquely identified, browsed and monitored from one Core with strict read-only/path boundaries and no arbitrary command channel.
## 24A.6 Phase 3 — Project onboarding, `.agent` authority, goal approval, and bootstrap/adoption
**Purpose:** make every project AI-ready through explicit authority rather than hidden PRIME state.
**Read:** §4.4, §5.2 onboarding, §7, §16A.24–§16A.25, §16A.33 fixed boundaries, applicable §17 bootstrap controls.
### Deliverables
- Add Project wizard through Identity → Machine → Repository → Goal → Authority → Review/Provision states.
- Project creation state machine with hard gates versus degradable capabilities exactly as defined in §5.
- Guided `PROJECT_GOAL.md` interview/generation, operator review/edit/approval, approved-goal hash/revision, and unauthorized-goal-mutation detection.
- `authority-template/v1` provisioning through a narrowly scoped lifecycle write path.
- Existing-project authority paths: no `.agent`, compatible current authority, known old version with migration preview, unknown/conflicting authority requiring review.
- Machine-enforced `AuthorityFileContract` validation, authority revision capture, and health state.
- Root Codex bridge creation/validation without overwriting existing `AGENTS.md`; inventory nested `AGENTS.md` / `AGENTS.override.md` instruction scope and surface conflicts as Integrity/Needs Attention conditions.
- `.agent` authority observation cannot be disabled by `.gitignore` or repository-index ignores.
- Bootstrap writes are auditable and resumable; partial provisioning can resume/repair/roll back without corrupting repository truth.
- Project image/name/description/tags and canonical Git target configuration.
### Required tests
- Every authority adoption/migration branch; missing/invalid template; interrupted bootstrap; duplicate project creation; unauthorized goal edit; conflicting nested Codex instructions; `.agent` ignored by Git/index policy; new unborn repo; operator rejects goal/migration.
### Exit gate
A new or existing repository can reach READY with operator-approved goal and validated authority without silent overwrite, and a coding agent has an explicit instruction bridge into `.agent`.
## 24A.7 Phase 4 — Event normalization, repository indexing/retrieval, canonical Git truth, and durable citations
**Purpose:** create the source-observation layer all intelligence features will depend on.
**Read:** §12, §13, §14 SourceReference/event records, §16A.13, §16A.17, §16A.26, relevant §18.7 and §19.6.
### Deliverables
- Incremental repository manifest/index with file metadata, hashes, supported text extraction, filename/path/text search, optional approved semantic chunks, Git revision linkage, parser/index status and explicit exclusions.
- Repository-native + PRIME-specific ignore behavior while always retaining authority observation.
- Canonical Git target/read model and separate Active Work/worktree/branch model; unmerged/experimental work cannot become canonical project truth.
- Normalized project event classification from filesystem/Git/authority changes with semantic diffs, debounce/coalescing, dedupe keys, source revision, project sequence, Core `observed_at`, source `occurred_at`, and provenance.
- First-class add/update/remove/retract event semantics for authority records and future source classes.
- AuthorityRevision history and repository snapshot/checkpoint references.
- Durable SourceReference resolver: citations capture exact source revision/hash/commit/block/artifact; if source later changes, the UI opens the historical/recorded evidence when retained or clearly labels `SOURCE_CHANGED`/unavailable rather than presenting current text as old evidence.
- Rebind execution primitives: pause watchers, validate new identity, switch binding atomically, rebuild disposable index, resume, verify.
- Event-driven freshness/staleness infrastructure used later by progress, docs, memory and Brain.
### Required tests
- Bulk checkout/dependency install coalescing; branch switch; force-push/rebase; out-of-order/duplicate events; Node clock skew; source removal; path rename; citation after source mutation; interrupted rebind; stale async projection attempt.
### Exit gate
PRIME can deterministically answer “what changed, against which canonical revision, from which source, and is the derived view current?” without an LLM.
## 24A.8 Phase 5 — Hindsight-backed PRIME Memory, correction ledger, Reflect and Mental Models
**Purpose:** establish durable project-isolated agent memory before exposing it to coding clients.
**Read:** §4.7 memory architecture, §10, applicable §14 memory/source records, §18.10 privacy, §19.5 backup expectations, §22 model/version rules, §16A.9–§16A.10 and §16A.12.
### Deliverables
- PRIME Memory adapter with exactly one isolated Hindsight bank per project and no Hindsight internals leaking into public product contracts.
- Stable PRIME memory/source IDs and Hindsight `document_id` mapping; canonical retained-source ledger with provenance, status, correction/supersession/tombstone state, branch/worktree context and Hindsight persistence verification.
- Retain flow for Hindsight world facts/experiences/observations plus PRIME tags/classes such as decision rationale, failure, procedure, environment, constraint, learning, hypothesis.
- Automatic consequential authority-event ingestion according to `AuthorityFileContract`, with deduplication and canonical/branch scope rules.
- Existing-project bounded warm start from high-value `.agent` history and explicitly selected Notion inputs only; no repository/Git bulk-memory dump.
- Memory salience/noise rejection and secret-sensitive-content filter.
- Recall/retrieval adapter with project scope, bounded token/results, source links, epistemic class and correction filtering.
- Reflect and Mental Models retained as derived/non-authoritative capabilities with provenance and model/config versioning.
- Memory Inspector, Memory Timeline and AI Memory Activity base UI.
- Memory is treated as untrusted retrieved data; it cannot create instructions/tool authority.
- Source removal/retraction reviews/tombstones downstream memory so invalid current guidance does not survive merely because Hindsight once extracted it.
- Hindsight backup/export/rebuild hooks and health/degraded state.
### Required tests
- Adversarial cross-project leakage, duplicate retain, retain reports success but durable verify fails, bank outage/recovery, secret-bearing memory, source removal, supersession, observation provenance, Reflect/Mental Model labeling, branch memory abandoned/merged, reconstruction from source ledger, memory prompt injection.
### Exit gate
High-value project history can be retained/recalled with verified durability and provenance, Project A cannot retrieve Project B under adversarial testing, and corrected/retracted memory cannot silently reappear as current-valid context.
## 24A.9 Phase 6 — PRIME Memory MCP, AI Connections, Codex bridge validation, and Context Export
**Purpose:** expose the stable project memory contract to coding agents without exposing Hindsight or project switching.
**Read:** §11, §15 MCP/AI-connection APIs, §16A.14–§16A.15, §18.3, relevant §18.10 and §22.
### Deliverables
- Canonical six-tool PRIME Memory MCP surface and exact schemas/errors/budgets from §11; remove/avoid any obsolete alternate tool names.
- Project-bound MCP grants where project identity is derived from authenticated session/credential, not a normal model-supplied `project_id`.
- Capability, payload, token, result, concurrency, rate and cost limits; revocation/rotation; audit without raw secret/sensitive payload leakage.
- `prime_memory_store` durable status semantics (`stored`, `queued`, `duplicate`, `rejected`, `degraded`) and validated optional worktree/commit hints.
- `prime_memory_context` bounded context compiler that mixes memory plus approved current-source references without treating memory as current code truth.
- AI Connections UI: client, state, last activity, grant health, capability list, config guidance, rotate/revoke.
- Codex-compatible MCP config generation with secrets stored outside Git.
- Validate root/nested Codex instruction-chain conflicts discovered in Phase 3.
- Transport modes: direct private MCP for local/tailnet-reachable clients; optional verified OpenAI Secure MCP Tunnel for supported cloud Codex surfaces under explicit privacy policy; Context Export fallback when no approved live transport exists.
- Portable Markdown/JSON context export with revision/freshness/provenance/redaction.
### Required tests
- Cross-project/project-ID injection, revoked/expired grants, oversized payload, flood/cost abuse, MCP outage, tunnel disabled by privacy policy, tunnel revocation, Context Export redaction, wrong worktree hint, raw Hindsight tool inaccessible.
### Exit gate
A fresh coding session can obtain relevant bounded history and store durable memory without being able to select another project or access unrestricted Hindsight; loss of MCP leaves the repository fully usable.
## 24A.10 Phase 7 — Notion Project Record, Documentation Agent, Knowledge Sources, and long-term documentation lifecycle
**Purpose:** maintain the human-readable project record independently from the coding agent.
**Read:** §4.6, §9, §16A.11–§16A.12, applicable §13/§14/§15 Notion records/APIs, §18.5/§18.7, §19 degraded rules.
### Deliverables
- Notion connection/configuration and dedicated Project Record creation during onboarding/reconciliation.
- Explicit PRIME-managed vs user-owned regions with durable block/section mapping, projection revision/source set, content hash and conflict state.
- Event-driven Documentation Agent consuming authority events; targeted section updates rather than full-page rewrites; semantic debounce; stale-job rejection; idempotent replay.
- Managed-content conflict workflow when operator edits a managed block; never overwrite user-owned content.
- Self-write suppression so PRIME-generated Notion content cannot recursively re-enter Knowledge or Hindsight.
- NotionProjectionRevision history for Time Lens.
- Additional operator-selected Notion Knowledge Sources: read-only from Documentation Agent, independent enable/disable/refresh/detach, project-local index/provenance, no generic connector framework.
- Source detach/removal retracts current retrieval and reviews derived memories while preserving historical provenance.
- Bounded main Project Record with linked PRIME-managed history/archive pages or equivalent rollover so years of chronological content do not make the primary page unusable.
- Retry/backoff/rate-limit behavior and clear stale/degraded UI during Notion outages.
- Knowledge UI with ownership, sync, last ingestion, conflict and detach status.
### Required tests
- Repeated sync, crash after Notion write before acknowledgement, user edits managed block, user adds free-form content, self-loop attempt, rate limit, permissions revoked, source detached, source changed, history rollover, current page remains readable, Notion outage and recovery.
### Exit gate
PRIME can maintain a useful human project record for repeated/long-term operation without overwriting user content, learning its own prose, or requiring Codex to write Notion.
## 24A.11 Phase 8 — GoalModel, progress, evidence mapping core, Alignment, Integrity, milestones, and completion semantics
**Purpose:** make project progress explainable and operator-controlled rather than an unconstrained model score.
**Read:** §8, §16A.5–§16A.8, §16A.24–§16A.26, §22, applicable §25 AI behavior tests.
### Deliverables
- GoalModel generation per approved goal revision with stable GoalItem IDs, weights, required flags and acceptance expectations.
- **Progress Baseline Review** requiring operator approval/correction before the first official percentage.
- Evidence retrieval pipeline from canonical repository/Git, authority, validation records, and later pluggable Evidence/remote check sources.
- Structured statuses including not started/in progress/partial/complete-unverified/verified-complete/blocked/unknown; confidence independent from percentage.
- Weighted scoring and complete provenance/explanation for every item and percentage.
- Reassessment triggers/staleness rules; goal change creates a new baseline and never rewrites historical percentages.
- Progress history segmented by GoalModel revision; no false delta across baselines.
- Goal Alignment/drift assessment with advisory-only semantics and source evidence.
- Project Integrity structural checks including repository/authority/canonical target/index/Notion/memory/MCP/progress/bridge health and `AUTHORITY_STALE_SUSPECTED` advisory behavior.
- Milestones as projections over GoalItems, not a second task-management authority.
- Human challenge/correction workflow.
- `COMPLETION_REVIEW` → explicit operator-confirmed `COMPLETED`; percentage alone never completes a project.
### Required tests
- AI golden fixtures from §25.8, baseline approval/correction, goal unauthorized mutation, goal expansion baseline shift, failed validation reducing progress, missing evidence, stale inputs, false alignment flags, completion without validation rejected, model/prompt upgrade regression.
### Exit gate
Every displayed progress value is reproducible/explainable from an approved GoalModel and cited evidence, operator correction works, and no LLM can silently move the target or mark the project complete.
## 24A.12 Phase 9 — Ask PRIME, unified Search, Home/attention/recap, Activity, remote development status, and knowledge conflict UX
**Purpose:** deliver the everyday operator intelligence layer that makes PRIME useful without opening the repository.
**Read:** §16A.1–§16A.4, §16A.12–§16A.16, §16A.29, §15 relevant APIs, §18.7, §22.
### Deliverables
- Global Home: project organization/filter/search/pin/tag metadata, Needs Attention, Recently Active, System Health; no cross-project strategic reasoning.
- Since You Were Here checkpoints and deterministic event summary; checkpoint advancement is explicit and cannot erase unread context accidentally.
- Project Ask with retrieval from canonical repository/index, `.agent`, Git, Notion Knowledge, memory, activity, progress, Evidence metadata where available, and optional remote status; source/epistemic classes and safe UNKNOWN behavior.
- Ask history short-lived/non-memory by default; explicit Remember/Save Insight path preserves underlying evidence rather than hidden reasoning.
- Unified deterministic Search grouped by Repository / Authority / Git / Notion / Memory / Activity / Evidence / remote status where configured.
- Activity timeline with meaningful event categories and evidence links.
- Project knowledge conflict detection using authority hierarchy without treating brainstorming as an error.
- Provider-neutral read-only Remote Development Status adapter interface and initial configured provider implementation if required by the approved V1 baseline; read-only PR/check/release/deployment-to-commit state, explicit freshness, least-privilege credentials and degraded behavior.
- Needs Attention resolution rules and notifications hooks for later Phase 13.
### Required tests
- Ask citation durability and stale-source handling, project isolation, prompt injection from every source class, unknown/partial evidence behavior, Since You Were Here boundaries, Home no-cross-project-reasoning rule, remote provider outage/credential revoke, CI success not counted unless explicitly mapped, knowledge conflict false positives.
### Exit gate
The operator can understand what changed, what matters, what PRIME knows, and why from PRIME alone; answers remain source-grounded and project-isolated.
## 24A.13 Phase 10 — Project Brain 3D visualization
**Purpose:** implement the artistic/explorable project-brain experience without creating another source of truth.
**Read:** complete **Project Brain — 3D Repository and Memory Visualization** normative appendix, §12 repository index, §10 memory, §16 navigation/accessibility, §18.7 browser safety.
### Deliverables
- Derived per-project topology model whose base graph is folder/file structure.
- Deterministic supported-language import/dependency edges; unsupported parser coverage is shown rather than invented.
- `.agent`/authority representation with clear visual class.
- Optional Hindsight memory overlays for facts/experiences/observations/Mental Models only where provenance creates a grounded relationship.
- Stable graph node IDs/layout anchors, clustering, LOD, lazy expansion, search, focus, filters, rotate/pan/zoom and click-through to canonical PRIME detail views.
- No graph position/proximity/layout enters retrieval, memory ranking, progress, MCP context, or agent reasoning.
- Large-repo performance budgets and graceful parser fallback.
- Equivalent searchable 2D/tree/list representation, keyboard navigation and reduced-motion/static fallback.
- Disposable cache/rebuild semantics.
- API/read-model integration and project isolation.
### Required tests
- Delete/rebuild cache with zero authoritative loss, unsupported-language repo, huge repo, cyclic dependencies, memory overlay with missing provenance, cross-project graph leak attempt, accessibility/reduced-motion, malicious SVG/labels/text rendering.
### Exit gate
Every project has a useful explorable Brain derived from real project data, but deleting the entire visualization subsystem changes no project authority, memory, progress or coding behavior.
## 24A.14 Phase 11 — Evidence & Artifacts, Time Lens, historical Git cache, and Fork/Clone
**Purpose:** add durable validation artifacts and historical/lineage capabilities only after current-state truth is stable.
**Read:** §16A.30–§16A.32, §12, §14 historical/fork/evidence records, §15 Time Lens/Fork APIs, §18.7, §19.5–§19.6, Project Brain appendix historical mode.
### Deliverables
- Evidence surface/storage modes: uploaded PRIME-managed artifact, approved Node-path reference, supported external reference/provider record.
- Artifact provenance, hash where practical, privacy classification, capture time, parser/index status, GoalItem/validation/directive/commit/outcome links.
- Sandboxed/limited parsers and SSRF-safe URL ingestion; no automatic OCR/transcription/embedding of all artifacts.
- Progress uses Evidence only through explicit acceptance/validation mapping.
- Time Lens checkpoints by commit/tag/time/assessment/milestone; per-source `EXACT` / `PARTIAL` / `UNAVAILABLE` reconstruction status.
- Historical repository reconstruction from selected/nearest earlier canonical commit; no invented uncommitted state.
- AuthorityRevision, GoalModel/ProgressAssessment, historical memory status, NotionProjectionRevision, Evidence and Brain historical rendering.
- Historical Ask strictly bound to `as_of`, with explicit later-correction annotations and no silent current evidence leakage.
- PRIME-owned historical Git checkpoint cache/bundle/object preservation for significant referenced canonical commits without mutating project refs.
- Fork/Clone preflight and workflow from explicit committed canonical revision only; new `project_id`, repo binding, Hindsight bank, Notion record, goal review/baseline, events, Brain, MCP credentials.
- Explicit remote choice and bounded optional copy of selected memories/Notion Knowledge bindings with lineage/provenance; never live cross-project retrieval.
### Required tests
Full §25.10 plus malicious artifacts, oversized archives, external redirect/DNS SSRF cases, source history rewritten/GC'd, Time Lens memory later corrected, fork crash/retry, inherited memory provenance, remote accidentally pointing to parent, historical Ask leakage.
### Exit gate
The operator can inspect trustworthy historical state and fork experiments without contaminating current truth, while missing history is represented honestly rather than synthesized.
## 24A.15 Phase 12 — Lifecycle operations, Tailscale remote access, destructive safety, and integrated security boundaries
**Purpose:** complete the deliberate write/destructive pathways and private remote-access model after normal read paths are stable.
**Read:** §17, complete §18, §16A.17, §16A.33 fixed boundaries, Tailscale §18.11, relevant §15 lifecycle/remote APIs.
### Deliverables
- Complete project lifecycle: pause/resume, completion, archive, remove-from-PRIME, deletion preflight, quarantine/archive-first where possible, permanent purge with exact target disclosure and typed confirmation.
- Step-up authentication for permanent purge, destructive restore, credential/recovery reset and sensitive credential export/reveal where supported.
- Final snapshot/docs sync/memory/evidence disposition workflow before destructive actions according to policy.
- Explicit purge disposition across repo, Hindsight bank, PRIME metadata, Evidence, caches, grants, backups and external Notion; never claim external deletion if PRIME does not control it.
- Repository Move/Rebind user workflow using Phase-4 atomic rebind primitives.
- Tailscale required remote-operator access: Core operator Web plane remains loopback; private Tailscale Serve HTTPS; MagicDNS/HTTPS status; Grants/device approval where observable; Funnel/public exposure detection/refusal; local access survives Tailscale outage.
- Fixed allowlisted Tailscale command construction or safe manual instructions when automatic configuration unavailable; no LLM/user raw shell injection.
- Node control and project MCP planes remain separately authenticated/private and do not share the operator UI listener.
- Single-human-operator boundary remains structural—no RBAC/team abstractions.
- Security headers/CSP/clickjacking/referrer/browser-cache controls and sensitive client-state clearing.
### Required tests
- Full destructive misuse suite, interrupted deletion, wrong typed target, stale session, recovery-key reset, Tailscale absent/offline, Serve private verification, Funnel/public bind detection, malicious rendering, CSRF/origin/cookie tests, Node/MCP exposure tests.
### Exit gate
Every intentional write/destructive path has explicit authority, authentication, audit and recovery behavior; remote operator access is private through Tailscale and cannot accidentally expose PRIME publicly.
## 24A.16 Phase 13 — Reliability, coherent backup/restore, capacity/backpressure, observability, notifications, cost controls, upgrades, and supply chain
**Purpose:** make PRIME survive years of operation and dependency failure without losing continuity or quietly accumulating risk/cost.
**Read:** §16A.19–§16A.23, §18.9, §19, §20, §22.1–§22.2, relevant §25 failure/recovery tests.
### Deliverables
- Full health/degraded model for Core, DB, Nodes, repository observation, Notion, Hindsight, model providers, MCP clients, remote status, Tailscale, backups and queues.
- Coherent backup coordinator with cross-component high-water marks/checkpoint semantics for PRIME DB, retained-source/tombstone ledger, Hindsight state/export, Evidence manifests, configuration and required historical cache; encryption at rest for sensitive backups; off-machine target support.
- Clear distinction between PRIME continuity backup and source-code backup; repository risk indicators for no remote/uncommitted/unpushed state where deterministically knowable.
- Restore preflight/version compatibility, safety backup before destructive restore where feasible, exact backend restore vs source-ledger Hindsight rebuild semantics, periodic integrity and actual recovery testing.
- Capacity/retention/reference-aware compaction: rebuildable caches first; do not prune evidence/source revisions still referenced by durable memory/progress/Time Lens/citations without explicitly degrading those references.
- Queue limits/coalescing/backpressure/per-project concurrency and mass-change reconnect reconciliation.
- Usage/cost accounting by project/function/provider/model; soft/hard limits; optional automation pauses explicitly.
- High-signal in-app notifications with deterministic resolution/anti-spam.
- Complete technical Diagnostics and redacted observability.
- Schema/Core↔Node/MCP/authority/Hindsight upgrade preflight, transactional migrations where possible, rollback/restore, version incompatibility UX and Node upgrade flow.
- SBOM/license inventory, pinned dependency/image policy, vulnerability review and qualified security-update process.
- AI regression suite tied to model/prompt/embedding/reranker/Hindsight configuration changes.
- No outbound product telemetry by default.
### Required tests
Full §25.5, backup corruption, inconsistent snapshot rejection, restore to fresh Core, restore over existing state, disk pressure, huge queue, rate/cost limit, dependency upgrade incompatibility, old Node protocol, Hindsight migration, notification spam suppression, telemetry network audit.
### Exit gate
PRIME can be recovered from host/service failures using tested procedures, years of derived data cannot grow without policy, upgrades cannot silently change persisted semantics, and optional automation cannot create uncontrolled spend.
## 24A.17 Phase 14 — Complete product UX, setup/packaging, responsive polish, and operator workflow closure
**Purpose:** turn the qualified capabilities into the finished single-user product rather than a collection of admin endpoints.
**Read:** §16, §16A.1–§16A.34 navigation/product surfaces, §21 packaging posture, all UX items in §25.7 and DoD §26.
### Deliverables
- Final global navigation and project navigation exactly covering the approved surfaces: Overview, Ask, Progress, Repository, Authority, Memory, Brain, Time Lens, Knowledge, Evidence, Activity, AI Connections and Settings.
- Home cards/Needs Attention/System Health remain comprehensible without enterprise-PM clutter or cross-project reasoning.
- First-run setup wizard: operator auth/recovery, storage, AI profiles/privacy, Notion, Hindsight, Node enrollment, allowed roots, backup, Tailscale, health, first project.
- Project onboarding polished across existing/new repo and degraded prerequisites.
- Responsive phone/tablet/desktop layouts suitable for Tailscale remote viewing.
- Consistent source citations, status badges, stale/degraded/unknown semantics, destructive confirmations, correction flows and drill-down patterns.
- Accessibility audit including keyboard navigation, focus states, contrast, reduced motion and Project Brain fallback.
- Installer/service packaging for Core and Linux/Windows Nodes; startup/restart behavior; configuration migration; no secret leakage in installer logs.
- Operator documentation: installation, Tailscale, Node setup, project onboarding, AI connection/Codex setup, Notion ownership, memory concepts, backup/restore, relocation, lifecycle/destruction, troubleshooting, privacy and upgrade procedure.
- Product performance budgets for dashboard, search, repository tree, Ask streaming/result latency where applicable, Brain interaction, large history/Time Lens and startup.
### Required tests
Complete §25.7 UX acceptance suite on supported desktop/mobile browser sizes plus fresh-install-from-zero and upgrade-from-previous-test-build flows; accessibility checks; installer/service restart; lost dependency/degraded UX; no terminal required for normal operator workflows after base prerequisites are installed.
### Exit gate
A single operator can install PRIME, configure it, add a project, understand it, connect a coding agent, use memory/docs/progress/Ask/Brain/history, recover it, access it through Tailscale and safely retire it without implementation knowledge.
## 24A.18 Phase 15 — Full-system qualification, V1 Definition-of-Done closure, and release candidate
**Purpose:** prove end-to-end behavior against the immutable baseline rather than declaring success because all components exist.
**Read:** entire approved implementation baseline, especially §23, §25, §26, §27, §28 future boundaries and Project Brain appendix.
### Deliverables
- Requirements traceability report with **zero ****`UNASSIGNED`****, ****`PLANNED`****, ****`IMPLEMENTING`****, ****`IMPLEMENTED`****-but-unverified, or unexplained ****`BLOCKED`**** V1 requirements**.
- Every §26 V1 DoD checkbox mapped to implementation evidence and passing test evidence.
- Full API surface audit against §15 and security capability audit against §18.
- Full data-model/migration semantic audit against §14 and all feature records added by later sections.
- Full test execution: unit, contract, integration, product behavior, UX, security/adversarial, failure/recovery, AI behavior, repository compatibility, Time Lens/Fork/remote access, workflow/privacy boundary tests (§25.1–§25.11).
- End-to-end cold-start scenario on a clean install with at least one Linux and one Windows repository Node.
- End-to-end existing-project adoption scenario including authority migration/review and memory warm start.
- End-to-end Codex/AI connection scenario using an approved transport and fresh agent session.
- End-to-end Notion documentation, source detach/retraction, progress regression/correction, Evidence validation, Time Lens and Fork workflows.
- End-to-end outage matrix: Node, Notion, Hindsight/Postgres dependent capability, model provider, MCP, remote status and Tailscale failures with honest degraded operation.
- End-to-end backup/restore onto a clean installation and verified project identity/memory/progress/history recovery.
- Destructive lifecycle drill proving remove/archive/delete/purge distinctions.
- Large-repository/performance/capacity qualification.
- Scope audit proving V1 does **not** contain autonomous coding, hidden cross-project reasoning, multi-user/RBAC, generic knowledge connectors, public hosting/Funnel, Dreaming execution, Oracle execution, or other §23 non-goals.
- Security/supply-chain release review, SBOM, pinned dependency manifest, migration manifest, release notes and known limitations.
### Mandatory release gate
V1 may be declared qualified only when:
- every applicable requirement is `VERIFIED` with traceable evidence;
- all §26 Definition-of-Done items pass;
- all high/critical security findings are resolved;
- backup/restore and degraded-operation drills pass;
- project isolation passes adversarial tests;
- no unresolved authority/template/baseline contradiction exists;
- no model-backed feature fabricates authority/freshness/evidence;
- the operator can complete the principal product journeys without manual database surgery or hidden developer-only steps.
A release-candidate failure returns work to the **owning phase** identified by the traceability artifact. The coder fixes the root contract there, re-runs that phase gate, then re-runs all affected downstream qualification—not a one-off patch that bypasses phase ownership.
## 24A.19 Phase qualification record template
At the end of every phase, the coder must produce a concise qualification record in the implementation repository:
```plain text
phase
implementation_baseline_spec_revision
start_commit
qualified_commit
requirements_owned
requirements_verified
requirements_blocked
migrations_or_protocol_versions_changed
tests_run
security_tests_run
recovery_tests_run
ai_regression_tests_run_if_applicable
known_degraded_behavior
known_limitations
operator_decisions_required
next_phase_prerequisites
result = PASS | FAIL | BLOCKED
```
A phase marked `FAIL` or `BLOCKED` may not be treated as complete by later phases.
## 24A.20 End-to-end coverage rule
The phase plan is complete only when **every normative V1 behavior in the approved implementation baseline is represented in the traceability artifact and reaches a verified owning phase plus final Phase-15 qualification**. Section references in this phase plan are navigation aids, not permission to ignore requirements elsewhere in the referenced section.
If the coder discovers a requirement that appears to have no phase owner:
1. stop;
2. add it to traceability as `UNASSIGNED`;
3. determine the correct owning phase from the approved product architecture;
4. if assigning it changes product scope or contradicts the baseline, raise an operator decision rather than implementing an invented interpretation;
5. update the traceability map before continuing.
**Nothing is considered complete merely because code exists. It is complete when the requirement, implementation, evidence, tests, failure behavior, security boundary, recovery behavior, user-facing state and final DoD can all be traced end to end.**
---
# 25. Testing Requirements
## 25.1 Unit tests
Cover:
- path normalization/security;
- authority template rendering;
- goal scoring math;
- event dedupe;
- project scoping;
- memory salience/deduplication;
- Notion managed-region merge logic;
- lifecycle transitions.
## 25.2 Contract tests
Cover:
- Core ↔ Node protocol;
- Core ↔ Memory;
- MCP schemas;
- Notion adapter abstractions;
- LLM structured outputs.
## 25.3 Integration tests
Cover:
- Linux node;
- Windows node;
- repo attach;
- repo create/bootstrap;
- filesystem changes → event → stale progress → assessment;
- Notion refresh preserving user text;
- memory ingest/search;
- MCP access.
## 25.4 Security tests
Cover:
- path traversal;
- symlink escape;
- unauthorized node;
- cross-project MCP attempts;
- cross-project memory retrieval attempts;
- prompt injection in repository/Notion/Evidence/Hindsight-memory/model-output text and verification that recalled memory cannot grant instruction/tool authority;
- destructive endpoint misuse;
- secret-file ingestion filters.
## 25.5 Failure/recovery tests
Cover:
- Core restart mid-job;
- Node disconnect/reconnect;
- Notion unavailable;
- Hindsight/PostgreSQL memory backend unavailable or partially degraded;
- malformed `.agent`;
- goal changed during assessment;
- large bulk repo change;
- duplicate event delivery;
- partial project provisioning;
- deletion interrupted before filesystem action completes.
## 25.6 Product-behavior tests
Cover:
- Since You Were Here checkpoint/event boundaries;
- Needs Attention creation and deterministic resolution;
- Ask project isolation, citation/source-class labeling, and unknown handling;
- unified search source grouping and freshness;
- stable GoalModel across reassessments;
- alignment/progress separation;
- progress-history reconstruction;
- completion requires operator confirmation;
- memory operator correction/supersession without destructive evidence loss;
- automatic authority-event memory ingestion and dedupe;
- existing-project warm start excludes indiscriminate source/Git ingestion;
- AI Memory Activity records recalled/stored IDs without exposing chain-of-thought;
- attached Notion knowledge is read-only to Documentation Agent;
- self-generated Notion writes do not re-ingest into knowledge/memory;
- managed-content edits create a conflict instead of being overwritten;
- canonical branch/worktree separation;
- branch-scoped memory retains work context and acceptance state;
- AI connection credential project scoping/rotation/revocation;
- context export redaction and revision metadata;
- citation durability when current files/pages change after an Ask/Progress/Documentation result, including historical resolution or explicit CHANGED/UNAVAILABLE behavior;
- retention pinning so compaction cannot silently destroy evidence still promised by durable citations/Time Lens/progress/memory;
- repository relocation identity validation;
- privacy policy blocks prohibited cloud-model egress;
- usage/cost attribution and limits;
- notification anti-spam rules;
- backup manifest verification and restore;
- upgrade/version compatibility detection;
- Project Brain parser fallback/large-repo behavior and strict non-authority;
- Dream/Oracle permissions remain read-only/derived as specified;
- Tailscale remote access remains private Serve-only, rejects/detects Funnel exposure, and keeps PRIME operator authentication active;
- Time Lens cannot fabricate missing history and correctly labels reconstruction gaps;
- historical memory that was later corrected/superseded is visibly annotated rather than resurfaced as current-valid guidance;
- Fork/Clone produces new project IDs/banks/credentials/Notion/progress state and cannot accidentally share mutable parent state;
- permanent one-human-operator and Notion-only knowledge-connector boundaries are enforced by product/API surface rather than left as UI conventions.
## 25.7 UX acceptance tests
A user must be able to:
- configure/verify private Tailscale Serve remote access without exposing PRIME through Funnel or a public listener;
- open PRIME remotely from an approved tailnet device and still pass PRIME's own operator authentication;
- enter Time Lens at a commit/time/assessment, understand EXACT/PARTIAL/UNAVAILABLE reconstruction status, inspect historical Progress/Authority/Memory/Brain state, and return clearly to the present;
- use historical Ask without current/later evidence being silently presented as if it existed at the selected historical point;
- fork a project from an explicit canonical committed revision and receive a new project with a new repo binding, Hindsight bank, Notion record, Progress baseline and AI credentials;
- choose whether any small set of memories/Notion Knowledge Source bindings is explicitly inherited during a fork and verify no live cross-project retrieval exists afterwards;
- add an existing project without terminal work;
- create/bootstrap a new project without manually copying authority files;
- identify project completion/status from the home screen;
- understand why a progress score exists;
- read goal/authority/repository without editing them;
- find an old memory quickly;
- open the living Notion record;
- distinguish offline/stale/current data;
- safely remove/archive/delete a project.
## 25.8 AI behavior/evaluation tests
In addition to ordinary unit/integration/security tests, release qualification must execute versioned AI regression fixtures for Progress, Ask, Documentation, Alignment, memory admission/correction, privacy egress, and prompt-injection handling. Tests must verify citation/source resolution and project isolation, and must compare material score/behavior changes against an approved baseline before model/prompt/config upgrades ship.
## 25.9 Repository compatibility tests
Cover Windows/Linux path normalization, case-sensitivity differences, Unicode-normalized filenames, rename/move detection, Git LFS pointers, submodules, nested repositories, sparse/partial clones, symlinks/junctions, very large files, non-UTF-8 text, binary assets, branch switches, detached HEAD/worktrees, force-push/rebase history changes, and repository rebind across machines. PRIME must not duplicate, escape, silently omit without status, or convert provisional work into canonical truth under these cases.
## 25.10 Time Lens, Fork and remote-access tests
Cover:
- exact repository reconstruction from known commits and nearest-earlier-commit labeling for timestamp selections;
- authority revision reconstruction including offline/missed-event gaps;
- historical ProgressAssessment/GoalModel fidelity without re-running newer model logic;
- managed Notion projection revision reconstruction and explicit limitations for uncaptured user-authored Notion history;
- historical memory views with later-correction/supersession overlays;
- historical Project Brain generation from selected Git/memory state;
- fork preflight from committed canonical refs only;
- new project identity/bank/Notion/MCP/progress isolation after fork;
- optional inherited-memory copying as independent provenance-tagged child records, never a live parent lookup;
- parent remote retain/clear safety selection;
- Tailscale absent/offline/degraded behavior;
- Tailscale Serve private HTTPS verification;
- detection/refusal of Funnel/public exposure for the PRIME endpoint;
- fixed allowlisted Tailscale command construction with no raw shell input;
- local PRIME usability while Tailscale is unavailable.
## 25.11 Final boundary, workflow, recovery and privacy tests
Cover:
- a physical Git repository/worktree set cannot be registered as two active PRIME projects; Fork/Clone remains the only supported path to a new project identity;
- repo-less and bare-repository onboarding fail clearly, while newly initialized unborn Git branches remain usable with commit-dependent features explicitly unavailable;
- `.agent` authority monitoring cannot be disabled accidentally by `.gitignore`/index-ignore rules;
- authority/knowledge/Evidence add, update, removal and retraction events correctly update current projections, tombstone invalid derived memory, invalidate dependent progress and remain visible historically;
- Core crash/restart at every meaningful step of project provisioning, Fork/Clone, rebind, archive/delete/purge, Notion creation and Hindsight bank creation resumes/repairs the durable workflow without hidden orphan resources;
- Node enrollment secrets expire and are single-use; unknown/revoked nodes cannot connect or escape allowed roots;
- operator Web/UI, Node control, MCP and backend planes remain separately exposed/authenticated as specified; making Nodes reachable cannot make the Web UI public/LAN-open;
- single-operator break-glass recovery restores access, revokes prior sessions and does not create a second identity; destructive operations enforce step-up re-authentication;
- browser/service-worker caching cannot persist protected project payloads contrary to policy, and logout/recovery revocation clears sensitive session state;
- outbound network/telemetry tests prove PRIME sends no product analytics/diagnostics by default and `LOCAL_ONLY` blocks every prohibited provider path;
- backup checkpoint manifests prove Core/source-ledger/Hindsight/Evidence consistency and reject incompatible/incomplete snapshots as verified backups;
- Hindsight source-ledger fallback recovery is labeled as potentially non-bit-identical for derived observations/Mental Models rather than silently rewriting history;
- the built version records/uses the operator-approved implementation-baseline revision and unapproved live specification edits do not silently alter implementation scope.
---
# 26. Definition of Done for V1
ANIMUS PRIME V1 is complete only when all of the following are true:
- [ ] The shipped implementation is traceable to an operator-approved immutable implementation-baseline revision plus approved change records; missing/unapproved spec artifacts fail closed during implementation qualification.
- [ ] Every managed PRIME project is backed by exactly one primary non-bare Git repository; repo-less mode is unsupported and the same physical repository/worktree set cannot be bound to two active projects.
- [ ] PRIME Core canonical state, jobs, and durable workflows use the approved PostgreSQL persistence layer; Hindsight uses separately owned PostgreSQL database/schema state without cross-table coupling.
- [ ] Multi-system lifecycle workflows are durable/resumable and do not hide orphan resources after crashes/partial external failures.
- [ ] Source removals/retractions propagate through current Search/Documentation/Progress/Memory while preserving historical provenance unless explicitly purged.
- [ ] Operator Web/UI, Node control, MCP, and backend services use separate private network planes with no public Internet exposure.
- [ ] Node enrollment, rotation and revocation are explicit, short-lived-bootstrap based, auditable, and allowed-root constrained.
- [ ] Single-operator break-glass recovery and step-up authentication are implemented and tested without creating a second human-account model.
- [ ] Protected project payloads are not persistently browser/service-worker cached contrary to policy; portable sensitive backups are encrypted and coherent recovery checkpoints are verified.
- [ ] PRIME emits no vendor/product analytics or diagnostic telemetry by default beyond operator-configured external dependencies/integrations.
- [ ] PRIME is implemented as a permanently single-human-operator product; there is no multi-user/RBAC/team collaboration path.
- [ ] Notion is the only supported external human-knowledge connector; unsupported generic connectors are not part of the product/API.
- [ ] Remote operator access can be configured through private Tailscale Serve HTTPS, remains protected by PRIME operator authentication, and never requires/permits Tailscale Funnel or a public PRIME listener.
- [ ] Every project has a Time Lens capable of source-labeled historical reconstruction with explicit EXACT/PARTIAL/UNAVAILABLE coverage and historical Project Brain support; designated historical Git checkpoints are preservable in PRIME-owned history storage so force-push/Git GC cannot silently destroy all meaningful Time Lens history.
- [ ] Historical Ask is strictly bound to the selected `as_of` state and cannot silently use later evidence as if it were historically available.
- [ ] Fork / Clone Project can create an isolated new project from a selected committed canonical revision with new project identity, repository binding, Hindsight bank, Notion record, Progress baseline and MCP credentials.
- [ ] Forking never shares mutable memory/authority/progress/credentials with the parent; any inherited context is explicit, bounded, copied and provenance-labeled.
- [ ] One primary Git repository remains the permanent PRIME project boundary; monorepos are supported and independent repositories remain independent projects.
- [ ] Home provides Projects, Needs Attention, Recently Active, and System Health without performing cross-project strategic reasoning.
- [ ] Every project can produce an inspectable **Since You Were Here** recap from normalized events.
- [ ] Every project has project-scoped **Ask PRIME** with grounded citations, explicit epistemic/source classes, safe unknown behavior, and revision-aware citation resolution that cannot silently substitute changed current content for the evidence originally used.
- [ ] Unified project search covers repository, `.agent`, Git, Notion knowledge, memory, and activity with source grouping.
- [ ] Lifecycle, connectivity, freshness, and work/authority condition are represented independently.
- [ ] Projects support `PAUSED`, `COMPLETION_REVIEW`, and operator-confirmed `COMPLETED` semantics.
- [ ] GoalModel structure remains stable for a given `PROJECT_GOAL.md` revision.
- [ ] Progress history, Goal Alignment, milestones, and correction/challenge workflows are visible and evidence-backed.
- [ ] Project Integrity detects and surfaces structural continuity problems without silently rewriting authority.
- [ ] Existing repositories with current/old/conflicting `.agent` authority follow explicit adopt/migrate/review paths and are never silently overwritten.
- [ ] The bundled authority template has a versioned `AuthorityFileContract` defining event/documentation/progress/memory semantics for every authority file.
- [ ] Consequential authority events automatically enter the correct Hindsight bank with provenance and deduplication.
- [ ] Existing-project warm start can seed memory from high-value `.agent` history and selected Notion knowledge without bulk-ingesting the entire repository/Git history.
- [ ] Memory Inspector, Memory Timeline, and AI Memory Activity are usable and project-isolated.
- [ ] Operator corrections to memory/derived artifacts preserve historical provenance.
- [ ] Every project has one PRIME-managed Project Notion Record plus support for additional read-only Notion Knowledge Sources; long-running managed history rolls over into PRIME-owned linked history pages without moving user content or losing provenance.
- [ ] Detaching/privately purging a Notion Knowledge Source retracts current retrieval and associated derived context correctly without pretending PRIME deleted the external Notion source.
- [ ] PRIME-generated Notion changes cannot recursively re-ingest themselves, and managed-content conflicts are surfaced rather than overwritten.
- [ ] Canonical Git state is explicitly configured and separated from experimental branches/worktrees.
- [ ] Branch/worktree memory provenance retains the work context and canonical acceptance/merge state where determinable.
- [ ] Repository relocation/rebinding preserves project identity and verifies the new repository before switching.
- [ ] AI Connections provide project-bound credentials/configuration, health, rotation, and revocation without storing secrets in Git; they explicitly distinguish local/tailnet MCP, optional privacy-approved Secure MCP Tunnel for supported cloud clients, and Context Export when no live transport is permitted.
- [ ] A minimal coding-agent bridge documents authority/MCP expectations without duplicating the authority package; existing root/nested `AGENTS.md`/`AGENTS.override.md` instruction chains are inventoried, never silently overwritten, and precedence/conflicts are visible in Integrity.
- [ ] Portable Markdown/JSON context export works with revision/freshness/provenance and privacy redaction.
- [ ] Activity provides a coherent filterable project timeline.
- [ ] First-run setup guides operator security, storage, AI provider/privacy, Notion, Hindsight, Nodes, roots, backups, health, and first project.
- [ ] Operator authentication/web-session protections guard management and destructive operations.
- [ ] Global/per-project model-egress privacy policies are enforced in software.
- [ ] Usage/cost is visible by model-backed PRIME function where data is available, with configurable limits.
- [ ] Notifications are high-signal and do not fire for routine file/memory noise.
- [ ] Backup/export/restore is user-visible, versioned, integrity-checked, and recovery-tested.
- [ ] Upgrade/version incompatibilities for Core, Nodes, authority template, MCP, schema, and Hindsight are visible and handled through preflight/migration/recovery behavior.
- [ ] Project Brain is present for every project, remains purely derived/non-authoritative, and meets its dedicated acceptance criteria.
- [ ] Dreaming Loop/Dream Inbox and Oracle boundaries are documented so future work cannot accidentally gain write/decision authority.
- [ ] Projects can be added from any enrolled LAN machine.
- [ ] Existing repositories can be registered.
- [ ] New repositories can be created in approved locations.
- [ ] Project name, image, description, node, and path persist reliably.
- [ ] `.agent` can be provisioned from the finalized versioned authority template.
- [ ] `PROJECT_GOAL.md` can be generated through guided setup and requires user approval.
- [ ] Repository and `.agent` are viewable read-only in PRIME.
- [ ] Git metadata is visible without PRIME mutating Git.
- [ ] Repository changes are observed incrementally.
- [ ] Each project has an evidence-backed progress percentage, confidence, and explanation.
- [ ] Progress automatically becomes stale after relevant changes and refreshes appropriately.
- [ ] Each project automatically receives a human-readable Notion page.
- [ ] PRIME-managed Notion sections update without overwriting user-authored knowledge.
- [ ] User Notion knowledge can be indexed/retrieved with provenance without automatically becoming authority or Hindsight memory.
- [ ] Each project maps to exactly one hard-isolated Hindsight bank plus PRIME-owned source/correction metadata.
- [ ] Hindsight native world/experience/observation memory and Mental Models are exposed correctly, while PRIME classifications such as decision rationale, failure, procedure, constraint, environment, and hypothesis are implemented as PRIME metadata/tags/policy rather than parallel memory stores.
- [ ] Hindsight is integrated behind PRIME-owned contracts as the selected V1 durable agent-memory engine; no second custom temporal graph/vector/episodic memory backend is created.
- [ ] Durable memory preserves source provenance, stable Hindsight document binding, correction/tombstone state, supersession, and verified/queued durability status.
- [ ] Coding agents can access project-bound memory through MCP.
- [ ] MCP cannot cross project boundaries.
- [ ] Codex can add high-value durable memories through MCP.
- [ ] PRIME remains usable when a repository node is temporarily offline.
- [ ] Repository remains usable when PRIME or memory is down.
- [ ] Remove, archive, and delete are distinct and safe.
- [ ] Destructive project deletion is protected and audited.
- [ ] Backup/restore exists for PRIME canonical data and durable memory.
- [ ] Linux and Windows repository nodes are supported and qualified.
- [ ] UI is polished, modern, responsive, and does not expose unnecessary subsystem complexity.
- [ ] All required security, integration, recovery, and project-isolation tests pass.
---
# 27. AI Coding Agent Operating Rules for Building ANIMUS PRIME
Any AI coding agent implementing this project must follow these rules.
1. **Build against the operator-approved implementation baseline revision.** Do not invent behavior outside that baseline or silently adopt unapproved edits from other sources.
2. **Do not turn PRIME into an autonomous coding system.** Codex/other AI coders remain external workers.
3. **Do not introduce cross-project reasoning or retrieval.** Project isolation is a hard requirement.
4. **Do not let model prompts enforce security boundaries that software can enforce structurally.**
5. **Do not duplicate repository authority into hidden competing state.** Derived indexes/summaries must identify themselves as derived.
6. **Do not make the progress bar an unexplained LLM score.** It must be structured, evidence-backed, and inspectable.
7. **Do not overwrite user Notion content.** PRIME may update only explicitly managed regions.
8. **Do not store entire codebases as durable memory merely because storage is available.** Memory stores high-value continuity information.
9. **Do not couple agent-facing memory contracts directly to Hindsight internals.** Hindsight sits behind PRIME interfaces.
10. **Do not allow project-scoped MCP callers to choose arbitrary project IDs.** Scope is bound by authentication/session.
11. **Do not give PRIME Node arbitrary shell execution.** It provides bounded repository/file/Git lifecycle capabilities only.
12. **Do not silently alter ****`.agent`**** after bootstrap.** Authority changes happen through explicit project work.
13. **Do not silently fix ambiguity by inventing requirements.** Surface any real conflict against this specification.
14. **Prefer vertical working slices over large speculative infrastructure.** Each phase must prove user-visible behavior.
15. **Keep dependencies replaceable behind explicit interfaces where practical.**
16. **Every write operation must have a clear owner/authority.** Normal monitoring is read-only.
17. **Preserve provenance and timestamps for derived knowledge.**
18. **Treat stale/offline/unknown as real states, not errors to hide.**
19. **Build for recovery.** A failed background service must not corrupt project truth.
20. **Stop scope expansion.** Build only what the operator-approved implementation baseline requires. After planning freeze, additional scope requires an approved SpecChangeRecord/new baseline revision; a live-page edit or unrelated source is not authorization.
---
# 28. Product Statement and Future Boundaries
<callout icon="⚡" color="purple_bg">
	**ANIMUS PRIME is the permanent continuity layer around AI-assisted projects.** It provisions each project with standardized authority and a clear goal, watches its repository without becoming the coder, shows explainable progress toward that goal, maintains a living human-readable Notion record, preserves high-value project memory across AI sessions, and exposes that memory to a project-bound coding agent through MCP. Projects remain isolated. The repository and `.agent` remain authoritative. Codex does the engineering. PRIME makes sure the project itself does not forget.
</callout>
## Future work is intentionally constrained
Two named future product capabilities are intentionally planned but remain outside ordinary V1 autonomous behavior:
**Dreaming Loop / Dream Inbox** — a project-scoped reflective process using Hindsight Observations, Reflect, and Mental Models to generate derived patterns, contradictions, improvement hypotheses, and candidate insights. Dream outputs appear in a human-reviewed Dream Inbox with actions such as inspect evidence, dismiss, keep as insight, mark incorrect, or copy a recommendation. Dreaming cannot directly edit code, `.agent`, Notion authority, decisions, directives, or progress.
**Oracle** — a separately permissioned, manually invoked, read-only cross-project research layer. Oracle may explicitly query multiple projects and cite them, but has no write authority, no decision authority, no ability to create directives/memories, and no automatic connection to project coding agents.
These future capabilities must be accommodated by clean read interfaces and provenance boundaries but must not force cross-project reasoning or autonomous execution into V1.
---
# Appendix A — Project Brain Detailed Specification
> **Normative appendix:** this detailed Project Brain contract is part of the implementation specification and must be included in the frozen implementation baseline.
## Purpose
ANIMUS PRIME must include a project-scoped **Project Brain** view: an interactive 3D neural-style visualization that makes the internal structure of a managed project feel visible and explorable.
This feature is intentionally **visual and interpretive only**. It does not participate in retrieval, memory ranking, progress scoring, coding-agent decisions, project authority, or Hindsight behavior. Nothing about node position, visual clustering, proximity, animation, or graph layout may become an input to AI reasoning.
The purpose is to provide an intuitive artistic representation of the project's "brain" while still grounding every visible node and connection in real project data.
<callout icon="🧠" color="purple_bg">
	**Project Brain is a projection, not a knowledge source.** The repository, `.agent`, Git, PRIME canonical data, and Hindsight remain the actual sources. The 3D graph is rebuilt from those sources and may always be discarded and regenerated without loss of project information.
</callout>
## Core mental model
The experience should resemble exploring a living neural network in three dimensions:
```plain text
folders / subsystems
        │
        ▼
     file nodes ───────── imports / dependencies ─────── file nodes
        │                                                    │
        │ source provenance                                  │
        ▼                                                    ▼
 memory nodes                                           test nodes
        │
        ├── experiences
        ├── world facts
        ├── observations
        └── mental models
```
The visual style may evoke neurons, synapses, constellations, or a digital brain, but the underlying structure must remain deterministic and traceable to project data.
## Primary graph: repository topology
The base graph represents the managed repository and should be conceptually similar to an interactive 3D rendering of `repo_map.md`.
### Required node types
At minimum:
- repository root;
- directories / logical folders;
- source files;
- configuration files;
- test files;
- documentation files;
- `.agent` files.
A later or optional detail layer may expose important symbols such as modules, classes, functions, services, or packages, but V1 must not require every symbol to exist as a permanent 3D node. Large repositories would become unusable if every AST symbol were rendered simultaneously.
### Required repository edge types
Connections should be generated mechanically wherever they can be established reliably:
- directory **contains** file/directory;
- file **imports / requires** file/module;
- module/package **depends on** another module/package;
- test file **tests / targets** a production module when deterministically known;
- configuration file **configures / references** a component when deterministically known;
- `.agent` artifact **references** a repository file or project artifact when an explicit reference exists.
Do not invent semantic relationships merely to make the graph visually dense. An edge must correspond to an actual detected relationship or explicit provenance link.
## Memory overlay
The Project Brain may optionally display the project's Hindsight memory as a second visual layer.
Memory is an **overlay on the repository graph**, not the graph's source of truth.
Supported visual memory classes should include:
- world facts;
- experiences;
- observations;
- mental models;
- future Dreaming Loop outputs when such outputs are explicitly stored as derived memory.
Memory nodes should connect only where PRIME has a grounded link, for example:
- explicit source file path stored with the memory;
- Git commit provenance;
- directive ID;
- outcome ID;
- learning ID;
- decision ID;
- `.agent` file/source event;
- other explicit project artifact reference.
PRIME should enrich memory writes with this provenance whenever possible so the visualization can show where a memory came from.
**Do not infer a file-memory edge solely because two embeddings appear similar.** The Project Brain must not create visually authoritative-looking connections from unverified semantic similarity.
## Visual hierarchy
The graph should make the project comprehensible even before the user clicks anything.
Recommended hierarchy:
1. repository/root as the central anchor;
2. major directories/subsystems as large clusters;
3. files arranged around their owning directories and dependency relationships;
4. dependency/import edges connecting file clusters;
5. memory nodes orbiting or clustering near explicitly associated project artifacts;
6. observations and mental models visually distinguishable from source-grounded facts/experiences because they are derived.
Exact colors, particles, materials, glow, line styles, and animation are visual-design decisions and should be tuned during UI implementation. The specification requires semantic distinction, not a fixed palette.
## Interaction requirements
The Project Brain must be genuinely explorable rather than a passive animation.
### Accessibility and reduced-motion requirement
Because Project Brain is intentionally visual and animated, it must never be the only way to inspect the underlying topology. The same repository/memory projection must be available through an accessible searchable tree/list/detail representation with keyboard navigation and semantic labels. Support reduced-motion preferences by disabling or minimizing continuous particle/force animation, and provide a static/2D fallback when WebGL, device capability, accessibility needs, or user preference make the 3D surface unsuitable. No information required for project understanding may exist only as color, spatial position, animation, or hover state.
Required interaction:
- rotate/orbit freely in 3D;
- pan and zoom;
- reset camera;
- search for a file, folder, memory, directive, or other displayed node;
- fly/focus camera to a searched node;
- click/tap a node to inspect it;
- highlight direct neighbors and connected edges;
- isolate/focus a selected subgraph;
- expand/collapse directory clusters where useful;
- toggle node/edge categories;
- toggle the Hindsight memory overlay independently from the repository graph;
- show a readable detail panel for the selected node;
- provide a direct transition from a file node to PRIME's read-only repository file viewer;
- provide a transition from a memory node to PRIME's memory detail/provenance view;
- provide breadcrumbs or an equivalent way to understand the selected node's location in repository structure;
- offer a clear "show entire project" action after focusing on a subgraph.
The UI must remain usable with mouse/trackpad and should support touch where practical.
## Selected-node detail panel
Selecting a repository node should expose relevant factual metadata such as:
- name;
- path;
- node type;
- language/file type;
- containing directory;
- imports/dependencies;
- inbound relationships;
- outbound relationships;
- associated tests when known;
- associated explicit memories;
- Git metadata when already available to PRIME;
- action to open in repository viewer.
Selecting a memory node should expose:
- memory class;
- content/summary;
- created/observed time;
- source/provenance;
- linked file/directive/outcome/commit references;
- whether it is source-grounded or derived;
- source facts for observations/mental models where available;
- action to open the full memory record.
## Graph-generation architecture
Project Brain must use a dedicated **derived graph projection** produced from data PRIME already maintains.
Conceptually:
```plain text
PRIME Node / repository watcher
          │
          ▼
repository index + dependency extraction
          │
          ├───────────────┐
          │               │
          ▼               ▼
repository graph      provenance links
                          from memory
          │               │
          └───────┬───────┘
                  ▼
        Project Brain Projection
                  │
                  ▼
        3D WebGL visualization
```
The projection should use a simple graph contract such as:
```plain text
BrainGraphSnapshot
  project_id
  source_revision
  generated_at
  nodes[]
  edges[]

BrainNode
  id
  kind
  label
  project-relative path/reference
  metadata

BrainEdge
  id
  source_node_id
  target_node_id
  kind
  provenance/reference
```
Node positions are **presentation state only**. They may be calculated client-side or cached for visual stability, but they must never be stored as semantic knowledge.
## Incremental updates
The graph should not rebuild the full repository unnecessarily.
Repository watcher events should update the derived projection incrementally:
```plain text
file added    → add/update node + relationships
file changed  → recalculate affected relationships
file moved    → update path/containment relationships
file deleted  → remove node + affected edges
memory stored → add/update optional memory overlay node
memory changed/superseded → update corresponding overlay state
```
A periodic full reconciliation may verify the derived graph against the repository index.
## Relationship extraction rules
Repository relationships should favor deterministic parsers and language-aware indexing over LLM interpretation.
Examples include:
- import/require/include parsing;
- package/module dependency manifests;
- language-server or AST/index information where available;
- repository tree relationships;
- explicit file references in `.agent` artifacts;
- explicit provenance metadata from PRIME Memory.
An LLM is not required to generate the graph and should not be in the critical graph-generation path.
## Performance and large repositories
The experience must remain usable for large codebases.
Required scaling strategies:
- WebGL/GPU-backed rendering rather than thousands of normal DOM elements;
- level-of-detail behavior;
- folder/subsystem clustering;
- lazy expansion of dense clusters;
- labels shown selectively rather than for every visible node at all zoom levels;
- progressive loading where necessary;
- background/worker computation for expensive layout work where practical;
- incremental graph updates rather than full recalculation after every change;
- configurable filters for generated/vendor/build directories;
- respect repository ignore rules and PRIME indexing exclusions.
For very large projects, the default view should favor folders and important files rather than attempting to display every low-value generated artifact at once.
## Visual stability
A constantly reshuffling graph would make the Project Brain frustrating to explore.
The implementation should preserve reasonably stable positions between updates. New nodes may settle into the existing layout, while unchanged portions of the graph should not needlessly move across the entire 3D space.
Layout state may be cached per graph revision as presentation metadata, but the layout remains disposable and non-authoritative.
## Project isolation
Project Brain is always scoped to exactly one PRIME project.
- Project A's graph may contain only Project A repository and Project A memory overlays.
- Project-scoped memory isolation rules apply unchanged.
- Oracle, if built later, does not automatically create a merged multi-project graph.
- No cross-project visual edges are allowed in the normal Project Brain view.
## Security and authority rules
Project Brain has no write authority over project sources.
It must not:
- edit repository files;
- edit `.agent`;
- modify Hindsight memory;
- create memories merely because the user moved a visual node;
- create project relationships based on visual proximity;
- feed node layout or graph clusters into MCP context selection;
- affect progress scoring;
- alter Notion documentation;
- become an alternative source of project truth.
The only state the visualization may own is presentation state such as camera position, filters, expanded clusters, selected node, and optional cached layout coordinates.
## Relationship to Hindsight and the Dreaming Loop
Hindsight remains the memory engine. Project Brain only renders selected Hindsight records and grounded provenance connections.
The future Dreaming Loop may create new observations, mental models, and derived improvement hypotheses. Once those records exist in Hindsight under the normal provenance/authority rules, the Project Brain may visualize them as a distinct derived-memory layer.
The visualization itself must never trigger reflection, dreaming, memory creation, or self-improvement simply because the user explored or rearranged the graph.
## UI placement
Each project's main navigation should include a dedicated **Brain** surface alongside Overview, Goal, Progress, Repository, Authority, Memory, Knowledge/Notion, Activity, and Settings.
The Brain page should prioritize the 3D canvas while keeping controls and selected-node details visually subordinate to the graph.
Recommended primary controls:
- Search;
- Repository / Memory overlay toggle;
- node-type filters;
- edge-type filters;
- focus/reset;
- layout/animation controls where useful;
- selected-node detail drawer/panel.
## Implementation sequencing
Project Brain should be implemented **after the repository index and Hindsight provenance contracts are stable**, because it consumes both rather than defining either one.
Recommended sequence:
1. establish repository tree/index contract;
2. establish deterministic dependency-edge extraction;
3. establish memory provenance links to files/directives/commits;
4. define `BrainGraphSnapshot` projection contract;
5. build static 3D repository graph;
6. add navigation/search/focus/filter interactions;
7. add incremental updates;
8. add optional Hindsight memory overlay;
9. optimize large-repository rendering and layout stability;
10. visually polish the neural/digital-brain presentation.
The choice of 3D rendering/force-graph library is an implementation decision and must be evaluated for WebGL performance, interaction quality, maintainability, mobile/touch behavior, large-graph support, and ability to control layout. PRIME should not couple its graph data model to a specific visualization library.
## Acceptance criteria
Project Brain is complete for V1 when:
- every managed project has a Brain view;
- the view can render the project's repository hierarchy in interactive 3D;
- grounded imports/dependencies appear as edges;
- `.agent` files are represented and recognizable;
- the user can rotate, pan, zoom, search, focus, filter, inspect, and reset the graph;
- clicking a file can open the read-only file view;
- optional Hindsight memory nodes can be toggled on/off;
- memory nodes only connect through grounded provenance;
- derived observations/mental models are visually distinguishable from source-grounded memories;
- repository changes update the projection without requiring a full manual rebuild;
- large repositories remain navigable through clustering/LOD/filtering;
- project isolation is enforced;
- the graph has no write path to repository authority or Hindsight;
- deleting the visualization cache and rebuilding it produces no loss of authoritative project data.
---
# 29. Planning Freeze and Implementation Handoff Checklist
<callout icon="✅" color="green_bg">
	**FREEZE AUTHORIZATION SATISFIED — ****`PRIME-SPEC-V1.0.0`**
	The operator explicitly declared planning complete and authorized implementation on `2026-08-10T15:41:00Z`. Phase 0 may begin. The exact byte-level specification export SHA-256, materialized `authority-template/v1` manifest/hash, exact dependency pins, and initial governed Git commit are now **Phase-0 source-lock outputs** rather than prerequisites that can prevent Phase 0 from starting. Phase 1 remains blocked until those outputs exist and Phase 0 records `PASS`.
</callout>
This section is the **actual end-of-spec handoff gate**. The operator approval requirement is now satisfied for baseline `PRIME-SPEC-V1.0.0`; subsequent normative changes require the SpecChangeRecord/new-baseline process.
Before freeze/handoff:
- [ ] The operator has reviewed the complete product scope, fixed boundaries, V1 Definition of Done, normative appendices, and explicit future-only capabilities.
- [ ] The approved authority package has been audited and snapshotted as `authority-template/v1` (or the approved equivalent) with a manifest/content hash; the historical `/home/sketch/Projects/authority` path is no longer required by the coder.
- [ ] This Notion specification is exported/snapshotted into an immutable implementation artifact with a unique `spec_revision`, content hash, freeze timestamp, and operator approval record.
- [ ] The implementation-baseline manifest explicitly includes this main specification, all normative appendices, the authority-template artifact, and any other required retained implementation inputs. Content not present in the approved manifest is not silently part of the implementation contract.
- [ ] The target PRIME Core host/deployment environment and supported container runtime are selected for qualification against the documented containerized production deployment shape.
- [ ] Phase 0 will select and pin exact compatible Hindsight, PostgreSQL, pgvector, runtime/container, parser, and other production-critical dependency versions; licenses/notices and upgrade constraints are verified against those exact versions.
- [ ] Initial function-specific AI profiles/provider choices, privacy/egress defaults, and local-vs-cloud policy are selected or explicitly left as Phase-0 configuration work with no hidden fallback assumptions.
- [ ] The initial AI regression/evaluation fixture set and expected baseline behavior are established before model/prompt/config changes can be qualified.
- [ ] Codex/AI-coder bootstrap behavior has been validated against the current supported instruction/MCP mechanisms, including applicable `AGENTS.md`/`AGENTS.override.md` precedence and the selected live MCP transport(s).
- [ ] Backup/recovery target, single-operator recovery mechanism, Tailscale private-access posture, Notion integration prerequisites, and Node enrollment assumptions are documented for the selected deployment environment.
- [ ] No unresolved `MISSING_AUTHORITY_TEMPLATE`, contradictory product boundary, unknown destructive-data disposition, or security/privacy prerequisite remains.
## Handoff package
The AI coding agent receives:
1. the immutable implementation-specification snapshot identified by `spec_revision`;
2. the approved authority-template artifact and manifest/hash;
3. the implementation repository/workspace created for ANIMUS PRIME;
4. any Phase-0 retained dependency/architecture decision records explicitly included in the baseline;
5. a clear statement that implementation is authorized against **that baseline revision**.
The live Notion page remains the human planning/reference surface. After freeze, any material product change requires operator approval and a new baseline revision/SpecChangeRecord before the coding agent treats it as implementation scope.
> **End-of-spec rule:** this checklist and every normative section/appendix before it belong to the product plan. Anything added after this end-of-spec marker must be intentionally integrated into a new approved baseline revision before it becomes implementation authority.
<page url="https://app.notion.com/p/3b8833cb27ff81d89229d461867ca547">ANIMUS PRIME — Implementation Handoff Record — PRIME-SPEC-V1.0.0</page>
</content>
</page>
