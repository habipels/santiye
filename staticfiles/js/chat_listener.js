document.addEventListener('DOMContentLoaded', function () {
    const groupId = "{{ group.id }}"; // Replace with the group ID dynamically
    const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + groupId + '/');

    chatSocket.onopen = function () {
        console.log('WebSocket connection established for group:', groupId);
    };

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log('New message received:', data);

        // Example: Display the message in the console
        console.log(`[${data.timestamp}] ${data.user}: ${data.message}`);

        // Optionally, update the UI
        const chatLog = document.getElementById('chatappend');
        if (chatLog) {
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
        }
    };

    chatSocket.onclose = function (e) {
        console.error('WebSocket connection closed unexpectedly');
    };

    chatSocket.onerror = function (e) {
        console.error('WebSocket error:', e);
    };
});
