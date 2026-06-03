
FROM python:3.13-slim

WORKDIR /app


COPY requirements.txt .
RUN pip install -r requirements.txt

# 4. Copy the rest of your code
COPY . .

# 5. Expose the port
EXPOSE 8000

# 6. Run the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]