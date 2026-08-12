package com.example;

public class Example2 {

    public static void main(String[] args) {
        
        Runnable task = () -> {
            for (int i = 0; i < 1000; i++) {
               
                System.out.println("Task is running: " + i);
                try {
                    Thread.sleep(1000); // Sleep for 1 second
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    System.out.println("Task was interrupted");
                }

                if (Thread.currentThread().isInterrupted()) {
                    System.out.println("Task is stopping due to interruption");
                    if(i>10){
                        break; // Exit the loop if interrupted and i > 10
                    }
                }
            }
        };
        Thread thread = new Thread(task);
        thread.start();

        
        try {
            Thread.sleep(5000); // Main thread sleeps for 5 seconds
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        thread.stop(); // Stop the thread after 5 seconds (not recommended in practice)

    }
}
