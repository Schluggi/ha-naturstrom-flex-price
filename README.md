# Naturstrom Flex Home Assistant Integration

Dies ist eine benutzerdefinierte Home Assistant Integration zur Überwachung der aktuellen Energiekosten des Naturstrom Flex Tarifs.

## Installation

### Über HACS (empfohlen)

1. Fügen Sie dieses Repository zu HACS als benutzerdefiniertes Repository hinzu.
2. Installieren Sie die "Naturstrom Flex" Integration.
3. Starten Sie Home Assistant neu.

### Manuelle Installation

1. Kopieren Sie den Ordner `custom_components/naturstrom_flex` in das `custom_components` Verzeichnis Ihrer Home Assistant Installation.
2. Starten Sie Home Assistant neu.

## Konfiguration

Die Integration kann über die Home Assistant Benutzeroberfläche konfiguriert werden:

1. Gehen Sie zu **Einstellungen** > **Geräte & Dienste**.
2. Klicken Sie auf **Integration hinzufügen**.
3. Suchen Sie nach "Naturstrom Flex" und wählen Sie es aus.
4. Folgen Sie dem Setup-Assistenten, um den Sensor-Namen zu konfigurieren (optional).

Eine manuelle Konfiguration in `configuration.yaml` ist nicht erforderlich.

## Funktionen

- Holt den aktuellen Energiekostensatz von der Naturstrom Website.
- Stellt den Preis in ct/kWh (Cent pro kWh) bereit.
- Aktualisiert automatisch.

## Anforderungen

- BeautifulSoup4

Die Integration installiert die erforderliche Abhängigkeit automatisch.