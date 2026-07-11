# Lab 4 — Mastery Quiz

Answer these a week after the lab to test retention of spec-driven development concepts.

**Q1.** What distinguishes a five-element spec from a "prompt like you'd Google"?
- A) It is written in a template file so the model treats it with more weight
- B) It names five elements that together define a verifiable contract
- C) It specifies which model version and temperature settings to use
- D) It always attaches a database schema so the model knows field types

**Q2.** Output doesn't match the spec. What does spec-driven development say to do?
- A) Re-run the prompt with different wording until the output looks right
- B) Update the spec to close the gap, then bring the code into line
- C) Accept the output if all tests pass and move on to the next task
- D) Switch to a more capable model and re-run the same prompt unchanged

**Q3.** Why model a spec's concrete input/output sample on an existing endpoint?
- A) It inflates the spec's word count, making the model read more carefully
- B) It shows expected I/O, steering the model toward existing conventions
- C) It allows you to skip the Format and Constraints sections entirely
- D) It disables the model's built-in schema inference for that route

**Q4.** In Explore→Plan→Code→Commit, what is the point of reviewing the plan before approving?
- A) To catch scope creep and verify each plan step traces to a spec line
- B) To give the model upfront context so it generates code more quickly
- C) To help the model compose a well-structured commit message for the work
- D) To decide which browser flag and editor settings to use for the session

**Q5.** Which is the best example of a good constraint in a spec?
- A) "Be thorough; the model knows what clean and well-structured means"
- B) "No new PyPI dependencies; response excludes internal cost fields"
- C) "Use your best judgment on fields, types, and structure throughout"
- D) "Write the endpoint however you would normally handle this pattern"

**Q6.** Your spec has two constraints that conflict: "return the full record" and "exclude internal cost fields." What is the right fix?
- A) Remove the broader constraint and keep only the more specific one
- B) Revise the spec until the constraints are consistent, then regenerate
- C) Implement both and add a query parameter to let the caller choose
- D) Log the conflict and proceed with whichever constraint the model picks

**Q7.** Contract-first approaches — writing the spec, API definition, or test before code — share a core mechanism with spec-driven development. What is it?
- A) They require a human reviewer to approve the contract before any work begins
- B) They force you to state expected behavior before producing any output
- C) They always produce exactly the same output given the same inputs
- D) They eliminate the need for tests once the contract is formally specified
