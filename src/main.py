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

# Register MCP Prompt Template
@mcp.prompt(
    name="course_comparison_template",
    description="A structured prompt that guides an LLM to compare two university courses in detail."
)
def course_comparison_template(course_code_1: str, course_code_2: str) -> list[dict]:
    """Generates a comparison prompt for two courses given their codes."""
    text = (
        "Create a table comparing the following two courses: "
        "{{course_code_1}} and {{course_code_2}}. "
        f"(Resolved values: course_code_1={course_code_1}, course_code_2={course_code_2}). "
        "Include columns for Title, Credits, Description, and Prerequisites. "
        "Use the available MCP tools to fetch information for both courses before building the table."
    )
    return [{"role": "user", "content": text}]

# Health check endpoint required by the prompt
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Mount the MCP server onto the FastAPI app
# This automatically exposes the SSE and messages endpoints under /mcp
app.mount("/mcp", mcp.sse_app())

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)
