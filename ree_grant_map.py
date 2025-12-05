#!/usr/bin/env python3
"""
Interactive map of REE Recovery Sites for DOE Grant Application
Shows REE deposits, coal ash sites, and mine tailings with REE content
"""

import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.models import (
    ColumnDataSource, HoverTool, LabelSet,
    Title, Legend, LegendItem, WMTSTileSource,
    TabPanel, Tabs, Div
)
from bokeh.layouts import column

# Convert latitude/longitude to Web Mercator projection
def lat_lon_to_web_mercator(lat, lon):
    """Convert lat/lon to Web Mercator coordinates (meters)."""
    r = 6378137.0  # Earth radius in meters
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    x = r * lon_rad
    y = r * np.log(np.tan(np.pi/4 + lat_rad/2))
    return x, y

# ============================================================================
# LOAD DATA FROM CSV FILES
# ============================================================================
print("Loading data from CSV files...")

# Load REE deposits
ree_df = pd.read_csv('data/ree_deposits.csv')
print(f"Loaded {len(ree_df)} REE deposits")

# Load coal ash sites
coal_df = pd.read_csv('data/coal_ash_sites.csv')
print(f"Loaded {len(coal_df)} coal ash sites")

# Load mine tailings
tailings_df = pd.read_csv('data/mine_tailings.csv')
print(f"Loaded {len(tailings_df)} mine tailings sites")

# Create REE deposits data dictionary
ree_deposits = {
    'name': ree_df['Name'].tolist(),
    'state': ree_df['State/Region'].tolist(),
    'latitude': ree_df['Latitude'].tolist(),
    'longitude': ree_df['Longitude'].tolist(),
    'deposit_type': ree_df['Deposit_Type'].tolist(),
    'grade': ree_df['Grade'].tolist(),
    'resource': ree_df['Resource'].tolist(),
}

# Create coal ash sites data dictionary
coal_ash_sites = {
    'name': coal_df['Name'].tolist(),
    'state': coal_df['State'].tolist(),
    'latitude': coal_df['Latitude'].tolist(),
    'longitude': coal_df['Longitude'].tolist(),
    'ree_content': coal_df['REE_Content_ppm'].tolist(),
    'site_type': coal_df['Site_Type'].tolist(),
}

# Create mine tailings data dictionary
mine_tailings = {
    'name': tailings_df['Name'].tolist(),
    'state': tailings_df['State'].tolist(),
    'latitude': tailings_df['Latitude'].tolist(),
    'longitude': tailings_df['Longitude'].tolist(),
    'ree_content': tailings_df['REE_Content'].tolist(),
    'type': tailings_df['Type'].tolist(),
}

# Convert coordinates to Web Mercator
for dataset in [ree_deposits, coal_ash_sites, mine_tailings]:
    x, y = lat_lon_to_web_mercator(
        np.array(dataset['latitude']),
        np.array(dataset['longitude'])
    )
    dataset['x'] = x
    dataset['y'] = y

# Add marker sizes
ree_deposits['size'] = [18 if 'Mt' in str(r) else 12 for r in ree_deposits['resource']]
coal_ash_sites['size'] = [20 if 'Superfund' in str(t) or 'Disaster' in str(t) else 12
                           for t in coal_ash_sites['site_type']]
mine_tailings['size'] = [16 if 'ppm' in str(c) and int(str(c).split()[0]) > 500 else 12
                          for c in mine_tailings['ree_content']]

# Add colors
us_states = ['California', 'Wyoming', 'Alaska', 'Texas', 'Nebraska', 'Missouri',
             'Colorado', 'Idaho', 'New Mexico', 'Montana', 'Illinois', 'Indiana', 'Kentucky']
ree_deposits['color'] = ['#e74c3c' if any(state in str(s) for state in us_states) else '#95a5a6'
                         for s in ree_deposits['state']]
coal_ash_sites['color'] = ['#c0392b' if 'Superfund' in str(t) or 'Disaster' in str(t) else '#e67e22'
                            for t in coal_ash_sites['site_type']]
mine_tailings['color'] = ['#16a085' if '7%' in str(c) or (str(c).replace('~','').replace('ppm','').strip().isdigit() and int(str(c).replace('~','').replace('ppm','').strip()) > 500) else '#1abc9c'
                           for c in mine_tailings['ree_content']]

# Create data sources
source_ree = ColumnDataSource(data=ree_deposits)
source_coal = ColumnDataSource(data=coal_ash_sites)
source_tailings = ColumnDataSource(data=mine_tailings)

