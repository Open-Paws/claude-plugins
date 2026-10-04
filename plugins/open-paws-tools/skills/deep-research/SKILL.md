---
name: deep-research
description: Research an animal-related question in depth with Open Paws Deep Research, which returns a report with sources after 6–20 minutes. Use when the user wants a researched report, briefing or evidence review on animal advocacy, farmed animals, wildlife, animal law or policy, or companies' animal welfare commitments, or asks for Open Paws Deep Research by name.
argument-hint: "[research question]"
allowed-tools: mcp__plugin_open-paws-tools_open-paws__get_run_result mcp__plugin_open-paws-tools_open-paws__list_runs
---

# Deep Research

Open Paws Deep Research writes an in-depth report with sources. A run takes 6–20
minutes and costs Open Paws money, so start one run per question, and only when
the user wants a researched report. For a quick answer, use the Open Paws
knowledge base instead (`send_chat_message`).

## 1. Agree on the question

A good brief names the topic, the places, the time frame, the angle, and who the
report is for. For example: "Cage-free egg commitments by UK supermarkets since
2020: which were met, which were dropped, and how campaigners responded." If the
request is too vague to research well, ask one round of questions first. Pass
`organization` only if the user named one.

## 2. Start one run

Call `start_deep_research` with the brief as `prompt`. Tell the user it has
started and that it usually takes 6–20 minutes. If a run for this question may
already exist (for example, after the conversation restarted), check `list_runs`
before starting another.

## 3. Wait for it

Call `get_run_result` with the `run_id`. It waits up to 14 minutes for the run
to finish, so one call usually returns the report. If the status is still
`pending`, call it again. If the call itself times out before the run finishes,
call it again with `wait_seconds` set to 40 and keep checking that way.

## 4. Present the report

When the status is `done`, the report follows as markdown. Give the user the full
report unless they asked for a summary, and keep its structure and links. Don't
add sources it doesn't cite. It was written by AI from web sources, so suggest
checking key facts and figures before they're published.

## If something goes wrong

- `error (timeout)`: the run didn't finish within 45 minutes. Offer to try
  again, perhaps with a narrower question.
- `error (n8n_unreachable)` or `error (n8n_rejected)`: the research service had
  a problem. Suggest trying again later.
- `rate_limited`: the message says when the next run can start.
- `unauthorized` or `token_revoked`: the token is missing or no longer valid.
  The user can enter a new one with `/plugin configure open-paws-tools@open-paws`,
  or ask Open Paws for one.

To find an earlier report, call `list_runs`, then `get_run_result` with
`wait_seconds` set to 0.
