document.addEventListener("DOMContentLoaded", function () {
    const booksTable = document.querySelector("#books-table tbody");
    const editBookForm = document.getElementById("edit-book-form");

    // Add Book Form Submission
    const addBookForm = document.getElementById("create-book-form");
    if (addBookForm) {
        addBookForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const formData = {
                title: document.getElementById("title").value,
                author_name: document.getElementById("author").value,
                language: document.getElementById("language").value,
                subject: document.getElementById("subject").value,
                genre: document.getElementById("genre").value,
            };

            const csrftoken = getCookie("csrftoken");

            fetch("/api/books/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify(formData),
            })
                .then((response) => {
                    if (!response.ok) {
                        return response.json().then((data) => {
                            throw new Error(JSON.stringify(data));
                        });
                    }
                    return response.json();
                })
                .then(() => {
                    alert("Book added successfully!");
                    window.location.href = "/data/"; // Redirect to data.html
                })
                .catch((error) => console.error("Error adding book:", error.message));
        });
    }

    // Handle Edit Button Click
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("edit-btn")) {
            const bookId = event.target.getAttribute("data-id");

            fetch(`/api/books/${bookId}/`)
                .then((response) => response.json())
                .then((book) => {
                    document.getElementById("edit-book-id").value = book.id;
                    document.getElementById("edit-title").value = book.title;
                    document.getElementById("edit-author").value = book.author_name;
                    document.getElementById("edit-language").value = book.language;
                    document.getElementById("edit-subject").value = book.subject;
                    document.getElementById("edit-genre").value = book.genre;

                    editBookForm.style.display = "block"; // Show edit form
                })
                .catch((error) => console.error("Error fetching book:", error));
        }
    });

    // Handle Edit Form Submission
    if (editBookForm) {
        editBookForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const bookId = document.getElementById("edit-book-id").value;
            const formData = {
                title: document.getElementById("edit-title").value,
                author_name: document.getElementById("edit-author").value,
                language: document.getElementById("edit-language").value,
                subject: document.getElementById("edit-subject").value,
                genre: document.getElementById("edit-genre").value,
            };

            const csrftoken = getCookie("csrftoken");

            fetch(`/api/books/${bookId}/`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify(formData),
            })
                .then((response) => {
                    if (!response.ok) {
                        return response.json().then((data) => {
                            throw new Error(JSON.stringify(data));
                        });
                    }
                    return response.json();
                })
                .then(() => {
                    alert("Book updated successfully!");
                    editBookForm.style.display = "none"; // Hide edit form
                    location.reload(); // Reload page
                })
                .catch((error) => console.error("Error updating book:", error.message));
        });
    }

    // Handle Delete Button Click
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-btn")) {
            const bookId = event.target.getAttribute("data-id");
            const csrftoken = getCookie("csrftoken");

            if (confirm("Are you sure you want to delete this book?")) {
                fetch(`/api/books/${bookId}/`, {
                    method: "DELETE",
                    headers: {
                        "X-CSRFToken": csrftoken,
                    },
                })
                    .then((response) => {
                        if (!response.ok) {
                            return response.json().then((data) => {
                                throw new Error(JSON.stringify(data));
                            });
                        }
                        alert("Book deleted successfully!");
                        location.reload(); // Reload page
                    })
                    .catch((error) => console.error("Error deleting book:", error.message));
            }
        }
    });

    // Get CSRF Token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