# Set up output file
output_file("index.html", title="REE Recovery Sites Map")

# Set up map bounds (US + international sites)
x_min, y_min = lat_lon_to_web_mercator(10, -180)
x_max, y_max = lat_lon_to_web_mercator(75, -40)

# ============================================================================
# REE DEPOSITS MAP
# ============================================================================
p1 = figure(
    title="Rare Earth Element Deposits - US and International",
    x_range=(x_min, x_max),
    y_range=(y_min, y_max),
    x_axis_type="mercator",
    y_axis_type="mercator",
    width=1200,
    height=650,
    tools="pan,wheel_zoom,box_zoom,reset,save",
    active_scroll="wheel_zoom",
)

# Add map tiles
tile_url = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
tile_source = WMTSTileSource(url=tile_url, attribution="© OpenStreetMap contributors")
p1.add_tile(tile_source)

# Plot REE deposits
scatter_ree = p1.scatter(
    'x', 'y',
    source=source_ree,
    size='size',
    color='color',
    alpha=0.8,
    line_color='black',
    line_width=1,
)

# Add hover tool
hover_ree = HoverTool(
    tooltips=[
        ('Name', '@name'),
        ('State/Region', '@state'),
        ('Type', '@deposit_type'),
        ('Grade', '@grade'),
        ('Resource', '@resource'),
    ],
    renderers=[scatter_ree],
)
p1.add_tools(hover_ree)

# Legend
legend_items_ree = []
off_x = x_min - 1e7
off_y = y_min

for i, (label, color, size) in enumerate([
    ('US REE Deposit', '#e74c3c', 18),
    ('International REE', '#95a5a6', 12),
]):
    ds = ColumnDataSource(data={'x': [off_x], 'y': [off_y + i*5e5]})
    sc = p1.scatter('x', 'y', source=ds, fill_color=color, size=size,
                    line_color='black', line_width=1)
    legend_items_ree.append(LegendItem(label=label, renderers=[sc]))

legend_ree = Legend(items=legend_items_ree, location='top_right', title='Deposit Location')
legend_ree.background_fill_alpha = 0.9
legend_ree.border_line_color = 'black'
p1.add_layout(legend_ree)

p1.title.text_font_size = '16pt'
p1.xaxis.visible = False
p1.yaxis.visible = False

# ============================================================================
# COAL ASH SITES MAP
# ============================================================================
# US bounds for coal ash sites
x_min_us, y_min_us = lat_lon_to_web_mercator(24, -125)
x_max_us, y_max_us = lat_lon_to_web_mercator(50, -66)

p2 = figure(
    title="Coal Ash Sites with REE Content - US",
    x_range=(x_min_us, x_max_us),
    y_range=(y_min_us, y_max_us),
    x_axis_type="mercator",
    y_axis_type="mercator",
    width=1200,
    height=650,
    tools="pan,wheel_zoom,box_zoom,reset,save",
    active_scroll="wheel_zoom",
)

p2.add_tile(tile_source)

# Plot coal ash sites
scatter_coal = p2.scatter(
    'x', 'y',
    source=source_coal,
    size='size',
    color='color',
    alpha=0.8,
    line_color='black',
    line_width=1,
)

hover_coal = HoverTool(
    tooltips=[
        ('Name', '@name'),
        ('State', '@state'),
        ('REE Content', '@ree_content'),
        ('Type', '@site_type'),
    ],
    renderers=[scatter_coal],
)
p2.add_tools(hover_coal)

# Legend
legend_items_coal = []
for i, (label, color, size) in enumerate([
    ('Superfund/Disaster Site', '#c0392b', 20),
    ('Operating Coal Ash Facility', '#e67e22', 12),
]):
    ds = ColumnDataSource(data={'x': [off_x], 'y': [off_y + i*5e5]})
    sc = p2.scatter('x', 'y', source=ds, fill_color=color, size=size,
                    line_color='black', line_width=1)
    legend_items_coal.append(LegendItem(label=label, renderers=[sc]))

legend_coal = Legend(items=legend_items_coal, location='top_right', title='Site Type')
legend_coal.background_fill_alpha = 0.9
legend_coal.border_line_color = 'black'
p2.add_layout(legend_coal)

p2.title.text_font_size = '16pt'
p2.xaxis.visible = False
p2.yaxis.visible = False

# ============================================================================
# MINE TAILINGS MAP
# ============================================================================
p3 = figure(
    title="Mine Tailings with REE Content - US",
    x_range=(x_min_us, x_max_us),
    y_range=(y_min_us, y_max_us),
    x_axis_type="mercator",
    y_axis_type="mercator",
    width=1200,
    height=650,
    tools="pan,wheel_zoom,box_zoom,reset,save",
    active_scroll="wheel_zoom",
)

