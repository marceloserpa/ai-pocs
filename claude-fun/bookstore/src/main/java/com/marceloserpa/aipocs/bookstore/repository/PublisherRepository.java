package com.marceloserpa.aipocs.bookstore.repository;

import com.marceloserpa.aipocs.bookstore.model.Publisher;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PublisherRepository extends JpaRepository<Publisher, Long> {}
