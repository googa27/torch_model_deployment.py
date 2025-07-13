FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY inference.py create_model.py doubleit_model.pt __torch__.py __torch__.py.debug_pkl constants.pkl data.pkl api.py /app/
COPY tests/ /app/tests/
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]