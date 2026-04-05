package com.marceloserpa.aipocs.bookstore.controller;

import com.marceloserpa.aipocs.bookstore.model.Publisher;
import com.marceloserpa.aipocs.bookstore.repository.PublisherRepository;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/publishers")
public class PublisherController {

    private final PublisherRepository publisherRepository;

    public PublisherController(PublisherRepository publisherRepository) {
        this.publisherRepository = publisherRepository;
    }

    @GetMapping
    public List<Publisher> listAll() {
        return publisherRepository.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Publisher> getById(@PathVariable Long id) {
        return publisherRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Publisher> create(@RequestBody PublisherRequest request) {
        Publisher publisher = new Publisher(request.name(), request.country(), request.website());
        return ResponseEntity.status(HttpStatus.CREATED).body(publisherRepository.save(publisher));
    }

    record PublisherRequest(String name, String country, String website) {}
}
