package com.marceloserpa.aipocs.bookstore.service;

import com.marceloserpa.aipocs.bookstore.model.Author;
import com.marceloserpa.aipocs.bookstore.model.Book;
import com.marceloserpa.aipocs.bookstore.model.Publisher;
import com.marceloserpa.aipocs.bookstore.repository.AuthorRepository;
import com.marceloserpa.aipocs.bookstore.repository.BookRepository;
import com.marceloserpa.aipocs.bookstore.repository.PublisherRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.NoSuchElementException;

@Service
@Transactional
public class BookService {

    private final BookRepository bookRepository;
    private final AuthorRepository authorRepository;
    private final PublisherRepository publisherRepository;

    public BookService(BookRepository bookRepository,
                       AuthorRepository authorRepository,
                       PublisherRepository publisherRepository) {
        this.bookRepository = bookRepository;
        this.authorRepository = authorRepository;
        this.publisherRepository = publisherRepository;
    }

    @Transactional(readOnly = true)
    public List<Book> findAll() {
        return bookRepository.findAll();
    }

    @Transactional(readOnly = true)
    public Book findById(Long id) {
        return bookRepository.findById(id)
                .orElseThrow(() -> new NoSuchElementException("Book not found: " + id));
    }

    public Book create(Book book, Long authorId, Long publisherId) {
        if (authorId != null) {
            Author author = authorRepository.findById(authorId)
                    .orElseThrow(() -> new NoSuchElementException("Author not found: " + authorId));
            book.setAuthor(author);
        }
        if (publisherId != null) {
            Publisher publisher = publisherRepository.findById(publisherId)
                    .orElseThrow(() -> new NoSuchElementException("Publisher not found: " + publisherId));
            book.setPublisher(publisher);
        }
        return bookRepository.save(book);
    }

    public Book update(Long id, Book updated, Long authorId, Long publisherId) {
        Book existing = findById(id);
        existing.setTitle(updated.getTitle());
        existing.setIsbn(updated.getIsbn());
        existing.setPrice(updated.getPrice());
        existing.setStockQuantity(updated.getStockQuantity());
        existing.setPublicationYear(updated.getPublicationYear());

        if (authorId != null) {
            Author author = authorRepository.findById(authorId)
                    .orElseThrow(() -> new NoSuchElementException("Author not found: " + authorId));
            existing.setAuthor(author);
        }
        if (publisherId != null) {
            Publisher publisher = publisherRepository.findById(publisherId)
                    .orElseThrow(() -> new NoSuchElementException("Publisher not found: " + publisherId));
            existing.setPublisher(publisher);
        }
        return bookRepository.save(existing);
    }

    public void delete(Long id) {
        if (!bookRepository.existsById(id)) {
            throw new NoSuchElementException("Book not found: " + id);
        }
        bookRepository.deleteById(id);
    }
}
