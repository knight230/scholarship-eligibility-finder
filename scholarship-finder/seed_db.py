"""
Run once to set up sample data:
    python seed_db.py
"""

import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["scholarship_finder"]

scholarships = db["scholarships"]
admins = db["admins"]

scholarships.delete_many({})
scholarships.insert_many([
    {
        "name": "Central Sector Scheme of Scholarship (NSP)",
        "description": "For meritorious students from families with annual income under ₹8,00,000.",
        "course_type": "any",
        "min_marks": 80,
        "max_income": 800000,
        "category": "any",
        "gender": "any",
        "state": "any",
        "requires_disability": False,
        "requires_first_gen": False,
        "amount": "₹20,000",
        "amount_label": "Per year",
        "deadline": "31 Oct",
        "renewable": "Yes, each year",
        "status": "active",
        "apply_url": "https://scholarships.gov.in",
    },
    {
        "name": "AICTE Pragati Scholarship for girls",
        "description": "For girl students in technical diploma or degree courses, family income under ₹8,00,000.",
        "course_type": "engineering",
        "min_marks": 0,
        "max_income": 800000,
        "category": "any",
        "gender": "female",
        "state": "any",
        "requires_disability": False,
        "requires_first_gen": False,
        "amount": "₹50,000",
        "amount_label": "Per year",
        "deadline": "31 Oct",
        "renewable": "Course duration",
        "status": "active",
        "apply_url": "https://scholarships.gov.in",
    },
    {
        "name": "State post-matric scholarship",
        "description": "For SC/ST/OBC/EWS students domiciled in your state, studying full-time.",
        "course_type": "any",
        "min_marks": 0,
        "max_income": 250000,
        "category": "obc",
        "gender": "any",
        "state": "any",
        "requires_disability": False,
        "requires_first_gen": False,
        "amount": "Varies",
        "amount_label": "By state",
        "deadline": "30 days",
        "renewable": "Yes",
        "status": "active",
        "apply_url": "https://scholarships.gov.in",
    },
    {
        "name": "First-generation learner grant",
        "description": "For students who are the first in their family to attend college.",
        "course_type": "any",
        "min_marks": 0,
        "max_income": 999999999,
        "category": "any",
        "gender": "any",
        "state": "any",
        "requires_disability": False,
        "requires_first_gen": True,
        "amount": "₹15,000",
        "amount_label": "One-time",
        "deadline": "20 days",
        "renewable": "No",
        "status": "active",
        "apply_url": "https://www.buddy4study.com",
    },
    {
        "name": "Reliance Foundation UG Scholarship",
        "description": "Private, merit-cum-means scholarship open to undergraduates in any stream.",
        "course_type": "any",
        "min_marks": 60,
        "max_income": 600000,
        "category": "any",
        "gender": "any",
        "state": "any",
        "requires_disability": False,
        "requires_first_gen": False,
        "amount": "₹50,000",
        "amount_label": "Per year",
        "deadline": "Mid-Oct",
        "renewable": "Yes",
        "status": "active",
        "apply_url": "https://www.scholarships.reliancefoundation.org",
    },
    {
        "name": "AICTE Saksham Scholarship",
        "description": "For differently-abled students in technical diploma or degree courses.",
        "course_type": "engineering",
        "min_marks": 0,
        "max_income": 800000,
        "category": "any",
        "gender": "any",
        "state": "any",
        "requires_disability": True,
        "requires_first_gen": False,
        "amount": "₹50,000",
        "amount_label": "Per year",
        "deadline": "31 Oct",
        "renewable": "Course duration",
        "status": "active",
        "apply_url": "https://scholarships.gov.in",
    },
])

# Demo admin login: admin@scholarfind.test / admin123
admins.delete_many({"email": "admin@scholarfind.test"})
admins.insert_one({
    "name": "Demo Admin",
    "email": "admin@scholarfind.test",
    "password_hash": generate_password_hash("admin123"),
})

print(f"Inserted {scholarships.count_documents({})} scholarships.")
print("Demo admin login -> email: admin@scholarfind.test  password: admin123")
