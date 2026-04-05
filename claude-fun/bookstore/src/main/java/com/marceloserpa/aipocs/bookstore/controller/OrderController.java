package com.marceloserpa.aipocs.bookstore.controller;

import com.marceloserpa.aipocs.bookstore.model.Book;
import com.marceloserpa.aipocs.bookstore.model.BookOrder;
import com.marceloserpa.aipocs.bookstore.model.Customer;
import com.marceloserpa.aipocs.bookstore.repository.BookOrderRepository;
import com.marceloserpa.aipocs.bookstore.repository.BookRepository;
import com.marceloserpa.aipocs.bookstore.repository.CustomerRepository;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.NoSuchElementException;

@RestController
@RequestMapping("/api/orders")
public class OrderController {

    private final BookOrderRepository orderRepository;
    private final CustomerRepository customerRepository;
    private final BookRepository bookRepository;

    public OrderController(BookOrderRepository orderRepository,
                           CustomerRepository customerRepository,
                           BookRepository bookRepository) {
        this.orderRepository = orderRepository;
        this.customerRepository = customerRepository;
        this.bookRepository = bookRepository;
    }

    @GetMapping
    public List<BookOrder> listAll() {
        return orderRepository.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<BookOrder> getById(@PathVariable Long id) {
        return orderRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/customer/{customerId}")
    public List<BookOrder> listByCustomer(@PathVariable Long customerId) {
        return orderRepository.findByCustomerId(customerId);
    }

    @PostMapping
    public ResponseEntity<?> create(@RequestBody OrderRequest request) {
        Customer customer = customerRepository.findById(request.customerId())
                .orElseThrow(() -> new NoSuchElementException("Customer not found: " + request.customerId()));
        Book book = bookRepository.findById(request.bookId())
                .orElseThrow(() -> new NoSuchElementException("Book not found: " + request.bookId()));

        BookOrder order = new BookOrder();
        order.setCustomer(customer);
        order.setBook(book);
        order.setQuantity(request.quantity() != null ? request.quantity() : 1);
        order.setUnitPrice(book.getPrice());

        return ResponseEntity.status(HttpStatus.CREATED).body(orderRepository.save(order));
    }

    @PatchMapping("/{id}/status")
    public ResponseEntity<BookOrder> updateStatus(@PathVariable Long id, @RequestBody StatusRequest request) {
        return orderRepository.findById(id).map(order -> {
            order.setStatus(request.status());
            return ResponseEntity.ok(orderRepository.save(order));
        }).orElse(ResponseEntity.notFound().build());
    }

    record OrderRequest(Long customerId, Long bookId, Integer quantity) {}
    record StatusRequest(String status) {}
}
