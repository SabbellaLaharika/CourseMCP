# 🎓 University Course Catalog MCP Server

A Model Context Protocol (MCP) server that exposes a university's course catalog to AI agents and Large Language Models (LLMs). Built with FastAPI, SQLite, and the official Python `mcp` SDK, this server securely provides structured tools, contextual resources, and prompt templates for building an AI-powered academic advisor.

---

## 🚀 Features
- **MCP Server Integration:** Exposes domain-specific knowledge to LLMs using the standardized Model Context Protocol (via SSE transport).
- **Strict Data Validation:** Utilizes Pydantic v2 to strictly validate tool inputs and enforce precise JSON output schemas.
- **Relational Data Mapping:** Uses SQLAlchemy ORM to manage departments, instructors, courses, and self-referential prerequisite relationships.
- **Graph Traversals:** Computes complex, multi-level prerequisite dependency chains using NetworkX.
- **Containerized:** Production-ready Docker environment with automatic idempotent database seeding.

---

## 🛠️ Setup & Installation

This application is fully containerized and orchestrated with Docker Compose for a seamless, one-command setup.

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd CourseMCP
   ```

2. **Set up Environment Variables:**
   Copy the provided `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

3. **Start the Server:**
   ```bash
   docker-compose up --build
   ```
   *The server will start on port `8080`. The SQLite database is automatically seeded on startup and persisted in the `./data` directory.*

4. **Verify Health:**
   Check that the server is healthy and running:
   ```bash
   curl http://localhost:8080/health
   ```

5. **Interactive Testing with the MCP Inspector:**
   Launch the official MCP Inspector UI to interactively test all tools, resources, and prompts — no code required:
   ```bash
   npx @modelcontextprotocol/inspector http://localhost:8080/mcp/sse
   ```
   Then open the URL shown in your terminal (usually **http://127.0.0.1:6274**) in your browser to explore the server live.

---

## 🧰 Available MCP Tools

AI agents can invoke these tools to dynamically query the live catalog:

1. **`search_courses`**
   - **Description:** Searches for courses by keyword (matching title or description) with an optional department code filter.
   - **Example LLM Query:** *"Find all Computer Science (CS) courses related to machine learning or artificial intelligence."*

2. **`get_prerequisites`**
   - **Description:** Retrieves the direct prerequisites for a given course code.
   - **Example LLM Query:** *"What classes do I need to take immediately before I can register for CS401?"*

3. **`lookup_instructor`**
   - **Description:** Finds an instructor's details (name, email, department) by matching their name.
   - **Example LLM Query:** *"Can you give me the contact details and department for Dr. Ada Lovelace?"*

4. **`get_prerequisite_graph`**
   - **Description:** Returns the full, recursive dependency graph (nodes and edges) representing all prerequisites required for a course.
   - **Example LLM Query:** *"Map out the complete, multi-semester path of prerequisite courses I need to complete to eventually take PHY301."*

---

## 📄 Available MCP Resources

Resources provide static or semi-static context directly to the LLM's prompt context:

1. **`course_descriptions`** (`resource://course_descriptions`)
   - A comprehensive, formatted text document listing all available courses and their full descriptions.

2. **`department_directory`** (`resource://department_directory`)
   - A directory listing all available academic departments alongside their official department codes.

---

## 📝 Prompt Templates

1. **`course_comparison_template`**
   - **Description:** Guides the LLM to create a structured comparison table for two specific courses using `{{course_code_1}}` and `{{course_code_2}}` placeholders.
   - **Usage:** Prompts the agent to proactively invoke MCP tools to fetch detailed course information and prerequisites before generating a side-by-side analysis table for the student.
