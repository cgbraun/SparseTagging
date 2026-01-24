# Claude Code Templates - Quick Reference Guide

**For**: Christopher @ MRSL
**Purpose**: Quick reference while implementing templates system with Claude Code
**Companion to**: CLAUDE_CODE_TEMPLATES_IMPLEMENTATION_PLAN.md

---

## 🚀 Quick Start

### In PyCharm Terminal:

```bash
# 1. Create workspace
mkdir claude-code-templates
cd claude-code-templates

# 2. Start Claude Code
claude

# 3. Give initial prompt (see below)
```

---

## 📋 Phase-by-Phase Prompts

### Phase 1: Foundation (Give to Claude Code)

```
I'm implementing a Claude Code project templates system for defense-grade Python projects.

Read CLAUDE_CODE_TEMPLATES_IMPLEMENTATION_PLAN.md for the complete specification.

Start with Phase 1 only:
1. Create directory structure: templates/, examples/, scripts/
2. Create QUALITY_STANDARDS.md based on SparseTag patterns
3. Create basic README.md with quick start guide
4. Set up examples/reference-sparsetag/ with copies of uploaded files

Show me the created structure before proceeding to Phase 2.
```

**Expected Output**:
```
claude-code-templates/
├── README.md
├── QUALITY_STANDARDS.md
├── templates/
├── examples/
│   └── reference-sparsetag/
│       ├── CLAUDE.md
│       └── settings.local.json
└── scripts/
```

**Validation**: `ls -R` to verify structure

---

### Phase 2: Python Library Template (Give to Claude Code)

```
Now implement Phase 2: Python Library Template.

Create templates/python-library/ with all files from the plan:
- CLAUDE.md.template (generalized from SparseTag)
- settings.local.json.template (defense-grade permissions)
- .claude/hooks.json.template
- Configuration files: mypy.ini, .ruff.toml, pyproject.toml, .pre-commit-config.yaml
- .github/workflows/ci.yml.template
- tests/test_example.py.template
- PROJECT_SETUP.md

Use placeholders: {{PROJECT_NAME}}, {{PACKAGE_NAME}}, {{AUTHOR_NAME}}, {{AUTHOR_EMAIL}}, {{PYTHON_VERSION}}, {{MIN_COVERAGE}}, {{MAX_COMPLEXITY}}

Show me CLAUDE.md.template structure before creating all files.
```

**Validation**:
```bash
ls -la templates/python-library/
cat templates/python-library/CLAUDE.md.template | grep "{{PROJECT_NAME}}"
```

---

### Phase 3: Interactive Script (Give to Claude Code)

```
Implement Phase 3: Interactive Setup Script (init_project.py).

Requirements from the plan:
- Python 3.8+ stdlib only
- Interactive prompts with validation
- Placeholder replacement engine with filter support
- Safe file operations with rollback capability
- Clear error messages
- Dry-run mode (--dry-run flag)

Test it works:
python init_project.py --dry-run

Then test actual creation:
python init_project.py

Expected inputs: project name, type (library), description, author info
```

**Validation**:
```bash
# Dry run
python init_project.py --dry-run

# Real test
mkdir test-output
cd test-output
python ../init_project.py
# Follow prompts: name=test-lib, type=library, description="Test library"

# Verify output
ls -la
cat CLAUDE.md | grep "Test library"
pytest tests/
```

---

### Phase 4: Testing (Give to Claude Code)

```
Now test the templates thoroughly:

1. Create test project: calculator-lib
   - Run: python init_project.py
   - Inputs: name=calculator-lib, type=library, description="Calculator library"
   - Verify: all files created, placeholders replaced, tests run

2. Test invalid inputs:
   - Try: name=InvalidName (should reject uppercase)
   - Try: name=-invalid (should reject starting with -)
   - Try: email=invalid (should reject bad format)

3. Run quality checks in test project:
   cd test-output/calculator-lib
   ruff check .
   mypy src/calculator_lib
   pytest tests/

Document any issues found in TESTING_NOTES.md
```

---

### Phase 5: Documentation (Give to Claude Code)

