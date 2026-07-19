# Enigma Operations

Use this reference for private memory, setup, scheduled ticks, persistence, and adjudication mechanics.

## Contents

1. Game files and Gmail layout
2. Default timing and disclosed conventions
3. Private Markdown memory
4. Wake-up and idempotent action procedure
5. Phase state machine
6. Message classification and scoring
7. Objective generation and replacement
8. Suggested scheduled activation

## 1. Game files and Gmail layout

Create a lowercase game ID from the start date and a short title slug, for example `2026-07-19-nightglass`. Search both the workspace and Gmail before adopting it.

Keep each game's private working memory here:

```text
<workspace>/.enigma-games/<game_id>/GAME_STATE.md
```

The repository ignores `.enigma-games/` because these files contain player emails and secret ground truth. Never commit, publish, attach, or place this file in a shared game thread. Keep all live-game state out of the skill directory itself.

Use these exact Gmail subjects:

- Public: `[ENIGMA][<game_id>] <game title> — Official Game Thread`
- Player private: `[ENIGMA PRIVATE][<game_id>][<player_id>] Objectives and GM Notices`
- GM memory mirror: `[ENIGMA GM][<game_id>] Private Memory`

The public thread contains the authenticated GM and all four players. Always reply with the public anchor or latest public message ID and the exact four-player recipient list. Never place a secret in this thread.

Create one private thread per player. Put initial objectives, replacements, and player-specific administrative replies only in that player's thread. Do not CC a teammate.

Address the GM memory-mirror thread only to `me`. Every reply contains a complete copy of `GAME_STATE.md`, not a patch. Treat it as recovery storage and an audit trail.

Use game statuses `planning`, `active`, and `game_over`. Use team states `planning`, `active`, `final_pending`, `finished_waiting`, and `finished`.

### Gmail identifiers and cursors

Store these identifiers as soon as Gmail returns them:

- `thread_id` for the public thread, all four player-private threads, and the GM memory thread;
- a real Gmail message ID for `reply_message_id` on each thread;
- the most recently observed message ID and timestamp for each thread;
- every processed player message ID and every sent GM message ID.

Thread IDs and message IDs are not interchangeable. Read a known conversation by `thread_id` with `id_type: thread`. Reply with a real message ID through `reply_message_id`; never pass a thread ID in that field.

The Gmail connector does not continuously watch a thread between scheduled activations. At each wake-up, directly fetch the stored thread IDs. Batch-read the public, four private, and memory threads together when possible, initially requesting the most recent 20 messages per thread. Confirm that the saved cursor appears before treating the result as complete. If it does not, expand the exact-thread read until the cursor or the beginning of the thread is reached.

Use mailbox search only to create or recover the index: initial thread discovery when a send response lacks an ID, an unresolved stored ID, a suspected thread split, or uncertain Sent mail. Use an exact game ID/subject query and verify participants before updating memory. Do not perform a broad inbox scan during a healthy scheduled run.

## 2. Default timing and disclosed conventions

Use `America/Chicago`; render deadlines with both local date/time and `CST` or `CDT` as applicable.

If the organizer gives no planning deadline, use the second upcoming noon Central after initialization. This creates a planning window of at least 24 hours and aligns with a daily noon activation.

Round periods are half-open intervals:

- Transmission: `[round_start, round_start + 24h)`
- Codebreaking/final answers: `[round_start + 24h, round_start + 48h)`

A message timestamped exactly at noon belongs to the period beginning at that noon, not the period that just ended. Use Gmail's internal received timestamp. Break identical timestamps by the stable order returned in the full thread, then Gmail message ID.

Publish these operational conventions in the setup email:

1. A player's first apparent team action in a period consumes that team's action even if malformed, duplicated, or over the character limit.
2. Count the newly authored transmission text as Unicode characters, including spaces, punctuation, greetings, signatures, and intentional formatting. Exclude transport headers and automatically quoted thread history. A count over 1,000 makes the transmission invalid.
3. Compare objective categories by the canonical eight-category list. Compare values after trimming surrounding whitespace and quotation marks, collapsing internal whitespace, and ignoring letter case. Otherwise require the exact current wording; do not accept paraphrases, omitted words, corrected spelling, or equivalent locations/times.
4. The first complete final-answer message from a player is final. A complete message supplies exactly the four categories originally owned by that player's teammate. A partial or malformed answer may be replaced before the deadline; once complete, it cannot be revised.
5. If an active team does not announce final submission during Round 25 transmission, it finishes with zero points at that transmission deadline.

Do not change these conventions during a game unless the organizer approves a public prospective ruling.

## 3. Private Markdown memory

Create `GAME_STATE.md` from [GAME_STATE.template.md](../assets/GAME_STATE.template.md). Keep its headings and fill every applicable field. This one file must answer five questions without rereading an entire mailbox:

