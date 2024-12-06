<script lang="ts">
import { defineComponent, ref, computed, PropType } from "vue";

export default defineComponent({
  name: "HomeComponent_1",
  props: {
    disabled: {
      type: Boolean,
      default: false, // Parent will control this state
      required: true,
    },
    pairedPoem: {
      type: Array as PropType<string[][]>, // Array of string arrays
      required: true,
      default: () => [], // Default to an empty array
    },
  },
  emits: ["submit", "update:isLoading", "update:pairedPoem"], // Emit loading state to parent
  setup(props, { emit }) {
    const selectedUserInput = ref(""); // Track user input

    // Computed property to handle default value
    const processedUserInput = computed(() => {
      return selectedUserInput.value.trim() ? selectedUserInput.value : "الذكاء الصناعي سلما";
    });

    const handleSubmit = async () => {
      emit("update:isLoading", true); // Notify parent that loading has started
      emit("submit");
      await new Promise((resolve) => setTimeout(resolve, 5000)); // Simulate loading
      emit("update:isLoading", false); // Notify parent that loading has ended
    };

    // Delete a poem line
    const deleteLine = (index: number) => {
      const updatedPoem = props.pairedPoem.slice(); // Create a shallow copy to modify
      updatedPoem.splice(index, 1); // Remove the line from the array
      emit("update:pairedPoem", updatedPoem); // Notify parent of the updated poem
    };

    return {
      selectedUserInput,
      processedUserInput,

      handleSubmit,

      deleteLine,
    };
  },
});
</script>

<template>
  <div class="flex flex-col items-center pl-10 w-full">
    <!-- Submit Button -->
    <div class="flex items-center w-full mb-4">
      <button
          @click="handleSubmit"
          :disabled="disabled"
          class="ml-3 bg-black hover:bg-gray-800 text-white p-3 rounded-full
          disabled:cursor-not-allowed"
      >
        <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 10l7-7m0 0l7 7m-7-7v18" />
        </svg>
      </button>

      <!-- Input Box -->
      <div class="flex items-center border rounded-xl p-3 w-full">
        <input
            :disabled="disabled"
            type="text"
            v-model="selectedUserInput"
            placeholder="أدخل فكرة القصيدة أو البيت الأول..."
            class="w-full bg-transparent placeholder-gray-300 focus:outline-none disabled:cursor-not-allowed"
        >
      </div>
    </div>

    <!-- Loading Indicator -->
    <div v-if="disabled" class="text-sm mt-15">
      جاري التحميل...
    </div>

    <!-- Generated Poem -->
    <div v-if="!disabled && pairedPoem.length > 0" class="w-full">
      <div
          v-for="(linePair, index) in pairedPoem"
          :key="index"
          class="flex justify-between text-center text-sm mt-5 items-center"
      >
        <button
            v-if="pairedPoem.length > 0"
            @click="deleteLine(index)"
            class="ml-3 bg-black px-2 py-1 rounded hover:bg-red-700"
        >
          حذف
        </button>

        <div class="w-1/2" v-if="linePair[0]">{{ linePair[0] }}</div>
        <div class="w-1/2" v-if="linePair[1]">{{ linePair[1] }}</div>
      </div>
    </div>

  </div>
</template>


<style scoped lang="scss">
</style>