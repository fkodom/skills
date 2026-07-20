# Enigma Email Templates

Use plain, readable email bodies. Replace bracketed fields, retain the `ENIGMA-EVENT` marker, and keep secrets out of public templates.

## Contents

1. Shared setup and rules
2. Private objective assignment
3. Planning close and Round 1 open
4. Codebreaking open
5. Round resolution and next round
6. Successful interception replacement
7. Final-answer call
8. Score and game result
9. Administrative response
10. Private memory mirror

## 1. Shared setup and rules

**To:** all four exact player addresses
**Subject:** `[ENIGMA][<game_id>] <game title> — Official Game Thread`

```text
ENIGMA-EVENT: setup-public

Welcome to Enigma, a four-player game of espionage, secret communication, and codebreaking.

Teams
Allies: <name> <email>; <name> <email>
Axis: <name> <email>; <name> <email>

This is the only public game thread. Keep every coded message, interception declaration, moderator update, final announcement, and final answer here by replying all. Administrative questions may be sent directly to the GM.

Pregame planning is open now and ends <absolute date>, 12:00 p.m. <CST/CDT>. Until objectives are distributed, teammates may communicate privately to agree on a permitted opening cipher, key-change method, formatting, sender plan, and general strategy. Do not build a complete answer codebook or a long list of unrelated future keys. Once the GM announces that objectives have been distributed, all teammate communication must occur in this thread through game messages.

Operational conventions
- Periods use America/Chicago and half-open noon-to-noon windows. A message stamped exactly at noon belongs to the new period.
- A team's first apparent action in a period consumes its action even if malformed, duplicated, or too long.
- The 1,000-character limit counts newly authored text, including spaces, punctuation, greetings, signatures, and intentional formatting; automatically quoted thread history and mail transport headers do not count.
- Category names use the canonical list below. Values are compared after trimming outer whitespace/quotation marks, collapsing internal whitespace, and ignoring case. All other wording must be exact; paraphrases do not count.
- A player's first complete final-answer message is final. Partial or malformed answers may be replaced before the deadline; complete answers may not be revised.
- An active team that does not announce final submission during Round 25 transmission finishes with zero points.

FULL RULES

<paste the complete current contents of references/rules.md here, omitting its Markdown title only>

The GM will send each player's four objectives privately when planning closes. Good luck.
```

## 2. Private objective assignment

**To:** one player only
**Subject:** `[ENIGMA PRIVATE][<game_id>][<player_id>] Objectives and GM Notices`

```text
ENIGMA-EVENT: objectives-<player_id>-v1

<player name>, you are on the <Allies/Axis> team.

These four categories are your fixed original assignments. Preserve the exact wording. Your teammate does not receive these values directly; you must communicate each current value through later coded messages in the public game thread.

<Canonical category label>: <exact current value>
<Canonical category label>: <exact current value>
<Canonical category label>: <exact current value>
<Canonical category label>: <exact current value>

Ownership of these categories remains yours if a value is replaced. Do not reply with mission information. Direct replies to the GM are for administrative questions only.

Private planning ends when the GM opens Round 1 in the public thread.
```

## 3. Planning close and Round 1 open

Reply all in the public thread.

```text
ENIGMA-EVENT: round-1-transmission-open

Planning is closed. All four private objective assignments have been sent. From this timestamp forward, teammates may communicate only through permitted coded messages in this public thread.

Round 1 — Transmission Period
Open: <timestamp Central>
Closes: <timestamp Central>

Each team may post one coded message of no more than 1,000 characters or announce its final submission. If both teammates act, only the team's first action is considered.
```

## 4. Codebreaking open

```text
ENIGMA-EVENT: round-<n>-codebreaking-open

Round <n> transmission is closed.

<Optional public-safe notes about invalid/duplicate team actions.>

Round <n> — Codebreaking Period
Open: <timestamp Central>
Closes: <timestamp Central>

Each eligible active team may post one interception declaration naming one enemy objective category and its proposed exact current value. <Finalizing team names> must instead have both teammates publicly submit the four objectives originally assigned to their teammate by the deadline.
```

## 5. Round resolution and next round

```text
ENIGMA-EVENT: round-<n>-resolution

Round <n> complete.

Allied interception: <succeeded / failed / no eligible declaration>
Axis interception: <succeeded / failed / no eligible declaration>
Teams remaining active: <teams>

Round <n+1> — Transmission Period
Open: <timestamp Central>
Closes: <timestamp Central>

Each active team may post one coded message or announce its final submission. <If n+1 is 25: Round 25 is mandatory final submission; coded messages are not permitted.>
```

Do not publish an interception line for a frozen team if doing so would imply it was still eligible. A success may name the compromised category because the declaration already made it public, but never publish the replacement.

## 6. Successful interception replacement

Reply only in the original owner's private thread.

```text
ENIGMA-EVENT: replacement-<team>-<category-key>-v<version>

Your team's <Canonical category label> was successfully intercepted. The prior value is invalid.

Replacement <Canonical category label>: <exact new value>

You remain the owner of this category. Communicate the replacement to your teammate through a later permitted coded message. Do not reply with mission information.
```

## 7. Final-answer call

Use as part of the codebreaking-open message or as a separate idempotent public reply.

```text
ENIGMA-EVENT: final-call-<team>-round-<n>

The <team> final announcement is recorded. Its objectives are frozen, and it can no longer send messages, make declarations, or be targeted.

By <deadline Central>, each <team> player must post one complete public answer containing only the four categories originally assigned to their teammate, with each category and exact current value. The first complete answer from each player is final. A player without a complete answer by the deadline scores zero for that four-answer block.
```

## 8. Score and game result

```text
ENIGMA-EVENT: final-result-<team>-round-<n>

<Team> final score: <score>/8.
Official submission time: <timestamp Central>.

<If play continues: This is the score to beat. <Opponent> remains active and must score higher to win.>
```

When the game ends:

```text
ENIGMA-EVENT: game-result

Enigma is complete.

Allies: <score or not submitted>/8
Axis: <score or not submitted>/8
Winner: <team>
Tiebreak applied: <none / first finisher / earlier official submission time>

Thank you for playing.
```

Do not list secret objective values in the GM's score or result message.

## 9. Administrative response

```text
ENIGMA-EVENT: admin-<game_id>-<short-unique-id>

GM ruling: <concise answer grounded in the published rules>

This ruling <does / does not> change general play. <If it does, it will also be posted publicly and applies prospectively.>
```

Do not answer questions about whether a cipher, key, plaintext guess, or friendly decode is correct.

## 10. Private memory mirror

**To:** `me`
**Subject:** `[ENIGMA GM][<game_id>] Private Memory`

```text
ENIGMA-EVENT: memory-revision-<revision>

Private GM memory. Do not forward or add recipients.

ENIGMA-GM-MEMORY
<complete current contents of GAME_STATE.md>
END-ENIGMA-GM-MEMORY
```
