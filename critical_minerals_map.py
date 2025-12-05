#!/usr/bin/env python3
"""
Critical Minerals Map of the United States
Maps deposits and contamination sites for multiple critical elements
"""

import numpy as np
import pandas as pd
from bokeh.plotting import figure, save, output_file
from bokeh.models import (ColumnDataSource, HoverTool, Legend, LegendItem,
                          Tabs, TabPanel, Div, WMTSTileSource)
from bokeh.layouts import column

# Coordinate conversion function
def lat_lon_to_web_mercator(lat, lon):
    """Convert latitude/longitude to Web Mercator coordinates."""
    r = 6378137.0  # Earth radius in meters
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    x = r * lon_rad
    y = r * np.log(np.tan(np.pi/4 + lat_rad/2))
    return x, y

# ============================================================================
# LOAD DATA FROM CSV FILES
# ============================================================================
csv_files = [
    'data/critical_minerals_tungsten.csv',
    'data/critical_minerals_antimony.csv',
    'data/critical_minerals_graphite.csv',
    'data/critical_minerals_chromium_manganese.csv',
    'data/critical_minerals_gallium_germanium.csv',
    'data/critical_minerals_rare_earths.csv',
    'data/critical_minerals_tantalum_tin.csv',
    'data/critical_minerals_fluorine.csv',
    'data/critical_minerals_contamination.csv',
]

# Read and combine all CSV files
dfs = []
for csv_file in csv_files:
    try:
        df = pd.read_csv(csv_file)
        dfs.append(df)
        print(f"Loaded {len(df)} sites from {csv_file}")
    except Exception as e:
        print(f"Warning: Could not load {csv_file}: {e}")

# Combine all dataframes
combined_df = pd.concat(dfs, ignore_index=True)
print(f"\nTotal sites loaded: {len(combined_df)}")

# Separate critical minerals from contamination sites
minerals_df = combined_df[combined_df['Deposit_Type'] != 'Superfund'].copy()
contamination_df = combined_df[combined_df['Deposit_Type'] == 'Superfund'].copy()

print(f"Critical minerals sites: {len(minerals_df)}")
print(f"Contamination sites: {len(contamination_df)}")

# Create deposits_data dictionary for critical minerals
deposits_data = {
    'name': minerals_df['Name'].tolist(),
    'latitude': minerals_df['Latitude'].tolist(),
    'longitude': minerals_df['Longitude'].tolist(),
    'element': minerals_df['Element'].tolist(),
    'type': minerals_df['Deposit_Type'].tolist(),
    'status': minerals_df['Status'].tolist(),
    'notes': minerals_df['Notes'].tolist(),
}

# Create contamination_data dictionary
contamination_data = {
    'name': contamination_df['Name'].tolist(),
    'latitude': contamination_df['Latitude'].tolist(),
    'longitude': contamination_df['Longitude'].tolist(),
    'element': contamination_df['Element'].tolist(),
    'type': contamination_df['Deposit_Type'].tolist(),
    'status': contamination_df['Status'].tolist(),
    'notes': contamination_df['Notes'].tolist(),
}

# Convert coordinates for critical minerals
x, y = lat_lon_to_web_mercator(
    np.array(deposits_data['latitude']),
    np.array(deposits_data['longitude'])
)
deposits_data['x'] = x
deposits_data['y'] = y

# Convert coordinates for contamination sites
x_contam, y_contam = lat_lon_to_web_mercator(
    np.array(contamination_data['latitude']),
    np.array(contamination_data['longitude'])
)
contamination_data['x'] = x_contam
contamination_data['y'] = y_contam

# Color mapping by element type
element_colors = {
    'Tungsten': '#8e44ad',
    'Tungsten/Antimony': '#9b59b6',
    'Tungsten/Molybdenum': '#6c3483',
    'Antimony': '#e74c3c',
    'Graphite': '#34495e',
    'Chromium/PGM': '#16a085',
    'Manganese': '#1abc9c',
    'Gallium/Germanium': '#f39c12',
    'Niobium/REE': '#d35400',
    'Scandium/REE': '#e67e22',
    'Tantalum': '#c0392b',
    'Tin/Tungsten': '#8e44ad',
    'Tin': '#95a5a6',
    'Tantalum/Tin': '#7f8c8d',
    'Fluorine': '#3498db',
    'Fluorine/Beryllium': '#2980b9',
    'As/Pb/Zn': '#e74c3c',
    'As/Cu': '#c0392b',
    'As/Cu/Zn': '#a93226',
    'Pb/Zn': '#922b21',
}

