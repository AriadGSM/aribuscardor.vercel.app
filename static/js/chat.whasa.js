function toggleChat() {
    const chatBot = document.getElementById('chatBot');
    chatBot.classList.toggle('active');
}

function selectOption(option) {
    const chatMessages = document.getElementById('chatMessages');
    let response = '';
    
    switch(option) {
        case 'precios':
            response = 'Los precios de las obras varían desde S/100.00. Cada pieza es única y el precio depende del tamaño y la complejidad.';
            break;
        case 'materiales':
            response = 'Trabajo con técnicas mixtas, incluyendo acuarelas, acrílicos y medios digitales para crear obras únicas.';
            break;
        case 'envios':
            response = 'Realizamos envíos a todo el Perú. El costo y tiempo de entrega depende de tu ubicación.';
            break;
        case 'contacto':
            window.open('https://wa.me/+TU_NUMERO_AQUI', '_blank');
            response = 'Te estoy redirigiendo a WhatsApp para una atención personalizada.';
            break;
    }

    chatMessages.innerHTML += `<div class="message user">${option}</div>`;
    chatMessages.innerHTML += `<div class="message bot">${response}</div>`;
    chatMessages.scrollTop = chatMessages.scrollHeight;
}