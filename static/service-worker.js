const CACHE_NAME = 'biadago-cache-v1';
const urlsToCache = [
    '/',
    '/tr',
    'http://127.0.0.1:8000/',
    'http://127.0.0.1:8000/tr',
    'http://127.0.0.1:8000/tr/accounting/expenses',
    'https://fonts.googleapis.com/css2?family=Red+Hat+Display:ital,wght@0,300..900;1,300..900&display=swap',
    '/static/go/style/style.css',
    'https://cdn.jsdelivr.net/npm/apexcharts',
    'https://momentjs.com/downloads/moment.min.js',
    'https://code.jquery.com/jquery-3.7.1.min.js',
    'https://cdn.datatables.net/v/dt/dt-2.1.6/r-3.0.3/datatables.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.14.0/Sortable.min.js'
];

// Service Worker kurulumu ve önbelleğe alma
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
            .catch(error => console.error('Caching failed:', error))
    );
});

// Fetch olayını dinleme ve önbellekten yanıt verme
self.addEventListener('fetch', event => {
    if (!navigator.onLine && event.request.url.includes('ipinfo.io')) {
        // API isteğini çevrimdışıyken kaydedin
        saveRequestOffline({
            url: event.request.url,
            method: event.request.method,
            headers: [...event.request.headers],
            body: event.request.body ? event.request.body : null
        });

        event.respondWith(
            new Response(JSON.stringify({ error: 'You are offline, request queued.' }), {
                headers: { 'Content-Type': 'application/json' }
            })
        );
    } else {
        event.respondWith(
            caches.match(event.request)
                .then(response => response || fetch(event.request))
                .catch(() => caches.match('/offline.html')) // Çevrimdışıyken gösterilecek bir dosya
        );
    }
});

// Eski cacheleri temizleme
self.addEventListener('activate', event => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then(cacheNames => Promise.all(
            cacheNames.map(cacheName => {
                if (!cacheWhitelist.includes(cacheName)) {
                    return caches.delete(cacheName);
                }
            })
        ))
    );
});

// Background Sync: Kuyruğa alınan API isteklerini çevrim içi olduğunda gönderme
self.addEventListener('sync', function(event) {
    if (event.tag === 'sendQueuedRequests') {
        event.waitUntil(sendQueuedRequests());
    }
});

// Çevrimdışı istekleri IndexedDB’ye kaydetme fonksiyonu
function saveRequestOffline(request) {
    openDatabase().then(db => {
        const transaction = db.transaction("requestsQueue", "readwrite");
        const store = transaction.objectStore("requestsQueue");
        store.add(request);
    }).catch(error => {
        console.error("Failed to save request offline:", error);
    });
}

// Çevrimdışı kuyruğu tekrar gönderen fonksiyon
function sendQueuedRequests() {
    return openDatabase().then(db => {
        const transaction = db.transaction("requestsQueue", "readonly");
        const store = transaction.objectStore("requestsQueue");

        return store.getAll().then(requests => {
            return Promise.all(
                requests.map(request => {
                    return fetch(request.url, {
                        method: request.method,
                        headers: new Headers(request.headers),
                        body: request.body
                    })
                    .then(response => {
                        if (response.ok) {
                            // Başarılı istekleri kuyruktan sil
                            const deleteTransaction = db.transaction("requestsQueue", "readwrite");
                            const deleteStore = deleteTransaction.objectStore("requestsQueue");
                            deleteStore.delete(request.id);
                        }
                    });
                })
            );
        });
    });
}

// IndexedDB: Çevrimdışı veri saklama fonksiyonları
function openDatabase() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open("offlineData", 1);
        
        request.onupgradeneeded = function(event) {
            const db = event.target.result;
            db.createObjectStore("formData", { keyPath: "id", autoIncrement: true });
            db.createObjectStore("requestsQueue", { keyPath: "id", autoIncrement: true });  // Yeni kuyruk tablosu
        };

        request.onsuccess = function(event) {
            resolve(event.target.result);
        };

        request.onerror = function(event) {
            reject("Database error: " + event.target.errorCode);
        };
    });
}

function saveDataOffline(data) {
    openDatabase().then(db => {
        const transaction = db.transaction("formData", "readwrite");
        const store = transaction.objectStore("formData");
        store.add(data);
    }).catch(error => {
        console.error("Failed to save data offline:", error);
    });
}
