<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRoute } from "vue-router";

export default defineComponent({
  name: 'PoemExplanationView',

  setup() {
    const activeTab = ref('الشرح العام'); // Default active tab

    const tabs = ['الشرح العام', 'الشرح المفصل', 'قصة', 'عرض صوري'];

    const setActiveTab = (tab: string) => {
      activeTab.value = tab;
    };

    const route = useRoute();

    // Parse the data from the query parameter
    const explanationData = route.query.data
        ? JSON.parse(route.query.data as string)
        : {};

    // Log the received data for debugging
    console.log("Received explanationData in PoemExplanationView:", explanationData);

    // Reactive variables to store the data
    const poem = ref(explanationData.poem || []);
    const topic = ref(explanationData.topic || "");
    const general = ref(explanationData.general || "");
    const detailed = ref(explanationData.detailed || []);
    const story = ref(explanationData.story || "");
    const pictures = ref(explanationData.pictures || []);

    // Log individual parts if needed
    console.log("Poem:", poem.value);
    console.log("Topic:", topic.value);
    console.log("General:", general.value);
    console.log("Detailed:", detailed.value);
    console.log("Story:", story.value);
    console.log("Pictures:", pictures.value);

    return {
      activeTab,
      tabs,
      setActiveTab,

      poem,
      topic,
      general,
      detailed,
      story,
      pictures,
    };
  },
});
</script>


<template>
  <div class="PoemExplanationView">

    <!-- Display Poem at the Top -->
    <h2 class="text-lg font-bold mb-2">القصيدة</h2>
    <div v-if="poem.length > 0" class="mx-auto max-w-lg space-y-4 mb-8 border rounded-md p-5">
      <div
          v-for="(linePair, index) in poem"
          :key="index"
          class="flex justify-between text-center text-sm mb-2 items-center"
      >
        <div class="w-1/2" v-if="linePair[0]">{{ linePair[0] }}</div>
        <div class="w-1/2" v-if="linePair[1]">{{ linePair[1] }}</div>
      </div>
    </div>
    <div v-else class="text-center mb-8">
      لا توجد قصيدة متاحة لعرضها.
    </div>


    <!-- Tabs -->
    <div class="tabs flex space-x-4 mb-10 justify-center">
      <button
          v-for="tab in tabs"
          :key="tab"
          @click="setActiveTab(tab)"
          :class="['px-4 py-2', activeTab === tab ? 'border-b-2 border-white font-bold' : 'text-gray-400']"
      >
        {{ tab }}
      </button>
    </div>

    <!-- Tab Content -->
    <div class="tab-content">

      <!-- General Explanation Tab -->
      <div v-if="activeTab === 'الشرح العام'">
        <h2 class="text-xl font-semibold mb-3">الشرح العام</h2>
        <p class="px-10 pt-2" v-if="general">
          {{ general }}
        </p>
        <p class="px-10 pt-2" v-else>لا توجد بيانات متاحة.</p>
      </div>

      <!-- Detailed Explanation Tab -->
      <div v-if="activeTab === 'الشرح المفصل'">
        <h2 class="text-xl font-semibold mb-3">الشرح المفصل</h2>
        <ul v-if="detailed.length > 0" class="px-10 pt-2 list-inside space-y-5">
          <li v-for="(line, index) in detailed" :key="index">- {{ line }}</li>
        </ul>
        <p class="px-10 pt-2" v-else>لا توجد بيانات متاحة.</p>
      </div>

      <!-- Story Tab -->
      <div v-if="activeTab === 'قصة'">
        <h2 class="text-xl font-semibold mb-3">قصة</h2>
        <p class="px-10 pt-2" v-if="story">
          {{ story }}
        </p>
        <p class="px-10 pt-2" v-else>لا توجد بيانات متاحة.</p>
      </div>

      <!-- Visual Display Tab -->
      <div v-if="activeTab === 'عرض صوري'">
        <h2 class="text-xl font-semibold mb-3">عرض صوري</h2>
        <ul v-if="pictures.length > 0" class="px-10 pt-2 list-inside space-y-5">
          <li v-for="(picture, index) in pictures" :key="index">{{ picture }}</li>
        </ul>
        <p class="px-10 pt-2" v-else>لا توجد بيانات متاحة.</p>
      </div>

    </div>

  </div>
</template>

<style lang="scss">
.PoemExplanationView {
  .tabs {
    button {
      transition: color 0.3s, border-color 0.3s;
    }

    button:hover {
      color: #ff1d1d;
    }
  }
}
</style>
