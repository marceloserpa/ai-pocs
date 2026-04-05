# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spring Boot 4.0.5 REST API for bookstore management. Java 25, PostgreSQL 14.2, Gradle build system.

## Commands

```bash
# Start PostgreSQL (required before running the app)
docker-compose up -d

# Build
./gradlew build
./gradlew clean build

# Run
./gradlew bootRun

# Test
./gradlew test
./gradlew test --tests "<FullyQualifiedTestClassName>"
```

The app runs on port 8080. The database must be initialized via `sql-scripts/database-init.sql` (Docker Compose does this automatically on first start).

## Architecture

Standard Spring Boot layered architecture:

```
Controllers → Service (BookService only) → Repositories (Spring Data JPA) → PostgreSQL
```

Five domain entities: **Book**, **Author**, **Publisher**, **Customer**, **BookOrder**.

- `BookController` routes through `BookService` for business logic (stock validation, `@Transactional`)
- All other controllers (`AuthorController`, `PublisherController`, `CustomerController`, `OrderController`) call repositories directly
- Request DTOs are Java records (e.g., `BookRequest`, `OrderRequest`)
- `BookOrder` links `Customer` → `Book` with quantity, unit_price, order_date, and status
- All JPA relationships use `FetchType.LAZY`

## Database Configuration

- Host: `localhost:5442`
- Database: `outbox-poc`
- Credentials: `postgres` / `postgres`
- `ddl-auto: validate` — schema must exist before app starts; do not rely on Hibernate to create tables

Docker Compose enables logical WAL replication (`wal_level=logical`), suggesting this project may evolve toward CDC/event sourcing patterns.

## Key Conventions

- `@Transactional(readOnly=true)` on read operations in services
- Controllers return `ResponseEntity` and catch `NoSuchElementException` → 404
- No linting or static analysis tools are currently configured
