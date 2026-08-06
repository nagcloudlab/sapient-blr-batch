package com.example;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

import com.example.model.Car;
import com.example.model.Owner;

public class MapExample {

    public static void main(String[] args) {
        

        Owner owner1 = new Owner("Riya");
        Owner owner2 = new Owner("Diya");

        Car car1 = new Car("Toyota", "Camry");
        Car car2 = new Car("Honda", "Civic");

        Map<Owner, Car> ownerCarMap = new HashMap<>();
        ownerCarMap.put(owner1, car1);
        ownerCarMap.put(owner2, car2);


        //-------------------------------------------------------

        Set<Owner> owners = ownerCarMap.keySet();
        for (Owner owner : owners) {
            Car car = ownerCarMap.get(owner);
            System.out.println("Owner: " + owner + ", Car: " + car);
        }
        ownerCarMap.values().forEach(car -> System.out.println("Car: " + car));

        //-------------------------------------------------------
        // Scanner scanner = new Scanner(System.in);
        // System.out.print("Enter the name of the owner: ");
        // String ownerName = scanner.nextLine();
        // Owner searchOwner = new Owner(ownerName);

        // Car car = ownerCarMap.get(searchOwner);
        // if (car != null) {
        //     System.out.println("Car details for owner " + ownerName + ": " + car);
        // } else {
        //     System.out.println("No car found for owner " + ownerName);
        // }
        // scanner.close();
        //-------------------------------------------------------


    }
    
}