deposits_data['color'] = [element_colors.get(e, '#95a5a6') for e in deposits_data['element']]
contamination_data['color'] = [element_colors.get(e, '#e74c3c') for e in contamination_data['element']]

# Size by status
status_sizes = {
    'Operating': 16,
    'Development': 14,
    'Exploration': 12,
    'Historic': 10,
    'Remediation': 18,
}
deposits_data['size'] = [status_sizes.get(s, 10) for s in deposits_data['status']]
contamination_data['size'] = [status_sizes.get(s, 18) for s in contamination_data['status']]

# Create data sources
source = ColumnDataSource(data=deposits_data)
source_contamination = ColumnDataSource(data=contamination_data)

# Set up output
output_file("critical_minerals_usa.html",
            title="US Critical Minerals Map")

# US bounds
x_min, y_min = lat_lon_to_web_mercator(24, -125)
x_max, y_max = lat_lon_to_web_mercator(50, -66)

# ============================================================================
# Create Main Map
# ============================================================================
p1 = figure(
    title="US Critical Minerals Deposits and Contamination Sites",
    x_range=(x_min, x_max),
    y_range=(y_min, y_max),
    x_axis_type="mercator",
    y_axis_type="mercator",
    width=1200,
    height=650,
    tools="pan,wheel_zoom,box_zoom,reset,save",
    active_scroll="wheel_zoom",
)

tile_url = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
tile_source = WMTSTileSource(url=tile_url, attribution="© OpenStreetMap contributors")
p1.add_tile(tile_source)

scatter = p1.scatter(
    'x', 'y',
    source=source,
    size='size',
    color='color',
    alpha=0.8,
    line_color='black',
    line_width=1,
)

hover = HoverTool(
    tooltips=[
        ('Site', '@name'),
        ('Element(s)', '@element'),
        ('Type', '@type'),
        ('Status', '@status'),
        ('Notes', '@notes'),
    ],
    renderers=[scatter],
)
p1.add_tools(hover)

p1.title.text_font_size = '16pt'
p1.xaxis.visible = False
p1.yaxis.visible = False

# Create legend manually with visible markers
legend_items = []
off_x = x_min - 1e7
off_y = y_min

unique_elements = ['Tungsten', 'Antimony', 'Graphite', 'Chromium/PGM',
                   'Manganese', 'Gallium/Germanium', 'Tantalum/Tin', 'REE', 'Fluorine']
legend_colors = ['#8e44ad', '#e74c3c', '#34495e', '#16a085',
                 '#1abc9c', '#f39c12', '#7f8c8d', '#e67e22', '#3498db']

for i, (label, color) in enumerate(zip(unique_elements, legend_colors)):
    ds = ColumnDataSource(data={'x': [off_x], 'y': [off_y + i*5e5]})
    sc = p1.scatter('x', 'y', source=ds, fill_color=color, size=12,
                    line_color='black', line_width=1)
    legend_items.append(LegendItem(label=label, renderers=[sc]))

legend = Legend(items=legend_items, location='top_right', title='Element Type')
legend.background_fill_alpha = 0.9
legend.border_line_color = 'black'
p1.add_layout(legend)

# ============================================================================
# Alaska Focused Map
# ============================================================================
x_min_ak, y_min_ak = lat_lon_to_web_mercator(55, -170)
x_max_ak, y_max_ak = lat_lon_to_web_mercator(68, -140)

p2 = figure(
    title="Alaska Critical Minerals - Detailed View",
    x_range=(x_min_ak, x_max_ak),
    y_range=(y_min_ak, y_max_ak),
    x_axis_type="mercator",
    y_axis_type="mercator",
    width=1200,
    height=650,
    tools="pan,wheel_zoom,box_zoom,reset,save",
    active_scroll="wheel_zoom",
)

p2.add_tile(tile_source)

scatter_ak = p2.scatter(
    'x', 'y',
    source=source,
    size='size',
    color='color',
    alpha=0.8,
    line_color='black',
    line_width=1,
)

hover_ak = HoverTool(
    tooltips=[
        ('Site', '@name'),
        ('Element(s)', '@element'),
        ('Type', '@type'),
        ('Status', '@status'),
        ('Notes', '@notes'),
    ],
    renderers=[scatter_ak],
)
p2.add_tools(hover_ak)

p2.title.text_font_size = '16pt'
p2.xaxis.visible = False
p2.yaxis.visible = False

