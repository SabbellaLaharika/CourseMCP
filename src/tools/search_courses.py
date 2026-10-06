from typing import Optional
from src.database import SessionLocal
from src.models import Course, Department
from src.schemas import CourseSummaryOutput

def search_courses(query: str, department_code: Optional[str] = None) -> list[CourseSummaryOutput]:
    """Searches the university course catalog for courses matching a query string. Can be filtered by a specific department code."""
    db = SessionLocal()
    try:
        q = db.query(Course)
        if department_code:
            q = q.join(Department).filter(Department.code == department_code.upper())
        
        search_filter = f"%{query}%"
        q = q.filter(Course.title.ilike(search_filter) | Course.description.ilike(search_filter))
        
        results = q.all()
        return [
            CourseSummaryOutput(
                course_code=c.course_code,
                title=c.title,
                credits=c.credits
            )
            for c in results
        ]
    finally:
        db.close()
