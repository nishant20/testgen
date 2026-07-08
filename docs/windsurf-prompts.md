# Windsurf extraction prompts

These two prompts let you recreate your Dell AI test-agent as a clean, public
project **without copying any company code or IP**. Prompt 1 runs in Windsurf on
your work laptop and produces an architecture-only spec (no source, no internal
URLs/credentials/class names). Prompt 2 feeds that spec to Claude on your
personal laptop to regenerate a clean implementation.

> Note: `testgen` (this repo) is already the clean, general-purpose framing of
> that agent. Its planned **source-code input adapter** is the "read the
> automation framework" step, and a **qTest-style test-management exporter** is
> the "push + map" step. Run Prompt 1 when you want the eventual source-code
> adapter to faithfully mirror what you actually built — paste the spec and we'll
> build that adapter to match.

---

## PROMPT 1 — run in Windsurf on your work laptop

```
Analyze this codebase and generate a detailed technical specification document.
Do not include any actual source code, internal URLs, credentials, company-specific
class names, package names, or proprietary implementation details.

The spec should include:

1. ARCHITECTURE OVERVIEW
   - High-level component diagram (described in text)
   - How data flows through the system end to end
   - Key design decisions and why they were made

2. AGENT WORKFLOW
   - Step by step description of what the agent does
   - How it reads and interprets the automation framework code
   - How it understands test data and test structure
   - How it generates manual test cases (logic, rules, format)
   - How it maps test cases to test plans
   - How it triggers execution

3. COMPONENT BREAKDOWN
   - List each major component/module
   - What it does (not how it's coded)
   - Its inputs and outputs
   - Its dependencies

4. LANGCHAIN SPECIFICS
   - Which LangChain components are used (chains, agents, tools, memory etc.)
   - How the LLM is prompted at each stage
   - How context from the codebase is passed to the LLM

5. TEST MANAGEMENT INTEGRATION
   - What API operations are performed (create, map, execute etc.)
   - The data structures passed to and from the test management system
   - How execution results are handled

6. CONFIGURATION & ENVIRONMENT
   - All configuration parameters needed (as generic names, not values)
   - What needs to be environment variables
   - Any external dependencies or services required

7. ERROR HANDLING & EDGE CASES
   - How the agent handles ambiguous or incomplete code
   - Retry logic or fallback behaviour
   - Known limitations

8. SAMPLE INPUT/OUTPUT
   - Describe (not copy) what a typical input framework structure looks like
   - Describe what a generated test case looks like (format, fields, structure)
   - Describe what the execution trigger payload looks like

Keep everything generic and architecture-focused.
The goal is a spec that could be used to rebuild this system from scratch
on a different codebase without any reference to the original implementation.
```

---

## PROMPT 2 — paste to Claude along with the spec output

```
I have a technical spec for an AI-powered test automation agent I built.
I want you to rebuild it from scratch as a clean, open-source,
portfolio-quality project.

Here is the spec:
[PASTE SPEC HERE]

Please build the following:

1. THE AGENT
   - Implement in Python using LangChain
   - Use environment variables for all configuration (API keys, URLs, model name)
   - Make the test management integration pluggable — default implementation
     should target a generic REST-based test management API (modelled on qTest
     but not specific to it)
   - Include clear inline comments explaining what each part does
   - Include a requirements.txt

2. SAMPLE FRAMEWORK
   - Create a small but realistic sample Selenium/Java test framework
     that the agent can be run against
   - Should include: page objects, test classes, test data files,
     at least 10 test methods across 3-4 test classes
   - Generic e-commerce or login scenario is fine

3. PROJECT STRUCTURE
   /agent
   /sample-framework
   /output-example   (example of what the agent generates, as static files)
   /docs             (architecture diagram described in Mermaid, usage guide)
   README.md

4. README
   - What it does and why it's useful
   - Architecture overview with Mermaid diagram
   - Prerequisites and setup instructions
   - How to run against the sample framework
   - How to point it at a real framework
   - Configuration reference

Make it clean, well-documented, and impressive as a portfolio piece.
Prioritise clarity and reusability over complexity.
```
