package com.example.model;

public class Owner implements Comparable<Owner> {
    private String name;

    public Owner(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    @Override
    public int compareTo(Owner other) {
        return this.name.compareTo(other.name);
    }

    // hashCode and equals methods are important for using Owner as a key in a HashMap
    @Override
    public int hashCode() {
        return name != null ? name.hashCode() : 0;
    }
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Owner other = (Owner) obj;
        return name != null ? name.equals(other.name) : other.name == null;
    }
}
