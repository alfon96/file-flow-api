FROM python:3.11-slim

# Install git and tree
RUN apt update && apt install -y git && apt install tree


# Create a vscode user and group
RUN groupadd --gid 1000 vscode && useradd --uid 1000 --gid 1000 -m vscode 

WORKDIR /app

COPY ./requirements.txt .

COPY ./app .

EXPOSE 8000

RUN pip install --no-cache-dir -r requirements.txt

CMD ["fastapi","dev", "app/main.py","--host","0.0.0.0"]