FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install mcp google-genai requests
CMD ["python", "agent.py"]
