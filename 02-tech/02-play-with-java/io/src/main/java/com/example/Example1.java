package com.example;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Scanner;

public class Example1 {
    

    public static void main(String[] args) {
        
        // try{
        //     InputStreamReader isr=new InputStreamReader(System.in);
        //     BufferedReader br=new BufferedReader(isr);
        //     String line=null;
        //     while((line=br.readLine())!=null){
        //         System.out.println(line);
        //     }
        // }catch(IOException e){
        //     System.out.println("Exception Occurred while reading input");
        // }


        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter a line of text:");
        String line = scanner.nextLine();
        System.out.println("You entered: " + line);

        scanner.close();
    }

}
