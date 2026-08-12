package com.example;

import java.util.Scanner;

public class Example1 {
    public static void main(String[] args) {

        String mainThreadName = Thread.currentThread().getName();

        Runnable ioTask = ()-> io(); // Job card ( Runnable) for I/O operation
        Thread ioThread = new Thread(ioTask); // Thread for I/O operation
        ioThread.start(); // Start the I/O thread

        Runnable computationTask = ()-> computation(); // Job card ( Runnable) for CPU-intensive operation
        Thread computationThread = new Thread(computationTask); // Thread for CPU-intensive operation
        computationThread.start(); // Start the CPU-intensive thread
        
        System.out.println("Main thread: " + mainThreadName + " is doing other work while I/O and computation are running.");

        
    }

    private static void io() {
        String threadName = Thread.currentThread().getName();
        System.out.println("I/O operation running in thread: " + threadName);
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter your name: ");
        String name = scanner.nextLine();
        System.out.println("Hello, " + name + "!");
        scanner.close();
    }
    private static void computation() {
        // Simulate CPU-intensive operation
        String threadName = Thread.currentThread().getName();
        System.out.println("Computation running in thread: " + threadName);
        long sum = 0;
        for (int i = 0; i < 1_000_000; i++) {
            sum += i;
        }
        System.out.println("Computation result: " + sum + " (computed in thread: " + threadName + ")");
    }
}