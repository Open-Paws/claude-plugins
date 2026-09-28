# Open Paws plugins for Claude

Plugins that bring [Open Paws](https://openpaws.ai)' AI tools for animal
advocates into Claude.

| Plugin | What it adds |
|---|---|
| [`open-paws-tools`](plugins/open-paws-tools) | Deep Research reports with sources, and quick answers from the Open Paws knowledge base of animal advocacy sources. |

## Install in Claude Code

You need an Open Paws access token. It starts with `opk_`; ask Open Paws for one.

In a Claude Code session (in a terminal, an IDE, or the Claude desktop app's Code
tab), run:

```text
/plugin marketplace add Open-Paws/claude-plugins
/plugin install open-paws-tools@open-paws
```

Claude Code asks for your token and keeps it in your system keychain. Then ask
for what you need, for example "Research cage-free egg commitments by UK
supermarkets since 2020", or run `/open-paws-tools:deep-research`.

- Needs Claude Code 2.1.269 or later.
- To change the token: `/plugin configure open-paws-tools@open-paws`.
- To get updates: `/plugin marketplace update open-paws`.

## claude.ai, the desktop app and Cowork

The plugin's skills load there too, but its connection to the Open Paws server
needs a token, and those apps can't ask for one. Until Open Paws offers
sign-in, an Owner of your Claude organization can add the server as a custom
connector:

- URL: `https://tools-api-production-71f4.up.railway.app/mcp`
- Request header: `authorization`, with the value `Bearer opk_…`

Request headers are a Claude beta that not every organization has yet, and
everyone in the organization then shares that one token.

## What the plugin sends, and where

Your questions, plus any organization name or instructions you add, go to the
Open Paws Tools API. It runs them through Open Paws' research workflows, which
search the web and use AI models. Open Paws keeps your runs and conversations,
linked to your token, until you ask for them to be deleted. Nothing is stored in
this plugin.

## License

[MIT](LICENSE)
