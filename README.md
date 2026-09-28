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

## claude.ai, the desktop app, mobile and Cowork

1. **The tools:** go to **Customize → Connectors → Add custom connector** and
   enter `https://tools-api-production-71f4.up.railway.app/mcp`. If it asks how
   Claude should identify itself, choose **Register automatically**. On a Team or
   Enterprise plan, an Owner adds the connector under **Organization settings →
   Connectors**, and each member connects with their own token.
2. **Connect:** Claude opens the Open Paws sign-in page. Paste your token there,
   once. Claude never sees the token itself: it gets a key for that connection
   and renews it by itself, and the key stops working if your token is revoked.
3. **The skills (optional):** go to **Customize → Plugins → Add → Add
   marketplace**, enter `https://github.com/Open-Paws/claude-plugins`, and install
   **Open Paws Tools**. If you also use Claude Code, it gets a synced copy of the
   plugin; keep one copy there and turn the other off.

## What the plugin sends, and where

Your questions, plus any organization name or instructions you add, go to the
Open Paws Tools API. It runs them through Open Paws' research workflows, which
search the web and use AI models. Open Paws keeps your runs and conversations,
linked to your token, until you ask for them to be deleted. Nothing is stored in
this plugin.

## License

[MIT](LICENSE)
