package com.quickticket.model;

import java.util.Objects;

/**
 * QuickTicket — Event domain model.
 */
public class Event {

    private Long id;
    private String name;
    private String venue;
    private double price;
    private int availableSeats;

    public Event() {
        // Default constructor required for JSON deserialization
    }

    public Event(Long id, String name, String venue, double price, int availableSeats) {
        this.id = id;
        this.name = name;
        this.venue = venue;
        this.price = price;
        this.availableSeats = availableSeats;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getVenue() {
        return venue;
    }

    public void setVenue(String venue) {
        this.venue = venue;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    public int getAvailableSeats() {
        return availableSeats;
    }

    public void setAvailableSeats(int availableSeats) {
        this.availableSeats = availableSeats;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Event event = (Event) o;
        return id != null && id.equals(event.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public String toString() {
        return "Event{" +
            "name='" + name + '\'' +
            ", venue='" + venue + '\'' +
            ", price=" + price +
            '}';
    }
}
