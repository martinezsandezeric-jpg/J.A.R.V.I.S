import os
from flask import Flask, jsonify, render_template_string, request
from google import genai

app = Flask(__name__)

# Inicializar el cliente de Gemini con la variable de entorno
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

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
            <div class="message jarvis-message" id="welcome-msg">Hola Señor, sistemas en línea. ¿Qué orden desea ejecutar?</div>
        </div>
        <div class="chat-input-container">
            <input type="text" id="user-input" placeholder="Escribe una orden para JARVIS..." onkeydown="if(event.key === 'Enter') sendMessage()">
            <button onclick="sendMessage()">Enviar</button>
        </div>
    </div>

    <script>
        function speak(text) {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'es-ES';
                utterance.rate = 1.0;
                utterance.pitch = 0.9;
                window.speechSynthesis.speak(utterance);
            }
        }

        window.onload = () => {
            const welcomeText = document.getElementById('welcome-msg').innerText;
            setTimeout(() => speak(welcomeText), 1000);
        };

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
                speak(data.reply);

            } catch (error) {
                const errorMsg = "Error de conexión con los servidores principales, Señor.";
                messagesDiv.innerHTML += `<div class="message jarvis-message">${errorMsg}</div>`;
                speak(errorMsg);
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
  user_message = user_data.get("message", "")

  if not user_message:
    return jsonify({"reply": "No he recibido ninguna instrucción, Señor."})

  try:
    prompt_sistema = (
        "Eres J.A.R.V.I.S., la avanzada inteligencia artificial de Tony"
        " Stark. Respondes siempre en español de manera educada, leal,"
        " ligeramente irónica y muy profesional, refiriéndote al usuario"
        " como 'Señor'. Mantén las respuestas concisas (ideales para ser"
        " leídas en voz alta)."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{prompt_sistema}\n\nInstrucción del usuario: {user_message}",
    )
    reply = response.text
  except Exception as e:
    reply = (
        "Lo siento Señor, mis circuitos cognitivos experimentaron una breve"
        " interrupción con la API."
    )

  return jsonify({"reply": reply})


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)
