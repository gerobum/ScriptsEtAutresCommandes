package log_gestion;

import java.util.Date;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import log_gestion.Log.Statut;

public class LogLine {

    private static Pattern pattern = Pattern.compile("(?<status>.*)[\\s]*de[\\s]*(?<num>.*)[\\s]*sur[\\s]*(?<sallemachine>.*)[\\s]*le[\\s]*(?<date>.*)[\\s]*a[\\s]*(?<heure>.*)");
    // logoff de e1401196 sur FST-I37-PC25 le 18/01/2017 a  8:07:48,08
    private Statut status;
    private String num;
    private String salleMache;
    private Date date;

    public LogLine(String line) {

        Matcher matcher = pattern.matcher(line);
        if (matcher.matches()) {
            if ("logoff".equals(matcher.group("status"))) {
                status = Statut.OFF;
            } else {
                status = Statut.ON;
            }

            System.out.print(matcher.group("num") + " ");
            System.out.print(matcher.group("sallemachine") + " ");
            System.out.print(matcher.group("date") + " ");
            System.out.print(matcher.group("heure") + "\n");

        }
    }

}
