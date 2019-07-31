import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import javax.imageio.ImageIO;

import kdtree.KDTree;

/**
 * LayerConverter<br></br>
 * This image analysis software was created as a complement to the 3D Bioprinter.
 * The program analyzes an image to generate a customized gcode coordinate map for
 * the bioprinter’s microprocessor to interpret<br></br>
 * 
 * Credits
 * @author Kevin Cheung   - Class of 2016
 * @author Mason Fujimoto - Class of 2017
 * @author Quinn Tran     - Class of 2018
 * @author Katie Wu       - Class of 2018
 * @author Randall White  - Class of 2018
 */
public class LayerConverter {
    public static final String START_GCODE = "G28; Home axes\nM42 P4 S245\n";
    public static final String END_GCODE = "M84; Motor off\nM42 P4 S255\nM42 P5 S255\nM42 P6 S255\n";
    public static final double STARTX = 40.0f;
    public static final double STARTY = 40.0f;
    public static final double UNIT = 1.0f;

    public static final int MATERIAL0 = 0;
    public static final int MATERIAL1 = 1;
    public static final int MATERIAL2 = 2;
    public static final int U_SECS0 = 100;
    public static final int U_SECS1 = 100;
    public static final int U_SECS2 = 100;

    public List<File> imagePath;
    public List<List<Gcommand>> convertedImages;
    public List<List<Gcommand>> finalResult;
    public File path;
    public String outputName;
    // Distance
    public double startDistance = 0;
    public double optimizedDistance = 0;
    // File Size
    public long startSize = 0;
    public long optimizedSize = 0;

    /**
     * Takes an image and converts it into gcode coordindates
     * @param p input file path
     * @param out desired output name for your result
     */
    public LayerConverter(String p, String out) {
        long start = System.currentTimeMillis();
        imagePath = new ArrayList<>();
        convertedImages = new ArrayList<>();
        finalResult = new ArrayList<>();
        path = new File(p);
        outputName = out;

        try {
            if (!path.isDirectory()) {
                intializeAsImage();
            } else {
                initializeAsFolder();
            }
        } catch (Exception e) {
            System.out.println("Initialization failed");
            e.printStackTrace();
            System.exit(-1);
        }
        convertToBW();
        optimizePath();
        convertToGCode();

        System.out.printf("Finished in %.3f secs\n", (System.currentTimeMillis() - start) / 1000.0f);
        System.out.printf("Distance: %.2f -> %.2f\n", startDistance, optimizedDistance);
        System.out.printf("Increased runtime efficiency by %.2f%%\n", ((startDistance / optimizedDistance) - 1) * 100);
        System.out.printf("Bytes: %d -> %d\n", startSize, optimizedSize);
        System.out.printf("Increased space efficiency by %.2f%%\n", (((double) startSize / (double) optimizedSize) - 1) * 100);
    }

    /**
     * Initializes path as an image.
     * @throws Error File provided is invalid or unsupported
     */
    private void intializeAsImage() {
        String name = path.getName();
        String ex = getExtension(name);
        if (ex.equals("png") || ex.equals("jpg") || ex.equals("jpeg")) {
            imagePath.add(path);
        } else {
            throw new Error("Unsupported image. Detected extension was: ." + ex);
        }
    }

    /**
     * Initializes path as a directory
     * @throws Error No valid files were detected
     */
    private void initializeAsFolder() {
        File[] files = path.listFiles();
        Arrays.sort(files, (a, b) -> a.getName().compareTo(b.getName()));
        for (File f : files) {
            String name = f.getName();
            String ex = getExtension(name);
            if (ex.equals("png") || ex.equals("jpg") || ex.equals("jpeg")) {
                imagePath.add(f);
            }
        }
        if (imagePath.size() == 0) {
            throw new Error("No valid files found");
        }
    }

    /**
     * Returns the extension of the FILE.
     * @param file the name of your file path
     */
    private String getExtension(String file) {
        StringBuilder extension = new StringBuilder(5);
        for (int i = file.length() - 1; i >= 0; i--) {
            char c = file.charAt(i);
            if (c != '.') {
                extension.append(Character.toLowerCase(c));
            } else {
                break;
            }
        }
        return extension.reverse().toString();
    }

