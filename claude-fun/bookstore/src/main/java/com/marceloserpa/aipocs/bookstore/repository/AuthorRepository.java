package com.marceloserpa.aipocs.bookstore.repository;

import com.marceloserpa.aipocs.bookstore.model.Author;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AuthorRepository extends JpaRepository<Author, Long> {}
