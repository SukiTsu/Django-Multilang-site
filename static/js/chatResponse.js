function askQuestion(questionId) {
    // Récupère la question et sélection la réponse en utilisant l'ID de la question
    const questionText = document.querySelector(`button[onclick="askQuestion('${questionId}')"]`).innerText;
    const botResponse = document.getElementById(`response-${questionId}`).innerText;

    // Affiche la question choisi par l'utilisateur
    const chatBox = document.getElementById('chatBox');
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user');
    userMessage.innerText = questionText;
    chatBox.appendChild(userMessage);

    // Affiche de la réponse du chatbot
    const botMessage = document.createElement('div');
    botMessage.classList.add('message', 'bot');
    botMessage.innerText = botResponse;
    chatBox.appendChild(botMessage);

    // Défile vers le bas pour voir les nouveaux messages
    chatBox.scrollTop = chatBox.scrollHeight;
}