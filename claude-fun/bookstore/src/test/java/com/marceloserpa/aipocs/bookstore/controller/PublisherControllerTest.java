package com.marceloserpa.aipocs.bookstore.controller;

import com.marceloserpa.aipocs.bookstore.model.Publisher;
import com.marceloserpa.aipocs.bookstore.repository.PublisherRepository;
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
class PublisherControllerTest {

    @Mock
    private PublisherRepository publisherRepository;

    @InjectMocks
    private PublisherController publisherController;

    @Test
    void listAll_returnsAllPublishers() {
        Publisher publisher = new Publisher("Prentice Hall", "US", "www.ph.com");
        when(publisherRepository.findAll()).thenReturn(List.of(publisher));

        List<Publisher> result = publisherController.listAll();

        assertThat(result).containsExactly(publisher);
    }

    @Test
    void getById_returnsOk_whenFound() {
        Publisher publisher = new Publisher("Prentice Hall", "US", "www.ph.com");
        publisher.setId(1L);
        when(publisherRepository.findById(1L)).thenReturn(Optional.of(publisher));

        ResponseEntity<Publisher> response = publisherController.getById(1L);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody()).isEqualTo(publisher);
    }

    @Test
    void getById_returnsNotFound_whenNotFound() {
        when(publisherRepository.findById(99L)).thenReturn(Optional.empty());

        ResponseEntity<Publisher> response = publisherController.getById(99L);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
    }

    @Test
    void create_returnsCreated() {
        Publisher saved = new Publisher("O'Reilly", "US", "www.oreilly.com");
        saved.setId(2L);
        when(publisherRepository.save(any(Publisher.class))).thenReturn(saved);

        PublisherController.PublisherRequest request =
                new PublisherController.PublisherRequest("O'Reilly", "US", "www.oreilly.com");

        ResponseEntity<Publisher> response = publisherController.create(request);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getBody()).isEqualTo(saved);
    }
}
