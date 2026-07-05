# 🏭 PromptMill — HumanLoopBatchEngine

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

⚙️ Configuration
Before first use, open run_engine.py and set your API key:

python
DEEPSEEK_API_KEY = "sk-your-api-key-here"
Get a free API key at DeepSeek Platform.

To change the model or use OpenAI, modify the my_llm function in run_engine.py.

🧠 The Framework Behind It
PromptMill is built on the "Review-Generate Separation" pattern. Read the full framework documentation in docs/FRAMEWORK.md.

text
Human writes prompt → AI generates 1 sample → Human reviews
                                              ├─ Not satisfied → Revise prompt ↺
                                              └─ Satisfied → AI batch-produces all → Download
📦 Tech Stack
Backend: Python

Interface: Streamlit (browser-based, works on desktop, tablet, and mobile)

LLM: DeepSeek by default (easily swappable to OpenAI, Claude, etc.)

Dependencies: requests, streamlit

🌐 Mobile / iPad Use
PromptMill's Streamlit interface works on any device with a browser.

To use it like a native app on iPhone/iPad:

Open the URL in Safari.

Tap the Share button → "Add to Home Screen".

You now have a full-screen app icon on your home screen.