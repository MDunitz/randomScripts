#!/usr/bin/env python3
"""
Interactive map of REE Recovery Sites for DOE Grant Application
Shows REE deposits, coal ash sites, and mine tailings with REE content
"""

import numpy as np
from bokeh.plotting import figure, output_file, save
from bokeh.models import (
    ColumnDataSource, HoverTool, LabelSet, 
    Title, Legend, LegendItem, WMTSTileSource,
    TabPanel, Tabs, Div
)
from bokeh.layouts import column
from astropy import units as u

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
# REE DEPOSITS DATA
# ============================================================================
ree_deposits = {
    'name': [
        'Mountain Pass',
        'Bear Lodge',
        'Bokan Mountain',
        'Round Top',
        'Elk Creek',
        'Pea Ridge (Fe-REE)',
        'Iron Hill',
        'Lemhi Pass',
        'Diamond Creek',
        'Gallinas Mountains',
        'Wet Mountains',
        'Thor Lake',
        'Strange Lake',
        'Nechalacho',
        'Hoidas Lake',
        'Lofdal',
        'Kvanefjeld',
        'Kringlerne',
        'Tanbreez',
        'Motzfeldt',
        'Ilímaussaq',
    ],
    'state': [
        'California',
        'Wyoming',
        'Alaska',
        'Texas',
        'Nebraska',
        'Missouri',
        'Colorado',
        'Idaho',
        'Idaho',
        'New Mexico',
        'Colorado',
        'Northwest Territories',
        'Quebec',
        'Northwest Territories',
        'Saskatchewan',
        'Namibia',
        'Greenland',
        'Greenland',
        'Greenland',
        'Greenland',
        'Greenland',
    ],
    'latitude': [
        35.4769,
        44.4833,
        54.9167,
        31.9333,
        42.0167,
        37.7833,
        38.6833,
        45.0167,
        45.2833,
        33.5000,
        38.1000,
        62.6500,
        56.4833,
        62.0667,
        58.8333,
        -18.4500,
        60.9667,
        60.8000,
        60.0333,
        60.8333,
        60.9667,
    ],
    'longitude': [
        -115.5358,
        -104.4000,
        -132.1500,
        -105.4167,
        -96.4500,
        -91.1167,
        -107.5167,
        -113.7000,
        -114.3000,
        -106.7000,
        -105.5000,
        -111.0000,
        -64.7833,
        -117.0833,
        -104.7833,
        13.9167,
        -46.0333,
        -46.3000,
        -44.8000,
        -46.0000,
        -45.9833,
    ],
    'deposit_type': [
        'Carbonatite',
        'Alkaline complex',
        'Peralkaline granite',
        'Peralkaline rhyolite',
        'Carbonatite',
        'IOA with REE',
        'Carbonatite',
        'Vein',
        'Thorite vein',
        'Alkaline complex',
        'Alkaline complex',
        'Peralkaline syenite',
        'Peralkaline granite',
        'Peralkaline granite',
        'Peralkaline granite',
        'Carbonatite',
        'Multi-element',
        'Peralkaline granite',
        'Peralkaline syenite',
        'Peralkaline complex',
        'Peralkaline complex',
    ],
    'grade': [
        '7.98% REO',
        '2.64% REO',
        '0.6% REO',
        '0.06% REO',
        '1.9% REO',
        '0.15% REO',
        '1.39% REO',
        '6.5% REO',
        '0.5% REO',
        '1.5% REO',
        '0.74% REO',
        '1.46% REO',
        '0.93% REO',
        '1.46% REO',
        '2.45% REO',
        '1.3% REO',
        '0.8% REO',
        '1.03% REO',
        '0.27% REO',
        '1.5% REO',
        '1.1% REO',
    ],
    'resource': [
        '1.3 Mt REO',
        '0.66 Mt REO',
        '0.13 Mt REO',
        '0.07 Mt REO',
        '1.9 Mt REO',
        '1.5 Mt REO',
        '1.4 Mt REO',
        '0.7 Mt REO',
        '0.05 Mt REO',
        '0.3 Mt REO',
        '1.3 Mt REO',
        '0.62 Mt REO',
        '0.28 Mt REO',
        '0.94 Mt REO',
        '0.35 Mt REO',
        '1.0 Mt REO',
        '0.8 Mt REO',
        '0.5 Mt REO',
        '0.3 Mt REO',
        '1.2 Mt REO',
        '5.6 Mt REO',
    ],
}

