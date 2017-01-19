package log_gestion;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 *
 * @author yvan
 */
public class Log {

    public enum Statut {
        ON, OFF;
    }

    public void init(File file) throws FileNotFoundException {
        try (Scanner in = new Scanner(file);) {
            while (in.hasNextLine()) {
                String line = in.nextLine();
                /*try (Scanner lin = new Scanner(line)) {
                    System.out.print(lin.next() + " ");
                    while (lin.hasNext()) {
                        lin.next();
                        System.out.print(lin.next() + " ");
                    }
                }*/
                System.out.println();
            }
        }
    }
}
