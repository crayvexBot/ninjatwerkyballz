from flask import Flask, render_template_string
import os

app = Flask(__name__)

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
    padding: 35px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    box-shadow: 0 0 30px rgba(155, 89, 255, 0.5);
    text-align: center;
    width: 100%;
    max-width: 360px;
    animation: fadeIn 0.8s ease;
}

button {
    width: 100%;
    padding: 14px;
    border-radius: 12px;
    border: none;
    background: #5865F2;
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: 0.25s;
    box-shadow: 0 0 20px #5865F2;
}

button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 30px #7983ff;
}

h1 {
    text-shadow: 0 0 15px #9b59ff;
    font-size: 22px;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(15px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
"""

# ---------------- ROUTE ----------------
@app.route("/")
def home():
    return render_template_string(f"""
    {STYLE}
    <div class="container">
        <h1>Join Our Discord Today!</h1>
        <a href="https://discord.gg/NinjaTurky" target="_blank">
            <button>Join</button>
        </a>
    </div>
    """)

# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
