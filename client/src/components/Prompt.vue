<template>
  <div>
    <b-modal ref="promptModal"
           id="prompt-modal"
           :title="message"
           hide-footer>
      <b-form class="w-100">
        <b-button type="submit" variant="primary" @click="handleYes">
          Yes</b-button>
        <b-button type="reset" variant="danger" @click="handleNo">No</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
export default {
  props: ['message'],
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
