package log_gestion;

import exceptions.WrongLineException;
import java.io.File;
import java.io.FileNotFoundException;
import java.text.DateFormat;
import java.util.Date;
import java.util.LinkedList;
import java.util.List;
import java.util.Optional;
import java.util.Scanner;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 *
 * @author yvan
 */
public class Log {

    // logoff de e1401196 sur FST-I37-PC25 le 18/01/2017 a  8:07:48,08
    private List<LogLine> liste = new LinkedList<>();
    private static final DateFormat DF = DateFormat.getTimeInstance(DateFormat.SHORT);

    public class Connexion {

        private String num;
        private String lieu;
        private String ufr;
        private String salle;
        private String poste;
        private Date debut;
        private Date fin;

        public Connexion(String num, String lieu, String ufr, String salle, String poste, Date debut, Date fin) {
            this.num = num;
            this.lieu = lieu;
            this.ufr = ufr;
            this.salle = salle;
            this.poste = poste;
            this.debut = debut;
            this.fin = fin;
        }
        
        
        
        @Override
        public String toString() {
            if (ufr != null) {
                return num + " sur le poste " + poste + " de " + DF.format(debut) + " à " + DF.format(fin);
            } else {
               return num + " en " + lieu + " de " + DF.format(debut) + " à " + DF.format(fin); 
            }
        }

        public String getNum() {
            return num;
        }

        public String getLieu() {
            return lieu;
        }

        public String getUfr() {
            return ufr;
        }

        public String getSalle() {
            return salle;
        }

        public String getPoste() {
            return poste;
        }

        public Date getDebut() {
            return debut;
        }

        public Date getFin() {
            return fin;
        }
        
        
    }

    private List<Connexion> connexions = new LinkedList<>();
    
    private String salle = null;
    
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
        this.salle = salle;
        connexions.clear();
            
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
            Optional<LogLine> opt = off.stream()
                    .filter(p -> p.getDateTime().after(line.getDateTime()))
                    .filter(p -> p.getDateTime().before(fin))
                    .filter(p -> p.getSalle() != null ? p.getSalle().equals(salle) : p.getLieu().contains(salle))
                    .filter(p -> p.getNum().equals(line.getNum()))
                    .filter(p -> p.getDateTime().after(line.getDateTime()))
                    .findFirst();
            connexions.add(new Connexion(line.getNum(), line.getLieu(), line.getUfr(), line.getSalle(), line.getPoste(), line.getDateTime(), opt.get().getDateTime()));
        });
    }
    
    @Override
    public String toString() {
        if (salle == null) {
            return "{}";
        } else {
            StringBuilder sb = new StringBuilder("Salle ");
            sb.append(salle).append('\n');
            connexions.stream().forEach((c) -> {
                sb.append(c).append('\n');
            });
            return sb.toString();
        }
    }
    
    public Stream<Connexion> stream() {
        return connexions.stream();
    }
}
