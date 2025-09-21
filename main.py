from fastapi import FastAPI, Request, Form
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import io
import zipfile
import re

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def parse_markdown_to_files(md_text: str):
    """
    Parses markdown looking for headers like:
    ### **6. Frontend JS (`main.js`)**
    followed by a code block.
    Returns a dict {filename: content}
    """
    pattern = r"###.*?\(`([^`]+)`\).*?\n```.*?\n(.*?)```"
    matches = re.findall(pattern, md_text, re.DOTALL)
    files = {filename.strip(): content.strip() for filename, content in matches}
    return files


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/convert")
def convert_to_zip(md_text: str = Form(...)):
    print(md_text)
    files = parse_markdown_to_files(md_text)
    print(files)
    if not files:
        return {"error": "No valid file blocks found in markdown."}

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
