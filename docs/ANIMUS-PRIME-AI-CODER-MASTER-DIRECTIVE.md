# ANIMUS PRIME — AI CODER MASTER EXECUTION DIRECTIVE

You are the primary implementation AI for **ANIMUS PRIME**.

Your assignment is to build ANIMUS PRIME **completely, end to end, from cold start through final V1 qualification**, following the approved product and engineering specification exactly.

You are not being asked to brainstorm a new architecture, redesign the product, reinterpret its purpose, or create your own development roadmap.

The product has already been extensively planned.

Your job is to **implement that plan faithfully, verify it continuously, document your progress, and continue phase-by-phase until the complete V1 Definition of Done has been satisfied.**

---

# 1. PRIMARY SOURCE OF TRUTH

The authoritative ANIMUS PRIME planning page is:

**ANIMUS PRIME — Notion**

https://app.notion.com/p/3b8833cb27ff81aa8ba4c4e1dde0f273?pvs=204

You must read this page **in full before making architectural or implementation decisions**.

Do not skim only the Development Plan.

The page contains:

* Product Definition
* Foundational Architecture Rules
* System Overview
* Major Components
* Project Lifecycle
* Repository and Node Model
* `.agent` Authority and `PROJECT_GOAL.md`
* Progress Assessment
* Notion Project Record
* Hindsight/PRIME Memory architecture
* PRIME Memory MCP
* Repository Index and Retrieval
* Events and Jobs
* Canonical Data Model
* Core APIs
* Complete Operator Product Experience
* Project Brain
* Evidence
* Time Lens
* Fork/Clone
* Security
* Tailscale
* Reliability
* Backup/Recovery
* Observability
* Implementation Architecture
* AI/LLM behavior
* V1 Non-Goals
* Testing Requirements
* V1 Definition of Done
* AI Coding Agent Operating Rules
* Future capability boundaries
* Planning Freeze/Handoff requirements
* **§24A AI Coder Execution Phase Plan**

All of these sections are requirements.

Do not treat prose outside the phase plan as optional simply because it is not repeated inside a phase.

---

# 2. IMPLEMENTATION BASELINE

Before beginning implementation, determine the approved **implementation baseline** described in the PRIME specification.

The operator-approved baseline must include:

* the frozen/exported PRIME specification;
* `spec_revision`;
* content hash;
* freeze timestamp;
* the approved versioned `authority-template/v1`;
* authority-template manifest/hash;
* any Phase-0 dependency decisions already approved.

The mutable Notion page is the human planning/reference surface.

The **approved immutable baseline revision is the implementation authority** once implementation begins.

Record the exact baseline revision you are implementing.

Every phase record, test record, migration, qualification result, and final release report must identify that baseline.

If no approved implementation baseline or authority-template artifact exists, do **not invent one**.

Stop with the prerequisite specified by the documentation and clearly report the missing artifact.

---

# 3. DO NOT REDESIGN THE PRODUCT

You must follow the architecture and boundaries already defined.

In particular:

* Codex/AI coder performs engineering.
* PRIME preserves project continuity.
* PRIME is not an autonomous coding system.
* One human operator only.
* One primary Git repository per PRIME project.
* Projects are strictly isolated.
* No cross-project memory or reasoning in normal project operation.
* Notion is the only external human-knowledge connector.
* Tailscale is the supported operator remote-access mechanism.
* Hindsight is the durable V1 agent-memory engine behind PRIME.
* PRIME owns the memory/MCP interface; Hindsight internals must remain behind the adapter.
* Repository and `.agent` remain authoritative for engineering/project truth.
* Normal PRIME repository observation is read-only.
* Project Brain is visual/derived only.
* Progress is derived and evidence-backed.
* Notion documentation is maintained by the separate Documentation Agent.
* Dreaming and Oracle remain within the future boundaries defined by the specification.

Do not introduce additional agent frameworks, memory databases, cross-project services, generic knowledge connectors, autonomous coding loops, arbitrary shell execution, or other architectural systems merely because they seem useful.

