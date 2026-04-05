package com.marceloserpa.aipocs.bookstore.model;

import jakarta.persistence.*;

@Entity
@Table(name = "publisher")
public class Publisher {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name", nullable = false, length = 200)
    private String name;

    @Column(name = "country", length = 100)
    private String country;

    @Column(name = "website", length = 255)
    private String website;

    public Publisher() {}

    public Publisher(String name, String country, String website) {
        this.name = name;
        this.country = country;
        this.website = website;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getCountry() { return country; }
    public void setCountry(String country) { this.country = country; }

    public String getWebsite() { return website; }
    public void setWebsite(String website) { this.website = website; }
}
