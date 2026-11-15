# Changelog

All notable changes to the Plantmark Home Assistant integration are documented
in this file.

## 1.4.0 - 2026-11-15

- Move watering reminders from individual plants to one central Plantmark
  switch and notification target in the sidebar settings.
- Migrate an existing enabled per-plant reminder and target automatically until
  the central settings are saved, then remove the obsolete per-plant fields.
- Rewrite the complete README in English.

## 1.3.3 - 2026-11-15

- Retry Perenual's official care-guide API by scientific or common plant name
  when the selected v2 species ID is outside the account's accessible range.
- Report clearly when neither the ID, name search nor public page provides a
  care guide instead of silently claiming that all care data was imported.

## 1.3.2 - 2026-11-15

- Fall back to the public Perenual species page when the account cannot access
  the separate care-guide API, then import its watering, sunlight and pruning
  guidance and explicit watering interval.

## 1.3.1 - 2026-11-15

- Load Perenual's separate plant-care guide, display its watering, sunlight and
  pruning texts, and apply explicit intervals such as "every 7-10 days" to the
  Plantmark watering window.

## 1.3.0 - 2026-11-15

- Import and retain substantially more Perenual care data, including growth,
  maintenance, hardiness, flowering, propagation, edible and tolerance fields.
- Derive a clearly marked watering-window estimate from the broad watering
  category when a plan-restricted search result has no detailed benchmark.
- Add a direct link from every search result to its Perenual plant page.
- Follow Perenual image-cloud redirects and detect image formats by content so
  actual API thumbnails replace the generic search icon.
- Continue to import pet toxicity only when Perenual explicitly supplies it.

## 1.2.3 - 2026-11-15

- Publish the Perenual image proxy, local API-image storage and free-plan detail
  fallback under a new version after the `v1.2.2` tag accidentally referenced
  the previous `1.2.1` commit.

## 1.2.2 - 2026-11-15

- Load trusted Perenual thumbnails through the Home Assistant backend so search
  images work with the frontend content-security policy.
- Store an applied Perenual image locally in Home Assistant while retaining its
  license attribution.
- Fall back to the basic species information returned by search when Perenual
  blocks detail data because of plan or request limits.

## 1.2.1 - 2026-11-14

- Add content-based cache busting for the Plantmark sidebar module so Home
  Assistant browsers immediately load the API, watering-window, moisture and
  notification controls delivered by an updated integration.

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

