
---

### 5. `docs/FRAMEWORK.md`

```markdown
# Human-AI Collaborative Batch Processing Framework

## "Review-Generate Separation" Pattern

An efficient collaboration model: **"Humans define the rules, AI produces the output; Humans review the sample, AI mass-produces the rest."**

### Division of Labor

- **Human**: Defines "what to do and how to do it," judges "whether it's done well," and revises instructions when necessary.
- **LLM (or Agent)**: Produces "one sample for human review first," and once approved, "continuously executes the remaining tasks following that same pattern."

---

## Workflow State Machine



---

## Roles and Responsibilities

### 🧑 Human's Job (Three Things)

1. **Clearly define "what to do and how to work"** — Write or revise the initial prompt with task requirements, format, style, and constraints.
2. **Review the "first output"** — The LLM generates a sample first. You evaluate it: satisfied → trigger batch production; not satisfied → rewrite the prompt.
3. **Final acceptance** — Spot-check batch results. If quality issues arise, return to step 1.

> **Key Principle**: Humans do not directly modify the model's output, but modify the "instructions," letting the model adjust itself.

### 🤖 LLM / Agent's Job (Also Three Things)

1. **Strictly generate one sample per current instruction** — No shortcuts.
2. **Upon "satisfied" signal, enter continuous execution mode** — Loop to generate the remaining target quantity.
3. **Structured output and error handling** — Auto-retry or log exceptions to ensure complete deliverables.

---

## Core Components

| Module | Function |
|--------|----------|
| **Instruction Editor** | Human writes and revises task prompts |
| **Single Sample Generator** | Calls the LLM to generate exactly 1 complete output |
| **Review Panel** | Displays sample with "Satisfied/Not Satisfied" controls |
| **Instruction Versioning** | Saves each prompt revision for rollback |
| **Batch Execution Engine** | Loops LLM calls for batch generation with retry logic |
| **Result Collector** | Compiles all outputs into a final deliverable |

---

## Example: Generating 100 Product Copy Highlights

**Step 1**: Human writes initial prompt.

**Step 2**: LLM generates one sample.

**Step 3**: Human reviews — tone not lively enough. **Rewrites prompt** (not the output).

**Step 4**: Model regenerates sample with revised instruction.

**Step 5**: Human satisfied, clicks "Approve, batch generate remaining 99."

**Step 6**: Agent auto-loops, producing 99 more. Human receives all 100. Task complete.

---

## Technical Implementation

```python
# Pseudocode for batch execution engine
def batch_generate(instruction, sample_approved, total_needed):
    results = []
    for i in range(total_needed - 1):
        result = call_llm(instruction)
        results.append(result)
    return results


For complex tasks, wrap the framework as a state machine Agent using tools like LangGraph:

human_input → generate_sample → human_review → [loop back or batch_run] → finish

In One Sentence
You set the standards and review the sample; the model produces the sample and runs the batch — neither oversteps, maximizing efficiency.