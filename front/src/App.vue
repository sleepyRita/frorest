<script>
import { RouterView } from 'vue-router';

export default {
  data() {
    return {
      importances: {},
    };
  },
  name: 'App',
  components: {
    RouterView,
  },
  methods: {
    dealRes(importance) {
      this.importances = importance;
    },
  },
};
</script>

<template>
  <div class="top">
    <RouterView name="top"></RouterView>
  </div>
  <div class="main">

    <div class="left">
      <RouterView name="left" @result="(importance) => dealRes(importance)">
      </RouterView>
    </div>
    <div class="right">
      <RouterView name="right" :importances="importances"></RouterView>
    </div>

  </div>
</template>

<style scoped></style>