"""
Scholarship Eligibility Finder — Flask backend (MongoDB)

Setup:
    1. pip install -r requirements.txt
    2. Make sure MongoDB is running locally (or set MONGO_URI to Atlas/remote).
    3. python seed_db.py      -> creates sample scholarships + a demo admin login
    4. python app.py
    5. Open http://127.0.0.1:5000
"""

import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-this")

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["scholarship_finder"]

students = db["students"]
admins = db["admins"]
scholarships = db["scholarships"]
applications = db["applications"]


# ---------- Public pages ----------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/eligibility", methods=["GET", "POST"])
def eligibility():
    if request.method == "GET":
        return render_template("eligibility.html")

    criteria = {
        "marks": float(request.form.get("marks") or 0),
        "course": request.form.get("course") or "any",
        "income": _income_upper_bound(request.form.get("income")),
        "category": request.form.get("category") or "any",
        "state": request.form.get("state") or "",
        "gender": request.form.get("gender") or "any",
        "disability": request.form.get("disability") == "yes",
        "first_gen": request.form.get("first-gen") == "yes",
    }
    session["last_criteria"] = criteria

    matches = find_matches(criteria)
    return render_template("results.html", matches=matches)


def _income_upper_bound(income_range):
    """Convert the dropdown value (e.g. '2.5-6l') to a numeric income for comparison."""
    mapping = {
        "under-1l": 100000,
        "1-2.5l": 250000,
        "2.5-6l": 600000,
        "6-8l": 800000,
        "over-8l": 999999999,
    }
    return mapping.get(income_range, 999999999)


def find_matches(criteria):
    """Query MongoDB for scholarships whose eligibility rules the student satisfies."""
    query = {
        "status": "active",
        "min_marks": {"$lte": criteria["marks"]},
        "max_income": {"$gte": criteria["income"]},
        "course_type": {"$in": ["any", criteria["course"]]},
        "category": {"$in": ["any", criteria["category"]]},
        "gender": {"$in": ["any", criteria["gender"]]},
    }
    if not criteria.get("disability"):
        query["requires_disability"] = False
    if not criteria.get("first_gen"):
        query["requires_first_gen"] = False

    return list(scholarships.find(query).sort("deadline", 1))


@app.route("/results")
def results():
    criteria = session.get("last_criteria")
    matches = find_matches(criteria) if criteria else []
    return render_template("results.html", matches=matches)


# ---------- Auth ----------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    admin = admins.find_one({"email": email})
    if admin and check_password_hash(admin["password_hash"], password):
        session["admin_id"] = str(admin["_id"])
        return redirect(url_for("admin_dashboard"))

    student = students.find_one({"email": email})
    if student and check_password_hash(student["password_hash"], password):
        session["student_id"] = str(student["_id"])
        return redirect(url_for("student_dashboard"))

    flash("Incorrect email or password.")
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------- Dashboards ----------

@app.route("/student-dashboard")
def student_dashboard():
    student_id = session.get("student_id")
    if not student_id:
        return redirect(url_for("login"))

    student = students.find_one({"_id": ObjectId(student_id)})

    matches = find_matches({
        "marks": float(student.get("marks") or 0),
        "course": student.get("course", "any"),
        "income": float(student.get("income") or 0),
        "category": student.get("category", "any"),
        "state": student.get("state", ""),
        "gender": student.get("gender", "any"),
        "disability": student.get("disability", False),
        "first_gen": student.get("first_gen", False),
    })

    return render_template("student-dashboard.html", student=student, matches=matches)


@app.route("/admin-dashboard")
def admin_dashboard():
    if not session.get("admin_id"):
        return redirect(url_for("login"))

    student_count = students.count_documents({})
    scholarship_count = scholarships.count_documents({"status": "active"})
    recent_scholarships = list(scholarships.find().sort("_id", -1).limit(10))

    return render_template(
        "admin-dashboard.html",
        student_count=student_count,
        scholarship_count=scholarship_count,
        scholarships=recent_scholarships,
    )


if __name__ == "__main__":
    app.run(debug=True)
