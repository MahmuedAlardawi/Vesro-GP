<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'AboutView',

  setup() {
    return {};
  }
});
</script>

<template>
  <div class="AboutView mx-auto max-w-4xl px-5">
    <h1 class="text-3xl font-bold text-center mb-4">حول Verso</h1>
    <p class="text-lg leading-relaxed mb-4">
      Verso AI هو منصة مبتكرة لإنشاء الشعر باستخدام الذكاء الاصطناعي.
      تعتمد المنصة على أحدث تقنيات الذكاء الاصطناعي لإنشاء أشعار ملهمة وآسرة، مما يجسر الفجوة بين الفن والتكنولوجيا.
    </p>
    <p class="text-lg leading-relaxed mb-4">
      تم تطوير هذا المشروع بتفانٍ وإبداع من قبل فريق متميز من الأفراد الشغوفين:
    </p>
    <ul class="list-disc list-inside text-lg mb-4">
      <li>محمود العرداوي</li>
      <li>ثامر المالكي</li>
      <li>رواد الغامدي</li>
    </ul>
    <p class="text-lg leading-relaxed">
      في Verso AI، نؤمن بقوة الشعر في ربط الناس، وإثارة المشاعر، وإشعال الخيال.
      سواء كنت من عشاق الشعر، أو كاتبًا، أو شخصًا مهتمًا بقدرات الذكاء الاصطناعي الإبداعية، فإن Verso AI يقدم شيئًا للجميع.
    </p>
  </div>
</template>


<style lang="scss">

</style>
