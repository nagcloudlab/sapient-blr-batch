package com.foodexpress.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.util.HtmlUtils;

import java.util.List;

@RestController
@RequestMapping("/api/v1/restaurants")
public class RestaurantController {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    // FIX: Read API key from environment variable instead of hardcoding
    @Value("${MAPS_API_KEY:not-configured}")
    private String mapsApiKey;

    // FIX: Use BCryptPasswordEncoder for password hashing
    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder(12);

    /**
     * Search restaurants by name
     * FIX: Uses parameterized query to prevent SQL injection
     */
    @GetMapping("/search")
    public List<Restaurant> searchRestaurants(@RequestParam String name) {
        // FIX: Parameterized query -- user input is treated as data, not SQL code
        String sql = "SELECT * FROM restaurants WHERE name LIKE ?";
        String searchTerm = "%" + name + "%";
        return jdbcTemplate.query(sql, (rs, rowNum) -> {
            Restaurant r = new Restaurant();
            r.setId(rs.getLong("id"));
            r.setName(rs.getString("name"));
            r.setCuisine(rs.getString("cuisine"));
            r.setRating(rs.getDouble("rating"));
            return r;
        }, searchTerm);
    }

    /**
     * Get restaurant reviews
     * FIX: HTML-escapes user input to prevent XSS
     */
    @GetMapping("/{id}/reviews")
    public String getReviewsHtml(@PathVariable Long id) {
        List<Review> reviews = getReviews(id);
        StringBuilder html = new StringBuilder();
        for (Review review : reviews) {
            // FIX: HTML-escape user input before rendering
            html.append("<div class='review'><p>")
                .append(HtmlUtils.htmlEscape(review.getComment()))  // FIX: escaped
                .append("</p><span>Rating: ")
                .append(review.getRating())
                .append("</span></div>");
        }
        return html.toString();
    }

    /**
     * Register new restaurant partner
     * FIX: Uses bcrypt for secure password hashing
     */
    public String hashPassword(String password) {
        // FIX: bcrypt with cost factor 12 -- slow by design, includes salt
        return passwordEncoder.encode(password);
    }

    // Helper methods (simplified)
    private List<Review> getReviews(Long restaurantId) {
        return List.of(); // Placeholder
    }
}
