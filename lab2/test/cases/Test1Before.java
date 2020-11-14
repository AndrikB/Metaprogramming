/*
 * Copyright (c) 1995-2020
 */
package com.quiz.services;

import java.util.List;


@SuppressWarnings({"ALL"})
public class Foo<t extends Bar & Abba, U> {

    public static void main(String args[]){
    }

    @Anotation
    int[] x = new int[]{1, 3, 5, 6, 7, 87, 1213, 2};

    public t foo(List<Integer, Float> x, int y) throws A, B {
    }

    void bar() {
    }

}


class Bar {

    static <U, T> U mess(T qw) {
        return null;
    }

}


interface Abba{

}


class Sample {

    public abstract String sampleMethod(int i, int longParameterName, int missingDescription) throws XXXException, YException, zException;


    public abstract String sampleMethod2();


    public abstract String sampleMethod3();
}


class A{

    public void get(String a, Integer b) {
        return a;
    }
}


class Main {


  public static void main(String ar_gs[]) {
    // Creates a string
    String name = "Programiz";
    System.out.println("String is: " + name);

  }
}