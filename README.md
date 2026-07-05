# 🏭 PromptMill — Human-AI Collaborative Batch Engine

**You set the standard and review the sample. The AI produces the sample and runs the batch. Neither oversteps — maximum efficiency.**

PromptMill is a lightweight engine for **human-AI collaboration** on batch content generation tasks. You write the instruction, the AI generates **one sample first**, you review it, and only when you're satisfied does it **automatically mass-produce the rest**.

No more regenerating entire batches because the first one was wrong.

---

## 🎯 What It Does

| Your Job | AI's Job |
|----------|----------|
| Write & refine the prompt | Generate one sample |
| Review the sample | Batch-produce the rest when approved |
| Download results | Handle errors & retries |

---

## 🚀 Quick Start

### For Non-Technical Users (Browser Interface)

1. **Download** and unzip this project.
2. **Windows**: Double-click `start.bat`  
   **Mac**: Double-click `start.command` (right-click → Open the first time)
3. Your browser opens automatically. Use the web interface.
4. Enter your task, review the sample, approve or revise.
5. Download results as JSON when done.

### For Developers (Command Line)

```bash
pip install -r requirements.txt
python run_engine.py