from src.database import SessionLocal
from src.models import Course, Department

def get_course_descriptions() -> str:
    """A single text resource containing a formatted list of all courses and their descriptions."""
    db = SessionLocal()
    try:
        courses = db.query(Course).all()
        lines = []
        for c in courses:
            desc = c.description or "No description available."
            lines.append(f"[{c.course_code}] {c.title}: {desc}")
        return "\n".join(lines)
    finally:
        db.close()

def get_department_directory() -> str:
    """A text resource listing all available academic departments and their codes."""
    db = SessionLocal()
    try:
        departments = db.query(Department).all()
        lines = []
        for d in departments:
            lines.append(f"{d.name} ({d.code})")
        return "\n".join(lines)
    finally:
        db.close()
