# Lab 7 Mastery Quiz

These questions test the underlying concepts from Lab 7. They are answerable without referring to your lab notes.

---

**Q1.** When does a sub-agent earn its coordination overhead?

- A) When work is separable, parallel, or specialised
- B) Only when the task spans more than one file in the repo
- C) Whenever context length might exceed the single-agent limit
- D) Always; sub-agents consistently outperform a single agent

---

**Q2.** What is the point of the 3-part MCP permission model (Explicit Read / Write / Blocks)?

- A) It speeds up tool calls by pre-authorising the allow list entries ahead of time
- B) It is the required configuration format for any MCP server connection
- C) It replaces manual review; once set, the agent's output is trusted
- D) It names what the workflow can and cannot touch, capping blast radius

---

**Q3.** Why pass a structured handoff (findings/decisions/constraints) to the implementing agent instead of the raw reviewer transcript?

- A) Sub-agents produce transcripts the next session cannot parse correctly
- B) The transcript format is incompatible with the downstream context window
- C) A distilled handoff cuts noise so the implementer acts on signal
- D) Transcripts are encrypted by default and cannot be shared between agent sessions

---

**Q4.** Why run an agentic task inside a git worktree?

- A) It triggers the CI workflow automatically on every commit to the branch
- B) It keeps the main checkout clean and the run is recoverable
- C) It grants the agent write access to external services like Jira
- D) It is the only supported way to open a cross-fork pull request

---

**Q5.** Before turning on auto mode for a workflow, what should you check?

- A) That you activate it via Shift+Tab before you send the first prompt
- B) That the token budget is set to unlimited for the session
- C) That overnight runs are enabled in the project settings file
- D) Whether the worst-case action is recoverable and the task is mostly reads

---

**Q6.** An MCP-connected agent reads a repository README containing hidden prompt-injection instructions. What limits the damage?

- A) Claude Code strips injected instructions before passing them to the model
- B) The MCP server sanitises all tool inputs before they reach the agent
- C) Injected instructions can only invoke the tools your allow list includes
- D) Context window limits prevent the agent from reading oversized injected content

---

**Q7.** Your workflow has a read-only code-review sub-agent and a write-capable implementation sub-agent. Which model pairing is most cost-appropriate?

- A) Sonnet for both to keep output quality consistent across agents
- B) Haiku for the read-only reviewer, Sonnet for the implementer
- C) Opus for the reviewer since code analysis needs the best reasoning
- D) Model choice has no effect on cost for read-only sub-agents
