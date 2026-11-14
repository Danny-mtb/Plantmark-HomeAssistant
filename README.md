# Plantmark for Home Assistant

Plantmark ist eine vollständig native Home-Assistant-Integration zur Verwaltung
und Pflege von Zimmerpflanzen. Sie benötigt keinen separaten Docker-Container,
keine Datenbank und keinen Cloud-Dienst. Alle Pflanzendaten werden im
Home-Assistant-Konfigurationseintrag gespeichert.

## Funktionen

- Jede Pflanze wird als eigenes Home-Assistant-Gerät angelegt.
- Pflanzen lassen sich direkt über **Einstellungen → Geräte & Dienste →
  Plantmark → Konfigurieren** hinzufügen, bearbeiten und entfernen.
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
6. Öffne anschließend **Konfigurieren**, um die erste Pflanze hinzuzufügen.

Für eine manuelle Installation kopierst du
`custom_components/plantmark` nach
`<home-assistant-config>/custom_components/plantmark` und startest Home
Assistant neu.

## Pflanzen verwalten

Unter **Plantmark → Konfigurieren** stehen folgende Aktionen bereit:

- **Pflanze hinzufügen** – legt ein neues Gerät samt Entitäten an.
- **Pflanze bearbeiten** – ändert Name, Standort, Bild, Intervall und Warnungen.
- **Pflanze entfernen** – entfernt Pflanze und Entitäten.
- **Pflanzen aus JSON importieren** – übernimmt frühere Plantmark-Daten.
- **Einstellungen** – legt die standardmäßig erfasste Gießmenge fest.

Nach Änderungen lädt Home Assistant die Integration automatisch neu. Beim
Drücken des Gießen-Buttons werden `last_watered` und `next_watering` sofort
aktualisiert und dauerhaft im Konfigurationseintrag gespeichert.

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
übertragen. Externe Bild-URLs werden nur dann durch Home Assistant bzw. den
Browser geladen, wenn du selbst eine solche URL bei einer Pflanze hinterlegst.

