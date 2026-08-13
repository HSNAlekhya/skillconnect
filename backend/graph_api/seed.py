from .database import execute_query


def seed_database():
    # Clear existing data
    execute_query("""
        MATCH (n)
        DETACH DELETE n
    """)

    # Create people
    execute_query("""
        CREATE
        (:Person {name: 'Alice'}),
        (:Person {name: 'John'}),
        (:Person {name: 'Sarah'}),
        (:Person {name: 'David'}),
        (:Person {name: 'Priya'})
    """)

    # Create skills
    execute_query("""
        CREATE
        (:Skill {name: 'Python'}),
        (:Skill {name: 'Django'}),
        (:Skill {name: 'React'}),
        (:Skill {name: 'Java'}),
        (:Skill {name: 'SQL'}),
        (:Skill {name: 'Machine Learning'}),
        (:Skill {name: 'JavaScript'}),
        (:Skill {name: 'AWS'})
    """)

    # Create jobs
    execute_query("""
        CREATE
        (:Job {title: 'Full Stack Developer'}),
        (:Job {title: 'Python Developer'}),
        (:Job {title: 'Frontend Developer'}),
        (:Job {title: 'Data Scientist'}),
        (:Job {title: 'Backend Developer'}),
        (:Job {title: 'Cloud Engineer'})
    """)

    # Create companies
    execute_query("""
        CREATE
        (:Company {name: 'TechCorp'}),
        (:Company {name: 'DataWorks'}),
        (:Company {name: 'CloudLabs'}),
        (:Company {name: 'WebSolutions'})
    """)

    # Person → Skill
    execute_query("""
        MATCH
        (alice:Person {name: 'Alice'}),
        (john:Person {name: 'John'}),
        (sarah:Person {name: 'Sarah'}),
        (david:Person {name: 'David'}),
        (priya:Person {name: 'Priya'}),

        (python:Skill {name: 'Python'}),
        (django:Skill {name: 'Django'}),
        (react:Skill {name: 'React'}),
        (java:Skill {name: 'Java'}),
        (sql:Skill {name: 'SQL'}),
        (ml:Skill {name: 'Machine Learning'}),
        (javascript:Skill {name: 'JavaScript'}),
        (aws:Skill {name: 'AWS'})

        CREATE
        (alice)-[:HAS_SKILL]->(python),
        (alice)-[:HAS_SKILL]->(django),
        (alice)-[:HAS_SKILL]->(react),

        (john)-[:HAS_SKILL]->(java),
        (john)-[:HAS_SKILL]->(sql),

        (sarah)-[:HAS_SKILL]->(python),
        (sarah)-[:HAS_SKILL]->(sql),
        (sarah)-[:HAS_SKILL]->(ml),

        (david)-[:HAS_SKILL]->(javascript),
        (david)-[:HAS_SKILL]->(react),

        (priya)-[:HAS_SKILL]->(python),
        (priya)-[:HAS_SKILL]->(aws)
    """)

    # Job → Skill
    execute_query("""
        MATCH
        (fullstack:Job {title: 'Full Stack Developer'}),
        (pythonjob:Job {title: 'Python Developer'}),
        (frontend:Job {title: 'Frontend Developer'}),
        (datascientist:Job {title: 'Data Scientist'}),
        (backend:Job {title: 'Backend Developer'}),
        (cloud:Job {title: 'Cloud Engineer'}),

        (python:Skill {name: 'Python'}),
        (django:Skill {name: 'Django'}),
        (react:Skill {name: 'React'}),
        (javascript:Skill {name: 'JavaScript'}),
        (sql:Skill {name: 'SQL'}),
        (ml:Skill {name: 'Machine Learning'}),
        (aws:Skill {name: 'AWS'})

        CREATE
        (fullstack)-[:REQUIRES]->(python),
        (fullstack)-[:REQUIRES]->(react),

        (pythonjob)-[:REQUIRES]->(python),
        (pythonjob)-[:REQUIRES]->(django),

        (frontend)-[:REQUIRES]->(react),
        (frontend)-[:REQUIRES]->(javascript),

        (datascientist)-[:REQUIRES]->(python),
        (datascientist)-[:REQUIRES]->(sql),
        (datascientist)-[:REQUIRES]->(ml),

        (backend)-[:REQUIRES]->(python),
        (backend)-[:REQUIRES]->(django),

        (cloud)-[:REQUIRES]->(aws)
    """)

    # Company → Job
    execute_query("""
        MATCH
        (techcorp:Company {name: 'TechCorp'}),
        (dataworks:Company {name: 'DataWorks'}),
        (cloudlabs:Company {name: 'CloudLabs'}),
        (websolutions:Company {name: 'WebSolutions'}),

        (fullstack:Job {title: 'Full Stack Developer'}),
        (pythonjob:Job {title: 'Python Developer'}),
        (frontend:Job {title: 'Frontend Developer'}),
        (datascientist:Job {title: 'Data Scientist'}),
        (backend:Job {title: 'Backend Developer'}),
        (cloud:Job {title: 'Cloud Engineer'})

        CREATE
        (techcorp)-[:POSTED]->(fullstack),
        (techcorp)-[:POSTED]->(backend),

        (dataworks)-[:POSTED]->(datascientist),
        (dataworks)-[:POSTED]->(pythonjob),

        (cloudlabs)-[:POSTED]->(cloud),

        (websolutions)-[:POSTED]->(frontend),
        (websolutions)-[:POSTED]->(pythonjob)
    """)

    print("SkillConnect database seeded successfully!")


if __name__ == "__main__":
    seed_database()