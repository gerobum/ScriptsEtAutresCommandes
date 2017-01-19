package log_gestion;

import exceptions.WrongLineException;
import java.text.DateFormat;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import log_gestion.Log.Statut;

public class LogLine {

    private static final Pattern LINE_PATTERN = Pattern.compile("(?<status>[^\\s]*)[\\s]*de[\\s]*(?<num>[^\\s]*)[\\s]*sur[\\s]*(?<sallemachine>[^\\s]*)[\\s]*le[\\s]*(?<date>.*)[\\s]*a[\\s]*(?<heure>.*)");
    private static final Pattern DATE_PATTERN = Pattern.compile("(?<jour>[0-9]*).*/(?<mois>[0-9]*).*/(?<annee>[0-9]*).*");
    private static final Pattern TIME_PATTERN = Pattern.compile("(?<heure>[0-9]*).*:(?<minute>[0-9]*).*:(?<seconde>[0-9]*).*,.*");
    private static final DateFormat DF = DateFormat.getDateTimeInstance();
  
    // logoff de e1401196 sur FST-I37-PC25 le 18/01/2017 a  8:07:48,08
    private Statut status;
    private String num;
    private String salleMachine;
    private Date dateTime;

    public LogLine(String line) throws WrongLineException {

        Matcher matcher = LINE_PATTERN.matcher(line);
        if (matcher.matches()) {
            System.out.println("#"+matcher.group("status")+"#");
            if ("logoff".equals(matcher.group("status"))) {
                status = Statut.OFF;
            } else {
                status = Statut.ON;
            }
            num = matcher.group("num");
            salleMachine = matcher.group("sallemachine");
            dateTime = get(matcher.group("date"), matcher.group("heure"));
        } else {
            throw new WrongLineException();
        }
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
            return num + " s'est logué en " + salleMachine + " le " + DF.format(dateTime);
        } else {
            return num + " s'est délogué en " + salleMachine + " le " + DF.format(dateTime);
        }
    }

    public Statut getStatus() {
        return status;
    }

    public String getNum() {
        return num;
    }

    public String getSalleMachine() {
        return salleMachine;
    }

    public Date getDateTime() {
        return dateTime;
    } 
}
