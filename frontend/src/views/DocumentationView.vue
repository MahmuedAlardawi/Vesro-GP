<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'DocumentationView',

  setup() {
    // Use the public folder or resolve the path with require
    const pdfUrl = ref('/assets/VERSO_final_report.pdf');

    return {
      pdfUrl,
    };
  },
});
</script>

<template>
  <div class="mx-auto max-w-5xl p-8 rounded-lg">
    <h1 class="text-4xl font-bold text-center mb-6">📄 التوثيق</h1>
    <p class="text-lg leading-relaxed mb-6 text-center">
      أدناه تجد توثيق مشروعنا. يمكنك عرض الملف مباشرة أو تنزيله باستخدام الرابط أدناه:
    </p>
    <div class="pdf-actions text-center mb-4 flex flex-col space-y-4">
      <a
          :href="pdfUrl"
          target="_blank"
          class="bg-black text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition"
      >
        عرض الملف في علامة تبويب جديدة
      </a>
      <a
          :href="pdfUrl"
          download
          class="bg-black text-white px-6 py-2 rounded-lg hover:bg-green-600 transition"
      >
        تنزيل الملف
      </a>
    </div>

    <div class="pdf-viewer mt-6 border rounded-lg overflow-hidden shadow-md">
      <iframe
          :src="pdfUrl"
          class="w-full h-[75vh] border"
          title="ملف التوثيق PDF"
      >
      </iframe>
    </div>
  </div>
</template>

<style lang="scss">
</style>
