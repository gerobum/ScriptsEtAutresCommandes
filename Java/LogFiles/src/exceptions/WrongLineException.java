package exceptions;

public class WrongLineException extends Exception {
    public WrongLineException() {
        super("Ligne incorrecte");
    }
}
