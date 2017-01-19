package log_gestion;

import exceptions.WrongLineException;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;

/**
 *
 * @author yvan
 */
public class Log {
    
    private List<LogLine> liste = new LinkedList<>();

    public enum Statut {
        ON, OFF;
    }

    public void add(File file) throws FileNotFoundException {
        try (Scanner in = new Scanner(file);) {
            while (in.hasNextLine()) {
                String line = in.nextLine();
                try {
                    liste.add(new LogLine(line));
                } catch (WrongLineException ex) {
                    System.err.println("ERREUR ---> " + line);
                }
            }
            for(LogLine line : liste) {
                System.out.println(line.getStatus());
            }
        }
    }
    
    public void clear() {
        liste.clear();
    }
    
    public void quiEtaientConnectes() {
        List<LogLine> on = liste.stream()
                .filter(p -> p.getStatus() == Statut.ON)
                .collect(Collectors.toList());
        List<LogLine> off = liste.stream()
                .filter(p -> p.getStatus() == Statut.OFF)
                .collect(Collectors.toList());
                
        for(LogLine line : on) {
            off.stream()
                    .filter(p -> p.getNum().equals(line.getNum()))
                    .filter(p -> p.getDateTime().after(line.getDateTime()))
                    .forEach(p -> { 
                        System.out.println(line.getNum() + " de " + line.getDateTime() + " à " + p.getDateTime());
                    });
        }
    }
}
