// Book Inventory JavaScript
document.addEventListener("DOMContentLoaded", function () {
  // Get DOM elements
  const searchForm = document.querySelector(".search-form");
  const searchInput = document.getElementById("search-input");
  const booksTableBody = document.querySelector("#books-table tbody");

  // Load initial book data
  function loadBooks(query = "") {
    fetch(`/books${query ? "?q=" + encodeURIComponent(query) : ""}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          populateTable(data.books);
        }
      })
      .catch((error) => console.error("Error loading books:", error));
  }

  // Populate table with book data
  function populateTable(books) {
    booksTableBody.innerHTML = "";

    if (books.length === 0) {
      booksTableBody.innerHTML =
        '<tr><td colspan="6" class="no-results">No books found</td></tr>';
      return;
    }

    books.forEach((book) => {
      const row = document.createElement("tr");

      row.innerHTML = `
                <td>${book.title}</td>
                <td>${book.author}</td>
                <td>${book.isbn}</td>
                <td>${book.available_quantity}</td>
                <td>${book.total_quantity}</td>
                <td class="actions">
                    <button class="edit-btn" data-id="${book.id}">Edit</button>
                    <button class="delete-btn" data-id="${book.id}">Delete</button>
                </td>
            `;

      booksTableBody.appendChild(row);
    });

    // Add event listeners to action buttons
    document.querySelectorAll(".edit-btn").forEach((btn) => {
      btn.addEventListener("click", handleEditBook);
    });

    document.querySelectorAll(".delete-btn").forEach((btn) => {
      btn.addEventListener("click", handleDeleteBook);
    });
  }

  // Handle search form submission
  searchForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const query = searchInput.value.trim();
    loadBooks(query);
  });

  // Handle edit book
  function handleEditBook(e) {
    const bookId = e.target.dataset.id;
    // Implement edit functionality
    alert("Edit functionality for book ID " + bookId + " will be implemented");
  }

  // Handle delete book
  function handleDeleteBook(e) {
    const bookId = e.target.dataset.id;
    if (confirm("Are you sure you want to delete this book?")) {
      fetch(`/books/${bookId}`, { method: "DELETE" })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            loadBooks(); // Refresh the list
          }
        })
        .catch((error) => console.error("Error deleting book:", error));
    }
  }

  // Initial load
  loadBooks();
});