```
Polish the documentation:

1. Complete README.md with:
   - Installation instructions
   - Quick start example
   - Template types comparison table
   - Customization guide
   - Troubleshooting section

2. Add examples/reference-sparsetag/REFERENCE_NOTES.md:
   - Key patterns from SparseTag
   - Why certain sections are structured that way
   - Lessons learned

3. Create templates/python-cli/ skeleton (same as library but with CLI additions)

Show me the README structure before writing full content.
```

---

## 🎯 Key Validation Commands

After each phase, run these:

```bash
# Structure validation
tree -L 3  # Or: find . -type f | sort

# Template validation
grep -r "{{PROJECT_NAME}}" templates/  # Should find placeholders

# Placeholder replacement test
grep "{{" test-output/*/  # Should find NONE after init_project.py

# Quality checks (in generated project)
cd test-output/test-lib/
ruff check .
mypy src/test_lib
pytest tests/ -v
```

---

## 📝 Expected Placeholders

These must be in templates:

```
{{PROJECT_NAME}}           # e.g., "sparsetag"
{{PROJECT_NAME_UPPER}}     # e.g., "SPARSETAG"
{{PACKAGE_NAME}}           # e.g., "sparsetag" (Python identifier)
{{PROJECT_DESCRIPTION}}    # e.g., "High-performance sparse arrays"
{{AUTHOR_NAME}}            # e.g., "Christopher Braun"
{{AUTHOR_EMAIL}}           # e.g., "cbraun@example.com"
{{PYTHON_VERSION}}         # e.g., "3.8"
{{CURRENT_YEAR}}           # e.g., "2026"
{{CURRENT_DATE}}           # e.g., "2026-01-23"
{{MIN_COVERAGE}}           # Fixed: 85 (defense-grade)
{{MAX_COMPLEXITY}}         # Fixed: 15 (defense-grade)
```

---

## 🔧 Troubleshooting

### Issue: Placeholders not replaced

**Check**:
```bash
# In generated project
grep "{{" CLAUDE.md
# Should return nothing
```

**Fix**: Check `replace_placeholders()` function in init_project.py

---

### Issue: Tests fail in generated project

**Check**:
```bash
cd test-output/test-lib/
python -m pytest tests/ -v
```

**Common causes**:
1. Import path wrong (should be `from package_name.module`)
2. Virtual environment not activated
3. Dependencies not installed

**Fix**: Check test_example.py.template imports

---

### Issue: Permissions errors in Claude Code

**Check**: settings.local.json in generated project

**Expected**:
- ✅ Read permissions: granted
- ✅ Quality tool permissions: granted
- ❌ Git commit/push: DENIED (by design)
- ❌ pip install: DENIED (by design)

---

### Issue: Git operations fail

**Check**:
```bash
git --version
git config user.name
git config user.email
```

**Fix**: Set git config if missing:
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

---

## 🎨 Customization Points

After basic implementation works, consider:

### Add to CLAUDE.md.template:
- [ ] Project-specific architecture notes
- [ ] Performance benchmarks section
- [ ] API documentation links
- [ ] Deployment guide (for services)

### Add to settings.local.json.template:
- [ ] Project-specific bash commands
- [ ] Additional WebFetch domains
- [ ] Custom tool permissions

### Add to CI template:
- [ ] Deployment steps
- [ ] Performance benchmarking
- [ ] Integration tests
- [ ] E2E tests (for services)

---

## 📊 Success Checklist

Before considering done:

- [ ] Phase 1: Foundation exists and documented
- [ ] Phase 2: Python library template complete
- [ ] Phase 3: init_project.py works end-to-end
- [ ] Phase 4: Tests pass on generated projects
- [ ] Phase 5: Documentation complete

**Test Project Creation**:
- [ ] Can create project in <5 minutes
- [ ] All placeholders replaced correctly
- [ ] pytest runs successfully
- [ ] ruff check passes
- [ ] mypy passes with strict mode
- [ ] CI workflow is valid YAML
- [ ] README renders correctly on GitHub