    /**
     * This takes the images, converts it into grayscale using a luminance value calculation.
     * Then points below 50% luminance (dark pixel) is pushed as a Gcommand point to visit.
     */
    private void convertToBW() {
        try {
            for (File f : imagePath) {
                String name = f.getName();
                List<Gcommand> temp = new ArrayList<>();
                BufferedImage img = ImageIO.read(f);
                int m = img.getWidth(), n = img.getHeight();
                for (int i = 0; i < m; i++) {
                    for (int j = 0; j < n; j++) {
                        // Calculate the luminance value
                        Color c = new Color(img.getRGB(i, j));
                        double luminance = (0.2126f * c.getRed() + 0.7152f * c.getGreen() + 0.0722f * c.getBlue()) / 255.0f;
                        if (luminance <= 0.5f) {
                            // (n - j) flips the image for proper output
                            temp.add(new Gcommand(i * UNIT + STARTX, (n - j) * UNIT + STARTY, 0, MATERIAL0, U_SECS0, name));
                        }
                    }
                }
                convertedImages.add(temp);
            }
        } catch (Exception e) {
            System.out.println("Image conversion error");
            e.printStackTrace();
            System.exit(-1);
        }
    }

    /**
     * Given a list of points, a k-nearest neighbor search optimizes path planning
     * for the 3D bioprinter.
     */
    private void optimizePath() {
        for (List<Gcommand> list : convertedImages) {
            Collections.sort(list);
            startDistance += Gcommand.pathDistance(list);

            // Initialize KDTree
            int totalPoints = 0;
            KDTree kdtree = new KDTree(2);
            for (Gcommand gc : list) {
                double[] temp = {gc.getX(), gc.getY()};
                kdtree.insert(temp, gc);
                totalPoints++;
            }

            // k-nearest neighbor search
            List<Gcommand> optimized = new ArrayList<>(list.size());
            HashSet<Gcommand> visited = new HashSet<>((int) (list.size() / 0.75f) + 1);
            double[] last = {0, 0};
            Gcommand prev = (Gcommand) kdtree.nearest(last);
            optimized.add(prev);
            visited.add(prev);
            
            while (visited.size() < totalPoints) {
                last[0] = prev.getX();
                last[1] = prev.getY();
                boolean foundNext = false;
                int topN = 5;
                int pos = 0;
                while (!foundNext) {
                    if (topN > totalPoints) {
                        topN = totalPoints;
                    }
                    Object[] nearRes = kdtree.nearest(last, topN);
                    int i;
                    for (i = pos; i < nearRes.length; i++) {
                        Gcommand gc = (Gcommand) nearRes[i];
                        if (!visited.contains(gc)) {
                            optimized.add(gc);
                            visited.add(gc);
                            prev = gc;
                            foundNext = true;
                            break;
                        }
                    }
                    pos = i; // continue where last left off
                    topN *= 2;
                }
            }
            finalResult.add(optimized);
            optimizedDistance += Gcommand.pathDistance(optimized);
        }
    }

    /**
     * Converts the optimized path into a .gcode file
     */
    private void convertToGCode() {
        try {
            String fileName = outputName + ".gcode";
            BufferedWriter out = new BufferedWriter(new FileWriter(fileName));
            int approxLines = 0;
            for (List<Gcommand> list : finalResult) {
                out.write(";" + list.get(0).getNameID() + "\n");
                for (Gcommand gc : list) {
                    out.write(gc.toString());
                    approxLines++;
                }
            }
            out.close();
            startSize = new File(fileName).length();

            StringBuilder optimize = new StringBuilder(approxLines);
            optimize.append(START_GCODE);
            BufferedReader in = new BufferedReader(new FileReader(fileName));
            String line, prevHead = null;
            boolean firstHead = true;
            while ((line = in.readLine()) != null) {
                switch (line) {
                    case "T0;": case "T1;": case "T2;":
                        if (firstHead) {
                            optimize.append(line);
                            optimize.append("\n");
                            prevHead = line;
                            firstHead = false;
                        } else if (!line.equals(prevHead))  {
                            optimize.append(line);
                            optimize.append("\n");
                            prevHead = line;
                        }
                        break;
                    default:
                        optimize.append(line);
                        optimize.append("\n");
                        break;
                }
            }
            in.close();
            optimize.append(END_GCODE);

            BufferedWriter opt = new BufferedWriter(new FileWriter(fileName));            
            opt.write(optimize.toString());
            opt.close();
            optimizedSize = new File(fileName).length();
        } catch (Exception e) {
            System.out.println("Gcode conversion failed");
            e.printStackTrace();
            System.exit(-1);
        }
    }

    public static void main(String[] args) {
        // LayerConverter convert = new LayerConverter("cal_logo", "aaa_cal_logo");
        LayerConverter convert = new LayerConverter("cal_logo/cal_logo_scaled.png", "cal_logo");
    }
}
