FROM python:3.10
WORKDIR /app
COPY mcp_server.py .
RUN pip install mcp requests
CMD ["python", "mcp_server.py"]
