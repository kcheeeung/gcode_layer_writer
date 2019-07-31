import java.util.List;
import java.util.Objects;

/** 
 * Gcommand 
 */
public class Gcommand implements Comparable {
    private double x, y, z;
    private int material;
    private int usecs;
    private String nameID;

    /**
     * Creates a Gcode command object with x,y,z coords, material, usecs, and associated file name
     */
    public Gcommand(double x, double y, double z, int mat, int us, String n) {
        this.x = x;
        this.y = y;
        this.z = z;
        this.material = mat;
        this.usecs = us;
        this.nameID = n;
    }

    /**
     * Creates a dummy Gcode command object
     */
    public Gcommand(double x, double y) {
        this.x = x;
        this.y = y;
        this.z = -999;
        this.material = -999;
        this.usecs = -999;
        this.nameID = null;
    }

    /** Returns the X coordinate */
    public double getX() {
        return x;
    }

    /** Returns the Y coordinate */
    public double getY() {
        return y;
    }

    /** Returns the Z coordinate */
    public double getZ() {
        return z;
    }

    /** Returns the material type */
    public int getMaterial() {
        return material;
    }

    /** Returns the pulse time in usecs */
    public int getUsecs() {
        return usecs;
    }
    
    /** Returns the associated file name */
    public String getNameID() {
        return nameID;
    }
    
    /**
     * Returns the euclidean distance 
     * @param a Gcommand A
     * @param b Gcommand B
     */
    public static double distance(Gcommand a, Gcommand b) {
        double x = a.x - b.x;
        double y = a.y - b.y;
        return Math.sqrt((x * x) + (y * y));
    }

    /**
     * Returns the euclidean total path distance
     * @param list input list of Gcommands
     */
    public static double pathDistance(List<Gcommand> list) {
        double totalDist = 0;
        int length = list.size();
        for (int i = 0; i < length - 1; i++) {
            totalDist += distance(list.get(i), list.get(i + 1));
        }
        return totalDist;
    }

    @Override
    public String toString() {
        if (material == 0) {
            return "T0;\n" + 
                "G1 X" + x + " Y" + y + "; Material: " + material + "\n" +
                "M430 V0 S" + usecs + "; Send pulse\n";
        } else if (material == 1) {
            return "T1;\n" + 
                "G1 X" + x + " Y" + y + "; Material: " + material + "\n" +
                "M430 V0 S" + usecs + "; Send pulse\n";
        } else if (material == 2) {
            return "T2;\n" + 
                "G1 X" + x + " Y" + y + "; Material: " + material + "\n" +
                "M430 V0 S" + usecs + "; Send pulse\n";
        } else {
            throw new Error("Invalid or unknown material");
        }
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Gcommand o = (Gcommand) obj;
        return x == o.x && y == o.y;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y, z);
    }

    @Override
    public int compareTo(Object o) {
        Gcommand gc = (Gcommand) o;
        int diff = Double.compare(y, gc.y);
        if (diff == 0) {
            diff = Double.compare(x, gc.x);
        }
        return diff;
    }
}
