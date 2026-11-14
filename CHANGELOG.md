# Changelog

All notable changes to the Plantmark Home Assistant integration are documented
in this file.

## 1.2.0 - 2026-11-14

- Add an optional Perenual plant database integration using each user's own API
  key stored in the Home Assistant config entry and redacted from diagnostics.
- Add plant search and selective import of botanical names, watering guidance,
  sunlight, soil, origin, care level, toxicity, descriptions and images.
- Cache searches and plant details locally to reduce API usage and handle
  invalid keys, rate limits and temporary network failures safely.
- Preserve areas, sensors, notes and locally uploaded images when enriching an
  existing plant, and display source image licensing where available.
- Add watering windows with minimum and maximum days plus separate spring,
  summer, autumn and winter schedules.
- Filter the plant sensor selector to relevant soil-moisture sensors and
  optionally postpone a due watering window while the configured sensor remains
  above its moisture threshold.
- Add one-time watering reminders using Home Assistant persistent notifications,
  notify entities or existing legacy notify services such as Pushover.
- Show watering windows in the calendar with a watering icon and localized
  event titles.

## 1.1.0 - 2026-11-14

- Add a responsive Plantmark sidebar panel for viewing and managing all plants.
- Add direct local JPEG, PNG and WebP image uploads with automatic browser-side
  resizing.
- Add native Home Assistant area assignment and keep the plant device area in
  sync.
- Add optional water or soil-moisture sensor assignment with its live state in
  the plant overview.
- Add plant creation, editing, deletion, watering, JSON import and global
  settings directly to the sidebar panel.

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

