import { initializeApp } from "firebase/app";
import 'firebase/auth'; // Import only what you need
import { getAuth, onAuthStateChanged } from "firebase/auth";


const firebase = async () => {
    const firebaseConfig = {
        apiKey: import.meta.env.VITE_API_FIREBASE_API_KEY,
        authDomain: import.meta.env.VITE_API_FIREBASE_AUTH_DOMAIN,
        projectId: import.meta.env.VITE_API_FIREBASE_PROJECT_ID,
        storageBucket: import.meta.env.VITE_API_FIREBASE_STORAGEBUCKET,
        messagingSenderId: import.meta.env.VITE_API_FIREBASE_MESSAGINGSENDERID,
        appId: import.meta.env.VITE_API_FIREBASE_APPID,
        measurementId: import.meta.env.VITE_API_FIREBASE_MEASUREMENTID
    };

    initializeApp(firebaseConfig);
    const auth = getAuth(app);
    console.log("Firebase running...");

}

export default firebase;
