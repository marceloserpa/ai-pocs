package com.marceloserpa.aipocs.bookstore.controller;

import com.marceloserpa.aipocs.bookstore.AbstractIntegrationTest;
import com.marceloserpa.aipocs.bookstore.model.Book;
import com.marceloserpa.aipocs.bookstore.repository.BookRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.client.RestTestClient;
import org.springframework.web.context.WebApplicationContext;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.Map;

class BookControllerIT extends AbstractIntegrationTest {

    @Autowired
    WebApplicationContext context;

    @Autowired
    BookRepository bookRepository;

    RestTestClient client;

    @BeforeEach
    void setUp() {
        bookRepository.deleteAll();
        client = RestTestClient.bindToApplicationContext(context).build();
    }

    @Test
    void create_shouldReturnCreated_whenRequestIsValid() {
        Map<String, Object> payload = new HashMap<>();
        payload.put("title", "Clean Code");
        payload.put("isbn", "978-0132350884");
        payload.put("price", 29.99);
        payload.put("stockQuantity", 5);
        payload.put("publicationYear", 2008);

        client.post().uri("/api/books")
                .contentType(MediaType.APPLICATION_JSON)
                .body(payload)
                .exchange()
                .expectStatus().isCreated()
                .expectBody()
                .jsonPath("$.title").isEqualTo("Clean Code")
                .jsonPath("$.isbn").isEqualTo("978-0132350884")
                .jsonPath("$.stockQuantity").isEqualTo(5);
    }

    @Test
    void getById_shouldReturnBook_whenBookExists() {
        Book book = new Book();
        book.setTitle("The Pragmatic Programmer");
        book.setIsbn("978-0135957059");
        book.setPrice(new BigDecimal("39.99"));
        book.setStockQuantity(3);
        Book saved = bookRepository.save(book);

        client.get().uri("/api/books/{id}", saved.getId())
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.id").isEqualTo(saved.getId())
                .jsonPath("$.title").isEqualTo("The Pragmatic Programmer");
    }

    @Test
    void getById_shouldReturnNotFound_whenBookDoesNotExist() {
        client.get().uri("/api/books/{id}", 9999L)
                .exchange()
                .expectStatus().isNotFound();
    }
}
