package com.foodexpress.io;

import com.foodexpress.model.MenuItem;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * FoodExpress MenuLoader - reads menu items from a CSV file.
 * FIXED: Uses try-with-resources to prevent resource leaks.
 */
public class MenuLoader {

    /**
     * Loads menu items from a CSV file.
     * Format: name,description,price,category
     */
    public List<MenuItem> loadFromFile(String filePath) throws IOException {
        List<MenuItem> items = new ArrayList<>();

        // FIX #1: try-with-resources ensures reader is always closed
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length == 4) {
                    String name = parts[0].trim();
                    String desc = parts[1].trim();
                    double price = Double.parseDouble(parts[2].trim());
                    String category = parts[3].trim();
                    items.add(new MenuItem(name, desc, price, category));
                }
            }
        }
        // Reader is automatically closed here, even if an exception occurs

        return items;
    }
}
