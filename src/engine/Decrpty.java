import java.util.Arrays;
public class Decrpty {

    //cek input
  public static int hitungFPB(int a, int b) {
        if (b == 0) {
            return a;
        }
        return hitungFPB(b, a % b);
    }

    public static boolean cekRelatifPrima(int m1, int m2, int m3) {
        if (hitungFPB(m1, m2) == 1 && hitungFPB(m1, m3) == 1 && hitungFPB(m2, m3) == 1) {
            return true;
        }
        return false;
    }

        // masukan angka
    public static int InversModulo(int a, int m) {
    int m0 = m;
    int y = 0;
    int x = 1;

    if (m == 1) {
        return 0;
    }

    while (a > 1) {
        int q = a / m;
        int t = m;

        m = a % m;
        a = t;
        t = y;

        y = x - q * y;
        x = t;
    }

    if (x < 0) {
        x = x + m0;
    }

    return x;
}

public static int China(int m1, int m2, int m3, int a1, int a2, int a3) {
    int M = m1 * m2 * m3;
    int M1 = M / m1;
    int M2 = M / m2;
    int M3 = M / m3;

    int y1 = InversModulo(M1, m1);
    int y2 = InversModulo(M2, m2);
    int y3 = InversModulo(M3, m3);

    return (a1 * M1 * y1 + a2 * M2 * y2 + a3 * M3 * y3) % M;

}

public static int[] logicmap(double x, double r, int m1, int m2, int m3) {
    int[] k = new int[3];

    x = r * x * (1 - x);
    k[0] = (int) (x * 1000000) % m1;

    x = r * x * (1 - x);
    k[1] = (int) (x * 1000000) % m2;

    x = r * x * (1 - x);
    k[2] = (int) (x * 1000000) % m3;

    return k;
}


}