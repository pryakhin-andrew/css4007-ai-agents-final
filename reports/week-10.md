# Semester Week 10 Progress Report

## Completed Work

- Chose the project topic: Bitlab TA Assistant, an autonomous Discord agent that helps me answer student questions, and selected A level.
- Wrote the full proposal in `reports/proposal.md`: problem, users, functions, the three agent tools, model choice, architecture, example requests, evaluation plan and weekly milestones.
- Built the Python project skeleton under `bitlab_ta/`: settings from environment, execution state, a tool base class and registry, three tools (student lookup, task context, Discord reply), an agent loop with limits and stopping conditions, guardrails and an execution trace.
- Added a runnable demo (`python -m bitlab_ta`) that lists the tools and exercises the mock student and task tools, including the not-found path.
- Updated `.env.example` and `requirements.txt`; confirmed secrets stay out of the repository.

## Important Commits

- Commit: project scaffold and Week 10 proposal (hash recorded after push).
- Description: adds the `bitlab_ta` package, mock tools, agent loop skeleton, guardrails and the completed proposal and weekly report.

## Current Functionality

The agent loop, tool registry and guardrails are in place as structure. The runnable demo registers the three tools and returns mock student and task data, and shows the student-not-found path. Real LLM calls and the live Discord listener are not wired yet; that is Week 11. Tools use mock data until Week 13.

## Problems Encountered

- Discord does not let a bot read my personal direct messages, and automating a personal account breaks Discord's terms.
- It is not yet confirmed whether the Bitlab portal exposes an API for task data.

## Solutions

- The design uses a dedicated bot account: students message the bot, and in channels the bot reacts to mentions. This is compliant and keeps the approval flow clean.
- Tools return mock data behind a stable interface, so the Google Sheets and Bitlab integrations can replace the mocks in Week 13 without changing the agent. Whether Bitlab offers an API will be checked before then; if not, a read-only fallback will be used.

## What I Learned

- How Anthropic tool calling is structured: tool schemas, `tool_use` blocks and `tool_result` messages fed back to the model.
- Why consequential actions (sending a message) must be gated in application code, not only in the prompt, and why external input must be treated as untrusted data.
- How to express an agent as a bounded loop with explicit state, step and tool-call limits, retries and stopping reasons.

## Next Week

- Integrate the LLM API and make the first real request end to end.
- Wire the Discord listener to the agent and implement the approval DM to the mentor.
- Add the first tests for tool validation and the agent loop with a stubbed LLM client.
