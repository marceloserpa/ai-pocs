package com.marceloserpa.aipocs.bookstore.controller;

import com.marceloserpa.aipocs.bookstore.model.Customer;
import com.marceloserpa.aipocs.bookstore.repository.CustomerRepository;
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
class CustomerControllerTest {

    @Mock
    private CustomerRepository customerRepository;

    @InjectMocks
    private CustomerController customerController;

    @Test
    void listAll_returnsAllCustomers() {
        Customer customer = new Customer("John", "Doe", "john@example.com", "555-0100");
        when(customerRepository.findAll()).thenReturn(List.of(customer));

        List<Customer> result = customerController.listAll();

        assertThat(result).containsExactly(customer);
    }

    @Test
    void getById_returnsOk_whenFound() {
        Customer customer = new Customer("John", "Doe", "john@example.com", "555-0100");
        customer.setId(1L);
        when(customerRepository.findById(1L)).thenReturn(Optional.of(customer));

        ResponseEntity<Customer> response = customerController.getById(1L);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody()).isEqualTo(customer);
    }

    @Test
    void getById_returnsNotFound_whenNotFound() {
        when(customerRepository.findById(99L)).thenReturn(Optional.empty());

        ResponseEntity<Customer> response = customerController.getById(99L);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
    }

    @Test
    void create_returnsCreated() {
        Customer saved = new Customer("Jane", "Smith", "jane@example.com", "555-0200");
        saved.setId(2L);
        when(customerRepository.save(any(Customer.class))).thenReturn(saved);

        CustomerController.CustomerRequest request =
                new CustomerController.CustomerRequest("Jane", "Smith", "jane@example.com", "555-0200");

        ResponseEntity<Customer> response = customerController.create(request);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getBody()).isEqualTo(saved);
    }
}
