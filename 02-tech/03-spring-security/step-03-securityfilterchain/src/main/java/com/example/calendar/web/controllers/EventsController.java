package com.example.calendar.web.controllers;

import java.util.Calendar;

import com.example.calendar.domain.CalendarUser;
import com.example.calendar.domain.Event;
import com.example.calendar.service.CalendarService;
import com.example.calendar.service.UserContext;
import com.example.calendar.web.model.CreateEventForm;
import jakarta.validation.Valid;

import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/events")
public class EventsController {

    private final CalendarService calendarService;
    private final UserContext userContext;

    public EventsController(CalendarService calendarService, UserContext userContext) {
        this.calendarService = calendarService;
        this.userContext = userContext;
    }

    @GetMapping("/")
    public ModelAndView events() {
        return new ModelAndView("events/list", "events", calendarService.getEvents());
    }

    @GetMapping("/my")
    public ModelAndView myEvents() {
        CalendarUser currentUser = userContext.getCurrentUser();
        ModelAndView result = new ModelAndView("events/my", "events",
                calendarService.findForUser(currentUser.getId()));
        result.addObject("currentUser", currentUser);
        return result;
    }

    @GetMapping("/{eventId}")
    public ModelAndView show(@PathVariable int eventId) {
        return new ModelAndView("events/show", "event", calendarService.getEvent(eventId));
    }

    @GetMapping("/form")
    public String createEventForm(@ModelAttribute CreateEventForm createEventForm) {
        return "events/create";
    }

    @PostMapping(value = "/new", params = "auto")
    public String autoPopulate(@ModelAttribute CreateEventForm createEventForm) {
        createEventForm.setSummary("A new event....");
        createEventForm.setDescription("This was autopopulated to save time.");
        createEventForm.setWhen(Calendar.getInstance());

        CalendarUser currentUser = userContext.getCurrentUser();
        int attendeeId = currentUser.getId() == 0 ? 1 : 0;
        CalendarUser attendee = calendarService.getUser(attendeeId);
        createEventForm.setAttendeeEmail(attendee.getEmail());

        return "events/create";
    }

    @PostMapping("/new")
    public String createEvent(@Valid CreateEventForm createEventForm,
                              BindingResult result,
                              RedirectAttributes redirectAttributes) {
        if (result.hasErrors()) {
            return "events/create";
        }
        CalendarUser attendee = calendarService.findUserByEmail(createEventForm.getAttendeeEmail());
        if (attendee == null) {
            result.rejectValue("attendeeEmail", "attendeeEmail.missing",
                    "Could not find a user for the provided Attendee Email");
        }
        if (result.hasErrors()) {
            return "events/create";
        }
        Event event = new Event(null, createEventForm.getSummary(),
                createEventForm.getDescription(), createEventForm.getWhen(),
                userContext.getCurrentUser(), attendee);
        calendarService.createEvent(event);
        redirectAttributes.addFlashAttribute("message", "Successfully added the new event");
        return "redirect:/events/my";
    }
}