p3.add_tile(tile_source)

# Plot mine tailings
scatter_tailings = p3.scatter(
    'x', 'y',
    source=source_tailings,
    size='size',
    color='color',
    alpha=0.8,
    line_color='black',
    line_width=1,
)

hover_tailings = HoverTool(
    tooltips=[
        ('Name', '@name'),
        ('State', '@state'),
        ('REE Content', '@ree_content'),
        ('Type', '@type'),
    ],
    renderers=[scatter_tailings],
)
p3.add_tools(hover_tailings)

# Legend
legend_items_tailings = []
for i, (label, color, size) in enumerate([
    ('High REE (>500 ppm or monazite)', '#16a085', 16),
    ('Moderate REE (<500 ppm)', '#1abc9c', 12),
]):
    ds = ColumnDataSource(data={'x': [off_x], 'y': [off_y + i*5e5]})
    sc = p3.scatter('x', 'y', source=ds, fill_color=color, size=size,
                    line_color='black', line_width=1)
    legend_items_tailings.append(LegendItem(label=label, renderers=[sc]))

legend_tailings = Legend(items=legend_items_tailings, location='top_right', title='REE Grade')
legend_tailings.background_fill_alpha = 0.9
legend_tailings.border_line_color = 'black'
p3.add_layout(legend_tailings)

p3.title.text_font_size = '16pt'
p3.xaxis.visible = False
p3.yaxis.visible = False

# ============================================================================
# CREATE TABS
# ============================================================================
tab1 = TabPanel(child=p1, title="REE Deposits")
tab2 = TabPanel(child=p2, title="Coal Ash Sites")
tab3 = TabPanel(child=p3, title="Mine Tailings")

tabs = Tabs(tabs=[tab1, tab2, tab3])

# Add information
info_div = Div(text="""
<div style="padding: 15px; background-color: #f8f9fa; border: 1px solid #dee2e6; margin-top: 10px;">
<h3 style="margin-top: 0;">REE Recovery Sites for DOE Grant Application</h3>
<p><strong>REE Deposits:</strong> Shows 21 major rare earth element deposits. Red markers indicate US deposits,
gray markers show international deposits for context. Includes carbonatite, alkaline complex, and IOA-type deposits.</p>
<p><strong>Coal Ash Sites:</strong> Shows coal ash impoundments with documented REE content across three major US coal basins:
<ul>
<li><strong>Appalachian Basin</strong> (PA, WV, KY, OH, IN): ~591 ppm REO average</li>
<li><strong>Illinois Basin</strong> (IL, IN, KY): ~403 ppm REO average</li>
<li><strong>Powder River Basin</strong> (WY, MT): ~337 ppm REO average (but 70% extraction rate vs 30% for other basins)</li>
</ul>
Red markers indicate Superfund or disaster sites like Kingston, TN (2008 spill) and Dan River, NC (2014 spill).
Total US coal ash REE resource estimated at ~11 Mt REO (UT Austin 2024).</p>
<p><strong>Mine Tailings:</strong> Shows 13 mine tailings facilities with recoverable REE content. Pea Ridge, MO
contains approximately 1.5 Mt REO in magnetite tailings. White Mesa Mill in Utah processes monazite (7% REO) as
a byproduct of uranium milling.</p>
<p><strong>Track 2a Alignment:</strong> This project targets byproduct recovery from existing waste streams
(coal ash, mine tailings) rather than primary mining. Focus on coal ash provides dual benefits:
critical minerals recovery + environmental remediation of legacy contamination sites.</p>
<p><em>Data sources: USGS SIR 2010-5220, Taggart et al. 2016 EST, Hower et al. 2020-2021, DOE Critical Minerals Reports,
EPA Coal Ash Database, NETL Coal Ash Database</em></p>
<p><em>See REFERENCES.md for detailed citations</em></p>
</div>
""", width=1200)

# Combine layout
layout = column(tabs, info_div)

save(layout)

print("\nREE Grant Map saved to index.html")
print(f"\nREE deposits mapped: {len(ree_deposits['name'])}")
print(f"Coal ash sites mapped: {len(coal_ash_sites['name'])}")
print(f"Mine tailings sites mapped: {len(mine_tailings['name'])}")
print(f"Total sites: {len(ree_deposits['name']) + len(coal_ash_sites['name']) + len(mine_tailings['name'])}")
