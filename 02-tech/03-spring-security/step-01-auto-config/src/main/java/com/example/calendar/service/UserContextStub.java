package com.example.calendar.service;

import com.example.calendar.dataaccess.CalendarUserDao;
import com.example.calendar.domain.CalendarUser;

import org.springframework.stereotype.Component;

/**
 * INSECURE: Always returns user1@example.com as the "current user".
 * No authentication is performed. This will be replaced by Spring Security.
 */
@Component
public class UserContextStub implements UserContext {

    private final CalendarUserDao userDao;
    private int currentUserId = 0;

    public UserContextStub(CalendarUserDao userDao) {
        this.userDao = userDao;
    }

    @Override
    public CalendarUser getCurrentUser() {
        return userDao.getUser(currentUserId);
    }

    @Override
    public void setCurrentUser(CalendarUser user) {
        if (user == null) {
            throw new IllegalArgumentException("user cannot be null");
        }
        this.currentUserId = user.getId();
    }
}
