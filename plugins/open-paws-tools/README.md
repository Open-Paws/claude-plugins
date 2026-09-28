# Open Paws Tools

Open Paws' AI tools for animal advocates, in Claude:

- **Deep Research** writes an in-depth report with sources on an animal-related
  question, such as farmed animal welfare, wildlife, animal law and policy, or
  companies' commitments. A run takes 6–20 minutes.
- **The knowledge base** answers questions from animal advocacy sources, usually
  within a minute, and keeps the context for follow-up questions.

The plugin connects Claude to the Open Paws Tools API's MCP server, and adds two
skills that tell Claude when and how to use each tool:
`/open-paws-tools:deep-research` and `/open-paws-tools:knowledge-base`. Claude
also picks them up on its own when a request fits.

## Setup

You need an Open Paws access token (it starts with `opk_`). Install the plugin
from the `open-paws` marketplace, as the [repository README](../../README.md)
shows, and enter the token when Claude Code asks. It's kept in your system
keychain.

## Tools

| Tool | What it does |
|---|---|
| `start_deep_research` | Starts a Deep Research run and returns its `run_id`. |
| `get_run_result` | Waits up to 40 seconds and returns the status: pending, done with the report, or error. |
| `list_runs` | Your runs, newest first. |
| `send_chat_message` | Asks the knowledge base. |
| `list_chat_sessions`, `get_chat_session` | Your knowledge-base conversations. |
| `get_me` | Your token's daily limits and usage. |

Claude asks before it starts a Deep Research run or sends a message. When a
skill is in use, Claude can check on runs and read conversations during that
turn without asking again.

## Data

Your questions and any organization details you add go to the Open Paws Tools
API, which runs them through Open Paws' workflows. Those workflows search the
web and use AI models. Open Paws keeps runs and conversations until you ask for
them to be deleted.
