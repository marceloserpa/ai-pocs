---
name: integration-test-generate
description: Generate integration tests using Testcontainers and Spring Boot Test. Asks how many tests to create and distributes them across controllers. Use when asked to generate, write, or create integration tests.
allowed-tools: AskUserQuestion, Bash, Read, Write, Edit, Glob, Grep
---

Generate Testcontainers-based integration tests for this Spring Boot project.

## Steps

### 1. Ask the user for input

Use the `AskUserQuestion` tool to collect:

- **How many integration tests** to generate (options: 3, 5, 10, or "Other" for a custom number)
- **Which scope** to cover (options: "All controllers", "Books only", "Orders only", "Other")

### 2. Inspect the current state

Run the following checks in parallel:

- Read `build.gradle` to check if Testcontainers dependencies are already present:
  - `org.springframework.boot:spring-boot-testcontainers`
  - `org.testcontainers:junit-jupiter`
  - `org.testcontainers:postgresql`
- Glob for `**/AbstractIntegrationTest.java` under `src/test/` to check if the base class exists
- Glob for `**/*IT.java` under `src/test/` to discover already existing integration tests
- Glob for all controller files under `src/main/java/**/controller/` to understand available endpoints

### 3. Add Testcontainers dependencies (if missing)

If any of the three Testcontainers dependencies are absent from `build.gradle`, add them inside the `dependencies` block using the Edit tool:

```groovy
testImplementation 'org.springframework.boot:spring-boot-testcontainers'
testImplementation 'org.testcontainers:junit-jupiter'
testImplementation 'org.testcontainers:postgresql'
```

No version needed — Spring Boot manages Testcontainers versions via its BOM.

### 4. Create the base class (if missing)

If `AbstractIntegrationTest.java` does not exist, create it at:
`src/test/java/com/marceloserpa/aipocs/bookstore/AbstractIntegrationTest.java`

```java
package com.marceloserpa.aipocs.bookstore;

import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureMockMvc
@Testcontainers
public abstract class AbstractIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:14.2")
            .withDatabaseName("outbox-poc")
            .withUsername("postgres")
            .withPassword("postgres");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
}
```

### 5. Read controllers in scope

For each controller that falls within the chosen scope:
- Read the controller source file
- Identify all endpoint methods: HTTP method, path, request body type, response type
- Read the corresponding repository interface if the controller calls it directly
- Note any existing `*IT.java` file for that controller to avoid duplicating tests

### 6. Plan the test distribution

Distribute the requested number of tests across the controllers in scope, prioritising:
1. Happy-path POST/create (always include — exercises the full write stack)
2. Happy-path GET by ID
3. GET all / list
4. 404 not-found cases
5. Validation / bad-input cases (if endpoints validate input)
6. Status transitions (e.g., PATCH order status)

Do not create trivial duplicates. Each test must exercise a distinct scenario.

### 7. Write the test conventions

Match this project's integration test style exactly:
- Extend `AbstractIntegrationTest`
- Inject `MockMvc` and `ObjectMapper` via `@Autowired`
- Inject the relevant repository to seed or clean test data
- Use `@BeforeEach` to call `repository.deleteAll()` so tests are isolated
- Use MockMvc fluent API: `mockMvc.perform(...).andExpect(...)`
- Use `jsonPath` assertions for response body fields
- Test class named `<Entity>ControllerIT` in package `com.marceloserpa.aipocs.bookstore.controller`
- Test method naming: `methodName_expectedBehavior_whenCondition`
- No Mockito mocks — this is a full-stack test hitting a real database

Example test shape:
```java
@Test
void createBook_shouldReturnCreated_whenRequestIsValid() throws Exception {
    var payload = Map.of("title", "Clean Code", "isbn", "978-0132350884", "price", 29.99, "stockQuantity", 10);

    mockMvc.perform(post("/api/books")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(objectMapper.writeValueAsString(payload)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.title").value("Clean Code"));
}
```

### 8. Write the test files

For each controller in scope:
- If an `*IT.java` file already exists for it: add the new `@Test` methods using the Edit tool
- If no `*IT.java` file exists: create it using the Write tool

Spread the total requested test count across all controllers in scope as evenly as possible.

### 9. Verify

Run `./gradlew test --tests "**/*IT"` to execute only the integration tests.
If any test fails, read the error output, fix the test, and re-run before reporting.

### 10. Report

After all tests pass, present a summary table:

| File | Tests added | Scenarios covered |
|------|-------------|-------------------|
| BookControllerIT.java | 3 | create, getById, notFound |
| ... | ... | ... |

Then one short paragraph on any scenarios that were skipped and why (e.g., endpoint requires auth not yet configured, no DELETE endpoint exists).