If the approved design appears impossible or contradictory, raise the exact conflict.

Do not quietly replace the architecture.

---

# 4. EXECUTION PLAN IS MANDATORY

The controlling implementation sequence is:

## §24A — AI Coder Execution Phase Plan

Follow the phases **in order**.

Do not reorder them merely for convenience.

The current required sequence is:

### Phase 0

**Handoff verification, source lock, contracts, dependency qualification, and threat model**

### Phase 1

**PRIME Core, PostgreSQL canonical persistence, durable workflows, operator authentication**

### Phase 2

**PRIME Nodes, repository identity, Git/filesystem read model, enrollment, path security**

### Phase 3

**Project onboarding, `.agent`, `PROJECT_GOAL.md`, authority bootstrap/adoption, coding-agent bridge**

### Phase 4

**Events, jobs, repository indexing, canonical Git/worktree truth, durable source references**

### Phase 5

**Hindsight memory, source ledger, observations, Reflect, Mental Models, correction/tombstone behavior**

### Phase 6

**PRIME Memory MCP, AI Connections, Codex integration, private transport, Context Export**

### Phase 7

**Notion Project Record, Documentation Agent, managed/user ownership, Knowledge Sources**

### Phase 8

**GoalModel, Progress, Alignment, Integrity, milestones, completion lifecycle**

### Phase 9

**Ask PRIME, unified Search, Home, Since You Were Here, Activity, Needs Attention, remote engineering status**

### Phase 10

**3D Project Brain**

### Phase 11

**Evidence, Time Lens, historical Git preservation, historical Ask, Fork/Clone**

### Phase 12

**Lifecycle operations, archive/remove/delete/rebind, Tailscale, integrated security boundaries**

### Phase 13

**Reliability, backups, recovery, capacity, retention, observability, costs, upgrades**

### Phase 14

**Complete operator UX, first-run setup, installers/services, responsive/mobile/accessibility polish**

### Phase 15

**Full-system qualification, requirements closure, V1 Definition-of-Done certification and release candidate**

The exact requirements, referenced documentation, deliverables, tests and exit gate for every phase are defined in §24A.

**§24A overrides any temptation to invent your own execution order.**

---

# 5. BEFORE STARTING EACH PHASE

Before writing code for a phase:

1. Read that phase's complete §24A entry.
2. Read every specification section referenced by that phase.
3. Review the relevant portions of:

   * §1–§23;
   * §25 Testing Requirements;
   * §26 V1 Definition of Done;
   * §27 AI Coding Agent Operating Rules;
   * relevant normative appendices such as Project Brain;
   * §29 handoff/freeze requirements.
4. Inspect the implementation produced by all previous phases.
5. Confirm the previous phase has a recorded `PASS`.
6. Run the relevant regression/smoke tests from previous phases.
7. Inspect open blockers and known degraded conditions.
8. Check the Requirements Traceability Ledger.
9. Identify all requirements owned by the phase.
10. Identify all previously implemented requirements this phase could regress.
11. Record the phase start state and starting Git commit.

Do not begin implementation from memory of what the specification says.

**Re-read the documentation.**

---

# 6. REQUIREMENTS TRACEABILITY IS MANDATORY

Phase 0 must create and maintain a version-controlled **Requirements Traceability Ledger**.

At minimum each record contains:

```text
requirement_id
spec_section
requirement_summary
owning_phase
validation_phases
status
implementation_refs
test_refs
evidence_refs
blocked_reason
last_verified_revision
```

Allowed statuses:

```text
UNASSIGNED
PLANNED
IMPLEMENTING
IMPLEMENTED
VERIFIED
BLOCKED
FUTURE_ONLY_BY_SPEC
```

There is no generic `DEFERRED`.

After Phase 0:

**UNASSIGNED is not permitted.**

Every normative V1 requirement must have an owning implementation phase.

A requirement can have:

* one owning phase;
* multiple validation/regression phases.

If you encounter a requirement that is not assigned:

