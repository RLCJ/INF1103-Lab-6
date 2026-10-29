FROM python:3.11-slim
WORKDIR /app
COPY inventory_manager_refractored.py .
CMD ["python", "inventory_manager_refractored.py"]