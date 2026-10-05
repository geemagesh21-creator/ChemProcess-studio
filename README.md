# ChemProcess Studio

A responsive process-engineering calculator with heat exchanger, pipe hydraulics, and reactor kinetics modules.

## Run locally

```bash
pip install -r requirements.txt
PORT=8501 python app.py
```

Open `http://127.0.0.1:8501`.

## Deploy with Docker

```bash
docker build -t chemprocess-studio .
docker run --rm -p 3000:3000 chemprocess-studio
```

The app honors the `PORT` environment variable and serves `/` plus the three JSON API endpoints.
