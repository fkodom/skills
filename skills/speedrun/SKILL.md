---
name: speedrun
description: Run a sequence of pre-scoped tickets back-to-back, each in its own
  non-interactive Claude sub-session. Triggers on "/speedrun 41-46".
allowed-tools: Bash, Read, Edit
---

# Speedrun

Drive a sequence of pre-scoped, execution-ready tickets to completion, one after
the next. You (the main agent) are the babysitter: set up branches, hand each
ticket to a fresh non-interactive sub-session, wait for CI, and merge the result.

Core assumption: these tickets are already scoped and reviewed. This is an
execution run, not design. If a ticket turns out to need real exploration, STOP
and hand it back to the human.

## 1. Set up one feature branch for the whole run

```bash
git checkout -b feature/<slug> && git push -u origin feature/<slug>
```

## 2. For each ticket, in order

Fetch the ticket and read its acceptance criteria:

```bash
linear issue view <id>
```

Branch off the latest feature branch:

```bash
git checkout feature/<slug> && git pull
git checkout -b ticket/<id>
```

Hand the ticket to a non-interactive sub-session. There are no special hooks here,
so the prompt itself tells the sub-session to commit and open its own PR:

```bash
claude -p --dangerously-skip-permissions "$(cat <<PROMPT
Implement exactly this ticket, no more and no less:

<title, description, and acceptance criteria from Linear>

When the work is done and the project's typecheck and tests pass, commit your
changes, push branch ticket/<id>, and open a PR into feature/<slug>.
Follow CLAUDE.md conventions throughout.
PROMPT
)"
```

Watch CI, then merge into the feature branch:

```bash
gh pr checks <pr> --watch
gh pr merge <pr> --merge
```

If CI fails on something trivial (a missed import, a lint nit), fix it yourself on
the branch and re-push. If it needs real debugging, STOP and hand back to the human.

## 3. Wrap up

Report which tickets merged and which are blocked. Do NOT merge the feature branch
into main. That is the human's review gate.
