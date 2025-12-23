# Naturstrom Flex Home Assistant Integration

This is a custom Home Assistant integration for monitoring the current energy costs of Naturstrom Flex tariff.

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
4. Follow the setup wizard to configure the sensor name (optional).

No manual configuration in `configuration.yaml` is required.

## Features

- Fetches the current energy price from the Naturstrom website.
- Provides the price in ct/kWh (cent per kWh).
- Updates automatically.

## Requirements

- BeautifulSoup4

The integration will install the required dependency automatically.
