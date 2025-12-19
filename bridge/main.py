import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import git
import requests

import shutil

app = FastAPI()

# Configuration
REPO_DIR = "/app/repos"
HTML_FILE = "/app/PenaltyBoxConfigurator_Mockup.html"

# Ensure repo directory exists
os.makedirs(REPO_DIR, exist_ok=True)

class CloneRequest(BaseModel):
    url: str
    name: str

@app.get("/")
async def read_root():
    if os.path.exists(HTML_FILE):
        return FileResponse(HTML_FILE)
    return {"error": "HTML file not found"}

@app.get("/repos")
async def list_repos():
    repos = []
    if os.path.exists(REPO_DIR):
        for name in os.listdir(REPO_DIR):
            path = os.path.join(REPO_DIR, name)
            if os.path.isdir(path):
                try:
                    repo = git.Repo(path)
                    branch = repo.active_branch.name
                    repos.append({"name": name, "branch": branch})
                except:
                    repos.append({"name": name, "branch": "unknown"})
    return repos

@app.post("/repos/clone")
async def clone_repo(req: CloneRequest):
    repo_path = os.path.join(REPO_DIR, req.name)
    if os.path.exists(repo_path):
        raise HTTPException(status_code=400, detail="Repo already exists")
    
    try:
        git.Repo.clone_from(req.url, repo_path)
        return {"status": "cloned", "path": repo_path}
    except Exception as e:
        # Clean up if clone failed
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/repos/{name}/pull")
async def pull_repo(name: str):
    repo_path = os.path.join(REPO_DIR, name)
    if not os.path.exists(repo_path):
        raise HTTPException(status_code=404, detail="Repo not found")
    
    try:
        repo = git.Repo(repo_path)
        origin = repo.remotes.origin
        origin.pull()
        return {"status": "pulled", "repo": name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/repos/{name}/push")
async def push_repo(name: str):
    repo_path = os.path.join(REPO_DIR, name)
    if not os.path.exists(repo_path):
        raise HTTPException(status_code=404, detail="Repo not found")
    
    try:
        repo = git.Repo(repo_path)
        origin = repo.remotes.origin
        origin.push()
        return {"status": "pushed", "repo": name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/templates")
async def list_templates(repo: str, branch: str = "main"):
    repo_path = os.path.join(REPO_DIR, repo)
    if not os.path.exists(repo_path):
        return []
    
    templates = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".tmpl") or file.endswith(".json"):
                 # Make path relative to repo root
                 rel_path = os.path.relpath(os.path.join(root, file), repo_path)
                 templates.append({"name": file, "path": rel_path})
    return templates

# Proxy to Alarm API (example)
@app.get("/alarm-proxy/{path:path}")
async def alarm_proxy(path: str):
    # This should be configured via environment variable
    ALARM_API_URL = os.environ.get("ALARM_API_URL", "http://localhost:8080")
    try:
        resp = requests.get(f"{ALARM_API_URL}/{path}")
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
