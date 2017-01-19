package main;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.GregorianCalendar;
import log_gestion.Log;
import sun.util.calendar.Gregorian;

public class Main {
    public static void main(String[] args) throws FileNotFoundException {
        Log logline = new Log();
        logline.add(new File("logon_18_01_2017.log"));
        logline.add(new File("logoff_18_01_2017.log"));
        GregorianCalendar debut = new GregorianCalendar(2017, 0, 18);
        GregorianCalendar fin = new GregorianCalendar(2017, 0, 19);
        logline.quiEtaientConnectes("I37", debut.getTime(), fin.getTime());
    }
 
}
