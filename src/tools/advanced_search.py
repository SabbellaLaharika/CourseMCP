from src.database import SessionLocal
from src.models import Instructor
from src.schemas import LookupInstructorOutput

def search_instructors(query: str) -> list[LookupInstructorOutput]:
    """Advanced search returning a list of all instructors whose names match the query string."""
    db = SessionLocal()
    try:
        search_filter = f"%{query}%"
        instructors = db.query(Instructor).filter(Instructor.name.ilike(search_filter)).all()
        
        return [
            LookupInstructorOutput(
                name=inst.name,
                email=inst.email,
                office=inst.office,
                department_name=inst.department.name
            )
            for inst in instructors
        ]
    finally:
        db.close()


