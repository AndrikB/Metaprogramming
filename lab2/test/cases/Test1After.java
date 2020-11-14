/*
 * Copyright (c) 1995-2020
 */
package com.quiz.services;

import java.util.List;


/**
 * The Foo class provides 
 */
@SuppressWarnings({"ALL"})
public class Foo<T extends Bar & Abba, U> {

    /**
     * @param args
     * @return
     */
    public static void main(String args[]){
    }

    /**
     * The x documentation comment
     */
    @Anotation
    int[] x = new int[]{1, 3, 5, 6, 7, 87, 1213, 2};

    /**
     * @param x
     * @param y
     * @return
     * @throws A
     * @throws B
     */
    public T foo(List<Integer, Float> x, int y) throws A, B {
    }

    /**
     * @return
     */
    void bar() {
    }

}


/**
 * The Bar class provides 
 */
class Bar {

    /**
     * @param qw
     * @return
     */
    static <U, T> U mess(T qw) {
        return null;
    }

}


/**
 * The Abba interface provides 
 */
interface Abba{

}


/**
 * The Sample class provides 
 */
class Sample {

    /**
     * @param i
     * @param longParameterName
     * @param missingDescription
     * @return
     * @throws XXXException
     * @throws YException
     * @throws zException
     */
    public abstract String sampleMethod(int i, int longParameterName, int missingDescription) throws XXXException, YException, zException;


    /**
     * @return
     */
    public abstract String sampleMethod2();


    /**
     * @return
     */
    public abstract String sampleMethod3();
}


/**
 * The A class provides 
 */
class A{

    /**
     * @param a
     * @param b
     * @return
     */
    public void get(String a, Integer b) {
        return a;
    }
}


/**
 * The Main class provides 
 */
class Main {


  /**
   * @param arGs
   * @return
   */
  public static void main(String arGs[]) {
    // Creates a string
    String name = "Programiz";
    System.out.println("String is: " + name);

  }
}