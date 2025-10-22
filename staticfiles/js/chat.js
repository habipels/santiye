document.addEventListener('DOMContentLoaded', function () {
    const groupId = "{{ group.id }}"; // Replace with the group ID dynamically
    const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + groupId + '/');

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        const chatLog = document.getElementById('chatappend');

        // Append the new message to the chat log
        chatLog.innerHTML += `
            <li class="send">
                <div class="d-flex">
                    <div class="profile">
                        <img class="bg-img" style="max-width: 50px;" src="{% static 'go/images/profile.png' %}" alt="Avatar"/>
                    </div>
                    <div class="flex-grow-1">
                        <div class="contact-name">
                            <h5>${data.user}</h5>
                            <h6>${new Date(data.timestamp).toLocaleTimeString()}</h6>
                            <ul class="msg-box">
                                <li class="msg-setting-main">
                                    <h5>${data.message}</h5>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </li>`;
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#send-message').onclick = function (e) {
        const messageInput = document.querySelector('#message-input');
        const message = messageInput.value;

        chatSocket.send(JSON.stringify({
            'message': message
        }));

        messageInput.value = '';
    };
});
