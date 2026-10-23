

from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("internship.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            education TEXT NOT NULL,
            skills TEXT NOT NULL,
            location TEXT NOT NULL,
            interest TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()
@app.route("/login")
def login():
    return """
    <h1>PM Internship Scheme</h1>
    <h2>Login Portal</h2>
    <a href="/candidate-login">Candidate Login</a><br><br>
    <a href="/company-login">Company Login</a><br><br>
    <a href="/admin-login">Admin Login</a>
    """
@app.route("/candidate-login")
def candidate_login():
    return """
    <h1>Candidate Login</h1>
    <form>
        <p>Email: <input type="email" required></p>
        <p>Password: <input type="password" required></p>
        <button type="submit">Login</button>
    </form>
    <a href="/login">Back to Login Portal</a>
    """
@app.route("/company-login")
def company_login():
    return """
    <h1>Company Login</h1>
    <form>
        <p>Email: <input type="email" required></p>
        <p>Password: <input type="password" required></p>
        <button type="submit">Login</button>
    </form>
    <a href="/login">Back to Login Portal</a>
    """
@app.route("/admin-login")
def admin_login():
    return """
    <h1>Admin Login</h1>
    <form>
        <p>Email: <input type="email" required></p>
        <p>Password: <input type="password" required></p>
        <button type="submit">Login</button>
    </form>
    <a href="/login">Back to Login Portal</a>
    """
@app.route("/")
def home():
    return render_template_string("""
    <h1>AI-Based Smart Allocation</h1>
    <h2>PM Internship Scheme</h2>
    <p>Welcome to the Internship Allocation Portal!</p>

    <h3>Candidate Registration</h3>
    <form action="/register" method="POST">
        <p>Full Name: <input name="name" required></p>
        <p>Education: <input name="education" required></p>
        <p>Skills: <input name="skills" required></p>
        <p>Preferred Location: <input name="location" required></p>
        <p>Internship Interest: <input name="interest" required></p>
        <button type="submit">Register</button>
    </form>

    <p><a href="/candidates">View Registered Candidates</a></p>
    """)


@app.route("/register", methods=["POST"])
def register():
    conn = sqlite3.connect("internship.db")
    conn.execute("""
        INSERT INTO candidates
        (name, education, skills, location, interest)
        VALUES (?, ?, ?, ?, ?)
    """, (
        request.form["name"],
        request.form["education"],
        request.form["skills"],
        request.form["location"],
        request.form["interest"]
    ))
    conn.commit()
    conn.close()
    return redirect("/candidates")


@app.route("/recommend")
def recommend():
    conn = sqlite3.connect("internship.db")
    conn.row_factory = sqlite3.Row
    candidates = conn.execute(
        "SELECT * FROM candidates"
    ).fetchall()
    conn.close()

    recommendations = []

    for c in candidates:
        skills = c["skills"].lower()
        interest = c["interest"].lower()

        if "java" in skills or "software" in interest:
            internship = "Software Development Internship"
        elif "python" in skills:
            internship = "Python Development Internship"
        else:
            internship = "General IT Internship"

        recommendations.append({
            "name": c["name"],
            "internship": internship
        })

    return render_template_string("""
    <h1>Smart Internship Recommendations</h1>
    {% for r in recommendations %}
        <hr>
        <p>Candidate: {{ r.name }}</p>
        <p>Recommended Internship: {{ r.internship }}</p>
    {% else %}
        <p>No candidates registered yet.</p>
    {% endfor %}
    <a href="/">Back to Home</a>
    """, recommendations=recommendations)



@app.route("/candidates")
def view_candidates():
    conn = sqlite3.connect("internship.db")
    conn.row_factory = sqlite3.Row
    candidates = conn.execute(
        "SELECT * FROM candidates"
    ).fetchall()
    conn.close()

    return render_template_string("""
    <h1>Registered Candidates</h1>
    {% for c in candidates %}
        <hr>
        <p>Name: {{ c['name'] }}</p>
        <p>Education: {{ c['education'] }}</p>
        <p>Skills: {{ c['skills'] }}</p>
        <p>Location: {{ c['location'] }}</p>
        <p>Interest: {{ c['interest'] }}</p>
    {% else %}
        <p>No candidates registered yet.</p>
    {% endfor %}
    <a href="/">Back to Home</a>
    """, candidates=candidates)


if __name__ == "__main__":
    app.run(debug=True)
