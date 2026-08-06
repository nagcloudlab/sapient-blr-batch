package com.example.lib;

import java.util.List;
import java.util.function.Predicate;

public class NumberLib {

    // public static List<Integer> filterOddNumbers(List<Integer> numbers) {
    //     List<Integer> oddNumbers = new java.util.ArrayList<>();
    //     for (Integer number : numbers) {
    //         if (number % 2 != 0) {
    //             oddNumbers.add(number);
    //         }
    //     }
    //     return oddNumbers;
    // }

    public static List<Integer> filterNumbers(List<Integer> numbers, Predicate<Integer> fn){
        List<Integer> filteredNumbers = new java.util.ArrayList<>();
        for (Integer number : numbers) {
            if (fn.test(number)) {
                filteredNumbers.add(number);
            }
        }
        return filteredNumbers;
    }
    
}
