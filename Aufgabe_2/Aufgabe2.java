package Aufgabe_2;
import java.net.*;
import java.util.Scanner;

public class Aufgabe2 {
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        while (true) {
            System.out.println("Gebe IP-Adresse oder Domain ein:");
            String input = scanner.nextLine();
            
            if ("exit".equalsIgnoreCase(input)) {
                break;
            }
            
            try {
                InetAddress address = InetAddress.getByName(input);
                System.out.println("Host-Name: " + address.getHostName());
                System.out.println("IP-Adresse: " + address.getHostAddress());
            } catch (UnknownHostException e) {
                System.out.println("Die Adresse konnte nicht aufgelöst werden: " + e.getMessage());
            }
        }
        
        scanner.close();
    }
}
