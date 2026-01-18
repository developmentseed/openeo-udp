"""
Unit tests for OpenEO UDP parameter management and widgets.

This test suite covers:
- ParameterManager functionality
- Widget creation and behavior
- Endpoint configuration loading
- Parameter validation
"""

import os
import tempfile
from unittest.mock import Mock, patch

import pytest
from openeo.api.process import Parameter

# Import the modules to test
from openeo_udp import ParameterManager
from openeo_udp.endpoints import get_all_endpoints


@pytest.fixture
def sample_params_content():
    """Sample parameter file content for testing."""
    return """
from openeo.api.process import Parameter

def get_parameters():
    return {
        'venice_lagoon': {
            'location_name': 'Venice Lagoon',
            'bounding_box': Parameter('bounding_box', description='Spatial extent for Venice Lagoon', default={'west': 12.0, 'south': 45.3, 'east': 12.6, 'north': 45.6}),
            'time': Parameter('time', description='Temporal range for data acquisition', default=['2023-06-01', '2023-06-30']),
            'bands': Parameter('bands', description='Sentinel-2 bands for analysis', default=['B02', 'B03', 'B04', 'B05', 'B08', 'B8A', 'B11']),
            'collection': Parameter('collection', description='Data collection identifier', default='SENTINEL2_L2A'),
            'cloud_cover': Parameter('cloud_cover', description='Maximum cloud cover percentage', default=30),
        },
        'lake_victoria': {
            'location_name': 'Lake Victoria',
            'bounding_box': Parameter('bounding_box', description='Spatial extent for Lake Victoria', default={'west': 31.5, 'south': -3.0, 'east': 34.5, 'north': 0.5}),
            'time': Parameter('time', description='Temporal range for data acquisition', default=['2023-07-01', '2023-07-31']),
            'bands': Parameter('bands', description='Sentinel-2 bands for analysis', default=['B02', 'B03', 'B04', 'B05', 'B08', 'B8A', 'B11']),
            'collection': Parameter('collection', description='Data collection identifier', default='SENTINEL2_L2A'),
            'cloud_cover': Parameter('cloud_cover', description='Maximum cloud cover percentage', default=20),
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
    """Test cases for Python-based endpoint configuration loading."""

    def test_get_all_endpoints(self):
        """Test loading endpoint configuration from Python modules."""
        all_endpoints = get_all_endpoints()

        # Should have at least our three configured endpoints
        assert "copernicus_explorer" in all_endpoints
        assert "copernicus_dataspace" in all_endpoints
        assert "ds_development" in all_endpoints

        # Check structure of endpoint config
        for config in all_endpoints.values():
            assert "url" in config
            assert "collection_id" in config
            assert "band_format" in config

    def test_endpoint_config_structure(self):
        """Test that endpoint configurations have the expected structure."""
        all_endpoints = get_all_endpoints()

        # Test EOPF Explorer endpoint specifically
        explorer_config = all_endpoints.get("copernicus_explorer")
        assert explorer_config is not None
        assert (
            explorer_config["url"] == "https://api.explorer.eopf.copernicus.eu/openeo"
        )
        assert explorer_config["collection_id"] == "sentinel-2-l2a"
        assert explorer_config["band_format"] == "reflectance|{band}"

        # Test Copernicus Data Space endpoint
        cdse_config = all_endpoints.get("copernicus_dataspace")
        assert cdse_config is not None
        assert "dataspace.copernicus.eu" in cdse_config["url"]
        assert cdse_config["collection_id"] == "SENTINEL2_L2A"
        assert cdse_config["band_format"] == "{band}"


class TestParameterManagerMethods:
    """Test cases for ParameterManager widget and helper methods."""

    @pytest.fixture
    def mock_param_manager(self, temp_params_file):
        """Create a real ParameterManager for testing."""
        return ParameterManager(temp_params_file)

    def test_print_options(self, mock_param_manager, capsys):
        """Test print_options helper method."""
        mock_param_manager.print_options("Test Algorithm")

        # Capture printed output
        captured = capsys.readouterr()
        output = captured.out

        # Should contain algorithm name and parameter sets
        assert "Test Algorithm" in output
        assert "venice_lagoon" in output
        assert "lake_victoria" in output
        assert "Available parameter sets" in output

    def test_interactive_parameter_selection_creation(self, mock_param_manager):
        """Test that interactive parameter selection creates widgets properly."""
        result = mock_param_manager.interactive_parameter_selection()

        # Should return a callable function
        assert callable(result)

    @patch("openeo.connect")
    def test_quick_connect_success(self, mock_connect, mock_param_manager):
        """Test successful quick connection."""
        # Mock successful connection
        mock_connection = Mock()
        mock_connect.return_value = mock_connection
        mock_connection.authenticate_oidc_authorization_code = Mock()

        connection, params = mock_param_manager.quick_connect(
            param_set="venice_lagoon", endpoint="copernicus_explorer", silent=True
        )

        assert connection == mock_connection
        assert "location_name" in params
        assert params["location_name"] == "Venice Lagoon"

    @patch("openeo_udp.endpoints.get_endpoint_connection")
    def test_quick_connect_with_defaults(self, mock_get_connection, mock_param_manager):
        """Test quick connection with default parameters."""
        mock_connection = Mock()
        mock_get_connection.return_value = mock_connection

        connection, params = mock_param_manager.quick_connect(silent=True)

        assert connection == mock_connection
        # Should use first available parameter set
        assert params["location_name"] in ["Venice Lagoon", "Lake Victoria"]
        mock_get_connection.assert_called_once()

    @patch("openeo_udp.endpoints.get_endpoint_connection")
    def test_quick_connect_failure(self, mock_get_connection, mock_param_manager):
        """Test quick connection failure handling."""
        # Mock connection failure
        mock_get_connection.side_effect = Exception("Connection failed")

        with pytest.raises(Exception, match="Connection failed"):
            mock_param_manager.quick_connect(silent=True)


class TestParameterValidation:
    """Test cases for parameter validation."""

    def test_parameter_object_validation(self):
        """Test that Parameter objects are created correctly."""
        bbox_param = Parameter(
            "bounding_box",
            description="Test bounding box parameter",
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


class TestParameterMapping:
    """Test cases for endpoint parameter mapping."""

    def test_copernicus_explorer_mapping(self, temp_params_file):
        """Test parameter mapping for EOPF Explorer endpoint."""
        param_manager = ParameterManager(temp_params_file)
        param_manager.use_parameter_set("venice_lagoon")
        raw_params = param_manager.get_parameter_set()

        # Apply EOPF Explorer mapping
        mapped_params = param_manager.apply_endpoint_mapping(
            raw_params, "copernicus_explorer"
        )

        # Check collection mapping
        assert mapped_params["collection"].default == "sentinel-2-l2a"

        # Check band mapping (should have reflectance prefix and lowercase)
        expected_bands = [
            "reflectance|b02",
            "reflectance|b03",
            "reflectance|b04",
            "reflectance|b05",
            "reflectance|b08",
            "reflectance|b8a",
            "reflectance|b11",
        ]
        assert mapped_params["bands"].default == expected_bands

    def test_copernicus_dataspace_mapping(self, temp_params_file):
        """Test parameter mapping for Copernicus Data Space endpoint."""
        param_manager = ParameterManager(temp_params_file)
        param_manager.use_parameter_set("venice_lagoon")
        raw_params = param_manager.get_parameter_set()

        # Apply CDSE mapping
        mapped_params = param_manager.apply_endpoint_mapping(
            raw_params, "copernicus_dataspace"
        )

        # Check collection mapping (should keep SENTINEL2_L2A)
        assert mapped_params["collection"].default == "SENTINEL2_L2A"

    def test_ds_development_mapping(self, temp_params_file):
        """Test parameter mapping for Development Seed endpoint."""
        param_manager = ParameterManager(temp_params_file)
        param_manager.use_parameter_set("venice_lagoon")
        raw_params = param_manager.get_parameter_set()

        # Apply DS development mapping
        mapped_params = param_manager.apply_endpoint_mapping(
            raw_params, "ds_development"
        )

        # Check collection mapping
        assert mapped_params["collection"].default == "sentinel-2-l2a"

        # Check band mapping (should keep original bands)
        expected_bands = ["B02", "B03", "B04", "B05", "B08", "B8A", "B11"]
        assert mapped_params["bands"].default == expected_bands

    def test_unknown_endpoint_mapping(self, temp_params_file):
        """Test parameter mapping for unknown endpoint uses default mapper."""
        param_manager = ParameterManager(temp_params_file)
        param_manager.use_parameter_set("venice_lagoon")
        raw_params = param_manager.get_parameter_set()

        # Apply mapping for unknown endpoint
        mapped_params = param_manager.apply_endpoint_mapping(
            raw_params, "unknown_endpoint"
        )

        # Should return original parameters unchanged
        assert mapped_params == raw_params


class TestIntegration:
    """Integration tests for the complete workflow."""

    @patch("openeo_udp.endpoints.get_endpoint_connection")
    def test_complete_workflow_simulation(self, mock_get_connection, temp_params_file):
        """Test a complete workflow from parameter loading to connection."""
        # Mock external dependencies
        mock_connection = Mock()
        mock_get_connection.return_value = mock_connection

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
        connection, current_params = param_manager.quick_connect(
            param_set="venice_lagoon",
            endpoint="copernicus_explorer",
            silent=True
        )

        assert connection == mock_connection
        assert current_params["location_name"] == "Venice Lagoon"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
