"""Test the Naturstrom Flex sensor."""
import pytest
from unittest.mock import patch, MagicMock
from custom_components.naturstrom_flex.sensor import get_current_price, get_current_total


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


def test_get_current_total_success():
    """Test successful total fetching."""
    mock_html = """
    <html>
    <script>
    window['Hoogi91.chartsData'] = {};
    window['Hoogi91.chartsData']['chartsData7'] = {labels: ["02/25 (34.33 ct/kWh)","12/25 (33.83 ct/kWh)"], datasets: [{"data":[34.33,33.83]}]};
    </script>
    </html>
    """
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.content = mock_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        total = get_current_total()
        assert total == 33.83


def test_get_current_total_no_script():
    """Test when script is not found."""
    mock_html = "<html></html>"
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.content = mock_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        total = get_current_total()
        assert total is None


def test_get_current_total_request_error():
    """Test request error for total."""
    with patch('requests.get', side_effect=Exception("Network error")):
        total = get_current_total()
        assert total is None


@pytest.mark.integration
def test_get_current_price_live():
    """Test fetching price from live URL."""
    price = get_current_price()
    # Price should be a positive float if the website is accessible
    assert price is None or (isinstance(price, float) and price > 0)


@pytest.mark.integration
def test_get_current_total_live():
    """Test fetching total from live URL."""
    total = get_current_total()
    # Total should be a positive float if the website is accessible
    assert total is None or (isinstance(total, float) and total > 0)


@pytest.mark.integration
def test_live_price_consistency():
    """Test that live price and total are consistent."""
    price = get_current_price()
    total = get_current_total()
    
    # If both are available, total should be greater than price
    if price is not None and total is not None:
        assert total > price, f"Total ({total}) should be greater than variable price ({price})"
        # Fix costs should be positive
        fix_costs = total - price
        assert fix_costs > 0, f"Fix costs ({fix_costs}) should be positive"