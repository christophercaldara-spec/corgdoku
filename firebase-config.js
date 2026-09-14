// Firebase project settings.
//
// These values are NOT secret - Firebase web config is public by design, and
// every app that uses it ships these in plain sight. The apiKey identifies the
// project; it doesn't authorise anything. What actually protects the data is
// firestore.rules, which is why that file matters and this one doesn't.
//
// From: Firebase console -> Project settings -> General -> Your apps -> Corgdoku
window.CORGDOKU_FIREBASE = {
  apiKey: "AIzaSyAuhNDgMWOa4VzyuuT42Ew2MDUxfF9QWHY",
  authDomain: "corgdoku.firebaseapp.com",
  projectId: "corgdoku",
  storageBucket: "corgdoku.firebasestorage.app",
  messagingSenderId: "684104008396",
  appId: "1:684104008396:web:46e6dbc3c2ef42547cf869"
};
