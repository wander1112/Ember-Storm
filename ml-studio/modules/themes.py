"""
ML Studio — Analytics Platform: Distinct Color Themes Engine
============================================================
Implements three genuine, distinct, vibrant, and professional design systems:

1. Theme A: Regression — Emerald Oasis (WHO Health)
   - Deep emerald: #0B6E4F
   - Vibrant jade: #10B981
   - Lime highlight: #D9F99D
   - Pale mint background: #F0FDF4
   - Forest typography: #15352B

2. Theme B: Classification — Coral Bloom (Maternal Care)
   - Raspberry: #BE3455
   - Vibrant coral: #F05A78
   - Warm peach: #FFB38A
   - Ivory background: #FFF0E8
   - Deep berry typography: #55253B

3. Theme C: Clustering — Calm Arctic Teal (CTG Telemetry)
   - Primary teal: #367F83
   - Secondary dusty blue: #719CB8
   - Soft seafoam: #CDEBE4
   - Pale ice-blue background: #F1F7FA
   - White card background: #FFFFFF
   - Muted lavender accent: #B6AEDB
   - Dark slate text: #293B4A
   - Secondary text: #657786
   - Subtle border: #DCE7ED
   - Soft turquoise chart accent: #70C9C0
"""

def get_theme_css(track_selection: str) -> str:
    """
    Returns custom CSS that completely and comprehensively transforms the entire application
    according to the selected problem track.
    """
    if "Classification" in track_selection:
        # -------------------------------------------------------------
        # THEME B: CORAL BLOOM (Classification — Maternal Care)
        # -------------------------------------------------------------
        c_primary = "#BE3455"        # Raspberry
        c_secondary = "#F05A78"      # Vibrant Coral
        c_accent = "#FFB38A"         # Warm Peach
        c_bg_canvas = "#FFF0E8"      # Ivory Peach Background
        c_bg_sidebar = "#FFE8DF"     # Soft Peach Sidebar
        c_card_bg = "#FFFFFF"        # Card background
        c_card_border = "#F05A78"    # Coral border
        c_text_head = "#55253B"      # Deep Berry Typography
        c_text_body = "#6E334D"      # Muted Berry Typography
        c_text_muted = "#914C6A"     # Soft Berry Subtext
        c_tab_active_bg = "#FFE2D5"  # Active tab background
        c_glow = "rgba(240, 90, 120, 0.35)"
        is_dark = False

        card_1_bg = "linear-gradient(135deg, #FFF1F2 0%, #FFE4E6 100%)"
        card_1_border = "#BE3455"
        card_1_val = "#BE3455"

        card_2_bg = "linear-gradient(135deg, #FFF0E8 0%, #FFE2D5 100%)"
        card_2_border = "#F05A78"
        card_2_val = "#F05A78"

        card_3_bg = "linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%)"
        card_3_border = "#FB923C"
        card_3_val = "#C2410C"

        card_4_bg = "linear-gradient(135deg, #FDF2F8 0%, #FCE7F3 100%)"
        card_4_border = "#DB2777"
        card_4_val = "#9D174D"

    elif "Clustering" in track_selection:
        # -------------------------------------------------------------
        # THEME C: CALM ARCTIC TEAL (Clustering — CTG Telemetry)
        # -------------------------------------------------------------
        c_primary = "#367F83"        # Primary Teal
        c_secondary = "#719CB8"      # Secondary Dusty Blue
        c_accent = "#70C9C0"         # Soft Turquoise Accent
        c_bg_canvas = "#F1F7FA"      # Pale Ice-Blue Canvas
        c_bg_sidebar = "#FFFFFF"     # Clean White Sidebar
        c_card_bg = "#FFFFFF"        # White Card Background
        c_card_border = "#DCE7ED"    # Subtle Border
        c_text_head = "#293B4A"      # Dark Slate Typography
        c_text_body = "#293B4A"      # Dark Slate Body
        c_text_muted = "#657786"     # Secondary Text
        c_tab_active_bg = "#CDEBE4"  # Soft Seafoam Active State
        c_glow = "rgba(41, 59, 74, 0.05)"
        is_dark = False

        # Metric cards: white with subtle borders and small colored top accents
        card_1_bg = "#FFFFFF"
        card_1_border = "#367F83"    # Teal top accent
        card_1_val = "#367F83"

        card_2_bg = "#FFFFFF"
        card_2_border = "#719CB8"    # Dusty blue top accent
        card_2_val = "#386583"

        card_3_bg = "#FFFFFF"
        card_3_border = "#B6AEDB"    # Muted lavender top accent
        card_3_val = "#5B5282"

        card_4_bg = "#FFFFFF"
        card_4_border = "#70C9C0"    # Soft turquoise top accent
        card_4_val = "#247169"

    else:
        # -------------------------------------------------------------
        # THEME A: EMERALD OASIS (Regression — WHO Health)
        # -------------------------------------------------------------
        c_primary = "#0B6E4F"        # Deep Emerald
        c_secondary = "#10B981"      # Vibrant Jade
        c_accent = "#D9F99D"         # Lime Highlight
        c_bg_canvas = "#F0FDF4"      # Pale Mint Background
        c_bg_sidebar = "#E6F7ED"     # Soft Mint Sidebar
        c_card_bg = "#FFFFFF"        # Card background
        c_card_border = "#0B6E4F"    # Deep Emerald border
        c_text_head = "#15352B"      # Forest Typography
        c_text_body = "#1E4738"      # Forest Body Text
        c_text_muted = "#2C5E4E"     # Forest Subtext
        c_tab_active_bg = "#D1FAE5"  # Active tab background
        c_glow = "rgba(16, 185, 129, 0.35)"
        is_dark = False

        card_1_bg = "linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%)"
        card_1_border = "#0B6E4F"
        card_1_val = "#0B6E4F"

        card_2_bg = "linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%)"
        card_2_border = "#10B981"
        card_2_val = "#047857"

        card_3_bg = "linear-gradient(135deg, #F7FEE7 0%, #ECFCCB 100%)"
        card_3_border = "#84CC16"
        card_3_val = "#4D7C0F"

        card_4_bg = "linear-gradient(135deg, #F0FDFA 0%, #CCFBF1 100%)"
        card_4_border = "#0D9488"
        card_4_val = "#0F766E"

    # Sidebar radio styling variables
    radio_inactive_bg = "#FFFFFF"
    radio_inactive_border = "#DCE7ED" if "Clustering" in track_selection else c_primary
    radio_inactive_color = "#293B4A" if "Clustering" in track_selection else c_text_head
    radio_active_bg = "#CDEBE4" if "Clustering" in track_selection else c_primary
    radio_active_border = "#367F83" if "Clustering" in track_selection else c_secondary
    radio_active_text = "#367F83" if "Clustering" in track_selection else "#ffffff"
    sidebar_border = "#DCE7ED" if "Clustering" in track_selection else c_primary

    # Input styling overrides
    input_bg = "#FFFFFF"
    input_text = c_text_head
    input_border = "#DCE7ED" if "Clustering" in track_selection else "#CBD5E1"
    container_bg = "#FFFFFF"
    disclaimer_bg = "#FFFFFF"

    # Metric card border styles (subtle borders and colored top accents for Arctic Teal)
    if "Clustering" in track_selection:
        card_1_border_style = "border: 1px solid #DCE7ED !important; border-top: 4px solid #367F83 !important;"
        card_2_border_style = "border: 1px solid #DCE7ED !important; border-top: 4px solid #719CB8 !important;"
        card_3_border_style = "border: 1px solid #DCE7ED !important; border-top: 4px solid #B6AEDB !important;"
        card_4_border_style = "border: 1px solid #DCE7ED !important; border-top: 4px solid #70C9C0 !important;"
    else:
        card_1_border_style = f"border: 2px solid {card_1_border} !important;"
        card_2_border_style = f"border: 2px solid {card_2_border} !important;"
        card_3_border_style = f"border: 2px solid {card_3_border} !important;"
        card_4_border_style = f"border: 2px solid {card_4_border} !important;"

    css = f"""
    <style>
    /* =========================================================
       DYNAMIC THEME INJECTION — {track_selection}
       ========================================================= */
    :root, html, body, .stApp {{
        --theme-primary: {c_primary};
        --theme-secondary: {c_secondary};
        --theme-accent: {c_accent};
        --theme-bg: {c_bg_canvas};
        --theme-text-head: {c_text_head};
        --theme-text-body: {c_text_body};
    }}

    /* Global App Canvas */
    .stApp {{
        background: {c_bg_canvas} !important;
        background-color: {c_bg_canvas} !important;
        color: {c_text_body} !important;
    }}

    /* Top Accent Line */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, {c_primary}, {c_secondary}, {c_accent});
        z-index: 999999;
    }}

    /* Typography Hierarchy */
    h1, h2, h3, h4, h5, h6, .hero-title, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        color: {c_text_head} !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
        letter-spacing: -0.02em !important;
    }}

    p, span, label, div {{
        color: {c_text_body};
    }}

    /* =========================================================
       SIDEBAR & NAVIGATION
       ========================================================= */
    [data-testid="stSidebar"] {{
        background: {c_bg_sidebar} !important;
        background-color: {c_bg_sidebar} !important;
        border-right: 1.5px solid {sidebar_border} !important;
    }}

    [data-testid="stSidebar"] * {{
        color: {c_text_head} !important;
    }}

    [data-testid="stSidebar"] .stRadio label {{
        background: {radio_inactive_bg} !important;
        border: 1.5px solid {radio_inactive_border} !important;
        border-radius: 8px !important;
        padding: 9px 12px !important;
        font-weight: 600 !important;
        color: {radio_inactive_color} !important;
        transition: all 0.2s ease !important;
    }}

    [data-testid="stSidebar"] .stRadio label:hover {{
        border-color: {c_secondary} !important;
        box-shadow: 0 2px 8px {c_glow} !important;
        transform: translateY(-1px);
    }}

    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {{
        background: {radio_active_bg} !important;
        border: 2px solid {radio_active_border} !important;
        color: {radio_active_text} !important;
        box-shadow: 0 2px 8px {c_glow} !important;
    }}

    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) * {{
        color: {radio_active_text} !important;
        font-weight: 700 !important;
    }}

    /* =========================================================
       TABS NAVIGATION
       ========================================================= */
    .stTabs [data-baseweb="tab-list"] {{
        border-bottom: 2px solid {c_primary} !important;
        gap: 6px !important;
        background: transparent !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 42px !important;
        padding: 0 18px !important;
        border-radius: 8px 8px 0 0 !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        color: {c_text_muted} !important;
        border: none !important;
        background: transparent !important;
        transition: all 0.15s ease;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        color: {c_secondary} !important;
        background: {c_tab_active_bg} !important;
    }}

    div[data-testid="stTab"][aria-selected="true"],
    div[data-testid="stTab"][data-selected="true"],
    [data-testid="stTab"][aria-selected="true"],
    div[data-testid="stTabs"] button[aria-selected="true"] {{
        color: {c_primary} !important;
        font-weight: 700 !important;
        background: {c_tab_active_bg} !important;
        border-bottom: 3.5px solid {c_primary} !important;
    }}

    div[data-testid="stTab"][aria-selected="true"] *,
    div[data-testid="stTab"][data-selected="true"] * {{
        color: {c_primary} !important;
        font-weight: 700 !important;
    }}

    div[data-baseweb="tab-highlight"], [data-baseweb="tab-highlight"] {{
        background-color: {c_primary} !important;
        height: 3.5px !important;
    }}

    /* =========================================================
       BUTTONS
       ========================================================= */
    div[data-testid="stButton"] > button[kind="primary"],
    div[data-testid="stButton"] > button[data-testid="stBaseButton-primary"],
    button[data-testid="stBaseButton-primary"],
    button[kind="primary"] {{
        background: linear-gradient(135deg, {c_primary} 0%, {c_secondary} 100%) !important;
        background-color: {c_primary} !important;
        border: 1.5px solid {c_secondary} !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px {c_glow} !important;
        transition: all 0.2s ease !important;
    }}

    div[data-testid="stButton"] > button[kind="primary"]:hover,
    button[kind="primary"]:hover {{
        box-shadow: 0 6px 18px {c_glow} !important;
        transform: translateY(-2px);
    }}

    div[data-testid="stButton"] > button[kind="primary"] *,
    button[kind="primary"] * {{
        color: #ffffff !important;
    }}

    div[data-testid="stButton"] > button[kind="secondary"],
    button[kind="secondary"] {{
        background: {c_card_bg} !important;
        border: 1.5px solid {c_primary} !important;
        color: {c_text_head} !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }}

    /* =========================================================
       METRIC CARDS — THEMED VARIATIONS
       ========================================================= */
    .metric-card-1 {{
        background: {card_1_bg} !important;
        {card_1_border_style}
        border-radius: 12px !important;
        box-shadow: 0 2px 8px {c_glow} !important;
    }}
    .metric-card-1 .metric-label {{ color: {card_1_val} !important; font-weight: 700 !important; }}
    .metric-card-1 .metric-value {{ color: {card_1_val} !important; font-weight: 800 !important; }}
    .metric-card-1 .metric-sub {{ color: {c_text_body} !important; font-weight: 500 !important; }}

    .metric-card-2 {{
        background: {card_2_bg} !important;
        {card_2_border_style}
        border-radius: 12px !important;
        box-shadow: 0 2px 8px {c_glow} !important;
    }}
    .metric-card-2 .metric-label {{ color: {card_2_val} !important; font-weight: 700 !important; }}
    .metric-card-2 .metric-value {{ color: {card_2_val} !important; font-weight: 800 !important; }}
    .metric-card-2 .metric-sub {{ color: {c_text_body} !important; font-weight: 500 !important; }}

    .metric-card-3 {{
        background: {card_3_bg} !important;
        {card_3_border_style}
        border-radius: 12px !important;
        box-shadow: 0 2px 8px {c_glow} !important;
    }}
    .metric-card-3 .metric-label {{ color: {card_3_val} !important; font-weight: 700 !important; }}
    .metric-card-3 .metric-value {{ color: {card_3_val} !important; font-weight: 800 !important; }}
    .metric-card-3 .metric-sub {{ color: {c_text_body} !important; font-weight: 500 !important; }}

    .metric-card-4 {{
        background: {card_4_bg} !important;
        {card_4_border_style}
        border-radius: 12px !important;
        box-shadow: 0 2px 8px {c_glow} !important;
    }}
    .metric-card-4 .metric-label {{ color: {card_4_val} !important; font-weight: 700 !important; }}
    .metric-card-4 .metric-value {{ color: {card_4_val} !important; font-weight: 800 !important; }}
    .metric-card-4 .metric-sub {{ color: {c_text_body} !important; font-weight: 500 !important; }}

    /* Arctic Group Headers */
    .arctic-group-header {{
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin-bottom: 12px !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }}
    .header-teal {{
        background: #CDEBE4 !important;
        color: #367F83 !important;
        border: 1px solid #B8E4DA !important;
    }}
    .header-blue {{
        background: #E1ECF4 !important;
        color: #3B6785 !important;
        border: 1px solid #BFD9EA !important;
    }}
    .header-lavender {{
        background: #EBE8F7 !important;
        color: #554C7D !important;
        border: 1px solid #D2CEEC !important;
    }}

    /* =========================================================
       SURFACES & CONTAINER CARDS
       ========================================================= */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: {container_bg} !important;
        border: 2px solid {c_card_border} !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        margin-bottom: 8px !important;
        box-shadow: 0 2px 8px {c_glow} !important;
    }}

    .themed-hero {{
        background: {c_card_bg} !important;
        border: 2px solid {c_primary} !important;
        border-left: 6px solid {c_secondary} !important;
        border-radius: 12px !important;
        padding: 18px 22px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 14px {c_glow} !important;
    }}

    .themed-pill {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: {c_tab_active_bg};
        border: 1.5px solid {c_secondary};
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: {c_primary} !important;
        margin-bottom: 6px;
    }}

    .themed-pill * {{
        color: {c_primary} !important;
    }}

    .themed-feature-tag {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: {c_tab_active_bg};
        border: 1px solid {c_secondary};
        border-radius: 6px;
        padding: 3px 9px;
        font-size: 0.74rem;
        color: {c_text_head};
        font-weight: 500;
        margin-right: 6px;
        margin-top: 5px;
    }}

    .theme-sidebar-badge {{
        background: {c_card_bg};
        border: 2px solid {c_primary};
        border-radius: 8px;
        padding: 12px 14px;
        margin-top: 8px;
        box-shadow: 0 2px 8px {c_glow};
    }}

    .theme-sidebar-title {{
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: {c_primary} !important;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 5px;
    }}

    .theme-sidebar-title * {{
        color: {c_primary} !important;
    }}

    .clinical-disclaimer {{
        margin-top: 10px;
        padding: 8px 12px;
        background: {disclaimer_bg};
        border-radius: 8px;
        border: 1px solid {c_secondary};
        border-left: 4px solid {c_primary};
        font-size: 0.74rem;
        color: {c_text_body};
        line-height: 1.45;
    }}

    /* Form Controls & Inputs */
    div[data-testid="stSelectbox"] > div,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border-color: {input_border} !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }}

    div[data-testid="stSlider"] div[data-baseweb="slider"] {{
        color: {c_secondary} !important;
    }}

    /* Dataframe styling */
    [data-testid="stDataFrame"] {{
        border: 1.5px solid {c_primary} !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }}

    /* Themed Headings and Subheadings */
    .themed-heading {{
        font-size: 1.05rem;
        font-weight: 700;
        color: {c_text_head} !important;
        margin-bottom: 4px;
        letter-spacing: -0.01em;
    }}
    .themed-subheading {{
        font-size: 0.82rem;
        color: {c_text_muted} !important;
        margin-bottom: 14px;
        line-height: 1.45;
    }}

    /* Duel Comparison Cards */
    .duel-card-a {{
        padding: 12px;
        background: {c_tab_active_bg} !important;
        border-radius: 8px !important;
        border: 1.5px solid {c_primary} !important;
        box-shadow: 0 2px 6px {c_glow} !important;
    }}
    .duel-card-b {{
        padding: 12px;
        background: {c_card_bg} !important;
        border-radius: 8px !important;
        border: 1.5px solid {c_card_border} !important;
        box-shadow: 0 2px 6px {c_glow} !important;
    }}

    /* Calculated MAP Badge */
    .themed-map-badge {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: {c_card_bg};
        border: 1.5px solid {c_secondary};
        border-radius: 8px;
        padding: 7px 14px;
        font-size: 0.82rem;
        color: {c_text_head};
        margin-bottom: 14px;
        box-shadow: 0 2px 6px {c_glow};
    }}

    /* Expanders */
    div[data-testid="stExpander"] {{
        background: {c_card_bg} !important;
        border: 1.5px solid {c_card_border} !important;
        border-radius: 8px !important;
    }}
    div[data-testid="stExpander"] details summary {{
        color: {c_text_head} !important;
        font-weight: 600 !important;
    }}
    </style>
    """
    return css


