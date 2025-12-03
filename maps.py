#!/usr/bin/env python3
"""
Critical Minerals Map of the United States
Maps deposits and contamination sites for: arsenic, antimony, bismuth, chromium, 
fluorine, gallium, germanium, graphite, indium, manganese, magnesium, niobium, 
scandium, tantalum, tin, tungsten, and yttrium.
"""

import numpy as np
from bokeh.plotting import figure, save, output_file
from bokeh.models import (ColumnDataSource, HoverTool, Legend, LegendItem,
                          Tabs, TabPanel, Title, Div, WMTSTileSource)
from bokeh.layouts import column

# Tile provider URL
TILE_URL = "https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png"

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
# COMPREHENSIVE CRITICAL MINERALS DATA
# ============================================================================

# Each entry: (name, lat, lon, element(s), type, status, notes)
deposits = [
    # TUNGSTEN DEPOSITS
    ("Pine Creek Mine", 37.42, -118.73, "Tungsten", "Skarn", "Historic", "CA - Bishop area, major WWII producer"),
    ("Stibnite-Yellow Pine", 44.93, -115.35, "Tungsten, Antimony, Gold", "Vein/Replacement", "Development", "ID - Largest US tungsten producer 1942-1944"),
    ("Climax Mine", 39.38, -106.17, "Tungsten, Molybdenum", "Porphyry", "Operating", "CO - Byproduct tungsten from Mo mining"),
    ("Strawberry Mine", 38.72, -119.85, "Tungsten", "Skarn", "Historic", "NV - Great Basin tungsten district"),
    ("Mill City District", 40.05, -118.12, "Tungsten", "Skarn", "Historic", "NV - Humboldt County"),
    ("Hamme District", 36.52, -78.35, "Tungsten", "Vein", "Historic", "NC/VA - Tungsten Queen Mine, produced 1.1 Mt WO3"),
    ("Johnson Lake Mine", 39.05, -114.30, "Tungsten", "Skarn", "Historic", "NV - Snake Range, Great Basin NP area"),
    ("Pilot Mountains", 40.15, -117.85, "Tungsten", "Skarn", "Historic", "NV - Pershing County"),
    ("Golconda Summit", 40.95, -117.50, "Tungsten", "Skarn", "Historic", "NV - Humboldt County"),
    ("Bishop District", 37.35, -118.40, "Tungsten", "Skarn", "Historic", "CA - Inyo County, multiple mines"),
    ("Luckey Baldwin", 34.15, -117.65, "Tungsten", "Vein", "Historic", "CA - San Bernardino County"),
    ("Atolia District", 35.05, -117.60, "Tungsten", "Vein", "Historic", "CA - San Bernardino County"),
    ("Idaho Springs", 39.75, -105.52, "Tungsten", "Vein", "Historic", "CO - Clear Creek County"),
    ("Boulder County District", 40.02, -105.35, "Tungsten", "Vein", "Historic", "CO - Multiple tungsten veins"),
    ("Butte District", 46.02, -112.52, "Tungsten, Manganese", "Vein/Replacement", "Historic", "MT - Polymetallic district"),
    
    # ANTIMONY DEPOSITS
    ("Stibnite Gold Project", 44.93, -115.35, "Antimony, Gold, Tungsten", "Vein/Replacement", "Development", "ID - Largest US antimony resource, DOD-backed"),
    ("Scrafford Mine", 64.92, -147.52, "Antimony", "Vein", "Historic", "AK - Fairbanks district, WWI-WWII producer"),
    ("Sliscovich Mine", 64.75, -165.35, "Antimony", "Vein", "Historic", "AK - Nome area"),
    ("Estelle Project", 61.85, -152.65, "Antimony, Gold", "Vein", "Exploration", "AK - West Susitna, high-grade Sb discovery"),
    ("Treasure Creek", 64.95, -147.60, "Antimony, Gold", "Vein", "Exploration", "AK - Felix Gold project"),
    ("Coyote Antimony District", 38.35, -112.85, "Antimony", "Vein", "Historic", "UT - Piute County"),
    ("White Caps Mine", 38.05, -117.05, "Antimony, Gold, Arsenic", "Carbonate Replacement", "Historic", "NV - Manhattan district"),
    
    # GRAPHITE DEPOSITS
    ("Graphite Creek", 65.02, -164.85, "Graphite", "Disseminated Flake", "Development", "AK - Largest US graphite deposit, 10+ Mt @ 7.8%"),
    ("Coosa Graphite", 32.95, -86.25, "Graphite", "Disseminated Flake", "Development", "AL - Alabama Graphite Belt, 26 Mt @ 2.89%"),
    ("Bama Mine", 32.78, -86.65, "Graphite", "Disseminated Flake", "Historic", "AL - Chilton County, highest quality in AL"),
    ("Ceylon Mine", 33.08, -86.15, "Graphite", "Disseminated Flake", "Exploration", "AL - Coosa County, WWII producer"),
    ("Burnet District", 30.75, -98.25, "Graphite", "Disseminated Flake", "Historic", "TX - Llano County, Southwestern Graphite Co."),
    ("Ticonderoga", 43.85, -73.42, "Graphite", "Vein", "Historic", "NY - Adirondack graphite deposits"),
    ("Chester County", 39.95, -75.75, "Graphite", "Disseminated Flake", "Historic", "PA - Eastern Pennsylvania deposits"),
    
    # CHROMIUM DEPOSITS  
    ("Stillwater Complex", 45.38, -110.05, "Chromium, PGE, Cobalt, Nickel", "Stratiform", "Operating/Resource", "MT - Only US chromium resource, chromite seams A-G"),
    ("Red Mountain", 61.05, -145.60, "Chromium", "Podiform", "Resource", "AK - Chugach Mountains ophiolite"),
    ("Goodnews Bay", 59.12, -161.58, "Chromium", "Podiform/Placer", "Historic", "AK - Platinum placer with chromite"),
    
    # MANGANESE DEPOSITS
    ("Emily Deposit", 46.72, -93.95, "Manganese", "Sedimentary", "Development", "MN - Cuyuna Range, richest US Mn deposit"),
    ("Butte Mn District", 46.02, -112.52, "Manganese", "Vein/Replacement", "Historic", "MT - Polymetallic with Mn"),
    ("Artillery Peak", 34.35, -113.55, "Manganese", "Sedimentary", "Historic", "AZ - Mohave County"),
    ("Three Kids Mine", 36.08, -114.88, "Manganese", "Sedimentary", "Historic", "NV - Clark County, WWII strategic producer"),
    
    # GALLIUM/GERMANIUM DEPOSITS (typically byproduct)
    ("Apex Mine", 37.15, -113.55, "Gallium, Germanium", "Carbonate Replacement", "Historic", "UT - Only US primary Ga/Ge producer (1980s)"),
    ("Round Top", 31.05, -105.48, "Gallium, REE, Lithium", "Peralkaline", "Development", "TX - Polymetallic with significant Ga resource"),
    ("Red Dog Mine", 68.08, -162.85, "Germanium, Indium (byproduct)", "Sedex Zn-Pb", "Operating", "AK - World's largest zinc mine, Ge potential"),
    ("Clarksville Zn Refinery", 36.53, -87.35, "Gallium, Germanium (recovery)", "Processing", "Development", "TN - Nyrstar planning Ga/Ge recovery from waste"),
    ("East Tennessee Zn District", 36.15, -83.55, "Germanium, Indium (byproduct)", "MVT Zn-Pb", "Operating", "TN - Multiple Zn mines with Ge potential"),
    
    # NIOBIUM DEPOSITS
    ("Elk Creek", 40.28, -96.18, "Niobium, REE, Scandium, Titanium", "Carbonatite", "Development", "NE - 2nd largest US REE, major Nb resource"),
    ("Bokan Mountain", 54.92, -132.15, "Niobium, REE, Tantalum", "Peralkaline", "Development", "AK - HREE-enriched, Dotson Ridge deposit"),
    
    # TANTALUM DEPOSITS
    ("Round Top", 31.05, -105.48, "Tantalum, REE, Gallium", "Peralkaline", "Development", "TX - 480+ Mt @ 67 ppm Ta2O5"),
    ("Tin Mountain Pegmatite", 43.78, -103.55, "Tantalum, Tin, Niobium", "LCT Pegmatite", "Historic", "SD - Black Hills, columbite-tantalite"),
    ("Etta Mine", 43.85, -103.52, "Tantalum, Lithium", "LCT Pegmatite", "Historic", "SD - Black Hills, giant spodumene crystals"),
    ("Kings Mountain", 35.25, -81.35, "Tantalum, Lithium, Tin", "LCT Pegmatite", "Historic", "NC - Largest US Li pegmatite, Ta coproduct"),
    
    # TIN DEPOSITS
    ("Lost River", 65.47, -167.15, "Tin, Tungsten, Fluorine", "Greisen/Skarn", "Resource", "AK - Seward Peninsula, significant Sn"),
    ("Cape Creek", 65.55, -167.25, "Tin", "Placer", "Historic", "AK - Seward Peninsula placers"),
    ("Tinton", 44.45, -104.02, "Tin", "Pegmatite/Greisen", "Historic", "SD - Black Hills tin district"),
    ("Irish Creek", 37.95, -79.15, "Tin", "Greisen", "Historic", "VA - Rockbridge County"),
    ("Franklin Mountains", 31.90, -106.48, "Tin", "Vein", "Resource", "TX - El Paso County"),
    
    # SCANDIUM (often with REE or Ni-Co)
    ("Elk Creek", 40.28, -96.18, "Scandium, Niobium, REE", "Carbonatite", "Development", "NE - Major Sc resource with REE"),
    
    # YTTRIUM (typically with REE)
    ("Bokan Mountain", 54.92, -132.15, "Yttrium, HREE", "Peralkaline", "Development", "AK - HREE-enriched including Y"),
    ("Bear Lodge", 44.48, -104.45, "Yttrium, REE", "Carbonatite", "Development", "WY - REE with Y enrichment"),
    ("Round Top", 31.05, -105.48, "Yttrium, HREE", "Peralkaline", "Development", "TX - Y-enriched REE deposit"),
    
    # MAGNESIUM
    ("Gabbs", 38.87, -117.92, "Magnesium", "Evaporite/Brine", "Historic", "NV - Magnesite deposits"),
    ("Brine Lake", 40.85, -112.22, "Magnesium", "Brine", "Operating", "UT - Great Salt Lake Mg production"),
    ("Dolomite deposits", 36.15, -115.15, "Magnesium", "Carbonate", "Resource", "NV - Various dolomite sources"),
    
    # FLUORINE (Fluorspar)
    ("Illinois-Kentucky District", 37.55, -88.35, "Fluorine", "MVT", "Historic", "IL/KY - Rosiclare, largest US fluorspar producer"),
    ("Spor Mountain", 39.75, -113.20, "Fluorine, Beryllium", "Volcanogenic", "Operating", "UT - Brush Wellman operation"),
    ("Jamestown District", 40.12, -105.38, "Fluorine", "Vein", "Historic", "CO - Boulder County"),
    ("Northgate District", 40.98, -105.95, "Fluorine", "Vein", "Historic", "CO - Jackson County"),
    
    # BISMUTH (typically byproduct)
    ("Park City", 40.65, -111.50, "Bismuth (byproduct)", "Carbonate Replacement", "Historic", "UT - Bi from Ag-Pb-Zn mining"),
    ("Coeur d'Alene", 47.55, -116.15, "Bismuth (byproduct)", "Vein", "Historic", "ID - Bi from Ag-Pb mining"),
]

