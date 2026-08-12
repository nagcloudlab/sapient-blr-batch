package com.example;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Example5 {

    public static void main(String[] args) {
        
        ExecutorService executorService = Executors.newFixedThreadPool(2);

        while(true){
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            Runnable task = new Runnable() {
                @Override
                public void run() {
                    System.out.println("Thread name: " + Thread.currentThread().getName()+" started the task");
                    try {
                        Thread.sleep(2000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    System.out.println("Thread name: " + Thread.currentThread().getName()+" finished the task");
                }
            };
            executorService.submit(task);

            //executorService.shutdown(); // Uncomment this line to stop the executor service after submitting tasks
        }

    }
    
}
