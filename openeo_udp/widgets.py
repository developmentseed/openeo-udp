"""
Interactive widgets for OpenEO UDP notebooks.

This module provides reusable UI components for parameter selection and backend connection.
"""

import ipywidgets as widgets
import openeo
from IPython.display import clear_output, display

from .endpoints import get_all_endpoints


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
        available_endpoints[0] if available_endpoints else "eopf_explorer"
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

                # Use endpoint-specific connection function
                from .endpoints import get_endpoint_connection

                connection = get_endpoint_connection(selected_endpoint)

                state["connection"] = connection
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
    def get_results() -> tuple[openeo.Connection, dict]:
        """Get the connection and parameters as a tuple."""
        if state["connection"] is None:
            print(
                "⚠️ No connection found. Please click 'Connect & Load Parameters' first."
            )
            return None, None
        return state["connection"], state["current_params"]

    return get_results
