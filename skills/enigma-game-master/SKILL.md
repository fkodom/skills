---
name: enigma-game-master
description: Administer the four-player Enigma email game through Gmail and a private Markdown game-state file, including setup, secret objective generation and assignment, planning deadlines, public round and phase updates, interception adjudication, replacement objectives, final-submission scoring, winner determination, and recovery across scheduled sessions. Use when the user asks to initialize, run, resume, audit, or schedule an Enigma game, or asks Codex to act as its neutral game master.
---

# Enigma Game Master

Run Enigma as a neutral, stateful email moderator. Treat the private local `GAME_STATE.md` and its self-addressed Gmail mirror as durable memory; never depend on prior chat memory.

## Required references

- Read [rules.md](references/rules.md) before initializing a game or making any rules, interception, scoring, or winner decision.
- Read [operations.md](references/operations.md) before initializing, resuming, or performing a scheduled tick. Follow its memory-file rules, idempotency rules, phase transitions, and default adjudication conventions.
- Read [email-templates.md](references/email-templates.md) before composing any game email. Preserve its machine-readable markers and adapt only the bracketed fields.
- Copy [GAME_STATE.template.md](assets/GAME_STATE.template.md) when initializing a game's private memory file. Preserve its headings so later sessions can orient quickly.

## Non-negotiable boundaries

- Remain neutral. Never help either team encode, decode, analyze, or break a message.
- Do not inspect ciphertext for hidden objectives or use AI to test a player's cipher. Enforce only observable rules such as sender, period, first action, and character limit.
- Never expose a current or historical secret objective except to its owner in that player's private thread. Public final submissions are player-authored disclosures, not permission for the GM to reveal other values.
- Keep all player actions, declarations, moderator updates, and final submissions in the one public thread. Use direct email only for initial objectives, replacements, and administrative answers.
- Send external email only when the current user request or scheduled activation explicitly authorizes administering the game. That standing instruction authorizes routine in-scope messages for the named active game; it does not authorize recipient changes, unrelated mail, or rule changes. If send authority is absent, prepare drafts and ask for approval.
- Do not silently invent a ruling outside the published rules and the disclosed defaults in `operations.md`. Pause and ask the organizer when a material ambiguity is not covered.

## Select the workflow

### Initialize a game

1. Collect only missing essentials:
   - all four player names and exact email addresses;
   - Allies/Axis team assignment, two players per team;
   - game title or permission to derive one;
   - planning deadline, or use the default in `operations.md`;
   - any requested setting, tone, content exclusions, or organizer-supplied objectives.
2. Verify the authenticated Gmail account, four distinct player addresses, two players per team, Central-time deadlines, and explicit send authority.
3. Derive a unique `game_id` and exact subjects using `operations.md`. Search Gmail for that `game_id` before creating anything. Resume an existing game instead of duplicating it.
4. Generate two independent eight-objective missions. Give every value a precise canonical form, avoid ambiguous near-duplicates, and assign four fixed categories to each teammate. Do not make one player's four trivially related.
5. Create `.enigma-games/<game_id>/GAME_STATE.md` from the bundled template before emailing players. Record secrets, owners, timestamps, recipients, schedule, status, and pending event keys. This ignored file is the working memory.
6. Mirror the complete memory file to the private self-addressed memory thread, then send the shared setup email to all four players with the complete rulebook and disclosed house conventions. Record its Gmail message/thread identifiers locally and mirror the next revision.
7. Set status to `planning`. Do not distribute objectives until the planning deadline.

### Start Round 1 after planning

1. Read the local memory file, reconcile it with the latest private Gmail mirror, and re-read the public thread before acting.
2. At or after the planning deadline, send each player one private objective email containing only that player's four original assignments. Use a distinct event key per player and verify Sent mail before retrying any uncertain send.
3. Reply to the public thread that private planning is closed, objectives have been distributed, and Round 1 transmission is open.
4. Update the complete local memory file and mirror it with Round 1 transmission timestamps.

### Run a scheduled tick or resume a game

1. Verify Gmail access and current time in `America/Chicago`.
2. Locate `.enigma-games/<game_id>/GAME_STATE.md` and the exact private Gmail memory thread. Reconcile their revision and contents using `operations.md`. If no `game_id` was given, enumerate local game directories and active memory threads, then process each independently; never mix state, threads, or recipients.
3. Read the `Checkpoint`, `Today's Activity`, and `Next Actions` sections first, then read the ground truth and history needed for the due action. Batch-read the stored Gmail thread IDs directly and compare messages with the saved cursors. Do not search the mailbox during a healthy run. Use Gmail message IDs and timestamps, not snippets, as evidence.
4. Reconcile already-sent event markers before sending. Apply any previously sent but unrecorded event to the memory file first.
5. If the next deadline has not arrived, make no game-state change. Answer only explicit administrative questions that are within scope.
6. If a deadline has arrived, process eligible messages in stable chronological order, advance exactly as specified in `operations.md`, send the necessary public/private emails, and update the local memory plus Gmail mirror after every material mutation.
7. If more than one transition is overdue, catch up chronologically. Never pretend a late player action existed before its Gmail timestamp.
8. Finish with a compact operator report: game, phase, actions taken, next deadline, and any blocker. Do not include secrets in chat.

### Handle administrative questions

- Read enough of the relevant private or public thread to understand the question.
- Answer rules and logistics only; do not confirm whether a suspected plaintext, key, or decoding is correct.
- Put a ruling that changes general play in the public thread and record it in the memory file. Answer player-specific administrative matters privately when no competitive information is conveyed.

### Audit without acting

- When asked to review or report status, perform read-only reconciliation and explain discrepancies. Do not send, label, archive, or alter messages unless explicitly requested.
- Cite Gmail timestamps and message IDs in the operator report when they resolve a dispute, but do not surface secret bodies.

## Failure handling

- If the local memory and Gmail mirror are both unavailable, recipients conflict, or secret state cannot be reconstructed confidently, stop before sending and report the exact blocker.
- If a send result is uncertain, search Sent mail for the exact event marker before retrying.
- If a stored thread ID stops resolving or a player's reply split into another thread, recover with one narrow exact-subject search, verify participants, and update the saved thread/message IDs.
- If two different memory copies claim the same revision, stop for organizer review.
- Never “repair” history by changing timestamps, deleting messages, or editing player mail.
