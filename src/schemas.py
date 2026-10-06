from pydantic import BaseModel, Field
from typing import List, Optional

# ==========================================
# Tool 1: search_courses
# ==========================================
class SearchCoursesInput(BaseModel):
    query: str = Field(description="Search keyword to match against course titles and descriptions.")
    department_code: Optional[str] = Field(default=None, description="Optional department code to filter by (e.g., CS, MATH).")

class CourseSummaryOutput(BaseModel):
    course_code: str
    title: str
    credits: int

# ==========================================
# Tool 2: get_prerequisites
# ==========================================
class GetPrerequisitesInput(BaseModel):
    course_code: str = Field(description="The unique course code (e.g., CS101).")

class PrerequisiteSummary(BaseModel):
    course_code: str
    title: str

class GetPrerequisitesOutput(BaseModel):
    course_code: str
    prerequisites: List[PrerequisiteSummary]

# ==========================================
# Tool 3: lookup_instructor
# ==========================================
class LookupInstructorInput(BaseModel):
    instructor_name: str = Field(description="The name of the instructor to look up.")

class LookupInstructorOutput(BaseModel):
    name: str
    email: str
    department_name: str

# Generic error structure
class ErrorOutput(BaseModel):
    error: str

# ==========================================
# Tool 4: get_prerequisite_graph
# ==========================================
class GetPrerequisiteGraphInput(BaseModel):
    course_code: str = Field(description="The unique course code to generate the full dependency graph for.")

class Node(BaseModel):
    id: str

class Edge(BaseModel):
    source: str
    target: str

class GetPrerequisiteGraphOutput(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
