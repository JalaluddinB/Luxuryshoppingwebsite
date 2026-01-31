---
name: reflect
description: Captures user corrections and discovers workflow patterns to improve future interactions.
---

# Reflection & Learning Skill

Use this skill when the user provides corrections (feedback) or when analyzing workflow patterns.

## Learned Corrections
- Workflow: Prefer `git stash` over `git checkout` to preserve uncommitted work.
- Workflow: Run full test suite (`cargo test`) locally before every commit.
- Workflow: Write tests *before* finalizing feature implementation.
- Interaction: Explicitly propose destructive/irreversible actions (commit, push, overwrite) and await confirmation.
- Interaction: Pause execution immediately upon "No!" or alarm signals.
- Interaction: When correcting mistakes, explain the cause and proposed fix *before* executing it.
- Interaction: Distinguish between generative (code) and additive (docs) tasks; verify file state before writing to docs.
- Workflow: Avoid reading entire large files when targeted edits are possible to prevent "looping"/stalling.

## Capability: Reflect (Learn from Corrections)

When the user provides a correction (e.g., "No, do it this way", "Don't use X", "Remember to Y"):

1.  **Capture the Learning**: Summarize the user's correction into a concise rule.
2.  **Update Memory**: Append this rule to the "Learned Corrections" section in THIS file (`.github/skills/reflect/SKILL.md`).
3.  **Confirm**: Tell the user you have updated the reflection memory with the new correction.

## Capability: Reflect (Discover Patterns)

When the user asks to "reflect on skills" or if you notice the user repeating a complex workflow multiple times:

1.  **Analyze History**: Read the conversation history to identify repeated sequences of commands or requests (e.g., "build then test then run").
2.  **Synthesize**: Draft a new skill definition based on the observed pattern, including a name, description, and steps.
3.  **Propose**: Present the draft skill to the user for review.
4.  **Create**: Upon user approval, create the new Skill file (e.g., `.github/skills/new-workflow/SKILL.md`).