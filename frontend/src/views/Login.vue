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
        <v-row>
          <v-col
              cols="12"
              sm="12"
              md="12"
          >
            <v-text-field
                label="Email"
                placeholder="Email"
                outlined
                dense
            ></v-text-field>
            <v-text-field
                label="Password"
                placeholder="Password"
                outlined
                dense
            ></v-text-field>
            <v-btn
                block
                class="mb-5"
                elevation="5"
                color="#8E24AA"
                text
            >Log In</v-btn>
          </v-col>
        </v-row>
        <!--  social login  -->
        <a class="link-btn kakao-type">Sign in with KakaoTalk</a>
        <a class="link-btn fb-type">Sign in with Facebook</a>
        <a class="link-btn g-type">Sign in with Google</a>
      </div>
    </div>
  </div>
</template>
<script>
import firebaseConfig from "../firebaseConfig";
import { FacebookAuthProvider, GoogleAuthProvider, getAuth, signInWithPopup, signOut } from "firebase/auth";

firebaseConfig

const provider = new GoogleAuthProvider();
// const fb_provider = new FacebookAuthProvider();
const auth = getAuth();

export default {
  name: "Login",
  data() {
    return {
      email: '',
      password: '',
      isSignedIn: false,
      show_pwd: false,
    }
  },
 methods: {
    // async login() {
    //   try {
    //     await this.$axios.post('http://localhost:5000/login', {
    //       email: this.email,
    //       password: this.password
    //     })
    //     this.$router.push("/protected")
    //   } catch (error) {
    //     console.log(error)
    //   }
    // }
   handleSignInGoogle() {
      signInWithPopup(auth, provider)
          .then((result) => {
            // The signed-in user info.
            // const user = result.user;
            // console.log(result)
            // this.user = result.user.displayName;
            // this.isSignedIn = true;
            // store jwt token
            // localStorage.setItem('token', JSON.stringify(result.user.idToken));
            alert("Welcome! ", this.user)
            this.$router.push("/");
          }).catch((error) => {
            console.log(error)

            this.user = "demo";
            this.isSignedIn = true;
            // store jwt token
            localStorage.setItem('token', "demo_token");
            alert("Welcome! ", this.user)
            this.$router.push("/");

      });
    },
 //   handleSignInFacebook() {
 //     signInWithPopup(auth, fb_provider)
 //         .then((result) => {
 //           // The signed-in user info.
 //           const user = result.user;
 //
 //           // This gives you a Facebook Access Token. You can use it to access the Facebook API.
 //           const credential = FacebookAuthProvider.credentialFromResult(result);
 //           const accessToken = credential.accessToken;
 //
 //           console.log(result)
 //           this.user = result.displayName;
 //           alert("Welcome! ", this.user)
 //           this.isSignedIn = true;
 //           this.$router.push("/");
 //         })
 //         .catch((error) => {
 //           console.log(error)
 //         });
 //   },
 //   handleSignOut() {
 //      signOut(auth).then(() => {
 //        this.user = '';
 //        this.isSignedIn = false;
 //      }).catch((error) => {
 //        console.log(error)
 //      });
 //    }
 },
  created() {
    this.handleSignInGoogle();
 //    this.handleSignInFacebook();
 //    this.handleSignOut();
  }
}
</script>
<style scoped>
</style>
