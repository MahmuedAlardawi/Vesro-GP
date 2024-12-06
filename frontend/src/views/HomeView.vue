<script lang="ts">
import { defineComponent, ref } from "vue";
import { useRouter } from "vue-router";

import HomeComponent_0 from '@/components/HomeComponent_0.vue';
import HomeComponent_1 from '@/components/HomeComponent_1.vue';
import HomeComponent_2 from '@/components/HomeComponent_2.vue';
import axios from "axios";

export default defineComponent({
  name: 'HomeView',

  components: {
    HomeComponent_0,
    HomeComponent_1,
    HomeComponent_2,
  },

  setup() {
    const isLoading = ref(false); // Add loading state

    const currentComponent = ref<"HomeComponent_1" | "HomeComponent_2">("HomeComponent_1");

    const switchComponent = (componentName: "HomeComponent_1" | "HomeComponent_2") => {
      currentComponent.value = componentName; // Update the component dynamically
    };

    const ref_HC0 = ref(); // Reference to HomeComponent_0
    const receivedData_HC0 = ref({
      meter: null,
      verseCount: null,
    });

    const handleFetchData_HC0 = () => {
      // Access data from HomeComponent_0 using the ref
      if (ref_HC0.value) {
        receivedData_HC0.value.meter = ref_HC0.value.selectedMeter;
        receivedData_HC0.value.verseCount = ref_HC0.value.selectedVerseCount;

        console.log("Received data from HomeComponent_0:", receivedData_HC0.value.meter);
        console.log("Received data from HomeComponent_0:", receivedData_HC0.value.verseCount);
      }
    };

    const ref_HC1 = ref(); // Reference to HomeComponent_1
    const receivedData_HC1 = ref({
      topic: null,
    });

    // Fetch data from HC1 using ref
    const handleFetchData_HC1 = () => {
      if (ref_HC1.value) {
        receivedData_HC1.value.topic = ref_HC1.value.processedUserInput;
        console.log("Received data from HomeComponent_1:", receivedData_HC1.value.topic);
      }
    };

    const pairedPoem = ref<string[][]>([]);

    // Populate pairedPoem from backendResponse initially
    const initializePairedPoem = () => {
      const pairs: string[][] = [];
      const poemLines = backendResponse_generatePoem.value?.poem || [];

      let i = 0;
      while (i < poemLines.length) {
        const firstLine = poemLines[i]
        const secondLine = poemLines[i + 1]
        pairs.push([firstLine, secondLine]);
        i += 2;
      }

      pairedPoem.value = cleanPairedPoem(pairs);
    };

    // Update pairedPoem from child components
    const updatePairedPoem = (updatedPairedPoem: string[][]) => {
      if (
          Array.isArray(updatedPairedPoem) &&
          updatedPairedPoem.every(
              pair => Array.isArray(pair) && pair.length === 2 && pair.every(line => true)
          )
      ) {
        pairedPoem.value = cleanPairedPoem(updatedPairedPoem);
      } else {
        console.error("Invalid paired poem structure:", updatedPairedPoem);
      }
    };

    // Clean up empty or invalid pairs from pairedPoem
    const cleanPairedPoem = (poem: string[][]): string[][] => {
      return poem.filter(pair => {
        // Ensure pair is valid and contains non-empty trimmed strings
        const firstLine = pair[0];
        const secondLine = pair[1];
        return firstLine || secondLine; // Keep pairs with at least one valid line
      });
    };

    const backendResponse_generatePoem = ref({
      topic: "",
      meter: "",
      verseCount: 0,
      poem: [] as string[],
    });

    const sendDataToBackend_generatePoem = async () => {
      if (receivedData_HC0.value.meter && receivedData_HC0.value.verseCount && receivedData_HC1.value.topic) {
        try {
          const response = await axios.post("http://127.0.0.1:8000/api/generate_poem_colab/", {
            topic: receivedData_HC1.value.topic,
            meter: receivedData_HC0.value.meter,
            verseCount: receivedData_HC0.value.verseCount,
          });

          // Store the backend response in the reactive property
          backendResponse_generatePoem.value = {
            topic: response.data.user_input,
            meter: response.data.meter,
            verseCount: response.data.verse_count,
            poem: response.data.response,
          };

          initializePairedPoem(); // Initialize pairedPoem after receiving backend response

          console.log("Data successfully sent to backend:", response.data);
        } catch (error) {
          console.error("Error sending data to backend:", error);
        }
      } else {
        console.error("Meter or verse count is missing. Cannot send data to backend.");
      }
    };

    const handleSubmit_generatePoem = () => {
      handleFetchData_HC0();
      handleFetchData_HC1();

      // Send the fetched data to the backend
      sendDataToBackend_generatePoem();
    };

    const backendResponse_generateExplanation = ref({
      poem: [] as string[],
      topic: "",
      general : "",
      detailed : [] as string[],
      story : "",
      pictures : [] as string[]
    });

    const handleBackendSubmissio_generateExplanationn = async () => {
      try {
        await sendDataToBackend_generateExplanation(); // Wait for backend processing
        console.log("Backend processing complete, ready to navigate.");
      } catch (error) {
        console.error("Error during backend submission:", error);
        throw error; // Propagate error back to the child
      }
    };


    const sendDataToBackend_generateExplanation = async () => {
      if (pairedPoem.value) {
        try {
          const response = await axios.post("http://127.0.0.1:8000/api/generate_explanation_colab/", {
            poem: pairedPoem.value,
            topic: receivedData_HC1.value.topic,
          });

          backendResponse_generateExplanation.value = {
            poem: response.data.poem,
            topic: response.data.topic,
            general: response.data.responses.generate_general,
            detailed: response.data.responses.generate_detailed,
            story: response.data.responses.generate_story,
            pictures: response.data.responses.generate_image_descriptions,
          };

          console.log("Data successfully sent to backend:", response.data);

          // Navigate after data is processed
          await router.push({
            name: "poemExplanation",
            query: {
              data: JSON.stringify(backendResponse_generateExplanation.value),
            },
          });
        } catch (error) {
          console.error("Error sending data to backend:", error);
          throw error; // Ensure errors propagate to `handleSubmit`
        }
      } else {
        console.error("Poem or topic is missing. Cannot send data to backend.");
        throw new Error("Invalid input data.");
      }
    };


    const handleSubmit_generateExplanation = () => {
      handleFetchData_HC1();

      // Send the fetched data to the backend
      sendDataToBackend_generateExplanation();
    };

    const router = useRouter();

    const navigateToExplanation = () => {
      router.push({
        name: "poemExplanation",
        query: {
          data: JSON.stringify(backendResponse_generateExplanation.value),
        },
      });
    };

    return {
      isLoading,

      currentComponent,
      switchComponent,

      ref_HC0,
      receivedData_HC0,
      handleFetchData_HC0,

      ref_HC1,
      receivedData_HC1,
      handleFetchData_HC1,

      pairedPoem,
      initializePairedPoem,
      updatePairedPoem,
      cleanPairedPoem,

      backendResponse_generatePoem,
      sendDataToBackend_generatePoem,

      handleSubmit_generatePoem,

      backendResponse_generateExplanation,
      handleBackendSubmissio_generateExplanationn,
      sendDataToBackend_generateExplanation,

      handleSubmit_generateExplanation,

      navigateToExplanation
    };
  },
});
</script>

<template>
  <div class="flex mx-10">

    <!-- Main Component Section -->
    <div class="w-4/5">
      <component
          :is="currentComponent"
          ref="ref_HC1"
          v-bind="{
          pairedPoem,
          disabled: isLoading
        }"
          @submit="handleSubmit_generatePoem"
          @update:pairedPoem="updatePairedPoem"
          @update:isLoading="isLoading = $event"
          v-if="currentComponent === 'HomeComponent_1'"
      />
      <component
          :is="currentComponent"
          :pairedPoem="pairedPoem"
          @update:pairedPoem="updatePairedPoem"
          v-else
      />
    </div>

    <!-- Side Component Section -->
    <div class="w-1/5 sticky top-0 h-screen">
      <HomeComponent_0
          ref="ref_HC0"
          :disabled="isLoading"
          @toggle="switchComponent"
          @update:isLoading="isLoading = $event"
          @submitToBackend="handleBackendSubmissio_generateExplanationn"
          @navigateToExplanation="navigateToExplanation"
      />
    </div>

  </div>
</template>

<style lang="scss">
/* Add your styles here */
</style>
