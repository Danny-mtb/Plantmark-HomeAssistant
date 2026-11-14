# Changelog

All notable changes to the Plantmark Home Assistant integration are documented
in this file.

## 1.0.2 - 2026-11-14

- Fix the sensor platform failing to import because the active watering interval
  helper was referenced before it was defined.

## 1.0.1 - 2026-11-14

- Fix the setup and plant forms returning HTTP 500 because Home Assistant could
  not serialize their custom lambda validators.

## 1.0.0 - 2026-11-14

- Rebuild Plantmark as a standalone, Marketplace/HACS-compatible Home Assistant
  integration without Docker, a database or an external API.
- Store and manage plants through the Home Assistant config entry and options UI.
- Represent every plant as a Home Assistant device with watering, interval,
  season, due-date, watering-amount and pet-toxicity entities.
- Add native watering buttons and a combined watering calendar.
- Add import support for legacy Plantmark JSON data.
- Add German and English translations, privacy-aware diagnostics, brand artwork,
  validation workflows and automated GitHub releases.

