# SkillConnect

SkillConnect is a graph-powered career discovery application built using React, Django, and CognoDB.

The application allows users to select a person and explore:

- Their skills
- Jobs matching those skills
- Companies offering those jobs
- Connections between people, skills, jobs, and companies

---

## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- Django
- Official Neo4j Python Driver

### Database

- CognoDB Cloud
- openCypher
- Bolt protocol

---

## Why a Graph Database?

SkillConnect is a relationship-focused application.

The important questions are not only:

> "What skills does Alice have?"

but also:

> "Which jobs require Alice's skills, and which companies have those jobs?"

This requires traversing multiple relationships:

```text
Person
   ↓
HAS_SKILL
   ↓
Skill
   ↓
REQUIRES
   ↓
Job
   ↓
POSTED
   ↓
Company
```

A relational database could represent this using multiple tables and join tables. However, as the number of relationships grows, queries involving multiple connections become increasingly dependent on joins.

A graph database represents these relationships directly.

For example:

```text
Alice → Python → Backend Developer → TechCorp
```

can be traversed naturally using Cypher.

This makes graph traversal the central part of SkillConnect rather than an additional operation on top of tabular data.

---

# Graph Data Model

The application uses the following nodes and relationships.

## Nodes

### Person

Properties:

```text
name
```

### Skill

Properties:

```text
name
```

### Job

Properties:

```text
title
```

### Company

Properties:

```text
name
```

## Relationships

```text
(Person)-[:HAS_SKILL]->(Skill)

(Job)-[:REQUIRES]->(Skill)

(Company)-[:POSTED]->(Job)
```

## Data Model Diagram

```text
                 HAS_SKILL
      Person ─────────────────> Skill
                                  ▲
                                  │
                               REQUIRES
                                  │
                                  │
                                Job
                                  ▲
                                  │
                               POSTED
                                  │
                                  │
                               Company
```

---

# Example Graph

For example:

```text
Alice
  │
  ├── HAS_SKILL ──> Python
  │
  ├── HAS_SKILL ──> React
  │
  └── HAS_SKILL ──> Django

Python
   ▲
   │ REQUIRES
   │
Backend Developer
   ▲
   │ POSTED
   │
TechCorp
```

This allows SkillConnect to discover career opportunities through relationships.

---

# Main Graph Queries

## 1. Find all people

```cypher
MATCH (p:Person)
RETURN p.name AS name
ORDER BY p.name
```

---

## 2. Find a person's skills

```cypher
MATCH (p:Person {name: $name})-[:HAS_SKILL]->(s:Skill)
RETURN s.name AS skill
ORDER BY s.name
```

The `$name` parameter is supplied separately through the Neo4j driver.

---

## 3. Find matching jobs

This is a multi-hop graph query:

```cypher
MATCH (p:Person {name: $name})
      -[:HAS_SKILL]->(s:Skill)
      <-[:REQUIRES]-(j:Job)

RETURN DISTINCT j.title AS job
ORDER BY j.title
```

The traversal is:

```text
Person → Skill → Job
```

---

## 4. Find matching companies

This query goes across multiple relationships:

```cypher
MATCH (p:Person {name: $name})
      -[:HAS_SKILL]->(s:Skill)
      <-[:REQUIRES]-(j:Job)
      <-[:POSTED]-(c:Company)

RETURN DISTINCT
       c.name AS company,
       j.title AS job

ORDER BY c.name, j.title
```

The traversal is:

```text
Person
   ↓
Skill
   ↓
Job
   ↓
Company
```

This is one of the main reasons a graph database is useful for this application.

---

# Parameterised Queries

All user-dependent Cypher queries use parameters.

For example:

```python
query = """
MATCH (p:Person {name: $name})
      -[:HAS_SKILL]->(s:Skill)
RETURN s.name AS skill
"""

result = execute_query(
    query,
    {"name": name}
)
```

User input is never concatenated directly into Cypher queries.

---

# Application Architecture

```text
┌─────────────────────┐
│    React Frontend   │
│                     │
│  SkillConnect UI    │
└──────────┬──────────┘
           │
           │ HTTP
           ↓
┌─────────────────────┐
│   Django Backend    │
│                     │
│     REST APIs       │
└──────────┬──────────┘
           │
           │ Cypher
           ↓
┌─────────────────────┐
│      CognoDB        │
│                     │
│   Graph Database    │
└─────────────────────┘
```

---

# Project Structure

```text
skillconnect/
│
├── backend/
│   ├── config/
│   ├── graph_api/
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── seed_graph.py
│   │   ├── database.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── manage.py
│   ├── test_cognodb.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# Local Setup

## 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd skillconnect
```

---

# Backend Setup

Open a terminal:

```bash
cd backend
```

Create and activate a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# CognoDB Setup

Create a free CognoDB Cloud instance.

You will receive:

```text
bolt+s://YOUR-INSTANCE.databases.cognodb.cloud
```

Create a `.env` file inside `backend`:

```text
COGNODB_URI=bolt+s://YOUR-INSTANCE.databases.cognodb.cloud
COGNODB_USERNAME=cognodb
COGNODB_PASSWORD=YOUR_PASSWORD
```

Never commit `.env` to GitHub.

---

# Seed the Database

From the `backend` directory:

```bash
python manage.py seed_graph
```

This loads realistic sample data into CognoDB.

---

# Test the Database

Run:

```bash
python test_cognodb.py
```

A successful connection should display:

```text
CognoDB connection successful!
```

---

# Start Django

Run:

```bash
python manage.py runserver
```

The backend will be available at:

```text
http://127.0.0.1:8000/
```

---

# API Endpoints

### People

```text
GET /api/people/
```

### Skills

```text
GET /api/skills/
```

### Jobs

```text
GET /api/jobs/
```

### Companies

```text
GET /api/companies/
```

### Person skills

```text
GET /api/people/<name>/skills/
```

### Job recommendations

```text
GET /api/people/<name>/recommendations/
```

### Company recommendations

```text
GET /api/people/<name>/companies/
```

---

# Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173/
```

---

# Error Handling

The application handles database/API failures gracefully.

If the backend cannot connect to CognoDB, the frontend displays an error message instead of failing silently.

Loading states are also displayed while graph data is being retrieved.

---

# Screenshots

Screenshots of the completed application will be added here.

## Home Screen

_Add screenshot here._

## Person Career Graph

_Add screenshot here._

## Job and Company Recommendations

_Add screenshot here._

---

# Hosted Demo

Demo:

_Add deployed application URL here._

---

# Screen Recording

A short demonstration of the application will be provided with the submission.

---

# Assignment

This project was developed as a take-home assignment for Wexa AI.

The application demonstrates:

- Graph data modeling
- CognoDB integration
- openCypher queries
- Multi-hop graph traversal
- Parameterised database queries
- Django backend development
- React frontend development
- Error handling
- Responsive UI