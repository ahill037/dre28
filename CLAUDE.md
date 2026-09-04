# DreAnalytica Project Agent Contract

## Required Operating Doctrine

- Frame: establish the outcome, authoritative sources, baseline, constraints, scope, risks, and measurable acceptance gates.
- Focus: execute the highest-impact work required for the outcome, preserve unrelated behavior, and do not substitute plans, visual polish, service health, or partial evidence for a working product.
- Finish: continue through root-cause analysis, regression tests, PR, merge, package, deployment, installation, and live acceptance whenever those stages are in scope and authorized.
- Listen: treat the user's definitions, naming, operating principles, and corrections as authoritative; inspect prior decisions and durable evidence.
- Learn: inspect the current repository, runtime, data, logs, tests, and installed product; encode lessons in contracts, tests, and evidence.
- Lead: make reversible, evidence-backed decisions without unnecessary questions; escalate only a true authorization boundary, irreversible risk, unavailable credential, product-intent decision, or external blocker.

## Autonomous End-To-End Ownership

- Own execution from the prompt through the final authorized acceptance gate. Planning, a draft PR, merge, deployment, and service health are not completion by themselves.
- Before implementation and again before merge, fetch the authoritative default branch and inspect open and recently merged PRs for superseding work, conflicts, overlap, schema or contract changes, and reintroduced bugs.
- Consolidate overlaps onto one authoritative implementation; rebase when relevant changes land and rerun focused and regression tests against the refreshed baseline.
- Every bug fix must add or identify a regression test that fails before the fix and passes after it unless technically impossible; document exceptions.
- Do not merge with unresolved conflicts, relevant failing CI, missing migrations or rollback, unevidenced regressions, or unresolved superseding work.
- Record exact source, PR, commit, build, migration, deployment, installation, test, and evidence identities.
- Preserve accepted records, validators, security boundaries, secrets, and unrelated user changes.
- If an external gate blocks completion, finish every preceding gate and report the precise blocker, attempted remediation, owner, evidence, and next executable action.

## Reporting

- Use bullets ordered by impact.
- Separate verified facts, inferences, assumptions, and recommendations.
- Separate plan, code, PR, merge, package, deployment, installation, and live acceptance.
- Never report planned work, acknowledgement, service health, or an unverified deployment as completed work.
- Use durable HTML for authoritative reports when project governance requires an artifact.

