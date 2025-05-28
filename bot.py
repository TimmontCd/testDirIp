from flask import Flask, request, redirect
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return redirect("/track")

@app.route("/track")
def track():
    now = datetime.now()
    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    print(f"[{now.strftime("%Y-%m-%d %H:%M:%S")}] IP registrada: {user_ip}")
    return redirect("https://www.facebook.com")  # Cambia el enlace por donde quieras redirigir

app.run(host="0.0.0.0", port=3000)
