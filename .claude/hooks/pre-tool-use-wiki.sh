#!/bin/bash

# Pre-tool-use hook for wiki nudge
# Reminds Claude to check the wiki before reading source files

# Check if wiki/index.md exists
if [ -f "wiki/index.md" ]; then
    # Output the hook response JSON
    cat <<'EOF'
{"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":"Check wiki/index.md for an article covering this area before reading source. It records runtime behavior and data gotchas the code does not state."}}
EOF
fi

# Always exit 0 to allow tool to proceed
exit 0
