FROM python:3.11-slim

WORKDIR /app

COPY *.py inventory.json ./

# Run tests:   docker run --rm inventory-lab8 python -m unittest -v
# Run demo:    docker run --rm inventory-lab8 python lab8_demo.py
# Run program: docker run -it --rm inventory-lab8
CMD ["python", "persistent_auditor.py"]
