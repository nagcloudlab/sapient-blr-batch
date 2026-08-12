package com.foodexpress.io;

import com.foodexpress.model.MenuItem;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * FoodExpress MenuLoader - reads menu items from a CSV file.
 *
 * BUG TO FIX (1 bug):
 * 1. FileReader/BufferedReader not closed — resource leak (no try-with-resources)
 */
public class MenuLoader {

    /**
     * Loads menu items from a CSV file.
     * Format: name,description,price,category
     */
    public List<MenuItem> loadFromFile(String filePath) throws IOException {
        List<MenuItem> items = new ArrayList<>();

        // BUG #1: FileReader not closed — resource leak!
        // Should use try-with-resources to ensure the reader is closed
        FileReader fileReader = new FileReader(filePath);
        BufferedReader reader = new BufferedReader(fileReader);

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

        // Reader is NEVER closed — if an exception occurs above, resources leak
        return items;
    }
}
