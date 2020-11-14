/*
 * %W% %E% Firstname Lastname
 *
 * Copyright (c) 1995-2020 %your company name%
 *
 * This software is the confidential and proprietary information of 
 * %your company name%.  You shall not
 * disclose such Confidential Information and shall use it only in
 * accordance with the terms of the license agreement you entered into
 * with %your company name%.
 *
 * %your company name% MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF
 * THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
 * TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE, OR NON-INFRINGEMENT. SUN SHALL NOT BE LIABLE FOR
 * ANY DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR
 * DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.
 */
package sample;

/**
 * The Sample class provides 
 */
public class Sample {

    /**
     * This is a method description that is long enough to exceed right margin.
     * <p>
     * Another paragraph of the description placed after blank line.
     * <p/>
     * Line with manual
     * line feed.
     * 
     * @param i short named parameter description
     * @param longParameterName long named parameter description
     * @param missingDescription
     * @return return description.
     * @throws XXXException description.
     * @throws YException   description.
     * @throws zException
     * @invalidTag
     */
    public abstract String sampleMethod(int i, int longParameterName, int missingDescription) throws XXXException, YException, zException;

    /**
     * One-line comment
     * @return
     */
    public abstract String sampleMethod2();

    /**
     * Simple method description
     * 
     * @return
     */
    public abstract String sampleMethod3();
}