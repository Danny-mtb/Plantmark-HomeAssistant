# Plantmark for Home Assistant

Plantmark ist eine vollständig native Home-Assistant-Integration zur Verwaltung
und Pflege von Zimmerpflanzen. Sie benötigt keinen separaten Docker-Container,
keine Datenbank und keinen Cloud-Dienst. Alle Pflanzendaten werden im
Home-Assistant-Konfigurationseintrag gespeichert. Die Verwaltung erfolgt über
eine eigene, responsive Plantmark-Seite in der Home-Assistant-Seitenleiste.

## Funktionen

- Eigener **Plantmark-Tab in der Seitenleiste** mit Kartenansicht für alle
  Pflanzen, Bilder, Gießtermine, Warnungen und Sensorwerte.
- Pflanzen direkt im Plantmark-Tab hinzufügen, bearbeiten, gießen und löschen.
- Direkter Upload von JPEG-, PNG- und WebP-Bildern. Die Bilder werden lokal in
  Home Assistant gespeichert und vor dem Upload automatisch verkleinert.
- Auswahl eines vorhandenen Home-Assistant-Bereichs. Das zugehörige
  Pflanzengerät wird automatisch diesem Bereich zugeordnet.
- Optionaler Wasser- oder Bodenfeuchtesensor pro Pflanze mit Live-Anzeige des
  Sensorwerts in der Übersicht.
- Auf Bodenfeuchte eingegrenzte Sensorauswahl und optionale automatische
  Verschiebung des Gießzeitraums, solange die Erde noch feucht genug ist.
- Gießzeiträume wie **7–10 Tage** sowie eigene Zeiträume für Frühling, Sommer,
  Herbst und Winter.
- Ein Gießkalender mit eigenem Symbol und mehrtägigen Gießfenstern.
- Einmalige Gießerinnerungen über die Home-Assistant-Benachrichtigungszentrale,
  moderne `notify`-Entitäten oder vorhandene `notify.*`-Dienste wie Pushover.
- Optionale Suche in der Perenual-Pflanzendatenbank. Wissenschaftlicher Name,
  Gießempfehlung, Licht, Erde, Herkunft, Pflegegrad, Giftigkeit, Beschreibung
  und Bild können direkt übernommen werden.
- Jede Pflanze wird weiterhin als eigenes Home-Assistant-Gerät mit nativen
  Entitäten für Automationen angelegt.
- Sensoren für das letzte Gießen, Beginn und Ende des nächsten Gießfensters,
  minimales und maximales Gießintervall, verbleibende Tage, Saison und letzte
  Gießmenge.
- Warnsensoren für fälliges Gießen sowie Giftigkeit für Katzen und Hunde.
- Nativer **Gießen**-Button pro Pflanze, geeignet für Dashboards und Automationen.
- Gemeinsamer Gießkalender mit allen bevorstehenden Terminen.
- Optionales Pflanzenbild, Standort, wissenschaftlicher Name und Notizen.
- Import alter Plantmark-Daten aus einer JSON-Liste oder einer früheren
  API-Antwort im Format `{ "plants": [...] }`.
- Deutsche und englische Oberfläche sowie datenschutzfreundliche Diagnosedaten.

## Installation über Home Assistant Marketplace / HACS

1. Öffne **Marketplace → Drei-Punkte-Menü → Benutzerdefinierte Repositories**.
2. Füge die URL dieses GitHub-Repositories als Typ **Integration** hinzu.
3. Installiere **Plantmark** und starte Home Assistant neu.
4. Öffne **Einstellungen → Geräte & Dienste → Integration hinzufügen** und
   wähle **Plantmark**.
5. Vergib einen Namen für deine Pflanzenbibliothek.
6. Öffne anschließend den neuen Eintrag **Plantmark** in der Seitenleiste und
   füge dort deine erste Pflanze hinzu.

Nach einem Update muss Home Assistant neu gestartet werden. Ab Version 1.2.1
verwendet das Plantmark-Panel automatisch eine aus dem Dateiinhalt erzeugte
Versionskennung, damit der Browser keine ältere Oberfläche aus dem Cache lädt.

Für eine manuelle Installation kopierst du
`custom_components/plantmark` nach
`<home-assistant-config>/custom_components/plantmark` und startest Home
Assistant neu.

## Pflanzen verwalten

Alle Verwaltungsfunktionen befinden sich im **Plantmark-Tab der Seitenleiste**:

- **Pflanze hinzufügen** – Name, wissenschaftlicher Name, Gießintervall,
  Home-Assistant-Bereich, Bild, Wassersensor, Notizen und Giftigkeitswarnungen.
- **Bearbeiten** – alle Pflanzendaten sowie Bereich, Bild und Sensor ändern.
- **Jetzt gießen** – aktualisiert den letzten und nächsten Gießtermin sofort.
- **Löschen** – entfernt die Pflanze, das lokale Bild und ihre Entitäten.
- **Importieren** – übernimmt frühere Plantmark-Daten aus einer JSON-Liste oder
  einer API-Antwort im Format `{ "plants": [...] }`.
