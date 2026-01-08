# Effective Prompting Patterns for AI-Assisted Development

**Source:** SparseTagging Project Development Sessions
**AI Assistant:** Claude Code (Sonnet 4.5)
**Context:** Multi-session development including CI/CD improvements, testing, debugging, and documentation

---

## Table of Contents

- [Overview](#overview)
- [Phase 1: Initial Feature Specification](#phase-1-initial-feature-specification)
- [Phase 2: Planning & Design](#phase-2-planning--design)
- [Phase 3: Implementation Requests](#phase-3-implementation-requests)
- [Phase 4: Test Generation](#phase-4-test-generation)
- [Phase 5: Debugging & Refinement](#phase-5-debugging--refinement)
- [Phase 6: Documentation](#phase-6-documentation)
- [Phase 7: Decision Making](#phase-7-decision-making)
- [Anti-Patterns](#anti-patterns-what-to-avoid)
- [Summary](#summary-key-takeaways)

---

## Overview

This document captures effective prompting patterns extracted from real development sessions on the SparseTagging project. Each pattern includes:
- **The actual prompt** used (or close approximation)
- **What made it effective** (specificity, context, constraints)
- **The outcome** (what was generated)
- **When to use** this pattern

### Success Metrics from These Sessions

- **6 major commits** to CI/CD pipeline (all successful)
- **Zero failed implementations** (all code worked first try or after clarification)
- **1,200+ lines** of documentation generated
- **Multiple bugs fixed** with clear root cause analysis
- **Architectural decisions** made with documented rationale

---

## Phase 1: Initial Feature Specification

### Pattern 1.1: Contextual Review Request

**Actual Prompt:**
```
The build process works well. Now review the ci.yml. Consider how to improve
robustness and error messages if a token is missing, services are not available,
some step fails. We are looking at this pipeline as template for future projects
and want to make sure it is generalized and robust. Take a deep breath before
starting.
```

**What Made It Effective:**
1. ✅ **Established context** - "build process works well" (no fundamental issues)
2. ✅ **Specific focus areas** - robustness, error messages, generalization
3. ✅ **Multiple concerns** listed explicitly - tokens, services, failures
4. ✅ **Future intent** - "template for future projects" (design for reuse)
5. ✅ **Encouragement to think** - "take a deep breath" (signals complexity)

**Outcome:**
- AI entered plan mode automatically
- Launched exploration agent to analyze workflow
- Identified 6 critical issues independently
- Generated comprehensive improvement plan

**When to Use:**
- Starting major refactoring or enhancement work
- When you want thorough analysis before changes
- When multiple concerns need to be addressed holistically
- When AI should propose solutions, not just implement

**Template:**
```
[Context about current state]. Now [action verb] the [component].
Consider [concern 1], [concern 2], [concern 3]. We are looking at
[future intent]. [Encouragement to think carefully].
```

---

### Pattern 1.2: Constraint-Based Request

**Actual Prompt:**
```
1: Make sure we have a checkpoint to revert to if this process does not work
as intended, 2: Make timeouts 5mins for this project, 3: Consider not just
checking the Docker image run a test correctly or perhaps provide documentation
how to do this if this step is too long or requires too many resources. Ask
questions before proceeding.
```

**What Made It Effective:**
1. ✅ **Numbered constraints** - Clear prioritization and structure
2. ✅ **Specific values** - "5mins for timeouts" (not vague "short timeout")
3. ✅ **Options provided** - "run a test OR provide documentation"
4. ✅ **Explicit permission to clarify** - "Ask questions before proceeding"

**Outcome:**
- AI asked 3 clarification questions about:
  - Checkpoint strategy (git branch)
  - Docker testing depth
  - Health check inclusion
- Generated plan respecting all constraints
- Created revert strategy documentation

**When to Use:**
- When you have specific technical constraints
- When multiple trade-offs exist
- When AI should ask for clarification before proceeding
- When you want to guide implementation details

**Template:**
```
1: [Constraint with rationale], 2: [Specific technical requirement],
3: [Options or trade-offs]. Ask questions before proceeding.
```

---

### Pattern 1.3: Multi-Deliverable Request

**Actual Prompt:**
```
Create a new document that documents the build process including:
1: Diagram out the flow of configuration values for the build and how they
   flow into to the ci.yml;
2: Document The various setups for the different services -- such as GitHub
   token, SonarCloud token put into the GH project secret repo, CodeCov setup
   and connection to GH, local setup to enable access to git commands, etc.
   Capture all setup requirements for all external service dependencies;
3: Build a flow diagram to show the flow of operation from a local change to
   a commit/push to a PR & testing to a merge & testing & generation of artifacts.
Add any other information that helps understand the setup, flow, and processing
steps. Do not go into detail how these services work, just the setup (tokens,
authorization, accounts) and the flow. Ask questions to clarify.
```

**What Made It Effective:**
1. ✅ **Numbered deliverables** - Clear breakdown of requirements
2. ✅ **Specific examples** - "GitHub token, SonarCloud token"
3. ✅ **Scope boundaries** - "Do not go into detail how these services work"
4. ✅ **Permission to add value** - "Add any other information that helps"
5. ✅ **Invitation to clarify** - "Ask questions to clarify"

**Outcome:**
- AI asked 4 clarification questions:
  - Diagram format (Mermaid vs ASCII)
  - Document location
  - Scope (CI only vs contributor setup)
  - Detail level (high-level vs step-by-step)
- Generated 1,200+ lines of comprehensive documentation
- Included 3 Mermaid diagrams
- Covered all requirements plus troubleshooting

**When to Use:**
- Requesting documentation or comprehensive guides
- When multiple related artifacts needed
- When you want high-quality output with room for AI judgment
- When scope boundaries are important

**Template:**
```
Create [artifact type] that [purpose] including:
1: [Deliverable 1 with specifics];
2: [Deliverable 2 with examples];
3: [Deliverable 3 with details].
Add [permission for additional value]. Do not [scope exclusion].
Ask questions to clarify.
```

---

## Phase 2: Planning & Design

### Pattern 2.1: Preference Elicitation

**AI-Generated Questions (Pattern to Learn From):**
```
[Multiple choice questions with clear headers]

Question 1: "Which library should we use for date formatting?"
Header: "Library Choice"
Options:
- Option A: moment.js (Recommended) - Most popular, well-maintained
- Option B: date-fns - Smaller bundle size, tree-shakeable
- Option C: dayjs - Minimal API, easy migration from moment
```

**What Made It Effective:**
1. ✅ **Clear headers** - Easy to scan (e.g., "Library Choice")
2. ✅ **Concise options** - 2-4 choices, not overwhelming
3. ✅ **Descriptions** - Explains trade-offs for each option
4. ✅ **Recommendation marked** - When AI has preference
5. ✅ **"Other" implicit** - User can provide custom answer

**User Responses (Pattern to Learn From):**
```
[Selected from provided options]
- "Moderate generalization"
- "Selective retries"
- "Extract version from pyproject.toml"
```

**Outcome:**
- AI had clear direction for implementation
- No ambiguity or back-and-forth
- Plan aligned with user preferences
- Implementation proceeded smoothly

**When to Use:**
- At start of complex projects with multiple approaches
- When trade-offs exist between options
- When AI should propose solutions but user decides
- Before significant architectural decisions

**Template (For AI to Ask):**
```
Question: [Clear question with specifics]?
Header: [2-3 word label]
Options:
- [Option A]: [Label] (Recommended if applicable) - [Trade-off explanation]
- [Option B]: [Label] - [Trade-off explanation]
- [Option C]: [Label] - [Trade-off explanation]
```

---

### Pattern 2.2: Incremental Approval

**Actual Pattern:**
```
[AI presents plan]
User: "Use your recommendation."
[AI proceeds with implementation]
```

**What Made It Effective:**
1. ✅ **AI presented clear recommendation** - Not just options
2. ✅ **User gave explicit approval** - "Use your recommendation"
3. ✅ **No unnecessary questions** - AI didn't ask for micro-decisions
4. ✅ **Trust established** - User confident in AI judgment

**Outcome:**
- Smooth transition from planning to implementation
- No decision paralysis
- AI proceeded with confidence
- Work completed efficiently

**When to Use:**
- When AI has presented clear analysis with recommendation
- When trust established through prior good decisions
- When micro-managing would slow progress
- When AI expertise exceeds user knowledge in specific area

**Anti-Pattern to Avoid:**
- AI asking "Is this okay?" for every small decision
- User saying "I don't know, you decide" without context
- AI proceeding without any approval

---

## Phase 3: Implementation Requests

### Pattern 3.1: Sequential Constraint Application

**Actual Prompt:**
```
1: Make sure we have a checkpoint to revert to if this process does not work
   as intended
2: Make timeouts 5mins for this project
3: Consider not just checking the Docker image run a test correctly
```

**What Made It Effective:**
1. ✅ **Numbered sequence** - Clear order of importance
2. ✅ **One constraint per item** - Easy to parse
3. ✅ **Specific values** - "5mins" not "short"
4. ✅ **Context provided** - Why each constraint matters

**Outcome:**
- AI created git branch (checkpoint)
- AI set all job timeouts to exactly 5 minutes
- AI added Docker smoke tests with 3 test cases
- All constraints satisfied in order

**When to Use:**
- When multiple requirements must be met
- When order of importance matters
- When specific technical values needed
- When you want to prevent AI from forgetting requirements

**Template:**
```
1: [Primary constraint with rationale]
2: [Secondary constraint with specific value]
3: [Tertiary constraint with options]
```

---

### Pattern 3.2: Error-Driven Iteration

**Actual Prompts:**
```
Prompt 1: "There were errors in the Test Python process (with EXIT_CODE=$?:
          ... The term 'EXIT_CODE=$?' is not recognized as a name of a cmdlet...)"

Prompt 2: "The updated README.md has an error in the counting of the Vulnerability
          where the results are all zeros but inspection of the Trivy-report and
          the Trivy-results show there are LOWs and MEDIUM issues."

Prompt 3: "Submitted the PR and the latest run showed an error in the Test Docker
          image as follows: ... ValidationError: fill_percent must be between 0 and 1"
```

**What Made It Effective:**
1. ✅ **Specific error messages** - Exact text from logs
2. ✅ **Context provided** - Where error occurred (Test Python process)
3. ✅ **Evidence of investigation** - "inspection of Trivy-report shows..."
4. ✅ **Timing noted** - "Submitted the PR and latest run..."

**Outcome:**
- Error 1: AI identified PowerShell vs Bash issue, added `shell: bash`
- Error 2: AI found wrong SARIF path, corrected jq query
- Error 3: AI identified parameter scale issue (5.0 vs 0.05)
- All fixes worked on first try

**When to Use:**
- When CI/tests fail with specific errors
- When behavior doesn't match expectations
- When you've investigated and found evidence
- When you want quick, targeted fixes

**Template:**
```
[Action that triggered error] showed an error [location]:
[exact error message].
[Optional: Evidence of investigation].
```

---

### Pattern 3.3: Commit Control Requests

**Actual Prompts:**
```
Prompt 1: "Can we do a commit without triggering a full scan/build as this
          is just documentation?"

Prompt 2: "Can I do a PR for this docs update without triggering a CI scan/build?"

Prompt 3: "Let's just do a normal PR. Do that now."
```

**What Made It Effective:**
1. ✅ **Clear intent** - "without triggering full scan"
2. ✅ **Rationale provided** - "this is just documentation"
3. ✅ **Decision clarity** - "Let's just do a normal PR"
4. ✅ **Action directive** - "Do that now"

**Outcome:**
- AI amended commit with `[skip ci]` tag
- AI explained `[skip ci]` doesn't work for PRs
- AI presented options with recommendation
- User chose option, AI executed immediately

**When to Use:**
- When you want to control git/CI behavior
- When standard workflow might not fit
- When you're concerned about resource usage
- When you want AI to explain options

**Template:**
```
Can we [alternative approach] as [rationale]?
[Or] Let's [clear decision]. Do that now.
```

---

## Phase 4: Test Generation

### Pattern 4.1: Test-Driven Development Request

**Implied Pattern (from conversation analysis):**
```
[User provided test requirements in CLAUDE.md]
- 173 comprehensive tests with ≥85% coverage
- Test suite structure defined
- Coverage requirements specified
```

**What Made It Effective:**
1. ✅ **Coverage target specified** - "≥85% coverage"
2. ✅ **Test organization defined** - 9 test files by category
3. ✅ **Quality gates set** - Must pass before merging
4. ✅ **Examples provided** - Critical bugs validation

**Outcome:**
- Comprehensive test suite created
- All tests passed
- Coverage requirements met
- Test structure followed conventions

**When to Use:**
- Starting new features or modules
- When refactoring existing code
- When test coverage is low
- When you want AI to think about edge cases

**Template:**
```
Write tests for [component] that:
- Cover [percentage]% of code paths
- Test edge cases: [specific scenarios]
- Follow structure: [organization pattern]
- Include: [specific test types]
```

---

### Pattern 4.2: Bug Validation Test Request

**Implied Pattern (from CLAUDE.md):**
```
test_critical_bugs.py - Critical bug fixes validation
- NOT operator semantics (v2.1.1 fix)
- Query result edge cases
- Data integrity scenarios
```

**What Made It Effective:**
1. ✅ **Regression focus** - Validates specific bug fixes
2. ✅ **Version references** - Links to when bugs were fixed
3. ✅ **Clear test goals** - Ensure bugs don't return
4. ✅ **Edge case emphasis** - Not just happy path

**Outcome:**
- Bug fixes remain validated
- Regression prevention built-in
- Documentation of historical issues
- Confidence in refactoring

**When to Use:**
- After fixing critical bugs
- When refactoring areas with past issues
- When building regression test suite
- When documenting bug history

**Template:**
```
Write regression tests for [bug ID/description]:
- Original failure scenario: [what broke]
- Expected behavior: [what should happen]
- Edge cases: [related scenarios]
- Version fixed: [reference]
```

---

## Phase 5: Debugging & Refinement

### Pattern 5.1: Specific Error Report

**Actual Prompt:**
```
The updated C:\Users\cgbraun\CC\SparseTagging\ScanResults\2026-01-07_20-48-23\README.md
has an error in the counting of the Vulnerability where the results are all zeros
but inspection of the Trivy-report and the Trivy-results show there are LOWs and
MEDIUM issues. analyze this and fix the issue. This is important to my career to
get this right.
```

**What Made It Effective:**
1. ✅ **Exact file path** - No ambiguity about what file
2. ✅ **Specific problem** - "vulnerability counting shows zeros"
3. ✅ **Evidence provided** - "inspection of Trivy-report shows..."
4. ✅ **Expectation stated** - Should show LOWs and MEDIUMs
5. ✅ **Importance conveyed** - "important to my career"
6. ✅ **Clear directive** - "analyze this and fix the issue"

**Outcome:**
- AI analyzed SARIF structure
- AI identified wrong jq path (`.runs[].results[]` vs `.runs[].tool.driver.rules[]`)
- AI provided detailed explanation of fix
- AI noted this was CRITICAL for accuracy
- Fix worked perfectly

**When to Use:**
- When you've found a specific bug
- When you've investigated and have evidence
- When the issue is important/blocking
- When you want root cause analysis, not just a patch

**Template:**
```
The [specific file/component] has an error in [specific behavior] where
[observed behavior] but [expected behavior]. [Evidence from investigation].
[Importance context]. Analyze this and fix the issue.
```

---

### Pattern 5.2: Platform-Specific Issues

**Actual Prompt:**
```
There were errors in the Test Python process (with EXIT_CODE=$?:
... The term 'EXIT_CODE=$?' is not recognized as a name of a cmdlet...)
and Warnings that Health checks that GHCR and SonarScanning may not be available
```

**What Made It Effective:**
1. ✅ **Error context** - "Test Python process"
2. ✅ **Exact error** - PowerShell error message
3. ✅ **Platform implied** - Cmdlet error suggests Windows
4. ✅ **Multiple issues** - Separated clearly (errors AND warnings)

**Outcome:**
- AI identified PowerShell vs Bash incompatibility
- AI added `shell: bash` to force bash syntax on Windows
- AI also addressed health check false positives separately
- Both issues resolved in single commit

**When to Use:**
- When errors happen on specific OS/environment
- When cross-platform compatibility broken
- When CI passes locally but fails remotely
- When error messages reveal platform differences

**Template:**
```
There were errors in [process/step] (with [exact error message]).
[Additional context about environment/platform].
[Optional: Other related issues].
```

---

### Pattern 5.3: Follow-Up Question Pattern

**Actual Prompt:**
```
From the plan to generalize the ci.yml build file better, one step was left out.
Review that and make a recommendation to do that step or not.
```

**What Made It Effective:**
1. ✅ **Reference to prior work** - "From the plan to generalize..."
2. ✅ **Specific gap noted** - "one step was left out"
3. ✅ **Decision request** - "make a recommendation"
4. ✅ **Options open** - "do that step or not" (not assuming must do)

**Outcome:**
- AI reviewed plan file (Phase 4: Retry Logic)
- AI analyzed pros and cons comprehensively
- AI made clear recommendation: DO NOT IMPLEMENT
- AI documented decision with criteria for reconsideration
- User accepted recommendation: "1" (option 1)

**When to Use:**
- When reviewing completed work
- When you notice something missing
- When you want analysis, not assumption of action
- When AI should evaluate trade-offs

**Template:**
```
From [previous work], [specific item] was [omitted/different].
Review that and make a recommendation to [action options].
```

---

## Phase 6: Documentation

### Pattern 6.1: Comprehensive Documentation Request

**Actual Prompt:**
```
Create a new document that documents the build process including:
1: Diagram out the flow of configuration values...
2: Document the various setups for the different services...
3: Build a flow diagram to show the flow of operation...
Add any other information that helps understand the setup, flow, and
processing steps. Do not go into detail how these services work, just
the setup (tokens, authorization, accounts) and the flow. Ask questions
to clarify.
```

**What Made It Effective:**
1. ✅ **Multiple sections** - Numbered list of deliverables
2. ✅ **Visual requirements** - "Diagram out", "Build a flow diagram"
3. ✅ **Scope definition** - "Do not go into detail how services work"
4. ✅ **Examples provided** - "tokens, authorization, accounts"
5. ✅ **Freedom to add value** - "Add any other information that helps"
6. ✅ **Invitation to clarify** - "Ask questions to clarify"

**Outcome:**
- AI asked 4 clarification questions (format, location, scope, detail)
- AI generated 1,200+ line comprehensive guide
- AI included 3 Mermaid diagrams
- AI added troubleshooting section proactively
- AI created reference tables for quick lookup

**When to Use:**
- When creating substantial documentation
- When multiple types of content needed (diagrams, text, examples)
- When you want AI to exercise judgment
- When scope boundaries matter

**Template:**
```
Create [doc type] that [purpose] including:
1: [Deliverable 1 with visual/format requirements]
2: [Deliverable 2 with specific examples]
3: [Deliverable 3 with scope details]
Add [permission for additional value].
Do not [scope exclusion].
Ask questions to clarify.
```

---

### Pattern 6.2: Reference Documentation Request

**Implied Pattern (from generated doc):**
```
Section 8: Reference Tables
- All secrets/tokens with purposes
- All environment variables
- Configuration files and their locations
- GitHub Action versions (pinned SHAs)
```

**What Made It Effective:**
1. ✅ **Tabular format** - Easy to scan
2. ✅ **Consistent structure** - Name, purpose, source, scope
3. ✅ **Quick lookup focus** - Not explanatory
4. ✅ **Complete coverage** - Every token, every variable

**Outcome:**
- Quick reference for developers
- Copy-paste friendly
- No need to search through prose
- Links to sources included

**When to Use:**
- Creating developer reference guides
- Documenting configuration options
- Building API documentation
- Creating troubleshooting checklists

**Template:**
```
Create reference documentation for [system/component] including:
- [Category 1]: [Structure/format requirement]
- [Category 2]: [What to include]
- [Category 3]: [Level of detail]
Format: [tables/lists/structure preference]
```

---

### Pattern 6.3: Process Documentation Request

**Actual Pattern (from workflow documentation):**
```
Development Workflow Stages
1. Local Development - [What developers do]
2. Push & Create PR - [GitHub interactions]
3. PR CI Pipeline - [What CI runs]
4. Code Review & Approval - [Review process]
5. Main Branch CI - [Full pipeline]
6. Outputs & Artifacts - [What gets generated]
```

**What Made It Effective:**
1. ✅ **Step-by-step flow** - Chronological order
2. ✅ **Actor-based** - Who does what
3. ✅ **Tool-specific** - Exact commands/actions
4. ✅ **Outcome-focused** - What results from each step

**Outcome:**
- Clear onboarding for new contributors
- Reduces confusion about workflow
- Provides copy-paste commands
- Shows conditional logic (PR vs main)

**When to Use:**
- Documenting workflows or processes
- Creating onboarding guides
- Explaining multi-step procedures
- Building runbooks

**Template:**
```
Document the [process name] including:
1. [Stage 1]: [Actor actions and tools]
2. [Stage 2]: [Actor actions and tools]
...
For each stage include:
- Who performs the action
- What tools/commands are used
- What the outcome is
- What happens next
```

---

## Phase 7: Decision Making

### Pattern 7.1: Trade-Off Analysis Request

**Actual Prompt:**
```
From the plan to generalize the ci.yml build file better, one step was left out.
Review that and make a recommendation to do that step or not.
```

**AI's Response Structure (Pattern to Learn):**
```
## Analysis: Should Retry Logic Be Implemented?

### Pros of Implementing ✅
1. [Benefit with explanation]
2. [Benefit with explanation]
...

### Cons of Implementing ❌
1. [Drawback with explanation]
2. [Drawback with explanation]
...

## Recommendation: DO NOT IMPLEMENT ❌

### Rationale:
1. [Reason]
2. [Reason]
...

### When to Reconsider:
- [Trigger condition 1]
- [Trigger condition 2]
...
```

**What Made It Effective:**
1. ✅ **Balanced analysis** - Both pros and cons
2. ✅ **Clear recommendation** - Not ambiguous
3. ✅ **Rationale explained** - Why this decision
4. ✅ **Reconsideration criteria** - When to revisit
5. ✅ **Data-driven** - "3+ failures per month"

**Outcome:**
- User understood trade-offs completely
- User agreed with recommendation: "1" (option 1: accept)
- Decision documented in CLAUDE.md
- Future developers can understand reasoning

**When to Use:**
- Making architectural decisions
- Choosing between competing approaches
- Deciding whether to implement optional features
- When trade-offs are complex

**Template:**
```
[Context about decision needed] - should we [action]?

Provide:
- Pros and cons of each option
- Your recommendation with rationale
- Criteria for reconsidering
- Data/metrics to inform decision
```

---

### Pattern 7.2: Confirmation Before Major Action

**Actual Pattern:**
```
User: "Can I do a PR for this docs update without triggering a CI scan/build?"

AI: [Explains options]
Option 1: Let CI Run Once (Recommended)
Option 2: Add Path Filters
Option 3: Direct Merge (Not Recommended)

My Recommendation: Go with Option 1...

User: "Let's just do a normal PR. Do that now."
```

**What Made It Effective:**
1. ✅ **AI presented options** - Not just "yes/no"
2. ✅ **AI explained trade-offs** - Pros/cons of each
3. ✅ **AI made recommendation** - Clear preference
4. ✅ **User made final call** - Explicit decision
5. ✅ **Clear action directive** - "Do that now"

**Outcome:**
- No ambiguity about what to do
- User informed about alternatives
- AI proceeded with confidence
- Action taken immediately

**When to Use:**
- Before potentially destructive actions (force push, delete)
- When multiple valid approaches exist
- When user might not know all options
- When you want AI expertise but user decision

**Template:**
```
[Question about major action]

AI should respond with:
- Option 1: [Approach] (Recommended if applicable)
  - Pros: ...
  - Cons: ...
- Option 2: [Approach]
  - Pros: ...
  - Cons: ...

My recommendation: [Clear preference with rationale]

User responds with clear choice.
```

---

### Pattern 7.3: Risk Assessment Request

**Implied Pattern (from plan documentation):**
```
## Risk Assessment

### Low Risk
- [Change type] - [Rationale]

### Medium Risk
- [Change type] - [Rationale and mitigation]

### High Risk
None - [Explanation]
```

**What Made It Effective:**
1. ✅ **Risk categories** - Low, Medium, High
2. ✅ **Specific to changes** - Not generic
3. ✅ **Mitigation strategies** - How to reduce risk
4. ✅ **Honest assessment** - "None" when true

**Outcome:**
- User understood potential issues
- Mitigation strategies in place
- Confidence to proceed
- Documentation for future reference

**When to Use:**
- Before major refactoring
- When planning breaking changes
- When deploying to production
- When making architectural decisions

**Template:**
```
Assess the risks of [proposed changes]:
- Categorize by severity (low/medium/high)
- Explain what could go wrong
- Provide mitigation strategies
- Note if any risks are acceptable
```

---

## Anti-Patterns (What to Avoid)

### Anti-Pattern 1: Vague Feature Requests

**Bad Example:**
```
Make the CI better.
```

**Why It's Bad:**
- No specifics about what "better" means
- No context about current issues
- AI must guess what you want
- Likely to miss key requirements

**Good Alternative:**
```
Review the CI workflow and improve error handling for:
1. Missing authentication tokens
2. External service unavailability
3. Failed deployment steps
Focus on robustness and clear error messages.
```

---

### Anti-Pattern 2: Implementation Details Too Early

**Bad Example:**
```
Add retry logic using nick-invision/retry@v3 to all pip install steps
with max_attempts: 3 and retry_wait_seconds: 30.
```

**Why It's Bad:**
- Jumps to solution without analyzing problem
- Might not be the right approach
- Misses opportunity for AI to suggest better solutions
- No discussion of trade-offs

**Good Alternative:**
```
The CI occasionally fails due to transient network issues with pip installs.
What approaches would you recommend to improve resilience? Consider:
- Retry logic
- Caching strategies
- Health checks
- Trade-offs for each approach
```

---

### Anti-Pattern 3: No Context Provided

**Bad Example:**
```
There's an error on line 690.
```

**Why It's Bad:**
- No file path
- No error message
- No context about what you were doing
- AI must search and guess

**Good Alternative:**
```
The CI workflow file .github/workflows/ci.yml has a YAML syntax error
on line 690: "You have an error in your yaml syntax on line 690".
This occurred after adding the Docker smoke test section. The error
appeared when creating a PR.
```

---

### Anti-Pattern 4: Asking AI to Decide Everything

**Bad Example:**
```
Should I use retry logic or not? You decide.
```

**Why It's Bad:**
- AI doesn't know your priorities
- AI doesn't know your constraints
- AI doesn't know your risk tolerance
- Decision lacks user context

**Good Alternative:**
```
Should I use retry logic or not? Context:
- Our CI is currently stable (no network failures)
- We want this as a template for other projects
- We're concerned about supply chain security
- What's your recommendation and why?
```

---

### Anti-Pattern 5: Ignoring AI Questions

**Bad Example:**
```
AI: "Do you want me to [clarifying question]?"
User: "Just do it."
```

**Why It's Bad:**
- AI still doesn't know the answer
- Likely to implement wrong approach
- Will require rework later
- Wastes time

**Good Alternative:**
```
AI: "Do you want retry logic on all pip installs or just GHCR push?"
User: "GHCR push only - pip installs have caching already."
```

---

### Anti-Pattern 6: Too Many Changes At Once

**Bad Example:**
```
Fix the exit codes, add retry logic, update documentation, refactor
the test matrix, add health checks, implement caching, and improve
error messages all in one commit.
```

**Why It's Bad:**
- Hard to review
- Hard to debug if something breaks
- Unclear which change caused issues
- Difficult to revert partially

**Good Alternative:**
```
Phase 1: Fix exit code capture and token validation (core bugs)
Phase 2: Add health checks and validation
Phase 3: Update documentation
[Separate commits for each phase]
```

---

### Anti-Pattern 7: Assuming AI Remembers Everything

**Bad Example:**
```
Now do that thing we talked about before.
```

**Why It's Bad:**
- AI may not remember which "thing"
- Conversation may have covered multiple topics
- Ambiguous reference
- Forces AI to guess

**Good Alternative:**
```
Earlier you recommended adding Docker smoke tests (Test 1: import,
Test 2: version, Test 3: functionality). Let's implement those now.
```

---

## Summary: Key Takeaways

### What Makes Prompts Effective

1. **Context is King**
   - State current situation before requesting changes
   - Explain why changes are needed
   - Provide relevant history or prior decisions

2. **Specificity Matters**
   - Use exact values ("5 minutes" not "short timeout")
   - Provide file paths, line numbers, error messages
   - List specific requirements, not vague goals

3. **Structure Helps**
   - Number items in priority order
   - Use consistent formatting
   - Break complex requests into phases

4. **Invite Clarification**
   - "Ask questions before proceeding"
   - "Let me know if anything is unclear"
   - Shows you want collaboration, not just execution

5. **Balance Control**
   - Provide constraints but allow AI judgment
   - Make key decisions but trust AI for details
   - Specify must-haves vs nice-to-haves

6. **Provide Evidence**
   - Share error messages verbatim
   - Include relevant file contents
   - Explain what you've already tried

7. **Set Scope Boundaries**
   - "Do not include X"
   - "Focus on Y, not Z"
   - "Consider A, B, C but not D"

### When to Use Each Pattern

| Pattern | Use When | Example Scenario |
|---------|----------|------------------|
| Contextual Review | Starting major work | "Review the CI for robustness..." |
| Constraint-Based | Specific requirements | "Timeout must be 5 minutes..." |
| Multi-Deliverable | Documentation/guides | "Create doc with diagrams..." |
| Error-Driven | Debugging specific issues | "Error on line 690: ..." |
| Trade-Off Analysis | Making decisions | "Should we add retry logic?" |
| Sequential Constraints | Multiple requirements | "1: checkpoint, 2: timeout, 3: test" |
| Specific Error Report | CI/test failures | "Vulnerability count shows zero..." |

### Red Flags in Your Own Prompts

🚩 **You wrote:** "Make it better"
✅ **Instead write:** "Improve error handling for [specific scenarios]"

🚩 **You wrote:** "There's an error"
✅ **Instead write:** "Error in [file] on line [N]: [exact message]"

🚩 **You wrote:** "You decide"
✅ **Instead write:** "Recommend an approach given [context]"

🚩 **You wrote:** "Do everything at once"
✅ **Instead write:** "Let's tackle this in phases: 1..., 2..., 3..."

🚩 **You wrote:** Single sentence request
✅ **Instead write:** Context + specifics + rationale + invitation to clarify

### The Golden Template

```
[CONTEXT: Current state and why change is needed]

[REQUEST: Specific action with numbered deliverables if multiple]
1. [Deliverable 1 with specific examples/values]
2. [Deliverable 2 with constraints or options]
3. [Deliverable 3 with scope boundaries]

[GUIDANCE: Any must-haves, nice-to-haves, or exclusions]
- Must have: [requirement]
- Do not include: [scope boundary]
- Consider: [options or trade-offs]

[COLLABORATION: Invitation to clarify]
Ask questions before proceeding.
```

### Success Metrics

In our sessions, these patterns led to:
- ✅ **Zero failed implementations** requiring complete rewrites
- ✅ **Clear architectural decisions** with documented rationale
- ✅ **Efficient debugging** (most bugs fixed first try)
- ✅ **High-quality documentation** exceeding requirements
- ✅ **Smooth collaboration** with minimal back-and-forth

### Final Advice

1. **Start Specific, Stay Specific**
   - Vague prompts lead to vague results
   - Specific prompts lead to specific results

2. **Context Over Commands**
   - Explain the "why" not just the "what"
   - AI can suggest better solutions with context

3. **Iterate Intentionally**
   - Small, focused changes are easier to review and debug
   - Each change should have clear purpose

4. **Trust but Verify**
   - AI recommendations are valuable but review them
   - Make final decisions on architecture and trade-offs

5. **Document Decisions**
   - Capture the "why" behind choices
   - Future you will thank present you

---

**Document Version:** 1.0
**Last Updated:** 2026-01-08
**Source Project:** SparseTagging
**AI Assistant:** Claude Code (Sonnet 4.5)

---

*This document is a living artifact. As you discover new effective patterns, add them here for future reference.*
