import os
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JARVIS - Panel de Control</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0b0f19;
            color: #38bdf8;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            height: 100vh;
            box-sizing: border-box;
        }
        h1 {
            margin: 10px 0;
            text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
        }
        .chat-container {
            width: 100%;
            max-width: 500px;
            background: #111827;
            border: 1px solid #1e3a8a;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            height: 70vh;
            box-shadow: 0 0 20px rgba(30, 58, 138, 0.5);
            overflow: hidden;
        }
        .chat-messages {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .message {
            padding: 10px 15px;
            border-radius: 8px;
            max-width: 80%;
            word-wrap: break-word;
        }
        .user-message {
            background: #1e3a8a;
            color: #fff;
            align-self: flex-end;
        }
        .jarvis-message {
            background: #1f2937;
            color: #38bdf8;
            align-self: flex-start;
            border: 1px solid #38bdf8;
        }
        .chat-input-container {
            display: flex;
            padding: 10px;
            background: #0f172a;
            border-top: 1px solid #1e3a8a;
        }
        input {
            flex: 1;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #38bdf8;
            background: #0b0f19;
            color: #fff;
            outline: none;
        }
        button {
            background: #38bdf8;
            color: #0b0f19;
            border: none;
            padding: 10px 20px;
            margin-left: 8px;
            border-radius: 5px;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover {
            background: #0ea5e9;
        }
    </style>
</head>
<body>
    <h1>J.A.R.V.I.S.</h1>
    <div class="chat-container">
        <div class="chat-messages" id="chat-messages">
            <div class="message jarvis-message">Hola Señor, sistemas en línea. ¿Qué orden desea ejecutar?</div>
        </div>
        <div class="chat-input-container">
            <input type="text" id="user-input" placeholder="Escribe una orden para JARVIS..." onkeydown="if(event.key === 'Enter') sendMessage()">
            <button onclick="sendMessage()">Enviar</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const text = input.value.trim();
            if (!text) return;

            const messagesDiv = document.getElementById('chat-messages');
            messagesDiv.innerHTML += `<div class="message user-message">${text}</div>`;
            input.value = '';
            messagesDiv.scrollTop = messagesDiv.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                messagesDiv.innerHTML += `<div class="message jarvis-message">${data.reply}</div>`;
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            } catch (error) {
                messagesDiv.innerHTML += `<div class="message jarvis-message">Error de conexión con los servidores principales, Señor.</div>`;
            }
        }
    </script>
</body>
</html>
"""


@app.route("/")
def home():
  return render_template_string(HTML_TEMPLATE)


@app.route("/chat", methods=["POST"])
def chat():
  user_data = request.get_json()
  user_message = user_data.get("message", "").lower()

  # Inteligencia ampliada de JARVIS
  if "hola" in user_message or "saludos" in user_message:
    reply = (
        "Hola Señor. Es un placer verle de nuevo. Todos los sistemas operativos"
        " funcionan al 100%."
    )
  elif "estado" in user_message or "diagnóstico" in user_message:
    reply = (
        "Diagnóstico del sistema: Servidores en Render estables, núcleo Flask"
        " operativo y enlace web seguro al 100%, Señor."
    )
  elif "protocolo" in user_message:
    reply = (
        "Entendido, Señor. Activando protocolos de seguridad y optimización"
        " de recursos."
    )
  elif "creador" in user_message or "quién te creó" in user_message:
    reply = (
        "Fui creado por usted, Señor, con la asistencia de los mejores sistemas"
        " de desarrollo."
    )
  else:
    reply = (
        f"Comando '{user_message}' procesado en los servidores. Mis"
        " capacidades cognitivas siguen expandiéndose, Señor."
    )

  return jsonify({"reply": reply})


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
