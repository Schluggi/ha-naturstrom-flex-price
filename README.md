# Naturstrom Flex Home Assistant Integration

This is a custom Home Assistant integration for monitoring the current energy costs of Naturstrom Flex tariff.

> **Note**: 100% vibe code

## Installation

### Via HACS (recommended)

1. Add this repository to HACS as a custom repository.
2. Install the "Naturstrom Flex" integration.
3. Restart Home Assistant.

### Manual Installation

1. Copy the `custom_components/naturstrom_flex` folder to your Home Assistant's `custom_components` directory.
2. Restart Home Assistant.

## Configuration

The integration can be configured via the Home Assistant UI:

1. Go to **Settings** > **Devices & Services**.
2. Click **Add Integration**.
3. Search for "Naturstrom Flex" and select it.
4. Follow the setup wizard to configure:
   - **Sensor Name** (optional): Custom name for the sensor (default: "Naturstrom Flex Price")
   - **Update Interval** (optional): How often to fetch data from the website in hours (default: 6 hours, range: 1-24 hours)

### Changing Settings

You can modify the configuration at any time:

1. Go to **Settings** > **Devices & Services**.
2. Find the "Naturstrom Flex" integration.
3. Click **Configure**.
4. Update the sensor name or update interval.
5. The integration will automatically reload with the new settings.

No manual configuration in `configuration.yaml` is required.

## Features

- Fetches the current variable energy price from the Naturstrom website.
- Calculates the fix costs (total price - variable price).
- Provides two sensors:
  - **Naturstrom Flex Price**: Variable energy price in ct/kWh
  - **Naturstrom Flex Price Fix Costs**: Fixed costs in ct/kWh
- Configurable update interval (1-24 hours) to reduce website load.
- Updates automatically based on the configured interval.

## Requirements

- BeautifulSoup4

The integration will install the required dependency automatically.
