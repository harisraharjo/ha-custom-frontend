<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'

import {
  getAuth,
  createConnection,
  subscribeEntities,
  // type getAuthOptions as AuthOptions,
  // Auth,
  ERR_HASS_HOST_REQUIRED,
  // type UnsubscribeFunc,
// Connection,
// type HassEntities,
// type HassServices,
// type HassConfig
} from 'home-assistant-js-websocket'

// interface HassStore {
//   connection?: Connection;
//   entities: HassEntities;
//   services: HassServices;
//   config: Partial<HassConfig>;
// }

// const hassStore = {
//   entities: {},
//   services: {},
//   config: {},
// }


const BASE_URL = 'http://localhost:8123';

// function getAuthOptions(): AuthOptions {
//   return {
//     hassUrl: BASE_URL,
//     async loadTokens() {
//       try {
//         return JSON.parse(localStorage.hassTokens);
//       } catch (e) {
//         return undefined;
//       }
//     },
//     saveTokens(tokens) {
//       localStorage.hassTokens = JSON.stringify(tokens);
//     }
//   }
// }

async function connect() {
  let auth;
  try {
    // Try to pick up authentication after user logs in
    auth = await getAuth({hassUrl: BASE_URL });
  } catch (err) {
    if (err === ERR_HASS_HOST_REQUIRED) {
      const hassUrl = BASE_URL
      // Redirect user to log in on their instance
      auth = await getAuth({ hassUrl });
    } else {
      alert(`Unknown error: ${err}`);
      return;
    }
  }
  const connection = await createConnection({ auth });
  subscribeEntities(connection, (ent) => console.log(ent));
}

connect();

</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
    

    <div class="wrapper">
      <HelloWorld msg="HELLO THERE" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
