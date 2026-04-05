package com.marceloserpa.aipocs.bookstore.repository;

import com.marceloserpa.aipocs.bookstore.model.Customer;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CustomerRepository extends JpaRepository<Customer, Long> {}