def get_hero_banner(track_selection: str) -> str:
    """
    Renders the theme-tailored domain hero card with dataset facts and emblems.
    """
    if "Classification" in track_selection:
        # THEME B: CORAL BLOOM (Classification — Maternal Care)
        return """
        <div class="themed-hero">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                <div style="flex: 1 1 580px;">
                    <div class="themed-pill">
                        <span>🩺</span>
                        <span>Clinical Obstetrics • 3-Tier Risk Stratification</span>
                    </div>
                    <h1 class="hero-title" style="color: #55253B !important; font-size: 1.35rem !important; margin: 2px 0 6px 0;">
                        Maternal Health Risk — Clinical Decision Support
                    </h1>
                    <p class="hero-subtitle" style="color: #6E334D; margin: 0; font-size: 0.86rem; line-height: 1.5; max-width: 860px;">
                        Assisting obstetric triage by categorizing patient vital signs, Mean Arterial Pressure (MAP), and blood glucose 
                        into <strong>Low Risk</strong>, <strong>Mid Risk</strong>, and <strong>High Risk</strong> tiers. Evaluated across 10 supervised classification pipelines.
                    </p>
                    <div style="margin-top: 10px; display: flex; flex-wrap: wrap; gap: 6px;">
                        <span class="themed-feature-tag">🩺 <strong>Clinical Vitals:</strong> Systolic/Diastolic BP, Heart Rate, BS, Body Temp</span>
                        <span class="themed-feature-tag">🤱 <strong>Maternal Cohort:</strong> 1,014 Patient Records</span>
                        <span class="themed-feature-tag">💓 <strong>Calculated MAP:</strong> (Systolic + 2×Diastolic) / 3</span>
                        <span class="themed-feature-tag">🏆 <strong>Top Model:</strong> AdaBoost Classifier (Test Acc = 85.2%)</span>
                    </div>
                </div>
                <div style="flex: 0 0 130px; text-align: right;">
                    <!-- Coral & Raspberry Medical Stethoscope Emblem -->
                    <svg width="110" height="90" viewBox="0 0 110 90" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="55" cy="45" r="40" fill="#FFF0E8" stroke="#F05A78" stroke-width="2"/>
                        <!-- Heartbeat Line -->
                        <path d="M 18 52 L 32 52 L 38 40 L 44 65 L 50 32 L 56 60 L 62 52 L 80 52" 
                              stroke="#BE3455" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                        <!-- Stethoscope Tube -->
                        <path d="M 62 18 C 58 18, 54 22, 54 28 L 54 40 C 54 48, 62 54, 70 54 C 78 54, 86 48, 86 40 L 86 28 C 86 22, 82 18, 78 18" 
                              stroke="#55253B" stroke-width="2.5" stroke-linecap="round" fill="none"/>
                        <circle cx="62" cy="18" r="2.5" fill="#F05A78"/>
                        <circle cx="78" cy="18" r="2.5" fill="#F05A78"/>
                        <circle cx="60" cy="42" r="7" fill="#FFFFFF" stroke="#BE3455" stroke-width="2"/>
                        <circle cx="60" cy="42" r="3.5" fill="#F05A78"/>
                    </svg>
                </div>
            </div>
            <div class="clinical-disclaimer">
                <strong>Clinical Decision Support Notice:</strong> This machine learning model provides probabilistic risk stratification based on historical patient vitals to assist triage prioritization. It does not constitute a definitive medical diagnosis.
            </div>
        </div>
        """

    elif "Clustering" in track_selection:
        # THEME C: CALM ARCTIC TEAL (Clustering — CTG Telemetry)
        return """
        <div class="themed-hero" style="background: #FFFFFF !important; border: 1.5px solid #DCE7ED !important; border-left: 5px solid #367F83 !important; border-radius: 12px !important; box-shadow: 0 2px 8px rgba(41, 59, 74, 0.04) !important;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                <div style="flex: 1 1 580px;">
                    <div style="display: inline-flex; align-items: center; gap: 6px; background: #CDEBE4; border: 1px solid #70C9C0; padding: 3px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; color: #367F83; margin-bottom: 6px;">
                        <span>📟</span>
                        <span>Biomedical Telemetry Lab • CTG Signal Analysis</span>
                    </div>
                    <h1 class="hero-title" style="color: #293B4A !important; font-size: 1.35rem !important; margin: 2px 0 6px 0;">
                        Cardiotocography (CTG) Telemetry & Fetal Phenotyping
                    </h1>
                    <p class="hero-subtitle" style="color: #657786; margin: 0; font-size: 0.86rem; line-height: 1.5; max-width: 860px;">
                        Unsupervised stratification of <strong>2,126 cardiotocograms</strong> into clinical signal sub-types using 
                        K-Means and Hierarchical Clustering across baseline fetal heart rate (FHR), variability, and uterine contractions.
                    </p>
                    <div style="margin-top: 10px; display: flex; flex-wrap: wrap; gap: 6px;">
                        <span style="display: inline-flex; align-items: center; gap: 5px; background: #CDEBE4; border: 1px solid #A8DDD2; border-radius: 6px; padding: 4px 10px; font-size: 0.74rem; color: #293B4A; font-weight: 500;">📟 <strong>Telemetry Strip:</strong> 21 Continuous Biometric Features</span>
                        <span style="display: inline-flex; align-items: center; gap: 5px; background: #F1F7FA; border: 1px solid #DCE7ED; border-radius: 6px; padding: 4px 10px; font-size: 0.74rem; color: #293B4A; font-weight: 500;">🫀 <strong>Fetal Vitals:</strong> Baseline HR (LB), Short/Long Var (ASTV/ALTV)</span>
                        <span style="display: inline-flex; align-items: center; gap: 5px; background: #F1F7FA; border: 1px solid #DCE7ED; border-radius: 6px; padding: 4px 10px; font-size: 0.74rem; color: #293B4A; font-weight: 500;">⚡ <strong>Uterine Activity:</strong> Contraction Frequency (UC) & Decelerations</span>
                        <span style="display: inline-flex; align-items: center; gap: 5px; background: #CDEBE4; border: 1px solid #A8DDD2; border-radius: 6px; padding: 4px 10px; font-size: 0.74rem; color: #293B4A; font-weight: 500;">🏆 <strong>Optimal Partition:</strong> K-Means (k = 3, Silhouette = 0.1547, NMI = 0.3166)</span>
                    </div>
                </div>
                <div style="flex: 0 0 130px; text-align: right;">
                    <!-- Muted Teal & Dusty Blue CTG Waveform Illustration -->
                    <svg width="110" height="90" viewBox="0 0 110 90" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect x="8" y="12" width="94" height="66" rx="8" fill="#F1F7FA" stroke="#DCE7ED" stroke-width="1.5"/>
                        <!-- Telemetry Grid Lines -->
                        <line x1="8" y1="34" x2="102" y2="34" stroke="#E2E8F0" stroke-width="1" stroke-dasharray="3 3"/>
                        <line x1="8" y1="56" x2="102" y2="56" stroke="#E2E8F0" stroke-width="1" stroke-dasharray="3 3"/>
                        <!-- Muted Teal FHR Waveform -->
                        <path d="M 12 32 L 25 32 L 30 22 L 36 42 L 42 18 L 48 38 L 54 32 L 68 32 L 74 24 L 80 40 L 98 32" 
                              stroke="#367F83" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                        <!-- Dusty Blue Uterine Contraction -->
                        <path d="M 12 62 L 35 62 C 45 62, 52 46, 58 46 C 64 46, 72 62, 85 62 L 98 62" 
                              stroke="#719CB8" stroke-width="2.2" stroke-linecap="round"/>
                        <!-- Soft Turquoise Pulse Point -->
                        <circle cx="80" cy="40" r="3" fill="#70C9C0"/>
                    </svg>
                </div>
            </div>
        </div>
        """

    else:
        # THEME A: EMERALD OASIS (Regression — WHO Health)
        return """
        <div class="themed-hero">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                <div style="flex: 1 1 580px;">
                    <div class="themed-pill">
                        <span>🌐</span>
                        <span>WHO Global Health Observatory • Continuous Target</span>
                    </div>
                    <h1 class="hero-title" style="color: #15352B !important; font-size: 1.35rem !important; margin: 2px 0 6px 0;">
                        WHO Life Expectancy & Longevity Analytics
                    </h1>
                    <p class="hero-subtitle" style="color: #1E4738; margin: 0; font-size: 0.86rem; line-height: 1.5; max-width: 860px;">
                        Epidemiological regression modeling across <strong>193 UN member nations (2000–2015)</strong>. 
                        Evaluating the impact of childhood immunization coverage, adult mortality, and socioeconomic indices on national life expectancy.
                    </p>
                    <div style="margin-top: 10px; display: flex; flex-wrap: wrap; gap: 6px;">
                        <span class="themed-feature-tag">🌐 <strong>Global Scope:</strong> 2,938 Country-Year Records (193 Nations)</span>
                        <span class="themed-feature-tag">💉 <strong>Immunization Index:</strong> Polio, DTP, Hepatitis B Coverage</span>
                        <span class="themed-feature-tag">🎯 <strong>Target Variable:</strong> Life Expectancy (36.3 to 89.0 Years)</span>
                        <span class="themed-feature-tag">🏆 <strong>Top Model:</strong> Random Forest Regressor (R² = 0.9631, RMSE = 1.78 yrs)</span>
                    </div>
                </div>
                <div style="flex: 0 0 130px; text-align: right;">
                    <!-- Emerald Oasis Globe & Vitality Emblem -->
                    <svg width="110" height="90" viewBox="0 0 110 90" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="55" cy="45" r="40" fill="#F0FDF4" stroke="#10B981" stroke-width="2"/>
                        <!-- Globe Grid -->
                        <circle cx="55" cy="45" r="30" stroke="#0B6E4F" stroke-width="1.8" fill="#ECFDF5"/>
                        <ellipse cx="55" cy="45" rx="30" ry="12" stroke="#10B981" stroke-width="1" stroke-dasharray="2 2" fill="none"/>
                        <ellipse cx="55" cy="45" rx="12" ry="30" stroke="#10B981" stroke-width="1" stroke-dasharray="2 2" fill="none"/>
                        <!-- Vitality Longevity Curve -->
                        <path d="M 22 65 Q 55 18, 88 38" stroke="#0B6E4F" stroke-width="3" stroke-linecap="round" fill="none"/>
                        <circle cx="88" cy="38" r="4.5" fill="#D9F99D" stroke="#0B6E4F" stroke-width="2"/>
                        <!-- Medical Cross Badge -->
                        <rect x="49" y="39" width="12" height="12" rx="2" fill="#0B6E4F"/>
                        <path d="M 55 42 V 48 M 52 45 H 58" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                </div>
            </div>
        </div>
        """


