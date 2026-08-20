package com.example.calendar.service;

import com.example.calendar.domain.CalendarUser;

public interface UserContext {
    CalendarUser getCurrentUser();
    void setCurrentUser(CalendarUser user);
}
