# Agentic Trading Arena deployment

This directory is ready to use as a standalone GitHub repository and Render Blueprint.

## Project routes

- `/` — interactive 3D Arena
- `/owner` or `/owner.html` — responsive participant Owner View
- `/health` — deployment health check

## Local production check

```powershell
cd arena
python -m pip install -r requirements.txt
python -m uvicorn server:app --host 0.0.0.0 --port 8053
```

## Publish to GitHub

Create an empty GitHub repository, then run these commands from this directory:

```powershell
git init
git add .
git commit -m "Initial Agentic Trading Arena deployment"
git branch -M main
git remote add origin https://github.com/YOUR_ACCOUNT/YOUR_REPOSITORY.git
git push -u origin main
```

Do not run `git init` here if you intend to keep this directory as part of the existing parent `FS` repository. In that case, commit it from the parent repository instead.

## Deploy on Render

1. Push this directory to GitHub.
2. In Render, select **New → Blueprint**.
3. Connect the GitHub repository.
4. Render will read `render.yaml`, install the Python dependencies from `arena/requirements.txt`, and start Uvicorn.
5. Confirm `/health` returns `{"status":"ok","service":"agentic-arena"}`.

No database, secrets, background workers, or scheduled jobs are required for this showcase. Browser state is local to each visitor and is not shared across devices.