def get_sidebar_badge(track_selection: str) -> str:
    """
    Renders the theme-tailored sidebar metadata badge with accurate dataset statistics.
    """
    if "Classification" in track_selection:
        return """
        <div class="theme-sidebar-badge">
            <div class="theme-sidebar-title">
                <span>🩺</span>
                <span>Dataset: Maternal Vitals</span>
            </div>
            <div style="font-weight: 700; color: #55253B; font-size: 0.85rem;">Maternal Health Risk Dataset</div>
            <div style="font-size: 0.76rem; color: #6E334D; line-height: 1.45; margin-top: 4px;">
                • <strong>1,014</strong> patient observations<br>
                • <strong>6</strong> clinical vitals + calculated MAP<br>
                • Target: <code>RiskLevel (3 classes)</code><br>
                • 10 benchmark algorithms evaluated
            </div>
            <div style="margin-top: 8px; padding: 4px 8px; background: #FFE2D5; border: 1px solid #F05A78; border-radius: 4px; font-size: 0.7rem; color: #BE3455; font-weight: 700; display: flex; align-items: center; gap: 5px;">
                <span>🩺</span>
                <span>Theme: Coral Bloom</span>
            </div>
        </div>
        """
    elif "Clustering" in track_selection:
        return """
        <div class="theme-sidebar-badge" style="background: #FFFFFF; border: 1.5px solid #DCE7ED;">
            <div class="theme-sidebar-title" style="color: #367F83;">
                <span>📟</span>
                <span>Dataset: Fetal Telemetry</span>
            </div>
            <div style="font-weight: 700; color: #293B4A; font-size: 0.85rem;">Cardiotocography (CTG) Dataset</div>
            <div style="font-size: 0.76rem; color: #657786; line-height: 1.45; margin-top: 4px;">
                • <strong>2,126</strong> cardiotocograms recorded<br>
                • <strong>21</strong> continuous biometric signals<br>
                • Ground Truth: <code>NSP fetal triage</code><br>
                • K-Means & Hierarchical linkage
            </div>
            <div style="margin-top: 8px; padding: 4px 8px; background: #CDEBE4; border: 1px solid #70C9C0; border-radius: 4px; font-size: 0.7rem; color: #367F83; font-weight: 700; display: flex; align-items: center; gap: 5px;">
                <span>📟</span>
                <span>Theme: Calm Arctic Teal</span>
            </div>
        </div>
        """
    else:
        return """
        <div class="theme-sidebar-badge">
            <div class="theme-sidebar-title">
                <span>🌐</span>
                <span>Dataset: WHO Global Health</span>
            </div>
            <div style="font-weight: 700; color: #15352B; font-size: 0.85rem;">WHO Life Expectancy Data</div>
            <div style="font-size: 0.76rem; color: #1E4738; line-height: 1.45; margin-top: 4px;">
                • <strong>2,938</strong> country-year observations<br>
                • <strong>18</strong> continuous health predictors<br>
                • Target: <code>Life expectancy (years)</code><br>
                • 10 regression algorithms benchmarked
            </div>
            <div style="margin-top: 8px; padding: 4px 8px; background: #D1FAE5; border: 1px solid #10B981; border-radius: 4px; font-size: 0.7rem; color: #0B6E4F; font-weight: 700; display: flex; align-items: center; gap: 5px;">
                <span>🌐</span>
                <span>Theme: Emerald Oasis</span>
            </div>
        </div>
        """


