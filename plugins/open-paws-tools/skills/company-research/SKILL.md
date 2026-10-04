---
name: company-research
description: Build an OSINT report on one company with Open Paws Research Companies (its key people, supply chain, recent news and other public information), ready after 5–20 minutes. Use when the user wants a profile or dossier of a company before a campaign, outreach or negotiation, wants to know who decides a company's animal welfare policy or who its suppliers are, or asks for Open Paws company research by name.
argument-hint: "[company name]"
allowed-tools: mcp__plugin_open-paws-tools_open-paws__get_run_result mcp__plugin_open-paws-tools_open-paws__list_runs
---

# Research Companies

Open Paws Research Companies builds an OSINT (open source intelligence) report on
one company from public information: its key people, supply chain, recent news
and more. A run takes 5–20 minutes and costs Open Paws money, so start one run
per company, and only when the user wants such a report. For a question about a
topic rather than one company (for example, which supermarkets kept their
cage-free pledges), use Deep Research instead.

## 1. Pin down the company

You need the company's name. Its website's domain (`examplefoods.com`) tells it
apart from companies with similar names, so ask for it, or suggest the domain
you believe is right and let the user confirm, when the name is ambiguous. If
the user said what the report is for (a campaign's ask, a meeting, a supplier
question), pass that as `report_goal`; otherwise leave it empty for the standard
report. Pass `organization` only if the user named one.

## 2. Start one run

Call `start_org_research` with `company_name`, and `company_domain` and
`report_goal` when you have them. Tell the user it has started and that it
usually takes 5–20 minutes. If a report on this company may already exist (for
example, after the conversation restarted), check `list_runs` before starting
another.

## 3. Wait for it

Call `get_run_result` with the `run_id`. It waits up to 14 minutes for the run
to finish, so one call usually returns the report. If the status is still
`pending`, call it again. If the call itself times out before the run finishes,
call it again with `wait_seconds` set to 40 and keep checking that way.

## 4. Present the report

When the status is `done`, the report follows as markdown. Give the user the full
report unless they asked for a summary, and keep its structure and links. It was
written by AI from public web sources and can confuse people or companies with
similar names, so suggest checking names, roles and figures before acting on
them. It names real people in their professional roles: use it for advocacy
about the company, not to target individuals.

## If something goes wrong

- `error (timeout)`: the run didn't finish within 45 minutes. Offer to try
  again.
- `error (n8n_unreachable)` or `error (n8n_rejected)`: the research service had
  a problem. Suggest trying again later.
- `tool_not_configured`: company research isn't switched on for this server yet.
- `rate_limited`: the message says when the next run can start.
- `unauthorized` or `token_revoked`: the token is missing or no longer valid.
  The user can enter a new one with `/plugin configure open-paws-tools@open-paws`,
  or ask Open Paws for one.

To find an earlier report, call `list_runs`, then `get_run_result` with
`wait_seconds` set to 0.
