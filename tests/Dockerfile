FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends chromium chromium-driver && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir selenium pytest
WORKDIR /tests
COPY test_gemstore.py .
CMD ["pytest", "-v", "--junitxml=report.xml", "test_gemstore.py"]
