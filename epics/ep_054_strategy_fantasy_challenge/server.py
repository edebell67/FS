from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parent
app = FastAPI(title='Strategy Fantasy Challenge Demo', docs_url=None, redoc_url=None)

@app.get('/health', include_in_schema=False)
def health():
    return {'status': 'ok', 'service': 'strategy-fantasy-challenge-demo'}

@app.get('/', include_in_schema=False)
def home():
    return FileResponse(ROOT / 'index.html')

app.mount('/', StaticFiles(directory=ROOT, html=True), name='static')
