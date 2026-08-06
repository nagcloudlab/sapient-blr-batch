package com.example;

import java.util.ArrayList;
import java.util.List;

import com.example.model.Dish;

public class Exercise1 {

    public static void main(String[] args) {
        

        List<Dish> menu = Dish.menu;

        System.out.println(
            getLowCalorieDishNames_v1(menu)
        );
        System.out.println(
            getLowCalorieDishNames_v2(menu)
        );


    }

    private static List<String> getLowCalorieDishNames_v1(List<Dish> menu) {
        // step-1: filter the dishes with calories < 400
        List<Dish> lowCalorieDishes = new ArrayList<>();
        for(Dish dish : menu){
            if(dish.getCalories() < 400){
                lowCalorieDishes.add(dish);
            }
        }
        // step-2: sort the low calorie dishes by calories
        lowCalorieDishes.sort((d1, d2) -> Integer.compare(d1.getCalories(), d2.getCalories()));
        // step-3: extract the names of the low calorie dishes
        List<String> lowCalorieDishNames = new ArrayList<>();
        for(Dish dish : lowCalorieDishes){
            lowCalorieDishNames.add(dish.getName());
        }
        return lowCalorieDishNames;
    }
    

    private static List<String> getLowCalorieDishNames_v2(List<Dish> menu) {
        return menu
            .stream()
            .filter(dish->dish.getCalories()<400)
            .sorted((d1,d2)->Integer.compare(d1.getCalories(), d2.getCalories()))
            .map(d->d.getName())
            .toList();
    }
}
