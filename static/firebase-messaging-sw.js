importScripts('https://www.gstatic.com/firebasejs/11.0.2/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/11.0.2/firebase-messaging.js');

// Firebase Config
firebase.initializeApp({
  apiKey: "AIzaSyD5HHO-gcwyuuWeXp1TzZKP8QTcPScwNZo",
  authDomain: "biadago-cloud.firebaseapp.com",
  projectId: "biadago-cloud",
  storageBucket: "biadago-cloud.firebasestorage.app",
  messagingSenderId: "990430074148",
  appId: "1:990430074148:web:83f5b40ec6944b8a268fb1",
  measurementId: "G-67DK949V4Q"
});

// Firebase Messaging
const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
  console.log('Arka planda mesaj alındı:', payload);
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});
