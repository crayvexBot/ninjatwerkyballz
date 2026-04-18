from flask import Flask, request, redirect, url_for, render_template_string, session
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# 🔐 SECRET KEY (Render env)
app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("SECRET_KEY is not set!")

# ---------------- FILE STORAGE ----------------
USER_FILE = "users.json"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ---------------- STYLE ----------------
STYLE = """
<style>
body {
    margin: 0;
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
}

.container {
    background: rgba(255, 255, 255, 0.05);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    box-shadow: 0 0 30px rgba(155, 89, 255, 0.5);
    text-align: center;
    width: 100%;
    max-width: 360px;
}

input {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    border-radius: 10px;
    border: none;
    background: rgba(255,255,255,0.1);
    color: white;
}

button {
    width: 100%;
    padding: 12px;
    border-radius: 12px;
    border: none;
    background: #9b59ff;
    color: white;
    cursor: pointer;
    box-shadow: 0 0 15px #9b59ff;
}

button:hover {
    box-shadow: 0 0 25px #b784ff;
}

.discord-btn {
    background: #5865F2;
    box-shadow: 0 0 20px #5865F2;
}

h1 {
    text-shadow: 0 0 15px #9b59ff;
}
</style>
"""

# ---------------- ROUTES ----------------

@app.route("/", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        users = load_users()

        if username in users and check_password_hash(users[username], password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"

    return render_template_string(f"""
    {STYLE}
    <div class="container">
        <h1>Login</h1>
        <form method="POST">
            <input name="username" placeholder="Username" required>
            <input name="password" type="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <p style="color:red;">{error}</p>
        <p><a href="/signup">Create account</a></p>
    </div>
    """)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        users = load_users()

        if username in users:
            error = "Username already exists!"
        else:
            users[username] = generate_password_hash(password)
            save_users(users)
            return redirect(url_for("login"))

    return render_template_string(f"""
    {STYLE}
    <div class="container">
        <h1>Sign Up</h1>
        <form method="POST">
            <input name="username" placeholder="Username" required>
            <input name="password" type="password" placeholder="Password" required>
            <button type="submit">Sign Up</button>
        </form>
        <p style="color:red;">{error}</p>
        <p><a href="/">Back to login</a></p>
    </div>
    """)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template_string(f"""
    {STYLE}
    <div class="container">
        <h1>Welcome, {{session['user']}}</h1>
        <p>Join Our Discord Today!</p>
        <a href="https://discord.gg/NinjaTurky" target="_blank">
            <button class="discord-btn">Join</button>
        </a>
        <br><br>
        <a href="/logout">Logout</a>
    </div>
    """)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# IMPORTANT: keep this for local testing, ignored by gunicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