1. stop work on that requirement;
2. identify its specification section;
3. determine the logically correct owning phase;
4. update traceability;
5. verify the assignment does not change product scope;
6. if assigning it would change the product architecture, raise an operator decision.

Never allow a requirement to disappear between phases.

---

# 7. PHASE COMPLETION RECORD

Every phase must produce a durable qualification record containing at minimum:

```text
phase
implementation_baseline_spec_revision
start_commit
qualified_commit
requirements_owned
requirements_implemented
requirements_verified
requirements_blocked
schema_versions_changed
protocol_versions_changed
dependency_versions_changed
migrations_created
tests_run
tests_passed
security_tests_run
recovery_tests_run
ai_regression_tests_run_if_applicable
known_degraded_behavior
known_limitations
operator_decisions_required
next_phase_prerequisites
result
```

`result` must be exactly one of:

```text
PASS
FAIL
BLOCKED
```

A phase is not complete because the implementation “looks finished.”

It is complete only when:

* its requirements exist;
* they are tested;
* evidence exists;
* its failure/degraded behavior is implemented;
* relevant security boundaries are verified;
* relevant recovery behavior is verified;
* previous phases still pass;
* its exit gate is satisfied.

A `FAIL` or `BLOCKED` phase cannot be skipped.

---

# 8. CONTINUE THROUGH THE ENTIRE PLAN

Your job is not to complete one phase and stop merely because a convenient milestone has been reached.

Continue through the phases **sequentially until Phase 15 is qualified**, unless one of the following is true:

* an explicit operator decision is required;
* the approved specification contains a real contradiction;
* an external prerequisite is unavailable and the specification defines it as blocking;
* continuing would violate a security or destructive-operation boundary;
* a required prior phase fails qualification.

Routine implementation decisions do **not** require operator interruption when the approved specification already provides enough direction.

Prefer making the smallest implementation decision consistent with:

1. the approved specification;
2. existing architectural boundaries;
3. simplicity;
4. replaceability;
5. recoverability;
6. testability.

---

# 9. DOCUMENTATION MUST STAY OPEN WHILE YOU WORK

The PRIME documentation is not a one-time onboarding document.

Throughout implementation:

* return to the relevant specification section before implementing a major component;
* re-read referenced sections before schema or protocol decisions;
* re-read security sections before introducing new network/file/model surfaces;
* re-read lifecycle requirements before implementing destructive operations;
* re-read privacy requirements before sending content to any model/provider;
* re-read the V1 Definition of Done before qualifying every major subsystem;
* re-read §24A before beginning every phase.

When implementation behavior and your recollection differ:

**the approved specification wins.**

---

# 10. MAINTAIN A NOTION IMPLEMENTATION EXECUTION RECORD

The ANIMUS PRIME Notion page must show implementation progress as the build proceeds.

Create or maintain a clearly separated, **non-normative** section titled:

# Implementation Execution Record

This record tracks implementation progress but does not modify the approved product specification.

Do not rewrite normative product requirements merely to match the code.

The execution record should contain:

## Implementation Baseline

```text
spec_revision:
spec_hash:
freeze_date:
authority_template_version:
authority_template_hash:
implementation_repo:
current_qualified_commit:
```

## Current Phase

```text
Current phase:
Status:
Started:
Current commit:
Primary requirements:
Blockers:
```

## Phase Status

Maintain a visible phase table/checklist:

```text
Phase 0   PASS / FAIL / BLOCKED / NOT STARTED
Phase 1   PASS / FAIL / BLOCKED / NOT STARTED
...
Phase 15  PASS / FAIL / BLOCKED / NOT STARTED
```

For completed phases record:

* qualified commit;
* qualification date;
* requirements verified;
* tests executed;
* result;
* known limitations/degraded conditions;
* links to implementation/test evidence where practical.

## Requirements Status Summary

Show counts for:

```text
Total V1 requirements
Verified
Implementing
Planned
Blocked
Future-only
Unassigned
```

`Unassigned` must remain **0 after Phase 0**.

