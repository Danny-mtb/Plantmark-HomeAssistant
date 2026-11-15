# Plantmark for Home Assistant

Plantmark is a native Home Assistant integration for managing and caring for
houseplants. It does not require a separate Docker container, database, or cloud
service. Plant data is stored in the Home Assistant config entry and managed
from a responsive Plantmark page in the Home Assistant sidebar.

## Features

- Dedicated Plantmark sidebar page with plant images, watering schedules,
  warnings, care information, and live sensor values.
- Add, edit, water, and delete plants without using the device page.
- Upload JPEG, PNG, or WebP images. Images are resized in the browser and stored
  locally in Home Assistant.
- Assign a native Home Assistant area to each plant and keep the plant device's
  area synchronized.
- Assign an optional water or soil-moisture sensor with a live value display.
- Filter the sensor selector to relevant moisture sensors.
- Postpone a watering window automatically while the configured sensor reports
  sufficient soil moisture.
- Configure watering windows such as 7–10 days and optional individual windows
  for spring, summer, autumn, and winter.
- Display all upcoming watering windows in a shared Home Assistant calendar.
- Configure watering reminders centrally for all plants, using one Home
  Assistant notification target.
- Send reminders through persistent notifications, modern `notify` entities,
  or existing `notify.*` services such as Pushover.
- Search the optional Perenual plant database and import names, care data,
  toxicity, descriptions, and images when available for the configured plan.
- Open every Perenual search result directly on its public plant page.
- Represent every plant as a Home Assistant device with native sensors, binary
  sensors, and a watering button for dashboards and automations.
- Import plants from legacy Plantmark JSON.
- German and English user interfaces with privacy-aware diagnostics.

## Installation with HACS

Plantmark can be installed from its GitHub URL without submitting it to the
default HACS repository list:

1. Open **HACS → Integrations**.
2. Open the three-dot menu and select **Custom repositories**.
3. Add this GitHub repository URL and select **Integration** as the category.
4. Install **Plantmark**.
5. Restart Home Assistant.
6. Open **Settings → Devices & services → Add integration** and select
   **Plantmark**.
7. Open the new **Plantmark** entry in the sidebar and add your first plant.

After every Plantmark update, restart Home Assistant. The sidebar module uses a
content-based version identifier, so browsers load the new interface instead of
an older cached copy.

For a manual installation, copy `custom_components/plantmark` to
`<home-assistant-config>/custom_components/plantmark` and restart Home
Assistant.

## Managing plants

All normal management is available from the Plantmark sidebar page:

- **Add plant** — configure the name, scientific name, watering window, area,
  image, moisture sensor, notes, and toxicity warnings.
- **Edit** — update all plant-specific information.
- **Water now** — record a watering event and calculate the next window.
- **Delete** — remove the plant, its local image, device, and entities.
- **Import** — import a JSON list or an old response containing a top-level
  `plants` list.
- **Settings** — configure the default watering amount, central reminders, the
  notification target, and the optional Perenual API key.

Watering windows use an earliest and latest day. Seasonal watering can provide
different windows for all four meteorological seasons in the Northern
Hemisphere: spring is March–May, summer is June–August, autumn is
September–November, and winter is December–February.

For moisture-based scheduling, Plantmark lists sensors with the Home Assistant
`moisture` device class and clearly plant-related percentage or humidity
sensors. If the sensor is still above the configured threshold when the
watering window begins, Plantmark shifts the complete window by the configured
number of days. The condition is checked at least every 15 minutes.

## Central watering reminders

Watering reminders are configured once under **Plantmark → Settings**. The
switch and selected notification target apply to every plant. Each due plant
sends one reminder per watering window.

Available targets include Home Assistant persistent notifications, modern
`notify` entities, and existing legacy notify services. External services such
as Pushover or the Home Assistant Companion App can be used when they are
already configured in Home Assistant. Recording a watering event automatically
dismisses the corresponding persistent notification.

When upgrading from a version with per-plant reminders, Plantmark temporarily
uses the first enabled legacy reminder and its target as the central setting.
Saving the central settings removes the obsolete per-plant reminder fields.

## Optional Perenual plant database

Plantmark works without any cloud service. A personal Perenual API key can be
added for plant search and care-data enrichment:

1. Create an API key in the [Perenual API documentation](https://www.perenual.com/docs/api).
2. Open **Plantmark → Settings**.
3. Enter the key under **Perenual plant database**.
4. Add or edit a plant.
5. Search by common or scientific name and select **Apply data**.

The API key remains in the Home Assistant config entry and is never returned to
the browser. Searches run only after an explicit user action. Search results are
cached for 30 minutes and details for 24 hours in memory.

Areas, sensors, notes, and locally uploaded images are preserved when API data
is applied. Perenual images are downloaded through Home Assistant, validated,
and stored under `www/plantmark` with the available license attribution.

Plantmark imports all useful fields supplied by Perenual, including watering,
light, soil, origin, maintenance, growth, hardiness, flowering, propagation,
edibility, and toxicity. Toxicity is never guessed. If only a broad watering
category is available, Plantmark creates a visibly marked estimated range.

The Perenual Personal plan currently limits species details and care guides to
IDs 1–3000. For restricted results, Plantmark attempts the following sources in
order:

1. species details by ID;
2. care guide by ID;
3. care guide by scientific or common name;
4. the selected public Perenual species page;
5. basic search-result data.

An explicit phrase such as “every 7–10 days” is converted into a 7–10 day
watering window. Plantmark reports when Perenual did not provide a care guide,
so missing data is not presented as a successful full import.

## Entities

Plantmark creates native Home Assistant entities for each plant, including:

- last watered date;
- beginning and end of the next watering window;
- minimum and maximum watering interval;
- remaining days and active season;
- last recorded watering amount;
- watering-due and pet-toxicity binary sensors;
- a native **Water** button.

The device page remains available for automations and dashboards, but it is not
required for Plantmark management.

## Repository and releases

The repository includes:

- `hacs.json` for installation as a custom HACS repository;
- Hassfest and HACS validation in `.github/workflows/validate.yml`;
- automated GitHub releases for tags such as `v1.4.0`;
- local brand artwork under `custom_components/plantmark/brand`;
- an MIT license and changelog.

Before publishing a fork, update `documentation`, `issue_tracker`, and
`codeowners` in `custom_components/plantmark/manifest.json`.

## Requirements

- Home Assistant 2025.8 or newer
- HACS for installation from a custom GitHub repository

## Privacy

Without Perenual, Plantmark operates entirely within Home Assistant. Uploaded
images are stored under `www/plantmark` in the Home Assistant configuration.
Like other files in the Home Assistant `www` directory, they are available from
a local static URL.

When Perenual is enabled, only user-entered search terms, selected species IDs,
and the related public Perenual page are requested from Perenual. Plantmark does
not transmit Home Assistant devices, areas, sensors, or plant notes.
