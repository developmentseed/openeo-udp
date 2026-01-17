"""
Unit tests for OpenEO UDP parameter management and widgets.

This test suite covers:
- ParameterManager functionality
- Widget creation and behavior
- Endpoint configuration loading
- Parameter validation
"""

import pytest
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Import the modules to test
from openeo_udp import ParameterManager
from openeo_udp.config import load_endpoint_config
from openeo.api.process import Parameter


@pytest.fixture
def sample_params_content():
    """Sample parameter file content for testing."""
    return """
from openeo.api.process import Parameter

def get_parameters():
    return {
        'venice_lagoon': {
            'location_name': 'Venice Lagoon',
            'bounding_box': Parameter('bounding_box', default={'west': 12.0, 'south': 45.3, 'east': 12.6, 'north': 45.6}),
            'time': Parameter('time', default=['2023-06-01', '2023-06-30']),
            'bands': Parameter('bands', default=['B02', 'B03', 'B04', 'B05', 'B08', 'B8A', 'B11']),
            'collection': Parameter('collection', default='SENTINEL2_L2A'),
            'cloud_cover': Parameter('cloud_cover', default=30),
        },
        'lake_victoria': {
            'location_name': 'Lake Victoria',
            'bounding_box': Parameter('bounding_box', default={'west': 31.5, 'south': -3.0, 'east': 34.5, 'north': 0.5}),
            'time': Parameter('time', default=['2023-07-01', '2023-07-31']),
            'bands': Parameter('bands', default=['B02', 'B03', 'B04', 'B05', 'B08', 'B8A', 'B11']),
            'collection': Parameter('collection', default='SENTINEL2_L2A'),
            'cloud_cover': Parameter('cloud_cover', default=20),
        }
    }
"""


