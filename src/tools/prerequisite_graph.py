import networkx as nx
from src.database import SessionLocal
from src.models import Course
from src.schemas import GetPrerequisiteGraphOutput, Node, Edge

def get_prerequisite_graph(course_code: str) -> GetPrerequisiteGraphOutput:
    """Returns the full dependency graph for a course."""
    db = SessionLocal()
    try:
        # Build the full graph of all courses and prerequisites
        all_courses = db.query(Course).all()
        G = nx.DiGraph()
        
        # Add all nodes and edges to networkx
        for c in all_courses:
            G.add_node(c.course_code)
            for p in c.prerequisites:
                # source is prerequisite for target
                G.add_edge(p.course_code, c.course_code)
                
        # Find the target course
        course_code = course_code.upper()
        if course_code not in G.nodes:
            return GetPrerequisiteGraphOutput(nodes=[], edges=[])
            
        # Get all ancestors (prerequisites) of the course
        ancestors = nx.ancestors(G, course_code)
        
        # The subgraph we care about includes the target course and its ancestors
        subgraph_nodes = ancestors.union({course_code})
        subgraph = G.subgraph(subgraph_nodes)
        
        nodes = [Node(id=n) for n in subgraph.nodes]
        edges = [Edge(source=u, target=v) for u, v in subgraph.edges]
        
        return GetPrerequisiteGraphOutput(nodes=nodes, edges=edges)
        
    finally:
        db.close()
