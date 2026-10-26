import java.awt.image.BufferedImage;
import java.util.Arrays;

public class App {
    public static int[] bongkarGambar(BufferedImage gambar) {
        int lebar = gambar.getWidth();
        int tinggi = gambar.getHeight();
        int[] deretPiksel = new int[lebar * tinggi];

        for (int y = 0; y < tinggi; y++) {
            for (int x = 0; x < lebar; x++) {
                int indeks = (y * lebar) + x;
                deretPiksel[indeks] = gambar.getRGB(x, y);
            }
        }
        return deretPiksel;
    }

    public static double[] generateLogisticMap(double xAwal, double r, int ukuran) {
        double[] deret = new double[ukuran];
        double x = xAwal;
        for (int i = 0; i < ukuran; i++) {
            deret[i] = x;
            x = r * x * (1 - x);
        }
        return deret;
    }

    public static int[] skibiditoilet(int[] deretPikselAsli, double[] deretChaotic) {
        int ukuran = deretPikselAsli.length;
        Integer[] indeks = new Integer[ukuran];
        
        for (int i = 0; i < ukuran; i++) {
            indeks[i] = i;
        }
        
        Arrays.sort(indeks, (a, b) -> Double.compare(deretChaotic[a], deretChaotic[b]));
        
        int[] deretPikselAcak = new int[ukuran];
        for (int i = 0; i < ukuran; i++) {
            deretPikselAcak[i] = deretPikselAsli[indeks[i]];
        }
        
        return deretPikselAcak;
    }

    public static int[] prosesDifusi(int[] deretPikselAcak, double xAwal, double r, int m1, int m2, int m3) {
        int ukuran = deretPikselAcak.length;
        int[] deretPikselSandi = new int[ukuran];
        double x = xAwal;

        for (int i = 0; i < ukuran; i++) {
            int warnaAsli = deretPikselAcak[i];
            
            warnaAsli = Math.abs(warnaAsli);

            int[] kunci = Decrpty.logicmap(x, r, m1, m2, m3);

            int a1 = (warnaAsli + kunci[0]) % m1;
            int a2 = (warnaAsli + kunci[1]) % m2;
            int a3 = (warnaAsli + kunci[2]) % m3;

            int warnaBaru = Decrpty.China(m1, m2, m3, a1, a2, a3);

            deretPikselSandi[i] = warnaBaru;

            x = r * x * (1 - x);
        }

        return deretPikselSandi;
    }

    public static BufferedImage susunGambar(int[] deretPiksel, int lebar, int tinggi) {
        BufferedImage gambarBaru = new BufferedImage(lebar, tinggi, BufferedImage.TYPE_INT_RGB);
        
        for (int y = 0; y < tinggi; y++) {
            for (int x = 0; x < lebar; x++) {
                int indeks = (y * lebar) + x;
                gambarBaru.setRGB(x, y, deretPiksel[indeks]);
            }
        }
        
        return gambarBaru;
    }
}