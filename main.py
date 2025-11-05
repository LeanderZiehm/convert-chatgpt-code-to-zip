from fastapi import FastAPI, Request,HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import io
import zipfile


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

import os
import re

def parse_markdown_to_files(md_text):
    """
    Parses markdown for headers starting with # that contain a valid filename.

    Valid filename:
      - Has at least one character before and after a dot (extension)
      - Can have folder paths
    Captures the code block that starts after the next ```
    Returns dict {filepath: content}
    """
    files = {}
    lines = md_text.splitlines()
    i = 0

    def clean_filename(name: str) -> str:
        # Remove markdown special chars (*, #, `, \) and surrounding whitespace
        return re.sub(r'[*#`\\]', '', name).strip()

    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#"):
            parts = line.split()
            filename = None

            for part in parts:
                part_clean = clean_filename(part)

                if "/" in part_clean or "." in part_clean:
                    if "." in part_clean:
                        before, after = part_clean.rsplit(".", 1)
                        if before and after:  # must have text on both sides
                            filename = part_clean
                            break

            if filename:
                # Look for opening ```
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    i += 1
                if i >= len(lines):
                    break

                i += 1  # skip the opening ```
                # Capture until closing ```
                content_lines = []
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    content_lines.append(lines[i])
                    i += 1

                files[filename] = "\n".join(content_lines).strip()

        i += 1

    return files


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/convert")
async def convert_to_zip_json(request: Request):
    try:
        data = await request.json()  # parse JSON safely
    except:
        raise HTTPException(status_code=400, detail="Invalid request. Please submit JSON.")

    md_text = data.get("md_text", "").strip()
    if not md_text:
        raise HTTPException(status_code=400, detail="Please provide markdown text before converting.")

    files = parse_markdown_to_files(md_text)
    if not files:
        raise HTTPException(status_code=400, detail="No valid file blocks found in markdown.")

    # Create zip in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for filename, content in files.items():
            zip_file.writestr(filename, content)
    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": 'attachment; filename="files.zip"'}
    )

