/***/
package some;

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
     * @return return description in invali place!!!!!!!!!!!!.
     * @throws XXX_Exception description exist.
     * @throws yException   description.
     * @throws zException
     * @invalidTag
     */
    public abstract String sampleMethod(int i, int longParameterName, int missingDescription) throws XXX_Exception, yException, zException;

    /**
     * One-line comment
     * @return
     */
    public abstract String sampleMethod2();

    /**
     * description
     * 
     * @return
     */
    public abstract String sampleMethod3();
}