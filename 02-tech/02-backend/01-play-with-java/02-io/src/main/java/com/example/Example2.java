package com.example;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;

public class Example2 {

    public static void main(String[] args) {
        
        try{
            File file = new File("/Users/nag/Downloads/Candidates Details.xlsx");
            // Open Byte Stream to read the file
            FileInputStream fis = new FileInputStream(file);
            byte[] data = new byte[(int) file.length()];
            fis.read(data);
            fis.close();

            // Workbook workbook = org.apache.poi.ss.usermodel.WorkbookFactory.create(fis);
            // Sheet sheet = workbook.getSheetAt(0);

            // for(Row row : sheet){
            //     for(Cell cell : row){
            //         System.out.print(cell + " ");
            //     }
            // }

            // workbook.close();


            FileOutputStream fos = new FileOutputStream("/Users/nag/Downloads/Candidates Details Copy.xlsx");
            fos.write(data);
            fos.close();

        }
        catch(FileNotFoundException e){
            System.out.println(e);
        }
        catch(IOException e){
            System.out.println(e);
        }

    }
    
}
