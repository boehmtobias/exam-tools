FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/boehmtobias/exam-tools.git .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 6767

HEALTHCHECK --interval=2m CMD curl --fail http://localhost:6767/_stcore/health

ENTRYPOINT ["python", "-m", "streamlit", "run", "ExamUtils.py", "--server.port=6767", "--server.address=0.0.0.0"]