# Agent skills

Personal agent skills for research, development, and everyday workflows. Each skill packages instructions and any supporting references, scripts, or templates in the [Agent Skills format](https://agentskills.io/).

Use them with Codex, Claude Code, or another compatible agent. The tools and account access needed for each workflow are listed below.

## Available skills

| Skill | What it does | When to use it |
| --- | --- | --- |
| [`seo-aeo-playbook`](skills/seo-aeo-playbook/SKILL.md) | Investigates search and AI-answer visibility, researches reader problems and backlinks, and turns findings into a content strategy. Includes site checks, backlink verification, source analysis, and transcript imports. | Auditing a website, refreshing SEO/AEO strategy, or deciding which content and reputation improvements to prioritize. |
| [`enigma-game-master`](skills/enigma-game-master/SKILL.md) | Moderates the four-player Enigma email game, including secret objectives, round updates, scoring, and durable game state. | Starting, resuming, auditing, or scheduling an Enigma game. |
| [`speedrun`](skills/speedrun/SKILL.md) | Executes pre-scoped Linear tickets in separate Claude sessions, checks CI, and merges completed work into a shared feature branch for review. | Working through execution-ready tickets after their scope and acceptance criteria are settled. |

Each skill's `SKILL.md` contains its full workflow. The SEO playbook also maintains a [source index and coverage register](skills/seo-aeo-playbook/references/sources/index.md), so unfinished research stays visible.

## Installation

### Use the skills CLI

With Node.js and npm available, use the [`skills` CLI](https://github.com/vercel-labs/skills) to browse or install from this repository:

```sh
# List available skills without installing
npx skills add https://github.com/fkodom/skills --list

# Install one skill; choose your agent and scope interactively
npx skills add https://github.com/fkodom/skills --skill seo-aeo-playbook
```

Replace `seo-aeo-playbook` with any name in the table. To choose an agent and install for your user account across projects:

```sh
# Codex
npx skills add https://github.com/fkodom/skills --skill seo-aeo-playbook --agent codex --global

# Claude Code
npx skills add https://github.com/fkodom/skills --skill speedrun --agent claude-code --global
```

Omit `--global` for a project installation. Run the command from that project's directory.

To try an unmerged branch, check out that branch locally and install from the repository root:

```sh
npx skills add . --skill seo-aeo-playbook
```

### Ask Codex to install

You can also use Codex's built-in installer. For example, send this as a prompt:

```text
$skill-installer install seo-aeo-playbook from fkodom/skills, path skills/seo-aeo-playbook
```

Codex discovers installed skills automatically. If a skill does not appear, restart Codex. See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills).

## Tools and accounts

Installing a skill adds its instructions and resources. Set up the tools used by the workflow separately:

| Skill | Requirements |
| --- | --- |
| `seo-aeo-playbook` | Web/browser access for research. Python 3.10+ for the bundled checks; those scripts use the standard library and need no paid SEO account. Search Console or analytics access is needed when inspecting those account reports. |
| `enigma-game-master` | Gmail access, a private writable directory for game state, and scheduling support for automatic rounds. |
| `speedrun` | Claude Code CLI (`claude`), Linear CLI (`linear`), GitHub CLI (`gh`), Git, and access to the target repository and its checks. |

## Using a skill

Ask for the task in plain language, or name the skill explicitly. In Codex, for example:

```text
Use $seo-aeo-playbook to audit our website and prioritize our next SEO improvements.
```

The `speedrun` workflow is written for Claude Code and accepts prompts such as `/speedrun 41-46`. Review each skill's setup and workflow before running it with a different agent.

## Updating installed skills

For installations managed by the skills CLI:

```sh
# Update one user-level installation
npx skills update seo-aeo-playbook --global

# Review installed user-level skills
npx skills list --global
```

## Repository layout

Each skill lives under `skills/<skill-name>/`. Supporting directories are included where the workflow needs them:

```text
skills/<skill-name>/
├── SKILL.md       # Entry point and workflow
├── agents/        # Optional agent metadata
├── references/    # Topic guides and source notes
├── scripts/       # Reusable helpers and tests
└── assets/        # Templates and example formats
```

For the SEO tools' commands, formats, and validation steps, see [Scripts and data contracts](skills/seo-aeo-playbook/references/tooling.md).
