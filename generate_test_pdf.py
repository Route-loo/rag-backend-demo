from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# 注册中文字体
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

# 创建PDF
c = canvas.Canvas("RAG技术测试文档.pdf")
c.setFont('STSong-Light', 14)

# 写内容
y = 750
c.drawString(100, y, "RAG检索增强生成技术入门简介")
y -= 50

content = [
    "一、什么是RAG？",
    "RAG的全称是检索增强生成，是一种结合了信息检索和大语言模型的技术。",
    "它的核心思想是先从外部知识库中检索相关的信息，再把这些信息作为上下文提供给大模型，",
    "让大模型基于私有知识生成回答，而不是完全依赖模型自身的预训练知识。",
    "",
    "二、RAG的基本工作流程",
    "1. 文档处理阶段：将上传的PDF、Word等文档进行文本提取和分块，",
    "再通过嵌入模型将文本块转换为向量，存入向量数据库。",
    "2. 检索阶段：当用户提出问题时，将用户的问题也转换为向量，",
    "在向量数据库中相似度最高的Top-K个文本块作为相关上下文。",
    "3. 生成阶段：将检索到的上下文和用户问题一起组装成提示词，",
    "调用大语言模型生成最终的回答，同时可以返回引用的来源原文。",
    "",
    "三、RAG的主要优点",
    "1. 减少大模型幻觉：因为回答是基于私有知识库的真实内容生成的，",
    "大大降低了大模型编造信息的概率。",
    "2. 支持私有知识：可以直接使用企业或个人自己的文档作为知识库，",
    "不需要重新训练大模型。",
    "3. 答案可溯源：可以直接定位到回答对应的原始文档片段，方便验证准确性。",
    "",
    "四、常见应用场景",
    "RAG技术目前广泛应用于智能客服、企业内部知识库问答、",
    "学术文献助手、法律文档分析等场景，是大模型落地最常用的技术方案之一。"
]

for line in content:
    if line == "":
        y -= 20
        continue
    c.drawString(80, y, line)
    y -= 28

c.save()
print("测试PDF生成完成：RAG技术测试文档.pdf")
