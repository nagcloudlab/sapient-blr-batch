package com.example.calendar.service;

import java.util.List;

import com.example.calendar.dataaccess.CalendarUserDao;
import com.example.calendar.dataaccess.EventDao;
import com.example.calendar.domain.CalendarUser;
import com.example.calendar.domain.Event;

import org.springframework.stereotype.Service;

@Service
public class DefaultCalendarService implements CalendarService {

    private final EventDao eventDao;
    private final CalendarUserDao userDao;

    public DefaultCalendarService(EventDao eventDao, CalendarUserDao userDao) {
        this.eventDao = eventDao;
        this.userDao = userDao;
    }

    @Override public CalendarUser getUser(int id) { return userDao.getUser(id); }
    @Override public CalendarUser findUserByEmail(String email) { return userDao.findUserByEmail(email); }
    @Override public List<CalendarUser> findUsersByEmail(String partialEmail) { return userDao.findUsersByEmail(partialEmail); }
    @Override public int createUser(CalendarUser user) { return userDao.createUser(user); }

    @Override public Event getEvent(int eventId) { return eventDao.getEvent(eventId); }
    @Override public int createEvent(Event event) { return eventDao.createEvent(event); }
    @Override public List<Event> findForUser(int userId) { return eventDao.findForUser(userId); }
    @Override public List<Event> getEvents() { return eventDao.getEvents(); }
}
