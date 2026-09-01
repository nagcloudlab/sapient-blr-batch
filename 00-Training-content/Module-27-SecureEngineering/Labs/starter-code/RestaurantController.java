package com.foodexpress.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;

import java.security.MessageDigest;
import java.util.List;

@RestController
@RequestMapping("/api/v1/restaurants")
public class RestaurantController {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    // BUG: Hardcoded API key -- should be in environment variable
    private static final String MAPS_API_KEY = "AIzaSyB1-xG0K3mR7vNdF5kJ8QwZhLm9pA2bC4d";

    /**
     * Search restaurants by name
     * BUG: SQL Injection vulnerability -- string concatenation in SQL
     */
    @GetMapping("/search")
    public List<Restaurant> searchRestaurants(@RequestParam String name) {
        // BUG: Direct string concatenation allows SQL injection
        String sql = "SELECT * FROM restaurants WHERE name LIKE '%" + name + "%'";
        return jdbcTemplate.query(sql, (rs, rowNum) -> {
            Restaurant r = new Restaurant();
            r.setId(rs.getLong("id"));
            r.setName(rs.getString("name"));
            r.setCuisine(rs.getString("cuisine"));
            r.setRating(rs.getDouble("rating"));
            return r;
        });
    }

    /**
     * Get restaurant reviews
     * BUG: XSS vulnerability -- review comment rendered without escaping
     */
    @GetMapping("/{id}/reviews")
    public String getReviewsHtml(@PathVariable Long id) {
        List<Review> reviews = getReviews(id);
        StringBuilder html = new StringBuilder();
        for (Review review : reviews) {
            // BUG: User input (review.getComment()) inserted directly into HTML
            html.append("<div class='review'><p>")
                .append(review.getComment())  // XSS: unescaped user input
                .append("</p><span>Rating: ")
                .append(review.getRating())
                .append("</span></div>");
        }
        return html.toString();
    }

    /**
     * Register new restaurant partner
     * BUG: Weak password hashing -- uses MD5
     */
    public String hashPassword(String password) {
        try {
            // BUG: MD5 is cryptographically broken -- use bcrypt
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] digest = md.digest(password.getBytes());
            StringBuilder sb = new StringBuilder();
            for (byte b : digest) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString();
        } catch (Exception e) {
            throw new RuntimeException("Hashing failed", e);
        }
    }

    // Helper methods (simplified)
    private List<Review> getReviews(Long restaurantId) {
        return List.of(); // Placeholder
    }
}
