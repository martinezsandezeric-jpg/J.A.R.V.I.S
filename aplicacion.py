import os
from flask import Flask, render_template_string, request, jsonify
import vertexai
from vertexai.generative_models import GenerativeModel

app = Flask(__name__)

# Inicialización nativa de Vertex AI (Google Cloud)
# Detecta automáticamente el proyecto y la región del entorno Cloud Run
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "tu-proyecto-id")
LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

try:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    # Modelo oficial y estable de la infraestructura de Google Cloud
    cloud_model = GenerativeModel("gemini-1.5-flash")
except Exception as e:
    cloud_model = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>J.A.R.V.I.S. - Cloud System</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #0b0f19; color: #38bdf8; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; height: 100vh; box-sizing: border-box; }
        h1 { text-align: center; font-size: 1.5rem; text-shadow: 0 0 10px rgba(56, 189, 248, 0.5); }
        #chat-container { flex: 1; width: 100%; max-width: 500px; background: rgba(0, 20, 40, 0.8); border: 1px solid #1e3a8a; border-radius: 10px; display: flex; flex-direction: column; overflow: hidden; }
        .chat-messages { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .message { padding: 10px 15px; border-radius: 8px; max-width: 80%; word-break: break-word; font-size: 0.95rem; }
        .user-message { background: rgba(0, 100, 150, 0.4); border: 1px solid #38bdf8; color: #fff; align-self: flex-end; }
        .jarvis-message { background: #1f2937; border: 1px solid #38bdf8; color: #38bdf8; align-self: flex-start; }
        .input-area { display: flex; padding: 10px; background: #0f172a; border-top: 1px solid #1e3a8a; }
        input[type="text"] { flex: 1; padding: 10px; border: 1px solid #38bdf8; border-radius: 4px; background: #0b0f19; color: #38bdf8; outline: none; }
        button { background: #0b0f19; border: 1px solid #38bdf8; color: #38bdf8; padding: 10px 20px; margin-left: 5px; border-radius: 4px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <h1>J.A.R.V.I.S. CLOUD NATIVE</h1>
    <div id="chat-container">
        <div class="chat-messages" id="chat-messages">
            <div class="message jarvis-message" id="welcome-msg">Sistemas en línea, Señor. Núcleo Cloud conectado. ¿Qué orden desea ejecutar?</div>
        </div>
        <div class="input-area">
            <input type="text" id="user-input" placeholder="Escribe una orden..." autofocus onkeydown="if(event.key === 'Enter') sendMessage()">
            <button onclick="sendMessage()">Enviar</button>
        </div>
    </div>
    <script>
        function speak(text) {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'es-ES';
                window.speechSynthesis.speak(utterance);
            }
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
            inputField.value = '';

            const jarvisDiv = document.createElement('div');
            jarvisDiv.className = 'message jarvis-message';
            jarvisDiv.textContent = 'Procesando en Google Cloud...';
            messagesDiv.appendChild(jarvisDiv);

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                messagesDiv.lastChild.textContent = data.reply;
                speak(data.reply);
            } catch (error) {
                messagesDiv.lastChild.textContent = 'Error de conexión con el núcleo Cloud.';
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

    if not cloud_model:
        return jsonify({'reply': 'Error: Conexión con Vertex AI no inicializada.'})

    prompt_completo = (
        "Eres J.A.R.V.I.S., la avanzada inteligencia artificial de Tony Stark. "
        "Respondes siempre en español de manera educada, leal, ligeramente irónica "
        "y muy profesional, refiriéndote al usuario como 'Señor'. "
        f"Instrucción del usuario: {user_message}"
    )

    try:
        response = cloud_model.generate_content(prompt_completo)
        return jsonify({'reply': response.text})
    except Exception as e:
        return jsonify({'reply': f'Error en Google Cloud: {str(e)}'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