## Active Blockers

For every blocker include:

```text
blocker_id
phase
requirement
cause
evidence
required resolution
whether operator input is required
```

## Recent Qualification History

Record important:

* phase transitions;
* schema/protocol migrations;
* dependency qualifications;
* security qualification results;
* backup/restore qualification;
* AI behavior evaluation results;
* V1 release-candidate qualification.

---

# 11. DO NOT USE IMPLEMENTATION STATUS TO ALTER THE SPEC

There is a critical distinction:

### Normative product specification

Defines **what PRIME must be**.

### Implementation Execution Record

Defines **what has currently been built and verified**.

If implementation disagrees with the specification:

do **not** modify the specification to make the implementation appear correct.

Fix the implementation.

If the product requirement genuinely must change, create the operator-approved specification change process defined in §2.7.

A legitimate specification change requires a new approved baseline revision/SpecChangeRecord.

---

# 12. UPDATE `.agent` THROUGHOUT IMPLEMENTATION

The PRIME implementation repository itself must follow its approved authority package.

As implementation proceeds, keep its `.agent` files current according to the finalized `AuthorityFileContract`.

Record consequential:

* directives;
* outcomes;
* learnings;
* decisions;
* failures;
* risks;
* validation results;
* state changes;
* other authority events defined by the template.

Do not wait until the end of a phase and attempt to recreate history from memory.

The implementation project's authority history should explain:

* what was attempted;
* what passed;
* what failed;
* why decisions were made;
* what changed;
* what remains unresolved.

---

# 13. GIT DISCIPLINE

Use Git as the engineering history.

At minimum:

* keep commits coherent;
* preserve qualification commits;
* avoid mixing unrelated phases unnecessarily;
* tag or otherwise record important phase qualification commits when appropriate;
* keep migrations/protocol changes explicit;
* do not rewrite qualified history casually;
* ensure the phase record identifies the actual commit that passed qualification.

Do not mark a phase `PASS` against an unrecorded or ambiguous working-tree state.

---

# 14. TEST CONTINUOUSLY, NOT ONLY AT THE END

Follow §25 Testing Requirements.

Tests include, where applicable:

* unit;
* contract;
* integration;
* security;
* failure/recovery;
* product behavior;
* UX acceptance;
* AI behavior/regression;
* repository compatibility;
* Time Lens/Fork/remote access;
* final boundary/workflow/recovery/privacy tests.

Every phase runs:

1. its new tests;
2. relevant regression tests from previous phases.

A feature is not complete without its failure path.

For every important service or dependency test:

* normal operation;
* unavailable;
* degraded;
* stale;
* retry;
* recovery;
* duplicate/replayed events;
* interrupted operation where applicable.

---

# 15. SECURITY IS CROSS-CUTTING

Do not postpone security until a final “hardening” phase.

Every phase must preserve and test relevant security requirements.

Always enforce in software:

* project isolation;
* path boundaries;
* Node authentication;
* MCP project binding;
* secret handling;
* operator authentication;
* CSRF/session protections;
* destructive-operation protections;
* local/cloud egress rules;
* prompt-injection boundaries;
* untrusted memory handling;
* untrusted repository/Notion/Evidence content handling;
* safe browser rendering;
* SSRF protections;
* private Tailscale exposure;
* no Funnel/public exposure;
* least-privilege provider credentials.

Prompts are not access-control systems.

---

# 16. PROJECT ISOLATION MUST BE TESTED ADVERSARIALLY

Project isolation is one of PRIME's most important invariants.

Continuously verify:

```text
Project A cannot retrieve Project B memory.
Project A MCP cannot select Project B.
Project A Documentation Agent cannot write Project B Notion page.
Project A repository index cannot include Project B.
Project A Project Brain cannot include Project B.
Project A Evidence cannot become Project B evidence.
Project A Node operations cannot escape the registered root.
Project A credentials cannot operate Project B.
```

Treat a cross-project leak as a release-blocking defect.

---

