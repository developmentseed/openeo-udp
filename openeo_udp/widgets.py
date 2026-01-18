"""
Interactive widgets for OpenEO UDP notebooks.

This module provides reusable UI components for parameter selection and backend connection.
"""

import ipywidgets as widgets
import openeo
from IPython.display import clear_output, display

from .endpoints import get_all_endpoints


def get_connection(endpoint_url, auth_method="oidc"):
    """Get an OpenEO connection to the specified backend."""
    connection = openeo.connect(endpoint_url)

    if auth_method in ["oidc", "oidc_authorization_code"]:
        connection.authenticate_oidc_authorization_code()
    # For other auth methods, connection is returned without authentication

    return connection


def interactive_parameter_selection(
    param_manager, default_param_set=None, default_endpoint=None
):
    """
    Create an interactive parameter selection widget for OpenEO UDP notebooks.

    This function provides a user-friendly interface with dropdown menus for selecting
    parameter sets and OpenEO backends, plus a connect button to establish the connection
    and load the selected parameters.

    Parameters
    ----------
    param_manager : ParameterManager
        An initialized ParameterManager instance
    default_param_set : str, optional
        Default parameter set to select. If None, uses the first available set.
    default_endpoint : str, optional
        Default endpoint to select. If None, uses the first available endpoint.

    Returns
    -------
    callable
        A function that returns (connection, current_params) tuple when called.
        Call it after clicking 'Connect & Load Parameters' button.

    Examples
    --------
    >>> param_manager = ParameterManager('algorithm.params.py')
    >>> get_results = interactive_parameter_selection(param_manager)
    >>> # Widgets are automatically displayed, user clicks connect
    >>> connection, params = get_results()
    """

    # Clear any existing outputs from previous runs
    clear_output(wait=True)

    # Get available parameter sets and endpoints
    available_sets = param_manager.list_parameter_sets()
    endpoint_config = get_all_endpoints()
    available_endpoints = [
        name for name, config in endpoint_config.items() if config.get("enabled", True)
    ]

    # Set defaults
    default_param = default_param_set or available_sets[0] if available_sets else None
    default_ep = default_endpoint or (
        available_endpoints[0] if available_endpoints else "copernicus_explorer"
    )

    # Create dropdown options
    param_options = [
        (f"{params.get('location_name', name)}", name)
        for name, params in [
            (set_name, param_manager.get_parameter_set(set_name))
            for set_name in available_sets
        ]
    ]

    endpoint_options = [
        (
            f"{endpoint} ({endpoint_config[endpoint].get('url', 'URL not specified')})",
            endpoint,
        )
        for endpoint in available_endpoints
    ]

    # Create widgets
    endpoint_dropdown = widgets.Dropdown(
        options=endpoint_options,
        value=default_ep,
        description="OpenEO Backend:",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="600px"),
    )

    param_dropdown = widgets.Dropdown(
        options=param_options,
        value=default_param,
        description="Location:",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="600px"),
    )

    connect_button = widgets.Button(
        description="Connect & Load Parameters",
        button_style="success",
        layout=widgets.Layout(width="300px"),
    )

    output = widgets.Output()

    # Storage for connection and parameters
    state = {"connection": None, "current_params": None, "selected_endpoint": None}

    def on_connect_click(b):
        # Clear output and disable button
        output.clear_output(wait=True)
        connect_button.disabled = True

        selected_param_set = param_dropdown.value
        selected_endpoint = endpoint_dropdown.value

        # Get the display name for the selected parameter set
        selected_location_name = "Unknown Location"
        for display_name, param_name in param_options:
            if param_name == selected_param_set:
                selected_location_name = display_name
                break

        with output:
            print("🔄 Starting connection process...")

            try:
                # Apply parameter set
                param_manager.use_parameter_set(selected_param_set)
                print(f"✓ Parameter set applied: {selected_location_name}")

                # Get parameter set and apply endpoint mapping
                raw_params = param_manager.get_parameter_set()
                state["current_params"] = param_manager.apply_endpoint_mapping(
                    raw_params, selected_endpoint
                )
                print(
                    f"✓ Parameters loaded and mapped for endpoint: {selected_endpoint}"
                )

                # Connect to endpoint
                print(f"🔗 Connecting to {selected_endpoint}...")

                # Get endpoint configuration
                endpoint_cfg = endpoint_config.get(selected_endpoint, {})
                endpoint_url = endpoint_cfg.get("url", selected_endpoint)
                auth_method = endpoint_cfg.get("auth_method", "oidc")

                # Connect using the actual URL
                state["connection"] = get_connection(endpoint_url, auth_method)
                state["selected_endpoint"] = selected_endpoint
                print("✅ Connected successfully!")

                # Display parameter details
                print("\n📊 Parameter Details:")
                for key, value in state["current_params"].items():
                    if key != "location_name":
                        if hasattr(value, "default"):
                            print(f"  {key}: {value.default}")
                        else:
                            print(f"  {key}: {value}")

                print("\n✨ Ready to proceed!")

            except Exception as e:
                print(f"❌ Error: {str(e)}")
                import traceback

                print(f"Details: {traceback.format_exc()}")
            finally:
                connect_button.disabled = False

    # Attach the handler to the button
    connect_button.on_click(on_connect_click)

    # Display the widgets
    print("🎛️ Interactive Parameter Selection")
    display(endpoint_dropdown)
    display(param_dropdown)
    display(connect_button)
    display(output)

    # Return a simple function that gets the connection and parameters as a tuple
    def get_results():
        """Get the connection and parameters as a tuple."""
        if state["connection"] is None:
            print(
                "⚠️ No connection found. Please click 'Connect & Load Parameters' first."
            )
            return None, None
        return state["connection"], state["current_params"]

    return get_results


