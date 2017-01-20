package main;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.GregorianCalendar;
import log_gestion.Log;
import sun.util.calendar.Gregorian;

public class Main {
    public static void main(String[] args) throws FileNotFoundException {
        Log log = new Log();
        log.add(new File("logon_18_01_2017.log"));
        log.add(new File("logoff_18_01_2017.log"));
        GregorianCalendar debut = new GregorianCalendar(2017, 0, 18);
        GregorianCalendar fin = new GregorianCalendar(2017, 0, 19);
        log.quiEtaientConnectes("I37", debut.getTime(), fin.getTime());
        GregorianCalendar apartir = new GregorianCalendar(2017, 0, 18, 9, 55, 0);
        log.stream()
                .filter(p -> !p.getFin().before(apartir.getTime()))
                .forEach(System.out::println);
    }
 
}
