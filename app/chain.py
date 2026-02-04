import os
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

# Cargar claves del archivo .env
load_dotenv()

# --- 1. INGESTA DE DATOS ---
urls = ["https://promtior.ai/"]
docs = []

# Cargar Web
print("--- Loading Web Content ---")
loader_web = WebBaseLoader(urls)
docs.extend(loader_web.load())

# Cargar PDF (si el archivo existe en la carpeta)
pdf_path = "Promtior_Presentation.pdf"
if os.path.exists(pdf_path):
    print(f"--- Loading PDF Content: {pdf_path} ---")
    loader_pdf = PyPDFLoader(pdf_path)
    docs.extend(loader_pdf.load())
else:
    print("--- Warning: PDF not found. Running only with Web content. ---")

# --- 2. PROCESAMIENTO (Transform) ---
# Divide el texto en fragmentos para que la IA pueda digerirlos
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(docs)

# --- 3. ALMACENAMIENTO (Load) ---
# Creamos la base de datos vectorial con Chroma
print("--- Creating Vector Store ---")
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings(),
    collection_name="promtior_data"
)
retriever = vectorstore.as_retriever()

# --- 4. CEREBRO (LLM) ---
# Usamos GPT-3.5-turbo (rápido y barato)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Prompt de Ingeniería: Le damos una personalidad y reglas estrictas
template = """You are a professional and helpful assistant for Promtior.
Use the following context to answer the question.
Provide a comprehensive answer, covering all relevant details found in the context.
If the information forms a list, use bullet points for clarity.
If you don't know the answer, just say that you don't know.

Context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# --- 5. CADENA (Pipeline) ---
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)