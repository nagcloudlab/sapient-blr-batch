package com.example.util;

import java.util.Iterator;

/*
Author: Nag
*/

// collection + iterator => Iterable

public class LinkedList<E> implements Iterable<E> {

    private Node head;
    private Node tail;

    public LinkedList() {
        this.head = null;
        this.tail = null;
    }  
    
    public void add(E data){
        Node newNode = new Node(data);
        if(head == null){
            head = newNode;
            tail = newNode;
        }else{
            tail.setNext(newNode);
            tail = newNode;
        }
    }

    public E get(int index){
        Node current = head;
        int count = 0;
        while(current != null){
            if(count == index){
                return current.getData();
            }
            count++;
            current = current.getNext();
        }
        throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + count);
    }

    public Iterator<E> iterator() {
        return new Iterator<E>() {
            private Node current = head;

            @Override
            public boolean hasNext() {
                return current != null;
            }

            @Override
            public E next() {
                E data = current.getData();
                current = current.getNext();
                return data;
            }
        };
    }

    private class Node{
        private E data;
        private Node next;

        public Node(E data){
            this.data = data;
            this.next = null;
        }

        public E getData() {
            return data;
        }

        public Node getNext() {
            return next;
        }
        public void setNext(Node next) {
            this.next = next;
        }

    }
    
}
