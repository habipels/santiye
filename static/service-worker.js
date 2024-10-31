const CACHE_NAME = 'biadago-cache-v1';
const urlsToCache = [
        'http://127.0.0.1:8000/',
        'http://127.0.0.1:8000/tr',
        'http://127.0.0.1:8000/tr/accounting/expenses',
        'https://fonts.googleapis.com/css2?family=Red+Hat+Display:ital,wght@0,300..900;1,300..900&display=swap',
        '{% static "go/style/style.css" %}',
        'https://cdn.jsdelivr.net/npm/apexcharts',
        'https://momentjs.com/downloads/moment.min.js',
        'https://code.jquery.com/jquery-3.7.1.min.js',
        'https://cdn.datatables.net/v/dt/dt-2.1.6/r-3.0.3/datatables.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.14.0/Sortable.min.js'
    ];
    
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});

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
