FROM python:3.11-slim

WORKDIR /app

COPY *.py inventory.json ./

# Run tests:   docker run --rm inventory-lab7 python -m unittest -v
# Run program: docker run -it --rm inventory-lab7
CMD ["python", "persistent_auditor.py"]
