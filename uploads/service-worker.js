// Firebase SDK'ları import edin (Non-Modüler Sürüm)
importScripts("https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js");
importScripts("https://www.gstatic.com/firebasejs/8.10.0/firebase-messaging.js");

// Firebase yapılandırması
const firebaseConfig = {
  apiKey: "AIzaSyD5HHO-gcwyuuWeXp1TzZKP8QTcPScwNZo",
  authDomain: "biadago-cloud.firebaseapp.com",
  projectId: "biadago-cloud",
  storageBucket: "biadago-cloud.appspot.com",
  messagingSenderId: "990430074148",
  appId: "1:990430074148:web:83f5b40ec6944b8a268fb1",
  measurementId: "G-67DK949V4Q",
};

// Firebase'i başlat
firebase.initializeApp(firebaseConfig);

// Firebase Cloud Messaging'i başlat
const messaging = firebase.messaging();

// Arka planda alınan bildirimleri işleyin
messaging.onBackgroundMessage((payload) => {
  console.log("[Service Worker] Background Notification Received", payload);
  const notificationTitle = payload.notification?.title || "Bildirim";
  const notificationOptions = {
    body: payload.notification?.body || "Bir mesajınız var.",
    icon: "/static/go/icon/favicon-32x32.png",
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});

// PWA önbellekleme için yapılandırma
const CACHE_NAME = 'biadago-cache-v1';
const urlsToCache = [
  '/',
  '/tr',
  '/en',
  '/ckb',
  '/ar',
  '/ru',
  '/de',
  'https://cloud.biadago.com/static/go/style/style.css',
  'https://fonts.googleapis.com/css2?family=Red+Hat+Display:ital,wght@0,300..900;1,300..900&display=swap',
];

// Service Worker kurulumu ve önbelleğe alma
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Kuruluyor...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
      .catch((error) => console.error('Caching failed:', error))
  );
});

// Fetch olayını dinleme ve önbellekten yanıt verme
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => response || fetch(event.request))
      .catch(() => caches.match('/offline.html'))
  );
});

// Eski cacheleri temizleme
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Aktivasyon tamamlandı.');
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then((cacheNames) =>
      Promise.all(
        cacheNames.map((cacheName) => {
          if (!cacheWhitelist.includes(cacheName)) {
            return caches.delete(cacheName);
          }
        })
      )
    )
  );
});

// IndexedDB işlemleri
function openDatabase() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("offlineData", 1);

    request.onupgradeneeded = function (event) {
      const db = event.target.result;
      db.createObjectStore("formData", { keyPath: "id", autoIncrement: true });
      db.createObjectStore("requestsQueue", { keyPath: "id", autoIncrement: true });
    };

    request.onsuccess = function (event) {
      resolve(event.target.result);
    };

    request.onerror = function (event) {
      reject("Database error: " + event.target.errorCode);
    };
  });
}

function saveRequestOffline(request) {
  openDatabase().then((db) => {
    const transaction = db.transaction("requestsQueue", "readwrite");
    const store = transaction.objectStore("requestsQueue");
    store.add(request);
  }).catch((error) => {
    console.error("Failed to save request offline:", error);
  });
}

function sendQueuedRequests() {
  return openDatabase().then((db) => {
    const transaction = db.transaction("requestsQueue", "readonly");
    const store = transaction.objectStore("requestsQueue");

    return store.getAll().then((requests) => {
      return Promise.all(
        requests.map((request) => {
          return fetch(request.url, {
            method: request.method,
            headers: new Headers(request.headers),
            body: request.body,
          }).then((response) => {
            if (response.ok) {
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
