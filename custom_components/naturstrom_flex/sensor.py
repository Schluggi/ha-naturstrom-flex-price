"""Sensor for Naturstrom Flex energy costs."""
import logging
import re
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DEFAULT_NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)

URL = "https://www.naturstrom.de/privatkunden/oekostrom/naturstrom-flex"


def get_current_price() -> Optional[float]:
    """Fetch and parse the current energy price from the website."""
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table with prices by finding 'Monat'
        monat = soup.find(string="Monat")
        if not monat:
            _LOGGER.error("Monat not found")
            return None

        table = monat.find_parent("table")
        if not table:
            _LOGGER.error("Table not found")
            return None

        # Get the rows
        rows = table.find_all("tr")
        if len(rows) < 2:
            _LOGGER.error("Invalid table rows")
            return None

        # First row: headers
        headers_row = rows[0]
        headers = [cell.get_text(strip=True) for cell in headers_row.find_all(["th", "td"])]

        # Second row: prices
        data_row = rows[1]
        prices_cells = [cell.get_text(strip=True) for cell in data_row.find_all(["th", "td"])]

        if len(headers) != len(prices_cells):
            _LOGGER.error("Headers and prices mismatch")
            return None

        prices = {}
        for month, price_text in zip(headers[1:], prices_cells[1:]):  # Skip first column
            price_text = price_text.replace(",", ".")
            try:
                price = float(price_text)
                prices[month] = price
            except ValueError:
                _LOGGER.warning(f"Invalid price for {month}: {price_text}")

        # Get current month in MM/YY format
        now = datetime.now()
        current_month = f"{now.month:02d}/{str(now.year)[-2:]}"

        if current_month in prices:
            return prices[current_month]

        # If not found, return the last price
        if prices:
            last_month = max(prices.keys())
            _LOGGER.info(f"Current month {current_month} not found, using {last_month}")
            return prices[last_month]

        return None

    except Exception as e:
        _LOGGER.error(f"Error fetching price: {e}")
        return None


def get_current_total() -> Optional[float]:
    """Fetch and parse the current total energy price from the website chart."""
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the script with chartsData7
        scripts = soup.find_all("script")
        script_text = None
        for script in scripts:
            if script.string and "chartsData7" in script.string:
                script_text = script.string
                break
        if not script_text:
            _LOGGER.error("Chart script not found")
            return None

        # Extract the data
        start = script_text.find("window['Hoogi91.chartsData']['chartsData7'] = {")
        if start == -1:
            _LOGGER.error("chartsData7 not found")
            return None

        # Find the end, before the next ;
        end = script_text.find(";", start)
        if end == -1:
            end = len(script_text)
        data_str = script_text[start:end]

        # Parse labels
        labels_match = re.search(r"labels\s*:\s*\[([^\]]+)\]", data_str, re.S)
        if not labels_match:
            _LOGGER.error("Labels not found")
            return None
        labels_str = labels_match.group(1)
        # extract quoted labels
        labels = re.findall(r'"([^\"]+)"', labels_str)

        # Parse data from datasets -> look for data array inside datasets
        data_match = re.search(r"datasets\s*:\s*\[\s*\{[^}]*[\'\"]?data[\'\"]?\s*:\s*\[([^\]]+)\]", data_str, re.S)
        if not data_match:
            _LOGGER.error("Data not found in datasets")
            return None
        data_str_match = data_match.group(1)
        # Parse data numbers
        data = [float(d.strip()) for d in data_str_match.split(',') if d.strip()]

        # Extract prices
        prices = {}
        for label, price in zip(labels, data):
            # label like "02\/25 (34,33 ct\/kWh)"
            month_match = re.search(r'(\d{2}\/\d{2})', label)
            if month_match:
                month = month_match.group(1)
                prices[month] = price

        # Get current month
        now = datetime.now()
        current_month = f"{now.month:02d}/{str(now.year)[-2:]}"

        if current_month in prices:
            return prices[current_month]

        # If not found, return the last price
        if prices:
            last_month = max(prices.keys())
            _LOGGER.info(f"Current month {current_month} not found, using {last_month}")
            return prices[last_month]

        return None

    except Exception as e:
        _LOGGER.error(f"Error fetching total: {e}")
        return None


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Naturstrom Flex sensor from a config entry."""
    name = config_entry.options.get(CONF_NAME, config_entry.data.get(CONF_NAME, DEFAULT_NAME))
    async_add_entities([NaturstromFlexSensor(name), NaturstromFlexFixCostsSensor(name)], True)


class NaturstromFlexSensor(SensorEntity):
    """Representation of a Naturstrom Flex sensor."""

    def __init__(self, name: str) -> None:
        """Initialize the sensor."""
        self._name = name
        self._state = None
        self._unit = "ct/kWh"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return self._unit

    @property
    def icon(self) -> str:
        """Return the icon."""
        return "mdi:currency-eur"

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        self._state = await self.hass.async_add_executor_job(get_current_price)


class NaturstromFlexFixCostsSensor(SensorEntity):
    """Representation of a Naturstrom Flex fix costs sensor."""

    def __init__(self, name: str) -> None:
        """Initialize the sensor."""
        self._name = f"{name} Fix Costs"
        self._state = None
        self._unit = "ct/kWh"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return self._unit

    @property
    def icon(self) -> str:
        """Return the icon."""
        return "mdi:currency-eur"

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        variable = await self.hass.async_add_executor_job(get_current_price)
        total = await self.hass.async_add_executor_job(get_current_total)
        if variable is not None and total is not None:
            self._state = round(total - variable, 2)
        else:
            self._state = None