# CONTAMINATION SITES (arsenic, chromium, other metals from mining/smelting)
contamination_sites = [
    # ARSENIC CONTAMINATION
    ("Bunker Hill Superfund", 47.55, -116.15, "Arsenic, Lead, Cadmium", "Mining/Smelting", "Cleanup Ongoing", "ID - 1,500 sq mi, one of largest Superfund sites"),
    ("Iron King Mine Superfund", 34.45, -112.25, "Arsenic, Lead", "Mining", "Cleanup Ongoing", "AZ - Dewey-Humboldt"),
    ("Summitville Mine", 37.42, -106.60, "Arsenic, Heavy Metals", "Mining", "Superfund", "CO - Acid mine drainage disaster"),
    ("California Gulch", 39.25, -106.30, "Arsenic, Lead, Zinc", "Mining/Smelting", "Superfund", "CO - Leadville historic mining"),
    ("Colorado Smelter", 38.28, -104.60, "Arsenic, Lead", "Smelting", "Superfund", "CO - Pueblo residential contamination"),
    ("Arsenic Mine Kent NY", 41.45, -73.70, "Arsenic", "Mining", "Superfund", "NY - Historic arsenic mine"),
    ("Brinton Mine", 37.05, -80.35, "Arsenic", "Mining", "Historic", "VA - Floyd County, only VA arsenic producer"),
    ("Gold Hill District", 40.50, -112.05, "Arsenic", "Mining", "Historic Producer", "UT - Tooele County, WWI-WWII As production"),
    ("Kennecott North Zone", 40.75, -112.15, "Arsenic, Lead, Heavy Metals", "Mining/Smelting", "Superfund", "UT - Salt Lake Valley contamination"),
    ("Eureka Mills", 39.95, -112.12, "Arsenic, Lead", "Mining/Smelting", "Superfund", "UT - Historic mining town"),
    ("Davenport Smelter", 40.57, -111.85, "Arsenic, Lead", "Smelting", "Superfund", "UT - Sandy, residential contamination"),
    ("Clear Creek/Central City", 39.80, -105.52, "Arsenic, Lead, Zinc", "Mining", "Superfund", "CO - Historic gaming towns"),
    ("Captain Jack Mill", 40.07, -105.52, "Arsenic, Heavy Metals", "Mining", "Superfund", "CO - Boulder County watershed"),
    ("Midvale Slag", 40.62, -111.90, "Arsenic, Lead", "Smelting", "Superfund", "UT - Sharon Steel site"),
    
    # CHROMIUM CONTAMINATION
    ("Hinkley CA", 34.93, -117.18, "Chromium VI", "Industrial", "Contaminated", "CA - PG&E, famous Erin Brockovich case"),
    ("Chrome Plating Sites", 33.95, -118.25, "Chromium VI", "Industrial", "Various", "CA - Multiple LA area sites"),
    ("Jersey City Cr Sites", 40.73, -74.08, "Chromium", "Industrial", "Superfund", "NJ - Multiple chrome processing sites"),
    
    # MULTI-ELEMENT MINING CONTAMINATION
    ("Tar Creek", 36.98, -94.85, "Lead, Zinc, Cadmium", "Mining", "Superfund", "OK - Tri-State Mining District"),
    ("Coeur d'Alene Basin", 47.55, -116.15, "Lead, Arsenic, Zinc, Cadmium", "Mining", "Superfund", "ID - Silver Valley, extensive contamination"),
    ("Anaconda Smelter", 46.12, -112.95, "Arsenic, Lead, Heavy Metals", "Smelting", "Superfund", "MT - 300+ sq miles affected"),
    ("Silver Bow Creek/Butte", 46.02, -112.52, "Arsenic, Lead, Copper, Zinc", "Mining", "Superfund", "MT - Berkeley Pit, historic mining"),
    ("Blackbird Mine", 45.10, -114.42, "Arsenic, Cobalt, Copper", "Mining", "Superfund", "ID - Lemhi County"),
    ("Yellow Pine Pit", 44.93, -115.35, "Arsenic, Antimony", "Mining", "Remediation Planned", "ID - Legacy contamination at Stibnite"),
]

