package com.example.calendar.domain;

import java.util.Calendar;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;

public record Event(
        Integer id,
        @NotEmpty(message = "Summary is required") String summary,
        @NotEmpty(message = "Description is required") String description,
        @NotNull(message = "When is required") Calendar dateWhen,
        @NotNull(message = "Owner is required") CalendarUser owner,
        CalendarUser attendee
) {}
