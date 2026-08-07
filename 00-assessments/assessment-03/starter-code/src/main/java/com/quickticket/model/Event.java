package com.quickticket.model;

import java.util.Objects;

/**
 * QuickTicket — Event domain model.
 */
public class Event {

    public Long id;
    public String name;
    public String venue;
    public double price;
    public int availableSeats;

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

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Event event = (Event) o;
        return id != null && id.equals(event.id);
    }
}