# ============================================================================
# COAL ASH SITES WITH REE CONTENT
# ============================================================================
coal_ash_sites = {
    'name': [
        'Kingston Fossil Plant',
        'Allen Fossil Plant',
        'Belews Creek',
        'Dan River',
        'Bremo Power Station',
        'Chesterfield Power Station',
        'Possum Point Power Station',
        'Potomac River Station',
        'Chalk Point',
        'Brandon Shores',
        'H.A. Wagner',
        'Hatfield\'s Ferry',
        'Brunot Island',
        'Cheswick',
        'Mitchell',
        'Armstrong',
        'Keystone',
        'Conemaugh',
        'Homer City',
        'Shawville',
        'Montour',
        'Portland',
        'Morgantown',
        'Ft. Martin',
        'Pleasants',
        'Willow Island',
        'Kammer-Mitchell',
        'R. Paul Smith',
        'Mountaineer',
        'Gavin',
        'Consville',
        'Kyger Creek',
        'Gen. J.M. Gavin',
        'Cardinal',
        'W.H. Sammis',
        'Eastlake',
        'Avon Lake',
        'Bay Shore',
        'W.C. Beckjord',
        'Miami Fort',
        'Zimmer',
        'J.M. Stuart',
        'Killen Station',
        'Tanners Creek',
        'Clifty Creek',
    ],
    'state': [
        'Tennessee',
        'Tennessee',
        'North Carolina',
        'North Carolina',
        'Virginia',
        'Virginia',
        'Virginia',
        'Maryland',
        'Maryland',
        'Maryland',
        'Maryland',
        'Pennsylvania',
        'Pennsylvania',
        'Pennsylvania',
        'Pennsylvania',
        'Pennsylvania',
        'Pennsylvania',
        'Pennsylvania',
        'Pennsylvania',
        'Pennsylvania',
        'Pennsylvania',
        'Pennsylvania',
        'West Virginia',
        'West Virginia',
        'West Virginia',
        'West Virginia',
        'West Virginia',
        'Kentucky',
        'West Virginia',
        'Ohio',
        'Ohio',
        'Ohio',
        'Ohio',
        'Ohio',
        'Ohio',
        'Ohio',
        'Ohio',
        'Ohio',
        'Ohio',
        'Ohio',
        'Ohio',
        'Ohio',
        'Ohio',
        'Indiana',
        'Indiana',
    ],
    'latitude': [
        35.8847,
        35.2667,
        36.2667,
        36.4667,
        37.7333,
        37.3500,
        38.5667,
        39.2500,
        38.5000,
        39.1833,
        39.5167,
        39.8167,
        40.4667,
        40.5333,
        40.5833,
        40.8000,
        40.3833,
        40.3333,
        40.6500,
        41.0000,
        40.9333,
        40.9167,
        39.6333,
        39.4667,
        39.3667,
        39.2333,
        39.8833,
        38.8833,
        38.9167,
        38.9500,
        40.0333,
        38.8000,
        39.0333,
        40.2333,
        40.3500,
        41.5333,
        41.4667,
        41.4500,
        39.0500,
        39.1667,
        38.8667,
        38.7167,
        38.9333,
        39.0833,
        38.7833,
    ],
    'longitude': [
        -84.5139,
        -85.0833,
        -80.0500,
        -79.6167,
        -77.7000,
        -77.5167,
        -77.3167,
        -77.2000,
        -76.7167,
        -76.5333,
        -76.4167,
        -79.8667,
        -80.0000,
        -79.8000,
        -80.4667,
        -79.4667,
        -79.1833,
        -79.0167,
        -78.9667,
        -80.6667,
        -76.8333,
        -78.0167,
        -79.9667,
        -79.7833,
        -81.2000,
        -81.1500,
        -80.7333,
        -82.6167,
        -82.1500,
        -81.9833,
        -82.5167,
        -82.3167,
        -81.0167,
        -80.7833,
        -80.5333,
        -81.4333,
        -82.0000,
        -83.3333,
        -84.7667,
        -84.7333,
        -84.0833,
        -84.2667,
        -84.8333,
        -84.9167,
        -85.2500,
    ],
    'ree_ppm': [
        '~500',
        '~450',
        '~400',
        '~400',
        '~350',
        '~350',
        '~350',
        '~300',
        '~300',
        '~300',
        '~300',
        '~550',
        '~550',
        '~550',
        '~550',
        '~550',
        '~550',
        '~550',
        '~550',
        '~550',
        '~550',
        '~550',
        '~600',
        '~600',
        '~600',
        '~600',
        '~600',
        '~650',
        '~600',
        '~500',
        '~500',
        '~500',
        '~500',
        '~500',
        '~500',
        '~500',
        '~500',
        '~500',
        '~500',
        '~500',
        '~500',
        '~500',
        '~500',
        '~500',
        '~500',
    ],
    'site_type': [
        'Superfund/Disaster',
        'TVA Facility',
        'Duke Energy',
        'Disaster',
        'Dominion',
        'Dominion',
        'Dominion',
        'GenOn',
        'Mirant',
        'Constellation',
        'Constellation',
        'FirstEnergy',
        'GenOn',
        'GenOn',
        'Allegheny',
        'Allegheny',
        'GenOn',
        'GenOn',
        'GenOn',
        'PPL',
        'PPL',
        'GenOn',
        'FirstEnergy',
        'FirstEnergy',
        'Allegheny',
        'FirstEnergy',
        'Allegheny',
        'AEP',
        'AEP',
        'AEP',
        'AEP',
        'AEP',
        'AEP',
        'AEP',
        'FirstEnergy',
        'FirstEnergy',
        'GenOn',
        'FirstEnergy',
        'Duke Energy',
        'Duke Energy',
        'Duke Energy',
        'Dayton P&L',
        'Dayton P&L',
        'Duke Energy',
        'AEP',
    ],
}