# ============================================================================
# CREATE MAP
# ============================================================================

output_file("/home/claude/critical_minerals_usa.html", title="US Critical Minerals Map")

# US bounds in Web Mercator
us_x_min, us_y_min = lat_lon_to_web_mercator(24.5, -125)
us_x_max, us_y_max = lat_lon_to_web_mercator(49.5, -66.5)
alaska_x_min, alaska_y_min = lat_lon_to_web_mercator(51, -180)
alaska_x_max, alaska_y_max = lat_lon_to_web_mercator(71, -130)

# Element color mapping
element_colors = {
    "Tungsten": "#E63946",           # Red
    "Antimony": "#F4A261",           # Orange
    "Graphite": "#2A2A2A",           # Dark gray
    "Chromium": "#457B9D",           # Steel blue
    "Manganese": "#9B2335",          # Burgundy
    "Gallium": "#7209B7",            # Purple
    "Germanium": "#3A0CA3",          # Deep purple
    "Niobium": "#4361EE",            # Blue
    "Tantalum": "#4CC9F0",           # Cyan
    "Tin": "#90BE6D",                # Green
    "Scandium": "#F72585",           # Pink
    "Yttrium": "#B5179E",            # Magenta
    "Magnesium": "#06D6A0",          # Teal
    "Fluorine": "#FFD166",           # Yellow
    "Bismuth": "#118AB2",            # Ocean blue
    "Arsenic": "#DC2F02",            # Bright red (contamination)
    "Multi-element": "#6C757D",      # Gray
}

