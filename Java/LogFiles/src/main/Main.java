package main;

import java.io.File;
import java.io.FileNotFoundException;
import log_gestion.Log;

public class Main {
    public static void main(String[] args) throws FileNotFoundException {
        Log logline = new Log();
        logline.add(new File("logon_18_01_2017.log"));
        logline.add(new File("logoff_18_01_2017.log"));
        logline.quiEtaientConnectes();
    }
 
}
