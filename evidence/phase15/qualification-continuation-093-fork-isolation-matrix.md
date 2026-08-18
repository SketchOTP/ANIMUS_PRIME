# Continuation 093 — Fork and Isolation Matrix

## Canonical identities

| Boundary | Parent | Fork child | Result |
|---|---|---|---|
| Project | `project_d9a1a5b609394282b62fc12c0d04634d` | `project_db3ef8c4bc834e68a2e9a9deabbb5a80` | Distinct |
| Repository | `repo_1eb92bbce8d44309861368d8690247c6` | `repo_196e1ef98aa046ef94b08e5773b80b46` | Distinct |
| Goal | `goal_a6fb1f34a58e4048951cf690048c255f` | `goal_7f4e145c235448829d53fec3039cfbee` | Distinct; child approved independently |
| Goal hash | `eddb...` | `3f7a...` | Distinct |
| Baseline | `baseline_c07d51d514d443c48b0482972aeaf165` | `baseline_c9f5fd36945f4ed490dc1076f23ee3bc` | Distinct; child references child Goal |
| Hindsight bank | `prime-project_d9a1a5b609394282b62fc12c0d04634d` | `prime-project_db3ef8c4bc834e68a2e9a9deabbb5a80` | Distinct |
| Notion page | `3be833cb-27ff-8159-add6-e883c1cc54af` | `3c0833cb-27ff-810b-a47b-cc15177ae075` | Distinct child-scoped record |
| MCP grant | existing parent grants | `grant_8fad1ae21cb94127b7a8c7dc1efe0ba3` | Distinct active child grant |

Child name: `V1_QUALIFICATION_FIXTURE Continuation 093 Fork Child`.

Child repository: `/home/sketch/Projects/ANIMUS_PRIME_V1_QUALIFICATION_FORK_093`.

Selected immutable revision: `252d71466b92fa3d7979a1b79f02898271b287c1`. The child checkout is detached at that exact revision and has no remotes.

## Durable workflow

- workflow: `workflow_8ef3ede...`
- final state: `SUCCEEDED / FINALIZED`
- durable steps: 17
- child event: `PROJECT_FORKED`, sequence 1, with the exact source revision
- parent activity contains no child Fork event
- child Hindsight contains the child marker and parent Hindsight does not
- child memory: `memory_458b3c...`; parent retained 75 existing memories

The browser replayed the exact confirmed request and returned the existing workflow. Database reconciliation showed one workflow, one child project, one child repository, one child Goal, and one child Fork event. A second exact API replay also returned the same workflow. No duplicate identity or state was created.

## Brain and operator state

The child Brain rendered as `EXACT`, with 451 nodes and 390 edges, `derived-3d`, and `SOURCE_BASED_ONLY`. The AGENT + AUTHORITY filter returned 24 nodes. Selecting `.agent/CURRENT.md` resolved to the child revision and content hash, not the parent.

After a persistent Core restart, authenticated browser re-reads returned HTTP 200 for both projects. The child retained one child-scoped memory; the parent retained 75 memories. Project, repository, Goal, baseline, Notion, Hindsight, credential, Brain, and activity identities remained isolated.

## Refusal matrix

| Case | Result | Mutation |
|---|---|---|
| Invalid source revision | HTTP 400 `FORK_PREFLIGHT_REJECTED` | None |
| Destination outside approved root (`/tmp`) | HTTP 400 | None |
| Existing unrelated destination | HTTP 400 | None |
| Missing confirmation | HTTP 400 | None |
| Stale preflight | HTTP 400 | None |
| Invalid memory content class | HTTP 422 | None |

The valid preflight declared `WRITE_CAPABILITY_UNPROVEN_DEFAULT_CLEAR`, memory copy `NONE`, and a new child Notion page. No untracked parent operator state was discarded or copied as canonical child authority.

## Disposition

The complete frozen Fork acceptance boundary is satisfied. `DOD-016` is `USER_USABLE_VERIFIED`. Existing `R-048` qualification remains preserved.