# Status shapes
status_markers = {
    "Operating": "circle",
    "Development": "diamond",
    "Exploration": "triangle",
    "Historic": "square",
    "Resource": "hex",
}

# Process deposit data
deposit_data = {
    'x': [], 'y': [], 'name': [], 'elements': [], 'type': [], 
    'status': [], 'notes': [], 'color': [], 'size': []
}

for name, lat, lon, elements, dep_type, status, notes in deposits:
    x, y = lat_lon_to_web_mercator(lat, lon)
    deposit_data['x'].append(x)
    deposit_data['y'].append(y)
    deposit_data['name'].append(name)
    deposit_data['elements'].append(elements)
    deposit_data['type'].append(dep_type)
    deposit_data['status'].append(status)
    deposit_data['notes'].append(notes)
    
    # Determine primary element for coloring
    primary = elements.split(',')[0].strip()
    if primary in element_colors:
        deposit_data['color'].append(element_colors[primary])
    else:
        deposit_data['color'].append(element_colors.get("Multi-element", "#6C757D"))
    
    # Size based on status
    if status == "Operating":
        deposit_data['size'].append(18)
    elif status == "Development":
        deposit_data['size'].append(15)
    else:
        deposit_data['size'].append(12)

deposit_source = ColumnDataSource(deposit_data)

