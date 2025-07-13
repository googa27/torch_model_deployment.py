# Dockerfile
# This Dockerfile sets up a Python environment for running the doubleit model API.
FROM python:3.13-slim
WORKDIR /app
# Install python dependencies
# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Copy the application code
# This includes the inference script, model, and API code
COPY inference.py create_model.py doubleit_model.pt __torch__.py __torch__.py.debug_pkl constants.pkl data.pkl api.py /app/
COPY tests/ /app/tests/
# Expose the port for the API
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]