import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;

public class Main {
    public static void main(String[] args) throws Exception {
        File fileAsli = new File("C:\\Users\\asus\\Pictures\\elkontole.png");
        BufferedImage gambar = ImageIO.read(fileAsli);

        double xAwal = 0.35;
        double r = 3.99;
        int m1 = 255; 
        int m2 = 256; 
        int m3 = 257;

        int[] pikselMentah = App.bongkarGambar(gambar);
        
        int totalPiksel = pikselMentah.length;
        double[] deretChaotic = App.generateLogisticMap(xAwal, r, totalPiksel);
        
        int[] pikselAcak = App.skibiditoilet(pikselMentah, deretChaotic);
        
        int[] pikselSandi = App.prosesDifusi(pikselAcak, xAwal, r, m1, m2, m3);
        
        BufferedImage gambarHasil = App.susunGambar(pikselSandi, gambar.getWidth(), gambar.getHeight());
        
        File fileSimpan = new File("C:\\Users\\asus\\Pictures\\elbangsate.png");
        ImageIO.write(gambarHasil, "png", fileSimpan);
        
        System.out.println("Enkripsi sukses!");
    }
}