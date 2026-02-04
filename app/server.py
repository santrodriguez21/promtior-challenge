from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from app.chain import chain as promtior_chain

app = FastAPI(
    title="Promtior RAG Challenge",
    version="1.0",
    description="API server for Promtior Technical Test using LangChain & LangServe",
)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

# Exponemos la cadena en la ruta /chain
add_routes(
    app,
    promtior_chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn
    # Corremos el servidor en localhost puerto 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)