# ============================================================================
# Contamination Sites Map
# ============================================================================
p3 = figure(
    title="US Contamination Sites - Superfund Mining Legacy",
    x_range=(x_min, x_max),
    y_range=(y_min, y_max),
    x_axis_type="mercator",
    y_axis_type="mercator",
    width=1200,
    height=650,
    tools="pan,wheel_zoom,box_zoom,reset,save",
    active_scroll="wheel_zoom",
)

p3.add_tile(tile_source)

scatter_contam = p3.scatter(
    'x', 'y',
    source=source_contamination,
    size='size',
    color='color',
    alpha=0.8,
    line_color='black',
    line_width=1,
)

hover_contam = HoverTool(
    tooltips=[
        ('Site', '@name'),
        ('Contaminants', '@element'),
        ('Type', '@type'),
        ('Status', '@status'),
        ('Notes', '@notes'),
    ],
    renderers=[scatter_contam],
)
p3.add_tools(hover_contam)

p3.title.text_font_size = '16pt'
p3.xaxis.visible = False
p3.yaxis.visible = False

# Legend for contamination
legend_items_contam = []
contam_elements = ['As/Pb/Zn', 'As/Cu', 'As/Cu/Zn', 'Pb/Zn']
contam_colors = ['#e74c3c', '#c0392b', '#a93226', '#922b21']

for i, (label, color) in enumerate(zip(contam_elements, contam_colors)):
    ds = ColumnDataSource(data={'x': [off_x], 'y': [off_y + i*5e5]})
    sc = p3.scatter('x', 'y', source=ds, fill_color=color, size=18,
                    line_color='black', line_width=1)
    legend_items_contam.append(LegendItem(label=label, renderers=[sc]))

legend_contam = Legend(items=legend_items_contam, location='top_right', title='Contaminant Type')
legend_contam.background_fill_alpha = 0.9
legend_contam.border_line_color = 'black'
p3.add_layout(legend_contam)

# ============================================================================
# Create tabs
# ============================================================================
tab1 = TabPanel(child=p1, title="Critical Minerals")
tab2 = TabPanel(child=p2, title="Alaska Focus")
tab3 = TabPanel(child=p3, title="Contamination Sites")

tabs = Tabs(tabs=[tab1, tab2, tab3])

# Add information
info_div = Div(text="""
<div style="padding: 15px; background-color: #f8f9fa; border: 1px solid #dee2e6; margin-top: 10px;">
<h3 style="margin-top: 0;">US Critical Minerals & Contamination Sites Map</h3>
<p><strong>Critical Minerals Mapped:</strong> Tungsten, Antimony, Graphite, Chromium, Manganese,
Gallium, Germanium, Niobium, Scandium, Tantalum, Tin, Fluorine, Beryllium</p>
<p><strong>Key Deposits:</strong></p>
<ul>
<li><strong>Tungsten:</strong> Stibnite (ID) - Largest US resource; Pine Creek (CA) - Historic WWII producer</li>
<li><strong>Antimony:</strong> Stibnite Gold Project (ID) - DOD-backed, only future US source</li>
<li><strong>Graphite:</strong> Graphite Creek (AK) - 10.3 Mt resource; 100% import reliant currently</li>
<li><strong>Chromium:</strong> Stillwater Complex (MT) - Only US chromium resource</li>
<li><strong>Manganese:</strong> Emily deposit (MN) - Richest US manganese deposit</li>
<li><strong>Gallium/Germanium:</strong> Tennessee Zinc - Byproduct recovery from zinc processing</li>
<li><strong>REE:</strong> Elk Creek (NE), Bear Lodge (WY) - Major rare earth element deposits</li>
</ul>
<p><strong>Contamination Sites Tab:</strong> EPA Superfund sites with arsenic, lead,
copper, and zinc contamination from historic mining and smelting operations. See the "Contamination Sites" tab for details.</p>
<p><em>Data sources: USGS Mineral Resources Data, EPA Superfund Database, Mining Company Reports</em></p>
<p><em>See REFERENCES.md for detailed citations</em></p>
</div>
""", width=1200)

layout = column(tabs, info_div)

save(layout)

print("\n✓ Critical Minerals Map saved to critical_minerals_usa.html")
print(f"Critical minerals sites: {len(deposits_data['name'])}")
print(f"Contamination sites: {len(contamination_data['name'])}")
print(f"Total sites mapped: {len(deposits_data['name']) + len(contamination_data['name'])}")
