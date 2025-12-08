"""
Constants for mineral mapping projects
Element lists, deposit type mappings, and other configuration
"""

# ============================================================================
# ELEMENT LISTS
# ============================================================================

# Rare Earth Elements (REE)
REE_ELEMENTS = ['REO_PPM', 'CE_PPM', 'LA_PPM', 'ND_PPM', 'Y_PPM', 'PR_PPM', 'DY_PPM']

# Primary commodity elements
COMMODITY_ELEMENTS = ['CU_PPM', 'AU_PPM']

# Byproduct elements for copper mines
COPPER_BYPRODUCTS = ['MO_PPM', 'AG_PPM', 'AU_PPM', 'RE_PPM']

# Byproduct elements for gold mines
GOLD_BYPRODUCTS = ['AG_PPM', 'CU_PPM', 'AS_PPM', 'TE_PPM', 'SE_PPM']

# All elements to extract from concentration data
ALL_ELEMENTS = REE_ELEMENTS + COMMODITY_ELEMENTS + COPPER_BYPRODUCTS + GOLD_BYPRODUCTS

# ============================================================================
# ELEMENT NAMES
# ============================================================================

ELEMENT_NAMES = {
    'CE': 'Cerium',
    'LA': 'Lanthanum',
    'ND': 'Neodymium',
    'Y': 'Yttrium',
    'PR': 'Praseodymium',
    'DY': 'Dysprosium',
    'SM': 'Samarium',
    'GD': 'Gadolinium',
    'ER': 'Erbium',
    'EU': 'Europium',
    'CU': 'Copper',
    'AU': 'Gold',
    'MO': 'Molybdenum',
    'AG': 'Silver',
    'AS': 'Arsenic',
    'TE': 'Tellurium',
    'SE': 'Selenium',
    'RE': 'Rhenium',
}

# ============================================================================
# DEPOSIT TYPE MAPPINGS
# ============================================================================

# Map deposit type names (from Data S2) to sheet names (in Data S1)
DEPOSIT_TYPE_TO_SHEET = {
    'Reduced Intrusion Related Gold': 'RIRG',
    'Carlin-Type': 'Carlin',
    'Alkalic Epithermal Gold': 'Alkalic',
    'LS Epithermal Gold Silver': 'LSepi',
    'Mesozonal Orogenic Gold': 'OrogenicAu',
    'Orogenic Silver Lead Zinc Copper Antimony': 'OrogenicAg',
    'Skarn Gold': 'Skarn',
    'Climax-Type Porphyry Molybendenum': 'PorphyryMo',
    'Porphyry Copper Gold and Porphyry Copper Molybendum': 'PorphyryCu',
    'Sed Hosted Cu': 'SedCu',
    'Ultramafic intrusion/layered intrusion/conduit nickle copper PGE': 'MagmaticNi',
    'Bimodal Felsic Volcanogenic Massive Sulfide': 'BimodalAg',
    'Mississippi Valley Type Zn-Pb': 'MVT',
    'Siliclastic Cabonate Zn-Pb': 'SEDEX',
    'Carbonatite': 'REE',
    'Ultramafic Layered Intrusion PGE': 'UMPGE',
    'Superior-type banded iron formation': 'BIF',
}

# ============================================================================
# VISUALIZATION PARAMETERS
# ============================================================================

# Map bounds (Continental US + Alaska)
MAP_BOUNDS = {
    'lat_min': 24,
    'lat_max': 50,
    'lon_min': -125,
    'lon_max': -66,
}

# Size parameters for markers (log scale)
MARKER_SIZE_MIN = 8
MARKER_SIZE_MAX = 24

# Default plot dimensions
DEFAULT_PLOT_WIDTH = 1200
DEFAULT_PLOT_HEIGHT = 650

# Earth radius in meters for Web Mercator projection
EARTH_RADIUS_METERS = 6378137.0
