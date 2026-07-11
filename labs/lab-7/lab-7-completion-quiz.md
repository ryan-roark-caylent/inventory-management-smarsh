# Lab 7 Completion Quiz

Answer these questions based on what you did in the lab. All questions are multiple choice; select the single best answer.

---

**Q1.** When you dispatched the `code-reviewer` sub-agent on the failing dashboard code, what was true about its access?

- A) It edited `server/main.py` directly to apply the one-line filter fix
- B) It ran in its own context and returned findings but could not write files
- C) It required the Jira MCP to be connected before it could read any files
- D) It merged the PR automatically after completing the review

---

**Q2.** In your `permission-scope.md`, which call did you put under **Explicit Write**?

- A) GitHub `merge_pull_request` on the fork
- B) Jira `create_issue` on one project
- C) GitHub `get_pull_request` check status
- D) Jira `delete_issue` on all projects

---

**Q3.** What made the PR's CI check go red in this lab?

- A) A missing MCP credential that prevented the Jira connection from activating
- B) A merge conflict created when pushing lab-7-work to the personal fork's origin
- C) `test_inventory_count_respects_filter` failing: `total_inventory_items` used the global unfiltered list
- D) A Vitest frontend test failing on an unrelated component in the client directory

---

**Q4.** After `git worktree add ../inv-lab7`, you created a file there. What did `git status` show in the main checkout?

- A) The new file listed as untracked
- B) A merge-in-progress warning
- C) Nothing — the working tree stayed clean
- D) The new file already staged for commit

---

**Q5.** In your Step 2 delegation sort, which task belongs in a single agent rather than delegated to a sub-agent?

- A) Generating pytest tests for 5 independent endpoints
- B) Scanning all API routes for missing auth and authorization gaps
- C) Renaming one local variable (or applying the one-line CORS change)
- D) The full CI-to-Jira read-and-create workflow
