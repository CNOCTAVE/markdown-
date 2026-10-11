# 八度君（b站id：CNOCTAVE）
# https://space.bilibili.com/1888473666
# 关注点赞转发收藏充电，祝我走向1000粉丝之路
# the MIT License (MIT)

import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

app = FastAPI(title="Markdown Editor API")

BASE_DIR = Path(__file__).resolve().parent

class SaveRequest(BaseModel):
    path: str
    content: str

@app.get("/", response_class=HTMLResponse)
def index():
    return FileResponse(BASE_DIR / "index.html")

@app.get("/api/files")
def list_files():
    """列出工作目录下的所有 markdown 文件"""
    files = []
    for p in sorted(BASE_DIR.glob("*.md")):
        files.append(p.name)
    return {"files": files}

@app.get("/api/file")
def open_file(name: str):
    """打开指定 markdown 文件，返回其内容"""
    p = (BASE_DIR / name).resolve()
    # 防止路径穿越
    if not str(p).startswith(str(BASE_DIR)):
        raise HTTPException(status_code=400, detail="非法路径")
    if p.suffix.lower() not in (".md", ".markdown"):
        raise HTTPException(status_code=400, detail="仅支持 markdown 文件")
    if not p.is_file():
        raise HTTPException(status_code=404, detail="文件不存在")
    content = p.read_text(encoding="utf-8")
    return {"name": p.name, "path": str(p), "content": content}

@app.post("/api/file")
def save_file(req: SaveRequest):
    """保存 markdown 文件"""
    p = Path(req.path).resolve()
    if not str(p).startswith(str(BASE_DIR)):
        raise HTTPException(status_code=400, detail="非法路径")
    if p.suffix.lower() not in (".md", ".markdown"):
        raise HTTPException(status_code=400, detail="仅支持 markdown 文件")
    p.write_text(req.content, encoding="utf-8")
    return {"ok": True, "name": p.name}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8030)
