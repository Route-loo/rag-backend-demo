import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import pypdf
from text_splitter import split_text
from llm_client import generate_answer
from vector_store import add_documents, search_documents, get_all_files


load_dotenv()
app = FastAPI(title="RAG私有知识库问答系统")

# 访问根路径直接返回前端页面
@app.get("/", summary="首页")
async def read_index():
    return FileResponse("static/index.html")


class QueryRequest(BaseModel):
    query: str
    top_k: int = 10


@app.post("/upload-pdf", summary="上传PDF到知识库")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="只支持PDF文件")

    pdf_reader = pypdf.PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    chunks = split_text(text)
    add_documents(chunks, source=file.filename)
    return {"message": f"成功上传{file.filename}，切分为{len(chunks)}个文本块"}


@app.post("/ask", summary="RAG知识库问答")
async def ask_question(request: QueryRequest):
    search_results = search_documents(request.query, top_k=request.top_k)
    if not search_results:
        return {"answer": "知识库为空，请先上传文档", "sources": []}

    context = "\n\n".join([f"[来自{r['source']}] {r['text']}" for r in search_results])
    answer = generate_answer(request.query, context)
    return {
        "answer": answer,
        "sources": [{"text": r["text"], "source": r["source"]} for r in search_results]
    }

@app.get("/files", summary="获取知识库所有已上传文件")
async def get_files():
    return {"files": get_all_files()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
