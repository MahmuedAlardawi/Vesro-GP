<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'NavBar',
  setup() {
    // Add any component logic here if needed in the future
  }
});
</script>

<template>
  <div class="flex flex-col items-center mt-2 mx-10">

    <!-- Navbar -->
    <nav class="flex">
      <router-link to="/about" class="hover:scale-110 duration-500 text-xl px-4 m-4">عن فيرسو</router-link>

      <router-link to="/">
        <img src="@/assets/Verso_logo.png" alt="Home Logo" class="hover:scale-110 duration-500 w-22 h-15 px-5" />
      </router-link>

      <router-link to="/documentation" class="hover:scale-110 duration-500 text-xl px-4 m-4">توثيق فيرسو</router-link>
    </nav>

    <!-- Divider -->
    <hr class="w-full mb-10"/>
  </div>
</template>



<style scoped lang="scss">

</style>

