---
name: knowledge-base
description: Ask the Open Paws knowledge base, an AI assistant grounded in animal advocacy sources, for a quick answer. Use when the user asks a factual or strategic question about animal advocacy (arguments, evidence, campaigns, organizations, history, terminology) that doesn't need a full research report, or asks to check with Open Paws.
argument-hint: "[question]"
allowed-tools: mcp__plugin_open-paws-tools_open-paws__get_chat_session mcp__plugin_open-paws-tools_open-paws__list_chat_sessions
---

# The Open Paws knowledge base

`send_chat_message` asks Open Paws' knowledge base of animal advocacy sources.
Answers usually take under a minute.

- Send the user's question as `message`, in their words. Use
  `custom_instructions` for format or length ("three bullet points"), and
  `organization` only if the user named one.
- The answer ends with a `session_id: …` line. Pass that id as `session_id` for
  follow-up questions on the same topic, so the knowledge base keeps the
  context. Leave it out to start a new conversation on a new topic.
- Tell the user the answer comes from the Open Paws knowledge base, and keep any
  sources it cites. Don't show them the `session_id` line.
- If a call times out, the answer is usually still saved: find the conversation
  with `list_chat_sessions` (most recent first) and read it with
  `get_chat_session`.
- For an in-depth report with sources, suggest Open Paws Deep Research instead
  (`start_deep_research`). It takes 6–20 minutes.
- `get_me` shows the token's daily limits and how much of them is used.
