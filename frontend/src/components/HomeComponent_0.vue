<script lang="ts">
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "HomeComponent_0",
  props: {
    disabled: {
      type: Boolean,
      default: false, // Parent will control this state
      required: true,
    },
  },
  emits: ["toggle", "submitToBackend", "update:isLoading", "navigateToExplanation"], // Declare the event this component emits

  setup(_, { emit }) {

    // Toggle Section
    const toggleOn = ref(false); // State for toggle
    const toggleLabel = ref("نظم القصيدة"); // Default label

    const toggleState = () => {
      if (!_.disabled) { // Ensure functionality only when not disabled
        toggleOn.value = !toggleOn.value; // Toggle the state
        toggleLabel.value = toggleOn.value ? "وزن القصيدة" : "نظم القصيدة"; // Update the label
        const componentName = toggleOn.value ? "HomeComponent_2" : "HomeComponent_1";
        emit("toggle", componentName); // Emit the component name
      }
    };

    // Meter Section
    const selectedMeter = ref("الطويل"); // Default selection

    // Slider Section
    const selectedVerseCount = ref<number>(3); // Default value

    const handleSubmit = async () => {
      try {
        emit("update:isLoading", true); // Notify parent that loading has started

        // Notify the parent to start backend processing and wait for its completion
        await emit("submitToBackend"); // Ensure this event resolves when backend processing is done

        // Notify parent to navigate after the backend response
        emit("navigateToExplanation");
      } catch (error) {
        console.error("Error during submission or backend processing:", error);
      } finally {
        emit("update:isLoading", false); // Notify parent that loading has ended
      }
    };


    return {
      // Toggle Section
      toggleOn,
      toggleLabel,
      toggleState,

      // Meter Section
      selectedMeter,

      // Slider Section
      selectedVerseCount,

      handleSubmit,
    };
  },
});
</script>

<template>
  <div class="flex flex-col items-center justify-center text-l">

    <!-- Toggle Button -->
    <h1 class="pb-2">{{ toggleLabel }}</h1>
    <div
        @click="toggleState"
        class="relative flex w-full items-center mb-6 p-5 rounded-full"
        :class="[
    toggleOn ? 'bg-gray-900' : 'bg-black',
    disabled ? 'cursor-not-allowed' : 'cursor-pointer'
  ]"
    >
      <!-- Circle -->
      <div
          class="absolute w-6 h-6 bg-white rounded-full duration-500"
          :class="toggleOn ? 'left-4' : 'right-4'"
      ></div>
    </div>

    <!-- Select Section -->
    <div class="w-full mb-6">
      <label class="block mb-2 text-right">اختر البحر:</label>
      <div class="relative border rounded-md p-3 bg-transparent">
        <select
            v-model="selectedMeter"
            class="appearance-none w-full bg-transparent text-white focus:outline-none cursor-pointer disabled:cursor-not-allowed"
            :disabled="disabled"
        >
          <option class="bg-black text-white" value="الطويل">الطويل</option>
        </select>

        <!-- Dropdown arrow -->
        <svg
            xmlns="http://www.w3.org/2000/svg"
            class="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 pointer-events-none"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </div>

    <!-- Slider Section -->
    <div v-if="!toggleOn" class="w-full mb-6">
      <label class="block mb-2 text-right">
        عدد الأبيات: <span>{{ selectedVerseCount }}</span>
      </label>
      <input
          type="range"
          :min="1"
          :max="6"
          v-model="selectedVerseCount"
          class="w-full accent-black h-6 cursor-pointer disabled:cursor-not-allowed"
          :disabled="disabled"
      />
    </div>

    <!-- Button Section -->
    <div class="w-full">
      <template v-if="disabled">
        <div class="w-full py-3 rounded-md bg-black cursor-not-allowed text-center">
          شرح القصيدة
        </div>
      </template>
      <template v-else>
        <button
            class="w-full py-3 rounded-md bg-black hover:bg-gray-700 transition duration-300 text-center block"
            :class="disabled ? 'cursor-not-allowed' : ''"
            @click="handleSubmit"
        >
          شرح القصيدة
        </button>
      </template>
    </div>

  </div>
</template>

<style scoped lang="scss">

</style>
