
In One Sentence
You set the standards and review the sample; the model produces the sample and runs the batch — neither oversteps, maximizing efficiency.

### 6. `run_engine.py`

(Use the same core engine from before, but with placeholder API key and English comments)

```python
"""
PromptMill — HumanLoopBatchEngine
=================================================
Core engine implementing the "Review-Generate Separation" pattern.

Usage:
    python run_engine.py

Configure your API key below before first use.
"""
import json
from enum import Enum
from typing import Callable, List, Optional
import requests

# ==================== CONFIGURATION ====================
DEEPSEEK_API_KEY = "sk-your-api-key-here"   # <-- REPLACE WITH YOUR KEY
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL_NAME = "deepseek-chat"
TOTAL_COUNT = 10

# ==================== STATES ====================
class EngineState(Enum):
    AWAIT_INSTRUCTION = "await_instruction"
    GENERATING_SAMPLE = "generating_sample"
    AWAIT_REVIEW = "await_review"
    BATCH_RUNNING = "batch_running"
    COMPLETED = "completed"
    ERROR = "error"

class EngineError(Exception):
    pass

# ==================== ENGINE ====================
class HumanLoopBatchEngine:
    """Human-in-the-loop batch generation engine."""

    def __init__(
        self,
        llm_call_func: Callable[[str], str],
        total_count: int = 100,
        on_sample_ready: Optional[Callable] = None,
        on_review_needed: Optional[Callable] = None,
        on_batch_progress: Optional[Callable] = None,
    ):
        self.llm = llm_call_func
        self.total = total_count
        self.on_sample_ready = on_sample_ready or (lambda s: print(f"\n[Sample] {s}"))
        self.on_review_needed = on_review_needed or (lambda: self._default_review())
        self.on_batch_progress = on_batch_progress or (lambda done, total: print(f"Progress: {done}/{total}"))
        self.state = EngineState.AWAIT_INSTRUCTION
        self.instruction = ""
        self.instruction_versions = []
        self.current_sample = None
        self.results = []

    def submit_instruction(self, instruction: str):
        if self.state not in [EngineState.AWAIT_INSTRUCTION, EngineState.AWAIT_REVIEW]:
            raise EngineError(f"Cannot submit instruction in state: {self.state}")
        self.instruction = instruction
        self.instruction_versions.append(instruction)
        self.state = EngineState.GENERATING_SAMPLE
        self._generate_sample()

    def _generate_sample(self):
        print("Generating sample, please wait...")
        try:
            self.current_sample = self.llm(self.instruction)
            self.state = EngineState.AWAIT_REVIEW
            self.on_sample_ready(self.current_sample)
            self.on_review_needed()
        except Exception as e:
            self.state = EngineState.ERROR
            raise EngineError(f"Sample generation failed: {e}")

    def review_sample(self, approved: bool, new_instruction: Optional[str] = None):
        if self.state != EngineState.AWAIT_REVIEW:
            raise EngineError("No sample to review")
        if approved:
            self.results.append(self.current_sample)
            self.state = EngineState.BATCH_RUNNING
            self._batch_generate()
        else:
            if new_instruction is None:
                raise ValueError("New instruction required when not satisfied")
            self.state = EngineState.AWAIT_INSTRUCTION
            self.submit_instruction(new_instruction)

    def _batch_generate(self):
        remaining = self.total - 1
        print(f"Batch generating {remaining} items...")
        for _ in range(remaining):
            try:
                result = self.llm(self.instruction)
                self.results.append(result)
                self.on_batch_progress(len(self.results), self.total)
            except Exception:
                try:
                    result = self.llm(self.instruction)
                    self.results.append(result)
                except:
                    self.results.append("[Generation failed]")
        self.state = EngineState.COMPLETED

    def get_all_results(self) -> List[str]:
        if self.state != EngineState.COMPLETED:
            raise EngineError("Batch not yet complete")
        return self.results

    def save_results(self, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

    def _default_review(self):
        print("\nReview the sample above. Satisfied? (y/n): ", end="")
        ans = input().strip().lower()
        if ans == 'y':
            self.review_sample(True)
        else:
            new_inst = input("Enter revised instruction: ").strip()
            self.review_sample(False, new_inst)

# ==================== LLM CALLER ====================
def my_llm(prompt: str) -> str:
    """Call DeepSeek API. Swap this function to use a different model."""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8
    }
    resp = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=90)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

# ==================== CLI ENTRY POINT ====================
if __name__ == "__main__":
    engine = HumanLoopBatchEngine(llm_call_func=my_llm, total_count=TOTAL_COUNT)

    print("=" * 40)
    print("  PromptMill — Batch Generation Engine")
    print("=" * 40)
    print(f"Target: {TOTAL_COUNT} items")
    print("Enter your prompt instruction.\n")

    instruction = input("Prompt: ").strip()
    if not instruction:
        print("No instruction provided. Exiting.")
        exit()

    engine.submit_instruction(instruction)

    if engine.state == EngineState.COMPLETED:
        results = engine.get_all_results()
        print(f"\nDone! {len(results)} items generated.")
        engine.save_results("output_results.json")
        print("Saved to output_results.json")