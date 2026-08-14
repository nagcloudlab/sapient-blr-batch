package com.quickticket.service;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import com.quickticket.model.Booking;
import com.quickticket.model.Event;
import com.quickticket.repository.BookingRepository;
import com.quickticket.repository.EventRepository;

// =============================================================
// TASK 2b (15 pts): Fix the three unit tests below.
// DEF-205, DEF-206, DEF-207
// =============================================================

@ExtendWith(MockitoExtension.class)
public class BookingServiceTest {

    @Mock
    BookingRepository bookingRepository;

    @InjectMocks
    BookingService bookingService;

    // DEF-205: This test never appears in test reports. The test runner does not execute it.
    public void testCalculateTotal_singleTicket() {
        double price = 50.0;
        int quantity = 1;

        double result = bookingService.calculateTotal(price, quantity);

        assertEquals(50.0, result);
    }

    // DEF-206: This test fails with "expected: <150.0> but was: <150.0>".
    //          The assertion parameters are in the wrong order.
    @Test
    public void testCalculateTotal_multipleTickets() {
        double price = 50.0;
        int quantity = 3;

        double result = bookingService.calculateTotal(price, quantity);

        assertEquals(result, 150.0);
    }

    // DEF-207: This test fails with a database connection error.
    //          Unit tests should use mocking, not a real database.
    @Test
    public void testFindEvent_returnsEvent() {
        try {
            Connection conn = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/quickticket", "root", "password"
            );
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT * FROM events WHERE id = 1");

            assertTrue(rs.next());
            assertEquals("Summer Concert", rs.getString("name"));

            conn.close();
        } catch (Exception e) {
            fail("Database error: " + e.getMessage());
        }
    }
}
