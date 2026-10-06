from src.database import SessionLocal
from src.models import Instructor
from src.schemas import LookupInstructorOutput, ErrorOutput

def lookup_instructor(instructor_name: str) -> LookupInstructorOutput | ErrorOutput:
    """Finds an instructor's details by their name."""
    db = SessionLocal()
    try:
        # Simple case-insensitive search
        search_filter = f"%{instructor_name}%"
        instructor = db.query(Instructor).filter(Instructor.name.ilike(search_filter)).first()
        
        if not instructor:
            return ErrorOutput(error="Instructor not found")
            
        return LookupInstructorOutput(
            name=instructor.name,
            email=instructor.email,
            department_name=instructor.department.name
        )
    finally:
        db.close()
