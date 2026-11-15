const TEXT = {
  de: {
    title: "Meine Pflanzen",
    subtitle: "Pflege, Bilder und Sensoren an einem Ort",
    add: "Pflanze hinzufügen",
    import: "Importieren",
    settings: "Einstellungen",
    total: "Pflanzen",
    due: "Gießen fällig",
    sensors: "Sensoren verbunden",
    emptyTitle: "Noch keine Pflanzen",
    emptyText: "Lege deine erste Pflanze an und Plantmark erinnert dich ans Gießen.",
    edit: "Bearbeiten",
    delete: "Löschen",
    water: "Jetzt gießen",
    watering: "Wird gespeichert …",
    lastWatered: "Zuletzt gegossen",
    nextWatering: "Nächstes Gießen",
    interval: "Gießintervall",
    days: "Tage",
    area: "Bereich",
    noArea: "Kein Bereich",
    waterSensor: "Wassersensor / Bodenfeuchte",
    noSensor: "Kein Sensor",
    unavailable: "Nicht verfügbar",
    notes: "Notizen",
    toxicCats: "Giftig für Katzen",
    toxicDogs: "Giftig für Hunde",
    plantName: "Name",
    scientificName: "Wissenschaftlicher Name",
    image: "Pflanzenbild",
    imageHelp: "JPEG, PNG oder WebP. Das Bild wird lokal in Home Assistant gespeichert.",
    removeImage: "Vorhandenes Bild entfernen",
    save: "Speichern",
    cancel: "Abbrechen",
    addTitle: "Pflanze hinzufügen",
    editTitle: "Pflanze bearbeiten",
    confirmDelete: "Diese Pflanze und ihre Home-Assistant-Entitäten wirklich löschen?",
    saved: "Pflanze gespeichert",
    deleted: "Pflanze gelöscht",
    watered: "Gießen wurde gespeichert",
    loadError: "Plantmark konnte nicht geladen werden",
    saveError: "Änderung konnte nicht gespeichert werden",
    importTitle: "Pflanzen importieren",
    importHelp: "Füge eine JSON-Liste oder eine alte Plantmark-Antwort mit einem plants-Feld ein.",
    importData: "Plantmark-JSON",
    imported: "Pflanzen wurden importiert",
    settingsTitle: "Plantmark-Einstellungen",
    defaultAmount: "Standard-Gießmenge (ml)",
    amountHelp: "0 bedeutet, dass keine Gießmenge gespeichert wird.",
    settingsSaved: "Einstellungen gespeichert",
    required: "Bitte gib einen Namen ein.",
    sensorState: "Sensorwert",
    today: "Heute",
    overdue: "Überfällig",
    database: "Pflanzendatenbank",
    databaseSearch: "Pflanze bei Perenual suchen",
    databasePlaceholder: "z. B. Monstera oder Monstera deliciosa",
    search: "Suchen",
    searching: "Suche läuft …",
    noResults: "Keine passenden Pflanzen gefunden.",
    applyData: "Daten übernehmen",
    openDatabaseEntry: "Pflanzenseite öffnen",
    dataApplied: "Pflegedaten wurden übernommen",
    basicDataApplied: "Basisdaten wurden übernommen. Perenual stellt die Detaildaten für diese Pflanze in deinem Tarif nicht bereit.",
    paidDetails: "Detaildaten eventuell nur mit kostenpflichtigem Perenual-Tarif",
    apiNotConfigured: "Hinterlege zuerst deinen persönlichen Perenual-API-Key in den Einstellungen.",
    openSettings: "API einrichten",
    providedBy: "Daten von Perenual",
    light: "Licht",
    soil: "Erde",
    careLevel: "Pflege",
    origin: "Herkunft",
    family: "Familie",
    apiDescription: "Pflegeinformationen",
    estimatedInterval: "Geschätzter Gießzeitraum",
    growthRate: "Wachstum",
    maintenance: "Pflegeaufwand",
    hardiness: "Winterhärtezone",
    propagation: "Vermehrung",
    floweringSeason: "Blütezeit",
    pests: "Anfällig für",
    dimensions: "Größe",
    attracts: "Zieht an",
    wateringPeriod: "Gießzeitpunkt",
    wateringQuality: "Wasserqualität",
    temperature: "Temperatur",
    phLevel: "pH-Wert",
    perenualTitle: "Perenual-Pflanzendatenbank",
    perenualDescription: "Optional: Suche Pflanzen und übernimm Pflegeinformationen automatisch. Der API-Key bleibt in Home Assistant.",
    perenualKey: "Persönlicher Perenual-API-Key",
    perenualKeyHelp: "Ein leeres Feld lässt den vorhandenen Schlüssel unverändert.",
    perenualConfigured: "API ist eingerichtet",
    perenualMissing: "API ist nicht eingerichtet",
    removePerenualKey: "Gespeicherten API-Key entfernen",
    getApiKey: "API-Key bei Perenual erhalten",
    intervalMin: "Frühestens nach",
    intervalMax: "Spätestens nach",
    seasonalWatering: "Unterschiedliche Gießzeiträume nach Jahreszeit",
    seasonalHelp: "Plantmark verwendet automatisch die aktuell passende Jahreszeit.",
    spring: "Frühling",
    summer: "Sommer",
    autumn: "Herbst",
    winter: "Winter",
    from: "von",
    to: "bis",
    moistureControl: "Gießzeitraum anhand der Feuchtigkeit verschieben",
    moistureThreshold: "Feucht genug ab",
    moistureDelay: "Bei ausreichender Feuchte verschieben um",
    moistureHelp: "Nur passende Bodenfeuchte- und Feuchtigkeitssensoren werden angezeigt.",
    reminder: "Gießerinnerung aktivieren",
    notificationTarget: "Benachrichtigung senden an",
    notificationHelp: "Verwendet ausschließlich Home-Assistant-Benachrichtigungen und vorhandene Notify-Integrationen.",
    selectNotification: "Benachrichtigungsziel auswählen",
    wateringWindow: "Gießzeitraum",
  },
  en: {
    title: "My plants",
    subtitle: "Care, images and sensors in one place",
    add: "Add plant",
    import: "Import",
    settings: "Settings",
    total: "Plants",
    due: "Watering due",
    sensors: "Sensors connected",
    emptyTitle: "No plants yet",
    emptyText: "Add your first plant and Plantmark will track its watering schedule.",
    edit: "Edit",
    delete: "Delete",
    water: "Water now",
    watering: "Saving …",
    lastWatered: "Last watered",
    nextWatering: "Next watering",
    interval: "Watering interval",
    days: "days",
    area: "Area",
    noArea: "No area",
    waterSensor: "Water sensor / soil moisture",
    noSensor: "No sensor",
    unavailable: "Unavailable",
    notes: "Notes",
    toxicCats: "Toxic to cats",
    toxicDogs: "Toxic to dogs",
    plantName: "Name",
    scientificName: "Scientific name",
    image: "Plant image",
    imageHelp: "JPEG, PNG or WebP. The image is stored locally in Home Assistant.",
    removeImage: "Remove existing image",
    save: "Save",
    cancel: "Cancel",
    addTitle: "Add plant",
    editTitle: "Edit plant",
    confirmDelete: "Really delete this plant and its Home Assistant entities?",
    saved: "Plant saved",
    deleted: "Plant deleted",
    watered: "Watering saved",
    loadError: "Plantmark could not be loaded",
    saveError: "The change could not be saved",
    importTitle: "Import plants",
    importHelp: "Paste a JSON list or a legacy Plantmark response containing a plants field.",
    importData: "Plantmark JSON",
    imported: "Plants imported",
    settingsTitle: "Plantmark settings",
    defaultAmount: "Default watering amount (ml)",
    amountHelp: "Use 0 if no watering amount should be stored.",
    settingsSaved: "Settings saved",
    required: "Please enter a name.",
    sensorState: "Sensor value",
    today: "Today",
    overdue: "Overdue",
    database: "Plant database",
    databaseSearch: "Search Perenual for a plant",
    databasePlaceholder: "e.g. Monstera or Monstera deliciosa",
    search: "Search",
    searching: "Searching …",
    noResults: "No matching plants found.",
    applyData: "Apply data",
    openDatabaseEntry: "Open plant page",
    dataApplied: "Plant care data applied",
    basicDataApplied: "Basic data was applied. Perenual does not provide this plant's details with your current plan.",
    paidDetails: "Details may require a paid Perenual plan",
    apiNotConfigured: "First add your personal Perenual API key in settings.",
    openSettings: "Configure API",
    providedBy: "Data from Perenual",
    light: "Light",
    soil: "Soil",
    careLevel: "Care",
    origin: "Origin",
    family: "Family",
    apiDescription: "Care information",
    estimatedInterval: "Estimated watering window",
    growthRate: "Growth",
    maintenance: "Maintenance",
    hardiness: "Hardiness zone",
    propagation: "Propagation",
    floweringSeason: "Flowering season",
    pests: "Susceptible to",
    dimensions: "Size",
    attracts: "Attracts",
    wateringPeriod: "Watering period",
    wateringQuality: "Water quality",
    temperature: "Temperature",
    phLevel: "pH level",
    perenualTitle: "Perenual plant database",
    perenualDescription: "Optional: Search plants and automatically apply care information. The API key stays in Home Assistant.",
    perenualKey: "Personal Perenual API key",
    perenualKeyHelp: "Leave this empty to keep the existing key unchanged.",
    perenualConfigured: "API is configured",
    perenualMissing: "API is not configured",
    removePerenualKey: "Remove the stored API key",
    getApiKey: "Get an API key from Perenual",
    intervalMin: "Earliest after",
    intervalMax: "Latest after",
    seasonalWatering: "Use different watering windows by season",
    seasonalHelp: "Plantmark automatically uses the currently active season.",
    spring: "Spring",
    summer: "Summer",
    autumn: "Autumn",
    winter: "Winter",
    from: "from",
    to: "to",
    moistureControl: "Postpone watering based on moisture",
    moistureThreshold: "Moist enough from",
    moistureDelay: "When moist, postpone by",
    moistureHelp: "Only matching soil-moisture and humidity sensors are shown.",
    reminder: "Enable watering reminder",
    notificationTarget: "Send notification to",
    notificationHelp: "Uses only Home Assistant notifications and configured notify integrations.",
    selectNotification: "Select notification target",
    wateringWindow: "Watering window",
  },
};

