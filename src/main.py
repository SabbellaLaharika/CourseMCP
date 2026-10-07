from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="University Course Catalog MCP Server")

# Initialize the MCP Server using FastMCP
mcp = FastMCP("university-catalog")

from src.tools.search_courses import search_courses
from src.tools.get_prerequisites import get_prerequisites
from src.tools.lookup_instructor import lookup_instructor
from src.tools.prerequisite_graph import get_prerequisite_graph

mcp.add_tool(search_courses)
mcp.add_tool(get_prerequisites)
mcp.add_tool(lookup_instructor)
mcp.add_tool(get_prerequisite_graph)

# Register MCP Resources
from src.resources import get_course_descriptions, get_department_directory
mcp.resource("resource://course_descriptions", name="course_descriptions")(get_course_descriptions)
mcp.resource("resource://department_directory", name="department_directory")(get_department_directory)

# Health check endpoint required by the prompt
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Mount the MCP server onto the FastAPI app
# This automatically exposes the SSE and messages endpoints under /mcp
app.mount("/mcp", mcp.sse_app())

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)
