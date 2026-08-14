package com.quickticket.service;

import com.quickticket.model.Booking;
import com.quickticket.model.Event;
import com.quickticket.repository.BookingRepository;
import com.quickticket.repository.EventRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;

@Service
public class BookingService {

    private final BookingRepository bookingRepository;
    private final EventRepository eventRepository;

    public BookingService(BookingRepository bookingRepository, EventRepository eventRepository) {
        this.bookingRepository = bookingRepository;
        this.eventRepository = eventRepository;
    }

    public double calculateTotal(double price, int quantity) {
        return price * quantity;
    }

    public Event findEvent(Long eventId) {
        return eventRepository.findById(eventId)
                .orElseThrow(() -> new IllegalArgumentException("Event not found with id: " + eventId));
    }

    public Booking createBooking(Booking booking) {
        Event event = findEvent(booking.getEventId());

        BigDecimal total = event.getPrice().multiply(BigDecimal.valueOf(booking.getSeats()));
        booking.setTotalAmount(total);
        booking.setStatus("pending");

        return bookingRepository.save(booking);
    }

    public Booking getBooking(Long id) {
        return bookingRepository.findById(id)
                .orElse(null);
    }

    public void deleteBooking(Long id) {
        if (!bookingRepository.existsById(id)) {
            throw new IllegalArgumentException("Booking not found with id: " + id);
        }
        bookingRepository.deleteById(id);
    }

    public Booking cancelBooking(Long id) {
        Booking booking = bookingRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Booking not found with id: " + id));
        booking.setStatus("cancelled");
        return bookingRepository.save(booking);
    }
}
