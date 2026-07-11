# Lab 5 — Mastery Quiz

These questions probe the underlying concepts. Answer them without referring to the lab steps.

---

**M1.** Which sequence correctly states the four steps of the debugging loop?

- A) explain → hypothesis → confirm/challenge → fix
- B) hypothesis → explain → fix → confirm/challenge
- C) explain → confirm/challenge → hypothesis → fix
- D) fix → explain → hypothesis → confirm/challenge

---

**M2.** In a multi-file change touching the model, data, route, and Vue layers, where does the single highest-value checkpoint belong?

- A) Immediately after the model change and before editing any dependent layers
- B) After all dependent layers are edited, as a final gate before committing the feature
- C) Before any changes run, to establish a green baseline all changes must return to
- D) Split across layers — one checkpoint after each individual file to catch errors incrementally

---

**M3.** You finished a debugging phase and reached a written conclusion. You are now switching to an unrelated feature. Which sequence is correct?

- A) `/compact` to keep the conclusion, then `/clear` before starting the new task
- B) `/clear` to drop the noise, then `/compact` to seed the new task's context
- C) `/compact` twice — once after debugging, once after completing the unrelated task
- D) `/clear` only — a single wipe handles both the debug session and the new task's context

---

**M4.** A `response_model` endpoint returned HTTP 500 with no changes to the route function. Which explanation is correct?

- A) FastAPI validates each response against `response_model`; a required field absent from the data fails serialization
- B) HTTP 500 is always a route function error; `response_model` only validates the schema of the incoming request body
- C) FastAPI skips response validation by default; the 500 was caused by an unhandled exception in the route function's filter logic
- D) The route was silently unregistered when the Pydantic model was modified; hot-reloading the server re-registers the route

---

**M5.** After the model layer is verified, which statement about completing the remaining layers is correct?

- A) Data and route serialization can proceed in parallel; the Vue display follows once the API contract holds
- B) All remaining layers must proceed in strict sequence: data first, then route, then Vue
- C) Route must precede data because `response_model` determines which fields need to be backfilled
- D) Vue can start immediately alongside data and route because it reads from the API, not from the model directly

---

**M6.** *(Beyond-lab mastery)* A developer adds a required field to a shared Pydantic model and sees test failures across four unrelated test modules. Applying blast-radius reasoning, what does this pattern indicate?

- A) The model is a root node; its required-field contract propagates failures to every consumer
- B) The developer introduced a separate bug in each test module while adding the field
- C) The test runner duplicates failures across modules when a Pydantic validation error is raised
- D) Required-field failures always appear in proportion to the number of test modules in the project

---

**M7.** *(Beyond-lab mastery)* The debugging loop makes the hypothesis a required written step. What does this requirement prevent?

- A) Accepting the model's first explanation without testing it against evidence
- B) Running the explain step before you have formed any initial understanding of the failure
- C) The model repeating the same incorrect explanation multiple times across the session
- D) Forgetting to record the final fix decision in the intervention log after the session ends
