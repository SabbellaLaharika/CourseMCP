from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="University Course Catalog MCP Server")

# Initialize the MCP Server using FastMCP
mcp = FastMCP("university-catalog")

# Health check endpoint required by the prompt
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Mount the MCP server onto the FastAPI app
# This automatically exposes the SSE and messages endpoints under /mcp
app.mount("/mcp", mcp.sse_app())

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)
