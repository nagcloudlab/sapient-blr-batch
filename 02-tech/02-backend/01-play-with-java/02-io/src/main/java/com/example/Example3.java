package com.example;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class Example3 {

    public static void main(String[] args) {
        try {
            FileReader fr = new FileReader("/Users/nag/sapient-blr-batch/02-tech/02-play-with-java/io/menu.txt");
            FileWriter fw = new FileWriter("/Users/nag/sapient-blr-batch/02-tech/02-play-with-java/io/menu_copy.txt");
            BufferedReader br = new BufferedReader(fr);
            String line;
            while ((line = br.readLine()) != null) {
                fw.write(line.toUpperCase() + "\n");
            }
            br.close(); 
            fr.close();
            fw.flush();
            fw.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    
}
