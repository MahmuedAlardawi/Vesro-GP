<script lang="ts">
import {defineComponent, onMounted, PropType, ref, watch} from "vue";
import axios from "axios";

export default defineComponent({
  name: "HomeComponent_2",
  props: {
    pairedPoem: {
      type: Array as PropType<string[][]>, // Array of string arrays
      required: true,
      default: () => [], // Default to an empty array
    },
  },
  emits: ["update:pairedPoem"], // Emit changes to the parent

  setup(props, { emit }) {
    // Initial lines with empty boxes
    const lines = ref<{ boxes: { content: string; analysis?: any }[] }[]>([]);

    // Populate lines with pairedPoem data and send pre-filled data to the backend
    onMounted(() => {
      for (const [lineIndex, pair] of props.pairedPoem.entries()) {
        const line = {
          boxes: pair.map((content: string) => ({ content, analysis: undefined })), // Initialize analysis as undefined
        };

        lines.value.push(line);

        // Send pre-filled data to the backend for each box
        line.boxes.forEach((box, boxIndex) => {
          if (box.content.trim()) {
            sendDataToBackend_generateAnalysis(lineIndex, boxIndex); // Call the backend for pre-filled content
          }
        });
      }
    });

    // Watch for changes in lines and emit updated pairedPoem to the parent
    watch(
        lines,
        (newLines) => {
          const updatedPairedPoem = newLines.map((line) =>
              line.boxes.map((box) => box.content)
          );
          emit("update:pairedPoem", updatedPairedPoem);
        },
        { deep: true } // Ensure deep watching for nested changes
    );

    // Add a new line with two empty boxes
    const addLine = () => {
      lines.value.push({
        boxes: [{ content: "" }, { content: "" }],
      });
    };

    // Delete a line by index
    const deleteLine = (index: number) => {
      lines.value.splice(index, 1);
    };

    // Send data to backend when a box is updated
    const sendDataToBackend_generateAnalysis = async (lineIndex: number, boxIndex: number) => {
      const box = lines.value[lineIndex].boxes[boxIndex];

      if (box.content.trim()) {
        try {
          const response = await axios.post("http://127.0.0.1:8000/api/generate_analysis/", {
            verse: box.content.trim(),
          });

          // Parse the analysis field if it's a JSON string
          // Store the parsed analysis in the box
          box.analysis =
              typeof response.data.analysis === "string"
                  ? JSON.parse(response.data.analysis)
                  : response.data.analysis;

          // Log success message
          console.log(
              `Success: Analysis for line ${lineIndex + 1}, box ${boxIndex + 1} received.`,
              response.data
          );
        } catch (error) {
          console.error("Error analyzing poem:", error);
        }
      }
    };

    const sendDataToBackend_generateDiacritization = async (lineIndex: number, boxIndex: number) => {
      const box = lines.value[lineIndex].boxes[boxIndex];

      if (box.content.trim()) {
        try {
          // Send the verse to the backend for diacritization
          const response = await axios.post("http://127.0.0.1:8000/api/generate_diacritization_colab/", {
            poem: box.content.trim(),
          });

          // Update the content with the diacritized verse received from the backend
          box.content = response.data.response;

          console.log(
              `Diacritized verse for Line ${lineIndex + 1}, Box ${boxIndex + 1} received:`,
              response.data.response
          );

          // Automatically send the diacritized verse for analysis
          await sendDataToBackend_generateAnalysis(lineIndex, boxIndex);

        } catch (error) {
          console.error("Error diacritizing verse:", error);
        }
      } else {
        console.warn(`Box at Line ${lineIndex + 1}, Box ${boxIndex + 1} is empty. Cannot diacritize.`);
      }
    };

    return {
      lines,
      addLine,
      deleteLine,

      sendDataToBackend_generateAnalysis,
      sendDataToBackend_generateDiacritization,
    };
  },
});
</script>


