# KB decision note

Two artifacts now live on this codebase: the graphify code graph and the LLM wiki.

## Question A — "What breaks if I change apply_filters()?"
Reached for: the graphify code graph.
Why: `graphify affected "apply_filters"` lists the endpoints that call it in one command.
This is a structural, static question — what the AST graph answers well.

## Question B — "Why does the app's locale persist across page reloads?"
Reached for: the LLM wiki.
Why: the answer is localStorage ('app-locale' in useI18n.js), a runtime behavior the graph
cannot see. The graph shows useI18n's 26 import edges but never why locale survives a reload.

## One judgment call I made
I did not run `graphify label` (no backend configured). The unlabeled Community_N wiki is
enough to make the free-graph / paid-navigation tradeoff concrete; I reasoned about the token
cost instead of paying it.
