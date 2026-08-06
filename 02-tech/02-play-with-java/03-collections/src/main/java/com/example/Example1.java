package com.example;

import java.util.Iterator;

import com.example.util.Box;
import com.example.util.LinkedList;

public class Example1 {
    public static void main(String[] args) {
        

        // int v=12;
        // String s="Hello";

        // int[] values = {1, 2, 3, 4, 5};
        // int[] values2 = new int[5];
        // String[] names = {"Alice", "Bob", "Charlie"};
        // String[] names2 = new String[3];

        // limitations of array data-structures
        //-----------------------------------
        // 1. Fixed size: Once an array is created, its size cannot be changed. This can lead to wasted memory if the array is too large or insufficient space if the array is too small.
        // 2. Homogeneous elements: Arrays can only store elements of the same data type
        // 3. Insertion and deletion: Inserting or deleting elements in an array can be inefficient, as it may require shifting elements to maintain the order of the array.
        // 4. Lack of built-in methods: Arrays do not have built-in methods for common operations like searching, sorting, or filtering, which can make it more difficult to work with them compared to other data structures like lists or sets.
        // 5. contiguous memory allocation: Arrays require contiguous memory allocation, which can lead to fragmentation and inefficient use of memory in certain situations.


        // Alternatives to arrays
        //-----------------------------------

        // -> LinkedList

        LinkedList<Integer> list1 = new LinkedList<>();
        list1.add(10); // int -> Integer (autoboxing)
        list1.add(20);
        list1.add(30);

        int valueAtIndex1 = list1.get(1);
        //System.out.println("Value at index 1: " + valueAtIndex1); //

        int valueAtIndex2 = list1.get(2);
        //System.out.println("Value at index 2: " + valueAtIndex2); //

        LinkedList<String> names = new LinkedList<>();
        names.add("Alice");
        names.add("Bob");
        names.add("Charlie");

        //-----------------------------------

        // for(int i=0; i<3; i++){
        //     System.out.println("Name at index " + i + ": " + names.get(i));
        // }

        //-----------------------------------

        Iterator<String> iterator = names.iterator();
        while(iterator.hasNext()){
            String name = iterator.next();
            System.out.println(name);
        }

        //-----------------------------------
        // Java 1.5
        //-----------------------------------

        for(String name : names){
            System.out.println(name);
        }

        //-----------------------------------

        Box box = new Box();
        box.add(10);
        box.add(20);

        for(int v:box){
            System.out.println(v);
        }
        

    }
}
