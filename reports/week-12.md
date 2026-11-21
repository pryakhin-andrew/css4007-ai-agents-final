# Semester Week 12 Progress Report

## Completed Work

- Strengthened the core answer flow with input and output validation.
- Added `validate_question`: empty or over-long questions are rejected before the agent runs, with a recorded guardrail event.
- The agent now stores every tool result in its execution state (`state.context`), so the gathered context is explicit and inspectable.
- Added output validation: an empty final answer is treated as a failure, not a success.
- Wrote the first automated tests: 19 tests across tools, guardrails and the agent loop, all passing. The loop tests use a stubbed LLM client, so they run offline with no API cost.

## Important Commits

- Commit: core validation, explicit state and the first test suite (hash recorded after push).
- Description: adds question and answer validation, stores tool results in state, and adds 19 tests covering tools, guardrails and the agent loop.

## Current Functionality

The agent validates the incoming question, runs the tool-calling loop, records each tool result in its state, and validates that the final answer is non-empty before reporting success. It distinguishes completed, stopped and failed outcomes with explicit stop reasons. The test suite covers found and not-found tool paths, argument validation, injection detection, the limit stop, an invalid question, an empty answer and a failed tool call. Tools still use mock data; the Google Sheets and Bitlab integrations come in Week 13.

## Problems Encountered

- The execution state existed but was never populated, so the gathered context was not actually tracked.
- A successful run and an empty answer were not distinguished.

## Solutions

- Tool results are now written into `state.context` keyed by the tool name as they are produced.
- The loop checks the final answer and marks an empty one as `failed` with stop reason `empty_answer`.

## What I Learned

- How to test an agent loop deterministically by injecting a stubbed LLM client that returns scripted tool calls and text, which keeps tests fast and free.
- Why input and output validation belong around the model, not inside the prompt.

## Next Week

- Replace the mock student and task tools with the real Google Sheets and Bitlab integrations.
- Add a tool permission policy (read-only data access, approval-gated sending).