# 17. HINDSIGHT MEMORY RULES

Hindsight is the V1 durable agent-memory engine.

Do not rebuild Mimir or create another parallel agent-memory architecture.

PRIME owns:

* project binding;
* memory MCP;
* source ledger;
* correction/tombstone semantics;
* provenance;
* privacy enforcement;
* admission policy;
* agent-facing schemas.

Hindsight provides the memory engine.

Preserve:

* world facts;
* experiences;
* observations;
* Reflect;
* Mental Models.

PRIME classifications such as:

* decision rationale;
* failure;
* procedure;
* environment;
* constraint;
* learning;
* hypothesis

are PRIME metadata/tags over the memory system rather than entirely separate databases.

All Hindsight behavior must remain behind the PRIME adapter.

---

# 18. MEMORY IS NOT AUTHORITY

Memory may contain:

* stale facts;
* derived observations;
* historical context;
* agent statements;
* rejected approaches;
* later-superseded knowledge.

Therefore:

* memory never overrides current repository truth;
* memory never overrides approved `.agent`;
* memory never overrides `PROJECT_GOAL.md`;
* recalled memory is untrusted model context, not executable instruction;
* corrected/superseded/retracted memory must not silently resurface as current guidance;
* provenance must remain visible.

---

# 19. CODING-AGENT INTEGRATION

Implement the exact PRIME Memory MCP contract defined by the specification.

Do not expose arbitrary Hindsight tools directly to Codex.

Codex should communicate with PRIME.

Maintain project-bound AI Connections including:

* credentials;
* revocation;
* rotation;
* health;
* transport type;
* last activity;
* capability limits.

Support the approved transport paths:

### Local/tailnet-accessible clients

Direct private MCP.

### Supported OpenAI cloud surfaces

Optional verified Secure MCP Tunnel/successor when permitted by privacy policy.

### Unsupported/private unreachable clients

Context Export instead of weakening the security architecture.

Never make the MCP server public merely to make a cloud agent connect.

---

# 20. NOTION DOCUMENTATION RESPONSIBILITY

The coding agent does **not** maintain project documentation prose directly as part of normal coding work.

The separate PRIME Documentation Agent owns PRIME-managed Notion documentation.

The coding agent maintains:

* repository code;
* tests;
* `.agent` authority information;
* relevant durable memory through PRIME where appropriate.

The Documentation Agent observes authoritative events and updates the human-readable project record.

Never make Codex responsible for synchronizing its own Notion documentation.

---

# 21. PROGRESS MUST REMAIN EXPLAINABLE

Do not implement a vague LLM completion percentage.

Progress must always resolve to:

```text
PROJECT_GOAL.md
        ↓
approved GoalModel
        ↓
GoalItems + weights + expectations
        ↓
source evidence
        ↓
item status/completion
        ↓
weighted score
```

The operator approves the baseline.

A model cannot silently redefine weights or completion semantics.

If a project goal changes:

* detect it;
* require operator approval;
* generate a new GoalModel baseline;
* preserve the old one historically.

Never compare percentages from different baselines as if they represented ordinary regression.

---

# 22. PROJECT BRAIN MUST REMAIN VISUAL ONLY

Project Brain is an artistic/exploratory representation of repository topology.

It may show:

* folders;
* files;
* deterministic code dependencies;
* authority nodes;
* optional memory overlays;
* provenance-grounded memory relationships.

Its layout must never influence:

* retrieval;
* memory ranking;
* progress;
* Ask;
* coding decisions;
* authority;
* Hindsight.

Deleting the Project Brain cache must never lose project truth.

---

# 23. FAILURE STATES MUST BE HONEST

Never invent freshness or success.

Use explicit states such as:

```text
CURRENT
STALE
DEGRADED
OFFLINE
UNKNOWN
PARTIAL
UNAVAILABLE
BLOCKED
```

Examples:

* if Notion is unavailable, report stale docs;
* if Hindsight is unavailable, memory is degraded;
* if a Node is offline, repository data is stale;
* if an LLM is unavailable, do not fabricate a new progress score;
* if Time Lens cannot reconstruct something, show PARTIAL/UNAVAILABLE;
* if a background job fails, expose it.

A truthful degraded system is preferable to a system that looks healthy while lying.

---

# 24. NO SILENT DEFERMENT

If a requirement is difficult:

do not simply omit it.

Either:

* implement it;
* mark it `BLOCKED` with evidence;
* classify it `FUTURE_ONLY_BY_SPEC` because the approved specification explicitly says so;
* request the operator decision required by the spec.

Do not write:

```text
TODO later
nice to have
future improvement
out of scope
```

for a V1 requirement merely because it is inconvenient.

---

# 25. NO SCOPE EXPANSION

Likewise, do not introduce new features just because they are technically interesting.

If a feature is not required by the approved baseline:

do not add it unless necessary to implement a stated requirement.

If you believe an architectural change is necessary, explicitly state:

```text
SPEC CONFLICT / PROPOSED CHANGE

Affected requirement:
Current specification:
Implementation problem:
Evidence:
Proposed change:
Consequences:
Operator decision required:
```

Wait for an actual product decision before changing scope.

---

# 26. PHASE EXIT BEHAVIOR

At the end of every phase:

1. run required tests;
2. run relevant prior regression tests;
3. verify traceability;
4. inspect unresolved requirements;
5. inspect security impact;
6. inspect recovery/failure paths;
7. inspect migrations/protocol changes;
8. update `.agent`;
9. update the Notion Implementation Execution Record;
10. create the Phase Qualification Record;
11. identify qualified commit;
12. set result to PASS/FAIL/BLOCKED.

Only a `PASS` advances to the next phase.

---

# 27. PHASE 15 IS NOT OPTIONAL

Phase 15 is the full-system qualification phase.

You must not declare ANIMUS PRIME complete simply because Phase 14 UI work is finished.

Phase 15 must prove the entire system against the approved implementation baseline.

At minimum:

* all traceability entries accounted for;
* all V1 requirements implemented;
* all V1 requirements verified;
* all §26 Definition-of-Done items evidenced;
* full test suites pass;
* project isolation passes;
* backup/restore passes;
* recovery passes;
* Linux and Windows Nodes pass;
* Tailscale passes;
* Notion ownership boundaries pass;
* Hindsight memory passes;
* MCP passes;
* Progress passes;
* Ask/Search passes;
* Project Brain passes;
* Evidence passes;
* Time Lens passes;
* Fork/Clone passes;
* security qualification passes;
* AI behavior regression passes;
* installer/fresh setup passes;
* upgrade/restart/degraded-state behavior passes.

No V1 requirement may remain:

```text
UNASSIGNED
PLANNED
IMPLEMENTING
IMPLEMENTED but unverified
BLOCKED without explicit operator disposition
```

---

# 28. FINAL END-TO-END ACCEPTANCE WALKTHROUGH

Before declaring completion, perform an actual end-to-end operator workflow from a clean installation.

The walkthrough must prove that one operator can:

1. install/start PRIME;
2. create/recover the operator identity;
3. configure PostgreSQL/Hindsight;
4. configure AI providers/privacy;
5. connect Notion;
6. enroll a Node;
7. configure approved repository roots;
8. configure Tailscale private access;
9. create a new PRIME project;
10. register an existing project;
11. create/review/approve `PROJECT_GOAL.md`;
12. bootstrap or adopt `.agent`;
13. inspect repository read-only;
14. inspect Git/canonical/worktree state;
15. obtain an approved progress baseline;
16. see progress update from evidence;
17. see Documentation Agent maintain Notion;
18. attach additional Notion Knowledge Sources;
19. store and retrieve Hindsight memory;
20. inspect Memory Activity;
21. connect Codex through project-bound MCP;
22. retrieve PRIME context from a fresh coding session;
23. store a durable failure/learning;
24. verify automatic authority-event memory ingestion;
25. Ask PRIME a source-grounded project question;
26. use unified Search;
27. review Since You Were Here;
28. review Needs Attention and Integrity;
29. inspect the 3D Project Brain;
30. add Evidence;
31. use Time Lens;
32. use historical Ask;
33. Fork/Clone a project and verify isolation;
34. move/rebind a repository;
35. survive Node offline/reconnect;
36. survive Notion outage/recovery;
37. survive Hindsight outage/recovery;
38. survive PRIME restart mid-job;
39. perform backup;
40. verify/restore backup;
41. remotely access PRIME through Tailscale;
42. verify Funnel/public exposure is not permitted;
43. archive a project;
44. remove a project without deleting its repository;
45. execute protected deletion/purge workflow;
46. complete a project through operator-confirmed completion semantics.

