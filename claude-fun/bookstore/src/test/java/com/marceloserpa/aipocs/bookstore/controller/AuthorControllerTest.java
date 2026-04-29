package com.marceloserpa.aipocs.bookstore.controller;

import com.marceloserpa.aipocs.bookstore.model.Author;
import com.marceloserpa.aipocs.bookstore.repository.AuthorRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class AuthorControllerTest {

    @Mock
    private AuthorRepository authorRepository;

    @InjectMocks
    private AuthorController authorController;

    @Test
    void listAll_returnsAllAuthors() {
        Author author = new Author("Robert", "Martin", "Clean Code author");
        when(authorRepository.findAll()).thenReturn(List.of(author));

        List<Author> result = authorController.listAll();

        assertThat(result).containsExactly(author);
    }

    @Test
    void getById_returnsOk_whenFound() {
        Author author = new Author("Robert", "Martin", "Clean Code author");
        author.setId(1L);
        when(authorRepository.findById(1L)).thenReturn(Optional.of(author));

        ResponseEntity<Author> response = authorController.getById(1L);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody()).isEqualTo(author);
    }

    @Test
    void getById_returnsNotFound_whenNotFound() {
        when(authorRepository.findById(99L)).thenReturn(Optional.empty());

        ResponseEntity<Author> response = authorController.getById(99L);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
    }

    @Test
    void create_returnsCreated() {
        Author saved = new Author("Martin", "Fowler", "Refactoring author");
        saved.setId(2L);
        when(authorRepository.save(any(Author.class))).thenReturn(saved);

        AuthorController.AuthorRequest request =
                new AuthorController.AuthorRequest("Martin", "Fowler", "Refactoring author");

        ResponseEntity<Author> response = authorController.create(request);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getBody()).isEqualTo(saved);
    }
}