def get_sidebar_header(track_selection: str) -> str:
    """
    Renders the theme-tailored sidebar branding with track-specific gradient, icon, and subtitles.
    """
    if "Classification" in track_selection:
        icon = "🩺"
        grad = "linear-gradient(135deg, #BE3455 0%, #F05A78 100%)"
        glow = "rgba(240, 90, 120, 0.3)"
        title_color = "#55253B"
        sub_color = "#BE3455"
        sub_text = "Maternal Healthcare Triage"
    elif "Clustering" in track_selection:
        icon = "📟"
        grad = "linear-gradient(135deg, #367F83 0%, #719CB8 100%)"
        glow = "rgba(54, 127, 131, 0.2)"
        title_color = "#293B4A"
        sub_color = "#367F83"
        sub_text = "Biomedical Telemetry Lab"
    else:
        icon = "🌐"
        grad = "linear-gradient(135deg, #0B6E4F 0%, #10B981 100%)"
        glow = "rgba(16, 185, 129, 0.3)"
        title_color = "#15352B"
        sub_color = "#0B6E4F"
        sub_text = "Public Health Analytics"

    return f"""
    <div style="padding: 4px 0 12px 0;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 36px; height: 36px; border-radius: 9px; background: {grad}; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.15rem; box-shadow: 0 3px 8px {glow};">
                {icon}
            </div>
            <div>
                <div style="color: {title_color}; font-size: 1.18rem; font-weight: 800; letter-spacing: -0.3px; line-height: 1.1;">ML Studio</div>
                <div style="color: {sub_color}; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700;">
                    {sub_text}
                </div>
            </div>
        </div>
    </div>
    """


