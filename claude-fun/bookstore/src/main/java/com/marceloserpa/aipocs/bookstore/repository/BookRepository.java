package com.marceloserpa.aipocs.bookstore.repository;

import com.marceloserpa.aipocs.bookstore.model.Book;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface BookRepository extends JpaRepository<Book, Long> {

    List<Book> findByAuthorId(Long authorId);

    List<Book> findByPublisherId(Long publisherId);

    boolean existsByIsbn(String isbn);
}
