package log_gestion;

import exceptions.WrongLineException;
import java.text.DateFormat;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import log_gestion.Log.Statut;

public class LogLine {

    private static final Pattern LINE_PATTERN = Pattern.compile("(?<status>[^\\s]*)[\\s]*de[\\s]*(?<num>[^\\s]*)[\\s]*sur[\\s]*(?<lieu>[^\\s]*)[\\s]*le[\\s]*(?<date>.*)[\\s]*a[\\s]*(?<heure>.*)");
    private static final Pattern DATE_PATTERN = Pattern.compile("(?<jour>[0-9]*).*/(?<mois>[0-9]*).*/(?<annee>[0-9]*).*");
    private static final Pattern TIME_PATTERN = Pattern.compile("(?<heure>[0-9]*).*:(?<minute>[0-9]*).*:(?<seconde>[0-9]*).*,.*");
    private static final Pattern LIEU_PATTERN = Pattern.compile("(?<ufr>.*)-(?<salle>.*)-(?<poste>.*)");
    private static final DateFormat DF = DateFormat.getDateTimeInstance();
  
    // logoff de e1401196 sur FST-I37-PC25 le 18/01/2017 a  8:07:48,08
    private Statut status;
    private String num;
    private String lieu;
    private String ufr;
    private String salle;
    private String poste;
    private Date dateTime;

    public LogLine(String line) throws WrongLineException {

        Matcher matcher = LINE_PATTERN.matcher(line);
        if (matcher.matches()) {
            if ("logoff".equals(matcher.group("status"))) {
                status = Statut.OFF;
            } else {
                status = Statut.ON;
            }
            num = matcher.group("num");
            lieu = matcher.group("lieu");
            Matcher ml = LIEU_PATTERN.matcher(lieu);
            if (ml.matches()) {
                ufr = ml.group("ufr");
                salle = ml.group("salle");
                poste = ml.group("poste");
            } else {
                ufr = salle = poste = null;
            }
            dateTime = get(matcher.group("date"), matcher.group("heure"));
        } else {
            throw new WrongLineException();
        }
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
    
    private Date get(String date, String time) throws WrongLineException {
        Matcher md = DATE_PATTERN.matcher(date);
        Matcher mt = TIME_PATTERN.matcher(time);
        if (md.matches() && mt.matches()) {
            try {
            return new GregorianCalendar(
                    Integer.parseInt(md.group("annee")), 
                    Integer.parseInt(md.group("mois"))-1, 
                    Integer.parseInt(md.group("jour")), 
                    Integer.parseInt(mt.group("heure")), 
                    Integer.parseInt(mt.group("minute")), 
                    Integer.parseInt(mt.group("seconde"))         
            ).getTime();
            } catch (NumberFormatException nde) {
                System.out.println(nde);
                throw new WrongLineException();
            }
        } else
            throw new WrongLineException();        
    }

    @Override
    public String toString() {
        if (status == Statut.ON) {
            return num + " s'est logué en " + lieu + " le " + DF.format(dateTime);
        } else {
            return num + " s'est délogué en " + lieu + " le " + DF.format(dateTime);
        }
    }

    public Statut getStatus() {
        return status;
    }

    public String getNum() {
        return num;
    }

    public Date getDateTime() {
        return dateTime;
    } 
}
