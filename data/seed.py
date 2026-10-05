import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import engine, Base, SessionLocal
from src.models import Department, Instructor, Course

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Check if we already have data
    if db.query(Department).first():
        print("Database already seeded.")
        db.close()
        return

    print("Seeding database...")

    # Departments (5)
    cs = Department(name="Computer Science", code="CS")
    math = Department(name="Mathematics", code="MATH")
    phy = Department(name="Physics", code="PHY")
    art = Department(name="Art and Design", code="ART")
    bus = Department(name="Business", code="BUS")
    db.add_all([cs, math, phy, art, bus])
    db.commit()

    # Instructors (10)
    i1 = Instructor(name="Dr. Alan Turing", email="alan@univ.edu", department_id=cs.id)
    i2 = Instructor(name="Dr. Ada Lovelace", email="ada@univ.edu", department_id=cs.id)
    i3 = Instructor(name="Dr. Grace Hopper", email="grace@univ.edu", department_id=cs.id)
    i4 = Instructor(name="Dr. Isaac Newton", email="isaac@univ.edu", department_id=phy.id)
    i5 = Instructor(name="Dr. Albert Einstein", email="albert@univ.edu", department_id=phy.id)
    i6 = Instructor(name="Dr. Carl Gauss", email="carl@univ.edu", department_id=math.id)
    i7 = Instructor(name="Dr. Leonhard Euler", email="leonhard@univ.edu", department_id=math.id)
    i8 = Instructor(name="Prof. Leonardo da Vinci", email="leo@univ.edu", department_id=art.id)
    i9 = Instructor(name="Prof. Frida Kahlo", email="frida@univ.edu", department_id=art.id)
    i10 = Instructor(name="Dr. Adam Smith", email="adam@univ.edu", department_id=bus.id)
    db.add_all([i1, i2, i3, i4, i5, i6, i7, i8, i9, i10])
    db.commit()

    # Courses (18)
    # CS
    c1 = Course(course_code="CS101", title="Introduction to Programming", description="A foundational course on programming principles.", credits=3, instructor_id=i1.id, department_id=cs.id)
    c2 = Course(course_code="CS201", title="Data Structures", description="Learn about arrays, lists, trees, and graphs.", credits=4, instructor_id=i2.id, department_id=cs.id)
    c3 = Course(course_code="CS301", title="Algorithms", description="Algorithm design and analysis.", credits=4, instructor_id=i1.id, department_id=cs.id)
    c4 = Course(course_code="CS401", title="Advanced Algorithms", description="Complex algorithms and P vs NP.", credits=3, instructor_id=i3.id, department_id=cs.id)
    c5 = Course(course_code="CS501", title="Machine Learning", description="Introduction to Machine Learning.", credits=4, instructor_id=i2.id, department_id=cs.id)
    c6 = Course(course_code="CS502", title="Artificial Intelligence", description="Deep learning and AI systems.", credits=4, instructor_id=i1.id, department_id=cs.id)
    
    # MATH
    c7 = Course(course_code="MATH101", title="Calculus I", description="Limits, derivatives, and integrals.", credits=4, instructor_id=i6.id, department_id=math.id)
    c8 = Course(course_code="MATH201", title="Linear Algebra", description="Vectors, matrices, and linear transformations.", credits=3, instructor_id=i7.id, department_id=math.id)
    c9 = Course(course_code="MATH301", title="Probability and Statistics", description="Distributions and statistical testing.", credits=3, instructor_id=i6.id, department_id=math.id)
    
    # PHY
    c10 = Course(course_code="PHY101", title="Physics I", description="Classical mechanics.", credits=4, instructor_id=i4.id, department_id=phy.id)
    c11 = Course(course_code="PHY201", title="Physics II", description="Electromagnetism.", credits=4, instructor_id=i5.id, department_id=phy.id)
    c12 = Course(course_code="PHY301", title="Quantum Mechanics", description="Introduction to quantum theory.", credits=3, instructor_id=i5.id, department_id=phy.id)

    # ART
    c13 = Course(course_code="ART101", title="Introduction to Fine Arts", description="Basics of drawing and painting.", credits=3, instructor_id=i8.id, department_id=art.id)
    c14 = Course(course_code="ART201", title="Digital Media Design", description="Creating art with digital tools.", credits=3, instructor_id=i9.id, department_id=art.id)
    c15 = Course(course_code="ART301", title="Advanced 3D Modeling", description="Advanced techniques in 3D creation.", credits=4, instructor_id=i8.id, department_id=art.id)
    
    # BUS
    c16 = Course(course_code="BUS101", title="Introduction to Business", description="Business fundamentals.", credits=3, instructor_id=i10.id, department_id=bus.id)
    c17 = Course(course_code="BUS201", title="Microeconomics", description="Individual and firm behavior.", credits=3, instructor_id=i10.id, department_id=bus.id)
    c18 = Course(course_code="BUS301", title="Macroeconomics", description="National and global economies.", credits=3, instructor_id=i10.id, department_id=bus.id)

    db.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18])
    db.commit()

    # Prerequisites Chains
    
    # CS Chain 1: CS101 -> CS201 -> CS301 -> CS401
    c2.prerequisites.append(c1)
    c3.prerequisites.append(c2)
    c4.prerequisites.append(c3)
    
    # CS Chain 2: ML needs Linear Algebra and Algorithms. AI needs ML.
    c5.prerequisites.append(c8)  # MATH201
    c5.prerequisites.append(c3)  # CS301
    c6.prerequisites.append(c5)  # CS501
    
    # MATH Chain: MATH101 -> MATH301
    c9.prerequisites.append(c7)
    
    # PHY Chain: PHY101 -> PHY201 -> PHY301 (also needs MATH201)
    c11.prerequisites.append(c10)
    c12.prerequisites.append(c11)
    c12.prerequisites.append(c8) # MATH201
    
    # ART Chain: ART101 -> ART201 -> ART301
    c14.prerequisites.append(c13)
    c15.prerequisites.append(c14)
    
    # BUS Chain: BUS101 -> BUS201 -> BUS301
    c17.prerequisites.append(c16)
    c18.prerequisites.append(c17)

    db.commit()
    db.close()
    print("Database seeded successfully with expanded dataset.")

if __name__ == "__main__":
    seed_data()
