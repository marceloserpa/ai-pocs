package com.marceloserpa.aipocs.bookstore.controller;

import com.marceloserpa.aipocs.bookstore.model.Book;
import com.marceloserpa.aipocs.bookstore.service.BookService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.List;
import java.util.NoSuchElementException;

@RestController
@RequestMapping("/api/books")
public class BookController {

    private final BookService bookService;

    public BookController(BookService bookService) {
        this.bookService = bookService;
    }

    @GetMapping
    public List<Book> listAll() {
        return bookService.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Book> getById(@PathVariable Long id) {
        try {
            return ResponseEntity.ok(bookService.findById(id));
        } catch (NoSuchElementException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @PostMapping
    public ResponseEntity<Book> create(@RequestBody BookRequest request) {
        Book book = new Book();
        book.setTitle(request.title());
        book.setIsbn(request.isbn());
        book.setPrice(request.price());
        book.setStockQuantity(request.stockQuantity() != null ? request.stockQuantity() : 0);
        book.setPublicationYear(request.publicationYear());
        Book saved = bookService.create(book, request.authorId(), request.publisherId());
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Book> update(@PathVariable Long id, @RequestBody BookRequest request) {
        try {
            Book book = new Book();
            book.setTitle(request.title());
            book.setIsbn(request.isbn());
            book.setPrice(request.price());
            book.setStockQuantity(request.stockQuantity() != null ? request.stockQuantity() : 0);
            book.setPublicationYear(request.publicationYear());
            return ResponseEntity.ok(bookService.update(id, book, request.authorId(), request.publisherId()));
        } catch (NoSuchElementException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        try {
            bookService.delete(id);
            return ResponseEntity.noContent().build();
        } catch (NoSuchElementException e) {
            return ResponseEntity.notFound().build();
        }
    }

    record BookRequest(
            String title,
            String isbn,
            BigDecimal price,
            Integer stockQuantity,
            Integer publicationYear,
            Long authorId,
            Long publisherId
    ) {}
}