const escapeHtml = (value) =>
  String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

class PlantmarkPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._loaded = false;
    this._loading = false;
    this._data = { plants: [], areas: [], settings: {} };
    this._modal = null;
    this._pendingImage = null;
    this._pendingImageSource = null;
    this._apiResults = null;
    this._apiQuery = "";
    this._apiLoading = false;
    this._toastTimer = null;
  }

  set hass(value) {
    this._hass = value;
    if (this.isConnected && !this._loaded && !this._loading) this._load();
    if (this._loaded) this._updateSensorValues();
  }

  set panel(value) {
    this._panel = value;
  }

  connectedCallback() {
    if (this._hass && !this._loaded && !this._loading) this._load();
    else this._render();
  }

  get _language() {
    return String(this._hass?.language || "en").toLowerCase().startsWith("de")
      ? "de"
      : "en";
  }

  get _t() {
    return TEXT[this._language];
  }

  async _load() {
    this._loading = true;
    this._render();
    try {
      this._data = await this._hass.callWS({ type: "plantmark/list" });
      this._loaded = true;
    } catch (error) {
      this._error = error?.message || this._t.loadError;
    } finally {
      this._loading = false;
      this._render();
    }
  }

  _render() {
    if (!this.shadowRoot) return;
    const t = this._t;
    const plants = this._data.plants || [];
    const due = plants.filter((plant) => this._isDue(plant)).length;
    const sensors = plants.filter((plant) => plant.water_sensor_entity_id).length;

    this.shadowRoot.innerHTML = `
      <style>${this._styles()}</style>
      <div class="page">
        <header>
          <div class="heading">
            <div class="brand"><ha-icon icon="mdi:sprout"></ha-icon></div>
            <div><h1>${t.title}</h1><p>${t.subtitle}</p></div>
          </div>
          <div class="header-actions">
            <button class="secondary" id="import"><ha-icon icon="mdi:database-import-outline"></ha-icon>${t.import}</button>
            <button class="secondary" id="settings"><ha-icon icon="mdi:cog-outline"></ha-icon>${t.settings}</button>
            <button class="primary" id="add"><ha-icon icon="mdi:plus"></ha-icon>${t.add}</button>
          </div>
        </header>
        ${this._error ? `<div class="error"><ha-icon icon="mdi:alert-circle"></ha-icon>${escapeHtml(this._error)}</div>` : ""}
        ${this._loading ? `<div class="loading"><div class="spinner"></div></div>` : `
          <section class="stats">
            ${this._stat("mdi:sprout", plants.length, t.total, "green")}
            ${this._stat("mdi:watering-can", due, t.due, due ? "blue active" : "blue")}
            ${this._stat("mdi:access-point", sensors, t.sensors, "purple")}
          </section>
          ${plants.length ? `<main class="grid">${plants.map((plant) => this._plantCard(plant)).join("")}</main>` : this._emptyState()}
        `}
      </div>
      <div id="modal-root">${this._modalHtml()}</div>
      <div class="toast" id="toast"></div>
    `;
    this._bindEvents();
  }

  _stat(icon, value, label, color) {
    return `<article class="stat"><span class="stat-icon ${color}"><ha-icon icon="${icon}"></ha-icon></span><div><strong>${value}</strong><span>${label}</span></div></article>`;
  }

  _emptyState() {
    const t = this._t;
    return `<section class="empty"><div class="empty-icon"><ha-icon icon="mdi:flower-outline"></ha-icon></div><h2>${t.emptyTitle}</h2><p>${t.emptyText}</p><button class="primary" id="empty-add"><ha-icon icon="mdi:plus"></ha-icon>${t.add}</button></section>`;
  }

  _plantCard(plant) {
    const t = this._t;
    const area = this._data.areas.find((item) => item.id === plant.area_id);
    const sensor = this._sensorInfo(plant.water_sensor_entity_id);
    const due = this._isDue(plant);
    const dateClass = due ? "due" : "";
    const [intervalMin, intervalMax] = this._wateringRange(plant);
    const intervalText = intervalMin === intervalMax ? `${intervalMin} ${t.days}` : `${intervalMin}–${intervalMax} ${t.days}`;
    const image = plant.image_url
      ? `<img src="${escapeHtml(plant.image_url)}" alt="${escapeHtml(plant.name)}" loading="lazy">`
      : `<div class="image-placeholder"><ha-icon icon="mdi:flower-tulip-outline"></ha-icon></div>`;
    const warnings = [
      plant.is_toxic_to_cats ? `<span class="warning"><ha-icon icon="mdi:cat"></ha-icon>${t.toxicCats}</span>` : "",
      plant.is_toxic_to_dogs ? `<span class="warning"><ha-icon icon="mdi:dog"></ha-icon>${t.toxicDogs}</span>` : "",
    ].filter(Boolean).join("");
    const careFacts = this._careFacts(plant);
    const licenseUrl = /^https?:\/\//i.test(plant.image_license_url || "")
      ? plant.image_license_url
      : null;
    const attribution = plant.image_license_name
      ? `<span class="image-attribution">${licenseUrl ? `<a href="${escapeHtml(licenseUrl)}" target="_blank" rel="noreferrer">${escapeHtml(plant.image_license_name)}</a>` : escapeHtml(plant.image_license_name)}</span>`
      : "";

    return `
      <article class="plant-card" data-plant-id="${escapeHtml(plant.id)}">
        <div class="plant-image">${image}<span class="area-chip"><ha-icon icon="mdi:map-marker-outline"></ha-icon>${escapeHtml(area?.name || t.noArea)}</span>${attribution}</div>
        <div class="plant-content">
          <div class="plant-title"><div><h2>${escapeHtml(plant.name)}</h2>${plant.scientific_name ? `<em>${escapeHtml(plant.scientific_name)}</em>` : ""}</div><button class="icon-button edit" title="${t.edit}"><ha-icon icon="mdi:pencil-outline"></ha-icon></button></div>
          <div class="schedule">
            <div><span>${t.lastWatered}</span><strong>${this._formatDate(plant.last_watered)}</strong></div>
            <div class="${dateClass}"><span>${t.wateringWindow}</span><strong>${this._formatDateRange(plant.next_watering, plant.next_watering_end)}</strong></div>
            <div><span>${t.interval}</span><strong>${intervalText}</strong></div>
          </div>
          ${plant.water_sensor_entity_id ? `<div class="sensor-row"><span class="sensor-icon"><ha-icon icon="mdi:water-percent"></ha-icon></span><div><span>${escapeHtml(sensor.name)}</span><strong data-sensor="${escapeHtml(plant.water_sensor_entity_id)}">${escapeHtml(sensor.value)}</strong></div></div>` : ""}
          ${careFacts ? `<div class="care-facts">${careFacts}</div>` : ""}
          ${warnings ? `<div class="warnings">${warnings}</div>` : ""}
          ${plant.description ? `<details class="api-description"><summary>${t.apiDescription}</summary><p>${escapeHtml(plant.description)}</p></details>` : ""}
          ${plant.notes ? `<p class="notes">${escapeHtml(plant.notes)}</p>` : ""}
          <div class="card-actions"><button class="water"><ha-icon icon="mdi:watering-can"></ha-icon>${t.water}</button><button class="danger delete" title="${t.delete}"><ha-icon icon="mdi:trash-can-outline"></ha-icon></button></div>
        </div>
      </article>`;
  }

  _modalHtml() {
    if (!this._modal) return "";
    if (this._modal.type === "plant") return this._plantForm(this._modal.plant);
    if (this._modal.type === "import") return this._importForm();
    if (this._modal.type === "settings") return this._settingsForm();
    return "";
  }

  _plantForm(plant) {
    const t = this._t;
    const isEdit = Boolean(plant?.id);
    const areaOptions = (this._data.areas || []).map((area) => `<option value="${escapeHtml(area.id)}" ${area.id === plant?.area_id ? "selected" : ""}>${escapeHtml(area.name)}</option>`).join("");
    const sensorOptions = this._sensorOptions(plant?.water_sensor_entity_id);
    const notificationOptions = this._notificationOptions(plant?.notification_target);
    const preview = this._pendingImage || plant?.image_url;
    const intervalMin = Number(plant?.watering_interval_min_days || plant?.watering_interval_days || 7);
    const intervalMax = Number(plant?.watering_interval_max_days || intervalMin);
    const seasonal = Boolean(plant?.seasonal_watering_enabled);
    const moistureControl = Boolean(plant?.moisture_control_enabled);
    const reminder = Boolean(plant?.watering_reminder_enabled);
    const seasonalFields = ["spring", "summer", "autumn", "winter"].map((season) => {
      const minimum = Number(plant?.[`watering_interval_${season}_min_days`] || intervalMin);
      const maximum = Number(plant?.[`watering_interval_${season}_max_days`] || intervalMax);
      return `<div class="season-row"><strong>${t[season]}</strong><label><span>${t.from}</span><input name="watering_interval_${season}_min_days" type="number" min="1" max="365" value="${minimum}"></label><label><span>${t.to}</span><input name="watering_interval_${season}_max_days" type="number" min="1" max="365" value="${maximum}"></label><span>${t.days}</span></div>`;
    }).join("");
    return `
      <div class="modal-backdrop"><section class="modal wide" role="dialog" aria-modal="true">
        <div class="modal-header"><div><h2>${isEdit ? t.editTitle : t.addTitle}</h2><p>${isEdit ? escapeHtml(plant.name) : t.subtitle}</p></div><button class="icon-button close"><ha-icon icon="mdi:close"></ha-icon></button></div>
        <form id="plant-form">
          <input type="hidden" name="id" value="${escapeHtml(plant?.id || "")}">
          ${this._apiSearchHtml(plant)}
          <div class="form-grid">
            <label class="field"><span>${t.plantName} *</span><input name="name" maxlength="255" required value="${escapeHtml(plant?.name || "")}"></label>
            <label class="field"><span>${t.scientificName}</span><input name="scientific_name" maxlength="255" value="${escapeHtml(plant?.scientific_name || "")}"></label>
            <label class="field"><span>${t.area}</span><select name="area_id"><option value="">${t.noArea}</option>${areaOptions}</select></label>
            <label class="field"><span>${t.waterSensor}</span><select name="water_sensor_entity_id"><option value="">${t.noSensor}</option>${sensorOptions}</select></label>
            <label class="field"><span>${t.intervalMin}</span><div class="number-suffix"><input name="watering_interval_min_days" type="number" min="1" max="365" required value="${intervalMin}"><span>${t.days}</span></div></label>
            <label class="field"><span>${t.intervalMax}</span><div class="number-suffix"><input name="watering_interval_max_days" type="number" min="1" max="365" required value="${intervalMax}"><span>${t.days}</span></div></label>
            <div class="field full advanced-block"><label class="check"><input id="seasonal-watering" name="seasonal_watering_enabled" type="checkbox" ${seasonal ? "checked" : ""}> ${t.seasonalWatering}</label><small>${t.seasonalHelp}</small><div class="season-grid" data-enabled-by="seasonal-watering">${seasonalFields}</div></div>
            <div class="field full advanced-block"><label class="check"><input id="moisture-control" name="moisture_control_enabled" type="checkbox" ${moistureControl ? "checked" : ""}> ${t.moistureControl}</label><small>${t.moistureHelp}</small><div class="conditional-grid" data-enabled-by="moisture-control"><label class="field"><span>${t.moistureThreshold}</span><div class="number-suffix"><input name="moisture_threshold_percent" type="number" min="0" max="100" value="${Number(plant?.moisture_threshold_percent ?? 35)}"><span>%</span></div></label><label class="field"><span>${t.moistureDelay}</span><div class="number-suffix"><input name="moisture_delay_days" type="number" min="1" max="30" value="${Number(plant?.moisture_delay_days || 1)}"><span>${t.days}</span></div></label></div></div>
            <div class="field full advanced-block"><label class="check"><input id="watering-reminder" name="watering_reminder_enabled" type="checkbox" ${reminder ? "checked" : ""}> ${t.reminder}</label><small>${t.notificationHelp}</small><div data-enabled-by="watering-reminder"><label class="field"><span>${t.notificationTarget}</span><select name="notification_target"><option value="">${t.selectNotification}</option>${notificationOptions}</select></label></div></div>
            <div class="field image-field"><span>${t.image}</span><div class="image-upload">${preview ? `<img id="image-preview" src="${escapeHtml(preview)}" alt="">` : `<div id="image-preview" class="mini-placeholder"><ha-icon icon="mdi:image-plus"></ha-icon></div>`}<label class="upload-button"><ha-icon icon="mdi:upload"></ha-icon>${t.image}<input id="image-input" type="file" accept="image/*"></label></div><small>${t.imageHelp}</small>${plant?.image_url ? `<label class="check"><input name="remove_image" type="checkbox"> ${t.removeImage}</label>` : ""}</div>
            <label class="field full"><span>${t.notes}</span><textarea name="notes" rows="3">${escapeHtml(plant?.notes || "")}</textarea></label>
            <div class="field full checks"><label class="check"><input name="is_toxic_to_cats" type="checkbox" ${plant?.is_toxic_to_cats ? "checked" : ""}> <ha-icon icon="mdi:cat"></ha-icon>${t.toxicCats}</label><label class="check"><input name="is_toxic_to_dogs" type="checkbox" ${plant?.is_toxic_to_dogs ? "checked" : ""}> <ha-icon icon="mdi:dog"></ha-icon>${t.toxicDogs}</label></div>
          </div>
          <div class="modal-actions"><button type="button" class="secondary close">${t.cancel}</button><button type="submit" class="primary"><ha-icon icon="mdi:content-save-outline"></ha-icon>${t.save}</button></div>
        </form>
      </section></div>`;
  }

  _apiSearchHtml(plant) {
    const t = this._t;
    if (!this._data.settings?.perenual_configured) {
      return `<section class="api-search-box"><div class="api-search-title"><ha-icon icon="mdi:database-search-outline"></ha-icon><div><strong>${t.database}</strong><span>${t.apiNotConfigured}</span></div></div><button type="button" class="secondary open-api-settings">${t.openSettings}</button></section>`;
    }
    const source = plant?.perenual_id
      ? `<span class="source-badge"><ha-icon icon="mdi:check-decagram"></ha-icon>${t.providedBy} · #${Number(plant.perenual_id)}</span>`
      : "";
    return `<section class="api-search-box"><div class="api-search-title"><ha-icon icon="mdi:database-search-outline"></ha-icon><div><strong>${t.databaseSearch}</strong>${source}</div></div><div class="api-search-row"><input id="api-query" value="${escapeHtml(this._apiQuery)}" placeholder="${t.databasePlaceholder}" maxlength="100"><button type="button" class="secondary" id="api-search" ${this._apiLoading ? "disabled" : ""}><ha-icon icon="mdi:magnify"></ha-icon>${this._apiLoading ? t.searching : t.search}</button></div>${this._apiResultsHtml()}</section>`;
  }

  _apiResultsHtml() {
    if (this._apiLoading) return `<div class="api-loading"><span class="small-spinner"></span>${this._t.searching}</div>`;
    if (!this._apiQuery || this._apiResults === null) return "";
    if (!this._apiResults.length) return `<p class="api-empty">${this._t.noResults}</p>`;
    return `<div class="api-results">${this._apiResults.map((result) => {
      const imageSource = result.image_data || null;
      const image = imageSource
        ? `<img src="${escapeHtml(imageSource)}" alt="">`
        : `<span class="api-result-placeholder"><ha-icon icon="mdi:sprout"></ha-icon></span>`;
      const planHint = Number(result.id) > 3000 ? this._t.paidDetails : null;
      const details = [result.scientific_name, result.watering, ...(result.sunlight || []).slice(0, 1), planHint].filter(Boolean).map(escapeHtml).join(" · ");
      const pageUrl = /^https:\/\/www\.perenual\.com\//.test(result.perenual_url || "")
        ? result.perenual_url
        : `https://www.perenual.com/plant-species-database-search-finder/species/${Number(result.id)}`;
      return `<article class="api-result">${image}<div class="api-result-copy"><strong>${escapeHtml(result.common_name || result.scientific_name || `#${result.id}`)}</strong><span>${details}</span></div><div class="api-result-actions"><a class="secondary api-page-link" href="${escapeHtml(pageUrl)}" target="_blank" rel="noreferrer" title="${this._t.openDatabaseEntry}" aria-label="${this._t.openDatabaseEntry}"><ha-icon icon="mdi:open-in-new"></ha-icon></a><button type="button" class="primary apply-api" data-species-id="${Number(result.id)}">${this._t.applyData}</button></div></article>`;
    }).join("")}</div>`;
  }

  _importForm() {
    const t = this._t;
    return `<div class="modal-backdrop"><section class="modal" role="dialog" aria-modal="true"><div class="modal-header"><div><h2>${t.importTitle}</h2><p>${t.importHelp}</p></div><button class="icon-button close"><ha-icon icon="mdi:close"></ha-icon></button></div><form id="import-form"><label class="field"><span>${t.importData}</span><textarea name="data" rows="12" required placeholder='[{"name": "Monstera", "watering_interval_days": 7}]'></textarea></label><div class="modal-actions"><button type="button" class="secondary close">${t.cancel}</button><button type="submit" class="primary"><ha-icon icon="mdi:database-import-outline"></ha-icon>${t.import}</button></div></form></section></div>`;
  }

  _settingsForm() {
    const t = this._t;
    const amount = Number(this._data.settings?.default_water_amount_ml || 0);
    const configured = Boolean(this._data.settings?.perenual_configured);
    return `<div class="modal-backdrop"><section class="modal" role="dialog" aria-modal="true"><div class="modal-header"><div><h2>${t.settingsTitle}</h2><p>${t.amountHelp}</p></div><button class="icon-button close"><ha-icon icon="mdi:close"></ha-icon></button></div><form id="settings-form"><label class="field"><span>${t.defaultAmount}</span><input name="amount" type="number" min="0" max="10000" value="${amount}" required></label><section class="api-settings"><div class="api-settings-heading"><div><h3>${t.perenualTitle}</h3><p>${t.perenualDescription}</p></div><span class="api-status ${configured ? "connected" : ""}"><ha-icon icon="${configured ? "mdi:check-circle" : "mdi:minus-circle-outline"}"></ha-icon>${configured ? t.perenualConfigured : t.perenualMissing}</span></div><label class="field"><span>${t.perenualKey}</span><input name="perenual_api_key" type="password" maxlength="512" autocomplete="off" placeholder="${configured ? "••••••••" : ""}"><small>${t.perenualKeyHelp} <a href="https://www.perenual.com/docs/api" target="_blank" rel="noreferrer">${t.getApiKey}</a></small></label>${configured ? `<label class="check remove-api"><input name="remove_perenual_api_key" type="checkbox"> ${t.removePerenualKey}</label>` : ""}</section><div class="modal-actions"><button type="button" class="secondary close">${t.cancel}</button><button type="submit" class="primary"><ha-icon icon="mdi:content-save-outline"></ha-icon>${t.save}</button></div></form></section></div>`;
  }

  _bindEvents() {
    this.shadowRoot.querySelector("#add")?.addEventListener("click", () => this._openPlant());
    this.shadowRoot.querySelector("#empty-add")?.addEventListener("click", () => this._openPlant());
    this.shadowRoot.querySelector("#import")?.addEventListener("click", () => this._openModal("import"));
    this.shadowRoot.querySelector("#settings")?.addEventListener("click", () => this._openModal("settings"));
    this.shadowRoot.querySelector(".open-api-settings")?.addEventListener("click", () => this._openModal("settings"));
    this.shadowRoot.querySelectorAll(".close").forEach((button) => button.addEventListener("click", () => this._closeModal()));
    this.shadowRoot.querySelector(".modal-backdrop")?.addEventListener("click", (event) => { if (event.target.classList.contains("modal-backdrop")) this._closeModal(); });
    this.shadowRoot.querySelectorAll(".plant-card").forEach((card) => {
      const id = card.dataset.plantId;
      card.querySelector(".edit")?.addEventListener("click", () => this._openPlant(id));
      card.querySelector(".delete")?.addEventListener("click", () => this._deletePlant(id));
      card.querySelector(".water")?.addEventListener("click", (event) => this._waterPlant(id, event.currentTarget));
    });
    this.shadowRoot.querySelector("#image-input")?.addEventListener("change", (event) => this._prepareImage(event.target.files?.[0]));
    this.shadowRoot.querySelector("#plant-form")?.addEventListener("submit", (event) => this._savePlant(event));
    this.shadowRoot.querySelector("#import-form")?.addEventListener("submit", (event) => this._importPlants(event));
    this.shadowRoot.querySelector("#settings-form")?.addEventListener("submit", (event) => this._saveSettings(event));
    this.shadowRoot.querySelector("#api-search")?.addEventListener("click", () => this._searchApi());
    this.shadowRoot.querySelector("#api-query")?.addEventListener("keydown", (event) => { if (event.key === "Enter") { event.preventDefault(); this._searchApi(); } });
    this.shadowRoot.querySelectorAll(".apply-api").forEach((button) => button.addEventListener("click", () => this._applyApi(Number(button.dataset.speciesId))));
    ["seasonal-watering", "moisture-control", "watering-reminder"].forEach((id) => this.shadowRoot.querySelector(`#${id}`)?.addEventListener("change", () => this._toggleConditionalFields()));
    this._toggleConditionalFields();
  }

  _toggleConditionalFields() {
    this.shadowRoot.querySelectorAll("[data-enabled-by]").forEach((section) => {
      const enabled = Boolean(this.shadowRoot.querySelector(`#${section.dataset.enabledBy}`)?.checked);
      section.classList.toggle("inactive", !enabled);
      section.setAttribute("aria-disabled", String(!enabled));
    });
  }

  _openPlant(id = null) {
    const source = id ? this._data.plants.find((plant) => String(plant.id) === String(id)) : null;
    this._pendingImage = null;
    this._pendingImageSource = null;
    this._apiResults = null;
    this._apiQuery = source?.scientific_name || source?.name || "";
    this._apiLoading = false;
    this._modal = { type: "plant", plant: source ? { ...source } : {} };
    this._render();
    queueMicrotask(() => this.shadowRoot.querySelector('input[name="name"]')?.focus());
  }

  _openModal(type) {
    this._pendingImage = null;
    this._pendingImageSource = null;
    this._apiResults = null;
    this._apiQuery = "";
    this._apiLoading = false;
    this._modal = { type };
    this._render();
  }

  _closeModal() {
    this._modal = null;
    this._pendingImage = null;
    this._pendingImageSource = null;
    this._apiResults = null;
    this._apiQuery = "";
    this._apiLoading = false;
    this._render();
  }

  _capturePlantForm() {
    const element = this.shadowRoot.querySelector("#plant-form");
    if (!element || this._modal?.type !== "plant") return;
    const form = new FormData(element);
    const intervalMin = Number(form.get("watering_interval_min_days")) || 7;
    Object.assign(this._modal.plant, {
      id: form.get("id") || undefined,
      name: String(form.get("name") || "").trim(),
      scientific_name: String(form.get("scientific_name") || "").trim(),
      area_id: String(form.get("area_id") || ""),
      water_sensor_entity_id: String(form.get("water_sensor_entity_id") || ""),
      watering_interval_days: intervalMin,
      watering_interval_min_days: intervalMin,
      watering_interval_max_days: Number(form.get("watering_interval_max_days")) || intervalMin,
      seasonal_watering_enabled: form.get("seasonal_watering_enabled") === "on",
      moisture_control_enabled: form.get("moisture_control_enabled") === "on",
      moisture_threshold_percent: Number(form.get("moisture_threshold_percent")) || 0,
      moisture_delay_days: Number(form.get("moisture_delay_days")) || 1,
      watering_reminder_enabled: form.get("watering_reminder_enabled") === "on",
      notification_target: String(form.get("notification_target") || ""),
      notes: String(form.get("notes") || "").trim(),
      is_toxic_to_cats: form.get("is_toxic_to_cats") === "on",
      is_toxic_to_dogs: form.get("is_toxic_to_dogs") === "on",
    });
    for (const season of ["spring", "summer", "autumn", "winter"]) {
      this._modal.plant[`watering_interval_${season}_min_days`] = Number(form.get(`watering_interval_${season}_min_days`)) || intervalMin;
      this._modal.plant[`watering_interval_${season}_max_days`] = Number(form.get(`watering_interval_${season}_max_days`)) || this._modal.plant[`watering_interval_${season}_min_days`];
    }
  }

  async _searchApi() {
    const query = String(this.shadowRoot.querySelector("#api-query")?.value || "").trim();
    if (query.length < 2) return;
    this._capturePlantForm();
    this._apiQuery = query;
    this._apiLoading = true;
    this._apiResults = [];
    this._render();
    let errorMessage = null;
    try {
      const response = await this._hass.callWS({ type: "plantmark/api/search", query });
      this._apiResults = response.results || [];
    } catch (error) {
      this._apiResults = null;
      errorMessage = error?.message || this._t.saveError;
    } finally {
      this._apiLoading = false;
      this._render();
      if (errorMessage) this._showToast(errorMessage, true);
    }
  }

  async _applyApi(speciesId) {
    this._capturePlantForm();
    this._apiLoading = true;
    this._render();
    let errorMessage = null;
    let applied = false;
    let basicDataOnly = false;
    try {
      const searchResult = this._apiResults?.find((result) => Number(result.id) === speciesId);
      let details;
      try {
        const response = await this._hass.callWS({ type: "plantmark/api/details", species_id: speciesId });
        details = response.plant || {};
      } catch (error) {
        if (!searchResult) throw error;
        details = {
          ...searchResult,
          api_provider: "perenual",
          perenual_id: speciesId,
          common_name: searchResult.common_name,
        };
        basicDataOnly = true;
      }
      const current = this._modal.plant;
      const hasLocalImage = String(current.image_url || "").startsWith("/plantmark_images/");
      Object.assign(current, details, {
        name: details.common_name || current.name || "",
        scientific_name: details.scientific_name || current.scientific_name || "",
        watering_interval_days: details.watering_interval_days || current.watering_interval_days || 7,
        image_url: hasLocalImage ? current.image_url : details.image_data ? details.image_url : current.image_url || null,
      });
      if (hasLocalImage) {
        current.image_license_name = null;
        current.image_license_url = null;
      } else if (details.image_data) {
        this._pendingImage = details.image_data;
        this._pendingImageSource = "api";
      }
      if (typeof details.poisonous_to_pets === "boolean") {
        current.is_toxic_to_cats = details.poisonous_to_pets;
        current.is_toxic_to_dogs = details.poisonous_to_pets;
      }
      this._apiResults = null;
      this._apiQuery = details.scientific_name || details.common_name || this._apiQuery;
      applied = true;
    } catch (error) {
      errorMessage = error?.message || this._t.saveError;
    } finally {
      this._apiLoading = false;
      this._render();
      if (applied) this._showToast(basicDataOnly ? this._t.basicDataApplied : this._t.dataApplied);
      if (errorMessage) this._showToast(errorMessage, true);
    }
  }

  _apiPayload(plant) {
    const fields = [
      "api_provider", "perenual_id", "api_last_synced", "common_name",
      "other_names", "family", "origin", "plant_type", "cycle", "watering",
      "sunlight", "soil", "care_level", "description", "poisonous_to_pets",
      "poisonous_to_humans", "indoor", "image_license_name", "image_license_url",
      "perenual_url", "watering_interval_estimated", "growth_rate", "maintenance",
      "hardiness_min", "hardiness_max", "flowering_season", "harvest_season",
      "propagation", "attracts", "pruning_month", "flowers", "fruits",
      "edible_fruit", "edible_leaf", "medicinal", "drought_tolerant",
      "salt_tolerant", "thorny", "invasive", "tropical", "fruiting_season",
      "harvest_method", "dimensions", "pruning_frequency", "pest_susceptibility",
      "cones", "leaf", "rare", "cuisine",
      "watering_quality", "watering_period", "water_depth_requirement",
      "water_volume_requirement", "average_volume_requirement", "base_temperature",
      "ph_level", "sunlight_duration", "temperature_tolerance",
      "spacing_requirement", "seeds", "flower_color", "fruit_color",
    ];
    return Object.fromEntries(fields.filter((field) => Object.hasOwn(plant, field)).map((field) => [field, plant[field]]));
  }

  async _prepareImage(file) {
    if (!file) return;
    try {
      this._pendingImage = await this._resizeImage(file);
      this._pendingImageSource = "upload";
      const preview = this.shadowRoot.querySelector("#image-preview");
      if (preview?.tagName === "IMG") preview.src = this._pendingImage;
      else if (preview) preview.outerHTML = `<img id="image-preview" src="${this._pendingImage}" alt="">`;
    } catch (error) {
      this._showToast(error?.message || this._t.saveError, true);
    }
  }

  async _resizeImage(file) {
    if (!file.type.startsWith("image/")) throw new Error(this._t.imageHelp);
    const url = URL.createObjectURL(file);
    try {
      const image = new Image();
      image.src = url;
      await image.decode();
      const maximum = 1280;
      const scale = Math.min(1, maximum / Math.max(image.naturalWidth, image.naturalHeight));
      const canvas = document.createElement("canvas");
      canvas.width = Math.max(1, Math.round(image.naturalWidth * scale));
      canvas.height = Math.max(1, Math.round(image.naturalHeight * scale));
      canvas.getContext("2d").drawImage(image, 0, 0, canvas.width, canvas.height);
      return canvas.toDataURL("image/webp", 0.82);
    } finally {
      URL.revokeObjectURL(url);
    }
  }

  async _savePlant(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const name = String(form.get("name") || "").trim();
    if (!name) return this._showToast(this._t.required, true);
    this._capturePlantForm();
    const current = this._modal?.plant || {};
    const plant = {
      id: form.get("id") || undefined,
      name,
      scientific_name: String(form.get("scientific_name") || "").trim(),
      area_id: String(form.get("area_id") || ""),
      water_sensor_entity_id: String(form.get("water_sensor_entity_id") || ""),
      image_url: current.image_url || null,
      watering_interval_days: current.watering_interval_days,
      notes: String(form.get("notes") || "").trim(),
      is_toxic_to_cats: form.get("is_toxic_to_cats") === "on",
      is_toxic_to_dogs: form.get("is_toxic_to_dogs") === "on",
      ...this._schedulePayload(current),
      ...this._apiPayload(current),
    };
    try {
      await this._hass.callWS({ type: "plantmark/save", plant, image_data: this._pendingImage || undefined, preserve_image_license: this._pendingImageSource === "api", remove_image: this._pendingImage ? false : form.get("remove_image") === "on" });
      this._closeModal();
      await this._load();
      this._showToast(this._t.saved);
    } catch (error) {
      this._showToast(error?.message || this._t.saveError, true);
    }
  }

  _schedulePayload(plant) {
    const fields = [
      "watering_interval_min_days", "watering_interval_max_days",
      "seasonal_watering_enabled", "moisture_control_enabled",
      "moisture_threshold_percent", "moisture_delay_days",
      "watering_reminder_enabled", "notification_target",
    ];
    for (const season of ["spring", "summer", "autumn", "winter"]) {
      fields.push(`watering_interval_${season}_min_days`, `watering_interval_${season}_max_days`);
    }
    return Object.fromEntries(fields.map((field) => [field, plant[field]]));
  }

  async _deletePlant(id) {
    if (!window.confirm(this._t.confirmDelete)) return;
    try {
      await this._hass.callWS({ type: "plantmark/delete", plant_id: String(id) });
      await this._load();
      this._showToast(this._t.deleted);
    } catch (error) {
      this._showToast(error?.message || this._t.saveError, true);
    }
  }

  async _waterPlant(id, button) {
    button.disabled = true;
    const old = button.innerHTML;
    button.innerHTML = `<ha-icon icon="mdi:loading"></ha-icon>${this._t.watering}`;
    try {
      await this._hass.callWS({ type: "plantmark/water", plant_id: String(id) });
      await this._load();
      this._showToast(this._t.watered);
    } catch (error) {
      button.disabled = false;
      button.innerHTML = old;
      this._showToast(error?.message || this._t.saveError, true);
    }
  }

  async _importPlants(event) {
    event.preventDefault();
    const data = String(new FormData(event.currentTarget).get("data") || "");
    try {
      const result = await this._hass.callWS({ type: "plantmark/import", data });
      this._closeModal();
      await this._load();
      this._showToast(`${result.added} ${this._t.imported}`);
    } catch (error) {
      this._showToast(error?.message || this._t.saveError, true);
    }
  }

  async _saveSettings(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const amount = Number(form.get("amount"));
    const apiKey = String(form.get("perenual_api_key") || "").trim();
    try {
      await this._hass.callWS({ type: "plantmark/settings", default_water_amount_ml: amount, perenual_api_key: apiKey || undefined, remove_perenual_api_key: form.get("remove_perenual_api_key") === "on" });
      this._closeModal();
      await this._load();
      this._showToast(this._t.settingsSaved);
    } catch (error) {
      this._showToast(error?.message || this._t.saveError, true);
    }
  }

  _sensorOptions(selected) {
    const states = Object.values(this._hass?.states || {}).filter((state) => this._isMoistureSensor(state));
    if (selected && !states.some((state) => state.entity_id === selected)) states.push({ entity_id: selected, attributes: { friendly_name: selected } });
    return states.sort((a, b) => this._sensorName(a).localeCompare(this._sensorName(b), this._language)).map((state) => `<option value="${escapeHtml(state.entity_id)}" ${state.entity_id === selected ? "selected" : ""}>${escapeHtml(this._sensorName(state))} · ${escapeHtml(state.entity_id)}</option>`).join("");
  }

  _isMoistureSensor(state) {
    if (!state?.entity_id?.startsWith("sensor.")) return false;
    const deviceClass = String(state.attributes?.device_class || "").toLowerCase();
    if (deviceClass === "moisture") return true;
    const unit = String(state.attributes?.unit_of_measurement || "").trim();
    const searchable = `${state.entity_id} ${state.attributes?.friendly_name || ""}`.toLowerCase();
    const plantContext = ["moisture", "boden", "soil", "plant", "pflanze", "flower", "erde"].some((word) => searchable.includes(word));
    return plantContext && (deviceClass === "humidity" || unit === "%");
  }

  _notificationOptions(selected) {
    const targets = [...(this._data.notification_targets || [])];
    if (selected && !targets.some((target) => target.id === selected)) targets.push({ id: selected, name: selected });
    return targets.map((target) => {
      const name = target.id === "persistent_notification"
        ? (this._language === "de" ? "Home-Assistant-Benachrichtigungszentrale" : "Home Assistant notification center")
        : target.name;
      return `<option value="${escapeHtml(target.id)}" ${target.id === selected ? "selected" : ""}>${escapeHtml(name)}</option>`;
    }).join("");
  }

  _careFacts(plant) {
    const facts = [];
    if (plant.watering) facts.push(["mdi:water-outline", this._t.interval, plant.watering]);
    if (plant.sunlight?.length) facts.push(["mdi:white-balance-sunny", this._t.light, plant.sunlight.slice(0, 2).join(", ")]);
    if (plant.care_level) facts.push(["mdi:leaf", this._t.careLevel, plant.care_level]);
    if (plant.soil?.length) facts.push(["mdi:terrain", this._t.soil, plant.soil.slice(0, 2).join(", ")]);
    if (plant.family) facts.push(["mdi:family-tree", this._t.family, plant.family]);
    if (plant.origin?.length) facts.push(["mdi:earth", this._t.origin, plant.origin.slice(0, 2).join(", ")]);
    if (plant.growth_rate) facts.push(["mdi:chart-timeline-variant-shimmer", this._t.growthRate, plant.growth_rate]);
    if (plant.maintenance) facts.push(["mdi:hand-heart-outline", this._t.maintenance, plant.maintenance]);
    if (plant.hardiness_min || plant.hardiness_max) facts.push(["mdi:snowflake", this._t.hardiness, [plant.hardiness_min, plant.hardiness_max].filter(Boolean).join("–")]);
    if (plant.flowering_season) facts.push(["mdi:flower", this._t.floweringSeason, plant.flowering_season]);
    if (plant.propagation?.length) facts.push(["mdi:sprout-outline", this._t.propagation, plant.propagation.slice(0, 2).join(", ")]);
    if (plant.dimensions) facts.push(["mdi:ruler", this._t.dimensions, plant.dimensions]);
    if (plant.attracts?.length) facts.push(["mdi:bee-flower", this._t.attracts, plant.attracts.slice(0, 3).join(", ")]);
    if (plant.pest_susceptibility?.length) facts.push(["mdi:bug-outline", this._t.pests, plant.pest_susceptibility.slice(0, 3).join(", ")]);
    if (plant.watering_period) facts.push(["mdi:clock-outline", this._t.wateringPeriod, plant.watering_period]);
    if (plant.watering_quality) facts.push(["mdi:water-check-outline", this._t.wateringQuality, plant.watering_quality]);
    if (plant.temperature_tolerance || plant.base_temperature) facts.push(["mdi:thermometer", this._t.temperature, plant.temperature_tolerance || plant.base_temperature]);
    if (plant.ph_level) facts.push(["mdi:ph", this._t.phLevel, plant.ph_level]);
    if (plant.watering_interval_estimated) facts.push(["mdi:approximately-equal", this._t.estimatedInterval, this._t.estimatedInterval]);
    return facts.map(([icon, label, value]) => `<span class="care-fact" title="${escapeHtml(label)}"><ha-icon icon="${icon}"></ha-icon>${escapeHtml(value)}</span>`).join("");
  }

  _sensorName(state) {
    return state?.attributes?.friendly_name || state?.entity_id || this._t.unavailable;
  }

  _sensorInfo(entityId) {
    const state = this._hass?.states?.[entityId];
    if (!state) return { name: entityId || this._t.noSensor, value: this._t.unavailable };
    const unit = state.attributes?.unit_of_measurement || "";
    return { name: this._sensorName(state), value: `${state.state}${unit ? ` ${unit}` : ""}` };
  }

  _updateSensorValues() {
    this.shadowRoot?.querySelectorAll("[data-sensor]").forEach((element) => { element.textContent = this._sensorInfo(element.dataset.sensor).value; });
  }

  _isDue(plant) {
    const date = new Date(plant.next_watering || "");
    return !Number.isNaN(date.getTime()) && date.getTime() <= Date.now();
  }

  _wateringRange(plant) {
    const fallback = Number(plant.watering_interval_days || 7);
    const prefix = plant.seasonal_watering_enabled && plant.current_season
      ? `watering_interval_${plant.current_season}`
      : "watering_interval";
    const minimum = Number(plant[`${prefix}_min_days`] || fallback);
    const maximum = Math.max(minimum, Number(plant[`${prefix}_max_days`] || minimum));
    return [minimum, maximum];
  }

  _formatDate(value) {
    const date = new Date(value || "");
    if (Number.isNaN(date.getTime())) return "–";
    return new Intl.DateTimeFormat(this._language, { day: "2-digit", month: "short", year: "numeric" }).format(date);
  }

  _formatDateRange(startValue, endValue) {
    const start = this._formatDate(startValue);
    const end = this._formatDate(endValue);
    return end === "–" || end === start ? start : `${start} – ${end}`;
  }

  _showToast(message, error = false) {
    const toast = this.shadowRoot?.querySelector("#toast");
    if (!toast) return;
    toast.textContent = message;
    toast.className = `toast show${error ? " error-toast" : ""}`;
    clearTimeout(this._toastTimer);
    this._toastTimer = setTimeout(() => { toast.className = "toast"; }, 3500);
  }

  _styles() {
    return `
      :host{display:block;min-height:100vh;background:var(--primary-background-color);color:var(--primary-text-color);font-family:var(--paper-font-body1_-_font-family,Roboto,sans-serif)}*{box-sizing:border-box}.page{max-width:1440px;margin:0 auto;padding:32px 28px 56px}header{display:flex;align-items:center;justify-content:space-between;gap:24px;margin-bottom:28px}.heading{display:flex;align-items:center;gap:16px}.brand{width:56px;height:56px;border-radius:18px;display:grid;place-items:center;color:#fff;background:linear-gradient(145deg,#4aa96c,#277c4b);box-shadow:0 10px 25px rgba(39,124,75,.25)}.brand ha-icon{--mdc-icon-size:32px}h1,h2,p{margin:0}h1{font-size:30px;line-height:1.15}.heading p,.modal-header p{color:var(--secondary-text-color);margin-top:5px}.header-actions,.card-actions,.modal-actions{display:flex;gap:10px}button,.upload-button{border:0;border-radius:12px;min-height:42px;padding:0 16px;font:inherit;font-weight:600;display:inline-flex;align-items:center;justify-content:center;gap:8px;cursor:pointer;transition:transform .15s,background .15s,opacity .15s}button:active{transform:scale(.97)}button:disabled{opacity:.55;cursor:wait}.primary{background:var(--primary-color,#43a047);color:var(--text-primary-color,#fff)}.secondary{background:var(--card-background-color);color:var(--primary-text-color);border:1px solid var(--divider-color)}.danger{background:color-mix(in srgb,var(--error-color,#db4437) 12%,transparent);color:var(--error-color,#db4437)}.icon-button{width:40px;height:40px;min-height:40px;padding:0;border-radius:50%;background:transparent;color:var(--secondary-text-color)}.icon-button:hover{background:var(--secondary-background-color);color:var(--primary-text-color)}.stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-bottom:24px}.stat{background:var(--card-background-color);border:1px solid var(--divider-color);border-radius:18px;padding:18px;display:flex;align-items:center;gap:14px;box-shadow:var(--ha-card-box-shadow,0 2px 8px rgba(0,0,0,.05))}.stat-icon{width:46px;height:46px;border-radius:14px;display:grid;place-items:center}.stat-icon.green{background:rgba(67,160,71,.14);color:#43a047}.stat-icon.blue{background:rgba(3,169,244,.14);color:#039be5}.stat-icon.purple{background:rgba(126,87,194,.14);color:#7e57c2}.stat strong{font-size:25px;display:block}.stat span:last-child{font-size:13px;color:var(--secondary-text-color)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:20px}.plant-card{overflow:hidden;background:var(--card-background-color);border:1px solid var(--divider-color);border-radius:22px;box-shadow:var(--ha-card-box-shadow,0 4px 18px rgba(0,0,0,.07));transition:transform .2s,box-shadow .2s}.plant-card:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(0,0,0,.12)}.plant-image{height:210px;position:relative;background:var(--secondary-background-color)}.plant-image img{width:100%;height:100%;object-fit:cover}.image-placeholder{height:100%;display:grid;place-items:center;color:var(--disabled-text-color);background:linear-gradient(135deg,rgba(67,160,71,.1),rgba(139,195,74,.16))}.image-placeholder ha-icon{--mdc-icon-size:72px}.area-chip{position:absolute;left:14px;bottom:14px;max-width:calc(100% - 28px);padding:7px 11px;border-radius:999px;background:rgba(20,30,24,.78);backdrop-filter:blur(8px);color:#fff;font-size:12px;display:flex;align-items:center;gap:5px}.area-chip ha-icon{--mdc-icon-size:16px}.image-attribution{position:absolute;right:10px;top:10px;padding:4px 7px;border-radius:7px;background:rgba(20,30,24,.72);color:#fff;font-size:9px}.image-attribution a{color:#fff}.plant-content{padding:18px}.plant-title{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}.plant-title h2{font-size:21px}.plant-title em{display:block;margin-top:4px;color:var(--secondary-text-color);font-size:13px}.schedule{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:18px 0}.schedule div{padding:10px 8px;border-radius:11px;background:var(--secondary-background-color);min-width:0}.schedule span{font-size:10px;color:var(--secondary-text-color);display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.schedule strong{font-size:12px;display:block;margin-top:4px;white-space:nowrap}.schedule .due{background:color-mix(in srgb,var(--error-color,#db4437) 11%,transparent)}.schedule .due strong{color:var(--error-color,#db4437)}.sensor-row{display:flex;align-items:center;gap:11px;padding:11px;border-radius:12px;background:rgba(3,169,244,.09);margin-bottom:12px}.sensor-icon{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:rgba(3,169,244,.15);color:#039be5}.sensor-row span:not(.sensor-icon){display:block;font-size:11px;color:var(--secondary-text-color)}.sensor-row strong{display:block;margin-top:2px}.care-facts{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}.care-fact{display:flex;align-items:center;gap:4px;padding:5px 8px;border-radius:8px;background:color-mix(in srgb,var(--primary-color) 9%,transparent);font-size:11px}.care-fact ha-icon{--mdc-icon-size:15px;color:var(--primary-color)}.warnings{display:flex;flex-wrap:wrap;gap:7px;margin:10px 0}.warning{display:flex;align-items:center;gap:4px;padding:5px 8px;border-radius:8px;background:rgba(255,152,0,.12);color:#ef8c00;font-size:11px}.warning ha-icon{--mdc-icon-size:15px}.notes{font-size:13px;line-height:1.45;color:var(--secondary-text-color);margin:12px 0;white-space:pre-line;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}.api-description{font-size:12px;margin:10px 0;color:var(--secondary-text-color)}.api-description summary{cursor:pointer;font-weight:600}.api-description p{line-height:1.45;margin-top:7px;white-space:pre-line}.card-actions{margin-top:16px}.card-actions .water{flex:1;background:rgba(3,169,244,.13);color:#0288d1}.card-actions .danger{width:44px;padding:0}.empty{min-height:420px;border:1px dashed var(--divider-color);border-radius:22px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:30px;background:var(--card-background-color)}.empty-icon{width:90px;height:90px;border-radius:30px;background:rgba(67,160,71,.12);color:#43a047;display:grid;place-items:center;margin-bottom:18px}.empty-icon ha-icon{--mdc-icon-size:48px}.empty h2{font-size:23px}.empty p{max-width:440px;color:var(--secondary-text-color);margin:9px 0 20px}.modal-backdrop{position:fixed;inset:0;z-index:999;display:flex;align-items:center;justify-content:center;padding:20px;background:rgba(0,0,0,.48);backdrop-filter:blur(3px)}.modal{width:min(560px,100%);max-height:calc(100vh - 40px);overflow:auto;background:var(--card-background-color);border-radius:22px;padding:24px;box-shadow:0 24px 80px rgba(0,0,0,.35)}.modal.wide{width:min(820px,100%)}.modal-header{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:22px}.modal-header h2{font-size:23px}.api-search-box{padding:15px;margin-bottom:19px;border:1px solid color-mix(in srgb,var(--primary-color) 30%,var(--divider-color));border-radius:14px;background:color-mix(in srgb,var(--primary-color) 5%,var(--card-background-color));display:grid;gap:11px}.api-search-title{display:flex;align-items:flex-start;gap:10px}.api-search-title>ha-icon{color:var(--primary-color)}.api-search-title strong,.api-search-title span{display:block}.api-search-title span{font-size:11px;color:var(--secondary-text-color);margin-top:3px}.source-badge{color:var(--primary-color)!important;display:flex!important;align-items:center;gap:4px}.source-badge ha-icon{--mdc-icon-size:14px}.api-search-row{display:flex;gap:8px}.api-search-row input{flex:1}.api-results{display:grid;gap:7px;max-height:270px;overflow:auto}.api-result{display:grid;grid-template-columns:46px 1fr auto;align-items:center;gap:9px;padding:8px;border-radius:10px;background:var(--card-background-color);border:1px solid var(--divider-color)}.api-result img,.api-result-placeholder{width:46px;height:46px;border-radius:8px;object-fit:cover}.api-result-placeholder{display:grid;place-items:center;background:var(--secondary-background-color);color:var(--primary-color)}.api-result div{min-width:0}.api-result strong,.api-result span{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.api-result span{font-size:10px;color:var(--secondary-text-color);margin-top:3px}.api-result button{min-height:34px;padding:0 10px;font-size:11px}.api-empty,.api-loading{font-size:12px;color:var(--secondary-text-color)}.api-loading{display:flex;align-items:center;gap:7px}.small-spinner{width:16px;height:16px;border:2px solid var(--divider-color);border-top-color:var(--primary-color);border-radius:50%;animation:spin .8s linear infinite}.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:17px}.field{display:flex;flex-direction:column;gap:7px}.field>span{font-size:13px;font-weight:600}.field.full{grid-column:1/-1}input,select,textarea{width:100%;border:1px solid var(--divider-color);border-radius:11px;background:var(--secondary-background-color);color:var(--primary-text-color);font:inherit;padding:11px 12px;outline:none}input:focus,select:focus,textarea:focus{border-color:var(--primary-color);box-shadow:0 0 0 2px color-mix(in srgb,var(--primary-color) 20%,transparent)}textarea{resize:vertical}.number-suffix{display:flex;align-items:center;position:relative}.number-suffix span{position:absolute;right:12px;color:var(--secondary-text-color);font-size:12px}.number-suffix input{padding-right:55px}.image-upload{display:flex;align-items:center;gap:12px}.image-upload img,.mini-placeholder{width:76px;height:76px;border-radius:13px;object-fit:cover;background:var(--secondary-background-color)}.mini-placeholder{display:grid;place-items:center;color:var(--secondary-text-color)}.upload-button{background:var(--secondary-background-color);border:1px solid var(--divider-color);font-size:13px}.upload-button input{display:none}.field small{color:var(--secondary-text-color);font-size:11px;line-height:1.4}.field small a{color:var(--primary-color)}.checks{display:flex;flex-direction:row;gap:22px;flex-wrap:wrap}.check{display:flex;align-items:center;gap:6px;font-size:13px;cursor:pointer}.check input{width:18px;height:18px;accent-color:var(--primary-color)}.check ha-icon{--mdc-icon-size:18px}.api-settings{display:grid;gap:14px;margin-top:22px;padding-top:20px;border-top:1px solid var(--divider-color)}.api-settings-heading{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}.api-settings h3{margin:0 0 5px;font-size:17px}.api-settings p{color:var(--secondary-text-color);font-size:12px;line-height:1.4}.api-status{display:flex;align-items:center;gap:4px;white-space:nowrap;font-size:10px;padding:5px 8px;border-radius:999px;background:var(--secondary-background-color);color:var(--secondary-text-color)}.api-status.connected{background:rgba(67,160,71,.12);color:#43a047}.api-status ha-icon{--mdc-icon-size:14px}.remove-api{color:var(--error-color)}.modal-actions{justify-content:flex-end;margin-top:24px}.loading{min-height:360px;display:grid;place-items:center}.spinner{width:42px;height:42px;border:4px solid var(--divider-color);border-top-color:var(--primary-color);border-radius:50%;animation:spin .8s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}.error{display:flex;align-items:center;gap:9px;padding:12px 14px;margin-bottom:18px;border-radius:12px;background:color-mix(in srgb,var(--error-color,#db4437) 12%,transparent);color:var(--error-color,#db4437)}.toast{position:fixed;z-index:1200;left:50%;bottom:30px;transform:translate(-50%,20px);padding:12px 18px;border-radius:11px;background:#263229;color:#fff;box-shadow:0 8px 30px rgba(0,0,0,.28);opacity:0;pointer-events:none;transition:.2s}.toast.show{opacity:1;transform:translate(-50%,0)}.toast.error-toast{background:var(--error-color,#db4437)}
      .advanced-block{padding:14px;border:1px solid var(--divider-color);border-radius:13px;background:color-mix(in srgb,var(--secondary-background-color) 72%,transparent)}.advanced-block>small{margin-left:24px}.season-grid{display:grid;gap:8px;margin-top:10px}.season-row{display:grid;grid-template-columns:minmax(80px,1fr) 110px 110px auto;align-items:end;gap:8px}.season-row>strong{align-self:center}.season-row label{display:grid;gap:3px}.season-row label span{font-size:10px;color:var(--secondary-text-color)}.season-row input{padding:8px}.conditional-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:10px}[data-enabled-by]{transition:opacity .15s}[data-enabled-by].inactive{opacity:.42;pointer-events:none}.advanced-block select{margin-top:4px}
      .api-result-actions{display:flex;align-items:center;gap:6px}.api-page-link{width:34px;height:34px;padding:0;border-radius:10px;display:grid;place-items:center;text-decoration:none}.api-page-link ha-icon{--mdc-icon-size:18px}
      @media(max-width:850px){.page{padding:22px 16px 42px}header{align-items:flex-start;flex-direction:column}.header-actions{width:100%;flex-wrap:wrap}.header-actions button{flex:1}.stats{grid-template-columns:1fr}.stat{padding:13px}.grid{grid-template-columns:repeat(auto-fill,minmax(280px,1fr))}.form-grid{grid-template-columns:1fr}.field.full{grid-column:auto}.season-row{grid-template-columns:1fr 1fr}.season-row>strong,.season-row>span{grid-column:1/-1}.conditional-grid{grid-template-columns:1fr}}
      @media(max-width:520px){h1{font-size:25px}.brand{width:48px;height:48px;border-radius:15px}.header-actions{display:grid;grid-template-columns:1fr 1fr}.header-actions #add{grid-column:1/-1}.plant-image{height:190px}.modal-backdrop{padding:0;align-items:flex-end}.modal,.modal.wide{width:100%;max-height:94vh;border-radius:22px 22px 0 0;padding:20px}.schedule{gap:5px}.schedule div{padding:9px 6px}.schedule strong{font-size:11px}.api-search-row{flex-direction:column}.api-result{grid-template-columns:42px 1fr}.api-result-actions{grid-column:1/-1}.api-result-actions button{flex:1}.api-settings-heading{flex-direction:column}.api-status{align-self:flex-start}}
    `;
  }
}

if (!customElements.get("plantmark-panel")) customElements.define("plantmark-panel", PlantmarkPanel);
