# 🎓 ExamUtils

A collection of utilities for portfolio exams and batch management of student GitLab projects.

## Features

- **📁 Batch Create GitLab Projects** — Create GitLab projects as needed across your namespaces and groups in one go.
- **🔗 Collate Student Data** — Aggregate and organize student data from multiple sources.
- **💾 Export GitLab Projects** — Download and export GitLab projects from your namespaces and groups.
- **📝 LLM Project Eval** — Evaluate student projects using LLMs and generate structured assessments.
- **💬 LLM Issue Feedback** — Generate feedback on student GitLab issues using LLMs.

## Requirements

- Python >= 3.9
- Docker (for containerized deployment)

## Installation

### Option A: Run locally

1. Clone the repository:
   ```bash
   git clone https://gitlab.com/youruser/exam-tools.git
   cd exam-tools
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run ExamUtils.py --server.port=6767 --server.address=0.0.0.0
   ```

### Option B: Run with Docker

1. Clone the repository:
   ```bash
   git clone https://gitlab.com/youruser/exam-tools.git
   cd exam-tools
   ```

2. Build and run:
   ```bash
   docker compose up
   ```

## Accessing the App

Once running, open your browser and navigate to:

- **Locally:** `http://localhost:6767`
- **On the network:** `http://<your-machine-ip>:6767`

To find your machine's IP on Windows, run `ipconfig` in a terminal and look for your IPv4 address.

> **Note:** The app binds to `0.0.0.0` by default, making it accessible to other devices on the same network without any additional configuration.

## Authors

- **Tobias Böhm** ([research@boehmt.de](mailto:research@boehmt.de))

## Changelog

- `V0.1.0` — Initial release. Core app structure with Streamlit multipage setup. Includes batch export of GitLab projects. Other features are still work in progress.