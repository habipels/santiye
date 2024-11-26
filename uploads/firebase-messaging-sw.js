// Firebase SDK'yı dahil et
importScripts("https://www.gstatic.com/firebasejs/9.17.1/firebase-app.js");
importScripts("https://www.gstatic.com/firebasejs/9.17.1/firebase-messaging.js");


// Firebase yapılandırması
const firebaseConfig = {
  apiKey: "AIzaSyD5HHO-gcwyuuWeXp1TzZKP8QTcPScwNZo",
  authDomain: "biadago-cloud.firebaseapp.com",
  projectId: "biadago-cloud",
  storageBucket: "biadago-cloud.appspot.com", // Düzeltilmiş URL
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
  console.log(
    "[firebase-messaging-sw.js] Background Notification Received ",
    payload
  );

  const notificationTitle = payload.notification?.title || "Bildirim";
  const notificationOptions = {
    body: payload.notification?.body || "Bir mesajınız var.",
    icon: "/static/go/icon/favicon-32x32.png", // Bildirim simgesi için doğru yol
  };

  // Bildirimi göster
  self.registration.showNotification(notificationTitle, notificationOptions);
});
