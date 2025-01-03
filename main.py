from fastapi import FastAPI, Query
import subprocess
import json

app = FastAPI()

@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.get("/check_username/")
async def check_username(username: str = Query(..., min_length=1)):
    try:
        # Run Sherlock command and capture output
        result = subprocess.run(
            ['sherlock', '--timeout','5', username],
            capture_output=True,
            text=True,
            check=True
        )
        # Parse the text output and convert it to JSON
        lines = result.stdout.splitlines()
        data = {}
        for line in lines:
            if line.startswith("[+]"):
                site, url = line.split(":", 1)
                site = site.strip("[+] ").strip()
                url = url.strip()
                data[site] = url
        return data
    except subprocess.CalledProcessError as e:
        return {"error": e.stderr}