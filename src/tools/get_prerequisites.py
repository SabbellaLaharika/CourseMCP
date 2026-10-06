from src.database import SessionLocal
from src.models import Course
from src.schemas import GetPrerequisitesOutput, PrerequisiteSummary

def get_prerequisites(course_code: str) -> GetPrerequisitesOutput:
    """Retrieves the direct prerequisites for a given course code."""
    db = SessionLocal()
    try:
        course = db.query(Course).filter(Course.course_code == course_code.upper()).first()
        
        if not course:
            return GetPrerequisitesOutput(course_code=course_code, prerequisites=[])
            
        prereqs = [
            PrerequisiteSummary(course_code=p.course_code, title=p.title)
            for p in course.prerequisites
        ]
        
        return GetPrerequisitesOutput(
            course_code=course.course_code,
            prerequisites=prereqs
        )
    finally:
        db.close()
