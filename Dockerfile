FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn streamlit requests

CMD bash -c "uvicorn api.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 7860 --server.address 0.0.0.0"