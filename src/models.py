from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

prerequisites = Table(
    'prerequisites',
    Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True),
    Column('prerequisite_id', Integer, ForeignKey('courses.id'), primary_key=True)
)

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, index=True, nullable=False)

    instructors = relationship("Instructor", back_populates="department")
    courses = relationship("Course", back_populates="department")


class Instructor(Base):
    __tablename__ = "instructors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("Department", back_populates="instructors")
    courses = relationship("Course", back_populates="instructor")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    credits = Column(Integer, nullable=False)
    instructor_id = Column(Integer, ForeignKey("instructors.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("Department", back_populates="courses")
    instructor = relationship("Instructor", back_populates="courses")
    
    # Self-referential many-to-many relationship for prerequisites
    prerequisites = relationship(
        "Course",
        secondary=prerequisites,
        primaryjoin=id == prerequisites.c.course_id,
        secondaryjoin=id == prerequisites.c.prerequisite_id,
        backref="is_prerequisite_for"
    )
