<template>
<!--  <div class="hello">-->
<!--    <h1 class="display-2 font-weight-bold mb-3">-->
<!--      Welcome to Vuetify-->
<!--    </h1>-->
<!--    <h2 v-if="user">{{ user }}</h2>-->

<!--    <br/>-->
<!--    <div id="logout" v-if="isSignedIn">-->
<!--      <v-btn @click="handleSignOut">logout</v-btn>-->
<!--    </div>-->

<!--    <br/>-->
<!--    <div id="GoogleSignIn" v-if="isSignedIn">-->
<!--      <h3>Google Signin</h3>-->
<!--      <v-btn @click.prevent="handleSignInGoogle">login</v-btn>-->
<!--    </div>-->

<!--    <br/>-->
<!--    <div id="FacebookSignIn" v-if="isSignedIn">-->
<!--      <h3>Facebook Signin</h3>-->
<!--      <v-btn @click="handleSignInFacebook">login</v-btn>-->
<!--    </div>-->
<!--  </div>-->
  <div class="welcome-wrapper">
    <div class="welcome-block">
      <div class="logo-holder">
        <img src="@/assets/img/mishkan-logo.svg" alt="Mishkan"/>
      </div>
      <div class="title-holder">
        <h3>Log in</h3>
      </div>
      <div class="buttons-holder">
        <a class="link-btn kakao-type" >Sign in with KakaoTalk</a>
        <a class="link-btn fb-type" @click.prevent="handleSignInFacebook">Sign in with Facebook</a>
        <a class="link-btn g-type" @click.prevent="handleSignInGoogle">Sign in with Google</a>
      </div>
    </div>
  </div>
</template>
<script>
import firebaseConfig from "../firebaseConfig";
import { FacebookAuthProvider, GoogleAuthProvider, getAuth, signInWithPopup, signOut } from "firebase/auth";

firebaseConfig

const provider = new GoogleAuthProvider();
const fb_provider = new FacebookAuthProvider();
const auth = getAuth();

export default {
  name: "Login",
  data() {
    return {
      user: '',
      isSignedIn: false,
      show_pwd: false,
    }
  },
 methods: {
   handleSignInGoogle() {
      signInWithPopup(auth, provider)
          .then((result) => {
            // The signed-in user info.
            // const user = result.user;
            // console.log(result)
            this.user = result.user.displayName;
            this.isSignedIn = true;
            // store jwt token
            localStorage.setItem('token', JSON.stringify(result.user.idToken));
            alert("Welcome! ", this.user)
            this.$router.push("/");
          }).catch((error) => {
            console.log(error)
      });
    },
   handleSignInFacebook() {
     signInWithPopup(auth, fb_provider)
         .then((result) => {
           // The signed-in user info.
           const user = result.user;

           // This gives you a Facebook Access Token. You can use it to access the Facebook API.
           const credential = FacebookAuthProvider.credentialFromResult(result);
           const accessToken = credential.accessToken;

           console.log(result)
           this.user = result.displayName;
           alert("Welcome! ", this.user)
           this.isSignedIn = true;
           this.$router.push("/");
         })
         .catch((error) => {
           console.log(error)
         });
   },
    handleSignOut() {
      signOut(auth).then(() => {
        this.user = '';
        this.isSignedIn = false;
      }).catch((error) => {
        console.log(error)
      });
    }
 },
  created() {
    this.handleSignInGoogle();
    this.handleSignInFacebook();
    this.handleSignOut();
  }
}
</script>
<style scoped>
</style>