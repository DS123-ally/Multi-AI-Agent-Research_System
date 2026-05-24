# ResearchMind · AI Research Agent 🔬

ResearchMind is a Multi-Agent AI System built with Streamlit and LangChain. It leverages a pipeline of four specialized AI agents that collaborate—searching, scraping, writing, and critiquing—to deliver a polished research report on any topic.

## 🚀 Features

- **Search Agent:** Gathers recent web information based on the given topic.
- **Reader Agent:** Scrapes and extracts deep content from the best resources found.
- **Writer Chain:** Drafts a full, comprehensive research report.
- **Critic Chain:** Reviews and scores the report to ensure high quality.
- **Beautiful UI:** Custom Streamlit interface with a sleek, modern design.

## 🛠️ Installation

1. Clone this repository.
2. Ensure you have Python installed.
3. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Configure your environment variables in a `.env` file (e.g., API keys for LLMs).

## 🏃‍♂️ Running the Application

You can easily run the application using the included PowerShell script:

```bash
.\run.ps1
```

Or manually:

```bash
python -m streamlit run app.py
```

The application will be accessible in your web browser at `http://localhost:8501`.

## 🧠 Pipeline Overview

1. Enter your **Research Topic** (e.g. "Quantum computing breakthroughs in 2025").
2. Click **Run Research Pipeline**.
3. Watch the live progress as the agents run step-by-step.
4. View the final, detailed research report and the critic's feedback.
5. Download your report as a `.md` file.

## 📜 License

MIT License
