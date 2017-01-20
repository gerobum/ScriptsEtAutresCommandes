package log_gestion;

import exceptions.WrongLineException;
import java.io.File;
import java.io.FileNotFoundException;
import java.text.DateFormat;
import java.util.Date;
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
    private static final DateFormat DF = DateFormat.getDateTimeInstance(DateFormat.SHORT, DateFormat.SHORT);

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
        }
    }

    public void clear() {
        liste.clear();
    }

    public void quiEtaientConnectes(String salle, Date debut, Date fin) {
        List<LogLine> on = liste.stream()
                .filter(p -> p.getDateTime().after(debut))
                .filter(p -> p.getDateTime().before(fin))
                .filter(p -> p.getSalle() != null ? p.getSalle().equals(salle) : p.getLieu().contains(salle))
                .filter(p -> p.getStatus() == Statut.ON)
                .collect(Collectors.toList());
        List<LogLine> off = liste.stream()
                .filter(p -> p.getStatus() == Statut.OFF)
                .collect(Collectors.toList());

        on.stream().forEach((line) -> {
            off.stream()
                    .filter(p -> p.getDateTime().after(debut))
                    .filter(p -> p.getDateTime().before(fin))
                    .filter(p -> p.getSalle() != null ? p.getSalle().equals(salle) : p.getLieu().contains(salle))
                    .filter(p -> p.getNum().equals(line.getNum()))
                    .filter(p -> p.getDateTime().after(line.getDateTime()))
                    .forEach(p -> {
                        System.out.println(line.getNum() + " en " + line.getLieu() + " de " + DF.format(line.getDateTime()) + " à " + DF.format(p.getDateTime()));
                    });
        });
    }
}
