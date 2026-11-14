# Semester Week 11 Progress Report

## Completed Work

- Set up the development environment: a Python virtual environment with `openai` and `python-dotenv`, configuration loaded from `.env`.
- Wired the LLM client to OpenRouter through its OpenAI-compatible API, with native tool calling and a normalized response shape.
- Added a real agent run mode to the CLI: `python -m bitlab_ta "question"` runs the full agent, while `--demo` keeps the offline mock run.
- Made the first working end-to-end request: the model selected a tool on its own, used the result and produced the answer.

## Important Commits

- Commit: initial LLM integration over OpenRouter and first working request (hash recorded after push).
- Description: OpenRouter client, real agent run mode in the CLI, environment loading, verified single-tool run.

## Current Functionality

The agent answers a real question against OpenRouter. For "What does task-07-auth require and when is it due?" it called `get_task_context`, read the result and replied with the requirements and deadline, finishing in two steps with stop reason `answer_ready`. The execution trace records the goal, each LLM step, the tool call and the stop. Step and tool-call limits are enforced. Tools still use mock data; the Discord listener is still a skeleton.

## Problems Encountered

- OpenAI-style tool calling uses a different message shape than the one I first wrote the loop against (assistant `tool_calls` and a `tool` role for results).
- In a non-interactive run the console approval prompt received end of input and raised an error.

## Solutions

- The client now returns an internal `LLMResponse` with `text` and `tool_calls`, so the agent loop does not depend on the provider's raw format.
- The console approval handler catches end of input and treats it as a denial, so a run never hangs or crashes.

## What I Learned

- How OpenRouter exposes many models behind one OpenAI-compatible endpoint, selected by the `model` field.
- How a tool-calling turn is structured: the model returns tool calls, the app executes them and feeds back `tool` messages, and the model then produces the final text.
- Why normalizing the provider response keeps the agent loop clean and swappable.

## Next Week

- Implement the core answer flow with structured context handling.
- Validate inputs and outputs more strictly.
- Add the first automated tests, including a loop test with a stubbed LLM client.