# Process contamination data
contam_data = {
    'x': [], 'y': [], 'name': [], 'elements': [], 'type': [], 
    'status': [], 'notes': [], 'color': [], 'size': []
}

for name, lat, lon, elements, cont_type, status, notes in contamination_sites:
    x, y = lat_lon_to_web_mercator(lat, lon)
    contam_data['x'].append(x)
    contam_data['y'].append(y)
    contam_data['name'].append(name)
    contam_data['elements'].append(elements)
    contam_data['type'].append(cont_type)
    contam_data['status'].append(status)
    contam_data['notes'].append(notes)
    contam_data['color'].append("#DC2F02")  # Red for all contamination
    
    if "Superfund" in status:
        contam_data['size'].append(16)
    else:
        contam_data['size'].append(12)

contam_source = ColumnDataSource(contam_data)

# ============================================================================
# TAB 1: ALL DEPOSITS BY ELEMENT
# ============================================================================

def create_deposits_map():
    p = figure(
        title="Critical Mineral Deposits in the United States",
        x_range=(us_x_min - 500000, us_x_max + 500000),
        y_range=(us_y_min - 200000, us_y_max + 200000),
        x_axis_type="mercator",
        y_axis_type="mercator",
        tools="pan,wheel_zoom,box_zoom,reset,save",
        width=1200,
        height=700
    )
    
    # Add tile provider
    tile_source = WMTSTileSource(url=TILE_URL)
    p.add_tile(tile_source)
    
    # Plot deposits
    deposits_glyph = p.scatter(
        'x', 'y', source=deposit_source,
        size='size', color='color', alpha=0.8,
        line_color='white', line_width=0.5
    )
    
    # Add hover tool
    hover = HoverTool(
        tooltips=[
            ("Name", "@name"),
            ("Elements", "@elements"),
            ("Type", "@type"),
            ("Status", "@status"),
            ("Notes", "@notes")
        ],
        renderers=[deposits_glyph]
    )
    p.add_tools(hover)
    
    # Create legend manually with actual data points placed off-screen
    legend_items = []
    x_off = us_x_min - 2e7
    y_off = us_y_min - 2e7
    
    for element, color in element_colors.items():
        if element not in ["Arsenic", "Multi-element"]:
            dummy_source = ColumnDataSource({'x': [x_off], 'y': [y_off]})
            r = p.scatter('x', 'y', source=dummy_source, size=10, 
                         fill_color=color, line_color='white', line_width=0.5)
            legend_items.append(LegendItem(label=element, renderers=[r]))
    
    legend = Legend(items=legend_items, location="top_right", 
                   click_policy="hide", title="Primary Element")
    p.add_layout(legend, 'right')
    
    p.xaxis.visible = False
    p.yaxis.visible = False
    
    return p

