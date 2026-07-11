# Lab 1 — Mastery Quiz

**Instructions:** These questions test your understanding of the concepts from Lab 1. Answer based on your knowledge, not just what you observed during the session.

---

**Q1.** Why does Claude.ai typically give a less specific fix than Claude Code for a bug that lives in your repo?

- A) Claude.ai has no access to the repo, so it reasons from the symptom you describe rather than reading the code
- B) Claude.ai uses a smaller default model than Claude Code, which limits how deeply it can reason about any code-level bugs
- C) Claude.ai applies rate limits to long responses, causing it to truncate output before identifying the exact file and line
- D) Claude.ai cannot execute or read Python files, so it can only describe a fix in general prose terms

---

**Q2.** A task needs Claude to run unattended across many files inside a CI pipeline, with no human in the loop. Which surface fits?

- A) API/CI
- B) Claude.ai
- C) Claude Code interactive session
- D) Claude Cowork

---

**Q3.** You pick a higher reasoning/effort tier for one task and a lighter one for another. What should drive that choice?

- A) The complexity and risk of the task
- B) Whichever model you happened to use last time
- C) Whichever tier is the cheapest to run that day
- D) The file extension of the code you are editing

---

**Q4.** What is Claude Cowork best suited for?

- A) Doc- and plan-oriented work in a desktop app, away from a live repo checkout
- B) Running the FastAPI test suite automatically on every commit as part of the CI pipeline
- C) Tracing a null-pointer exception three function calls deep into the backend service code
- D) Auto-completing single lines or short blocks of code directly inside your editor window

---

**Q5.** "Same model every time; the only thing that changed was which surface I picked." What is the practical takeaway?

- A) Match the surface to the shape of the task instead of defaulting to whatever's already open
- B) Always start in Claude Code because it is the most capable surface for any technical task
- C) The model tier you select matters more than which surface you open for a given task
- D) Use all four surfaces once per task so you can benchmark and pick the best one

---

**Q6.** What makes Claude Code repo-aware when Claude.ai is not, given both use the same underlying model?

- A) Claude Code uses tool calls to read files in your local filesystem; Claude.ai only sees what you type or paste
- B) Claude Code downloads a full repo snapshot to Anthropic servers on startup; Claude.ai has no network access to local files
- C) Claude Code uses a fine-tuned variant trained on code repositories; Claude.ai uses the general-purpose version with no code tuning
- D) Claude Code hooks into your IDE's language server, giving it cross-file context that Claude.ai cannot access without a plugin

---

**Q7.** A data team wants Claude to summarize newly landed files every night and post the result to Slack, with no human triggering it. Which surface fits?

- A) API/CI: a scheduled script calls the API with the file contents and posts the result through Slack's webhook
- B) Claude.ai: a team member opens the browser each morning, pastes the files, and copies the summary to Slack manually
- C) Claude Code: a developer runs the CLI each night, reviews the summary interactively, then pastes it into Slack
- D) Claude Cowork: the desktop app monitors the file directory, generates summaries, and routes them to Slack automatically

---

**Q8.** You finish a long Claude.ai planning session and switch to Claude Code to implement the plan. What context does Claude Code start with?

- A) A blank context; Claude Code reads the repo but has no memory of the Claude.ai conversation
- B) The last exchange from Claude.ai, which is automatically injected as Claude Code's opening system prompt
- C) The full Claude.ai conversation, which syncs through your Anthropic account session to Claude Code on launch
- D) A brief summary of the Claude.ai thread that Claude Code generates by querying the Claude.ai session history
