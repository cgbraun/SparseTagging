# Claude Code Comprehensive Cheat Sheet
**MRSL Engineering Reference | v1.0 | January 2026**

**Quick Links:**
- [Official Docs](https://docs.anthropic.com/en/docs/claude-code/overview)
- [GitHub](https://github.com/anthropics/claude-code)
- [Anthropic Skills Repo](https://github.com/anthropics/skills)
- [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code)

---

## Table of Contents
1. [Key Files & Configuration](#key-files--configuration)
2. [Core Slash Commands](#core-slash-commands)
3. [Built-in Skills](#built-in-skills)
4. [Session Management](#session-management)
5. [Context & Memory](#context--memory)
6. [File & Directory References](#file--directory-references)
7. [Plan Mode](#plan-mode)
8. [Permissions & Security](#permissions--security)
9. [Subagents](#subagents)
10. [MCP Integration](#mcp-integration)
11. [Hooks System](#hooks-system)
12. [Custom Commands & Skills](#custom-commands--skills)
13. [Git Workflows](#git-workflows)
14. [Advanced Prompting](#advanced-prompting)
15. [Parallel Sessions](#parallel-sessions)
16. [Performance & Cost](#performance--cost)
17. [Windows Configuration](#windows-configuration)
18. [Keyboard Shortcuts](#keyboard-shortcuts)
19. [Troubleshooting](#troubleshooting)
20. [Power User Techniques](#power-user-techniques)
21. [Anti-Patterns](#anti-patterns)

---

## Key Files & Configuration

### File Hierarchy & Locations

| File/Directory | Location | Purpose | Scope |
|----------------|----------|---------|-------|
| `CLAUDE.md` | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Project memory, conventions, architecture | Project-wide |
| `CLAUDE.md` | `~/.claude/CLAUDE.md` | Global user preferences | User-wide |
| `CLAUDE_ENTERPRISE.md` | Enterprise managed | IT-managed conventions | Enterprise |
| `settings.json` | `./.claude/settings.json` | Project config (shared via git) | Project team |
| `settings.local.json` | `./.claude/settings.local.json` | Personal overrides (gitignored) | Individual |
| `settings.json` | `~/.claude/settings.json` | Global user settings | User-wide |
| Commands | `./.claude/commands/` | Project slash commands | Project team |
| Commands | `~/.claude/commands/` | Personal slash commands | User-wide |
| Skills | `./.claude/skills/` | Project skills | Project team |
| Skills | `~/.claude/skills/` | Personal skills | User-wide |
| Agents | `./.claude/agents/` | Project subagents | Project team |
| Agents | `~/.claude/agents/` | Personal subagents | User-wide |
| Plans | `~/.claude/plans/` (default) | Plan mode files | User (not project-specific) |
| Plans | On Windows | `%USERPROFILE%\.claude\plans\` | User |
| `.mcp.json` | `./.mcp.json` | MCP server config | Project team |

**Hierarchy:** Project local > Project > User > Default
**Security:** Store API keys in environment variables, deny CC access to `.env` files

---

## Core Slash Commands

### Essential Commands

| Command | Purpose | When/Why | Example |
|---------|---------|----------|---------|
| `/help` | Show available commands | When stuck, discovering features | `/help` shows all commands including custom |
| `/init` | Create CLAUDE.md | **Always use at start of new project** | `/init` analyzes codebase, creates project context |
| `/clear` | Clear conversation | Context too cluttered, fresh start needed | `/clear` wipes history, keeps session |
| `/compact` | Compress context | Context filling up, preserve essence | `/compact focus on auth logic` |
| `/context` | Visualize context usage | Check token usage, see what's loaded | `/context` shows colored grid of usage |
| `/memory` | Edit CLAUDE.md | Add project conventions, update context | `/memory` opens editor for persistent memory |
| `/status` | Version & connectivity | Troubleshoot connection issues | `/status` shows model, version, connection |
| `/exit` | Exit session | End work session | `/exit` or `Ctrl+D` |

### Configuration Commands

| Command | Purpose | When/Why | Example |
|---------|---------|----------|---------|
| `/config` | Open settings UI | Change model, permissions, features | `/config` opens full settings interface |
| `/model` | Switch Claude model | Quick model change (Sonnet/Opus/Haiku) | `/model opus` for complex tasks |
| `/permissions` | Manage tool permissions | Set allow/ask/deny rules | `/permissions` opens permission editor |
| `/output-style` | Configure response format | Minimal vs detailed output | `/output-style minimal` |
| `/privacy-settings` | Control data sharing | Adjust telemetry, data storage | `/privacy-settings` |

### Development Commands

| Command | Purpose | When/Why | Example |
|---------|---------|----------|---------|
| `/review` | Request code review | Before commits, quality checks | `/review` analyzes current changes |
| `/todos` | List tracked TODOs | Check action items from conversation | `/todos` shows all tracked tasks |
| `/doctor` | Health check CC install | Troubleshoot installation issues | `/doctor` diagnoses problems |
| `/add-dir` | Add working directories | Monorepos, multi-project work | `/add-dir ../services` |
| `/bug` | Report issues | File bugs with context | `/bug` auto-includes diagnostic info |

### Session Analytics

| Command | Purpose | When/Why | Example |
|---------|---------|----------|---------|
| `/usage` | Show usage limits | Track plan limits, rate limits | `/usage` displays current usage |
| `/cost` | Token usage & cost | Monitor spending in session | `/cost` shows tokens and dollars |
| `/export` | Export conversation | Save for documentation, sharing | `/export report.md` |
| `/rewind` | Time travel code/chat | Undo changes, return to checkpoint | `/rewind` or `Esc+Esc` |

### Agent & Tool Commands

| Command | Purpose | When/Why | Example |
|---------|---------|----------|---------|
| `/agents` | Manage subagents | Create/configure specialized agents | `/agents` shows available subagents |
| `/bashes` | List background tasks | Check long-running commands | `/bashes` shows active background jobs |
| `/skills` | List available skills | Discover what skills exist | `/skills` (if command exists) |
| `/plugin` | Manage plugins | Install marketplace plugins | `/plugin install <name>` |
| `/hooks` | Configure hooks | Automate workflows at trigger points | `/hooks` opens hooks configuration |
| `/mcp` | MCP authentication | Authenticate MCP servers | `/mcp` handles auth for MCP |

---

## Built-in Skills

### Anthropic Official Skills

| Skill ID | Purpose | When to Use | Invocation |
|----------|---------|-------------|------------|
| `docx` | Create/edit Word documents | Professional docs, reports, proposals | "Create a business proposal in Word" |
| `pdf` | Generate/analyze PDFs | PDF creation, form filling, extraction | "Extract form fields from PDF" |
| `pptx` | Create/edit presentations | Slide decks, presentations | "Create a 5-slide pitch deck" |
| `xlsx` | Create/edit spreadsheets | Financial models, data analysis | "Create budget spreadsheet" |
| `algorithmic-art` | Generate art with p5.js | Generative art, visualizations | "Create flow field art" |
| `canvas-design` | Design PNG/PDF visuals | Visual design, graphics | "Design a logo concept" |
| `frontend-design` | UI/UX development | Web components, interfaces | "Design responsive navbar" |
| `doc-coauthoring` | Collaborative editing | Team document work | "Track changes in document" |
| `slack-gif-creator` | Animated GIFs for Slack | Team communication visuals | "Create reaction GIF" |
| `theme-factory` | Style artifacts | Themed output, branding | "Apply dark theme" |
| `web-artifacts-builder` | Build React artifacts | Complex web artifacts | "Build data dashboard" |

**Discovery:** Use natural language - CC auto-selects appropriate skill
**Custom Skills:** Create in `.claude/skills/<skill-name>/SKILL.md`
**Marketplace:** Install via `/plugin` command
**Reference:** https://github.com/anthropics/skills

---

## Session Management

### CLI Session Commands

| Command/Flag | Purpose | When/Why | Example |
|--------------|---------|----------|---------|
| `claude` | Start interactive REPL | Begin coding session | `claude` in project directory |
| `claude "query"` | REPL with initial prompt | Start with specific question | `claude "explain this project"` |
| `claude -p "query"` | Print mode (one-shot) | Scripting, automation, CI/CD | `claude -p "fix lint errors"` |
| `claude -c` | Continue last conversation | Resume recent work | `claude -c` or `claude --continue` |
| `claude -r <session-id>` | Resume specific session | Return to particular work | `claude -r` shows picker |
| `claude --resume` | Resume with picker | Select from recent sessions | `claude --resume` |
| `claude update` | Update to latest version | Get new features, fixes | `claude update` |
| `claude --dangerous-skip-permissions` | YOLO mode | Skip all permission prompts (⚠️ use carefully) | Use only in sandboxed environments |

### Session Modifiers

| Flag | Purpose | When/Why | Example |
|------|---------|----------|---------|
| `--model <model>` | Specify model | Use specific Claude version | `--model opus` for reasoning |
| `--add-dir <path>` | Add working directories | Multiple project directories | `--add-dir ./services --add-dir ./shared` |
| `--allowedTools <tools>` | Pre-approve tools | Skip permission prompts | `--allowedTools "Read,Write,WebSearch"` |
| `--disallowedTools <tools>` | Block tools | Security restrictions | `--disallowedTools "Bash(rm*)"` |
| `--system-prompt <text>` | Replace system prompt | Custom behavior | `--system-prompt "You are security auditor"` |
| `--append-system-prompt <text>` | Append to system prompt | Add instructions | `--append-system-prompt "Always write tests"` |
| `--max-turns <n>` | Limit agentic loops | Prevent runaway execution | `--max-turns 10` |
| `--output-format json` | JSON output | Scripting integration | `--output-format json` for parsing |
| `--json-schema <schema>` | Structured output | Enforce response format | `--json-schema '{"type":"object"...}'` |
| `--mcp-debug` | Debug MCP issues | Troubleshoot MCP servers | `--mcp-debug` shows connection details |

---

## Context & Memory

### Context Management Commands

| Command | Purpose | When/Why | Example |
|---------|---------|----------|---------|
| `/context` | Visualize usage | Check context window fullness | `/context` shows colored grid |
| `/compact [instructions]` | Compress history | Save tokens, preserve key info | `/compact focus on database logic` |
| `/clear` | Wipe conversation | Start fresh, reset context | `/clear` when context too noisy |
| `/memory` | Edit CLAUDE.md | Update persistent context | `/memory` opens memory file |
| `#<text>` | Quick memory add | Add to CLAUDE.md instantly | `#Use 2-space indentation` |

### CLAUDE.md Best Practices

**Structure:**
```markdown
# Project Context

## Code Style
- Language-specific conventions
- Formatting rules
- Naming patterns

## Architecture
- System design overview
- Key components
- Data flow

## Testing
- Test frameworks
- Coverage requirements
- Testing patterns

## Git Workflow
- Branch strategy
- Commit conventions
- PR requirements
```

**Tips:**
- Be specific: "Use 2-space indent" not "Good formatting"
- Include examples: "Test files: `*.test.ts`"
- Update as project evolves
- Keep under 500 lines, reference other files for details

---

## File & Directory References

### @ Symbol References

| Syntax | Purpose | When/Why | Example |
|--------|---------|----------|---------|
| `@<filename>` | Reference file | Include file in context | `@./src/auth.ts` review this |
| `@<directory>/` | Reference directory | Include entire directory | `@./src/components/` refactor |
| `@<glob>` | Glob pattern | Multiple files pattern | `@./src/**/*.test.ts` review tests |
| `@~/` | User home files | Reference home directory | `@~/.bashrc` |
| Tab completion | Auto-complete paths | Quick file selection | Type `@./` then Tab |

### Import in CLAUDE.md

| Syntax | Purpose | When/Why | Example |
|--------|---------|----------|---------|
| `@path/to/file.md` | Import file into CLAUDE.md | Modular memory files | `@./docs/conventions.md` |

---

## Plan Mode

### Entering Plan Mode

| Method | Purpose | When/Why | Example |
|--------|---------|----------|---------|
| `Shift+Tab+Tab` | Toggle plan mode | **Use before coding complex features** | Cycle: Normal → Auto → Plan |
| Natural request | Ask for plan | Let CC enter plan mode | "Plan the authentication system" |

### Plan Mode Workflow

| Step | Action | Purpose | Notes |
|------|--------|---------|-------|
| 1 | Enter plan mode | Read-only analysis | `Shift+Tab+Tab` to enter |
| 2 | CC asks questions | Clarify requirements | Answer via `AskUserQuestion` |
| 3 | CC creates plan | Writes to `~/.claude/plans/<session>.md` | Edit with `/plan open` |
| 4 | Review & edit plan | Refine approach | Changes sync to CC context |
| 5 | Exit & implement | `Shift+Tab+Tab` to normal | CC executes plan |

### Plan Files

| Aspect | Detail | Notes |
|--------|--------|-------|
| **Location (default)** | `~/.claude/plans/` | Windows: `%USERPROFILE%\.claude\plans\` |
| **Naming** | Auto-generated session-based | Not customizable currently |
| **Editing** | `/plan open` | Opens in default editor |
| **Clearing** | `/clear` | Creates fresh plan file |
| **Version Control** | Not automatic | Manually copy to project for tracking |

**Note:** Feature requests exist for project-local plans - check official docs for updates

---

## Permissions & Security

### Permission Levels

| Level | Meaning | Use Case |
|-------|---------|----------|
| `allow` | Pre-approved, no prompts | Trusted operations |
| `ask` | Prompt each time | Sensitive operations |
| `deny` | Blocked completely | Dangerous operations |

### Configuration Format

**In `.claude/settings.json`:**
```json
{
  "permissions": {
    "allow": [
      "Read",
      "Write(src/**)",
      "Bash(git *)",
      "Bash(npm *)",
      "WebSearch",
      "WebFetch(domain:github.com)"
    ],
    "ask": [
      "Write(*.config.*)",
      "Bash(git push*)"
    ],
    "deny": [
      "Read(.env*)",
      "Read(**/*.key)",
      "Write(package-lock.json)",
      "Bash(rm *)",
      "Bash(sudo *)"
    ]
  }
}
```

### Security Best Practices

| Practice | Implementation | Why |
|----------|----------------|-----|
| Deny .env access | `"deny": ["Read(.env*)"]` | Protect secrets |
| Store keys in env vars | `export ANTHROPIC_API_KEY=...` | Not in files |
| Limit write permissions | `"ask": ["Write(*.prod.*)"]` | Protect production |
| Block destructive commands | `"deny": ["Bash(rm *)"]` | Prevent accidents |
| Use glob patterns | `"deny": ["Read(**/*.key)"]` | Cover all cases |
| Review permissions | `/permissions` | Regular audits |

### MCP Permissions

| Permission Format | Purpose | Example |
|-------------------|---------|---------|
| `mcp__<server>` | Allow all tools from server | `mcp__github` |
| `mcp__<server>__<tool>` | Allow specific tool | `mcp__github__create_pr` |

---

## Subagents

### What Are Subagents?

| Aspect | Detail |
|--------|--------|
| **Purpose** | Specialized Claude instances with own context/persona |
| **Benefits** | Isolated context, domain expertise, token efficiency |
| **Location** | `.claude/agents/` (project) or `~/.claude/agents/` (user) |

### Creating Subagents

**File:** `.claude/agents/code-reviewer.md`

```markdown
---
name: code-reviewer
description: Security and performance code review expert
model: sonnet
color: orange
tools:
  - Read
  - Grep
  - Glob
---

# Code Reviewer Agent

You are a senior code reviewer focusing on:
- Security vulnerabilities
- Performance issues
- Code maintainability
- Best practices

## Review Checklist
1. Authentication/authorization
2. Input validation
3. Error handling
4. Performance patterns
5. Test coverage
```

### Invoking Subagents

| Method | Example | When |
|--------|---------|------|
| Natural language | "Use code-reviewer to analyze this" | Let CC choose |
| Direct invocation | `/agents` then select | Manual control |
| Auto-invocation | CC selects based on description | Task matches expertise |

---

## MCP Integration

### Adding MCP Servers

| Command | Purpose | Example |
|---------|---------|---------|
| `claude mcp add` | Add MCP server | `claude mcp add --transport http api https://api.example.com --header "Authorization: Bearer token"` |
| `claude mcp add` (stdio) | Add local MCP server | `claude mcp add --transport stdio github npx -y @modelcontextprotocol/server-github` |
| `claude mcp list` | List servers | `claude mcp list` |
| `claude mcp get <n>` | Get server details | `claude mcp get 1` |
| `claude mcp remove <n>` | Remove server | `claude mcp remove 1` |
| `/mcp` | Authenticate in session | `/mcp` for OAuth flows |

### Common MCP Servers (MRSL Stack)

| Server | Purpose | Setup |
|--------|---------|-------|
| **GitHub** | PR reviews, issues, commits | `npx -y @modelcontextprotocol/server-github` |
| **Jira** | Ticket management | MCP Jira server |
| **Confluence** | Documentation access | MCP Confluence server |
| **SonarQube** | Code quality metrics | Custom MCP integration |
| **Google Drive** | Access design docs | MCP Google Drive server |

### Using MCP Resources

| Syntax | Purpose | Example |
|--------|---------|---------|
| `@<server>:<resource>` | Reference MCP resource | `@github:issue://123` |
| `/mcp__<server>__<prompt>` | Execute MCP prompt | `/mcp__github__list_prs` |

---

## Hooks System

### Available Hooks

| Hook | Trigger | Use Case | Example |
|------|---------|----------|---------|
| `SessionStart` | Session begins | Setup scripts, load context | Run environment check |
| `SessionEnd` | Session ends | Cleanup, export logs | Save session report |
| `PreToolUse` | Before tool runs | Validate operations | Check file permissions |
| `PostToolUse` | After tool runs | Log actions, format code | Auto-format on write |
| `PermissionRequest` | Permission asked | Auto-approve patterns | Allow specific tools |
| `UserPromptSubmit` | Before processing | Pre-process input | Add context |
| `Stop` | After response | Post-process output | Format responses |

### Hook Configuration

**In `.claude/settings.json`:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write(*.py)",
        "hooks": [
          {
            "type": "command",
            "command": "python -m black \"$file\""
          }
        ]
      }
    ],
    "SessionStart": {
      "command": "echo 'Session started at $(date)'",
      "enabled": true
    }
  }
}
```

### Access Hooks Interface

| Command | Purpose |
|---------|---------|
| `/hooks` | Interactive hooks configuration |

---

## Custom Commands & Skills

### Custom Slash Commands

**Location:** `.claude/commands/<name>.md` (project) or `~/.claude/commands/<name>.md` (user)

**Format:**
```markdown
---
description: Review code for security issues
allowed-tools: Read, Grep, Glob
---

Review this code for:
- SQL injection vulnerabilities
- XSS attack vectors
- Authentication flaws
- Exposed credentials

Provide specific line numbers and fixes.
```

**With Arguments:**
```markdown
---
description: Fix GitHub issue with tests
---

Analyze and fix GitHub issue #$ARGUMENTS.
Include unit tests for the fix.
```

**Invocation:** `/security-review` or `/fix-issue 123`

### Custom Skills

**Location:** `.claude/skills/<skill-name>/SKILL.md`

**Structure:**
```
.claude/skills/db-migration/
├── SKILL.md
├── scripts/
│   └── validate.py
├── templates/
│   └── migration.sql
└── REFERENCE.md
```

**SKILL.md Format:**
```markdown
---
name: db-migration
description: Database schema migrations and SQL optimization
disable-model-invocation: true
user-invocable: true
---

# Database Migration Expert

You specialize in:
- Schema design
- Migration scripts
- SQL optimization
- Data integrity

## Workflow
1. Analyze schema changes
2. Generate migration script
3. Validate with @scripts/validate.py
4. Provide rollback plan
```

**Invocation:** `/db-migration` or mention naturally "help with database migration"

---

## Git Workflows

### Basic Git Commands in CC

| CC Capability | Purpose | Example |
|---------------|---------|---------|
| Direct git commands | Run any git command | `git status`, `git log`, `git diff` |
| `!git <cmd>` | Direct execution | `!git status` (bypasses CC) |
| Built-in git awareness | CC understands repo context | "Show uncommitted changes" |

### Git Workflow Commands

| Task | Command/Prompt | Notes |
|------|----------------|-------|
| **Status** | `git status` or "What files changed?" | CC reads git state |
| **Diff** | `git diff` or "Show my changes" | Review before commit |
| **Stage** | `git add <files>` or "Stage these changes" | Prepare commit |
| **Commit** | "Create commit with message" | CC writes descriptive messages |
| **PR Review** | `/review` or "Review for PR" | Code quality check |
| **Branch** | `git checkout -b feature-name` | New feature branch |
| **Merge** | `git merge` or "Merge feature branch" | Integration |

### Safety Practices

| Practice | Implementation | Why |
|----------|----------------|-----|
| **Commit before CC** | `git commit -am "WIP"` before asking CC | Revert point |
| **New branch per feature** | `git checkout -b feature-x` | Isolate changes |
| **Review before push** | `/review` before `git push` | Quality gate |
| **Commit after success** | `git commit -am "Working: feature"` immediately | Save progress |
| **Use worktrees** | `git worktree add ../project-feature-a -b feature-a` | Parallel work |

### GitHub PR Workflow

| Step | Action | Example |
|------|--------|---------|
| 1 | Create feature branch | `git checkout -b feature-auth` |
| 2 | Work with CC | Use plan mode, implement |
| 3 | Review changes | `/review` |
| 4 | Commit | CC: "Create commit message" |
| 5 | Push | `git push -u origin feature-auth` |
| 6 | Create PR | "Create GitHub PR with description" (if MCP connected) |

---

## Advanced Prompting

### Thinking Modes

| Mode | Tokens | When to Use | How to Invoke |
|------|--------|-------------|---------------|
| Normal | Default | Standard tasks | No special prompt |
| `think` | ~4,000 | Step-by-step reasoning | Add "think" to prompt |
| `think hard` / `megathink` | ~10,000 | Architectural decisions | Add "think hard" to prompt |
| `think harder` | Extended | Deep analysis | Add "think harder" to prompt |
| `ultrathink` | Max 31,999 | Complex system design | Add "ultrathink" to prompt |
| Extended thinking toggle | As set | Always use extended | Press `Tab` key |

**Note:** These are prompt keywords, not CLI flags. Include in your message.

### Prompting Best Practices

| Technique | Description | Example |
|-----------|-------------|---------|
| **Be specific** | Exact requirements | "Create React auth with JWT" not "login thing" |
| **Sequential steps** | Numbered instructions | "1. Analyze 2. Plan 3. Implement" |
| **Provide context** | Framework, language, constraints | "In Python using FastAPI..." |
| **Define output** | Specify format | "Only code, no explanations" |
| **Few-shot examples** | Show patterns | "Example 1:... Example 2:... Now create..." |
| **Role setting** | Set expertise level | "You're a senior security engineer" |

### What NOT to Prompt

| ❌ Avoid | ✅ Instead |
|---------|-----------|
| "fix the bug" | "Fix race condition in auth.js:42" |
| "make it better" | "Optimize SQL query with indexes" |
| "optimize this" | "Reduce API response time by caching" |
| "help me" | "Explain async/await in JavaScript" |

---

## Parallel Sessions

### Multiple Session Strategies

| Strategy | Purpose | How | Use Case |
|----------|---------|-----|----------|
| **Multiple terminals** | Different tasks | Open multiple `claude` sessions | Planning + Coding + Docs |
| **Git worktrees** | Code isolation | `git worktree add ../proj-feature-a -b feature-a` | Parallel features |
| **Subagents** | Specialized work | Spawn agents for different roles | Code + Review + Security |
| **Background tasks** | Long operations | `Ctrl+B` or background bash | Tests, builds |

### Git Worktree Workflow

| Command | Purpose | Example |
|---------|---------|---------|
| `git worktree add <path> -b <branch>` | Create worktree | `git worktree add ../proj-bugfix -b bug-123` |
| `cd <worktree>; claude` | Work in isolation | Each CC session separate codebase |
| `git worktree list` | List all worktrees | See active workspaces |
| `git worktree remove <path>` | Clean up | `git worktree remove ../proj-bugfix` |

**Anthropic Power User Pattern:**
- Terminal 1: Planning (plan mode)
- Terminal 2: Implementation (coding)
- Terminal 3: Testing (run tests)
- Terminal 4: Documentation (write docs)
- Terminal 5: Web search (research)

Reference: https://www.anthropic.com/engineering/claude-code-best-practices

---

## Performance & Cost

### Monitoring Tools

| Tool | Purpose | Command |
|------|---------|---------|
| `/usage` | Check limits | `/usage` in session |
| `/cost` | Session tokens/cost | `/cost` shows spending |
| `npx ccusage` | Overall usage stats | `npx ccusage@latest` |
| `/context` | Context window usage | `/context` shows fullness |

### Token Optimization

| Strategy | Impact | When |
|----------|--------|------|
| `/compact` regularly | 30-50% reduction | Context approaching full |
| Use subagents | Isolated contexts | Complex multi-task work |
| Clear between unrelated tasks | Reset context | New topic/feature |
| Use Haiku for simple tasks | 10x cost savings | Routine operations |
| Use Opus sparingly | Best results | Critical/complex work |
| Front-load context | Fewer round-trips | Give all info upfront |

### Model Selection

| Model | Best For | Cost | When to Use |
|-------|----------|------|-------------|
| **Haiku 4.5** | Simple tasks, fast responses | $ | Linting, simple refactors |
| **Sonnet 4.5** | Everyday coding | $$ | Standard development (default for Pro/Max5) |
| **Opus 4.5** | Complex reasoning, planning | $$$$ | Architecture, debugging (default for Max20) |

**Switch:** `/model <sonnet|opus|haiku>`

### Plan Tier Selection

| Tier | Tokens | Best For | Monthly Cost |
|------|--------|----------|--------------|
| **Pro** | Base | Medium workload, supplement to own coding | $20 |
| **Max5** | 5x Pro | Intense workload, frequent use | $100 |
| **Max20** | 20x Pro | Near-autonomous, multiple sessions, heavy Opus | $200 |
| **API** | Pay-as-go | Custom integrations, production | Variable |

---

## Windows Configuration

### Shell Options for Windows

| Shell | Recommendation | Notes |
|-------|----------------|-------|
| **Git Bash** | ✅ Recommended | Easiest setup, Unix compatibility |
| **WSL2** | ✅ Best experience | Full Linux environment |
| **WSL1** | ⚠️ Works | Limited, no WSL2 networking issues |
| **PowerShell** | ⚠️ Limited | Some commands fail, path issues |
| **CMD** | ❌ Not recommended | Poor compatibility |

### Windows Installation

| Method | Command | Notes |
|--------|---------|-------|
| **Native (Recommended)** | `irm https://claude.ai/install.ps1 \| iex` | PowerShell, auto-updates |
| **WinGet** | `winget install Anthropic.ClaudeCode` | Manual updates |
| **NPM (Deprecated)** | Not recommended | Use native installer |

### Git Bash Setup (Simplest)

```bash
# 1. Install Git for Windows (includes Git Bash)
# Download from: https://git-scm.com/download/win

# 2. Install Claude Code in Git Bash
npm install -g @anthropic-ai/claude-code

# 3. Run from Git Bash
claude
```

### WSL2 Setup (Best Experience)

```powershell
# In PowerShell (Admin)
wsl --install
# Restart computer

# In WSL Ubuntu terminal
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source ~/.bashrc
nvm install 22
npm install -g @anthropic-ai/claude-code

# From PowerShell, create helper function
function claude { wsl -e bash -c "source ~/.profile && claude" }
```

### Common Windows Issues

| Issue | Cause | Solution |
|-------|-------|---------|
| **Bash variable expansion** | Bash pre-processes PowerShell vars | Use Git Bash or escape properly |
| **Commands fail, then succeed** | Path/environment mismatch | CC auto-retries, works second time |
| **"Node not found"** | WSL using Windows Node.js | Install Node in WSL via nvm |
| **Path issues** | Windows/Linux path confusion | Ensure `which node` shows `/usr/` not `/mnt/c/` |

### Windows Workaround for Cross-Platform Scripts

**Issue:** Test scripts must work locally (Windows) AND in GitHub Actions (Linux)

**Solutions:**
1. Use Git Bash for local development
2. Write platform-agnostic scripts (Node.js instead of bash)
3. Test in WSL2 to match Linux behavior
4. Use PowerShell Core (cross-platform) for automation

### Environment Variable for Windows Context

```json
// Tell CC it's running on Windows
{
  "environment": {
    "CLAUDE_OS": "windows"
  }
}
```

**Note:** Check official docs for latest Windows-specific configurations

---

## Keyboard Shortcuts

### Essential Shortcuts

| Shortcut | Action | Use Case |
|----------|--------|----------|
| `Ctrl+C` | Cancel current operation | Stop generation, exit input |
| `Ctrl+R` | Search command history | Find previous commands |
| `Ctrl+L` | Clear screen (not conversation) | Visual cleanup |
| `Tab` | Toggle extended thinking | Show/hide reasoning |
| `Shift+Tab` | Cycle permission modes | Normal → Auto → Plan |
| `Esc` | Interrupt current phase | Stop thinking/tools/edits |
| `Esc+Esc` | Rewind/edit previous | Time travel, fix mistakes |
| `Ctrl+B` | Background bash command | Run without blocking |
| `Ctrl+D` | Exit session | Clean exit |
| `Ctrl+O` | Verbose mode toggle | Show detailed output |
| `Ctrl+G` | Open text editor | For long responses |

### Multiline Input

| Method | Keys | When |
|--------|------|------|
| **Backslash-enter** | `\ + Enter` | Continue to next line |
| **Option-enter** (macOS) | `Option + Enter` | macOS multiline |
| **Shift-enter** | `Shift + Enter` | After `/terminal-setup` |
| **Control sequence** | `Ctrl+J` | Alternative method |

### Quick Prefixes

| Prefix | Action | Example |
|--------|--------|---------|
| `#` | Quick memory add | `#Use 2-space indentation` |
| `/` | Slash command | `/help`, `/review` |
| `!` | Direct bash execution | `!ls -la` (bypasses CC) |
| `@` | File/path autocomplete | `@./src/` then Tab |

---

## Troubleshooting

### Common Issues & Solutions

| Issue | Cause | Solution | Command |
|-------|-------|----------|---------|
| **"Context window full"** | Too much conversation | Compact or clear | `/compact` or `/clear` |
| **Slow responses** | High context usage | Compress history | `/compact` |
| **"Rate limit exceeded"** | Too many requests | Slow down, check usage | `/usage` |
| **Agent not responding** | Stuck subprocess | Cancel or check background | `Ctrl+C` or `/bashes` |
| **Repeated permission prompts** | Not in allow list | Add to permissions | `/permissions` |
| **Installation issues** | Various | Run diagnostics | `/doctor` or `claude --debug` |
| **MCP connection fails** | Auth or config | Check with debug flag | `--mcp-debug` |
| **Commands fail on Windows** | Shell incompatibility | Use Git Bash or WSL | See Windows section |

### Diagnostic Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/doctor` | Health check | Installation problems |
| `/status` | Connection status | Can't reach API |
| `claude --debug` | Debug mode | See internal operations |
| `claude --version` | Check version | Verify installation |
| `claude update` | Update to latest | Get bug fixes |
| `npx ccusage@latest` | Usage analytics | Track consumption |

### Finding Help

| Resource | When to Use | Access |
|----------|-------------|--------|
| `/help` | Quick command reference | In any session |
| Official docs | Detailed features | https://docs.anthropic.com/en/docs/claude-code/overview |
| GitHub issues | Known bugs | https://github.com/anthropics/claude-code/issues |
| `/bug` | Report new issues | In session |
| Community resources | Advanced techniques | Awesome Claude Code repo |

### Lost? Try This Order

1. `/help` - See available commands
2. Check built-in skills - "What skills do you have?"
3. Review CLAUDE.md - `/memory`
4. Ask CC itself - "What's the best way to [task]?"
5. Search official docs - https://docs.anthropic.com
6. Community resources - GitHub, Reddit, Medium

---

## Power User Techniques

### Plan-First Approach (Anti-YOLO)

| Step | Action | Purpose | Command |
|------|--------|---------|---------|
| 1. **Brainstorm** | Explain problem space | Explore approaches | Natural discussion |
| 2. **ASCII Wireframe** | Request visual | Fast iterations | "Draw ASCII wireframe" |
| 3. **Plan³** | Enter plan mode, ask questions | Thorough planning | `Shift+Tab+Tab` |
| 4. **Test** | Verify solution | Catch issues early | Run tests |
| 5. **Ship** | Deploy with confidence | Quality assured | Commit & push |

### Multi-Agent Workflows

| Pattern | Setup | Use Case |
|---------|-------|----------|
| **Specialist** | Create domain experts | database-expert, api-designer, performance-optimizer |
| **Role** | Model team roles | code-reviewer, product-manager, devops-engineer |
| **Tool** | Focus on specific tools | docker-specialist, kubernetes-expert, terraform-engineer |

### Context Priming

Load project overview before work:
```markdown
# In CLAUDE.md or custom command
Load:
- Architecture overview @./docs/architecture.md
- API patterns @./docs/api-patterns.md
- Style guide @./docs/style-guide.md

Then begin work on [task].
```

### Productivity Tracking

| Tool | Purpose | Command |
|------|---------|---------|
| Vibe-Log CLI | Track productivity over time | `npx vibe-log-cli@latest` |
| Vibe-Log Co-Pilot | Strategic guidance | `npx vibe-log-cli` |
| CCusage | Token/cost tracking | `npx ccusage@latest` |

Reference: https://github.com/vibe-log/vibe-log-cli

### Solo Dev Anti-Bloat

**Add to CLAUDE.md for POC work:**
```markdown
## Anti-Bloat Rules
- YOU MUST prioritize simple, readable code with minimal abstraction
- DO NOT preserve backward compatibility unless requested
- DO NOT add abstractions until actually needed
- DO NOT build for imaginary future requirements
- DO NOT suggest design patterns unless problem requires them
- Keep it simple and direct
```

---

## Anti-Patterns

### What NOT to Do

| ❌ Anti-Pattern | ✅ Instead | Why |
|----------------|-----------|-----|
| Not committing before CC | Always `git commit -am "WIP"` | No rollback point |
| Dumping 20+ tasks at once | Feed 3-5 tasks max | CC loses focus after task 5 |
| No plan mode for complex work | Use `Shift+Tab+Tab` | Jumping to code causes mistakes |
| Waiting for "perfect" code | Commit when working | Save progress immediately |
| Using YOLO mode everywhere | Reserve for trusted scenarios | Dangerous for exploratory work |
| Over-explaining basic concepts | Claude knows programming | Wastes tokens |
| Not spreading rules across files | Use hierarchical CLAUDE.md | Cleaner organization |
| Ignoring context usage | Check `/context` regularly | Avoid degraded performance |
| Same session for unrelated work | `/clear` between topics | Context pollution |
| Not using subagents | Delegate to specialists | Better results, token efficiency |

### Quality Gates

| Before Action | Check | Command |
|---------------|-------|---------|
| **Before coding** | Enter plan mode | `Shift+Tab+Tab` |
| **Before commit** | Run review | `/review` |
| **Before push** | Check TODOs | `/todos` |
| **After success** | Commit immediately | `git commit -am "Working: feature"` |
| **Context >20%** | Compact | `/compact` |

---

## Quick Reference Card

### Most Used Commands
```
/help           Get help
/init           Create CLAUDE.md (new projects)
/clear          Clear conversation
/compact        Compress context
/context        View context usage
/memory         Edit CLAUDE.md
/review         Code review
/permissions    Manage permissions
/cost           Token usage
/status         View status
```

### Essential Shortcuts
```
Ctrl+C          Cancel
Ctrl+R          Search history
Shift+Tab+Tab   Plan mode
Tab             Toggle thinking
Esc+Esc         Rewind
# text          Quick memory add
@ path          File autocomplete
! command       Direct bash
```

### Critical Workflow
```
1. cd <project>
2. git checkout -b feature-x
3. claude
4. /init (if new project)
5. Shift+Tab+Tab (plan mode)
6. [Work with CC]
7. git commit -am "Working"
8. /review
9. git push
```

---

## Additional Resources

### Official Anthropic
- Docs: https://docs.anthropic.com/en/docs/claude-code/overview
- Best Practices: https://www.anthropic.com/engineering/claude-code-best-practices
- Skills Repo: https://github.com/anthropics/skills
- GitHub: https://github.com/anthropics/claude-code

### Community
- Awesome Claude Code: https://github.com/hesreallyhim/awesome-claude-code (13k+ stars)
- Volt Subagents: https://github.com/VoltAgent/awesome-claude-skills (2k+ stars)
- Productivity Tools: https://github.com/vibe-log/vibe-log-cli

### Tutorials
- Shipyard Cheat Sheet: https://shipyard.build/blog/claude-code-cheat-sheet/
- Neon Workflow: https://neon.tech/blog/our-claude-code-cheatsheet
- Medium Articles: Search "Claude Code" on Medium

---

**Version:** 1.0 | **Date:** January 21, 2026
**Maintained by:** MRSL Engineering
**Feedback:** Submit via `/bug` or team channels

**Remember:** Plan first (`Shift+Tab+Tab`), commit often (`git commit -am "WIP"`), use `/review` before pushing!
