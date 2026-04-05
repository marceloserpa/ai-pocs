package com.marceloserpa.aipocs.bookstore.repository;

import com.marceloserpa.aipocs.bookstore.model.BookOrder;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface BookOrderRepository extends JpaRepository<BookOrder, Long> {

    List<BookOrder> findByCustomerId(Long customerId);
}
