function toggleChat() {
    const chatBot = document.getElementById('chatBot');
    chatBot.classList.toggle('active');
}

function selectOption(option) {
    const chatMessages = document.getElementById('chatMessages');
    let response = '';
    
    switch(option) {
        case 'bienvenida':
            response = '👋 ¡Hola! 😊 Gracias por tu interés en nuestros cuadros personalizados. Cuéntame, ¿qué tipo de retrato te gustaría? (por ejemplo: una persona, pareja, mascota, fondo especial, etc.)';
            break;
        case 'detalles':
            response = '🎨 ¡Qué emoción! Nuestros cuadros se hacen a mano con todo el detalle. ¿Podrías indicarme el tamaño del lienzo y cuántas personas o elementos quieres incluir?';
            break;
        case 'estilo':
            response = '✨ Perfecto, puedo prepararte una cotización personalizada. ¿Tienes una foto de referencia o una idea del estilo (realista, tipo Van Gogh, caricatura, etc.)?';
            break;
        case 'contacto':
            window.open('https://wa.me/+51929917873', '_blank');
            response = 'Te estoy redirigiendo a WhatsApp para una atención personalizada.';
            break;
    }

    chatMessages.innerHTML += `<div class="message user">${option}</div>`;
    chatMessages.innerHTML += `
        <div class="message bot">
            ${response}
            <button onclick="window.open('https://wa.me/+51929917873?text=${encodeURIComponent(response)}', '_blank')" class="whatsapp-reply-button">
                <i class="fab fa-whatsapp"></i> Responder en WhatsApp
            </button>
        </div>
    `;
    chatMessages.scrollTop = chatMessages.scrollHeight;
}