<template>
  <div class="pl-10 text-xs">
    <!-- Dynamic Lines -->
    <div>
      <div
          v-for="(line, lineIndex) in lines"
          :key="lineIndex"
          class="mb-8"
      >
        <!-- Line Header -->
        <div class="mb-4 flex justify-between items-center">
          <h1 class="text-3xl text-right">البيت {{ lineIndex + 1 }}</h1>
          <button
              @click="deleteLine(lineIndex)"
              class="bg-black py-1 px-4 rounded-full hover:bg-red-700 transition"
          >
            -
          </button>
        </div>

        <!-- Two Editable Boxes Per Line -->
        <div class="grid grid-cols-2 gap-3">
          <div
              v-for="(box, boxIndex) in line.boxes"
              :key="boxIndex"
              class=""
          >

            <!-- Verse headline -->
            <h1 class="text-right mb-2">الشطر {{ boxIndex + 1 }}</h1>

            <div class="flex flex-col items-end">
              <!-- Editable Textarea -->
              <textarea
                  v-model="box.content"
                  @blur="sendDataToBackend_generateAnalysis(lineIndex, boxIndex)"
                  placeholder="اكتب..."
                  class="w-full h-auto bg-transparent placeholder-gray-300 border rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-purple-600 resize-none"
              ></textarea>

              <!-- Small Tashkeel Button -->
              <button
                  @click="sendDataToBackend_generateDiacritization(lineIndex, boxIndex)"
                  class="bg-black px-2 py-1 text-xs rounded mt-1 hover:bg-gray-500 transition"
              >
                تشكيل
              </button>
            </div>

            <!-- Analysis -->
            <div v-if="box.analysis" class="mt-4 p-4 border rounded-md ">

              <!-- Display general analysis -->
              <div class="mb-6 text-right space-y-3">
                <p><strong>الكتابة المشكلة:</strong> {{ box.analysis.discretized_poem }}</p>
                <p><strong>الكتابة العروضية:</strong> {{ box.analysis.normalized_poem }}</p>
                <p><strong>البحر:</strong> {{ box.analysis.meter }}</p>
                <p><strong>نسبة التطابق:</strong> {{ box.analysis.matching_percentage }}</p>
              </div>

              <!-- Table for word analysis -->
              <div class="overflow-x-auto">
                <table class="table-auto border-collapse w-full text-right ">
                  <thead class="bg-black">
                  <tr>
                    <th class="border px-4 py-2">الكلمة</th>
                    <th class="border px-4 py-2">ترميز الكلمة</th>
                    <th class="border px-4 py-2">التفعيلة</th>
                    <th class="border px-4 py-2">ترميز التفعيلة</th>
                    <th class="border px-4 py-2">ترميز التطابق</th>
                    <th class="border px-4 py-2">نسبة التطابق</th>
                  </tr>
                  </thead>

                  <tbody>
                  <tr v-for="(word, index) in box.analysis.words" :key="index">
                    <td class="border px-4 py-2">{{ word.normalized_word }}</td>
                    <td class="border px-4 py-2">{{ word.binary_word }}</td>
                    <td class="border px-4 py-2">{{ word.tafeela }}</td>
                    <td class="border px-4 py-2">{{ word.binary_tafeela }}</td>
                    <td class="border px-4 py-2">{{ word.binary_match }}</td>
                    <td class="border px-4 py-2">{{ word.matching_percentage }}</td>
                  </tr>
                  </tbody>
                </table>
              </div>

              <!-- Changes Section -->
              <div class="mt-6 text-right">
                <h4 class="mb-4">التغييرات:</h4>
                <ul class="list-disc list-inside space-y-2">
                  <!-- Iterate over words and handle change logic -->
                  <li v-for="(word, index) in box.analysis.words" :key="index">
                    <strong>{{ word.normalized_word }}:</strong>
                    <span class="mr-2 ml-2">{{ word.change ? word.change : "لا يوجد تغيير" }}</span>
                    <span v-if="word.original_tafeela">
                      <strong>والتفعيلة الأصلية: {{ word.original_tafeela }}</strong>
                    </span>
                  </li>
                </ul>
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>

    <!-- Add New Line Button -->
    <div class="text-center mt-8">
      <button
          @click="addLine"
          class="bg-black py-1 px-4 rounded-full hover:bg-green-700 transition"
      >
        +
      </button>
    </div>
  </div>
</template>

<style scoped lang="scss">

</style>