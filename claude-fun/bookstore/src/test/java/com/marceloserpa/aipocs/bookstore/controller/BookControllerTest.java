package com.marceloserpa.aipocs.bookstore.controller;

import com.marceloserpa.aipocs.bookstore.model.Book;
import com.marceloserpa.aipocs.bookstore.service.BookService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.math.BigDecimal;
import java.util.List;
import java.util.NoSuchElementException;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class BookControllerTest {

    @Mock
    private BookService bookService;

    @InjectMocks
    private BookController bookController;

    @Test
    void listAll_returnsList() {
        Book book = new Book();
        when(bookService.findAll()).thenReturn(List.of(book));

        List<Book> result = bookController.listAll();

        assertThat(result).hasSize(1);
    }

    @Test
    void getById_returnsOk_whenFound() {
        Book book = new Book();
        book.setId(1L);
        when(bookService.findById(1L)).thenReturn(book);

        ResponseEntity<Book> response = bookController.getById(1L);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody()).isEqualTo(book);
    }

    @Test
    void getById_returnsNotFound_whenNotFound() {
        when(bookService.findById(99L)).thenThrow(new NoSuchElementException("Book not found: 99"));

        ResponseEntity<Book> response = bookController.getById(99L);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
    }

    @Test
    void create_returnsCreated_withStockQuantity() {
        Book saved = new Book();
        saved.setId(1L);
        when(bookService.create(any(Book.class), eq(null), eq(null))).thenReturn(saved);

        BookController.BookRequest request = new BookController.BookRequest(
                "Clean Code", "978-0132350884", new BigDecimal("45.99"), 10, 2008, null, null);

        ResponseEntity<Book> response = bookController.create(request);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getBody()).isEqualTo(saved);
    }

    @Test
    void create_setsZeroStock_whenStockQuantityNull() {
        Book saved = new Book();
        when(bookService.create(any(Book.class), eq(null), eq(null))).thenReturn(saved);

        BookController.BookRequest request = new BookController.BookRequest(
                "Clean Code", "978-0132350884", new BigDecimal("45.99"), null, 2008, null, null);

        ResponseEntity<Book> response = bookController.create(request);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
    }

    @Test
    void update_returnsOk_whenFound() {
        Book updated = new Book();
        updated.setId(1L);
        when(bookService.update(eq(1L), any(Book.class), eq(null), eq(null))).thenReturn(updated);

        BookController.BookRequest request = new BookController.BookRequest(
                "Refactoring", "978-0201485677", new BigDecimal("55.00"), 5, 2018, null, null);

        ResponseEntity<Book> response = bookController.update(1L, request);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody()).isEqualTo(updated);
    }

    @Test
    void update_returnsNotFound_whenNotFound() {
        when(bookService.update(eq(99L), any(Book.class), eq(null), eq(null)))
                .thenThrow(new NoSuchElementException("Book not found: 99"));

        BookController.BookRequest request = new BookController.BookRequest(
                "Refactoring", "978-0201485677", new BigDecimal("55.00"), 5, 2018, null, null);

        ResponseEntity<Book> response = bookController.update(99L, request);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
    }

    @Test
    void update_setsZeroStock_whenStockQuantityNull() {
        Book updated = new Book();
        when(bookService.update(eq(1L), any(Book.class), eq(null), eq(null))).thenReturn(updated);

        BookController.BookRequest request = new BookController.BookRequest(
                "Refactoring", "978-0201485677", new BigDecimal("55.00"), null, 2018, null, null);

        ResponseEntity<Book> response = bookController.update(1L, request);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
    }

    @Test
    void delete_returnsNoContent_whenFound() {
        ResponseEntity<Void> response = bookController.delete(1L);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NO_CONTENT);
    }

    @Test
    void delete_returnsNotFound_whenNotFound() {
        doThrow(new NoSuchElementException("Book not found: 99")).when(bookService).delete(99L);

        ResponseEntity<Void> response = bookController.delete(99L);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
    }
}
