package com.example.calendar.dataaccess;

import java.util.List;

import com.example.calendar.domain.Event;

public interface EventDao {
    Event getEvent(int eventId);
    int createEvent(Event event);
    List<Event> findForUser(int userId);
    List<Event> getEvents();
}
