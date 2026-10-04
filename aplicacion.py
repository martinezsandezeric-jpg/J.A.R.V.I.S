import os
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
  return """
    <html>
        <head><title>JARVIS</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px; background-color: #0f172a; color: #38bdf8;">
            <h1>¡JARVIS está activo y online!</h1>
            <p>El servidor Flask funciona correctamente en Render.</p>
        </body>
    </html>
    """


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