# ============================================================================
# TAB 2: CONTAMINATION SITES
# ============================================================================

def create_contamination_map():
    p = figure(
        title="Mining & Industrial Contamination Sites (Arsenic, Chromium, Heavy Metals)",
        x_range=(us_x_min - 500000, us_x_max + 500000),
        y_range=(us_y_min - 200000, us_y_max + 200000),
        x_axis_type="mercator",
        y_axis_type="mercator",
        tools="pan,wheel_zoom,box_zoom,reset,save",
        width=1200,
        height=700
    )
    
    tile_source = WMTSTileSource(url=TILE_URL)
    p.add_tile(tile_source)
    
    # Plot contamination sites as X markers
    contam_glyph = p.scatter(
        'x', 'y', source=contam_source,
        size='size', color='color', alpha=0.8,
        marker='x', line_width=3
    )
    
    hover = HoverTool(
        tooltips=[
            ("Site", "@name"),
            ("Contaminants", "@elements"),
            ("Source", "@type"),
            ("Status", "@status"),
            ("Notes", "@notes")
        ],
        renderers=[contam_glyph]
    )
    p.add_tools(hover)
    
    p.xaxis.visible = False
    p.yaxis.visible = False
    
    return p

# ============================================================================
# TAB 3: COMBINED VIEW
# ============================================================================