1. What has already been done?
2. What is the current secret ground truth?
3. What happened during the current Central-calendar day?
4. Where exactly is the game at this activation?
5. What must the GM do next, and when?

Use a monotonically increasing integer revision and ISO 8601 timestamps with explicit offsets. Increment the revision after every material state change. Preserve exact objective values and Gmail IDs. Escape `|` inside Markdown tables as `\|`; preferably generate objective values without that character.

Maintain these sections:

- `Checkpoint`: current game/round/phase, status, deadline, next wake-up, and single most important next action.
- `Players and Threads`: exact identities, teams, fixed ownership, Gmail thread/reply IDs, and last-observed cursors.
- `Team Status`: active/final/finished state, scores, and official submission times.
- `Objective Ground Truth`: all sixteen current values, fixed owners, versions, and compromised-value history.
- `Processed Player Actions`: every accepted, rejected, duplicate, late, or malformed action needed for idempotency and disputes.
- `GM Mail Sent`: every external event key and Gmail message ID.
- `Today's Activity`: a dated plain-language log of what the GM found and did today. Start a new date subsection when the Central date changes; never erase older dates.
- `Next Actions`: ordered checkboxes with due times, prerequisites, exact thread, and event keys.
- `Rulings and Recovery Notes`: public rulings, unusual facts, pending-send uncertainty, and recovery decisions.

For each objective, retain every old version after replacement with its invalidation time and declaration message ID. Ownership never changes.

The top of the file is the wake-up view. Keep it concise and current even if the historical tables grow long. Remove completed items from `Next Actions` only after recording them in the history and today's log.

### Reconcile local memory and Gmail

At activation, compare the local file with the latest complete Gmail mirror:

- Same revision and same substantive content: continue.
- Gmail has a higher revision: restore that complete version locally, then continue.
- Local has a higher revision: verify its recorded Gmail evidence, then mirror it before taking a new external action.
- One copy is missing: rebuild it from the other and record the recovery.
- Same revision but different content, or neither copy is trustworthy: stop and ask the organizer.

Do not paste secret memory contents into chat. Report only public-safe status.

## 4. Wake-up and idempotent action procedure

At the start of every scheduled or manual GM run:

1. Verify current time in `America/Chicago` and Gmail access.
2. Open `GAME_STATE.md`; read `Checkpoint`, today's activity, and `Next Actions` first.
3. Directly read the stored private Gmail memory-thread ID and reconcile the latest mirror with the local file.
4. Batch-read the stored public and player-private thread IDs. Compare their newest message IDs/timestamps with each saved cursor and process only unseen messages.
5. Add a timestamped “woke up” entry under today's date, including what changed since the previous run.
6. If no event is due, refresh `Checkpoint`, `Next Actions`, `Last checked`, and the daily log; increment and mirror the revision only when the file substantively changed.

Before every external game email:

1. Construct a unique event key and exact body marker `ENIGMA-EVENT: <event_key>`.
2. Check `GM Mail Sent` for that key.
3. If absent, search Sent mail using the exact game ID and event key; read any candidate to verify recipients and body.
4. If found, record the recovered event in local memory, increment the revision, and mirror it. Do not resend.
5. If not found, add a pending item to `Next Actions` or `Recovery Notes`, save locally, send once, capture its Gmail IDs/timestamp, then mark it complete in `GM Mail Sent`, update today's log/checkpoint, increment the revision, and mirror the full file.

Never retry solely because a connector result was terse. Search Sent mail first.

One Gmail message may satisfy multiple public event keys only when every literal `ENIGMA-EVENT: <event_key>` marker appears in its body. Record the same Gmail message ID for each key.

Locate a memory mirror with a narrow query such as:

```text
in:anywhere from:me to:me subject:"[ENIGMA GM][<game_id>] Private Memory"
```

Wrap the mirrored Markdown with the literal markers from the private-memory template. Select the complete copy with the highest `Revision` value.

Use full Gmail message bodies for player actions. Strip automatically quoted history only for character counting; preserve the raw message and ID as evidence.

After processing a thread, advance its cursor to the newest fully inspected message. Do not advance past an unreadable, truncated, or otherwise unverified message. A cursor is an efficiency aid, not proof that a message is irrelevant; the processed-action and sent-mail tables remain the idempotency record.

## 5. Phase state machine

### Planning close

- Send each player's private objectives idempotently.
- After all four are confirmed sent, announce that private planning is closed and Round 1 transmission is open.
- Set Round 1, transmission, and the next noon deadline in `Checkpoint`.
- If objective delivery occurs materially after the planned noon boundary, do not backdate Round 1. Open it at the next noon Central and publish the extension. A few minutes of connector latency may retain the planned boundary, but never claim players had hours they did not actually have.

### Transmission close

