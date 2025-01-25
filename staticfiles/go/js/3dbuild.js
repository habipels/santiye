        let currentRotation = 0;
        const infoModal = document.getElementById('infoModal');

        function createBuilding() {
            const floors = 27;
            const imageUrl = 'https://github.com/habipels/santiye/blob/main/building1.png?raw=true';

            for (let i = 1; i <= 4; i++) {
                const face = document.getElementById(`face${i}`);
                face.innerHTML = ''; // Yüzeyi temizle

                for (let j = floors; j >= 1; j--) { // Aşağıdan yukarı doğru artan sıra
                    const floor = document.createElement('div');
                    floor.className = 'floor';
                    floor.style.backgroundImage = `url(${imageUrl})`;
                    floor.setAttribute('data-floor', `Kat ${j}`);
                    floor.innerHTML = `Kat ${j}`;

                    const completionOverlay = document.createElement('div');
                    completionOverlay.className = 'completion-overlay';
                    completionOverlay.style.height = '0%'; // %100 tamamlanma varsayılan

                    // Yanıp sönen katlara tıklanabilir link ekleyin
                    if (['Kat 5', 'Kat 9', 'Kat 20', 'Kat 21'].includes(`Kat ${j}`)) {
                        floor.addEventListener('click', function(event) {
                            showInfoModal(event, `R5 - Kat ${j} görevi`);
                        });
                    }

                    floor.appendChild(completionOverlay);
                    face.appendChild(floor);
                }
            }
        }

        // Mini modal gösterimi (mouse yanında çıkar)
        function showInfoModal(event, message) {
            const modalText = document.getElementById('modalText');
            modalText.innerHTML = message;
            infoModal.style.display = 'block';
            infoModal.style.left = `${event.clientX + 15}px`; // Mouse yanında
            infoModal.style.top = `${event.clientY + 15}px`;
        }

        // Mini modal kapatma
        function closeInfoModal() {
            infoModal.style.display = 'none';
        }

        // İş Emrine Git fonksiyonu
        function goToTask() {
            alert("İş Emrine gidiliyor...");
            closeInfoModal(); // Modal kapatılıyor
        }

        document.body.addEventListener('mousedown', function(e) {
            let startX = e.clientX;
            document.onmousemove = function(e) {
                const deltaX = e.clientX - startX;
                currentRotation += deltaX * 0.1;
                document.querySelector('.building').style.transform = `rotateY(${currentRotation}deg)`;
                startX = e.clientX;
            };
            document.onmouseup = function() {
                document.onmousemove = null;
                document.onmouseup = null;
            };
        });

        createBuilding();
      document.body.addEventListener('mousedown', function(e) {
    let startX = e.clientX;
    document.onmousemove = function(e) {
        const deltaX = e.clientX - startX;
        currentRotation += deltaX * 0.05; // Daha yavaş döndürme
        document.querySelector('.building').style.transform = `rotateY(${currentRotation}deg)`;
        startX = e.clientX;
    };
});
