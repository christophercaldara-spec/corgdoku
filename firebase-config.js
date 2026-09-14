// Firebase project settings.
//
// These values are NOT secret - Firebase web config is public by design, and
// every app that uses it ships these in plain sight. What actually protects
// the data is the security rules in firestore.rules, which is why those matter
// and this file doesn't.
//
// Replace the placeholders with the config from:
//   Firebase console -> Project settings -> General -> Your apps -> Web app
window.CORGDOKU_FIREBASE = {
  apiKey: "PASTE_ME",
  authDomain: "PASTE_ME.firebaseapp.com",
  projectId: "PASTE_ME",
  storageBucket: "PASTE_ME.firebasestorage.app",
  messagingSenderId: "PASTE_ME",
  appId: "PASTE_ME"
};
