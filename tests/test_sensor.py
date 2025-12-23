"""Test the Naturstrom Flex sensor."""
import pytest
from unittest.mock import patch, MagicMock
from custom_components.naturstrom_flex.sensor import get_current_price


def test_get_current_price_success():
    """Test successful price fetching."""
    mock_html = """
    <table>
    <tr><th>Monat</th><th>12/25</th></tr>
    <tr><td>ct/kWh (brutto)</td><td>14,30</td></tr>
    </table>
    """
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.content = mock_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        price = get_current_price()
        assert price == 14.3


def test_get_current_price_no_table():
    """Test when table is not found."""
    mock_html = "<html></html>"
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.content = mock_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        price = get_current_price()
        assert price is None


def test_get_current_price_request_error():
    """Test request error."""
    with patch('requests.get', side_effect=Exception("Network error")):
        price = get_current_price()
        assert price is None