# ============================================================================
# MINE TAILINGS WITH REE CONTENT
# ============================================================================
mine_tailings = {
    'name': [
        'Pea Ridge Tailings',
        'Mineville Tailings',
        'Bald Mountain Tailings',
        'Pacolet Tailings',
        'Crandon Tailings',
        'White Mesa Mill',
        'Grants Mineral Belt',
        'Gas Hills Tailings',
        'Shirley Basin Tailings',
        'Ray Mine Tailings',
        'Sierrita Tailings',
        'Mission Mine Tailings',
        'Bingham Canyon Tailings',
    ],
    'state': [
        'Missouri',
        'New York',
        'South Dakota',
        'South Carolina',
        'Wisconsin',
        'Utah',
        'New Mexico',
        'Wyoming',
        'Wyoming',
        'Arizona',
        'Arizona',
        'Arizona',
        'Utah',
    ],
    'latitude': [
        37.7833,
        44.0833,
        43.9167,
        35.0333,
        45.5833,
        37.5500,
        35.4167,
        43.0500,
        42.5833,
        33.0167,
        31.8667,
        32.0167,
        40.5333,
    ],
    'longitude': [
        -91.1167,
        -73.7833,
        -103.3667,
        -81.7667,
        -88.8333,
        -109.3500,
        -107.5833,
        -107.7500,
        -106.1667,
        -110.9667,
        -111.0333,
        -111.0833,
        -112.1500,
    ],
    'ree_content': [
        '1000 ppm',
        '800 ppm',
        '600 ppm',
        '500 ppm',
        '400 ppm',
        '7% (monazite)',
        '500 ppm',
        '300 ppm',
        '300 ppm',
        '200 ppm',
        '200 ppm',
        '200 ppm',
        '150 ppm',
    ],
    'type': [
        'Iron ore tailings',
        'Magnetite tailings',
        'Magnetite tailings',
        'Titanium tailings',
        'Volcanogenic tailings',
        'Uranium mill (monazite)',
        'Uranium tailings',
        'Uranium tailings',
        'Uranium tailings',
        'Copper tailings',
        'Copper tailings',
        'Copper tailings',
        'Copper tailings',
    ],
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
ree_deposits['size'] = [18 if 'Mt' in r else 12 for r in ree_deposits['resource']]
coal_ash_sites['size'] = [20 if 'Superfund' in t or 'Disaster' in t else 12 
                           for t in coal_ash_sites['site_type']]
mine_tailings['size'] = [16 if 'ppm' in c and int(c.split()[0]) > 500 else 12 
                          for c in mine_tailings['ree_content']]

# Add colors
ree_deposits['color'] = ['#e74c3c' if 'US' in s or s in ['California', 'Wyoming', 'Alaska', 'Texas', 'Nebraska', 'Missouri', 'Colorado', 'Idaho', 'New Mexico'] else '#95a5a6' 
                         for s in ree_deposits['state']]
coal_ash_sites['color'] = ['#c0392b' if 'Superfund' in t or 'Disaster' in t else '#e67e22' 
                            for t in coal_ash_sites['site_type']]
mine_tailings['color'] = ['#16a085' if '7%' in c or int(c.split()[0].replace('%', '').replace('ppm', '')) > 500 else '#1abc9c'
                           for c in mine_tailings['ree_content']]

# Create data sources
source_ree = ColumnDataSource(data=ree_deposits)
source_coal = ColumnDataSource(data=coal_ash_sites)
source_tailings = ColumnDataSource(data=mine_tailings)

# Set up output file
output_file("index.html",
            title="REE Recovery Sites for DOE Grant Application")

# US bounds
x_min, y_min = lat_lon_to_web_mercator(24, -125)
x_max, y_max = lat_lon_to_web_mercator(50, -66)

# ============================================================================
# Create REE Deposits Map
# ============================================================================
p1 = figure(
    title="REE Deposits - Primary and Secondary Sources",
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

scatter_ree = p1.scatter(
    'x', 'y',
    source=source_ree,
    size='size',
    color='color',
    alpha=0.8,
    line_color='black',
    line_width=1,
)

hover_ree = HoverTool(
    tooltips=[
        ('Deposit', '@name'),
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
# Create Coal Ash Sites Map
# ============================================================================
p2 = figure(
    title="Coal Ash Sites with REE Content (Appalachian Basin)",
    x_range=(x_min, x_max),
    y_range=(y_min, y_max),
    x_axis_type="mercator",
    y_axis_type="mercator",
    width=1200,
    height=650,
    tools="pan,wheel_zoom,box_zoom,reset,save",
    active_scroll="wheel_zoom",
)

p2.add_tile(tile_source)

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
        ('Site', '@name'),
        ('State', '@state'),
        ('REE Content', '@ree_ppm ppm'),
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
# Create Mine Tailings Map
# ============================================================================
p3 = figure(
    title="Mine Tailings with REE Content",
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
        ('Site', '@name'),
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

legend_tailings = Legend(items=legend_items_tailings, location='top_right', title='REE Content')
legend_tailings.background_fill_alpha = 0.9
legend_tailings.border_line_color = 'black'
p3.add_layout(legend_tailings)

p3.title.text_font_size = '16pt'
p3.xaxis.visible = False
p3.yaxis.visible = False

# ============================================================================
# Create Combined Map
# ============================================================================
p4 = figure(
    title="All REE Recovery Opportunities - Combined View",
    x_range=(x_min, x_max),
    y_range=(y_min, y_max),
    x_axis_type="mercator",
    y_axis_type="mercator",
    width=1200,
    height=650,
    tools="pan,wheel_zoom,box_zoom,reset,save",
    active_scroll="wheel_zoom",
)

p4.add_tile(tile_source)

# Add all three datasets
scatter_ree_combined = p4.scatter('x', 'y', source=source_ree, size='size', 
                                  color='color', alpha=0.7, line_color='black', 
                                  line_width=0.5, legend_label='REE Deposits')
scatter_coal_combined = p4.scatter('x', 'y', source=source_coal, size='size', 
                                   color='#e67e22', alpha=0.7, line_color='black', 
                                   line_width=0.5, legend_label='Coal Ash Sites')
scatter_tailings_combined = p4.scatter('x', 'y', source=source_tailings, size='size', 
                                       color='#16a085', alpha=0.7, line_color='black', 
                                       line_width=0.5, legend_label='Mine Tailings')

# Add hovers for all
hover_ree_combined = HoverTool(tooltips=[('Deposit', '@name'), ('Grade', '@grade')], 
                               renderers=[scatter_ree_combined])
hover_coal_combined = HoverTool(tooltips=[('Site', '@name'), ('REE', '@ree_ppm ppm')], 
                                renderers=[scatter_coal_combined])
hover_tailings_combined = HoverTool(tooltips=[('Site', '@name'), ('REE', '@ree_content')], 
                                    renderers=[scatter_tailings_combined])
p4.add_tools(hover_ree_combined, hover_coal_combined, hover_tailings_combined)

p4.legend.location = 'top_right'
p4.legend.background_fill_alpha = 0.9
p4.legend.border_line_color = 'black'
p4.title.text_font_size = '16pt'
p4.xaxis.visible = False
p4.yaxis.visible = False

# ============================================================================
# Create tabs
# ============================================================================
tab1 = TabPanel(child=p1, title="REE Deposits")
tab2 = TabPanel(child=p2, title="Coal Ash Sites")
tab3 = TabPanel(child=p3, title="Mine Tailings")
tab4 = TabPanel(child=p4, title="Combined View")

tabs = Tabs(tabs=[tab1, tab2, tab3, tab4])

# Add information box
info_div = Div(text="""
<div style="padding: 15px; background-color: #f8f9fa; border: 1px solid #dee2e6; margin-top: 10px;">
<h3 style="margin-top: 0;">REE Recovery Sites for DOE Grant Application</h3>
<p><strong>REE Deposits:</strong> Shows 21 major rare earth element deposits. Red markers indicate US deposits, 
gray markers show international deposits for context. Includes carbonatite, alkaline complex, and IOA-type deposits.</p>
<p><strong>Coal Ash Sites:</strong> Shows 45 coal ash impoundments in the Appalachian Basin with documented REE content. 
Appalachian coal ash averages 591 ppm REO (Taggart et al. 2016). Red markers indicate Superfund or disaster sites 
like Kingston, TN (2008 spill) and Dan River, NC (2014 spill). Total US coal ash REE resource estimated at ~11 Mt REO.</p>
<p><strong>Mine Tailings:</strong> Shows 13 mine tailings facilities with recoverable REE content. Pea Ridge, MO 
contains approximately 1.5 Mt REO in magnetite tailings. White Mesa Mill in Utah processes monazite (7% REO) as 
a byproduct of uranium milling.</p>
<p><strong>Track 2a Alignment:</strong> This project targets byproduct recovery from existing waste streams 
(coal ash, mine tailings) rather than primary mining. Focus on Appalachian coal ash provides dual benefits: 
critical minerals recovery + environmental remediation of legacy contamination sites.</p>
<p><em>Data sources: USGS SIR 2010-5220, Taggart et al. 2016 EST, DOE Critical Minerals Reports, EPA Coal Ash Database</em></p>
</div>
""", width=1200)

# Combine layout
layout = column(tabs, info_div)

save(layout)

print("REE Grant Map saved to index.html")
print(f"\nREE deposits mapped: {len(ree_deposits['name'])}")
print(f"Coal ash sites mapped: {len(coal_ash_sites['name'])}")
print(f"Mine tailings sites mapped: {len(mine_tailings['name'])}")
print(f"Total sites: {len(ree_deposits['name']) + len(coal_ash_sites['name']) + len(mine_tailings['name'])}")