- **Einstellungen** – legt die standardmäßig erfasste Gießmenge fest.

Im Pflanzendialog kann der allgemeine Gießzeitraum über einen frühesten und
spätesten Tag festgelegt werden. Optional lassen sich abweichende Zeiträume für
alle vier Jahreszeiten aktivieren. Plantmark verwendet meteorologische
Jahreszeiten der Nordhalbkugel: Frühling März–Mai, Sommer Juni–August, Herbst
September–November und Winter Dezember–Februar.

Für die feuchtigkeitsabhängige Steuerung zeigt Plantmark nur Sensoren mit der
Home-Assistant-Geräteklasse `moisture` oder eindeutig pflanzenbezogene
Prozent-/Feuchtesensoren an. Ist der Sensor beim Beginn des Gießzeitraums noch
oberhalb des eingestellten Grenzwerts, wird das gesamte Fenster um die
konfigurierte Anzahl Tage verschoben. Die Prüfung erfolgt spätestens alle 15
Minuten.

Gießerinnerungen werden einmal je Gießfenster versendet. Als Ziel stehen die
Home-Assistant-Benachrichtigungszentrale, moderne `notify`-Entitäten und
vorhandene klassische Notify-Dienste zur Verfügung. Plantmark benötigt dafür
keinen externen Benachrichtigungsdienst; Pushover oder die Companion App können
verwendet werden, wenn sie bereits in Home Assistant eingerichtet sind. Eine
persistente Home-Assistant-Erinnerung wird beim Erfassen des Gießens automatisch
geschlossen.

Der Gerätebereich von Home Assistant zeigt weiterhin die erzeugten Entitäten,
ist aber nicht mehr für die Plantmark-Verwaltung erforderlich.

## Optionale Perenual-Pflanzendatenbank

Plantmark funktioniert vollständig ohne Cloud-Dienst. Für die automatische
Pflanzensuche kann zusätzlich ein persönlicher Perenual-API-Key eingerichtet
werden:

1. Erstelle bei [Perenual](https://www.perenual.com/docs/api) einen eigenen
   API-Key.
2. Öffne in der Plantmark-Seitenleiste **Einstellungen**.
3. Trage den Schlüssel unter **Perenual-Pflanzendatenbank** ein.
4. Öffne **Pflanze hinzufügen** oder bearbeite eine vorhandene Pflanze.
5. Suche nach einem allgemeinen oder wissenschaftlichen Pflanzennamen und
   wähle **Daten übernehmen**.

Der API-Key wird ausschließlich im Home-Assistant-Konfigurationseintrag
gespeichert und niemals an die Plantmark-Browseroberfläche zurückgesendet. Die
Suche wird nur auf ausdrückliche Benutzeraktion ausgeführt. Suchergebnisse
werden 30 Minuten, Pflanzendetails 24 Stunden im Arbeitsspeicher
zwischengespeichert. Bereich, Wassersensor, Notizen und lokal hochgeladene
Bilder bleiben bei der Datenübernahme erhalten. Von Perenual gelieferte Bilder
werden zusammen mit der vorhandenen Lizenzangabe angezeigt.

## Veröffentlichen

Vor der öffentlichen Veröffentlichung müssen in
`custom_components/plantmark/manifest.json` die Felder `documentation`,
`issue_tracker` und `codeowners` an dein GitHub-Repository angepasst werden.

Das Repository enthält:

- `hacs.json` für Marketplace/HACS
- Hassfest- und HACS-Validierung unter `.github/workflows/validate.yml`
- automatische GitHub-Releases für Tags wie `v1.0.0`
- lokale Brand-Grafik unter `custom_components/plantmark/brand/icon.png`
- MIT-Lizenz und Changelog

## Voraussetzungen

- Home Assistant 2025.8 oder neuer
- Marketplace/HACS für die Installation aus einem benutzerdefinierten Repository

## Datenschutz

Ohne die optionale Perenual-Anbindung arbeitet Plantmark vollständig lokal.
Hochgeladene Pflanzenbilder werden unter `www/plantmark` innerhalb deiner
Home-Assistant-Konfiguration gespeichert. Wie andere Dateien aus dem
Home-Assistant-`www`-Verzeichnis werden sie über eine lokale statische URL
bereitgestellt. Wenn die optionale Perenual-Anbindung aktiviert ist, werden nur
vom Benutzer eingegebene Pflanzensuchbegriffe und ausgewählte Pflanzen-IDs an
Perenual übertragen. Zur Anzeige eines übernommenen API-Bilds lädt der Browser
außerdem die von Perenual bereitgestellte externe Bild-URL. Es werden keine
Home-Assistant-Geräte-, Bereichs- oder Sensordaten übermittelt.

