package com.foodexpress.repository;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * FoodExpress OrderRepository - JDBC data access layer.
 *
 * BUGS TO FIX (2 bugs):
 * 1. JDBC Connection leak — connection not closed in finally block
 * 2. SQL injection — uses string concatenation instead of PreparedStatement
 */
public class OrderRepository {

    private static final String DB_URL = "jdbc:mysql://localhost:3306/foodexpress";
    private static final String DB_USER = "root";
    private static final String DB_PASS = "password";

    /**
     * Finds an order by customer name.
     * BUG #1: Connection is never closed — resource leak
     * BUG #2: SQL injection vulnerability — string concatenation
     */
    public String findOrderByCustomer(String customerName) {
        Connection conn = null;
        String result = null;

        try {
            conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASS);

            // BUG #2: SQL injection! User input directly concatenated into query
            String sql = "SELECT * FROM orders WHERE customer_name = '" + customerName + "'";
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery(sql);

            if (rs.next()) {
                result = rs.getString("order_id") + ": " + rs.getString("customer_name");
            }

        } catch (SQLException e) {
            System.err.println("Database error: " + e.getMessage());
        }
        // BUG #1: Connection is NEVER closed!
        // No finally block to ensure conn.close() is called

        return result;
    }

    /**
     * Inserts a new order. Also has SQL injection vulnerability.
     */
    public void insertOrder(String orderId, String customerName, double total) {
        Connection conn = null;
        try {
            conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASS);

            // BUG #2: SQL injection again
            String sql = "INSERT INTO orders (order_id, customer_name, total) VALUES ('"
                    + orderId + "', '" + customerName + "', " + total + ")";
            Statement stmt = conn.createStatement();
            stmt.executeUpdate(sql);
            System.out.println("Order inserted: " + orderId);

        } catch (SQLException e) {
            System.err.println("Insert failed: " + e.getMessage());
        }
        // BUG #1: Connection leak again — no finally/try-with-resources
    }
}
