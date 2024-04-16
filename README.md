# RPS

RPS steht für "Resourse Planning System" und ist eine Webanwendung, die entwickelt wurde, um Materiallager in Bildungseinrichtungen zu verwalten. Die Anwendung wurde mit Flask, einem Python-Webanwendungs-Framework, erstellt.  

## Funktionen

- **Anmeldung:** Nutzende können sich anmelden, um auf die Funktionen der Anwendung zuzugreifen.  
- **Begrüßungsseite:** Nach der Anmeldung werden die Nutzenden auf einer Begrüßungsseite weitergeleitet, die Informationen über die Bildungseinrichtung, Dozierende und verfügbare Kurse enthält.  
- **Buchung von Kursen:** Nutzende können Kurse buchen und dabei Materialien und Teilnehmendenanzahl angeben.  
- **Lagerverwaltung:** Die Anwendung ermöglicht die Anzeige aller vorhandenen Materialien im Lager, Bearbeiten und Hinzufügen neuer Materialien.  
- **Kursverwaltung:** Nutzende können vorhandene Kurse anzeigen, bearbeiten oder neue Kurse hinzufügen.  
- **Dozentenverwaltung:** Die Anwendung ermöglicht das Hinzufügen neuer Dozierender, Anzeigen vorhandener Dozierender sowie das Bearbeiten von Kursen und Materialien, die diesen zugeordnet sind.  

## Installation

1. Stelle sicher, dass Python installiert ist.  
2. Installiere die erforderlichen Abhängigkeiten mit `pip install -r requirements.txt`.  
3. Füge einen Nutzer zu der Datenbank `users.db` hinzu um die Anwendung nutzen zu können:  
    - Navigiere innerhalb der Konsole zu dem Ordner `rps/database/`.  
    - Führe den Konsolenbefehl `sqlite3 users.db` aus.  
    - Führe den Konsolenbefehl `INSERT INTO USERS(user, password) VALUES(<Nutzer/in>, <Passwort>);` aus. Ersetze `<Nutzer/in>` durch den gewünschten Nutzendennamen und `<Passwort>` durch das gewünschte Passwort.  
    - Führe den Konsolenbefehl `.quit` aus.  
4. Starte die Anwendung auf einem der folgenden Wege:  
    - Führe den Konsolenbefehl `flask run` innerhalb des Hauptverzeichnisses der Anwendung aus.  
    - Führe die Datei `rps.bat` oder eine Verknüpfung zu dieser aus (Windows).  
    - Führe die Datei `rps.sh` oder eine Verknüpfung zu dieser aus (Linux, Mac).  

## Konfiguration

Die Konfiguration der Anwendung erfolgt über die Datei `config.json`, welche folgendermaßen aufgebaut ist:  

>{  
>&nbsp;&nbsp;&nbsp;&nbsp;"company": "&lt;Unternehmen&gt;",  
>&nbsp;&nbsp;&nbsp;&nbsp;"color": "#&lt;RGB&gt;",  
>&nbsp;&nbsp;&nbsp;&nbsp;"font_color": "&lt;Farbe&gt;"  
>}  

Ersetze `<Unternehmen>` durch deinen Unternehmensnamen, `<RGB>` durch einen hexadezimahlen RGB-Farbwert und `<Farbe>` durch eine der folgenden Optionen: `Schwarz`, `Weiß`, `Grau`, `Dunkelblau`, `Hellblau`, `Rot`, `Grün`, `Gelb`.  

Ein Unternehmenslogo kann als Icon genutzt werden, indem eine Datei vom Format `ico` und mit dem Namen `logo.ico` in das Verzeichnis `rps/static/` eingefügt wird.  
