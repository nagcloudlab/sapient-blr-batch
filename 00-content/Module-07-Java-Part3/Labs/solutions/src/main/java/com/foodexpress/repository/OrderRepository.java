package com.foodexpress.repository;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * FoodExpress OrderRepository - JDBC data access layer.
 * FIXED: try-with-resources for connection management, PreparedStatement for SQL injection prevention.
 */
public class OrderRepository {

    private static final String DB_URL = "jdbc:mysql://localhost:3306/foodexpress";
    private static final String DB_USER = "root";
    private static final String DB_PASS = "password";

    /**
     * Finds an order by customer name.
     * FIX #1: Connection closed via try-with-resources
     * FIX #2: PreparedStatement prevents SQL injection
     */
    public String findOrderByCustomer(String customerName) {
        String result = null;

        // FIX #1: try-with-resources ensures connection is always closed
        String sql = "SELECT * FROM orders WHERE customer_name = ?";

        try (Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASS);
             // FIX #2: PreparedStatement with parameterized query
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setString(1, customerName);  // Safe parameter binding
            ResultSet rs = pstmt.executeQuery();

            if (rs.next()) {
                result = rs.getString("order_id") + ": " + rs.getString("customer_name");
            }

        } catch (SQLException e) {
            System.err.println("Database error: " + e.getMessage());
        }
        // Connection is automatically closed here

        return result;
    }

    /**
     * Inserts a new order using PreparedStatement.
     */
    public void insertOrder(String orderId, String customerName, double total) {
        // FIX #1 & #2: try-with-resources + PreparedStatement
        String sql = "INSERT INTO orders (order_id, customer_name, total) VALUES (?, ?, ?)";

        try (Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASS);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setString(1, orderId);
            pstmt.setString(2, customerName);
            pstmt.setDouble(3, total);
            pstmt.executeUpdate();
            System.out.println("Order inserted: " + orderId);

        } catch (SQLException e) {
            System.err.println("Insert failed: " + e.getMessage());
        }
    }
}
