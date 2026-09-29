import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "carepoint-health-secret-key-2026-capstone")

# Demo Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "HospitalAdmin@2026"


@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid medical staff credentials. Access denied.", "danger")
            return render_template("login.html"), 401

    if "user" in session:
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    department_stats = {
        "emergency_beds": "88% Occupied",
        "icu_capacity": "14 / 20 Available",
        "duty_physicians": "32 On Call",
        "pending_triage": "3 Urgent Cases"
    }

    return render_template(
        "dashboard.html",
        username=session["user"],
        stats=department_stats
    )


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/health")
def health():
    return jsonify({
        "status": "HEALTHY",
        "service": "hospital-auth",
        "uptime": "ok"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
