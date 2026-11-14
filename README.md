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
- Jede Pflanze wird weiterhin als eigenes Home-Assistant-Gerät mit nativen
  Entitäten für Automationen angelegt.
- Sensoren für das letzte und nächste Gießen, Gießintervall, verbleibende Tage,
  Saison und letzte Gießmenge.
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

Der Gerätebereich von Home Assistant zeigt weiterhin die erzeugten Entitäten,
ist aber nicht mehr für die Plantmark-Verwaltung erforderlich.

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

Plantmark arbeitet vollständig lokal. Es werden keine Daten an externe Dienste
übertragen. Hochgeladene Pflanzenbilder werden unter `www/plantmark` innerhalb
deiner Home-Assistant-Konfiguration gespeichert. Wie andere Dateien aus dem
Home-Assistant-`www`-Verzeichnis werden sie über eine lokale statische URL
bereitgestellt.

