# vector_store.py 完整内容
import os
import chromadb
from modelscope import snapshot_download
from sentence_transformers import SentenceTransformer
from typing import List, Dict

# 1. 从阿里云ModelScope下载模型到本地（第一次运行自动下载，之后直接读本地）
model_dir = snapshot_download('BAAI/bge-large-zh-v1.5')

# 2. 加载本地下载好的模型
embedding_model = SentenceTransformer(model_dir)

# 初始化向量库
client = chromadb.PersistentClient(path="./.chroma")
collection = client.get_or_create_collection(name="knowledge_base")

def add_documents(chunks: List[str], source: str):
    ids = [f"{source}_{i}" for i in range(len(chunks))]
    embeddings = embedding_model.encode(chunks).tolist()
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[{"source": source} for _ in chunks]
    )

def search_documents(query: str, top_k: int = 10) -> List[Dict]:
    query_embedding = embedding_model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    return [
        {"text": doc, "source": meta["source"], "distance": dist}
        for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0])
    ]

def get_all_files():
    """获取当前向量库中所有已上传的文件及对应的块数"""
    all_data = collection.get(include=["metadatas"])
    file_stats: dict[str, int] = {}
    for meta in all_data["metadatas"]:
        source: str = str(meta["source"])
        file_stats[source] = file_stats.get(source, 0) + 1
    return [{"name": name, "chunks": count} for name, count in file_stats.items()]

