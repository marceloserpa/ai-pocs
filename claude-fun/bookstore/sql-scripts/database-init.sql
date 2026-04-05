CREATE TABLE IF NOT EXISTS author (
    id          BIGSERIAL PRIMARY KEY,
    first_name  VARCHAR(100) NOT NULL,
    last_name   VARCHAR(100) NOT NULL,
    biography   TEXT
);

CREATE TABLE IF NOT EXISTS publisher (
    id       BIGSERIAL PRIMARY KEY,
    name     VARCHAR(200) NOT NULL,
    country  VARCHAR(100),
    website  VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS book (
    id               BIGSERIAL PRIMARY KEY,
    title            VARCHAR(300) NOT NULL,
    isbn             VARCHAR(20)  NOT NULL UNIQUE,
    price            NUMERIC(10, 2) NOT NULL,
    stock_quantity   INT NOT NULL DEFAULT 0,
    publication_year INT,
    author_id        BIGINT REFERENCES author(id),
    publisher_id     BIGINT REFERENCES publisher(id)
);

CREATE TABLE IF NOT EXISTS customer (
    id         BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name  VARCHAR(100) NOT NULL,
    email      VARCHAR(255) NOT NULL UNIQUE,
    phone      VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS book_order (
    id          BIGSERIAL PRIMARY KEY,
    customer_id BIGINT REFERENCES customer(id) NOT NULL,
    book_id     BIGINT REFERENCES book(id) NOT NULL,
    quantity    INT NOT NULL DEFAULT 1,
    unit_price  NUMERIC(10, 2) NOT NULL,
    order_date  TIMESTAMP NOT NULL DEFAULT NOW(),
    status      VARCHAR(50) NOT NULL DEFAULT 'PENDING'
);
