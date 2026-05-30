<template>
  <div class="laquiz" :class="{ 'is-submitted': submitted }">
    <div class="laquiz-body">
      <div class="laquiz-q">
        <slot />
      </div>
      <div
        v-for="(choice, i) in choices"
        :key="i"
        class="laquiz-choice"
        :class="{
          'laquiz-choice--correct': submitted && i === answerIndex,
          'laquiz-choice--wrong': submitted && selected === i && i !== answerIndex,
          'laquiz-choice--dimmed': submitted && selected !== i && i !== answerIndex,
          'laquiz-choice--disabled': submitted,
        }"
        @click="select(i)"
      >
        <span class="laquiz-choice-marker">{{ markers[i] }}</span>
        <span class="laquiz-choice-content">{{ choice }}</span>
      </div>
      <div v-if="submitted" class="laquiz-result" :class="isCorrect ? 'laquiz-result--ok' : 'laquiz-result--fail'">
        {{ isCorrect ? 'Correct!' : `Incorrect, the answer is ${markers[answerIndex]}` }}
        <span v-if="!isCorrect" class="laquiz-retry" @click="reset">Retry</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';

export default {
  name: 'ChoiceX',
  props: {
    choices: { type: Array, required: true },
    answer: { type: Number, required: true },
  },
  setup(props) {
    const markers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
    const submitted = ref(false);
    const selected = ref(-1);

    const answerIndex = computed(() => props.answer - 1);
    const isCorrect = computed(() => selected.value === answerIndex.value);

    function select(idx) {
      if (submitted.value) return;
      selected.value = idx;
      submitted.value = true;
    }

    function reset() {
      submitted.value = false;
      selected.value = -1;
    }

    return { markers, submitted, selected, answerIndex, isCorrect, select, reset };
  },
};
</script>

<style scoped>
.laquiz {
  max-width: 720px;
  margin: 16px auto;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  background: #fff;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
}

.laquiz-body {
  padding: 14px 16px;
}

.laquiz-q {
  margin-bottom: 10px;
  font-size: 15px;
  line-height: 1.6;
  color: #1e293b;
  font-weight: 500;
}

.laquiz-choice {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  margin-bottom: 6px;
  border: 1.5px solid #e2e8f0;
  border-radius: 7px;
  cursor: pointer;
  transition: all .15s ease;
  background: #fff;
}

.laquiz-choice:hover:not(.laquiz-choice--disabled) {
  border-color: #818cf8;
  background: #eef2ff;
}

.laquiz-choice--correct {
  border-color: #22c55e;
  background: #f0fdf4;
}

.laquiz-choice--wrong {
  border-color: #ef4444;
  background: #fef2f2;
}

.laquiz-choice--dimmed {
  opacity: .45;
}

.laquiz-choice--disabled {
  cursor: default;
}

.laquiz-choice-marker {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  border-radius: 5px;
  background: #f1f5f9;
  color: #475569;
  font-size: 12px;
  font-weight: 600;
  margin-right: 10px;
  flex-shrink: 0;
  transition: all .15s ease;
}

.laquiz-choice--correct .laquiz-choice-marker {
  background: #22c55e;
  color: #fff;
}

.laquiz-choice--wrong .laquiz-choice-marker {
  background: #ef4444;
  color: #fff;
}

.laquiz-choice-content {
  font-size: 14px;
  line-height: 1.5;
  color: #1e293b;
}

.laquiz-result {
  margin-top: 10px;
  font-size: 13px;
  font-weight: 600;
  line-height: 1.5;
}

.laquiz-result--ok {
  color: #16a34a;
}

.laquiz-result--fail {
  color: #dc2626;
}

.laquiz-retry {
  margin-left: 8px;
  color: #6366f1;
  cursor: pointer;
  font-weight: 500;
}

.laquiz-retry:hover {
  color: #4f46e5;
  text-decoration: underline;
}
</style>
