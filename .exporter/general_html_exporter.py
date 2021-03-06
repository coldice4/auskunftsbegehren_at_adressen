#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#######################
# Genereller Exporter #
#        HTML         #
#######################

import csv
import os
import sys

# In diesem Ordner sind wir
workDir = os.path.dirname(os.path.realpath(__file__)) + "/.."

# Hardgecodede Parameter
outFile = workDir + "/general.html"
csvFile = workDir + "/upload/general.csv"

def writeRecord(outFileHandler, record):
    # TODO: Library suchen für das
    outFileHandler.write("<div class=\"listItem {0}\">".format(record["Ebene"])) # Das ist der Container eines Datensatzes
    outFileHandler.write("<h4>{0}</h4>\n".format(record["Name"])) # Kurzbezeichnung
    outFileHandler.write("<p><strong>{0}</strong></p>\n".format(record["Name_Lang"])) # Langname
    outFileHandler.write("<p>{0}<br>\n".format(record["Adresse"])) # Straße, Hausnummer, Postfach
    outFileHandler.write("{0} {1}</p>\n".format(record["PLZ"], record["Ort"])) # PLZ und Ort
    outFileHandler.write("<p>Typ: <em>{0}</em></p>".format(record["Typ"])) # Typ der Firma; Branche steht schon in der Überschrift
    if record["E-Mail"]: # Email nur anzeigen wenn vorhanden, mit Icon
        outFileHandler.write("<span class=\"icon-mail screenOnly\"></span><span class=\"marginLeft\">Mail:</span> <a href=\"mailto:{0}\">{1}</a><br>\n".format(record["E-Mail"], record["E-Mail"]))

    if record["Tel"]: # Telefon nur anzeigen wenn vorhanden, mit Icon
        outFileHandler.write("<span class=\"icon-phone screenOnly\"></span><span class=\"marginLeft\">Tel:</span> <a href=\"tel:{0}\">{1}</a><br>\n".format(record["Tel"], record["Tel"]))

    if record["Fax"]: # Fax nur anzeigen wenn vorhanden, mit Icon
        outFileHandler.write("<span class=\"icon-upload screenOnly\"></span><span class=\"marginLeft\">Fax:</span> {0}<br>\n".format(record["Fax"]))

    outFileHandler.write("<p>Letzte Prüfung am: <em>{0}</em></p>\n".format(record["Pruefung"])) # Das ist die Beschreibung wann der Datensatz das letzte mal geprüft wurde
    outFileHandler.write("</div> <!-- List Item End -->\n\n") # Container Ende

# Header schreiben
try:
    with open(outFile, "w") as outFileHandler:
        outFileHandler.write("""<!DOCTYPE html>
            <html lang="de">
            <head>
                <meta charset="utf-8">
                <link rel="stylesheet" media="screen" href="mini-default.min.css">
                <link rel="stylesheet" type="text/css" href="style.css">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>
                    Export
                </title>
            </head>
            <body>
                <header class="sticky screenOnly">
                    <!-- TODO: Das automatisch generieren -->
                    <a href="?filter=Bund" role="button">Bund</a>
                    <a href="?filter=Burgenland" role="button">Burgenland</a>
                    <a href="?filter=Kärnten" role="button">Kärnten</a>
                    <a href="?filter=Niederösterreich" role="button">Niederösterreich</a>
                    <a href="?filter=Oberösterreich" role="button">Oberösterreich</a>
                    <a href="?filter=Salzburg" role="button">Salzburg</a>
                    <a href="?filter=Steiermark" role="button">Steiermark</a>
                    <a href="?filter=Tirol" role="button">Tirol</a>
                    <a href="?filter=Vorarlberg" role="button">Vorarlberg</a>
                    <a href="?filter=Wien" role="button">Wien</a>
                    <a href="?filter=Privat" role="button">Privat</a>
              </header>
              <div id="mainContainer">""")
except IOError:
    print("Cant write to file!")
    exit(1)

