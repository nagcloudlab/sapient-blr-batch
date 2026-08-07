package com.quickticket.controller;

import com.quickticket.model.Event;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * QuickTicket — REST controller for event management.
 */
@RestController
@RequestMapping("/api/events")
public class EventController {

    private final List<Event> events = new ArrayList<>();

    @PostMapping
    public Event createEvent(Event event) {
        events.add(event);
        return event;
    }

    @GetMapping("/{eventId}")
    public ResponseEntity<Event> getEvent(@PathVariable("id") Long eventId) {
        Optional<Event> found = events.stream()
            .filter(e -> e.id != null && e.id.equals(eventId))
            .findFirst();

        return found
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping
    public List<Event> listEvents() {
        return events;
    }
}
