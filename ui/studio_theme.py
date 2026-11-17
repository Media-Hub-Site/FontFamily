"""
ui/studio_theme.py
──────────────────
Sistema de temas estéticos tipo "Atelier Tipográfico / Editorial" para MediaHub-FontFamily.
Diseñado específicamente para diferenciarse del resto del ecosistema MediaHub:
1. 'paper'  — Papel Editorial (Cálido, crema pergamino, tinta espresso y terracota).
2. 'velvet' — Atelier Nocturno (Obsidiana ciruela, crema champán, oro rosa y ámbar).
3. 'matcha' — Cyber Matcha (Tinta botánica profunda, menta neón y verde salvia).
"""

from __future__ import annotations

THEMES: dict[str, dict[str, str]] = {
    "paper": {
        "id": "paper",
        "name_es": "📜 Papel Editorial",
        "name_en": "📜 Editorial Paper",
        "bg_main": "#F4EFE6",
        "bg_panel": "#FAF7F2",
        "bg_card": "#FFFFFF",
        "bg_card_hover": "#FDFBF7",
        "bg_subtle": "#EAE3D5",
        "bg_input": "#FFFFFF",
        "bg_xray": "#FFF8EB",
        "text_primary": "#1C1815",
        "text_secondary": "#5C5349",
        "text_muted": "#8C8175",
        "border": "#DED5C5",
        "border_strong": "#C4B7A3",
        "accent": "#D9462F",
        "accent_hover": "#B83520",
        "accent_soft": "#FCECE9",
        "accent_text": "#FFFFFF",
        "secondary_accent": "#9A5B13",
        "secondary_soft": "#FEF3C7",
        "success": "#15803D",
        "success_soft": "#DCFCE7",
        "badge_bg": "#EFE8DA",
        "badge_fg": "#6E5D4F",
        "scroll_thumb": "#C9BFAEE0",
    },
    "velvet": {
        "id": "velvet",
        "name_es": "🍷 Atelier Nocturno",
        "name_en": "🍷 Velvet Atelier",
        "bg_main": "#120E16",
        "bg_panel": "#19141F",
        "bg_card": "#221B2A",
        "bg_card_hover": "#2B2235",
        "bg_subtle": "#282032",
        "bg_input": "#15101A",
        "bg_xray": "#261C24",
        "text_primary": "#F7F2EB",
        "text_secondary": "#C4B5CE",
        "text_muted": "#847391",
        "border": "#31273D",
        "border_strong": "#49395B",
        "accent": "#E11D48",
        "accent_hover": "#BE123C",
        "accent_soft": "#3B1525",
        "accent_text": "#FFFFFF",
        "secondary_accent": "#F59E0B",
        "secondary_soft": "#38260B",
        "success": "#10B981",
        "success_soft": "#0F2E24",
        "badge_bg": "#2D2338",
        "badge_fg": "#E9D5FF",
        "scroll_thumb": "#433554",
    },
    "matcha": {
        "id": "matcha",
        "name_es": "🍵 Cyber Matcha",
        "name_en": "🍵 Cyber Matcha",
        "bg_main": "#0A110E",
        "bg_panel": "#101A15",
        "bg_card": "#16241E",
        "bg_card_hover": "#1D3028",
        "bg_subtle": "#1B2B24",
        "bg_input": "#0D1612",
        "bg_xray": "#13261E",
        "text_primary": "#ECFDF5",
        "text_secondary": "#A7F3D0",
        "text_muted": "#5E8C76",
        "border": "#21382E",
        "border_strong": "#2E5242",
        "accent": "#10B981",
        "accent_hover": "#059669",
        "accent_soft": "#0E2E23",
        "accent_text": "#06120D",
        "secondary_accent": "#84CC16",
        "secondary_soft": "#1E2E0B",
        "success": "#34D399",
        "success_soft": "#0E3325",
        "badge_bg": "#1D3329",
        "badge_fg": "#6EE7B7",
        "scroll_thumb": "#2D4F40",
    },
}


def build_studio_stylesheet(t: dict[str, str]) -> str:
    """Construye la hoja de estilos QSS completa para el tema Atelier seleccionado."""
    return f"""
        QMainWindow, QWidget#rootCanvas {{
            background-color: {t['bg_main']};
            color: {t['text_primary']};
            font-family: "Segoe UI Variable Display", "Segoe UI", -apple-system, sans-serif;
        }}
        QLabel {{
            background: transparent;
            color: {t['text_primary']};
        }}
        QFrame#mastheadFrame {{
            background-color: {t['bg_panel']};
            border: 1px solid {t['border']};
            border-radius: 16px;
        }}
        QFrame#composerPane {{
            background-color: {t['bg_panel']};
            border: 1px solid {t['border']};
            border-radius: 18px;
        }}
        QFrame#catalogPane {{
            background-color: {t['bg_panel']};
            border: 1px solid {t['border']};
            border-radius: 18px;
        }}
        QFrame#subCard {{
            background-color: {t['bg_card']};
            border: 1px solid {t['border']};
            border-radius: 12px;
        }}
        QFrame#subCard:hover {{
            background-color: {t['bg_card_hover']};
            border: 1px solid {t['border_strong']};
        }}
        QFrame#xrayBox {{
            background-color: {t['bg_xray']};
            border: 1px dashed {t['secondary_accent']};
            border-radius: 10px;
        }}
        QFrame#mockupBox {{
            background-color: {t['bg_card']};
            border: 1px solid {t['border']};
            border-radius: 12px;
        }}
        QPlainTextEdit#masterEditor {{
            background-color: {t['bg_input']};
            color: {t['text_primary']};
            border: 2px solid {t['border_strong']};
            border-radius: 14px;
            padding: 12px 14px;
            font-family: "Segoe UI", "Segoe UI Emoji", "Segoe UI Symbol", sans-serif;
            font-size: 13.5pt;
            selection-background-color: {t['accent']};
            selection-color: {t['accent_text']};
        }}
        QPlainTextEdit#masterEditor:focus {{
            border: 2px solid {t['accent']};
        }}
        QLineEdit {{
            background-color: {t['bg_input']};
            color: {t['text_primary']};
            border: 1px solid {t['border_strong']};
            border-radius: 10px;
            padding: 7px 12px;
            font-size: 10pt;
        }}
        QLineEdit:focus {{
            border: 1.5px solid {t['accent']};
        }}
        QComboBox {{
            background-color: {t['bg_input']};
            color: {t['text_primary']};
            border: 1px solid {t['border_strong']};
            border-radius: 9px;
            padding: 5px 10px;
            font-size: 9.5pt;
            font-weight: 600;
        }}
        QComboBox:hover {{
            border: 1px solid {t['accent']};
        }}
        QComboBox::drop-down {{
            border: none;
            padding-right: 8px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {t['bg_card']};
            color: {t['text_primary']};
            border: 1px solid {t['border_strong']};
            selection-background-color: {t['accent']};
            selection-color: {t['accent_text']};
            padding: 4px;
        }}
        QScrollArea {{
            background: transparent;
            border: none;
        }}
        QScrollBar:vertical {{
            border: none;
            background: transparent;
            width: 8px;
            margin: 2px;
        }}
        QScrollBar::handle:vertical {{
            background: {t['scroll_thumb']};
            min-height: 30px;
            border-radius: 4px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        QScrollBar:horizontal {{
            border: none;
            background: transparent;
            height: 6px;
        }}
        QScrollBar::handle:horizontal {{
            background: {t['scroll_thumb']};
            border-radius: 3px;
        }}
    """
