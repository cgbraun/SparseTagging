\# Key Prompts and Plans



Significant user prompts and resulting plans/architectures from Claude Code sessions.



\## Inclusion Criteria

\*\*Evaluate conversation threads, not isolated messages.\*\*

\*\*Include conversation threads that:\*\*

1\. \*\*Show iterative refinement\*\* - User and Claude refine a plan/design/approach through back-and-forth exchanges

2\. \*\*Result in significant decisions\*\* - Architecture choices, implementation strategies, design patterns

3\. \*\*Demonstrate problem-solving process\*\* - From problem statement → exploration → constraints → solution

4\. \*\*Contain substantial user input\*\* - 2+ lines with meaningful content (not just commands)

\*\*Aggregate related exchanges into ONE entry\*\* showing the full collaborative process.

\*\*Thread boundaries (topic changes):\*\*

\- Resolved one item and moved to another

\- Finished planning and started implementation

\- Pivoted to different problem/approach

\*\*Exclude:\*\*

\- 1-line simple commands ("fix X", "proceed", "continue")

\- Pasted debug/error output (even with brief context)

\- Simplistic multi-line tasks ("rename these 5 functions", "update version numbers")

\- Routine implementation without design decisions

\*\*Edge Cases:\*\*

\- \*\*Iterative debugging:\*\* Capture if conversation leads to significant approach change (not just "fix line 23")

\- \*\*Abandoned explorations:\*\* Keep if significant per standard criteria (shows valuable reasoning/anti-patterns)

\- \*\*Significance:\*\* Use qualitative judgment, not message count thresholds



\## Entry Format

```

---

Ref: SESSION-\[PROJECTNAME]-\[YYYY-MM-DD]

Type: \[Architecture/Planning/Debug-Strategy/Testing/Refactoring/Documentation/Research]

Context: \[1 sentence - what situation prompted this thread]

User Prompt (Restated):

"""

\[Complete prompt restated with all clarifications, refinements, and updates from the conversation thread - NOT individual fragments, NOT a summary, but a complete synthesized prompt]

"""

AI Response Type: \[Plan/Analysis/Implementation/Questions/Mixed]

Outcome: \[1 sentence - what was delivered]

Pattern Category: \[Short descriptive name for reuse]

---

```



---



<!-- PROMPT ENTRIES APPENDED BELOW -->


---
Ref: SESSION-SparseTagging-2026-01-11
Type: Planning
Context: User created session documentation templates and needed system validation, refinement, and automation to eliminate manual workflow steps.

User Prompt (Restated):
"""
Design and implement an automated session documentation system for Claude Code that captures sessions for retrospectives and training purposes.

**Core Requirements:**
- Session = One Claude Code conversation (even if spans multiple days)
- SESSION-ID uses date only for chronological ordering (format: SESSION-ProjectName-YYYY-MM-DD)
- Purpose: Retrospectives and training, not complete history tracking
- Automated workflow triggered by simple slash command (no manual copy/paste)
- Works identically for current and old/resumed sessions

**Documentation Structure:**
Four files in .claude/ directory:
1. SUMMARY_SESSION.md - All sessions for statistics and reference
2. KEY_PROMPTS_AND_PLANS.md - Significant prompts using thread-based aggregation
3. OTHER_SESSION_NOTES.md - Insights, breakthroughs, anti-patterns
4. PROMPTING_PATTERNS.md - Reusable patterns across sessions

**Thread-Based Aggregation Criteria:**
Evaluate conversation threads, not isolated messages. Include threads that:
- Show iterative refinement through back-and-forth exchanges
- Result in significant decisions (architecture, strategy, design patterns)
- Demonstrate problem-solving: problem → exploration → constraints → solution
- Contain substantial user input (2+ lines with meaningful content)

Thread boundaries defined by topic changes:
- Resolved one item and moved to another
- Finished planning and started implementation
- Pivoted to different problem/approach

For qualifying threads, restate as ONE complete synthesized prompt incorporating all clarifications, refinements, and constraints from the conversation (not individual fragments, not a summary).

Exclude:
- 1-line simple commands
- Pasted debug output
- Simplistic multi-line tasks without design decisions
- Routine implementation

**Implementation Approach:**
Create /document-session slash command that:
- Auto-generates SESSION-ID from project name and today's date
- Identifies conversation threads per criteria above
- Automatically appends formatted entries to documentation files using Bash tool
- No manual copy/paste required
- Works same way for current and old sessions

**Key Simplifications:**
- No start-session helper scripts
- No timestamp capture files
- No time component in SESSION-ID (date only)
- Same SESSION-ID acceptable for multiple sessions on same day
- Fully automated 10-second workflow

**Technical Requirements:**
- Slash command file requires YAML frontmatter with description field
- Use Bash tool with heredoc syntax to append entries to files
- Validate on current session before finalizing
- Update all template files to match new format
- Delete obsolete complexity (timestamp scripts, manual extraction prompt)
"""

AI Response Type: Mixed (Planning → Implementation → Debugging → Refinement)
Outcome: Implemented fully automated /document-session command with thread-based aggregation and automatic file appending; reduced workflow from manual 30-second copy/paste to automated 10-second execution; validated on live session; fixed slash command frontmatter requirement.
Pattern Category: Workflow Automation via Progressive Simplification
---
