<template>
  <div>
    <b-modal ref="promptModal"
           id="prompt-modal"
           :title="title"
           hide-footer>
      <div class="d-block text-center">
        {{ message }}
      </div>
      <b-button class="mt-3" type="submit" variant="primary" @click="handleYes">
        Yes</b-button>
      <b-button class="mt-3" type="reset" variant="danger" @click="handleNo">No</b-button>
    </b-modal>
  </div>
</template>

<script>
export default {
  props: ['title', 'message'],
  methods: {
    handleYes() {
      this.$emit('yes');
      this.hide();
    },
    handleNo() {
      this.$emit('no');
      this.hide();
    },
    show() {
      this.$refs.promptModal.show();
    },
    hide() {
      this.$refs.promptModal.hide();
    },
  },
};
</script>