def quick_connect(param_manager, param_set=None, endpoint=None, silent=False):
    """
    Quickly connect to an OpenEO backend with specified parameters (non-interactive).

    This function provides a programmatic way to connect without UI widgets,
    useful for automated workflows or when the desired parameters are known.

    Parameters
    ----------
    param_manager : ParameterManager
        An initialized ParameterManager instance
    param_set : str, optional
        Parameter set to use. If None, uses the first available set.
    endpoint : str, optional
        Endpoint to connect to. If None, uses the first available endpoint.
    silent : bool, optional
        If True, suppress output messages. Default is False.

    Returns
    -------
    tuple
        (connection, current_params)

    Examples
    --------
    >>> param_manager = ParameterManager('algorithm.params.py')
    >>> connection, params = quick_connect(param_manager, 'venice_lagoon', 'copernicus_explorer')
    """

    available_sets = param_manager.list_parameter_sets()
    endpoint_config = get_all_endpoints()
    available_endpoints = [
        name for name, config in endpoint_config.items() if config.get("enabled", True)
    ]

    # Set defaults
    selected_param_set = param_set or available_sets[0] if available_sets else None
    selected_endpoint = endpoint or (
        available_endpoints[0] if available_endpoints else "copernicus_explorer"
    )

    if not silent:
        print(f"🔄 Connecting to {selected_endpoint}...")
        print(f"📍 Using parameter set: {selected_param_set}")

    try:
        # Apply parameter set
        param_manager.use_parameter_set(selected_param_set)
        raw_params = param_manager.get_parameter_set()

        # Apply endpoint mapping
        current_params = param_manager.apply_endpoint_mapping(
            raw_params, selected_endpoint
        )

        # Get endpoint configuration and connect
        endpoint_cfg = endpoint_config.get(selected_endpoint, {})
        endpoint_url = endpoint_cfg.get("url", selected_endpoint)
        auth_method = endpoint_cfg.get("auth_method", "oidc")

        # Connect to endpoint using the actual URL
        connection = get_connection(endpoint_url, auth_method)

        if not silent:
            print(f"✅ Successfully connected to {selected_endpoint}")
            print(
                f"✅ Parameters loaded and mapped for: {current_params.get('location_name', 'Unknown')}"
            )

            # Show mapping details if parameters were transformed
            if current_params != raw_params:
                print(f"🔄 Parameters mapped for endpoint {selected_endpoint}:")
                for param_name, param_value in current_params.items():
                    if param_name != "location_name" and hasattr(
                        param_value, "default"
                    ):
                        raw_value = raw_params.get(param_name)
                        if (
                            raw_value
                            and hasattr(raw_value, "default")
                            and raw_value.default != param_value.default
                        ):
                            print(
                                f"  {param_name}: {raw_value.default} -> {param_value.default}"
                            )

        return connection, current_params

    except Exception as e:
        if not silent:
            print(f"❌ Error: {str(e)}")
        raise