def create_combined_map():
    p = figure(
        title="All Critical Mineral Sites: Deposits and Contamination",
        x_range=(us_x_min - 500000, us_x_max + 500000),
        y_range=(us_y_min - 200000, us_y_max + 200000),
        x_axis_type="mercator",
        y_axis_type="mercator",
        tools="pan,wheel_zoom,box_zoom,reset,save",
        width=1200,
        height=700
    )
    
    tile_source = WMTSTileSource(url=TILE_URL)
    p.add_tile(tile_source)
    
    # Plot deposits
    deposits_glyph = p.scatter(
        'x', 'y', source=deposit_source,
        size='size', color='color', alpha=0.7,
        line_color='white', line_width=0.5,
        legend_label="Mineral Deposits"
    )
    
    # Plot contamination
    contam_glyph = p.scatter(
        'x', 'y', source=contam_source,
        size='size', color='color', alpha=0.8,
        marker='x', line_width=3,
        legend_label="Contamination Sites"
    )
    
    hover_deposits = HoverTool(
        tooltips=[
            ("Name", "@name"),
            ("Elements", "@elements"),
            ("Type", "@type"),
            ("Status", "@status"),
            ("Notes", "@notes")
        ],
        renderers=[deposits_glyph]
    )
    
    hover_contam = HoverTool(
        tooltips=[
            ("Site", "@name"),
            ("Contaminants", "@elements"),
            ("Source", "@type"),
            ("Status", "@status"),
            ("Notes", "@notes")
        ],
        renderers=[contam_glyph]
    )
    
    p.add_tools(hover_deposits, hover_contam)
    
    p.legend.location = "top_right"
    p.legend.click_policy = "hide"
    
    p.xaxis.visible = False
    p.yaxis.visible = False
    
    return p

# ============================================================================
# TAB 4: ALASKA FOCUS
# ============================================================================

def create_alaska_map():
    p = figure(
        title="Critical Mineral Deposits in Alaska",
        x_range=(alaska_x_min, alaska_x_max),
        y_range=(alaska_y_min, alaska_y_max),
        x_axis_type="mercator",
        y_axis_type="mercator",
        tools="pan,wheel_zoom,box_zoom,reset,save",
        width=1200,
        height=700
    )
    
    tile_source = WMTSTileSource(url=TILE_URL)
    p.add_tile(tile_source)
    
    # Filter for Alaska deposits (lat > 51)
    ak_data = {k: [] for k in deposit_data.keys()}
    for i, (name, lat, lon, elements, dep_type, status, notes) in enumerate(deposits):
        if lat > 51:
            for k in deposit_data.keys():
                ak_data[k].append(deposit_data[k][i])
    
    ak_source = ColumnDataSource(ak_data)
    
    ak_glyph = p.scatter(
        'x', 'y', source=ak_source,
        size='size', color='color', alpha=0.8,
        line_color='white', line_width=1
    )
    
    hover = HoverTool(
        tooltips=[
            ("Name", "@name"),
            ("Elements", "@elements"),
            ("Type", "@type"),
            ("Status", "@status"),
            ("Notes", "@notes")
        ],
        renderers=[ak_glyph]
    )
    p.add_tools(hover)
    
    p.xaxis.visible = False
    p.yaxis.visible = False
    
    return p

# Create tabs
tab1 = TabPanel(child=create_deposits_map(), title="Mineral Deposits")
tab2 = TabPanel(child=create_contamination_map(), title="Contamination Sites")
tab3 = TabPanel(child=create_combined_map(), title="Combined View")
tab4 = TabPanel(child=create_alaska_map(), title="Alaska Focus")

# Add info panel
info_html = """
<div style="padding: 10px; background: #f8f9fa; border-radius: 5px; margin-bottom: 10px;">
<h3 style="margin-top: 0;">US Critical Minerals Map</h3>
<p><strong>Elements mapped:</strong> Arsenic, Antimony, Bismuth, Chromium, Fluorine, Gallium, 
Germanium, Graphite, Indium, Manganese, Magnesium, Niobium, Scandium, Tantalum, Tin, Tungsten, Yttrium</p>
<p><strong>Data sources:</strong> USGS USMIN database, USGS Earth MRI, EPA Superfund, state geological surveys</p>
<p><strong>Notes:</strong> Many elements (Ga, Ge, In, Bi) are recovered as byproducts from zinc/copper processing. 
Contamination sites primarily show arsenic and heavy metal pollution from historic mining and smelting.</p>
</div>
"""

info_div = Div(text=info_html, width=1200)
tabs = Tabs(tabs=[tab1, tab2, tab3, tab4])

layout = column(info_div, tabs)
save(layout)

print("Map saved to /home/claude/critical_minerals_usa.html")