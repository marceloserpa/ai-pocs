package com.marceloserpa.aipocs.bookstore.controller;

import com.marceloserpa.aipocs.bookstore.model.Book;
import com.marceloserpa.aipocs.bookstore.model.BookOrder;
import com.marceloserpa.aipocs.bookstore.model.Customer;
import com.marceloserpa.aipocs.bookstore.repository.BookOrderRepository;
import com.marceloserpa.aipocs.bookstore.repository.BookRepository;
import com.marceloserpa.aipocs.bookstore.repository.CustomerRepository;
import org.junit.jupiter.api.BeforeEach;
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
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class OrderControllerTest {

    @Mock
    private BookOrderRepository orderRepository;

    @Mock
    private CustomerRepository customerRepository;

    @Mock
    private BookRepository bookRepository;

    @InjectMocks
    private OrderController orderController;

    private Customer customer;
    private Book book;
    private BookOrder order;

    @BeforeEach
    void setUp() {
        customer = new Customer("John", "Doe", "john@example.com", "555-0100");
        customer.setId(1L);

        book = new Book();
        book.setId(1L);
        book.setTitle("Clean Code");
        book.setPrice(new BigDecimal("45.99"));

        order = new BookOrder();
        order.setId(1L);
        order.setCustomer(customer);
        order.setBook(book);
        order.setQuantity(2);
    }

    @Test
    void listAll_returnsAllOrders() {
        when(orderRepository.findAll()).thenReturn(List.of(order));

        List<BookOrder> result = orderController.listAll();

        assertThat(result).containsExactly(order);
    }

    @Test
    void getById_returnsOk_whenFound() {
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));

        ResponseEntity<BookOrder> response = orderController.getById(1L);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody()).isEqualTo(order);
    }

    @Test
    void getById_returnsNotFound_whenNotFound() {
        when(orderRepository.findById(99L)).thenReturn(Optional.empty());

        ResponseEntity<BookOrder> response = orderController.getById(99L);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
    }

    @Test
    void listByCustomer_returnsOrdersForCustomer() {
        when(orderRepository.findByCustomerId(1L)).thenReturn(List.of(order));

        List<BookOrder> result = orderController.listByCustomer(1L);

        assertThat(result).containsExactly(order);
    }

    @Test
    void create_returnsCreated_whenValidRequest() {
        when(customerRepository.findById(1L)).thenReturn(Optional.of(customer));
        when(bookRepository.findById(1L)).thenReturn(Optional.of(book));
        when(orderRepository.save(any(BookOrder.class))).thenReturn(order);

        OrderController.OrderRequest request = new OrderController.OrderRequest(1L, 1L, 2);

        ResponseEntity<?> response = orderController.create(request);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
    }

    @Test
    void create_setsQuantityOne_whenQuantityNull() {
        when(customerRepository.findById(1L)).thenReturn(Optional.of(customer));
        when(bookRepository.findById(1L)).thenReturn(Optional.of(book));
        when(orderRepository.save(any(BookOrder.class))).thenReturn(order);

        OrderController.OrderRequest request = new OrderController.OrderRequest(1L, 1L, null);

        ResponseEntity<?> response = orderController.create(request);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
    }

    @Test
    void create_throwsNoSuchElementException_whenCustomerNotFound() {
        when(customerRepository.findById(99L)).thenReturn(Optional.empty());

        OrderController.OrderRequest request = new OrderController.OrderRequest(99L, 1L, 1);

        assertThatThrownBy(() -> orderController.create(request))
                .isInstanceOf(NoSuchElementException.class)
                .hasMessageContaining("99");
    }

    @Test
    void create_throwsNoSuchElementException_whenBookNotFound() {
        when(customerRepository.findById(1L)).thenReturn(Optional.of(customer));
        when(bookRepository.findById(99L)).thenReturn(Optional.empty());

        OrderController.OrderRequest request = new OrderController.OrderRequest(1L, 99L, 1);

        assertThatThrownBy(() -> orderController.create(request))
                .isInstanceOf(NoSuchElementException.class)
                .hasMessageContaining("99");
    }

    @Test
    void updateStatus_returnsOk_whenOrderFound() {
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        when(orderRepository.save(order)).thenReturn(order);

        OrderController.StatusRequest request = new OrderController.StatusRequest("SHIPPED");

        ResponseEntity<BookOrder> response = orderController.updateStatus(1L, request);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(order.getStatus()).isEqualTo("SHIPPED");
    }

    @Test
    void updateStatus_returnsNotFound_whenOrderNotFound() {
        when(orderRepository.findById(99L)).thenReturn(Optional.empty());

        OrderController.StatusRequest request = new OrderController.StatusRequest("SHIPPED");

        ResponseEntity<BookOrder> response = orderController.updateStatus(99L, request);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
    }
}