- Consider only messages from player addresses whose timestamps fall within the transmission interval.
- For each active team, accept its first apparent action: a coded transmission or an explicit final announcement.
- If the action is a final announcement, freeze that team's objective set at its timestamp, set its state to `final_pending`, and prohibit declarations by or against it immediately.
- If Round 25 and an active team did not announce final, finish it with score 0 at the deadline.
- Open the following codebreaking/final-answer period publicly. State which teams are finalizing without revealing secret state.

### Codebreaking close

1. Score final-pending teams from player messages received within the period.
2. For each still-active team, accept its first declaration attempt only when the opposing team remained an eligible target at the declaration timestamp.
3. Resolve declarations against current objectives as they existed at the declaration timestamp. Simultaneous cross-declarations in the same period resolve against the pre-resolution objective state; neither replacement can retroactively affect the other attempt.
4. For every success, invalidate the value, generate a replacement, update memory, and privately notify only the original owner.
5. Determine whether the game has ended under the winning rules.
6. If play continues and Round 25 has not completed, post the round resolution and open the next transmission period.

Always resolve all eligible actions from a period before announcing outcomes. Do not reveal friendly decode progress.

### Final states

- `final_pending`: announcement made; objectives frozen; answers due during the following period; no messages or declarations; cannot be targeted.
- `finished_waiting`: scored below 8 before the opponent finished; score is the threshold to beat.
- `finished`: no further play; result settled for that team.
- `game_over`: winner and scores determined.

If one team finishes first with 8 and the opponent did not announce in the same transmission period, end immediately after verification. If both announced in the same period, score both and apply simultaneous-submission rules. If the first finisher scores below 8, the opponent continues and wins only by exceeding that score; a tie belongs to the first finisher.

## 6. Message classification and scoring

### Transmission

Treat any newly authored public player message during transmission as that player's team action unless it is unmistakably a direct administrative question containing no game transmission or final-announcement intent. Encourage administrative questions by direct email.

Recognize an explicit final announcement by clear meaning, not only exact capitalization. A coded message that incidentally contains the words “final submission” is not an announcement unless its plain public intent is to finish.

Do not decode, identify, or test ciphertext. You cannot enforce the one-objective content rule beyond clear player admissions or observable uncoded violations. Refer suspected hidden-content disputes to the organizer without analyzing the cipher.

### Interception

An attempt must publicly identify the declaring team, one canonical enemy category, and one proposed current value. The first apparent attempt consumes the action even when malformed. Resolve with the normalization rule above. Announce success or failure, not the replacement.

### Final answers

Determine the four categories each player owes from fixed original ownership: a player submits the categories originally owned by that player's teammate. Replacement ownership never moves.

Accept the first complete answer from each player during the final-answer interval. Score one point per exact current value. If a player has no complete submission by the deadline, that player's entire four-answer block scores zero. The team's official submission time is the later timestamp of its two first complete submissions. If either is missing, use the deadline as its comparison timestamp.

For simultaneous announcements, higher score wins; equal score goes to earlier official submission time. If those times are exactly equal, stop and ask the organizer for a tie ruling because the published rules do not define a further tiebreaker.

## 7. Objective generation and replacement

Generate values that are fictional, tasteful, and easy to compare exactly. Avoid real operational instructions, real personal data, slurs, current emergencies, or actionable wrongdoing. Keep each value distinct across both teams when practical.

- Operation codename: `Operation` plus a memorable noun or two.
- Agent codename: a short handle clearly different from player names.
- Rendezvous: a specific fictional or harmless public-facing location phrase.
- Target: a fictional person, object, file, or location; avoid real private people.
- Date/time: include weekday-independent absolute date, time, and Central zone.
- Package/equipment/intelligence: one concrete noun phrase.
- Escape route: one concrete, bounded route phrase.
- Authentication phrase: a memorable sentence unlikely to occur accidentally.

Assign four categories to each teammate with a 4/4 split. Mix short and long values and different semantic types across owners. Ownership remains fixed forever.

For a replacement, preserve category and owner, create a genuinely different value, increment its version, retain the old value with its history, and send only the new value to the original owner. Never reuse any prior value in that game.

## 8. Suggested scheduled activation

Schedule the agent for noon Central every day from the same persistent workspace. Use a prompt that includes send authority, the workspace, and preferably the game ID:

```text
Use $enigma-game-master to administer active Enigma game <game_id> through Gmail and maintain its private memory at <workspace>/.enigma-games/<game_id>/GAME_STATE.md. This scheduled activation authorizes you to read the relevant Enigma threads and send the routine public moderator updates, private objective or replacement notices, and private memory mirrors required by the published game workflow. Do not send unrelated email or change recipients or rules. If no event is due, update the wake-up checkpoint and report that no external action was needed.
```

Daily activation is sufficient because every transmission and codebreaking period lasts 24 hours. Schedule near 12:00 p.m. `America/Chicago`; the state machine still uses exact deadlines if the activation runs late.
