import os
import time
from flask import Flask, render_template_string, request, jsonify
from google import genai

app = Flask(__name__)

# Inicializar el cliente de Gemini usando la variable de entorno configurada en Render
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Interfaz HTML/CSS integrada para JARVIS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>J.A.R.V.I.S. - Panel de Control</title>
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
            text-align: center;
            font-size: 1.5rem;
            text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
            margin-bottom: 10px;
        }
        #chat-container {
            flex: 1;
            width: 100%;
            max-width: 500px;
            background: rgba(0, 20, 40, 0.8);
            border: 1px solid #1e3a8a;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
            margin-bottom: 15px;
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
            word-break: break-word;
            font-size: 0.95rem;
            line-height: 1.4;
        }
        .user-message {
            background: rgba(0, 100, 150, 0.4);
            border: 1px solid #38bdf8;
            color: #fff;
            align-self: flex-end;
        }
        .jarvis-message {
            background: #1f2937;
            border: 1px solid #38bdf8;
            color: #38bdf8;
            align-self: flex-start;
        }
        .input-area {
            display: flex;
            padding: 10px;
            background: #0f172a;
            border-top: 1px solid #1e3a8a;
        }
        input[type="text"] {
            flex: 1;
            padding: 10px;
            border: 1px solid #00ffff;
            border-radius: 4px;
            background: #000fff;
            color: #00ffff;
            font-family: 'Courier New', monospace;
            font-size: 1rem;
            outline: none;
        }
        input[type="text"]::placeholder {
            color: rgba(0, 255, 255, 0.4);
        }
        button {
            background: #000f19;
            border: 1px solid #00ffff;
            color: #00ffff;
            padding: 10px 20px;
            margin-left: 5px;
            border-radius: 4px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
        }
        button:hover {
            background: #0ea5e9;
            color: #fff;
        }
    </style>
</head>
<body>
    <h1>J.A.R.V.I.S. SYSTEM ONLINE</h1>
    <div id="chat-container">
        <div class="chat-messages" id="chat-messages">
            <div class="message jarvis-message" id="welcome-msg">Hola Señor, sistemas en línea. ¿Qué orden desea ejecutar?</div>
        </div>
        <div class="input-area">
            <input type="text" id="user-input" placeholder="Escribe una orden para JARVIS..." autofocus onkeydown="if(event.key === 'Enter') sendMessage()">
            <button onclick="sendMessage()">Enviar</button>
        </div>
    </div>

    <script>
        function speak(text) {
            if ('SpeechSynthesis' in window) {
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
        }

        async function sendMessage() {
            const inputField = document.getElementById('user-input');
            const text = inputField.value.trim();
            if (!text) return;

            const messagesDiv = document.getElementById('chat-messages');
            
            const userDiv = document.createElement('div');
            userDiv.className = 'message user-message';
            userDiv.textContent = text;
            messagesDiv.appendChild(userDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            
            inputField.value = '';

            const jarvisDiv = document.createElement('div');
            jarvisDiv.className = 'message jarvis-message';
            jarvisDiv.textContent = 'Procesando orden...';
            messagesDiv.appendChild(jarvisDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                
                messagesDiv.lastChild.remove();
                
                const replyDiv = document.createElement('div');
                replyDiv.className = 'message jarvis-message';
                replyDiv.textContent = data.reply;
                messagesDiv.appendChild(replyDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;

                speak(data.reply);

            } catch (error) {
                messagesDiv.lastChild.remove();
                const errorDiv = document.createElement('div');
                errorDiv.className = 'message jarvis-message';
                errorDiv.textContent = 'Error de conexión con el núcleo central.';
                messagesDiv.appendChild(errorDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'reply': 'No se ha recibido ninguna instrucción, Señor.'})

    prompt_sistema = (
        "Eres J.A.R.V.I.S., la avanzada inteligencia artificial de Tony Stark. "
        "Respondes siempre en español de manera educada, leal, ligeramente irónica "
        "y muy profesional, refiriéndote al usuario como 'Señor'. "
        "Mantén las respuestas concisas (ideales para ser leídas en voz alta)."
    )

    # Sistema de reintentos automáticos para evitar errores 503 por saturación temporal
    intentos = 3
    for intento in range(intentos):
        try:
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=[prompt_sistema, "\nInstrucción del usuario: ", user_message]
            )
            return jsonify({'reply': response.text})
        except Exception as e:
            if intento < intentos - 1:
                time.sleep(1) # Espera 1 segundo antes de reintentar
                continue
            else:
                return jsonify({'reply': f'Error técnico: {str(e)}'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
