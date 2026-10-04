import os
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
    <title>J.A.R.V.I.S.</title>
    <style>
        body { background-color: #050b14; color: #00ffff; font-family: 'Courier New', monospace; margin: 0; padding: 20px; display: flex; flex-direction: column; height: 100vh; box-sizing: border-box; }
        h1 { text-align: center; font-size: 1.5rem; text-shadow: 0 0 10px #00ffff; margin-bottom: 10px; }
        #chat-container { flex: 1; border: 1px solid #00ffff; border-radius: 5px; padding: 15px; overflow-y: auto; background: rgba(0, 20, 40, 0.8); box-shadow: inset 0 0 15px rgba(0,255,255,0.2); margin-bottom: 15px; display: flex; flex-direction: column; gap: 10px; }
        .message { padding: 10px 15px; border-radius: 4px; max-width: 80%; line-height: 1.4; word-break: break-word; }
        .user-message { background: rgba(0, 100, 150, 0.4); border: 1px solid #00aaff; align-self: flex-end; color: #ffffff; }
        .jarvis-message { background: rgba(0, 255, 255, 0.1); border: 1px solid #00ffff; align-self: flex-start; color: #00ffff; box-shadow: 0 0 5px rgba(0,255,255,0.1); }
        .input-area { display: flex; gap: 10px; }
        input[type="text"] { flex: 1; background: #020d1a; border: 1px solid #00ffff; color: #00ffff; padding: 12px; border-radius: 4px; font-family: 'Courier New', monospace; font-size: 1rem; outline: none; }
        input[type="text"]::placeholder { color: rgba(0,255,255,0.4); }
        button { background: #00ffff; color: #020d1a; border: none; padding: 0 20px; border-radius: 4px; font-weight: bold; font-family: 'Courier New', monospace; cursor: pointer; text-shadow: none; transition: 0.2s; }
        button:hover { background: #00b3b3; box-shadow: 0 0 10px #00ffff; }
    </style>
</head>
<body>
    <h1>J.A.R.V.I.S. SYSTEM ONLINE</h1>
    <div id="chat-container">
        <div class="message jarvis-message">Hola Señor, sistemas en línea. ¿Qué orden desea ejecutar?</div>
    </div>
    <div class="input-area">
        <input type="text" id="user-input" placeholder="Escribe una orden para JARVIS..." autofocus>
        <button onclick="sendMessage()">Enviar</button>
    </div>

    <script>
        const inputField = document.getElementById('user-input');
        inputField.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') { sendMessage(); }
        });

        async function sendMessage() {
            const text = inputField.value.trim();
            if (!text) return;

            const chatContainer = document.getElementById('chat-container');
            
            // Mensaje del usuario
            const userDiv = document.createElement('div');
            userDiv.className = 'message user-message';
            userDiv.textContent = text;
            chatContainer.appendChild(userDiv);
            
            inputField.value = '';
            chatContainer.scrollTop = chatContainer.scrollHeight;

            // Mensaje temporal de espera
            const jarvisDiv = document.createElement('div');
            jarvisDiv.className = 'message jarvis-message';
            jarvisDiv.textContent = 'Procesando orden...';
            chatContainer.appendChild(jarvisDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                if (data.reply) {
                    jarvisDiv.textContent = data.reply;
                } else {
                    jarvisDiv.textContent = 'Lo siento Señor, mis circuitos cognitivos experimentaron una breve interrupción con la API.';
                }
            } catch (error) {
                jarvisDiv.textContent = 'Error de conexión con el núcleo central.';
            }
            chatContainer.scrollTop = chatContainer.scrollHeight;
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
    try:
        user_message = request.json.get('message', '')
        if not user_message:
            return jsonify({'reply': 'No se ha recibido ninguna instrucción, Señor.'})
        
        # Llamada al modelo oficial de Gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
        )
        return jsonify({'reply': response.text})
    except Exception as e:
        return jsonify({'reply': f'Lo siento Señor, mis circuitos cognitivos experimentaron una breve interrupción con la API.'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
