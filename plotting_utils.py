"""
Plotting utilities for mineral maps
Functions for creating interactive Bokeh plots
"""

import numpy as np
from bokeh.plotting import figure
from bokeh.models import (
    ColumnDataSource, HoverTool, WMTSTileSource
)
from constants import ELEMENT_NAMES, EARTH_RADIUS_METERS


def lat_lon_to_web_mercator(lat, lon):
    """Convert lat/lon to Web Mercator coordinates (meters)."""
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    x = EARTH_RADIUS_METERS * lon_rad
    y = EARTH_RADIUS_METERS * np.log(np.tan(np.pi/4 + lat_rad/2))
    return x, y


def create_element_tooltips(elements_list):
    """Generate tooltip list with element names and concentrations"""
    tooltips = [
        ('Mine', '@{Mine Name}'),
        ('State', '@State'),
        ('Deposit Type', '@{Deposit Type}'),
        ('Primary Commodity', '@{Main Product Commodity}'),
        ('', ''),  # Blank line
    ]

    # Add element concentration tooltips
    for elem in elements_list:
        elem_code = elem.replace('_PPM', '')

        if elem_code == 'REO':
            label = 'Total REE Oxides (REO)'
        else:
            name = ELEMENT_NAMES.get(elem_code, elem_code)
            label = f'{name} ({elem_code})'

        tooltips.append((label, f'@{{{elem}}}{{0.0}} ppm'))

    tooltips.extend([
        ('', ''),  # Blank line
        ('Coordinate Source', '@{Coordinate_Source}'),
        ('Verification', '@{Verification_Status}'),
    ])

    return tooltips


def create_mine_plot(title, x_range, y_range, width=1200, height=650):
    """Create a base figure for mine plotting with map tiles"""
    p = figure(
        title=title,
        x_range=x_range,
        y_range=y_range,
        x_axis_type="mercator",
        y_axis_type="mercator",
        width=width,
        height=height,
        tools="pan,wheel_zoom,box_zoom,reset,save",
        active_scroll="wheel_zoom",
    )

    # Add map tiles
    tile_url = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
    tile_source = WMTSTileSource(url=tile_url, attribution="© OpenStreetMap contributors")
    p.add_tile(tile_source)

    # Style
    p.title.text_font_size = '16pt'
    p.xaxis.visible = False
    p.yaxis.visible = False

    return p


def plot_mines_by_deposit_type(plot, data_df, size_col='size', default_size=16):
    """
    Plot mines grouped by deposit type with interactive legend

    Args:
        plot: Bokeh figure object
        data_df: DataFrame with mine data including 'Deposit Type', 'x', 'y', 'color', size_col
        size_col: Column name for marker size (default: 'size')
        default_size: Default size if size_col not in data (default: 16)

    Returns:
        dict: Mapping of deposit type to scatter renderer
    """
    scatter_renderers = {}

    for dep_type in data_df['Deposit Type'].unique():
        if np.isnan(dep_type) if isinstance(dep_type, float) else False:
            continue

        subset = data_df[data_df['Deposit Type'] == dep_type]
        source_subset = ColumnDataSource(data=subset.to_dict('list'))

        # Use size column if it exists, otherwise use default
        size = size_col if size_col in subset.columns else default_size

        renderer = plot.scatter(
            'x', 'y',
            source=source_subset,
            size=size,
            color='color',
            alpha=0.8,
            line_color='black',
            line_width=1,
            legend_label=str(dep_type)[:35] + ('...' if len(str(dep_type)) > 35 else '')
        )
        scatter_renderers[dep_type] = renderer

    return scatter_renderers


def configure_legend(plot, location='top_right', placement='right'):
    """Configure plot legend with consistent styling"""
    plot.legend.location = location
    plot.legend.click_policy = 'hide'
    plot.legend.background_fill_alpha = 0.9
    plot.legend.border_line_color = 'black'
    plot.legend.title = 'Deposit Type'
    plot.add_layout(plot.legend[0], placement)


def add_hover_tool(plot, elements_list, renderers):
    """Add hover tool with element tooltips to plot"""
    hover = HoverTool(
        tooltips=create_element_tooltips(elements_list),
        renderers=renderers,
    )
    plot.add_tools(hover)
    return hover
