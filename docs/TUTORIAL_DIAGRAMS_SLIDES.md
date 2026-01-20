# Tutorial Diagrams - LLM-First Development (Slide-Optimized)

## Overview

This document contains slide-optimized versions of the tutorial diagrams, formatted for standard 8x10 PPT 4:3 layout with:
- **Minimum font size**: 14pt bold (16pt+ preferred)
- **Layout**: 4:3 aspect ratio, horizontal/landscape orientation
- **Color palette**: Academic/Technical (neutral tones with accent colors)
- **Text**: Always bold; white text on dark backgrounds, black text on light backgrounds
- **Borders**: White outlines for visibility on dark backgrounds

## Color Palette

- **Primary Actions**: Dark Blue/Cyan (#0e7490) - **WHITE BOLD TEXT**
- **Success/Complete**: Dark Green (#065f46) - **WHITE BOLD TEXT**
- **Decisions**: Muted Orange (#b45309) - **WHITE BOLD TEXT**
- **Light Backgrounds**: Pastels - **BLACK BOLD TEXT**
- **Borders**: White (2-3px) for shape outlines

## Table of Contents

### Master/Big Picture
1. [Complete Development Lifecycle](#1-complete-development-lifecycle)
2. [Tool Ecosystem Map](#2-tool-ecosystem-map)
3. [LLM Plan-Execute-Refine Loop](#3-llm-plan-execute-refine-loop)

---

## Master/Big Picture

### 1. Complete Development Lifecycle

**Summary**: This diagram shows the complete 12-phase development lifecycle organized in four horizontal rows stacked vertically for optimal 4:3 slide format. The flow progresses from top-to-bottom and left-to-right within each row. The first section covers concept through core development, the second handles testing through CI/CD, the third covers quality tools through documentation, and the fourth completes with Docker build, deployment, and publishing. Each phase includes quality gates (decision points) that determine whether work proceeds or requires refinement.

The lifecycle follows logical progression but shows the reality of development: failed tests trigger refactoring, security issues force architectural changes, and documentation gaps reveal requirements ambiguities. Feedback loops connect upward to earlier phases when quality gates fail, routing around intermediate sections. This represents the rigorous, quality-focused approach where LLM assistance accelerates iteration speed without compromising standards.

**Purpose**: Provide 10,000-foot view of entire development process with quality checkpoints.

**Usage**: Tutorial introduction to show complete journey from idea to published package.

```mermaid
graph LR
    subgraph CONCEPT["<b>CONCEPT TO CORE DEVELOPMENT</b>"]
        direction TB
        Start([<b>CONCEPT</b>]) --> P0[<b>PHASE 0</b><br/><b>Requirements</b>]
        P0 --> QG0{<b>Clear?</b>}
        QG0 -->|<b>No</b>| P0
        QG0 -->|<b>Yes</b>| P1[<b>PHASE 1</b><br/><b>Architecture</b>]
        P1 --> QG1{<b>Viable?</b>}
        QG1 -->|<b>No</b>| P1
        QG1 -->|<b>Yes</b>| P2[<b>PHASE 2</b><br/><b>Core Dev</b>]
    end

    subgraph TESTING["<b>TESTING TO CI/CD</b>"]
        direction TB
        P3[<b>PHASE 3</b><br/><b>Testing</b>] --> QG2{<b>Pass?</b>}
        QG2 -->|<b>Yes</b>| P4[<b>PHASE 4</b><br/><b>Integration</b>]
        P4 --> P5[<b>PHASE 5</b><br/><b>CI/CD</b>]
        P5 --> QG3{<b>Healthy?</b>}
        QG3 -->|<b>No</b>| P4
    end

    subgraph QUALITY["<b>QUALITY TO DOCUMENTATION</b>"]
        direction TB
        P6[<b>PHASE 6</b><br/><b>Quality</b>] --> QG4{<b>Standards<br/>Met?</b>}
        QG4 -->|<b>Yes</b>| P7[<b>PHASE 7</b><br/><b>Security</b>]
        P7 --> QG5{<b>Secure?</b>}
        QG5 -->|<b>Yes</b>| P8[<b>PHASE 8</b><br/><b>Docs</b>]
    end

    subgraph DEPLOY["<b>BUILD TO RELEASE</b>"]
        direction TB
        P9[<b>PHASE 9</b><br/><b>Docker</b>] --> QG6{<b>Built?</b>}
        QG6 -->|<b>No</b>| P9
        QG6 -->|<b>Yes</b>| P10[<b>PHASE 10</b><br/><b>Deploy</b>]
        P10 --> QG7{<b>Works?</b>}
        QG7 -->|<b>No</b>| P10
        QG7 -->|<b>Yes</b>| P11[<b>PHASE 11</b><br/><b>Publish</b>]
        P11 --> End([<b>RELEASED</b>])
    end

    P2 --> P3
    QG2 -->|<b>No</b>| P2
    QG3 -->|<b>Yes</b>| P6
    QG4 -->|<b>No</b>| P2
    QG5 -->|<b>No</b>| P1
    P8 --> P9

    style Start fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style End fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style P0 fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style P1 fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style P2 fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style P3 fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style P4 fill:#cffafe,stroke:#fff,stroke-width:2px,color:#000
    style P5 fill:#cffafe,stroke:#fff,stroke-width:2px,color:#000
    style P6 fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style P7 fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style P8 fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
    style P9 fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
    style P10 fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style P11 fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style QG0 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style QG1 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style QG2 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style QG3 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style QG4 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style QG5 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style QG6 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style QG7 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
```

---

### 2. Tool Ecosystem Map

**Summary**: This diagram maps the complete tool ecosystem organized by functional layers, showing how tools interconnect through data flows and API integrations. The foundation layer contains development tools (Claude Code, ChatGPT) that interact with version control (Git/GitHub). The quality layer shows how code flows through pre-commit hooks (Ruff, Mypy) before reaching CI/CD, which then coordinates with external scanning services (SonarCloud, CodeCov, Trivy). The deployment layer shows the build-publish pipeline from Docker to GHCR, with security validation at each step.

The diagram emphasizes data flow and interdependencies: test results flow to CodeCov, code flows to SonarCloud, vulnerabilities flow from Trivy to PR checks. This helps developers understand which tools to configure first and how changes propagate through the system.

**Purpose**: Show interconnected tool landscape organized by functional layers and data flows.

**Usage**: Architecture overview to understand tool selection, configuration order, and integration points.

```mermaid
graph TB
    subgraph DEV["<b>DEVELOPMENT LAYER</b>"]
        CC[<b>Claude Code</b><br/><b>AI Assistant</b>]
        GPT[<b>ChatGPT Codex</b><br/><b>AI Assistant</b>]
        GIT[<b>Git</b><br/><b>Version Control</b>]
    end

    subgraph QUALITY["<b>QUALITY LAYER</b>"]
        RUFF[<b>Ruff</b><br/><b>Lint/Format</b>]
        MYPY[<b>Mypy</b><br/><b>Type Check</b>]
        PYTEST[<b>Pytest</b><br/><b>Testing</b>]
        PRECOMMIT[<b>Pre-commit</b><br/><b>Hook Manager</b>]
    end

    subgraph CI["<b>CI/CD LAYER</b>"]
        GHA[<b>GitHub Actions</b><br/><b>Automation</b>]
        SONAR[<b>SonarCloud</b><br/><b>Code Quality</b>]
        CODECOV[<b>CodeCov</b><br/><b>Coverage</b>]
        TRIVY[<b>Trivy</b><br/><b>CVE Scan</b>]
    end

    subgraph DEPLOY["<b>DEPLOYMENT LAYER</b>"]
        DOCKER[<b>Docker</b><br/><b>Container Build</b>]
        GHCR[<b>GHCR</b><br/><b>Registry</b>]
        PYPI[<b>PyPI</b><br/><b>Package Repo</b>]
    end

    CC -->|<b>Code Changes</b>| GIT
    GPT -->|<b>Code Changes</b>| GIT
    GIT -->|<b>Pre-commit</b>| PRECOMMIT
    PRECOMMIT -->|<b>Run</b>| RUFF
    PRECOMMIT -->|<b>Run</b>| MYPY
    GIT -->|<b>Push</b>| GHA
    GHA -->|<b>Run</b>| PYTEST
    GHA -->|<b>Analysis</b>| SONAR
    PYTEST -->|<b>Coverage</b>| CODECOV
    GHA -->|<b>Scan</b>| TRIVY
    GHA -->|<b>Build</b>| DOCKER
    DOCKER -->|<b>Push</b>| GHCR
    GHA -->|<b>Publish</b>| PYPI
    SONAR -->|<b>Quality Gate</b>| GHA
    CODECOV -->|<b>Coverage Gate</b>| GHA
    TRIVY -->|<b>Vuln Gate</b>| GHA

    style CC fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style GPT fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style GIT fill:#374151,stroke:#fff,stroke-width:3px,color:#fff
    style RUFF fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style MYPY fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style PYTEST fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style PRECOMMIT fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style GHA fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style SONAR fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style CODECOV fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style TRIVY fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
    style DOCKER fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
    style GHCR fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
    style PYPI fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
```

---

### 3. LLM Plan-Execute-Refine Loop

**Summary**: This diagram captures the iterative cycle at the heart of LLM-first development: detailed planning before execution, rigorous validation after execution, and learning-driven refinement. Unlike traditional "code first, fix later" approaches, this workflow emphasizes upfront planning where the LLM explores the codebase, reviews existing patterns, and proposes architecture before writing any code. The execution phase involves TDD cycles with continuous testing, and validation checks code quality, test coverage, and security standards.

The refinement loop is critical: failed validation triggers analysis and learning rather than abandonment. The LLM examines what went wrong and refines the implementation. This cycle repeats until all quality gates pass. LLM speed makes multiple iterations practical - what would take hours manually takes minutes with AI assistance.

**Purpose**: Show iterative planning-execution-validation cycle with learning feedback loops.

**Usage**: Core methodology section explaining how LLM assistance enables rigorous iterative development.

```mermaid
graph LR
    subgraph PLAN_PHASE["<b>PLANNING</b>"]
        direction TB
        Start([<b>TASK/FEATURE</b>]) --> Plan[<b>PLAN</b><br/><b>Explore Codebase</b><br/><b>Review Patterns</b><br/><b>Propose Architecture</b>]
        Plan --> Review{<b>Review<br/>Plan?</b>}
        Review -->|<b>Issues</b>| Plan
    end

    subgraph EXECUTE_PHASE["<b>EXECUTION</b>"]
        direction TB
        Execute[<b>EXECUTE</b><br/><b>Write Code</b><br/><b>Run Tests</b><br/><b>Fix Failures</b>]
        Execute --> Validate[<b>VALIDATE</b><br/><b>Check Quality</b><br/><b>Review Coverage</b><br/><b>Scan Security</b>]
        Validate --> Gate{<b>Pass All<br/>Gates?</b>}
    end

    subgraph REFINE_PHASE["<b>REFINEMENT</b>"]
        direction TB
        Refine[<b>REFINE</b><br/><b>Analyze Failures</b><br/><b>Update Approach</b><br/><b>Learn Patterns</b>]
        Refine --> RefineOut[ ]
    end

    subgraph COMPLETE_PHASE["<b>COMPLETION</b>"]
        direction TB
        Complete([<b>FEATURE<br/>COMPLETE</b>])
    end

    Review -->|<b>Approved</b>| Execute
    Gate -->|<b>No</b>| Refine
    RefineOut --> Execute
    Gate -->|<b>Yes</b>| Complete

    style RefineOut fill:none,stroke:none

    style Start fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style Plan fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style Execute fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Validate fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Refine fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style Review fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Gate fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Complete fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
```

---


## Phase-Specific Flows

### 4. Phase 0: Concept to Requirements

**Summary**: Phase 0 begins with a user need or business problem. The developer engages with the LLM to clarify the concept through dialogue, asking questions about scope, constraints, users, and success criteria. The LLM helps refine vague ideas into specific requirements by prompting for missing information and identifying edge cases. Once requirements are clear, they are documented in a structured format. This phase emphasizes thorough upfront thinking to avoid rework later.

**Purpose**: Transform vague concepts into clear, documented requirements through LLM-assisted dialogue.

**Usage**: Phase 0 chapter - teaches readers how to use LLMs to clarify requirements before writing code.

```mermaid
graph LR
    subgraph CLARIFY["<b>CLARIFICATION PHASE</b>"]
        direction TB
        Start([<b>USER NEED</b>]) --> InitPrompt[<b>Initial Prompt to LLM</b>]
        InitPrompt --> Clarify[<b>LLM: Ask Questions</b>]
        Clarify --> Dialogue{<b>Iterative Dialogue</b>}
        Dialogue -->|<b>More Questions</b>| Clarify
        Dialogue -->|<b>Sufficient Detail</b>| Scope[<b>Define Scope</b>]
    end

    subgraph DOCUMENT["<b>DOCUMENTATION PHASE</b>"]
        direction TB
        Users[<b>Identify Users</b>] --> Success[<b>Success Criteria</b>]
        Success --> Document[<b>Document Requirements</b>]
        Document --> Review{<b>Complete?</b>}
        Review -->|<b>Complete</b>| Output([<b>REQUIREMENTS DOC</b>])
    end

    Scope --> Users
    Review -->|<b>Missing Info</b>| Clarify

    style Start fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style Output fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style Review fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Dialogue fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style InitPrompt fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style Clarify fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Scope fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Users fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Success fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Document fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
```

---

### 5. Phase 1: Feature Specification

**Summary**: With requirements in hand, Phase 1 creates a detailed feature specification. The developer provides the requirements document as context to the LLM along with relevant codebase information. The LLM analyzes existing code to understand conventions and proposes how the feature should integrate. Together they define the feature interface, data structures, and integration points with usage examples.

**Purpose**: Create detailed feature specification with usage examples and integration points.

**Usage**: Phase 1 chapter - shows how to leverage LLM knowledge of codebase to create consistent designs.

```mermaid
graph LR
    subgraph ANALYSIS["<b>ANALYSIS PHASE</b>"]
        direction TB
        Input([<b>REQUIREMENTS DOC</b>]) --> Context[<b>Provide Context to LLM</b>]
        Context --> Analyze[<b>LLM: Analyze Codebase</b>]
        Analyze --> Patterns[<b>Identify Patterns</b>]
        Patterns --> Interface[<b>Define Feature Interface</b>]
    end

    subgraph SPECIFICATION["<b>SPECIFICATION PHASE</b>"]
        direction TB
        Data[<b>Define Data Structures</b>] --> Integration[<b>Define Integration Points</b>]
        Integration --> Examples[<b>Create Usage Examples</b>]
        Examples --> Review{<b>Review Complete?</b>}
        Review -->|<b>Complete</b>| Output([<b>FEATURE SPECIFICATION</b>])
    end

    Interface --> Data
    Review -->|<b>Incomplete</b>| Interface

    style Input fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style Output fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style Review fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Context fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style Analyze fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Patterns fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Interface fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Data fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Integration fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Examples fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
```

---

### 6. Phase 2: Planning & Design

**Summary**: Phase 2 is the detailed technical planning phase. The LLM enters plan mode to explore the codebase thoroughly, understanding existing architecture, dependencies, and potential conflicts. Based on this exploration, the LLM proposes an architectural approach. The developer and LLM discuss trade-offs between different approaches. Once an approach is selected, they break it into implementation tasks, identify files to modify, plan test strategy, and identify risks.

**Purpose**: Create detailed technical implementation plan through LLM-assisted architecture exploration.

**Usage**: Phase 2 chapter - demonstrates the critical planning phase that determines implementation success.

```mermaid
graph LR
    subgraph EXPLORATION["<b>EXPLORATION PHASE</b>"]
        direction TB
        Input([<b>FEATURE SPEC</b>]) --> PlanMode[<b>LLM: Enter Plan Mode</b>]
        PlanMode --> Explore[<b>LLM: Explore Codebase</b>]
        Explore --> Arch[<b>LLM: Propose Architecture</b>]
        Arch --> Tradeoffs[<b>Discuss Trade-offs</b>]
        Tradeoffs --> Select{<b>Select Approach</b>}
        Select -->|<b>Alternative</b>| Arch
    end

    subgraph PLANNING["<b>PLANNING PHASE</b>"]
        direction TB
        Tasks[<b>Break Into Tasks</b>] --> Files[<b>Identify Files to Modify</b>]
        Files --> Tests[<b>Plan Test Strategy</b>]
        Tests --> Risks[<b>Identify Risks</b>]
        Risks --> Review{<b>Review Plan?</b>}
        Review -->|<b>Approved</b>| Output([<b>IMPLEMENTATION PLAN</b>])
    end

    Select -->|<b>Approved</b>| Tasks
    Review -->|<b>Revise</b>| Arch

    style Input fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style Output fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style Select fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Review fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style PlanMode fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style Explore fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Arch fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Tradeoffs fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Tasks fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Files fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Tests fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Risks fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
```

---

### 7. Phase 3: Implementation (TDD Cycle)

**Summary**: Phase 3 is where code gets written using test-driven development. The cycle starts by writing a failing test for the next small piece of functionality (Red). The LLM writes minimal code to make the test pass (Green). Then the code is refactored for quality while keeping tests passing (Refactor). This red-green-refactor cycle repeats for each piece of functionality. Quality checks (Ruff, Mypy) run continuously. When all functionality is complete and all tests pass, Phase 3 is done.

**Purpose**: Show test-driven development cycle with LLM writing tests and implementation code.

**Usage**: Phase 3 chapter - demonstrates rigorous TDD approach with immediate quality feedback.

```mermaid
graph LR
    subgraph RED["<b>RED: WRITE TEST</b>"]
        direction TB
        Start([<b>PLAN</b>]) --> WriteTest[<b>Write<br/>Failing Test</b>]
        WriteTest --> Fail{<b>Fails?</b>}
        Fail -->|<b>No</b>| WriteTest
    end

    subgraph GREEN["<b>GREEN: MAKE PASS</b>"]
        direction TB
        WriteCode[<b>Write<br/>Code</b>] --> Pass{<b>Passes?</b>}
        Pass -->|<b>No</b>| WriteCode
    end

    subgraph REFACTOR["<b>REFACTOR: IMPROVE</b>"]
        direction TB
        Refactor[<b>Refactor<br/>Code</b>] --> Quality[<b>Quality<br/>Checks</b>]
        Quality --> QPass{<b>Pass?</b>}
        QPass -->|<b>No</b>| Refactor
        QPass -->|<b>Yes</b>| More{<b>More?</b>}
        More -->|<b>No</b>| Complete([<b>DONE</b>])
    end

    Fail -->|<b>Yes</b>| WriteCode
    Pass -->|<b>Yes</b>| Refactor
    More -->|<b>Yes</b>| WriteTest

    style Start fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style Complete fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style Fail fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Pass fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style QualityPass fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style More fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style WriteTest fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
    style RunTest1 fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
    style WriteCode fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style RunTest2 fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Refactor fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Quality fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
```

---

### 8. Phase 4: Integration Testing

**Summary**: Phase 4 verifies that components work together correctly. Unit tests from Phase 3 tested individual functions in isolation. Integration tests verify workflows across multiple components, database interactions, API calls, and file I/O. The LLM helps write integration test scenarios based on user workflows. Failed integration tests often reveal interface mismatches or incorrect assumptions. The LLM assists in debugging by analyzing test failures and proposing fixes.

**Purpose**: Validate cross-component interactions and end-to-end workflows.

**Usage**: Phase 4 chapter - shows how to design and debug integration tests with LLM assistance.

```mermaid
graph LR
    Start([<b>IMPLEMENTATION<br/>COMPLETE</b>]) --> Identify[<b>Identify Integration<br/>Scenarios</b>]
    Identify --> WriteTests[<b>Write Integration<br/>Tests</b>]
    WriteTests --> RunTests[<b>Run Integration<br/>Tests</b>]
    RunTests --> Results{<b>All Pass?</b>}
    Results -->|<b>No</b>| Analyze[<b>LLM: Analyze<br/>Failures</b>]
    Analyze --> Debug[<b>Debug Integration<br/>Issues</b>]
    Debug --> Fix[<b>Fix Code/Tests</b>]
    Fix --> RunTests
    Results -->|<b>Yes</b>| Coverage[<b>Check Coverage</b>]
    Coverage --> CovGate{<b>Coverage<br/>≥85%?</b>}
    CovGate -->|<b>No</b>| Identify
    CovGate -->|<b>Yes</b>| Complete([<b>INTEGRATION<br/>VERIFIED</b>])

    style Start fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style Complete fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style Results fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style CovGate fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Identify fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style WriteTests fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style RunTests fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Analyze fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style Debug fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style Fix fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style Coverage fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
```

---

### 9. Phase 5: CI/CD Setup

**Summary**: Phase 5 establishes continuous integration and deployment pipelines. The developer and LLM configure GitHub Actions workflows to run on every commit and PR. The pipeline includes multiple stages: install dependencies, run linters (Ruff), run type checking (Mypy), run all tests with coverage, build artifacts, and run security scans. Each stage has pass/fail gates. The LLM helps troubleshoot pipeline failures and optimize workflow performance. The result is automated quality enforcement on every code change.

**Purpose**: Establish automated testing, quality checks, and deployment pipelines.

**Usage**: Phase 5 chapter - demonstrates setting up robust CI/CD with multiple quality gates.

```mermaid
graph TB
    subgraph ROW1["<b>PIPELINE STAGES</b>"]
        direction LR
        Start([<b>INTEGRATION VERIFIED</b>]) --> Config[<b>Configure GitHub Actions</b>]
        Config --> Deps[<b>Stage 1: Install Deps</b>]
        Deps --> Lint[<b>Stage 2: Ruff Lint</b>]
        Lint --> Type[<b>Stage 3: Mypy Check</b>]
        Type --> Test[<b>Stage 4: Pytest Coverage</b>]
        Test --> Build[<b>Stage 5: Build Artifacts</b>]
        Build --> Scan[<b>Stage 6: Security Scan</b>]
        Scan --> Results{<b>All Stages Pass?</b>}
        Results -->|<b>Yes</b>| Complete([<b>CI/CD OPERATIONAL</b>])
    end

    subgraph ROW2["<b>DEBUG CYCLE</b>"]
        direction LR
        Debug[<b>LLM: Debug Failures</b>] --> Fix[<b>Fix Issues</b>]
        Fix --> Rerun[<b>Rerun Pipeline</b>]
    end

    Results -->|<b>No</b>| Debug
    Rerun --> Results

    style Start fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style Complete fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style Results fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Config fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style Deps fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Lint fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Type fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Test fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Build fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Scan fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Debug fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style Fix fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style Rerun fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
```

---
### 10. Phase 6: Performance Tuning

**Summary**: Phase 6 optimizes code performance once functionality is correct. The process starts with establishing baseline performance using benchmarks - measuring current speed, memory usage, and resource consumption. The LLM helps identify bottlenecks through profiling. Each bottleneck is analyzed to understand why it is slow. The LLM proposes optimizations specific to the bottleneck type. Each optimization is applied and measured to verify improvement. SparseTagging achieved 100-170x speedups through sparse matrix operations and intelligent caching.

**Purpose**: Systematically optimize performance using benchmarking, profiling, and targeted improvements.

**Usage**: Phase 6 chapter - teaches data-driven performance optimization with measurable improvements.

```mermaid
graph TB
    subgraph ROW1["<b>MEASUREMENT AND ANALYSIS</b>"]
        direction LR
        Input([<b>WORKING CODE</b>]) --> Baseline[<b>Establish Baseline</b>]
        Baseline --> Profile[<b>Profile Execution</b>]
        Profile --> Bottlenecks[<b>Identify Bottlenecks</b>]
        Bottlenecks --> Analyze[<b>LLM: Analyze Type</b>]
        Analyze --> Propose[<b>LLM: Propose Optimizations</b>]
    end

    subgraph ROW2["<b>OPTIMIZATION CYCLE</b>"]
        direction LR
        Select[<b>Select Optimization</b>] --> Implement[<b>Implement Change</b>]
        Implement --> Measure[<b>Measure Performance</b>]
        Measure --> Improved{<b>Improved?</b>}
        Improved -->|<b>No/Worse</b>| Select
        Improved -->|<b>Yes</b>| Verify[<b>Verify Tests Pass</b>]
        Verify --> TestsPass{<b>Tests Pass?</b>}
        TestsPass -->|<b>No</b>| Select
    end

    subgraph ROW3["<b>VALIDATION AND COMPLETION</b>"]
        direction LR
        Acceptable{<b>Acceptable Performance?</b>} -->|<b>No</b>| Profile
        Acceptable -->|<b>Yes</b>| Document[<b>Document Optimizations</b>]
        Document --> Output([<b>OPTIMIZED CODE</b>])
    end

    Propose --> Select
    TestsPass -->|<b>Yes</b>| Acceptable

    style Input fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style Output fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style Improved fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style TestsPass fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Acceptable fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Baseline fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style Profile fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Bottlenecks fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Analyze fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Propose fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Select fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Implement fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Measure fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
    style Verify fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
    style Document fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
```

---

### 11. Phase 7: Quality Checks

**Summary**: Phase 7 ensures code meets quality standards before CI/CD. The workflow runs three key tools in sequence: Ruff (linting and formatting), Mypy (type checking), and pre-commit hooks (automated enforcement). Ruff checks code style and identifies bugs. Mypy performs static type analysis. Pre-commit hooks run all checks automatically before each commit, preventing bad code from entering version control. Any failures must be fixed before proceeding.

**Purpose**: Enforce code quality standards locally before pushing to CI.

**Usage**: Phase 7 chapter - establishes local quality workflow that mirrors CI checks.

```mermaid
graph LR
    subgraph RUFF["<b>RUFF CHECKS</b>"]
        direction TB
        Input([<b>CODE</b>]) --> RuffLint[<b>Run Ruff Linting</b>]
        RuffLint --> RuffResult{<b>Pass?</b>}
        RuffResult -->|<b>Fail</b>| RuffFix[<b>Fix Issues</b>]
        RuffFix --> RuffLint
        RuffResult -->|<b>Pass</b>| Format[<b>Run Ruff Format</b>]
    end

    subgraph MYPY["<b>TYPE CHECKS</b>"]
        direction TB
        MypyRun[<b>Run Mypy</b>] --> MypyResult{<b>Pass?</b>}
        MypyResult -->|<b>Fail</b>| MypyFix[<b>Fix Type Errors</b>]
        MypyFix --> MypyRun
        MypyResult -->|<b>Pass</b>| PreCommit[<b>Install Pre-commit</b>]
    end

    subgraph HOOKS["<b>PRE-COMMIT HOOKS</b>"]
        direction TB
        TestCommit[<b>Test Commit</b>] --> HooksPass{<b>Hooks Pass?</b>}
        HooksPass -->|<b>Fail</b>| RuffFix
        HooksPass -->|<b>Pass</b>| Output([<b>QUALITY PASS</b>])
    end

    Format --> MypyRun
    PreCommit --> TestCommit

    style Input fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style Output fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style RuffResult fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style MypyResult fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style HooksPass fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style RuffLint fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style Format fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style RuffFix fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
    style MypyRun fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style MypyFix fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
    style PreCommit fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style TestCommit fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
```

---

### 12. Phase 8: Documentation

**Summary**: Phase 8 creates comprehensive documentation at multiple levels. Starting with code-level docstrings, the LLM generates descriptions for all public functions, classes, and modules. These docstrings are used to generate API reference documentation automatically. User-facing documentation includes quickstart guides, tutorials, and architecture overviews. The LLM can extract patterns from code to explain complex designs.

**Purpose**: Create multi-level documentation from docstrings through user guides.

**Usage**: Phase 8 chapter - shows how LLMs can generate consistent, comprehensive documentation.

```mermaid
graph LR
    subgraph ROW1["<b>CONTENT GENERATION</b>"]
        Input([<b>CODE</b>]) --> Docstrings[<b>LLM: Generate Docstrings</b>]
        Docstrings --> Review1{<b>Complete?</b>}
        Review1 -->|<b>No</b>| Docstrings
        Review1 -->|<b>Yes</b>| APIRef[<b>Generate API Reference</b>]
        APIRef --> Architecture[<b>Write Architecture Doc</b>]
        Architecture --> Quickstart[<b>Write Quickstart</b>]
    end

    subgraph ROW2["<b>REVIEW AND BUILD</b>"]
        Tutorial[<b>Write Tutorial</b>] --> Examples[<b>Add Examples</b>]
        Examples --> Review2{<b>Complete?</b>}
        Review2 -->|<b>No</b>| Architecture
        Review2 -->|<b>Yes</b>| Build[<b>Build Docs</b>]
        Build --> Preview[<b>Preview Output</b>]
        Preview --> Quality{<b>Good Quality?</b>}
        Quality -->|<b>No</b>| Docstrings
        Quality -->|<b>Yes</b>| Output([<b>DOCUMENTATION COMPLETE</b>])
    end

    Quickstart --> Tutorial

    style Input fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style Output fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style Review1 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Review2 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Quality fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Docstrings fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style APIRef fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Architecture fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Quickstart fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Tutorial fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Examples fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Build fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
    style Preview fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
```

---

### 13. Phase 9: Docker Containerization

**Summary**: Phase 9 packages the application in a Docker container for consistent deployment. The process starts with creating a Dockerfile that defines the container image. The image uses multi-stage builds to minimize size - build dependencies are separate from runtime dependencies. The LLM helps optimize layer caching and choose base images. Security scanning with Trivy checks for vulnerabilities before deployment. Smoke tests verify the container works correctly. The final image is tagged with version numbers and pushed to a registry.

**Purpose**: Create production-ready Docker containers with security validation.

**Usage**: Phase 9 chapter - demonstrates containerization best practices and security scanning.

```mermaid
graph LR
    subgraph BUILD["<b>BUILD PHASE</b>"]
        direction TB
        Input([<b>CODE + TESTS</b>]) --> Dockerfile[<b>Create Dockerfile</b>]
        Dockerfile --> Optimize[<b>Optimize Layers</b>]
        Optimize --> BuildImg[<b>Build Image</b>]
        BuildImg --> Tag[<b>Tag Image</b>]
    end

    subgraph SECURITY["<b>SECURITY PHASE</b>"]
        direction TB
        Scan[<b>Run Trivy Scan</b>] --> Vulns{<b>Vulnerabilities?</b>}
        Vulns -->|<b>Critical/High</b>| Fix[<b>Fix Issues</b>]
        Fix --> BuildImg
        Vulns -->|<b>Acceptable</b>| Smoke[<b>Run Smoke Tests</b>]
    end

    subgraph DEPLOY["<b>DEPLOYMENT PHASE</b>"]
        direction TB
        TestsPass{<b>Tests Pass?</b>} -->|<b>No</b>| Fix
        TestsPass -->|<b>Yes</b>| Push[<b>Push to Registry</b>]
        Push --> Output([<b>CONTAINER DEPLOYED</b>])
    end

    Tag --> Scan
    Smoke --> TestsPass

    style Input fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style Output fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style Vulns fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style TestsPass fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Dockerfile fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style Optimize fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style BuildImg fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Tag fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Scan fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
    style Fix fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style Smoke fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Push fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
```

---

### 14. Phase 10: External Services Integration

**Summary**: Phase 10 integrates external quality and deployment services. SonarCloud provides code quality analysis with quality gates. CodeCov tracks coverage trends. GitHub Container Registry (GHCR) hosts Docker images. Each service requires setup - creating accounts, generating tokens, adding secrets to GitHub, and configuring workflows. The LLM helps troubleshoot authentication issues and explains configuration options. Services coordinate through the CI pipeline with graceful degradation.

**Purpose**: Integrate SonarCloud, CodeCov, GHCR, and other external services with CI pipeline.

**Usage**: Phase 10 chapter - step-by-step external service setup with troubleshooting guidance.

```mermaid
graph TB
    subgraph ROW1["<b>SONARCLOUD SETUP</b>"]
        direction TB
        Input([<b>WORKING CI</b>]) --> SonarAcct[<b>Create Account</b>]
        SonarAcct --> SonarToken[<b>Generate Token</b>]
        SonarToken --> SonarSecret[<b>Add GitHub Secret</b>]
        SonarSecret --> SonarConfig[<b>Configure Workflow</b>]
    end

    subgraph ROW2["<b>CODECOV SETUP</b>"]
        direction TB
        CodeCovAcct[<b>Create Account</b>] --> CodeCovToken[<b>Generate Token</b>]
        CodeCovToken --> CodeCovSecret[<b>Add GitHub Secret</b>]
        CodeCovSecret --> CodeCovConfig[<b>Configure Upload</b>]
    end

    subgraph ROW3["<b>GHCR SETUP</b>"]
        direction TB
        GHCRPerms[<b>Configure Permissions</b>] --> GHCRPush[<b>Configure Push</b>]
        GHCRPush --> Test[<b>Test Integration</b>]
        Test --> Results{<b>Working?</b>}
        Results -->|<b>Fail</b>| Debug[<b>Debug Auth</b>]
        Debug --> Test
        Results -->|<b>Pass</b>| Output([<b>SERVICES INTEGRATED</b>])
    end

    style Input fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style Output fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style Results fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style SonarAcct fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style SonarToken fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style SonarSecret fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style SonarConfig fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style CodeCovAcct fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style CodeCovToken fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style CodeCovSecret fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style CodeCovConfig fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style GHCRPerms fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
    style GHCRPush fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
    style Test fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style Debug fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
```

---

### 15. Phase 11: Publishing and Release

**Summary**: Phase 11 handles release preparation and deployment. The process starts with version bumping in pyproject.toml, which propagates through Docker images and package metadata. A comprehensive changelog documents all changes since the last release. Git tags mark release points, triggering deployment workflows. The CI pipeline builds distribution packages, runs final quality checks, creates Docker images with version tags, and pushes to registries (PyPI, GHCR). Release notes are generated from the changelog.

**Purpose**: Prepare and execute releases with versioning, tagging, and deployment automation.

**Usage**: Phase 11 chapter - demonstrates complete release workflow from version bump to deployment.

```mermaid
graph TB
    subgraph ROW1["<b>PREPARATION</b>"]
        direction LR
        A1([<b>COMPLETED FEATURE</b>]) --> A2[<b>Bump Version</b>]
        A2 --> A3[<b>Update Changelog</b>]
        A3 --> A4[<b>Create Git Tag</b>]
    end

    subgraph ROW2["<b>BUILD</b>"]
        direction LR
        B1[<b>Push Tag</b>] --> B2[<b>Build Packages</b>]
        B2 --> B3[<b>Quality Checks</b>]
        B3 --> B4[<b>Build Docker</b>]
    end

    subgraph ROW3["<b>PUBLISH</b>"]
        direction LR
        C1[<b>Push PyPI</b>] --> C2[<b>Push GHCR</b>]
        C2 --> C3[<b>Generate Notes</b>]
        C3 --> C4[<b>Publish Release</b>]
    end

    subgraph ROW4["<b>VERIFY</b>"]
        direction LR
        D1[<b>Test Deploy</b>] --> D2[<b>Monitor</b>]
        D2 --> D3([<b>RELEASED</b>])
    end

    A4 -.-> B1
    B4 -.-> C1
    C4 -.-> D1

    style A1 fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style D3 fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style A2 fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style A3 fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style A4 fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style B1 fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style B2 fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style B3 fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style B4 fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style C1 fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
    style C2 fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
    style C3 fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style C4 fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style D1 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style D2 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000

    linkStyle 11,12,13 stroke-width:0px
```

---

## Interaction Groups

### 16. Scanning Services Interaction

**Summary**: Multiple scanning and quality services coordinate during the CI pipeline through shared data formats. Pytest generates coverage data consumed by both CodeCov and SonarCloud. Ruff and Mypy results feed into SonarCloud's quality gate. Trivy scans Docker images and uploads SARIF results to GitHub Security. This data sharing creates a comprehensive quality picture.

**Purpose**: Show coordination between scanning services through shared data formats.

**Usage**: External Services chapter - explains service integration and data flow.

```mermaid
graph LR
    subgraph SOURCES["<b>DATA SOURCES</b>"]
        direction TB
        CI([<b>CI TRIGGER</b>]) --> Pytest[<b>Run Pytest</b>]
        Pytest --> CovXML[<b>coverage.xml</b>]
        CI --> Ruff[<b>Run Ruff</b>]
        CI --> Mypy[<b>Run Mypy</b>]
        CI --> Docker[<b>Build Docker</b>]
    end

    subgraph CODECOV["<b>CODECOV FLOW</b>"]
        direction TB
        UploadCC[<b>Upload Coverage</b>] --> CCDash[<b>Dashboard</b>]
        CCDash --> PRComment[<b>PR Comment</b>]
    end

    subgraph SONAR["<b>SONARCLOUD FLOW</b>"]
        direction TB
        UploadSC[<b>Upload Results</b>] --> SCAnalysis[<b>Analysis</b>]
        SCAnalysis --> Gate{<b>Quality<br/>Gate?</b>}
        Gate -->|<b>Pass</b>| Merge[<b>Allow</b>]
        Gate -->|<b>Fail</b>| Block[<b>Block</b>]
    end

    subgraph TRIVY["<b>SECURITY FLOW</b>"]
        direction TB
        Scan[<b>Trivy Scan</b>] --> SARIF[<b>SARIF</b>]
        SARIF --> GHSec[<b>GitHub<br/>Security</b>]
    end

    CovXML --> UploadCC
    CovXML --> UploadSC
    Ruff --> UploadSC
    Mypy --> UploadSC
    Docker --> Scan

    style CI fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style Gate fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Merge fill:#065f46,stroke:#fff,stroke-width:2px,color:#fff
    style Block fill:#b91c1c,stroke:#fff,stroke-width:2px,color:#fff
    style Pytest fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style CovXML fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Ruff fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style Mypy fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style Docker fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
    style UploadCC fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style UploadSC fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Scan fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
```

---

### 17. Build & Deploy Pipeline

**Summary**: Docker build and deployment pipeline with quality gates. Extracts version from pyproject.toml, builds image, runs three Trivy scans (SARIF, table, SBOM), executes smoke tests (import, version, functionality), then pushes to GHCR. Failed steps prevent deployment.

**Purpose**: Show Docker build-to-deploy workflow with quality gates.

**Usage**: CI/CD and Publishing chapters - production container deployment.

```mermaid
graph TB
    subgraph BUILD["<b>BUILD PHASE</b>"]
        direction TB
        Trigger([<b>MAIN PUSH</b>]) --> Extract[<b>Extract Version</b>]
        Extract --> Build[<b>Build Image</b>]
        Build --> Tag[<b>Tag Image</b>]
    end

    subgraph SCAN["<b>SECURITY SCAN</b>"]
        direction TB
        Scan1[<b>Trivy: SARIF</b>] --> Scan2[<b>Trivy: Table</b>]
        Scan2 --> Scan3[<b>Trivy: SBOM</b>]
        Scan3 --> Vulns{<b>Critical?</b>}
        Vulns -->|<b>Yes</b>| Fail[<b>BLOCK</b>]
    end

    subgraph SMOKE["<b>SMOKE TESTS</b>"]
        direction TB
        Test1[<b>Import Test</b>] --> Pass1{<b>Pass?</b>}
        Pass1 -->|<b>No</b>| Fail
        Pass1 -->|<b>Yes</b>| Test2[<b>Version Test</b>]
        Test2 --> Pass2{<b>Pass?</b>}
        Pass2 -->|<b>No</b>| Fail
        Pass2 -->|<b>Yes</b>| Test3[<b>Function Test</b>]
        Test3 --> Pass3{<b>Pass?</b>}
        Pass3 -->|<b>No</b>| Fail
    end

    subgraph DEPLOY["<b>DEPLOYMENT</b>"]
        direction TB
        Login[<b>Login GHCR</b>] --> Push[<b>Push Image</b>]
        Push --> Success([<b>DEPLOYED</b>])
    end

    Tag --> Scan1
    Vulns -->|<b>No</b>| Test1
    Pass3 -->|<b>Yes</b>| Login

    style Trigger fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style Success fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style Fail fill:#b91c1c,stroke:#fff,stroke-width:2px,color:#fff
    style Vulns fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Pass1 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Pass2 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Pass3 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Extract fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style Build fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Tag fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Scan1 fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
    style Scan2 fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
    style Scan3 fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
```

---

### 18. Quality Tools Integration

**Summary**: Three-layer quality enforcement: local development (manual runs), pre-commit hooks (automatic enforcement), and CI pipeline (clean environment). Same tools (Ruff, Mypy, Pytest) at all layers with consistent configurations. Catches issues progressively earlier, reducing fix cost.

**Purpose**: Show defense-in-depth quality strategy across three layers.

**Usage**: Quality Checks and CI/CD chapters - establishes layered quality approach.

```mermaid
graph TB
    subgraph LOCAL["<b>LOCAL DEV</b>"]
        direction LR
        Dev[<b>Write Code</b>] --> ManRuff[<b>ruff check</b>]
        ManRuff --> ManMypy[<b>mypy</b>]
        ManMypy --> ManTest[<b>pytest</b>]
    end

    subgraph PRECOMMIT["<b>PRE-COMMIT</b>"]
        direction LR
        Commit[<b>git commit</b>] --> HookRuff[<b>ruff hook</b>]
        HookRuff --> HookMypy[<b>mypy hook</b>]
        HookMypy --> HookTest[<b>pytest hook</b>]
        HookTest --> Decision{<b>Pass?</b>}
        Decision -->|<b>No</b>| Block[<b>BLOCK</b>]
        Decision -->|<b>Yes</b>| Allow[<b>ALLOW</b>]
    end

    subgraph CI["<b>CI PIPELINE</b>"]
        direction LR
        Push[<b>git push</b>] --> CIRuff[<b>ruff job</b>]
        CIRuff --> CIMypy[<b>mypy job</b>]
        CIMypy --> CITest[<b>test matrix</b>]
        CITest --> CIGate{<b>Pass?</b>}
        CIGate -->|<b>No</b>| FailPR[<b>FAIL PR</b>]
        CIGate -->|<b>Yes</b>| PassPR[<b>PASS PR</b>]
    end

    ManTest --> Commit
    Allow --> Push

    style Dev fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style Decision fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style CIGate fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Block fill:#b91c1c,stroke:#fff,stroke-width:2px,color:#fff
    style FailPR fill:#b91c1c,stroke:#fff,stroke-width:2px,color:#fff
    style Allow fill:#065f46,stroke:#fff,stroke-width:2px,color:#fff
    style PassPR fill:#065f46,stroke:#fff,stroke-width:2px,color:#fff
    style ManRuff fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style ManMypy fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style ManTest fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
```

---

## New Content

### 19. Development Artifacts Map

**Summary**: Maps artifacts generated at each development phase. Planning phases (0-2) produce documents. Implementation (3-4) generates code and tests. Refinement (5-6) creates reports. Quality (7) produces tool outputs. Documentation (8) generates guides. CI/CD (9-11) produces workflow files, images, and packages.

**Purpose**: Show artifacts created at each phase and by which processes.

**Usage**: Cross-cutting reference - tracks deliverables at each stage.

```mermaid
graph LR
    subgraph PLAN["<b>PLANNING (0-2)</b>"]
        direction TB
        P0[<b>Phase 0</b>] --> A0[<b>Requirements</b>]
        P1[<b>Phase 1</b>] --> A1[<b>Spec</b>]
        P2[<b>Phase 2</b>] --> A2[<b>Plan</b>]
    end

    subgraph IMPL["<b>IMPLEMENTATION (3-4)</b>"]
        direction TB
        P3[<b>Phase 3</b>] --> A3[<b>Code Files</b>]
        P4[<b>Phase 4</b>] --> A4[<b>Test Files</b>]
        P4 --> A4b[<b>Coverage</b>]
    end

    subgraph REFINE["<b>REFINEMENT (5-6)</b>"]
        direction TB
        P5[<b>Phase 5</b>] --> A5[<b>Bug Reports</b>]
        P6[<b>Phase 6</b>] --> A6[<b>Benchmarks</b>]
    end

    subgraph QUALITY["<b>QUALITY (7)</b>"]
        direction TB
        P7[<b>Phase 7</b>] --> A7[<b>Ruff/Mypy<br/>Reports</b>]
    end

    subgraph DOCS["<b>DOCS (8)</b>"]
        direction TB
        P8[<b>Phase 8</b>] --> A8[<b>Docstrings<br/>API Docs</b>]
    end

    subgraph CICD["<b>CI/CD (9-11)</b>"]
        direction TB
        P9[<b>Phase 9</b>] --> A9[<b>Workflows<br/>SARIF</b>]
        P10[<b>Phase 10</b>] --> A10[<b>SonarCloud<br/>CodeCov</b>]
        P11[<b>Phase 11</b>] --> A11[<b>Images<br/>Packages</b>]
    end

    style A0 fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style A1 fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style A2 fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style A3 fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style A4 fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style A4b fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style A5 fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style A6 fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style A7 fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
    style A8 fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
    style A9 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style A10 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style A11 fill:#065f46,stroke:#fff,stroke-width:2px,color:#fff
```

---

### 20. Tool Category Comparison Matrix

**Summary**: Development tool categories with top alternatives. SparseTagging choices marked with ⭐. Categories include Linting (Ruff⭐), Type Checking (Mypy⭐), Testing (Pytest⭐), Coverage (pytest-cov⭐), CI/CD (GitHub Actions⭐), Quality Platforms (SonarCloud⭐), Container Tools (Docker⭐), Security Scanning (Trivy⭐), Container Registry (GHCR⭐), and Pre-commit (pre-commit⭐). Blue = local tools, Yellow = external services.

**Purpose**: Compare tool options with SparseTagging choices highlighted.

**Usage**: Tool Selection chapter - evaluate alternatives and trade-offs.

```mermaid
graph TB
    subgraph LOCAL["<b>LOCAL TOOLS</b>"]
        direction LR
        Lint[<b>LINTING</b><br/>1. Ruff ⭐<br/>2. Flake8<br/>3. Pylint]
        Type[<b>TYPE CHECK</b><br/>1. Mypy ⭐<br/>2. Pyright<br/>3. Pyre]
        Test[<b>TESTING</b><br/>1. Pytest ⭐<br/>2. unittest<br/>3. nose2]
        Cov[<b>COVERAGE</b><br/>1. pytest-cov ⭐<br/>2. coverage.py<br/>3. codecov]
        Pre[<b>PRE-COMMIT</b><br/>1. pre-commit ⭐<br/>2. husky<br/>3. hooks]
    end

    subgraph SERVICES["<b>EXTERNAL SERVICES</b>"]
        direction LR
        CICD[<b>CI/CD</b><br/>1. GH Actions ⭐<br/>2. GitLab CI<br/>3. CircleCI]
        Qual[<b>QUALITY</b><br/>1. SonarCloud ⭐<br/>2. Code Climate<br/>3. Scrutinizer]
        Cont[<b>CONTAINERS</b><br/>1. Docker ⭐<br/>2. Podman<br/>3. Buildah]
        Sec[<b>SECURITY</b><br/>1. Trivy ⭐<br/>2. Snyk<br/>3. Grype]
        Reg[<b>REGISTRY</b><br/>1. GHCR ⭐<br/>2. Docker Hub<br/>3. ECR]
    end

    style Lint fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Type fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Test fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Cov fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Pre fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style CICD fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style Qual fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style Cont fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style Sec fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style Reg fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
```

**Legend**: ⭐ = Used in SparseTagging | Blue = Local | Yellow = External

---

### 21. LLM Prompting Best Practices

**Summary**: Visual synthesis of effective prompting patterns. Golden template: Context (current state, why) → Request (specific action) → Constraints (requirements) → Guidance (boundaries) → Collaboration (ask questions). Success patterns include specificity, structure, context, and permission. Anti-patterns include vagueness, no context, early implementation, assuming memory, and too many changes.

**Purpose**: Visualize effective LLM prompting patterns and anti-patterns.

**Usage**: Prompting chapter - teaches effective prompt crafting.

```mermaid
graph LR
    subgraph TEMPLATE["<b>GOLDEN TEMPLATE</b>"]
        direction TB
        Context[<b>CONTEXT</b><br/>Current state<br/>Why needed]
        Context --> Request[<b>REQUEST</b><br/>Specific action<br/>Clear scope]
        Request --> Constraints[<b>CONSTRAINTS</b><br/>Requirements<br/>Specific values]
        Constraints --> Guidance[<b>GUIDANCE</b><br/>Boundaries<br/>Exclusions]
        Guidance --> Collab[<b>COLLABORATE</b><br/>Ask questions<br/>Iterate]
    end

    subgraph SUCCESS["<b>SUCCESS PATTERNS</b>"]
        direction TB
        S1[<b>✅ Specificity</b><br/>5min not short]
        S2[<b>✅ Structure</b><br/>Numbered lists]
        S3[<b>✅ Context</b><br/>Explain why]
        S4[<b>✅ Permission</b><br/>Invite questions]
    end

    subgraph ANTI["<b>ANTI-PATTERNS</b>"]
        direction TB
        A1[<b>❌ Vague</b><br/>Make it better]
        A2[<b>❌ No Context</b><br/>Fix line 690]
        A3[<b>❌ Too Early</b><br/>Use library X]
        A4[<b>❌ Assume Memory</b><br/>Do that thing]
    end

    Collab --> Results{<b>Good?</b>}
    Results -->|<b>Yes</b>| Success([<b>ZERO FAILURES</b>])
    Results -->|<b>No</b>| Context

    style Context fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Request fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Constraints fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Guidance fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Collab fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Results fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Success fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style S1 fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style S2 fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style S3 fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style S4 fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style A1 fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
    style A2 fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
    style A3 fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
    style A4 fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
```

---

### 22. Claude Code Cheat Sheet

**Summary**: Quick reference for Claude Code keyboard shortcuts, slash commands, and workflow patterns.

**Purpose**: Quick reference for Claude Code features.

**Usage**: Getting Started and throughout - efficient Claude Code usage.

| **Category** | **Item** | **Description** |
|---|---|---|
| **Essential Shortcuts** | Tab | Accept suggestion |
| | Shift+Tab | Toggle auto-accept |
| | Ctrl+R | Show full output |
| | Ctrl+B | Background task |
| | Ctrl+O | Transcript mode |
| | Ctrl+C | Interrupt |
| | Ctrl+Z | Undo input |
| | Alt+T | Toggle thinking |
| **Slash Commands** | /plan | Enter plan mode |
| | /commit | Create commit |
| | /pr | Create pull request |
| | /context | Show context usage |
| | /model | Switch model |
| | /permissions | Manage tool access |
| | /resume | Resume session |
| | /clear | Clear conversation |
| **@-Mention Features** | @file.py | Reference file |
| | @folder/ | Reference directory |
| | @agent | Invoke custom agent |
| **Workflow Patterns** | Plan First | Use /plan for complex changes |
| | Background Tasks | Ctrl+B for dev servers |
| | Iterative Refinement | Give feedback on results |
| | Context Management | Check /context regularly |
| | Permission Management | Set per-project tool access |

---

### 23. ChatGPT Codex Cheat Sheet

**Summary**: Quick reference for ChatGPT integration patterns and when to use ChatGPT vs Claude Code.

**Purpose**: Quick reference for ChatGPT usage patterns.

**Usage**: Tool Selection chapter - when to use ChatGPT vs Claude Code.

| **Category** | **Pattern** | **Description** |
|---|---|---|
| **ChatGPT Strengths** | Algorithm Design | Design data structures and algorithms |
| | Code Explanation | Understand complex code |
| | Research Tasks | Compare approaches and libraries |
| | Boilerplate Generation | Generate templates and scaffolding |
| | Refactoring Ideas | Suggest improvements and patterns |
| **Effective Patterns** | Provide Context | Share relevant files and dependencies |
| | Specify Format | Code only, markdown, step-by-step |
| | Break Down Tasks | Smaller focused prompts |
| | Give Examples | Show desired output format |
| | Iterate | Refine responses through dialogue |
| **Best Use Cases** | Research Phase | Explore options before implementation |
| | Algorithm Help | Design efficient solutions |
| | Code Review | Get feedback on approach |
| | Documentation | Generate explanations and guides |
| **Integration with Claude** | ChatGPT: Research | Claude Code: Implement |
| | ChatGPT: Design | Claude Code: Integrate |
| | ChatGPT: Explain | Claude Code: Refactor |
| | ChatGPT: Explore | Claude Code: Execute |

---

### 24. CI Pipeline Evolution

**Summary**: Progressive enhancement of ci.yml from basic build to production pipeline. Stage 1: Build and test. Stage 2: Test matrix. Stage 3: Save artifacts. Stage 4: Security scanning. Stage 5: Docker smoke tests. Stage 6: External services. Stage 7: Result summary. Stage 8: Graceful degradation. SparseTagging evolved through these stages over 66 PRs.

**Purpose**: Show progressive CI improvement from basic to production-grade.

**Usage**: CI/CD chapter - demonstrates incremental improvement approach.

```mermaid
graph LR
    subgraph BASIC["<b>BASIC (1-3)</b>"]
        direction TB
        S1[<b>Stage 1</b><br/>Build<br/>Test]
        S1 --> S2[<b>Stage 2</b><br/>Test Matrix<br/>Multi-OS]
        S2 --> S3[<b>Stage 3</b><br/>Save Artifacts<br/>Results]
    end

    subgraph SECURE["<b>SECURITY (4-5)</b>"]
        direction TB
        S4[<b>Stage 4</b><br/>Trivy Scan<br/>SARIF Upload]
        S4 --> S5[<b>Stage 5</b><br/>Docker Smoke<br/>Tests]
    end

    subgraph SERVICES["<b>SERVICES (6-7)</b>"]
        direction TB
        S6[<b>Stage 6</b><br/>SonarCloud<br/>CodeCov]
        S6 --> S7[<b>Stage 7</b><br/>Result Summary<br/>README]
    end

    subgraph ROBUST["<b>ROBUST (8)</b>"]
        direction TB
        S8[<b>Stage 8</b><br/>Graceful Degrade<br/>Continue on Error]
        S8 --> Prod([<b>PRODUCTION<br/>READY</b>])
    end

    S3 --> S4
    S5 --> S6
    S7 --> S8

    style S1 fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
    style S2 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style S3 fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style S4 fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style S5 fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style S6 fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style S7 fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
    style S8 fill:#d4edda,stroke:#fff,stroke-width:2px,color:#000
    style Prod fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
```

---

### 25. Iterative Development Reality

**Summary**: Non-linear reality of software development with multiple concurrent work streams, frequent backtracking, and iterative refinement. SparseTagging had 66 PRs demonstrating this reality. Features reveal bugs, performance issues trigger optimization, new features break old ones, quality issues require refactoring. This is normal and expected.

**Purpose**: Show realistic non-linear development with multiple refinement cycles.

**Usage**: Introduction - sets realistic expectations about development process.

```mermaid
graph TB
    subgraph WEEK1["<b>WEEK 1</b>"]
        direction LR
        S1([<b>PROJECT START</b>]) --> F1[<b>Feature 1</b>]
        F1 --> B1[<b>Bug Found</b>]
        B1 --> FIX1[<b>Fix Bug</b>]
        FIX1 --> P1[<b>Perf Issue</b>]
        P1 --> OPT1[<b>Optimize</b>]
    end

    subgraph WEEK2["<b>WEEK 2</b>"]
        direction LR
        F2[<b>Feature 2</b>] --> B2[<b>Breaks F1</b>]
        B2 --> REF[<b>Refactor Both</b>]
        REF --> CI[<b>Setup CI</b>]
        CI --> B3[<b>CI Fails</b>]
        B3 --> FIX2[<b>Fix CI</b>]
    end

    subgraph WEEK3["<b>WEEK 3</b>"]
        direction LR
        SC[<b>Add SonarCloud</b>] --> Q1[<b>Quality Issues</b>]
        Q1 --> FIXQ[<b>Fix Quality</b>]
        FIXQ --> F3[<b>Feature 3</b>]
        F3 --> EDGE[<b>Edge Case</b>]
        EDGE --> TESTS[<b>Add Tests</b>]
    end

    subgraph WEEK4["<b>WEEK 4</b>"]
        direction LR
        DOCS[<b>Write Docs</b>] --> API[<b>API Issue</b>]
        API --> REDES[<b>Redesign API</b>]
        REDES --> F4[<b>Feature 4</b>]
        F4 --> P2[<b>Perf Regression</b>]
        P2 --> OPT2[<b>Re-Optimize</b>]
        OPT2 --> END([<b>66 PRS LATER</b>])
    end

    OPT1 -.-> F2
    FIX2 -.-> SC
    TESTS -.-> DOCS

    style S1 fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style END fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style B1 fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
    style B2 fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
    style B3 fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
    style P1 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style P2 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Q1 fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style API fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000

    linkStyle 21,22,23 stroke-width:0px
```

**Note**: Each box could expand into multiple PRs. This is normal, not failure.

---

### 26. Configuration Consolidation Map

**Summary**: Unified view of all configuration sources. Single source of truth: pyproject.toml (version, dependencies, metadata). Secrets flow from external services through GitHub Secrets into CI workflow. Environment variables defined in ci.yml. Configuration files include sonar-project.properties, .codecov.yml, mypy.ini, .pre-commit-config.yaml. Workflow ci.yml orchestrates everything.

**Purpose**: Unified view of all configuration sources and their relationships.

**Usage**: Configuration chapter - understand settings sources and interactions.

```mermaid
graph TB
    subgraph TRUTH["<b>SOURCE OF TRUTH</b>"]
        direction TB
        PyProj[<b>pyproject.toml</b><br/>version: 2.4.1<br/>dependencies<br/>metadata]
    end

    subgraph SECRETS["<b>SECRETS</b>"]
        direction TB
        GHSecrets[<b>GitHub Secrets</b><br/>SONAR_TOKEN<br/>CODECOV_TOKEN<br/>GITHUB_TOKEN]
    end

    subgraph ENV["<b>ENVIRONMENT</b>"]
        direction TB
        EnvVars[<b>ci.yml env:</b><br/>SOURCE_DIR: src<br/>TEST_DIR: tests<br/>COVERAGE: 85<br/>PYTHON: 3.11]
    end

    subgraph CONFIG["<b>CONFIG FILES</b>"]
        direction TB
        Sonar[<b>sonar-project</b><br/>.properties]
        CodeCov[<b>.codecov.yml</b>]
        Mypy[<b>mypy.ini</b>]
        PreCom[<b>.pre-commit-</b><br/>config.yaml]
    end

    subgraph ORCH["<b>ORCHESTRATION</b>"]
        direction TB
        Workflow[<b>ci.yml</b><br/>Reads all configs<br/>Coordinates execution]
    end

    subgraph BUILD["<b>BUILD</b>"]
        direction TB
        Docker[<b>Dockerfile</b><br/>APP_VERSION arg<br/>Base image]
    end

    PyProj --> Workflow
    PyProj --> Docker
    GHSecrets --> Workflow
    EnvVars --> Workflow
    Sonar --> Workflow
    CodeCov --> Workflow
    Mypy --> Workflow
    PreCom --> Workflow
    Workflow --> BuildProc([<b>BUILD PROCESS</b>])
    Docker --> BuildProc

    style PyProj fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style GHSecrets fill:#fecaca,stroke:#fff,stroke-width:2px,color:#000
    style EnvVars fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Workflow fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style BuildProc fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
```

**Key Insight**: Version in pyproject.toml flows through entire system.

---

## Documentation Consolidations

### 27. Troubleshooting Decision Trees

**Summary**: Consolidated troubleshooting guide combining scattered debugging information into decision trees. Starting with symptom identification (test failures, CI failures, memory issues, slow queries, type errors), the tree guides users through systematic diagnosis with actionable solutions.

**Purpose**: Systematic diagnostic approach for common issues.

**Usage**: Troubleshooting chapter - provides diagnostic decision trees.

```mermaid
graph TB
    Start{<b>SYMPTOM?</b>} --> TestFail[<b>Tests Failing</b>]
    Start --> CIFail[<b>CI Failing</b>]
    Start --> Memory[<b>High Memory</b>]
    Start --> Slow[<b>Slow Queries</b>]
    Start --> TypeError[<b>Type Errors</b>]

    TestFail --> Platform{<b>Local<br/>or CI?</b>}
    Platform -->|<b>CI Only</b>| Matrix[<b>Check matrix job</b><br/>Python version<br/>OS platform]
    Platform -->|<b>Both</b>| Deps[<b>Check deps<br/>versions</b>]

    CIFail --> WhichJob{<b>Which<br/>job?</b>}
    WhichJob -->|<b>Quality</b>| Ruff[<b>Run ruff<br/>Fix issues</b>]
    WhichJob -->|<b>Test</b>| Coverage[<b>Check coverage<br/>Add tests</b>]
    WhichJob -->|<b>SonarCloud</b>| Token[<b>Check token<br/>Verify config</b>]

    Memory --> CheckCache[<b>Check cache<br/>stats</b>]
    CheckCache --> CacheBig{<b>Cache<br/>>8MB?</b>}
    CacheBig -->|<b>Yes</b>| ClearCache[<b>Clear cache<br/>Reduce limits</b>]
    CacheBig -->|<b>No</b>| Indices[<b>Optimize<br/>indices dtype</b>]

    Slow --> Cached{<b>Cache<br/>enabled?</b>}
    Cached -->|<b>No</b>| EnableCache[<b>Enable caching</b>]
    Cached -->|<b>Yes</b>| HitRate{<b>Hit rate<br/>>60%?</b>}
    HitRate -->|<b>No</b>| QueryPattern[<b>Analyze query<br/>patterns</b>]

    TypeError --> RunMypy[<b>Run mypy</b>]
    RunMypy --> MypyErrors{<b>Errors?</b>}
    MypyErrors -->|<b>Yes</b>| FixTypes[<b>Add type hints<br/>Fix errors</b>]

    style Start fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style Platform fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style WhichJob fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style CacheBig fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Cached fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style HitRate fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style MypyErrors fill:#fed7aa,stroke:#fff,stroke-width:2px,color:#000
    style Matrix fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style Deps fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style Ruff fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Coverage fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Token fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style ClearCache fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style EnableCache fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style FixTypes fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
```

---

### 28. Service Setup Dependencies

**Summary**: Prerequisite chain for setting up external services. Foundation is GitHub account. Creating repository enables GitHub Actions. SonarCloud requires account creation, organization setup, project creation, and token generation. CodeCov requires account and repository connection. GHCR uses GitHub but needs permissions. Dependabot needs enabling.

**Purpose**: Show prerequisite chain for external service setup.

**Usage**: External Services chapter - understand setup order and dependencies.

```mermaid
graph TB
    Start([<b>DEVELOPER</b>]) --> GH[<b>1. GitHub Account</b>]
    GH --> Repo[<b>2. Create Repository</b>]
    Repo --> Actions[<b>3. GitHub Actions<br/>Automatic</b>]

    Repo --> SC1[<b>4a. SonarCloud Account</b>]
    SC1 --> SC2[<b>4b. Link GitHub</b>]
    SC2 --> SC3[<b>4c. Create Org</b>]
    SC3 --> SC4[<b>4d. Create Project</b>]
    SC4 --> SC5[<b>4e. Generate Token</b>]
    SC5 --> SCSecret[<b>4f. Add Secret</b>]

    Repo --> CC1[<b>5a. CodeCov Account</b>]
    CC1 --> CC2[<b>5b. Connect Repo</b>]
    CC2 --> CC3[<b>5c. Copy Token</b>]
    CC3 --> CCSecret[<b>5d. Add Secret</b>]

    Repo --> GHC1[<b>6a. GHCR Access<br/>Automatic</b>]
    GHC1 --> GHC2[<b>6b. Configure Perms</b>]
    GHC2 --> GHC3[<b>6c. Enable Write</b>]

    Repo --> Dep1[<b>7a. Enable Dependabot</b>]
    Dep1 --> Dep2[<b>7b. Configure YAML</b>]

    SCSecret --> Config[<b>8. Configure<br/>Workflows</b>]
    CCSecret --> Config
    GHC3 --> Config
    Dep2 --> Config

    Config --> Test[<b>9. Test Integration</b>]
    Test --> Done([<b>ALL SERVICES<br/>INTEGRATED</b>])

    style Start fill:#0e7490,stroke:#fff,stroke-width:3px,color:#fff
    style Done fill:#065f46,stroke:#fff,stroke-width:3px,color:#fff
    style GH fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Repo fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style Actions fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style SCSecret fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style CCSecret fill:#fef3c7,stroke:#fff,stroke-width:2px,color:#000
    style Config fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
```

**Critical Path**: GitHub → Repository → Individual Services → Secrets → Workflow → Test

---

### 29. Version/Release Propagation

**Summary**: How a single version number in pyproject.toml propagates through the entire system. Version 2.4.1 in pyproject.toml becomes Docker build arg, image tag, git tag, PyPI release version, and appears in changelog and release notes. Single source of truth prevents version mismatches.

**Purpose**: Trace version from pyproject.toml through entire release process.

**Usage**: Publishing chapter - demonstrates version management best practices.

```mermaid
graph TB
    Dev[<b>Developer Edits<br/>pyproject.toml</b>] --> Version[<b>version = '2.4.1'</b>]
    Version --> Git[<b>Git Commit & Push</b>]
    Git --> CI[<b>CI Triggered</b>]

    CI --> Extract[<b>extract-version.py</b>]
    Extract --> CIVar[<b>VERSION=2.4.1</b>]

    CIVar --> Docker[<b>Docker Build</b>]
    Docker --> BuildArg[<b>APP_VERSION=2.4.1</b>]
    BuildArg --> ImageEnv[<b>Image Env Var</b>]

    CIVar --> Tag1[<b>Tag: 2.4.1</b>]
    CIVar --> Tag2[<b>Tag: latest</b>]

    Version --> GitTag[<b>Git Tag: v2.4.1</b>]
    GitTag --> Release[<b>GitHub Release</b>]

    Version --> PackageMeta[<b>__version__</b>]
    PackageMeta --> PyPI[<b>PyPI: 2.4.1</b>]

    Version --> Changelog[<b>CHANGELOG.md</b>]
    Changelog --> ReleaseNotes[<b>Release Notes</b>]

    Tag1 --> GHCR[<b>Push to GHCR</b>]
    Tag2 --> GHCR

    style Version fill:#fef3c7,stroke:#fff,stroke-width:3px,color:#000
    style CIVar fill:#dbeafe,stroke:#fff,stroke-width:2px,color:#000
    style GitTag fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style PyPI fill:#065f46,stroke:#fff,stroke-width:2px,color:#fff
    style GHCR fill:#065f46,stroke:#fff,stroke-width:2px,color:#fff
    style Extract fill:#e0e7ff,stroke:#fff,stroke-width:2px,color:#000
    style BuildArg fill:#e5e7eb,stroke:#fff,stroke-width:2px,color:#000
```

**Key Principle**: Single source of truth in pyproject.toml - change once, propagates everywhere.

---

### 30. Quality Metrics Dashboard

**Summary**: Unified dashboard consolidating quality metrics from all sources. Security: Vulnerabilities (0 Critical, 0 High, A rating). Reliability: 0 bugs, A rating. Maintainability: 12 code smells, 0.3% tech debt, max cognitive complexity 12, A rating. Coverage: 88% line, 82% branch, 92% new code. Performance: 0.19ms uncached, 0.009ms cached, 95% memory savings, 65% cache hit rate. Quality: 0.8% duplication, max cyclomatic complexity 8. Overall: 9/10 metrics meeting targets.

**Purpose**: Unified view of all quality metrics in single dashboard.

**Usage**: Quality Assessment chapter - track and improve project health holistically.

```mermaid
graph TB
    Dashboard[<b>QUALITY METRICS<br/>DASHBOARD</b>]

    subgraph SEC["<b>SECURITY</b>"]
        direction TB
        Vuln[<b>Vulnerabilities</b><br/>Critical: 0<br/>High: 0<br/>Rating: A ✅]
    end

    subgraph REL["<b>RELIABILITY</b>"]
        direction TB
        Bugs[<b>Bugs</b><br/>Count: 0<br/>Rating: A ✅]
    end

    subgraph MAINT["<b>MAINTAINABILITY</b>"]
        direction TB
        Smells[<b>Code Smells: 12</b><br/>Tech Debt: 0.3%<br/>Cognitive: ≤15<br/>Rating: A ✅]
    end

    subgraph COV["<b>COVERAGE</b>"]
        direction TB
        LineCov[<b>Line: 88%</b><br/>Branch: 82%<br/>New: 92%<br/>Target: ≥85% ✅]
    end

    subgraph PERF["<b>PERFORMANCE</b>"]
        direction TB
        QueryTime[<b>Query Time</b><br/>Uncached: 0.19ms<br/>Cached: 0.009ms<br/>Savings: 95% ✅]
    end

    subgraph QUAL["<b>QUALITY</b>"]
        direction TB
        Dup[<b>Duplication: 0.8%</b><br/>Cyclomatic: ≤8<br/>Target: ≤3% ✅]
    end

    Dashboard --> Vuln
    Dashboard --> Bugs
    Dashboard --> Smells
    Dashboard --> LineCov
    Dashboard --> QueryTime
    Dashboard --> Dup

    style Dashboard fill:#fef3c7,stroke:#fff,stroke-width:3px,color:#000
    style Vuln fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Bugs fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Smells fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style LineCov fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style QueryTime fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
    style Dup fill:#d1fae5,stroke:#fff,stroke-width:2px,color:#000
```

**Overall Health**: 9/10 metrics meeting targets - Production-Ready Quality ✅

---
