<script lang="ts">
import { defineComponent } from 'vue';
import NavBar from './components/NavBar.vue';
import FootBar from './components/FootBar.vue';

export default defineComponent({
  name: 'App',
  components: {
    NavBar,
    FootBar,
  },
});
</script>

<template>
  <div id="app">
    <div class="content">
      <NavBar />
      <router-view />
    </div>
    <FootBar />
  </div>
</template>

<style lang="scss">
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content {
  flex: 1;
}
</style>