# Wir brauchen ein neues dict, weil wir die überschriften schreiben wollen
recordsDict = {}

# csv lesen und parsen
with open(csvFile, newline='') as csvFileReader:
    readFile = csv.DictReader(csvFileReader)

    for record in readFile: # Das geht durch alle Datensätze ...
        if not record["Ebene"] in recordsDict: # ... und wenn die "Ebene", d.h. "Bund", "Steiermark", "Privat" etc. noch nicht vorhanden ist ...
            print("Adding administration Level: " + record["Ebene"])
            recordsDict[record["Ebene"]] = {} # ... wird sie dem Dict hinzugefügt, und ebenfalls als dict initialisiert

        if not record["Branche"] in recordsDict[record["Ebene"]]: # Hier passiert das gleiche wie oben mit den Ebenen, nur mit den Branchen
            print("Adding sector: " + record["Branche"])
            recordsDict[record["Ebene"]][record["Branche"]] = {}

        print("Processing entry: " + record["Name"])
        lastChecked = record["Pruefung"].replace(".", "-") # Hier und in den nächsten zwei Zeilen wird eine eindeutige ID für jeden Datensatz generiert
        nameForId = record["Name"].replace(" ", "-").lower()
        id = record["Ebene"] + "_" + record["Branche"] + "_" + lastChecked + "_" + nameForId

        recordsDict[record["Ebene"]][record["Branche"]][id] = record # Hier fügen wir dann den Datensatz dem großen dict hinzu

try:
    with open(outFile, "a+") as outFileHandler:
        for administrationLevel in recordsDict:
            print("Writing administration Level: " + administrationLevel)

            outFileHandler.write("<div class=\"administrationLevelContainer filter\" id=\"{0}\">".format(administrationLevel)) # Das ist der "Ebene" Container
            outFileHandler.write("<h2 class=\"strong\">{0}</h2>".format(administrationLevel))

            for type in recordsDict[administrationLevel]:
                print("Writing type: " + type)
                outFileHandler.write("<div class=\"typeContainer {0}\">".format(type)) # Das ist der "Branche" Container
                outFileHandler.write("<h3 class=\"strong\">{0}</h3>".format(type))

                outFileHandler.write("<div class=\"itemContainer\">") # Hier ist der Item Container - Hierdrauf wirkt das CSS Grid
                for record in recordsDict[administrationLevel][type]:
                    print("Writing entry: " + recordsDict[administrationLevel][type][record]["Name"])
                    writeRecord(outFileHandler, recordsDict[administrationLevel][type][record]) # Hier schreiben wir den Datensatz
                outFileHandler.write("</div><!-- end of {0} itemContainer -->".format(recordsDict[administrationLevel][type][record]["Name"])) # Ende des itemContainer

                outFileHandler.write("</div><!-- end of {0} typeContainer -->".format(type)) # Ende des Branchen Containers
                print("End of: " + type)

            outFileHandler.write("</div><!-- end of {0} administrationLevelContainer -->".format(administrationLevel)) # Ende des Ebenen Containers
            print("End of: " + administrationLevel)

except IOError:
    print("Cant write to file!")
    exit(1)

# Footer
try:
    with open(outFile, "a+") as outFileHandler:
        outFileHandler.write("""</div> <!-- This is the end of the mainContainer -->
                <footer>
                    <p>
                    Lizenz: <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International</a><br>
                    <a href="https://github.com/cyber-perikarp/auskunftsbegehren_at_adressen/blob/master/docs/mitwirkende.md" target="_blank">Mitwirkende</a><br>
                    <a href="https://github.com/cyber-perikarp/auskunftsbegehren_at_adressen/issues/new" target="_blank" class="important">Neuen Datensatz einreichen</a>
                  </p>
                </footer>
                <script src="jquery-3.5.1.min.js"></script>
                <script src="filter.js"></script>
            </body>
            </html>
        """)
except IOError:
    print("Cant write to file!")
    exit(1)
