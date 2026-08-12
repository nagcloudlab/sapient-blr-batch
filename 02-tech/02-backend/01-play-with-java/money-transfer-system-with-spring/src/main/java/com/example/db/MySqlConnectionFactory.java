package com.example.db;

import com.mysql.cj.jdbc.AbandonedConnectionCleanupThread;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Driver;
import java.sql.SQLException;
import java.util.Enumeration;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MySqlConnectionFactory {
    private static final Logger logger = LoggerFactory.getLogger(MySqlConnectionFactory.class);

    public static Connection getConnection() {
        logger.info("Attempting to establish database connection");
        try {
            Connection connection = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/money_transfer_system_db",
                "root",
                "yourpassword"
            );
            logger.info("Database connection established successfully");
            return connection;
        } catch (SQLException e) {
            logger.error("Failed to establish database connection", e);
            throw new RuntimeException("Failed to connect to the database", e);
        }
    }

    public static void shutdown() {
        logger.info("Running JDBC shutdown cleanup");

        try {
            AbandonedConnectionCleanupThread.checkedShutdown();
            logger.info("MySQL abandoned connection cleanup thread shut down");
        } catch (Exception e) {
            logger.warn("Failed to shut down MySQL cleanup thread cleanly", e);
        }

        Enumeration<Driver> drivers = DriverManager.getDrivers();
        while (drivers.hasMoreElements()) {
            Driver driver = drivers.nextElement();
            try {
                DriverManager.deregisterDriver(driver);
                logger.info("Deregistered JDBC driver: {}", driver.getClass().getName());
            } catch (SQLException e) {
                logger.warn("Failed to deregister JDBC driver: {}", driver.getClass().getName(), e);
            }
        }
    }
    
}
