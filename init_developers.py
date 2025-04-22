from db_utils import db

developers = [
    {
        "name": "Atharv Patil",
        "role": "Documentation and Report",
        "bio": "Responsible for project documentation, technical writing, and report generation.",
        "contributions": "Created comprehensive project documentation, user manuals, and technical reports.",
        "email": "atharv.patil@example.com",
        "linkedin": "https://linkedin.com/in/atharvpatil",
        "github": "https://github.com/atharvpatil"
    },
    {
        "name": "Pranav Chavan",
        "role": "Frontend Developer",
        "bio": "Specialized in creating responsive and user-friendly interfaces.",
        "contributions": "Developed the frontend architecture and implemented user interfaces.",
        "email": "pranav.chavan@example.com",
        "linkedin": "https://linkedin.com/in/pranavchavan",
        "github": "https://github.com/pranavchavan"
    },
    {
        "name": "Karan Ghatage",
        "role": "Idea and system development",
        "bio": "Project visionary and system architect.",
        "contributions": "Conceived the project idea and designed the system architecture.",
        "email": "karan.ghatage@example.com",
        "linkedin": "https://linkedin.com/in/karanghatage",
        "github": "https://github.com/karanghatage"
    },
    {
        "name": "Aary Kulkarni",
        "role": "Backend Developer",
        "bio": "Expert in backend development and database management.",
        "contributions": "Implemented backend services and database architecture.",
        "email": "aary.kulkarni@example.com",
        "linkedin": "https://linkedin.com/in/aarykulkarni",
        "github": "https://github.com/aarykulkarni"
    }
]

def init_developers():
    # Clear existing developers
    db.db.developers.delete_many({})
    
    # Insert new developers
    for developer in developers:
        db.create_developer(developer)
    
    print("Developer profiles initialized successfully!")

if __name__ == "__main__":
    init_developers() 