def get_sidebar_status_box(track_selection: str) -> str:
    """
    Renders the model cache status box in the sidebar according to the active theme.
    """
    if "Classification" in track_selection:
        bg = "#FFF0E8"
        border = "#F05A78"
        dot = "#BE3455"
        head_color = "#BE3455"
        sub_color = "#6E334D"
    elif "Clustering" in track_selection:
        bg = "#F1F7FA"
        border = "#DCE7ED"
        dot = "#367F83"
        head_color = "#367F83"
        sub_color = "#657786"
    else:
        bg = "#ECFDF5"
        border = "#10B981"
        dot = "#0B6E4F"
        head_color = "#0B6E4F"
        sub_color = "#1E4738"

    return f"""
    <div style="margin-top: 14px; padding: 10px 12px; background: {bg}; border: 1.5px solid {border}; border-radius: 8px;">
        <div style="display: flex; align-items: center; gap: 7px; font-size: 0.74rem; font-weight: 700; color: {head_color};">
            <span style="display: inline-block; width: 8px; height: 8px; background: {dot}; border-radius: 50%;"></span>
            24 Pre-trained Models Active
        </div>
        <div style="font-size: 0.7rem; color: {sub_color}; margin-top: 3px; font-weight: 500;">Deterministic inference enabled.</div>
    </div>
    """