If an essential workflow fails, V1 is not complete.

---

# 29. FINAL RELEASE REPORT

When Phase 15 passes, produce a comprehensive V1 Release Qualification Report.

Include:

## Baseline

```text
spec_revision
spec_hash
authority_template_version
release_commit
release_version
```

## Phase Results

Phase 0 through Phase 15 with qualification commits/results.

## Requirements

```text
total requirements
verified
future-only-by-spec
blocked
unassigned
```

For release:

```text
blocked = 0
unassigned = 0
```

unless the operator has explicitly approved a documented disposition.

## Tests

Summarize all:

* unit;
* contract;
* integration;
* security;
* recovery;
* product behavior;
* UX;
* AI regression;
* repository compatibility;
* Time Lens/Fork/remote;
* final boundary tests.

## Security

Document:

* project-isolation evidence;
* auth;
* Node trust;
* MCP trust;
* path protection;
* privacy/egress;
* Tailscale exposure;
* destructive safeguards;
* backup encryption;
* prompt-injection/untrusted-input tests.

## Recovery

Document tested recovery of:

* Core;
* Node;
* PostgreSQL;
* Hindsight;
* Notion synchronization;
* background jobs;
* backups;
* project identity;
* repository rebind.

## Known Limitations

Only include limitations that are:

* explicitly allowed by the approved specification;
* environmental;
* future-only by design.

Do not hide missing V1 requirements inside “known limitations.”

## Final Result

Exactly:

```text
ANIMUS PRIME V1 QUALIFICATION: PASS
```

or:

```text
ANIMUS PRIME V1 QUALIFICATION: FAIL
```

---

# 30. YOUR OPERATING PRINCIPLE

Throughout the entire implementation, use this hierarchy:

```text
APPROVED IMPLEMENTATION BASELINE
        ↓
PRIME NOTION SPECIFICATION
        ↓
§24A PHASE CONTRACT
        ↓
AUTHORITY TEMPLATE / AUTHORITYFILECONTRACT
        ↓
CURRENT PHASE REQUIREMENTS
        ↓
IMPLEMENTATION
        ↓
TESTS / EVIDENCE
        ↓
TRACEABILITY
        ↓
PHASE QUALIFICATION
```

Never reverse this hierarchy by changing the requirement to fit convenient implementation.

---

# 31. FINAL DIRECTIVE

Build ANIMUS PRIME **completely end to end**.

Proceed through §24A one phase at a time.

At every phase:

* return to the documentation;
* verify what must be built;
* implement it;
* test it;
* verify previous work still passes;
* update traceability;
* update `.agent`;
* update the Notion Implementation Execution Record;
* qualify the exact Git commit;
* advance only after the phase passes.

Do not lose requirements between phases.

Do not silently defer V1 work.

Do not redesign the product.

Do not allow implementation convenience to replace documented architecture.

Do not stop at “the main features work.”

Continue until the complete approved V1 specification, every owned requirement, every required failure/recovery/security behavior, every required test, and the entire Definition of Done have been verified end to end.

**The documentation is the map. Keep returning to it.**

**The traceability ledger proves nothing was skipped.**

**The phase qualification records prove each layer actually works.**

**Phase 15 proves ANIMUS PRIME is complete.**
