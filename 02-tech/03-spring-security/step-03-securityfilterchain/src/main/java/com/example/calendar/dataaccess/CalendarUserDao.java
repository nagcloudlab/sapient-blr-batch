package com.example.calendar.dataaccess;

import java.util.List;

import com.example.calendar.domain.CalendarUser;

public interface CalendarUserDao {
    CalendarUser getUser(int id);
    CalendarUser findUserByEmail(String email);
    List<CalendarUser> findUsersByEmail(String partialEmail);
    int createUser(CalendarUser user);
}