**Generated Project Quality**:
- [ ] CLAUDE.md is comprehensive
- [ ] settings.local.json has defense-grade permissions
- [ ] All config files are valid
- [ ] Pre-commit hooks work
- [ ] Can add new module and test it
- [ ] Quality checks catch intentional errors

---

## 🔄 Iterative Refinement

After first implementation:

### Round 1: Basic Functionality
1. Get init_project.py working
2. Generate one test project
3. Fix obvious bugs

### Round 2: Quality
1. Add comprehensive validation
2. Improve error messages
3. Add dry-run mode

### Round 3: Polish
1. Complete documentation
2. Add CLI and service templates
3. Create upgrade script

---

## 💡 Pro Tips for Working with Claude Code

### Effective Prompts:

**Good**:
```
Create init_project.py with these specific requirements:
1. Collect user input for project name (validate: lowercase, hyphens ok)
2. Collect project type: library | cli | service
3. Replace all {{PLACEHOLDER}} in template files
4. Show summary before executing

Test by running: python init_project.py --dry-run
```

**Less Good**:
```
Make the script
```

### Validation Strategy:

After Claude creates files:
```
Show me:
1. Directory structure (ls -R)
2. First 20 lines of CLAUDE.md.template
3. Placeholders used (grep "{{" templates/ -r)

Then I'll confirm you should continue.
```

### Incremental Testing:

```
Let's test the placeholder replacement function first:

Create test_placeholder_replacement.py with:
- Test replace "{{PROJECT_NAME}}" → "myproject"
- Test replace "{{PROJECT_NAME_UPPER}}" → "MYPROJECT"
- Test with filters: "{{PYTHON_VERSION|replace}}" → "38"

Run: python test_placeholder_replacement.py
```

---

## 🎓 Expected Learning Outcomes

After implementing this:

1. ✅ **Understand template systems**: Reusable project skeletons
2. ✅ **Defense-grade standards**: What they are, why they matter
3. ✅ **Effective Claude Code**: Structured prompts, validation, iteration
4. ✅ **Python tooling**: ruff, mypy, pytest, pre-commit ecosystem
5. ✅ **CI/CD patterns**: Quality gates, graceful degradation, path filtering

---

## 📚 Reference Documents

While implementing, keep these open:

1. **CLAUDE_CODE_TEMPLATES_IMPLEMENTATION_PLAN.md** - Full specification
2. **examples/reference-sparsetag/CLAUDE.md** - Real-world example
3. **QUALITY_STANDARDS.md** - Defense-grade requirements
4. **This file** - Quick reference

---

## 🚨 Critical Reminders

1. **Don't hardcode**: Use placeholders everywhere
2. **Validate early**: Check inputs before file operations
3. **Test frequently**: Run init_project.py after each change
4. **Read permissions**: Defense-grade = permissive reads, restrictive writes
5. **No shortcuts**: Follow the plan, it's based on real experience

---

## 🎯 Final Test Scenario

Before declaring victory:

```bash
# Clean slate
rm -rf claude-code-templates/
mkdir claude-code-templates/
cd claude-code-templates/

# Run implementation (Phases 1-5)
# ... (follow prompts above)

# Final validation
python init_project.py
# Inputs:
#   name: defense-calculator
#   type: library
#   description: "High-security calculator for defense applications"
#   author: Christopher Braun
#   email: cbraun@mrsl.com
#   python: 3.10
#   [accept all defaults]

# Navigate to project
cd defense-calculator/

# Run complete quality suite
ruff format .
ruff check .
mypy src/defense_calculator
pytest tests/ --cov=src/defense_calculator --cov-report=html
bandit -r src/defense_calculator
pip-audit

# All should pass ✅

# Verify Claude Code integration
cat CLAUDE.md  # Should be comprehensive, no placeholders
cat .claude/settings.local.json  # Should have defense-grade permissions
cat .claude/hooks.json  # Should have post-edit test running

# Try editing code
# Claude Code should auto-run tests after save (if hooks enabled)

# Success! 🎉
```

---

**Remember**: This is a living system. After using it on 2-3 real projects, update templates with lessons learned.

**Good luck!** 🚀
