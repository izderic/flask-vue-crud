<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Books</h1>
        <hr>
        <br><br>
        <alert :message=message variant="success" v-if="message"></alert>
        <button type="button" class="btn btn-success btn-sm"
                @click="showBookModal">Add Book</button>
        <br><br>

        <template v-if="books.length">
          <!-- books table -->
          <table id="books-table" class="table table-hover table-bordered table-dark">
            <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Author</th>
              <th scope="col">Read?</th>
              <th scope="col">Purchase Price</th>
              <th></th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(book, index) in books" :key="index">
              <td>{{ book.title }}</td>
              <td>{{ book.author }}</td>
              <td>
                <span v-if="book.read">Yes</span>
                <span v-else>No</span>
              </td>
              <td>${{ book.price }}</td>
              <td>
                <button type="button"
                        class="btn btn-warning btn-sm mt-1"
                        @click="editBook(book)">
                  Update

                </button>
                <button type="button"
                        class="btn btn-danger btn-sm mt-1"
                        @click="showDeleteModal(book)">
                  Delete
                </button>

                <router-link :to="`/order/${book.id}`"
                             class="btn btn-primary btn-sm mt-1">
                  Purchase

                </router-link>
              </td>
            </tr>
            </tbody>
          </table>
        </template>
        <template v-else>No books at the momemt.</template>

      </div>
    </div>

    <!-- add/edit book modal -->
    <b-modal ref="bookModal"
             id="book-modal"
             :title="bookModalTitle"
             hide-footer>
      <alert :message=modalMessage variant="danger" v-if="modalMessage"></alert>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-title-group"
                      label="Title:"
                      label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="bookForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="Author:"
                      label-for="form-author-input">
          <b-form-input id="form-author-input"
                        type="text"
                        v-model="bookForm.author"
                        required
                        placeholder="Enter author">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-price-group"
                      label="Purchase price:"
                      label-for="form-price-input">
          <b-form-input id="form-price-input"
                        type="number"
                        v-model="bookForm.price"
                        required
                        placeholder="Enter price">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-read-group">
          <b-form-checkbox-group v-model="bookForm.read" id="form-checks">
            <b-form-checkbox value="true">Read?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>

        <b-button type="submit" variant="primary">
          <template v-if="bookForm.id">Update</template>
          <template v-else>Submit</template>
        </b-button>
        <b-button type="reset" variant="danger">
          <template v-if="bookForm.id">Cancel</template>
          <template v-else>Reset</template>
        </b-button>

      </b-form>
    </b-modal>

    <!--delete book modal-->
    <prompt
      ref="prompt"
      v-on:yes="onDeleteBook(bookToDelete)"
      title="Warning"
      message="Are you sure you want to delete this book?">
    </prompt>

  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert';
import Prompt from './Prompt';

export default {
  data() {
    return {
      books: [],
      bookForm: {
        id: '',
        title: '',
        author: '',
        read: [],
        price: '',
      },
      message: '',
      modalMessage: '',
      bookToDelete: '',
    };
  },
  components: {
    alert: Alert,
    prompt: Prompt,
  },
  computed: {
    bookModalTitle() {
      return this.bookForm.id ? 'Update' : 'Add a new book';
    },
  },
  methods: {
    getBooks() {
      const path = 'http://localhost:5000/books';
      axios.get(path)
        .then((res) => {
          this.books = res.data.books;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addBook(payload) {
      const path = 'http://localhost:5000/books';
      axios.post(path, payload)
        .then(() => {
          this.getBooks();
          this.message = 'Book added!';
          this.$refs.bookModal.hide();
          this.initForm();
        })
        .catch((error) => {
          this.modalMessage = error.response.data.message;
          this.getBooks();
        });
    },
    updateBook(payload, bookID) {
      const path = `http://localhost:5000/books/${bookID}`;
      axios.put(path, payload)
        .then(() => {
          this.getBooks();
          this.message = 'Book updated!';
          this.$refs.bookModal.hide();
          this.initForm();
        })
        .catch((error) => {
          this.modalMessage = error.response.data.message;
          this.getBooks();
        });
    },
    removeBook(bookID) {
      const path = `http://localhost:5000/books/${bookID}`;
      axios.delete(path)
        .then(() => {
          this.getBooks();
          this.message = 'Book removed!';
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
    initForm() {
      this.bookForm.id = '';
      this.bookForm.title = '';
      this.bookForm.author = '';
      this.bookForm.read = [];
      this.bookForm.price = '';
      this.modalMessage = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      let read = false;
      if (this.bookForm.read[0]) read = true;
      const payload = {
        title: this.bookForm.title,
        author: this.bookForm.author,
        read, // property shorthand
        price: this.bookForm.price,
      };
      if (this.bookForm.id) {
        this.updateBook(payload, this.bookForm.id);
      } else {
        this.addBook(payload);
      }
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.bookModal.hide();
      this.initForm();
      this.getBooks();
    },
    onDeleteBook(book) {
      this.removeBook(book.id);
      this.$refs.prompt.hide();
    },
    editBook(book) {
      this.bookForm.id = book.id;
      this.bookForm.title = book.title;
      this.bookForm.author = book.author;
      this.bookForm.read = book.read;
      this.bookForm.price = book.price;
      this.$refs.bookModal.show();
    },
    showDeleteModal(book) {
      this.$refs.prompt.show();
      this.bookToDelete = book;
    },
    showBookModal() {
      this.initForm();
      this.$refs.bookModal.show();
    },
  },
  created() {
    this.getBooks();
  },
};
</script>

<style scoped>
  #books-table th {color: greenyellow;}
</style>
