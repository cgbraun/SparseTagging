\# Session Documentation Quick Reference



\## Setup (One-time)



1\. Create `.claude/` directory in project root

2\. Create these four files (use templates provided):

&nbsp;  - `SUMMARY\_SESSION.md`

&nbsp;  - `KEY\_PROMPTS\_AND\_PLANS.md`

&nbsp;  - `OTHER\_SESSION\_NOTES.md`

&nbsp;  - `PROMPTING\_PATTERNS.md`

3\. Ensure `.claude/commands/document-session.md` exists (slash command)



\## Workflow



\### At End of Session



\*\*Step 1:\*\* Type `/document-session` in Claude Code



\*\*Step 2:\*\* Done! Entries are automatically appended to:

\- `.claude/SUMMARY\_SESSION.md`

\- `.claude/KEY\_PROMPTS\_AND\_PLANS.md` (if qualifying threads exist)

\- `.claude/OTHER\_SESSION\_NOTES.md` (if notable items exist)



\*\*Time:\*\* 10 seconds per session



\### Works for Current and Old Sessions



\- \*\*Current session:\*\* Type `/document-session` before closing

\- \*\*Old/resumed session:\*\* Open the conversation, type `/document-session`

\- SESSION-ID uses today's date for chronological ordering

\- Same workflow regardless of when session occurred



\## What Gets Documented



\*\*Do document:\*\*

\- Every session (even short ones) in SUMMARY

\- Conversation threads showing iterative refinement/design decisions in KEY\_PROMPTS

\- Workflow improvements and insights in OTHER\_SESSION\_NOTES



\*\*Don't document:\*\*

\- 1-line commands in KEY\_PROMPTS

\- Pasted error messages in KEY\_PROMPTS

\- Simplistic multi-line tasks in KEY\_PROMPTS

\- Trivial sessions can be marked "Routine" in SUMMARY



\*\*KEY\_PROMPTS captures threads, not individual messages:\*\*

\- Aggregate related exchanges showing problem → solution progression

\- Restate as one complete synthesized prompt

\- Thread boundary = topic change (resolved → new item, planning → implementation)



\## SESSION-ID Format



\- `SESSION-PROJECTNAME-YYYY-MM-DD`

\- Project name from git/directory

\- Date: Today's date (for chronological ordering)

\- Same ID if multiple sessions documented same day (acceptable)



\## Periodic Pattern Analysis



After documenting 5-10 sessions:



\*\*Prompt to use in Claude Code:\*\*

```

Review my KEY\_PROMPTS\_AND\_PLANS.md file and identify recurring patterns.



For each pattern found, create entry for PROMPTING\_PATTERNS.md following the template format.



Abstract away project-specific details. Focus on:

\- General approach/structure

\- What makes it effective

\- Measurable outcomes when applicable

\- Cross-reference SESSION-IDs using the pattern

```



\## File Maintenance



\*\*Monthly:\*\* Sort entries by date if desired (currently append-order)



\*\*Quarterly:\*\* Run pattern analysis to update PROMPTING\_PATTERNS.md



\*\*As needed:\*\* Clean up duplicate/low-value entries



\---



\*\*Version History:\*\*

\- v1.0 (2025-01-11): Initial templates for manual workflow

\- v2.0 (2026-01-11): Simplified with `/document-session` command, date-only SESSION-IDs
