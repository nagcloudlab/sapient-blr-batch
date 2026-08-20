package com.example.calendar.service;

import java.util.List;

import com.example.calendar.domain.CalendarUser;
import com.example.calendar.domain.Event;

public interface CalendarService {
    CalendarUser getUser(int id);
    CalendarUser findUserByEmail(String email);
    List<CalendarUser> findUsersByEmail(String partialEmail);
    int createUser(CalendarUser user);

    Event getEvent(int eventId);
    int createEvent(Event event);
    List<Event> findForUser(int userId);
    List<Event> getEvents();
}
