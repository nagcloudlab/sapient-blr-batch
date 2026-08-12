package com.example;

import java.util.List;
import java.util.function.Predicate;

import com.example.lib.NumberLib;
import com.example.model.Apple;

/*

    style of programming
    --------------------
    1. Imperative programming => solve the problem by giving a sequence of statements to the computer
        => intention & implementation are mixed together
    2. Declarative programming => solve the problem by giving a description of the solution
        => intention & implementation are separated
        
        How?
        -> by parameters ( value | object | function | behavior )

*/

public class Why_We_Need_Lambda {

    public static void main(String[] args) {
       
        //----------------------------------------------
       
        List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        List<Integer> oddNumbers = NumberLib.filterNumbers(numbers, inp-> inp % 2 != 0);
        System.out.println("Odd Numbers: " + oddNumbers);
        List<Integer> evenNumbers = NumberLib.filterNumbers(numbers, inp-> inp % 2 == 0);
        System.out.println("Even Numbers: " + evenNumbers);
        List<Integer> greaterThanFive = NumberLib.filterNumbers(numbers, inp-> inp > 5);
        System.out.println("Greater than 5: " + greaterThanFive);

        //----------------------------------------------





    }
    

}


