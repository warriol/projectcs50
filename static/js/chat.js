const chatForm = document.getElementById('chat-form');
const chatWindow = document.getElementById('chat-window');
const spinner = document.getElementById('spinner');

chatForm.onsubmit = async (e) => {
    e.preventDefault();
    
    const input = document.getElementById('user-input');
    const selector = document.getElementById('ia-selector');
    const message = input.value;
    const iaType = selector.value;

    // 1. Mostrar pregunta del usuario en el chat inmediatamente
    appendMessage('user', message);
    input.value = '';
    
    // 2. Mostrar spinner y bloquear botón
    spinner.classList.remove('d-none');
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // 3. Enviar a Flask
    const response = await fetch('/preguntar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message, type: iaType })
    });

    const data = await response.json();

    // 4. Ocultar spinner y mostrar respuesta de la IA
    spinner.classList.add('d-none');
    appendMessage(iaType, data.answer);
    chatWindow.scrollTop = chatWindow.scrollHeight;
};

function appendMessage(type, text) {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const alignment = type === 'user' ? 'align-items-end' : 'align-items-start';
    const html = `
        <div class="d-flex flex-column mb-3 ${alignment}">
            <div class="p-3 rounded-3 shadow-sm chat-bubble ${type}">
                ${marked.parse(text)}
                <div class="text-end small opacity-50 mt-1" style="font-size: 0.7rem;">${time}</div>
            </div>
        </div>`;
    chatWindow.insertAdjacentHTML('beforeend', html);
}

document.addEventListener('DOMContentLoaded', () => {
    const bubbles = document.querySelectorAll('.chat-bubble');
    bubbles.forEach(bubble => {
        // Obtenemos el texto crudo, lo pasamos por marked y lo reinsertamos
        const rawText = bubble.innerHTML.trim();
        bubble.innerHTML = marked.parse(rawText);
    });
    // Hacer scroll al final al cargar
    chatWindow.scrollTop = chatWindow.scrollHeight;
});

document.addEventListener("DOMContentLoaded", function() {
    const alerts = document.getElementById("mensajes");

    setTimeout(function() {
        alerts.classList.add('fade');
        alerts.style.display = 'none';
    }, 5000);

});
