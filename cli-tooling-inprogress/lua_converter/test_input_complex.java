// Complex Java input for end-to-end CLI test
public class TestComplex {
    public static void main(String[] args) {
        int[] arr = {1,2,3,4,5};
        for (int i : arr) {
            System.out.println(i * 2);
        }
        try {
            throw new Exception("Test error");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}