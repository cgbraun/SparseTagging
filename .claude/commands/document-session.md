---
description: Generate documentation entries for this session (SUMMARY, KEY_PROMPTS, OTHER_NOTES)
---

Analyze this Claude Code session and automatically append documentation entries to the appropriate files.

**STEP 1: Generate SESSION-ID**
- Project name: Extract using `basename $(git rev-parse --show-toplevel 2>/dev/null)` or `basename $(pwd)`
- Today's date: Use YYYY-MM-DD format
- Format: `SESSION-{ProjectName}-{YYYY-MM-DD}`

**STEP 2: Analyze conversation for THREADS**

Identify conversation threads (not individual messages) where user and Claude iteratively refine plans/designs/approaches.

Thread boundaries = topic changes (resolved item → new item, planning → implementation, pivot).

**Include threads that:**
- Show iterative refinement through back-and-forth exchanges
- Result in significant decisions (architecture, strategy, design)
- Demonstrate problem-solving: problem → exploration → solution
- Contain substantial user input (2+ lines with meaningful content)

**Exclude threads with:**
- Only 1-line commands or pasted debug output
- Simplistic tasks without design decisions
- Routine implementation (unless approach is novel)

For qualifying threads, **RESTATE** as ONE complete synthesized prompt (all clarifications/refinements, NOT fragments).

**STEP 3: Generate and APPEND entries**

Generate three entries and automatically append them to the files:

**Entry 1: SUMMARY_SESSION.md**
Format:
```
---
SESSION-ID: SESSION-[PROJECTNAME]-[YYYY-MM-DD]
Date: [YYYY-MM-DD]
Title: [2-5 word description]
Category: [Primary] / [Secondary if applicable]
Duration: [Estimate minutes]
Prompts: [Count user prompts]
Tokens: [From /context if available, else "Unknown"]
Impact: [Files modified, lines changed, features added, or "Research only"]
Status: [Complete/Ongoing/Abandoned/Routine]
Key Outcomes: [1-2 sentences]
---
```

Append to: `.claude/SUMMARY_SESSION.md`

**Entry 2: KEY_PROMPTS_AND_PLANS.md (if qualifying threads exist)**
For each thread, format:
```
---
Ref: SESSION-[PROJECTNAME]-[YYYY-MM-DD]
Type: [Architecture/Planning/Debug-Strategy/Testing/Refactoring/Documentation/Research]
Context: [1 sentence]

User Prompt (Restated):
"""
[Complete synthesized prompt with all refinements]
"""

AI Response Type: [Plan/Analysis/Implementation/Questions/Mixed]
Outcome: [1 sentence]
Pattern Category: [Short descriptive name]
---
```

Append to: `.claude/KEY_PROMPTS_AND_PLANS.md`
(Skip if no qualifying threads)

**Entry 3: OTHER_SESSION_NOTES.md (if notable items exist)**
Format:
```
---
Ref: SESSION-[PROJECTNAME]-[YYYY-MM-DD]
Note: [2-3 sentences]
Why Notable: [Significance]
---
```

Append to: `.claude/OTHER_SESSION_NOTES.md`
(Skip if nothing notable)

**STEP 4: Use Bash tool to append entries**

After generating the content, use the Bash tool to append each entry to its file:

```bash
cat >> .claude/SUMMARY_SESSION.md << 'EOF'
[generated entry]
EOF
```

Repeat for KEY_PROMPTS and OTHER_NOTES if applicable.

**STEP 5: Report completion**

After appending all entries, display a summary:
- Which files were updated
- SESSION-ID used
- Number of threads captured
- Any notable items added