@pytest.fixture
def temp_params_file(sample_params_content):
    """Create a temporary params file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(sample_params_content)
        params_file = f.name

    yield params_file

    # Cleanup
    if os.path.exists(params_file):
        os.unlink(params_file)


class TestParameterManager:
    """Test cases for ParameterManager class."""

    def test_parameter_manager_initialization(self, temp_params_file):
        """Test ParameterManager can be initialized with a valid params file."""
        manager = ParameterManager(temp_params_file)
        assert str(manager.param_file) == temp_params_file
        assert hasattr(manager, "list_parameter_sets")

    def test_parameter_manager_missing_file(self):
        """Test ParameterManager handles missing file gracefully."""
        with pytest.raises(FileNotFoundError):
            ParameterManager("nonexistent_file.py")

    def test_list_parameter_sets(self, temp_params_file):
        """Test listing available parameter sets."""
        manager = ParameterManager(temp_params_file)
        sets = manager.list_parameter_sets()
        assert "venice_lagoon" in sets
        assert "lake_victoria" in sets
        assert len(sets) == 2

    def test_get_parameter_set(self, temp_params_file):
        """Test getting a specific parameter set."""
        manager = ParameterManager(temp_params_file)
        params = manager.get_parameter_set("venice_lagoon")
        assert params["location_name"] == "Venice Lagoon"
        assert hasattr(params["bounding_box"], "default")
        assert params["bounding_box"].default["west"] == 12.0

    def test_use_parameter_set(self, temp_params_file):
        """Test switching to a different parameter set."""
        manager = ParameterManager(temp_params_file)

        # Switch to lake_victoria
        manager.use_parameter_set("lake_victoria")
        params = manager.get_parameter_set()
        assert params["location_name"] == "Lake Victoria"

        # Switch to venice_lagoon
        manager.use_parameter_set("venice_lagoon")
        params = manager.get_parameter_set()
        assert params["location_name"] == "Venice Lagoon"

    def test_get_parameter(self, temp_params_file):
        """Test getting a specific parameter from the current set."""
        manager = ParameterManager(temp_params_file)
        manager.use_parameter_set("venice_lagoon")

        bbox = manager.get_parameter("bounding_box")
        assert hasattr(bbox, "default")
        assert bbox.default == {
            "west": 12.0,
            "south": 45.3,
            "east": 12.6,
            "north": 45.6,
        }

        time_param = manager.get_parameter("time")
        assert hasattr(time_param, "default")
        assert time_param.default == ["2023-06-01", "2023-06-30"]

    def test_parameter_set_not_found(self, temp_params_file):
        """Test handling of non-existent parameter set."""
        manager = ParameterManager(temp_params_file)

        with pytest.raises(ValueError):
            manager.use_parameter_set("nonexistent_set")

    def test_parameter_not_found(self, temp_params_file):
        """Test handling of non-existent parameter."""
        manager = ParameterManager(temp_params_file)
        manager.use_parameter_set("venice_lagoon")

        with pytest.raises(ValueError):
            manager.get_parameter("nonexistent_parameter")


class TestEndpointConfiguration:
    """Test cases for endpoint configuration loading."""

    @patch("pathlib.Path.exists")
    @patch("builtins.open")
    @patch("yaml.safe_load")
    def test_load_endpoint_config(self, mock_yaml_load, mock_open, mock_exists):
        """Test loading endpoint configuration from YAML file."""
        mock_exists.return_value = True
        mock_yaml_load.return_value = {
            "endpoints": {
                "test_endpoint": {
                    "url": "https://test.example.com",
                    "enabled": True,
                    "auth": {"type": "basic"},
                }
            }
        }

        config = load_endpoint_config()
        assert "endpoints" in config
        assert "test_endpoint" in config["endpoints"]
        assert config["endpoints"]["test_endpoint"]["url"] == "https://test.example.com"

    @patch("pathlib.Path.exists")
    def test_load_endpoint_config_missing_file(self, mock_exists):
        """Test handling of missing endpoint config file."""
        # Since the actual implementation raises FileNotFoundError when file doesn't exist,
        # let's test that behavior instead
        mock_exists.return_value = False
        
        with pytest.raises(FileNotFoundError):
            load_endpoint_config()


class TestWidgets:
    """Test cases for widget functionality."""

    @pytest.fixture
    def mock_param_manager(self, temp_params_file):
        """Create a real ParameterManager for testing."""
        return ParameterManager(temp_params_file)

    @patch("openeo_udp.widgets.load_endpoint_config")
    @patch("openeo_udp.widgets.display")
    @patch("openeo_udp.widgets.clear_output")
    def test_interactive_parameter_selection_creation(
        self, mock_clear_output, mock_display, mock_load_config, mock_param_manager
    ):
        """Test that interactive parameter selection creates widgets properly."""
        from openeo_udp.widgets import interactive_parameter_selection

        # Mock endpoint config
        mock_load_config.return_value = {
            "endpoints": {"test_endpoint": {"url": "https://test.com", "enabled": True}}
        }

        result = interactive_parameter_selection(mock_param_manager)

        # Should return a callable function
        assert callable(result)

        # Should have called clear_output and display
        mock_clear_output.assert_called_once_with(wait=True)
        assert mock_display.call_count >= 1  # Should display widgets

    @patch("openeo_udp.widgets.load_endpoint_config")
    @patch("openeo_udp.widgets.get_connection")
    def test_quick_connect_success(
        self, mock_get_connection, mock_load_config, mock_param_manager
    ):
        """Test successful quick connection."""
        from openeo_udp.widgets import quick_connect

        # Mock successful connection
        mock_connection = Mock()
        mock_get_connection.return_value = mock_connection

        # Mock endpoint config
        mock_load_config.return_value = {
            "endpoints": {"test_endpoint": {"url": "https://test.com", "enabled": True}}
        }

        connection, params = quick_connect(
            mock_param_manager,
            param_set="venice_lagoon",
            endpoint="test_endpoint",
            silent=True,
        )

        assert connection == mock_connection
        assert "location_name" in params
        assert params["location_name"] == "Venice Lagoon"

    @patch("openeo_udp.widgets.load_endpoint_config")
    @patch("openeo_udp.widgets.get_connection")
    def test_quick_connect_with_defaults(
        self, mock_get_connection, mock_load_config, mock_param_manager
    ):
        """Test quick connection with default parameters."""
        from openeo_udp.widgets import quick_connect

        mock_connection = Mock()
        mock_get_connection.return_value = mock_connection

        mock_load_config.return_value = {
            "endpoints": {
                "default_endpoint": {"url": "https://default.com", "enabled": True}
            }
        }

        connection, params = quick_connect(mock_param_manager, silent=True)

        assert connection == mock_connection
        # Should use first available parameter set
        assert params["location_name"] in ["Venice Lagoon", "Lake Victoria"]

    @patch("openeo_udp.widgets.load_endpoint_config")
    @patch("openeo_udp.widgets.get_connection")
    def test_quick_connect_failure(
        self, mock_get_connection, mock_load_config, mock_param_manager
    ):
        """Test quick connection failure handling."""
        from openeo_udp.widgets import quick_connect

        # Mock connection failure
        mock_get_connection.side_effect = Exception("Connection failed")

        mock_load_config.return_value = {
            "endpoints": {"test_endpoint": {"url": "https://test.com", "enabled": True}}
        }

        with pytest.raises(Exception, match="Connection failed"):
            quick_connect(mock_param_manager, silent=True)


class TestParameterValidation:
    """Test cases for parameter validation."""

    def test_parameter_object_validation(self):
        """Test that Parameter objects are created correctly."""
        bbox_param = Parameter(
            "bounding_box",
            default={"west": 12.0, "south": 45.3, "east": 12.6, "north": 45.6},
        )

        assert bbox_param.name == "bounding_box"
        assert isinstance(bbox_param.default, dict)
        assert "west" in bbox_param.default
        assert "south" in bbox_param.default
        assert "east" in bbox_param.default
        assert "north" in bbox_param.default

    def test_parameter_set_structure(self, temp_params_file):
        """Test that parameter sets have the expected structure."""
        manager = ParameterManager(temp_params_file)
        param_set = manager.get_parameter_set("venice_lagoon")

        expected_keys = [
            "location_name",
            "bounding_box",
            "time",
            "bands",
            "collection",
            "cloud_cover",
        ]

        for key in expected_keys:
            assert key in param_set

            if key != "location_name":
                # All parameters except location_name should be Parameter objects
                assert hasattr(param_set[key], "default")


class TestIntegration:
    """Integration tests for the complete workflow."""

    @patch("openeo_udp.widgets.get_connection")
    @patch("openeo_udp.widgets.load_endpoint_config")
    def test_complete_workflow_simulation(
        self, mock_load_config, mock_get_connection, temp_params_file
    ):
        """Test a complete workflow from parameter loading to connection."""
        from openeo_udp.widgets import quick_connect

        # Mock external dependencies
        mock_connection = Mock()
        mock_get_connection.return_value = mock_connection
        mock_load_config.return_value = {
            "endpoints": {"test_endpoint": {"url": "https://test.com", "enabled": True}}
        }

        # Test complete workflow
        param_manager = ParameterManager(temp_params_file)

        # Test parameter loading
        sets = param_manager.list_parameter_sets()
        assert "venice_lagoon" in sets

        # Test parameter set selection
        param_manager.use_parameter_set("venice_lagoon")
        params = param_manager.get_parameter_set()
        assert params["location_name"] == "Venice Lagoon"

        # Test individual parameter access
        bbox = param_manager.get_parameter("bounding_box")
        assert bbox.default["west"] == 12.0

        # Test quick connect
        connection, current_params = quick_connect(
            param_manager,
            param_set="venice_lagoon",
            endpoint="test_endpoint",
            silent=True,
        )

        assert connection == mock_connection
        assert current_params["location_name"] == "Venice Lagoon"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
