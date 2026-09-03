package com.foodexpress.io;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

/**
 * FoodExpress ReportWriter - generates daily order summary reports.
 * FIXED: readLine() result is null-checked before use.
 */
public class ReportWriter {

    /**
     * Reads an order log file and generates a summary report.
     */
    public void generateReport(String inputPath, String outputPath) throws IOException {
        try (BufferedReader reader = new BufferedReader(new FileReader(inputPath));
             PrintWriter writer = new PrintWriter(new FileWriter(outputPath))) {

            writer.println("=== FoodExpress Daily Report ===");
            writer.println();

            int orderCount = 0;
            double totalRevenue = 0.0;

            // FIX #1: Null-check the readLine() result before using it
            String line = reader.readLine();
            if (line != null) {
                String[] header = line.split(",");
                writer.println("Report header: " + header[0]);
            } else {
                writer.println("Warning: Empty input file");
            }

            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length >= 3) {
                    orderCount++;
                    totalRevenue += Double.parseDouble(parts[2].trim());
                }
            }

            writer.println("Total Orders: " + orderCount);
            writer.println("Total Revenue: $" + String.format("%.2f", totalRevenue));
            writer.println("=== End Report ===");
        }
    }
}
