"""
ui/main_window.py
─────────────────
Ventana principal de MediaHub-FontFamily — "Atelier Tipográfico & Glifos".
Diseño editorial de doble lienzo ("El Telar Tipográfico") que permite combinar
múltiples fuentes Unicode, símbolos raros, caracteres invisibles, marcos y emojis
dentro de una misma caja de composición antes de copiar el resultado final.
"""

from __future__ import annotations

import json
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QPlainTextEdit, QLineEdit, QComboBox, QScrollArea, QGridLayout,
    QStackedWidget, QApplication, QSizePolicy
)
from PyQt6.QtGui import QIcon, QFont, QTextCursor
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

from core.typography_engine import (
    TypographyEngine, FONT_STYLES, FONT_STYLES_BY_ID
)
from core.glyph_catalog import (
    INVISIBLE_CHARACTERS, INVISIBLE_CHARS_SET, SYMBOL_CATEGORIES,
    TEXT_WRAPPERS, AESTHETIC_DIVIDERS, KAOMOJI_CATEGORIES,
    AESTHETIC_EMOJI_COMBOS, EMOJI_CATEGORIES
)
from ui.studio_theme import THEMES, build_studio_stylesheet


# ─────────────────────────────────────────────────────────────────────────────
#  Traducciones Bilingües (ES / EN)
# ─────────────────────────────────────────────────────────────────────────────

UI_TEXTS = {
    "es": {
        "window_title": "FontFamily — Atelier Tipográfico, Símbolos & Caracteres Invisibles",
        "masthead_title": "FontFamily Atelier",
        "masthead_sub": "Estudio de Composición Tipográfica Unicode, Símbolos Especiales, Invisibles & Emojis",
        "composer_title": "✒️ MESA DE COMPOSICIÓN (TU TEXTO FINAL)",
        "composer_hint": "Escribe aquí, activa una fuente en vivo o inserta símbolos y emojis en tu cursor.",
        "live_kbd_label": "⌨️ Fuente al escribir:",
        "btn_invisible_quick": "👻 +Invisible (U+3164)",
        "btn_braille_quick": "⠀ +Espacio IG (U+2800)",
        "btn_strike": "S̶ Tachar",
        "btn_underline": "U̲ Subrayar",
        "btn_clean_font": "🧹 Limpiar Fuente",
        "xray_toggle_off": "👁 Rayos-X Invisibles: OFF",
        "xray_toggle_on": "👁 Rayos-X Invisibles: ON",
        "xray_empty": "Sin caracteres invisibles detectados en el lienzo.",
        "mockup_label": "Vista Previa en Plataforma:",
        "mockup_gamer": "🎮 Nick Gamer / Discord",
        "mockup_bio": "📸 Bio Instagram / TikTok",
        "mockup_chat": "💬 Mensaje de Chat",
        "btn_copy_master": "📋 COPIAR COMPOSICIÓN COMPLETA",
        "btn_copied_master": "✨ ¡COMPOSICIÓN COPIADA AL PORTAPAPELES!",
        "btn_save_fav": "★ Guardar",
        "btn_clear": "🗑 Vaciar",
        "tab_fonts": "𝐀𝐚 Fuentes (30+)",
        "tab_invisibles": "👻 Invisibles & Símbolos",
        "tab_frames": "🎭 Marcos & Kaomojis",
        "tab_emojis": "😀 Emojis & Combos",
        "tab_favs": "★ Favoritos",
        "sample_placeholder": "Escribe texto de muestra o usa lo que seleccionaste en tu caja...",
        "sync_from_canvas": "🔄 Sincronizar con mi caja",
        "cat_all": "Todas",
        "cat_gothic": "Góticas & Gamer",
        "cat_script": "Caligrafía & Cursiva",
        "cat_serif": "Editorial Serif",
        "cat_sans": "Modernas & Mono",
        "cat_boxed": "Cajas & Burbujas",
        "cat_decorated": "Glitch & Efectos",
        "btn_apply_canvas": "➕ Llevar a mi Caja",
        "btn_use_kbd": "⌨️ Usar al Escribir",
        "btn_active_kbd": "⚡ Activa en Teclado",
        "btn_copy_single": "📋 Copiar",
        "inv_header": "👻 LABORATORIO DE CARACTERES INVISIBLES (ESPACIOS VACÍOS)",
        "inv_sub": "Inserta espacios invisibles en tu caja de texto o cópialos puros para Nicks de juegos, Discord, WhatsApp e Instagram.",
        "inv_qty": "Cantidad al insertar:",
        "btn_insert_cursor": "➕ Insertar en mi Caja",
        "btn_copy_pure": "📋 Copiar Puro",
        "sym_header": "✦ BÓVEDA DE SÍMBOLOS ESPECIALES (CLIC PARA INSERTAR EN TU CAJA)",
        "sym_status_default": "Haz clic en cualquier símbolo para insertarlo exactamente donde está tu cursor.",
        "frames_header": "༺ ENVOLVEDORES DE TEXTO (1 CLIC ENVUELVE TU SELECCIÓN O LÍNEA)",
        "dividers_header": "─── SEPARADORES & BORDES ESTÉTICOS PARA BIOS ───",
        "kaomoji_header": "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ COLECCIÓN KAOMOJI JAPONÉS",
        "emoji_search": "🔍 Buscar emoji (ej: fuego, corazon, corona, espada, estrella, gato)...",
        "combos_header": "✨ COMBOS ESTÉTICOS LISTOS PARA INSERTAR",
        "favs_header": "★ TUS COMPOSICIONES FAVORITAS & HISTORIAL RECIENTE",
        "favs_empty": "Guarda tus Nicks, Bios o textos personalizados con el botón '★ Guardar' para reutilizarlos cuando quieras.",
        "btn_load_canvas": "📥 Cargar al Lienzo",
        "btn_delete": "✕",
        "stats_fmt": "{chars} caracteres • {words} palabras • {inv} invisibles",
        "toast_inserted": "Insertado en tu caja: {item}",
        "toast_copied": "Copiado al portapapeles: {item}",
        "toast_wrapped": "Marco aplicado a tu texto: {item}",
        "toast_kbd": "Modo Teclado activado: ahora escribes en {item}",
    },
    "en": {
        "window_title": "FontFamily — Typography Atelier, Rare Symbols & Invisible Glyphs",
        "masthead_title": "FontFamily Atelier",
        "masthead_sub": "Unicode Typography Studio, Invisible Characters, Rare Symbols & Emoji Composer",
        "composer_title": "✒️ MASTER COMPOSITION STAGE (YOUR FINAL TEXT)",
        "composer_hint": "Type directly here, activate a live typing font, or insert symbols & emojis at your cursor.",
        "live_kbd_label": "⌨️ Typing Font:",
        "btn_invisible_quick": "👻 +Invisible (U+3164)",
        "btn_braille_quick": "⠀ +IG Blank (U+2800)",
        "btn_strike": "S̶ Strike",
        "btn_underline": "U̲ Underline",
        "btn_clean_font": "🧹 Plain Text",
        "xray_toggle_off": "👁 Invisible X-Ray: OFF",
        "xray_toggle_on": "👁 Invisible X-Ray: ON",
        "xray_empty": "No invisible characters detected in canvas.",
        "mockup_label": "Live Platform Preview:",
        "mockup_gamer": "🎮 Gamer Nick / Discord",
        "mockup_bio": "📸 Instagram / TikTok Bio",
        "mockup_chat": "💬 Chat Message",
        "btn_copy_master": "📋 COPY FULL COMPOSITION",
        "btn_copied_master": "✨ FULL COMPOSITION COPIED TO CLIPBOARD!",
        "btn_save_fav": "★ Save",
        "btn_clear": "🗑 Clear",
        "tab_fonts": "𝐀𝐚 Fonts (30+)",
        "tab_invisibles": "👻 Invisibles & Symbols",
        "tab_frames": "🎭 Frames & Kaomojis",
        "tab_emojis": "😀 Emojis & Combos",
        "tab_favs": "★ Favorites",
        "sample_placeholder": "Type preview text or use selection from your canvas...",
        "sync_from_canvas": "🔄 Sync from Canvas",
        "cat_all": "All Styles",
        "cat_gothic": "Gothic & Gamer",
        "cat_script": "Calligraphy & Script",
        "cat_serif": "Editorial Serif",
        "cat_sans": "Modern Sans & Mono",
        "cat_boxed": "Boxed & Bubbles",
        "cat_decorated": "Glitch & Decorated",
        "btn_apply_canvas": "➕ Send to Canvas",
        "btn_use_kbd": "⌨️ Type in This",
        "btn_active_kbd": "⚡ Active on Keyboard",
        "btn_copy_single": "📋 Copy",
        "inv_header": "👻 INVISIBLE CHARACTERS LAB (BLANK SPACES)",
        "inv_sub": "Insert invisible characters into your composition box or copy pure blanks for Game Nicks, Discord, WhatsApp & IG.",
        "inv_qty": "Insert count:",
        "btn_insert_cursor": "➕ Insert in Canvas",
        "btn_copy_pure": "📋 Copy Pure",
        "sym_header": "✦ RARE & SPECIAL SYMBOLS VAULT (CLICK TO INSERT AT CURSOR)",
        "sym_status_default": "Click any symbol to insert it right at your cursor position.",
        "frames_header": "༺ 1-CLICK TEXT WRAPPERS (WRAPS SELECTION OR CURRENT LINE)",
        "dividers_header": "─── AESTHETIC DIVIDERS & BIO HEADERS ───",
        "kaomoji_header": "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ JAPANESE KAOMOJI COLLECTION",
        "emoji_search": "🔍 Search emoji (e.g. fire, heart, crown, sword, star, cat)...",
        "combos_header": "✨ READY-TO-INSERT AESTHETIC EMOJI COMBOS",
        "favs_header": "★ SAVED FAVORITES & RECENT CLIPBOARD HISTORY",
        "favs_empty": "Save your favorite Nicks, Bios or custom texts using '★ Save' to reuse anytime.",
        "btn_load_canvas": "📥 Load to Canvas",
        "btn_delete": "✕",
        "stats_fmt": "{chars} chars • {words} words • {inv} invisibles",
        "toast_inserted": "Inserted into canvas: {item}",
        "toast_copied": "Copied to clipboard: {item}",
        "toast_wrapped": "Frame applied to text: {item}",
        "toast_kbd": "Live Keyboard Mode: now typing in {item}",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
#  Editor Maestro con Transformación de Teclado en Tiempo Real
# ─────────────────────────────────────────────────────────────────────────────

class LiveComposerTextEdit(QPlainTextEdit):
    """
    Editor personalizado que intercepta las pulsaciones de teclado cuando hay una
    fuente Unicode activa (`active_font_id != 'normal'`) y transforma cada letra
    escrita en tiempo real directamente en el cursor.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_font_id: str = "normal"
        self.setObjectName("masterEditor")

    def keyPressEvent(self, event):
        # Si hay una fuente activa y es escritura normal (sin Ctrl/Alt/Meta)
        modifiers = event.modifiers()
        is_ctrl_or_alt = bool(
            modifiers & (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.AltModifier | Qt.KeyboardModifier.MetaModifier)
        )
        text = event.text()
        if (
            self.active_font_id != "normal"
            and not is_ctrl_or_alt
            and text
            and len(text) == 1
            and text.isprintable()
        ):
            transformed = TypographyEngine.transform_char(text, self.active_font_id)
            self.insertPlainText(transformed)
            return

        super().keyPressEvent(event)


# ─────────────────────────────────────────────────────────────────────────────
#  Ventana Principal del Estudio (FontFamilyWindow)
# ─────────────────────────────────────────────────────────────────────────────

class FontFamilyWindow(QMainWindow):
    def __init__(self, lang: str = "es"):
        super().__init__()
        self.lang = "en" if lang == "en" else "es"
        self.current_theme_id = "paper"  # Por defecto: Papel Editorial para diferenciarse del resto de apps
        self.active_font_cat = "all"
        self.active_symbol_cat = "stars"
        self.active_emoji_cat = "all"
        self.xray_enabled = False
        self.favorites: list[str] = []
        self.history: list[str] = []

        self._load_favorites()
        self._setup_window()
        self.init_ui()
        self.apply_theme(self.current_theme_id)
        self.retranslate_ui()

        # Texto inicial demostrativo rico en estilos
        initial_demo = "꧁༺ ℌ𝔬𝔩𝔞 𝔐𝔲𝔫𝔡𝔬 ༻꧂\n✦ 𝓔𝓼𝓬𝓻𝓲𝓫𝓮 𝔂 𝓹𝓮𝓻𝓼𝓸𝓷𝓪𝓵𝓲𝔃𝓪 𝓽𝓾 𝓽𝓮𝔁𝓽𝓸 ✦ ✨"
        self.editor.setPlainText(initial_demo)
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.editor.setTextCursor(cursor)

    def tr_str(self, key: str, **kwargs) -> str:
        d = UI_TEXTS.get(self.lang, UI_TEXTS["es"])
        val = d.get(key, UI_TEXTS["es"].get(key, key))
        if kwargs:
            try:
                return val.format(**kwargs)
            except Exception:
                return val
        return val

    def _get_favs_file(self) -> str:
        home = os.environ.get("USERPROFILE") or os.path.expanduser("~")
        folder = os.path.join(home, ".mediahub")
        os.makedirs(folder, exist_ok=True)
        return os.path.join(folder, "fontfamily_favorites.json")

    def _load_favorites(self):
        fpath = self._get_favs_file()
        if os.path.isfile(fpath):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.favorites = data.get("favorites", [])
            except Exception:
                self.favorites = []
        if not self.favorites:
            self.favorites = [
                "꧁༺ 𝕯𝖆𝖗𝖐 𝕶𝖓𝖎𝖌𝖍𝖙 ༻꧂",
                "✧･ﾟ: * 𝓢𝓽𝓪𝓻𝓵𝓲𝓰𝓱𝓽 *:･ﾟ✧\u3164✨",
                "『 ＶＡＰＯＲＷＡＶＥ 』 🎧💜🌌",
            ]

    def _save_favorites(self):
        fpath = self._get_favs_file()
        try:
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump({"favorites": self.favorites[:40]}, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _setup_window(self):
        self.resize(1240, 800)
        self.setMinimumSize(1040, 680)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, "assets", "hub", "Media-Hub.ico")
        if os.path.isfile(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    # ─────────────────────────────────────────────────────────────────────────
    #  Construcción de la Interfaz ("El Telar Tipográfico")
    # ─────────────────────────────────────────────────────────────────────────

    def init_ui(self):
        root = QWidget()
        root.setObjectName("rootCanvas")
        self.setCentralWidget(root)

        main_layout = QVBoxLayout(root)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(14)

        # ── 1. Masthead Editorial Superior ───────────────────────────────────
        self.masthead = QFrame()
        self.masthead.setObjectName("mastheadFrame")
        mh_layout = QHBoxLayout(self.masthead)
        mh_layout.setContentsMargins(18, 12, 18, 12)
        mh_layout.setSpacing(14)

        self.emblem_lbl = QLabel("𝔄𝔞")
        self.emblem_lbl.setFixedSize(48, 48)
        self.emblem_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mh_layout.addWidget(self.emblem_lbl)

        title_col = QVBoxLayout()
        title_col.setSpacing(2)
        self.lbl_title = QLabel()
        self.lbl_sub = QLabel()
        title_col.addWidget(self.lbl_title)
        title_col.addWidget(self.lbl_sub)
        mh_layout.addLayout(title_col)

        mh_layout.addStretch()

        # Toast / Notificación de acción en vivo
        self.lbl_toast = QLabel("")
        self.lbl_toast.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_toast.hide()
        mh_layout.addWidget(self.lbl_toast)

        # Selector de los 3 Temas Atelier
        self.theme_buttons: dict[str, QPushButton] = {}
        for tid, tdata in THEMES.items():
            btn = QPushButton(tdata["name_es"])
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedHeight(32)
            btn.clicked.connect(lambda checked, k=tid: self.apply_theme(k))
            mh_layout.addWidget(btn)
            self.theme_buttons[tid] = btn

        # Botón Idioma ES/EN
        self.btn_lang = QPushButton("EN" if self.lang == "es" else "ES")
        self.btn_lang.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_lang.setFixedSize(44, 32)
        self.btn_lang.clicked.connect(self._toggle_language)
        mh_layout.addWidget(self.btn_lang)

        main_layout.addWidget(self.masthead)

        # ── 2. Cuerpo Principal Dividido (Izquierda: Mesa de Composición | Derecha: Bóveda)
        workspace_layout = QHBoxLayout()
        workspace_layout.setSpacing(16)

        # === PANEL IZQUIERDO: MESA DE COMPOSICIÓN EN VIVO ===
        self.composer_pane = QFrame()
        self.composer_pane.setObjectName("composerPane")
        comp_layout = QVBoxLayout(self.composer_pane)
        comp_layout.setContentsMargins(18, 16, 18, 16)
        comp_layout.setSpacing(10)

        # Cabecera del compositor
        comp_hdr = QHBoxLayout()
        self.lbl_comp_title = QLabel()
        comp_hdr.addWidget(self.lbl_comp_title)
        comp_hdr.addStretch()
        self.lbl_stats = QLabel()
        comp_hdr.addWidget(self.lbl_stats)
        comp_layout.addLayout(comp_hdr)

        self.lbl_comp_hint = QLabel()
        self.lbl_comp_hint.setWordWrap(True)
        comp_layout.addWidget(self.lbl_comp_hint)

        # Barra de Fuente en Vivo (Modo Teclado)
        kbd_bar = QHBoxLayout()
        kbd_bar.setSpacing(8)
        self.lbl_live_kbd = QLabel()
        kbd_bar.addWidget(self.lbl_live_kbd)

        self.combo_live_font = QComboBox()
        self.combo_live_font.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._populate_live_font_combo()
        self.combo_live_font.currentIndexChanged.connect(self._on_live_font_combo_changed)
        kbd_bar.addWidget(self.combo_live_font, 1)

        comp_layout.addLayout(kbd_bar)

        # Cinta Rápida de Inserción de Invisibles y Decoradores de Selección
        quick_ribbon = QHBoxLayout()
        quick_ribbon.setSpacing(6)

        self.btn_quick_inv = QPushButton()
        self.btn_quick_inv.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_quick_inv.setToolTip("Inserta Hangul Filler (U+3164) en tu cursor")
        self.btn_quick_inv.clicked.connect(lambda: self.insert_at_cursor("\u3164", "[ㅤU+3164]"))
        quick_ribbon.addWidget(self.btn_quick_inv)

        self.btn_quick_braille = QPushButton()
        self.btn_quick_braille.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_quick_braille.setToolTip("Inserta Vacío Braille (U+2800) para Bios")
        self.btn_quick_braille.clicked.connect(lambda: self.insert_at_cursor("\u2800", "[⠀U+2800]"))
        quick_ribbon.addWidget(self.btn_quick_braille)

        self.btn_quick_strike = QPushButton()
        self.btn_quick_strike.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_quick_strike.clicked.connect(lambda: self.apply_combiner("\u0336"))
        quick_ribbon.addWidget(self.btn_quick_strike)

        self.btn_quick_under = QPushButton()
        self.btn_quick_under.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_quick_under.clicked.connect(lambda: self.apply_combiner("\u0332"))
        quick_ribbon.addWidget(self.btn_quick_under)

        self.btn_quick_clean = QPushButton()
        self.btn_quick_clean.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_quick_clean.clicked.connect(self.clean_selected_or_all_font)
        quick_ribbon.addWidget(self.btn_quick_clean)

        comp_layout.addLayout(quick_ribbon)

        # Editor Maestro
        self.editor = LiveComposerTextEdit()
        self.editor.setMinimumHeight(175)
        self.editor.textChanged.connect(self._on_editor_text_changed)
        self.editor.selectionChanged.connect(self._on_editor_selection_changed)
        comp_layout.addWidget(self.editor, 1)

        # Barra de Rayos-X de Caracteres Invisibles
        xray_hdr = QHBoxLayout()
        self.btn_xray_toggle = QPushButton()
        self.btn_xray_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_xray_toggle.clicked.connect(self._toggle_xray)
        xray_hdr.addWidget(self.btn_xray_toggle)
        xray_hdr.addStretch()
        comp_layout.addLayout(xray_hdr)

        self.xray_frame = QFrame()
        self.xray_frame.setObjectName("xrayBox")
        xray_lay = QVBoxLayout(self.xray_frame)
        xray_lay.setContentsMargins(10, 8, 10, 8)
        self.lbl_xray_content = QLabel()
        self.lbl_xray_content.setWordWrap(True)
        xray_lay.addWidget(self.lbl_xray_content)
        self.xray_frame.hide()
        comp_layout.addWidget(self.xray_frame)

        # Vista Previa en Plataforma (Mockup Gamer / Bio / Chat)
        mockup_hdr = QHBoxLayout()
        self.lbl_mockup_title = QLabel()
        mockup_hdr.addWidget(self.lbl_mockup_title)
        mockup_hdr.addStretch()
        self.combo_mockup = QComboBox()
        self.combo_mockup.currentIndexChanged.connect(self._update_mockup_preview)
        mockup_hdr.addWidget(self.combo_mockup)
        comp_layout.addLayout(mockup_hdr)

        self.mockup_frame = QFrame()
        self.mockup_frame.setObjectName("mockupBox")
        m_lay = QVBoxLayout(self.mockup_frame)
        m_lay.setContentsMargins(12, 10, 12, 10)
        self.lbl_mockup_preview = QLabel()
        self.lbl_mockup_preview.setWordWrap(True)
        m_lay.addWidget(self.lbl_mockup_preview)
        comp_layout.addWidget(self.mockup_frame)

        # Botones de Acción Final (Copiar Todo, Guardar en Favoritos, Vaciar)
        action_bar = QHBoxLayout()
        action_bar.setSpacing(8)

        self.btn_copy_all = QPushButton()
        self.btn_copy_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_copy_all.setMinimumHeight(46)
        self.btn_copy_all.clicked.connect(self.copy_master_composition)
        action_bar.addWidget(self.btn_copy_all, 1)

        self.btn_save_fav = QPushButton()
        self.btn_save_fav.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save_fav.setMinimumHeight(46)
        self.btn_save_fav.clicked.connect(self.save_current_to_favorites)
        action_bar.addWidget(self.btn_save_fav)

        self.btn_clear_all = QPushButton()
        self.btn_clear_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_clear_all.setMinimumHeight(46)
        self.btn_clear_all.clicked.connect(lambda: self.editor.clear())
        action_bar.addWidget(self.btn_clear_all)

        comp_layout.addLayout(action_bar)

        workspace_layout.addWidget(self.composer_pane, 43)

        # === PANEL DERECHO: CATÁLOGO Y ESTUDIOS INTERACTIVOS ===
        self.catalog_pane = QFrame()
        self.catalog_pane.setObjectName("catalogPane")
        cat_layout = QVBoxLayout(self.catalog_pane)
        cat_layout.setContentsMargins(18, 16, 18, 16)
        cat_layout.setSpacing(12)

        # Selector de Modo del Estudio (5 Pestañas Editoriales)
        nav_bar = QHBoxLayout()
        nav_bar.setSpacing(6)
        self.nav_buttons: list[QPushButton] = []
        for idx in range(5):
            b = QPushButton()
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setMinimumHeight(38)
            b.clicked.connect(lambda checked, i=idx: self.switch_studio_tab(i))
            nav_bar.addWidget(b)
            self.nav_buttons.append(b)
        cat_layout.addLayout(nav_bar)

        self.stack = QStackedWidget()
        cat_layout.addWidget(self.stack, 1)

        # Construir las 5 páginas del catálogo
        self._build_page_fonts()
        self._build_page_invisibles_and_symbols()
        self._build_page_frames_and_kaomojis()
        self._build_page_emojis()
        self._build_page_favorites()

        workspace_layout.addWidget(self.catalog_pane, 57)
        main_layout.addLayout(workspace_layout, 1)

        self.active_tab_idx = 0

    # ─────────────────────────────────────────────────────────────────────────
    #  Página 0: Estudio de Fuentes Unicode (30+ Tipografías)
    # ─────────────────────────────────────────────────────────────────────────

    def _build_page_fonts(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 4, 0, 0)
        lay.setSpacing(10)

        # Barra de muestra de texto + sincronización
        top_row = QHBoxLayout()
        top_row.setSpacing(8)
        self.input_font_sample = QLineEdit("Hola MediaHub 2026")
        self.input_font_sample.textChanged.connect(self._refresh_font_cards_preview)
        top_row.addWidget(self.input_font_sample, 1)

        self.btn_sync_sample = QPushButton()
        self.btn_sync_sample.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_sync_sample.clicked.connect(self._sync_sample_from_editor)
        top_row.addWidget(self.btn_sync_sample)
        lay.addLayout(top_row)

        # Píldoras de filtro de categoría tipográfica
        cat_row = QHBoxLayout()
        cat_row.setSpacing(6)
        self.font_cat_buttons: dict[str, QPushButton] = {}
        font_cats = ["all", "gothic", "script", "serif", "sans", "boxed", "decorated"]
        for cid in font_cats:
            btn = QPushButton()
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedHeight(28)
            btn.clicked.connect(lambda checked, c=cid: self._set_font_category(c))
            cat_row.addWidget(btn)
            self.font_cat_buttons[cid] = btn
        cat_row.addStretch()
        lay.addLayout(cat_row)

        # Área desplazable con las tarjetas de cada fuente
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.fonts_container = QWidget()
        self.fonts_grid = QVBoxLayout(self.fonts_container)
        self.fonts_grid.setContentsMargins(0, 0, 6, 0)
        self.fonts_grid.setSpacing(8)

        self.font_cards_widgets: dict[str, dict] = {}
        for style in FONT_STYLES:
            if style["id"] == "normal":
                continue
            sid = style["id"]
            card = QFrame()
            card.setObjectName("subCard")
            c_lay = QHBoxLayout(card)
            c_lay.setContentsMargins(14, 10, 14, 10)
            c_lay.setSpacing(12)

            info_col = QVBoxLayout()
            info_col.setSpacing(3)

            hdr_line = QHBoxLayout()
            lbl_name = QLabel(style["name_es"])
            lbl_badge = QLabel(style["badge"])
            hdr_line.addWidget(lbl_name)
            hdr_line.addWidget(lbl_badge)
            hdr_line.addStretch()
            info_col.addLayout(hdr_line)

            lbl_preview = QLabel()
            lbl_preview.setWordWrap(True)
            lbl_preview.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            info_col.addWidget(lbl_preview)

            c_lay.addLayout(info_col, 1)

            # Botones de acción de la fuente
            btn_col = QHBoxLayout()
            btn_col.setSpacing(6)

            btn_apply = QPushButton()
            btn_apply.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_apply.clicked.connect(lambda checked, s=sid: self.apply_or_insert_font(s))
            btn_col.addWidget(btn_apply)

            btn_kbd = QPushButton()
            btn_kbd.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_kbd.clicked.connect(lambda checked, s=sid: self.activate_live_keyboard_font(s))
            btn_col.addWidget(btn_kbd)

            btn_copy = QPushButton()
            btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_copy.clicked.connect(lambda checked, s=sid: self.copy_single_font_preview(s))
            btn_col.addWidget(btn_copy)

            c_lay.addLayout(btn_col)
            self.fonts_grid.addWidget(card)

            self.font_cards_widgets[sid] = {
                "card": card,
                "style": style,
                "lbl_name": lbl_name,
                "lbl_badge": lbl_badge,
                "lbl_preview": lbl_preview,
                "btn_apply": btn_apply,
                "btn_kbd": btn_kbd,
                "btn_copy": btn_copy,
            }

        self.fonts_grid.addStretch()
        scroll.setWidget(self.fonts_container)
        lay.addWidget(scroll, 1)
        self.stack.addWidget(page)

    # ─────────────────────────────────────────────────────────────────────────
    #  Página 1: Caracteres Invisibles & Bóveda de Símbolos Especiales
    # ─────────────────────────────────────────────────────────────────────────

    def _build_page_invisibles_and_symbols(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 4, 0, 0)
        lay.setSpacing(10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        c_lay = QVBoxLayout(content)
        c_lay.setContentsMargins(0, 0, 6, 0)
        c_lay.setSpacing(12)

        # 1. Sección Destacada: Laboratorio de Caracteres Invisibles
        inv_hdr_row = QHBoxLayout()
        self.lbl_inv_header = QLabel()
        inv_hdr_row.addWidget(self.lbl_inv_header)
        inv_hdr_row.addStretch()

        self.lbl_inv_qty = QLabel()
        inv_hdr_row.addWidget(self.lbl_inv_qty)
        self.combo_inv_qty = QComboBox()
        self.combo_inv_qty.addItems(["x1", "x2", "x3", "x5", "x10"])
        inv_hdr_row.addWidget(self.combo_inv_qty)
        c_lay.addLayout(inv_hdr_row)

        self.lbl_inv_sub = QLabel()
        self.lbl_inv_sub.setWordWrap(True)
        c_lay.addWidget(self.lbl_inv_sub)

        inv_grid = QGridLayout()
        inv_grid.setSpacing(8)
        self.inv_card_refs: list[dict] = []

        for idx, item in enumerate(INVISIBLE_CHARACTERS):
            card = QFrame()
            card.setObjectName("subCard")
            v = QVBoxLayout(card)
            v.setContentsMargins(12, 10, 12, 10)
            v.setSpacing(5)

            top = QHBoxLayout()
            lbl_code = QLabel(f"{item['code']} • {item['xray_tag']}")
            lbl_badge = QLabel(item["badge"])
            top.addWidget(lbl_code)
            top.addStretch()
            top.addWidget(lbl_badge)
            v.addLayout(top)

            lbl_title = QLabel(item["name_es"])
            lbl_title.setWordWrap(True)
            v.addWidget(lbl_title)

            lbl_desc = QLabel(item["desc_es"])
            lbl_desc.setWordWrap(True)
            v.addWidget(lbl_desc)

            btns = QHBoxLayout()
            btn_ins = QPushButton()
            btn_ins.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_ins.clicked.connect(
                lambda checked, ch=item["char"], tag=item["xray_tag"]: self._insert_invisible_with_qty(ch, tag)
            )
            btn_cp = QPushButton()
            btn_cp.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_cp.clicked.connect(
                lambda checked, ch=item["char"], tag=item["xray_tag"]: self._copy_invisible_with_qty(ch, tag)
            )
            btns.addWidget(btn_ins, 1)
            btns.addWidget(btn_cp)
            v.addLayout(btns)

            inv_grid.addWidget(card, idx // 2, idx % 2)
            self.inv_card_refs.append({
                "item": item,
                "lbl_code": lbl_code,
                "lbl_badge": lbl_badge,
                "lbl_title": lbl_title,
                "lbl_desc": lbl_desc,
                "btn_ins": btn_ins,
                "btn_cp": btn_cp,
            })

        c_lay.addLayout(inv_grid)

        # 2. Bóveda de Símbolos Especiales
        self.lbl_sym_header = QLabel()
        c_lay.addWidget(self.lbl_sym_header)

        # Selector de categoría de símbolos
        sym_cat_row = QHBoxLayout()
        sym_cat_row.setSpacing(6)
        self.sym_cat_buttons: dict[str, QPushButton] = {}
        for scat in SYMBOL_CATEGORIES:
            btn = QPushButton(scat["name_es"].split()[0] + " " + scat["name_es"].split()[1])
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedHeight(30)
            btn.clicked.connect(lambda checked, cid=scat["id"]: self._set_symbol_category(cid))
            sym_cat_row.addWidget(btn)
            self.sym_cat_buttons[scat["id"]] = btn
        sym_cat_row.addStretch()
        c_lay.addLayout(sym_cat_row)

        self.lbl_sym_status = QLabel()
        c_lay.addWidget(self.lbl_sym_status)

        self.sym_grid_container = QWidget()
        self.sym_grid_layout = QGridLayout(self.sym_grid_container)
        self.sym_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.sym_grid_layout.setSpacing(6)
        c_lay.addWidget(self.sym_grid_container)

        c_lay.addStretch()
        scroll.setWidget(content)
        lay.addWidget(scroll, 1)
        self.stack.addWidget(page)

    # ─────────────────────────────────────────────────────────────────────────
    #  Página 2: Marcos Envolventes, Separadores & Kaomojis
    # ─────────────────────────────────────────────────────────────────────────

    def _build_page_frames_and_kaomojis(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 4, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        c_lay = QVBoxLayout(content)
        c_lay.setContentsMargins(0, 0, 6, 0)
        c_lay.setSpacing(12)

        # 1. Marcos Envolventes
        self.lbl_frames_header = QLabel()
        c_lay.addWidget(self.lbl_frames_header)

        frames_grid = QGridLayout()
        frames_grid.setSpacing(8)
        self.wrapper_buttons: list[QPushButton] = []
        for idx, w in enumerate(TEXT_WRAPPERS):
            btn = QPushButton(f"{w['prefix']}Texto{w['suffix']}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(40)
            btn.setToolTip(w["name"])
            btn.clicked.connect(
                lambda checked, p=w["prefix"], s=w["suffix"], n=w["name"]: self.wrap_selection_or_line(p, s, n)
            )
            frames_grid.addWidget(btn, idx // 2, idx % 2)
            self.wrapper_buttons.append(btn)
        c_lay.addLayout(frames_grid)

        # 2. Divisores Estéticos
        self.lbl_dividers_header = QLabel()
        c_lay.addWidget(self.lbl_dividers_header)

        div_grid = QGridLayout()
        div_grid.setSpacing(8)
        self.divider_buttons: list[QPushButton] = []
        for idx, div_str in enumerate(AESTHETIC_DIVIDERS):
            btn = QPushButton(div_str)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(36)
            btn.clicked.connect(lambda checked, d=div_str: self.insert_at_cursor(d, d[:16]))
            div_grid.addWidget(btn, idx // 2, idx % 2)
            self.divider_buttons.append(btn)
        c_lay.addLayout(div_grid)

        # 3. Kaomojis
        self.lbl_kaomoji_header = QLabel()
        c_lay.addWidget(self.lbl_kaomoji_header)

        self.kaomoji_buttons: list[QPushButton] = []
        for kcat in KAOMOJI_CATEGORIES:
            lbl_k = QLabel(kcat["name_es"])
            c_lay.addWidget(lbl_k)
            k_grid = QGridLayout()
            k_grid.setSpacing(6)
            for idx, kao in enumerate(kcat["items"]):
                btn = QPushButton(kao)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setMinimumHeight(36)
                btn.clicked.connect(lambda checked, k=kao: self.insert_at_cursor(k, k))
                k_grid.addWidget(btn, idx // 5, idx % 5)
                self.kaomoji_buttons.append(btn)
            c_lay.addLayout(k_grid)

        c_lay.addStretch()
        scroll.setWidget(content)
        lay.addWidget(scroll, 1)
        self.stack.addWidget(page)

    # ─────────────────────────────────────────────────────────────────────────
    #  Página 3: Estudio de Emojis & Combos Estéticos
    # ─────────────────────────────────────────────────────────────────────────

    def _build_page_emojis(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 4, 0, 0)
        lay.setSpacing(10)

        self.input_emoji_search = QLineEdit()
        self.input_emoji_search.textChanged.connect(self._refresh_emoji_grid)
        lay.addWidget(self.input_emoji_search)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        c_lay = QVBoxLayout(content)
        c_lay.setContentsMargins(0, 0, 6, 0)
        c_lay.setSpacing(10)

        self.lbl_combos_header = QLabel()
        c_lay.addWidget(self.lbl_combos_header)

        combos_grid = QGridLayout()
        combos_grid.setSpacing(8)
        self.combo_emoji_buttons: list[QPushButton] = []
        for idx, item in enumerate(AESTHETIC_EMOJI_COMBOS):
            btn = QPushButton(f"{item['combo']}  {item['label']}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(36)
            btn.clicked.connect(lambda checked, c=item["combo"]: self.insert_at_cursor(c, c))
            combos_grid.addWidget(btn, idx // 3, idx % 3)
            self.combo_emoji_buttons.append(btn)
        c_lay.addLayout(combos_grid)

        self.emoji_cats_container = QWidget()
        self.emoji_cats_layout = QVBoxLayout(self.emoji_cats_container)
        self.emoji_cats_layout.setContentsMargins(0, 0, 0, 0)
        self.emoji_cats_layout.setSpacing(10)
        c_lay.addWidget(self.emoji_cats_container)

        c_lay.addStretch()
        scroll.setWidget(content)
        lay.addWidget(scroll, 1)
        self.stack.addWidget(page)

    # ─────────────────────────────────────────────────────────────────────────
    #  Página 4: Favoritos & Historial
    # ─────────────────────────────────────────────────────────────────────────

    def _build_page_favorites(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 4, 0, 0)
        lay.setSpacing(10)

        self.lbl_favs_header = QLabel()
        lay.addWidget(self.lbl_favs_header)

        self.lbl_favs_empty = QLabel()
        self.lbl_favs_empty.setWordWrap(True)
        lay.addWidget(self.lbl_favs_empty)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.favs_container = QWidget()
        self.favs_list_layout = QVBoxLayout(self.favs_container)
        self.favs_list_layout.setContentsMargins(0, 0, 6, 0)
        self.favs_list_layout.setSpacing(8)
        scroll.setWidget(self.favs_container)
        lay.addWidget(scroll, 1)

        self.stack.addWidget(page)

    # ─────────────────────────────────────────────────────────────────────────
    #  Lógica de Composición, Inserción y Transformación
    # ─────────────────────────────────────────────────────────────────────────

    def _populate_live_font_combo(self):
        self.combo_live_font.blockSignals(True)
        self.combo_live_font.clear()
        for style in FONT_STYLES:
            sid = style["id"]
            label_name = style[f"name_{self.lang}"]
            sample = TypographyEngine.transform_text("Abc", sid) if sid != "normal" else "Abc"
            self.combo_live_font.addItem(f"{sample}  —  {label_name}", sid)
        self.combo_live_font.blockSignals(False)

    def _on_live_font_combo_changed(self, idx: int):
        sid = self.combo_live_font.itemData(idx) or "normal"
        self.editor.active_font_id = sid
        self._update_font_cards_kbd_state()
        style = FONT_STYLES_BY_ID.get(sid, {})
        name = style.get(f"name_{self.lang}", sid)
        if sid != "normal":
            self.show_toast(self.tr_str("toast_kbd", item=name))
        self.editor.setFocus()

    def activate_live_keyboard_font(self, style_id: str):
        for i in range(self.combo_live_font.count()):
            if self.combo_live_font.itemData(i) == style_id:
                self.combo_live_font.setCurrentIndex(i)
                break
        self.editor.setFocus()

    def _update_font_cards_kbd_state(self):
        active_id = self.editor.active_font_id
        t = THEMES[self.current_theme_id]
        for sid, refs in self.font_cards_widgets.items():
            btn = refs["btn_kbd"]
            if sid == active_id:
                btn.setText(self.tr_str("btn_active_kbd"))
                btn.setStyleSheet(self._btn_style(t["secondary_accent"], "#FFFFFF", t["secondary_accent"]))
            else:
                btn.setText(self.tr_str("btn_use_kbd"))
                btn.setStyleSheet(self._btn_style(t["bg_subtle"], t["text_primary"], t["border_strong"]))

    def insert_at_cursor(self, text_to_insert: str, label_for_toast: str = ""):
        cursor = self.editor.textCursor()
        cursor.insertText(text_to_insert)
        self.editor.setTextCursor(cursor)
        self.editor.setFocus()
        if label_for_toast:
            self.show_toast(self.tr_str("toast_inserted", item=label_for_toast))

    def _insert_invisible_with_qty(self, ch: str, tag: str):
        qty_str = self.combo_inv_qty.currentText().lstrip("x")
        qty = int(qty_str) if qty_str.isdigit() else 1
        self.insert_at_cursor(ch * qty, f"{tag} ×{qty}")
        if not self.xray_enabled:
            self._toggle_xray(force_on=True)

    def _copy_invisible_with_qty(self, ch: str, tag: str):
        qty_str = self.combo_inv_qty.currentText().lstrip("x")
        qty = int(qty_str) if qty_str.isdigit() else 1
        QApplication.clipboard().setText(ch * qty)
        self.show_toast(self.tr_str("toast_copied", item=f"{tag} ×{qty}"))

    def apply_or_insert_font(self, style_id: str):
        """
        Si el usuario tiene texto seleccionado en su Mesa de Composición, transforma
        únicamente esa selección a `style_id`.
        Si no hay selección pero escribió una frase en la barra de muestra de fuentes,
        inserta esa frase transformada en el cursor (o transforma todo el lienzo si coincide).
        """
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            selected_txt = cursor.selectedText().replace("\u2029", "\n")
            styled = TypographyEngine.transform_text(selected_txt, style_id)
            cursor.insertText(styled)
            self.editor.setTextCursor(cursor)
            self.editor.setFocus()
            self.show_toast(self.tr_str("toast_inserted", item=styled[:22]))
            return

        sample_txt = self.input_font_sample.text().strip()
        canvas_txt = self.editor.toPlainText()
        if sample_txt and sample_txt != "Hola MediaHub 2026":
            styled = TypographyEngine.transform_text(sample_txt, style_id)
            if not canvas_txt.strip():
                self.editor.setPlainText(styled)
            else:
                cursor.insertText(styled)
                self.editor.setTextCursor(cursor)
            self.editor.setFocus()
            self.show_toast(self.tr_str("toast_inserted", item=styled[:22]))
        else:
            # Transformar el texto actual del lienzo
            if canvas_txt.strip():
                styled = TypographyEngine.transform_text(canvas_txt, style_id)
                self.editor.setPlainText(styled)
                self.show_toast(self.tr_str("toast_inserted", item=styled[:22]))
            else:
                styled = TypographyEngine.transform_text("Hola MediaHub", style_id)
                self.editor.setPlainText(styled)

    def copy_single_font_preview(self, style_id: str):
        sample_txt = self.input_font_sample.text().strip() or self.editor.toPlainText().strip() or "Hola MediaHub"
        styled = TypographyEngine.transform_text(sample_txt, style_id)
        QApplication.clipboard().setText(styled)
        self.show_toast(self.tr_str("toast_copied", item=styled[:24]))

    def apply_combiner(self, mark: str):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            sel = cursor.selectedText().replace("\u2029", "\n")
            cursor.insertText(TypographyEngine.apply_combining_mark(sel, mark))
        else:
            all_txt = self.editor.toPlainText()
            if all_txt:
                self.editor.setPlainText(TypographyEngine.apply_combining_mark(all_txt, mark))
        self.editor.setFocus()

    def clean_selected_or_all_font(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            sel = cursor.selectedText().replace("\u2029", "\n")
            cursor.insertText(TypographyEngine.normalize_to_plain(sel))
        else:
            all_txt = self.editor.toPlainText()
            if all_txt:
                self.editor.setPlainText(TypographyEngine.normalize_to_plain(all_txt))
        self.editor.setFocus()

    def wrap_selection_or_line(self, prefix: str, suffix: str, name: str):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            sel = cursor.selectedText().replace("\u2029", "\n")
            cursor.insertText(f"{prefix}{sel}{suffix}")
        else:
            all_txt = self.editor.toPlainText().strip()
            if all_txt and "\n" not in all_txt:
                self.editor.setPlainText(f"{prefix}{all_txt}{suffix}")
            else:
                cursor.insertText(f"{prefix}{suffix}")
                for _ in range(len(suffix)):
                    cursor.movePosition(QTextCursor.MoveOperation.Left)
                self.editor.setTextCursor(cursor)
        self.editor.setFocus()
        self.show_toast(self.tr_str("toast_wrapped", item=name))

    def copy_master_composition(self):
        txt = self.editor.toPlainText()
        if not txt:
            return
        QApplication.clipboard().setText(txt)
        if txt not in self.history:
            self.history.insert(0, txt)
            self._refresh_favorites_page()

        t = THEMES[self.current_theme_id]
        self.btn_copy_all.setText(self.tr_str("btn_copied_master"))
        self.btn_copy_all.setStyleSheet(self._btn_style(t["success"], "#FFFFFF", t["success"], font_pt=11))
        QTimer.singleShot(1800, self._restore_copy_btn)

    def _restore_copy_btn(self):
        t = THEMES[self.current_theme_id]
        self.btn_copy_all.setText(self.tr_str("btn_copy_master"))
        self.btn_copy_all.setStyleSheet(self._btn_style(t["accent"], t["accent_text"], t["accent"], font_pt=11))

    def save_current_to_favorites(self):
        txt = self.editor.toPlainText().strip()
        if not txt:
            return
        if txt not in self.favorites:
            self.favorites.insert(0, txt)
            self._save_favorites()
            self._refresh_favorites_page()
        self.show_toast("★ Guardado en tus Favoritos")

    # ─────────────────────────────────────────────────────────────────────────
    #  Actualización de Vistas Previas, Rayos-X y Contadores
    # ─────────────────────────────────────────────────────────────────────────

    def _on_editor_text_changed(self):
        txt = self.editor.toPlainText()
        chars = len(txt)
        words = len(txt.split()) if txt.strip() else 0
        inv_count = sum(1 for c in txt if c in INVISIBLE_CHARS_SET)

        self.lbl_stats.setText(self.tr_str("stats_fmt", chars=chars, words=words, inv=inv_count))
        self._update_xray_view(txt, inv_count)
        self._update_mockup_preview()

    def _on_editor_selection_changed(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            sel = cursor.selectedText().replace("\u2029", " ").strip()
            if sel and len(sel) <= 60:
                self.input_font_sample.setText(sel)

    def _sync_sample_from_editor(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            txt = cursor.selectedText().replace("\u2029", " ").strip()
        else:
            txt = self.editor.toPlainText().replace("\n", " ").strip()
        if txt:
            self.input_font_sample.setText(txt[:60])

    def _toggle_xray(self, force_on: bool = False):
        if force_on:
            self.xray_enabled = True
        else:
            self.xray_enabled = not self.xray_enabled
        self.xray_frame.setVisible(self.xray_enabled)
        self.btn_xray_toggle.setText(
            self.tr_str("xray_toggle_on") if self.xray_enabled else self.tr_str("xray_toggle_off")
        )
        txt = self.editor.toPlainText()
        inv_count = sum(1 for c in txt if c in INVISIBLE_CHARS_SET)
        self._update_xray_view(txt, inv_count)

    def _update_xray_view(self, txt: str, inv_count: int):
        if not self.xray_enabled:
            return
        if inv_count == 0:
            self.lbl_xray_content.setText(self.tr_str("xray_empty"))
            return
        revealed = []
        for ch in txt:
            if ch in INVISIBLE_CHARS_SET:
                revealed.append(f" {INVISIBLE_CHARS_SET[ch]} ")
            else:
                revealed.append(ch)
        self.lbl_xray_content.setText("🔍 Rayos-X: " + "".join(revealed))

    def _update_mockup_preview(self):
        txt = self.editor.toPlainText().strip() or "ℌ𝔬𝔩𝔞"
        mode = self.combo_mockup.currentIndex()
        first_line = txt.split("\n")[0][:42]
        if mode == 0:
            # Gamer / Discord Nick
            self.lbl_mockup_preview.setText(f"🟢  {first_line}  #0001   •   En partida competitiva")
        elif mode == 1:
            # Bio Instagram / TikTok
            self.lbl_mockup_preview.setText(f"📸 @usuario.atelier\n{txt}")
        else:
            # Chat Message
            self.lbl_mockup_preview.setText(f"💬 Tú hoy a las 18:45:\n{txt}")

    # ─────────────────────────────────────────────────────────────────────────
    #  Refresco de Catálogos (Fuentes, Símbolos, Emojis, Favoritos)
    # ─────────────────────────────────────────────────────────────────────────

    def _refresh_font_cards_preview(self):
        sample = self.input_font_sample.text().strip() or "Hola MediaHub 2026"
        for sid, refs in self.font_cards_widgets.items():
            styled = TypographyEngine.transform_text(sample, sid)
            refs["lbl_preview"].setText(styled)

    def _set_font_category(self, cat_id: str):
        self.active_font_cat = cat_id
        t = THEMES[self.current_theme_id]
        for cid, btn in self.font_cat_buttons.items():
            if cid == cat_id:
                btn.setStyleSheet(self._btn_style(t["accent"], t["accent_text"], t["accent"], font_pt=8.5, pad="3px 10px"))
            else:
                btn.setStyleSheet(self._btn_style(t["bg_subtle"], t["text_secondary"], t["border"], font_pt=8.5, pad="3px 10px"))

        for sid, refs in self.font_cards_widgets.items():
            style_cat = refs["style"]["category"]
            refs["card"].setVisible(cat_id == "all" or style_cat == cat_id)

    def _set_symbol_category(self, cat_id: str):
        self.active_symbol_cat = cat_id
        t = THEMES[self.current_theme_id]
        for cid, btn in self.sym_cat_buttons.items():
            if cid == cat_id:
                btn.setStyleSheet(self._btn_style(t["accent"], t["accent_text"], t["accent"], font_pt=9, pad="4px 10px"))
            else:
                btn.setStyleSheet(self._btn_style(t["bg_subtle"], t["text_secondary"], t["border"], font_pt=9, pad="4px 10px"))

        # Limpiar y poblar cuadrícula de símbolos
        while self.sym_grid_layout.count():
            item = self.sym_grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cat_data = next((c for c in SYMBOL_CATEGORIES if c["id"] == cat_id), SYMBOL_CATEGORIES[0])
        btn_qss = self._btn_style(t["bg_card"], t["text_primary"], t["border"], font_pt=14, pad="6px")
        for idx, sym in enumerate(cat_data["symbols"]):
            b = QPushButton(sym)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setFixedSize(48, 44)
            b.setStyleSheet(btn_qss)
            code_str = f"U+{ord(sym[0]):04X}"
            b.setToolTip(f"Símbolo {sym} ({code_str}) — Clic para insertar")
            b.clicked.connect(lambda checked, s=sym, c=code_str: self._on_symbol_clicked(s, c))
            self.sym_grid_layout.addWidget(b, idx // 8, idx % 8)

    def _on_symbol_clicked(self, sym: str, code_str: str):
        self.insert_at_cursor(sym, f"{sym} ({code_str})")
        self.lbl_sym_status.setText(f"✨ Insertado en tu caja:  {sym}   •   Código Unicode: {code_str}")

    def _refresh_emoji_grid(self):
        query = self.input_emoji_search.text().strip().lower()
        t = THEMES[self.current_theme_id]

        while self.emoji_cats_layout.count():
            item = self.emoji_cats_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        btn_qss = self._btn_style(t["bg_card"], t["text_primary"], t["border"], font_pt=14, pad="4px")

        for ecat in EMOJI_CATEGORIES:
            filtered = [
                (em, kw) for (em, kw) in ecat["emojis"]
                if not query or query in kw.lower() or query in em
            ]
            if not filtered:
                continue

            sec_widget = QWidget()
            sec_lay = QVBoxLayout(sec_widget)
            sec_lay.setContentsMargins(0, 4, 0, 4)
            sec_lay.setSpacing(6)

            lbl = QLabel(ecat[f"name_{self.lang}"])
            lbl.setStyleSheet(f"font-weight: 700; font-size: 10pt; color: {t['text_secondary']};")
            sec_lay.addWidget(lbl)

            grid = QGridLayout()
            grid.setSpacing(6)
            for idx, (em, kw) in enumerate(filtered):
                b = QPushButton(em)
                b.setCursor(Qt.CursorShape.PointingHandCursor)
                b.setFixedSize(46, 42)
                b.setStyleSheet(btn_qss)
                b.setToolTip(kw.capitalize())
                b.clicked.connect(lambda checked, e=em: self.insert_at_cursor(e, e))
                grid.addWidget(b, idx // 8, idx % 8)
            sec_lay.addLayout(grid)
            self.emoji_cats_layout.addWidget(sec_widget)

    def _refresh_favorites_page(self):
        t = THEMES[self.current_theme_id]
        while self.favs_list_layout.count():
            item = self.favs_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        combined = []
        for fav in self.favorites:
            combined.append(("★ FAVORITO", fav, True))
        for hist in self.history:
            if hist not in self.favorites:
                combined.append(("🕒 RECIENTE", hist, False))

        for badge_txt, text_val, is_fav in combined:
            card = QFrame()
            card.setObjectName("subCard")
            row = QHBoxLayout(card)
            row.setContentsMargins(14, 10, 14, 10)
            row.setSpacing(10)

            badge = QLabel(badge_txt)
            badge.setStyleSheet(
                f"background: {t['badge_bg']}; color: {t['badge_fg']}; padding: 3px 8px; border-radius: 6px; font-size: 8pt; font-weight: 700;"
            )
            row.addWidget(badge)

            lbl = QLabel(text_val)
            lbl.setWordWrap(True)
            lbl.setStyleSheet(f"font-size: 11.5pt; color: {t['text_primary']};")
            row.addWidget(lbl, 1)

            btn_load = QPushButton(self.tr_str("btn_load_canvas"))
            btn_load.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_load.setStyleSheet(self._btn_style(t["accent"], t["accent_text"], t["accent"], font_pt=9))
            btn_load.clicked.connect(lambda checked, v=text_val: self.editor.setPlainText(v))
            row.addWidget(btn_load)

            btn_cp = QPushButton(self.tr_str("btn_copy_single"))
            btn_cp.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_cp.setStyleSheet(self._btn_style(t["bg_subtle"], t["text_primary"], t["border_strong"], font_pt=9))
            btn_cp.clicked.connect(lambda checked, v=text_val: self._copy_direct(v))
            row.addWidget(btn_cp)

            if is_fav:
                btn_del = QPushButton(self.tr_str("btn_delete"))
                btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
                btn_del.setFixedSize(30, 30)
                btn_del.setStyleSheet(self._btn_style(t["bg_subtle"], t["text_muted"], t["border"], font_pt=9))
                btn_del.clicked.connect(lambda checked, v=text_val: self._remove_favorite(v))
                row.addWidget(btn_del)

            self.favs_list_layout.addWidget(card)

        self.favs_list_layout.addStretch()

    def _copy_direct(self, val: str):
        QApplication.clipboard().setText(val)
        self.show_toast(self.tr_str("toast_copied", item=val[:20]))

    def _remove_favorite(self, val: str):
        if val in self.favorites:
            self.favorites.remove(val)
            self._save_favorites()
            self._refresh_favorites_page()

    # ─────────────────────────────────────────────────────────────────────────
    #  Navegación, Temas y Traducción
    # ─────────────────────────────────────────────────────────────────────────

    def switch_studio_tab(self, idx: int):
        self.active_tab_idx = idx
        self.stack.setCurrentIndex(idx)
        t = THEMES[self.current_theme_id]
        for i, btn in enumerate(self.nav_buttons):
            if i == idx:
                btn.setStyleSheet(self._btn_style(t["accent"], t["accent_text"], t["accent"], font_pt=9.5, pad="6px 12px"))
            else:
                btn.setStyleSheet(self._btn_style(t["bg_subtle"], t["text_primary"], t["border"], font_pt=9.5, pad="6px 12px"))

    def show_toast(self, message: str):
        self.lbl_toast.setText(f"✨ {message}")
        self.lbl_toast.show()
        QTimer.singleShot(2600, self.lbl_toast.hide)

    def _toggle_language(self):
        self.lang = "en" if self.lang == "es" else "es"
        self.btn_lang.setText("EN" if self.lang == "es" else "ES")
        self._populate_live_font_combo()
        self.retranslate_ui()
        self.apply_theme(self.current_theme_id)

    def _btn_style(self, bg: str, fg: str, border: str, font_pt: float = 9.5, pad: str = "6px 12px") -> str:
        return f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                border: 1px solid {border};
                border-radius: 9px;
                padding: {pad};
                font-size: {font_pt}pt;
                font-weight: 700;
            }}
            QPushButton:hover {{
                border: 1.5px solid {THEMES[self.current_theme_id]['accent']};
            }}
        """

    def apply_theme(self, theme_id: str):
        if theme_id not in THEMES:
            theme_id = "paper"
        self.current_theme_id = theme_id
        t = THEMES[theme_id]

        self.setStyleSheet(build_studio_stylesheet(t))

        # Emblema y cabecera editorial
        self.emblem_lbl.setStyleSheet(
            f"background-color: {t['accent']}; color: {t['accent_text']}; border-radius: 12px; font-size: 20pt; font-weight: 900;"
        )
        self.lbl_title.setStyleSheet(
            f"font-family: Georgia, 'Times New Roman', serif; font-size: 18pt; font-weight: 800; color: {t['text_primary']};"
        )
        self.lbl_sub.setStyleSheet(f"font-size: 9.5pt; color: {t['text_secondary']};")
        self.lbl_toast.setStyleSheet(
            f"background-color: {t['secondary_soft']}; color: {t['secondary_accent']}; border: 1px solid {t['secondary_accent']}; border-radius: 8px; padding: 4px 12px; font-weight: 700; font-size: 9pt;"
        )

        # Botones de tema
        for tid, btn in self.theme_buttons.items():
            btn.setText(THEMES[tid][f"name_{self.lang}"])
            if tid == theme_id:
                btn.setStyleSheet(self._btn_style(t["accent"], t["accent_text"], t["accent"], font_pt=9, pad="4px 10px"))
            else:
                btn.setStyleSheet(self._btn_style(t["bg_subtle"], t["text_secondary"], t["border"], font_pt=9, pad="4px 10px"))

        self.btn_lang.setStyleSheet(self._btn_style(t["bg_subtle"], t["text_primary"], t["border_strong"], font_pt=9, pad="4px 8px"))

        # Panel izquierdo
        self.lbl_comp_title.setStyleSheet(f"font-size: 10.5pt; font-weight: 800; letter-spacing: 0.4px; color: {t['accent']};")
        self.lbl_stats.setStyleSheet(f"font-size: 8.5pt; font-weight: 700; color: {t['text_muted']};")
        self.lbl_comp_hint.setStyleSheet(f"font-size: 9pt; color: {t['text_secondary']};")
        self.lbl_live_kbd.setStyleSheet(f"font-size: 9.5pt; font-weight: 700; color: {t['text_primary']};")

        chip_qss = self._btn_style(t["bg_subtle"], t["text_primary"], t["border_strong"], font_pt=8.5, pad="5px 8px")
        for b in (self.btn_quick_inv, self.btn_quick_braille, self.btn_quick_strike, self.btn_quick_under, self.btn_quick_clean):
            b.setStyleSheet(chip_qss)

        self.btn_xray_toggle.setStyleSheet(self._btn_style(t["secondary_soft"], t["secondary_accent"], t["secondary_accent"], font_pt=8.5, pad="4px 10px"))
        self.lbl_xray_content.setStyleSheet(f"font-family: Consolas, monospace; font-size: 9.5pt; color: {t['text_primary']};")
        self.lbl_mockup_title.setStyleSheet(f"font-size: 9pt; font-weight: 700; color: {t['text_secondary']};")
        self.lbl_mockup_preview.setStyleSheet(f"font-size: 10.5pt; color: {t['text_primary']};")

        self.btn_copy_all.setStyleSheet(self._btn_style(t["accent"], t["accent_text"], t["accent"], font_pt=11))
        self.btn_save_fav.setStyleSheet(self._btn_style(t["secondary_soft"], t["secondary_accent"], t["secondary_accent"], font_pt=10))
        self.btn_clear_all.setStyleSheet(self._btn_style(t["bg_subtle"], t["text_secondary"], t["border"], font_pt=10))

        # Tarjetas de fuentes
        self.btn_sync_sample.setStyleSheet(self._btn_style(t["bg_subtle"], t["text_primary"], t["border_strong"], font_pt=9))
        for sid, refs in self.font_cards_widgets.items():
            refs["lbl_name"].setStyleSheet(f"font-size: 9.5pt; font-weight: 700; color: {t['text_secondary']};")
            refs["lbl_badge"].setStyleSheet(
                f"background-color: {t['badge_bg']}; color: {t['badge_fg']}; border-radius: 5px; padding: 2px 7px; font-size: 7.5pt; font-weight: 800;"
            )
            refs["lbl_preview"].setStyleSheet(f"font-size: 14pt; color: {t['text_primary']};")
            refs["btn_apply"].setStyleSheet(self._btn_style(t["accent"], t["accent_text"], t["accent"], font_pt=8.5, pad="5px 10px"))
            refs["btn_copy"].setStyleSheet(self._btn_style(t["bg_subtle"], t["text_primary"], t["border"], font_pt=8.5, pad="5px 10px"))

        self._update_font_cards_kbd_state()
        self._set_font_category(self.active_font_cat)

        # Página Invisibles y Símbolos
        self.lbl_inv_header.setStyleSheet(f"font-size: 10.5pt; font-weight: 800; color: {t['accent']};")
        self.lbl_inv_sub.setStyleSheet(f"font-size: 9pt; color: {t['text_secondary']};")
        self.lbl_sym_header.setStyleSheet(f"font-size: 10.5pt; font-weight: 800; color: {t['accent']};")
        self.lbl_sym_status.setStyleSheet(f"font-size: 9pt; font-weight: 600; color: {t['secondary_accent']};")

        for ref in self.inv_card_refs:
            ref["lbl_code"].setStyleSheet(f"font-family: Consolas, monospace; font-size: 9pt; font-weight: 700; color: {t['secondary_accent']};")
            ref["lbl_badge"].setStyleSheet(
                f"background-color: {t['badge_bg']}; color: {t['badge_fg']}; border-radius: 5px; padding: 2px 6px; font-size: 7.5pt; font-weight: 800;"
            )
            ref["lbl_title"].setStyleSheet(f"font-size: 10pt; font-weight: 800; color: {t['text_primary']};")
            ref["lbl_desc"].setStyleSheet(f"font-size: 8.5pt; color: {t['text_secondary']};")
            ref["btn_ins"].setStyleSheet(self._btn_style(t["accent"], t["accent_text"], t["accent"], font_pt=8.5, pad="5px 8px"))
            ref["btn_cp"].setStyleSheet(self._btn_style(t["bg_subtle"], t["text_primary"], t["border_strong"], font_pt=8.5, pad="5px 8px"))

        self._set_symbol_category(self.active_symbol_cat)

        # Página Marcos, Divisores & Kaomojis
        self.lbl_frames_header.setStyleSheet(f"font-size: 10.5pt; font-weight: 800; color: {t['accent']};")
        self.lbl_dividers_header.setStyleSheet(f"font-size: 10.5pt; font-weight: 800; color: {t['accent']};")
        self.lbl_kaomoji_header.setStyleSheet(f"font-size: 10.5pt; font-weight: 800; color: {t['accent']};")

        card_btn_qss = self._btn_style(t["bg_card"], t["text_primary"], t["border"], font_pt=10, pad="6px 10px")
        for b in self.wrapper_buttons + self.divider_buttons + self.kaomoji_buttons + self.combo_emoji_buttons:
            b.setStyleSheet(card_btn_qss)

        # Página Emojis & Favoritos
        self.lbl_combos_header.setStyleSheet(f"font-size: 10.5pt; font-weight: 800; color: {t['accent']};")
        self.lbl_favs_header.setStyleSheet(f"font-size: 10.5pt; font-weight: 800; color: {t['accent']};")
        self.lbl_favs_empty.setStyleSheet(f"font-size: 9pt; color: {t['text_secondary']};")

        self._refresh_emoji_grid()
        self._refresh_favorites_page()
        self.switch_studio_tab(self.active_tab_idx)

    def retranslate_ui(self):
        self.setWindowTitle(self.tr_str("window_title"))
        self.lbl_title.setText(self.tr_str("masthead_title"))
        self.lbl_sub.setText(self.tr_str("masthead_sub"))

        self.lbl_comp_title.setText(self.tr_str("composer_title"))
        self.lbl_comp_hint.setText(self.tr_str("composer_hint"))
        self.lbl_live_kbd.setText(self.tr_str("live_kbd_label"))

        self.btn_quick_inv.setText(self.tr_str("btn_invisible_quick"))
        self.btn_quick_braille.setText(self.tr_str("btn_braille_quick"))
        self.btn_quick_strike.setText(self.tr_str("btn_strike"))
        self.btn_quick_under.setText(self.tr_str("btn_underline"))
        self.btn_quick_clean.setText(self.tr_str("btn_clean_font"))

        self.btn_xray_toggle.setText(
            self.tr_str("xray_toggle_on") if self.xray_enabled else self.tr_str("xray_toggle_off")
        )
        self.lbl_mockup_title.setText(self.tr_str("mockup_label"))

        self.combo_mockup.blockSignals(True)
        cur_m = max(0, self.combo_mockup.currentIndex())
        self.combo_mockup.clear()
        self.combo_mockup.addItems([
            self.tr_str("mockup_gamer"),
            self.tr_str("mockup_bio"),
            self.tr_str("mockup_chat"),
        ])
        self.combo_mockup.setCurrentIndex(cur_m)
        self.combo_mockup.blockSignals(False)

        self.btn_copy_all.setText(self.tr_str("btn_copy_master"))
        self.btn_save_fav.setText(self.tr_str("btn_save_fav"))
        self.btn_clear_all.setText(self.tr_str("btn_clear"))

        tab_keys = ["tab_fonts", "tab_invisibles", "tab_frames", "tab_emojis", "tab_favs"]
        for i, k in enumerate(tab_keys):
            self.nav_buttons[i].setText(self.tr_str(k))

        self.input_font_sample.setPlaceholderText(self.tr_str("sample_placeholder"))
        self.btn_sync_sample.setText(self.tr_str("sync_from_canvas"))

        cat_map = {
            "all": "cat_all",
            "gothic": "cat_gothic",
            "script": "cat_script",
            "serif": "cat_serif",
            "sans": "cat_sans",
            "boxed": "cat_boxed",
            "decorated": "cat_decorated",
        }
        for cid, k in cat_map.items():
            if cid in self.font_cat_buttons:
                self.font_cat_buttons[cid].setText(self.tr_str(k))

        for sid, refs in self.font_cards_widgets.items():
            st = refs["style"]
            refs["lbl_name"].setText(st[f"name_{self.lang}"])
            refs["btn_apply"].setText(self.tr_str("btn_apply_canvas"))
            refs["btn_copy"].setText(self.tr_str("btn_copy_single"))

        self.lbl_inv_header.setText(self.tr_str("inv_header"))
        self.lbl_inv_sub.setText(self.tr_str("inv_sub"))
        self.lbl_inv_qty.setText(self.tr_str("inv_qty"))
        for ref in self.inv_card_refs:
            it = ref["item"]
            ref["lbl_title"].setText(it[f"name_{self.lang}"])
            ref["lbl_desc"].setText(it[f"desc_{self.lang}"])
            ref["btn_ins"].setText(self.tr_str("btn_insert_cursor"))
            ref["btn_cp"].setText(self.tr_str("btn_copy_pure"))

        self.lbl_sym_header.setText(self.tr_str("sym_header"))
        self.lbl_sym_status.setText(self.tr_str("sym_status_default"))

        self.lbl_frames_header.setText(self.tr_str("frames_header"))
        self.lbl_dividers_header.setText(self.tr_str("dividers_header"))
        self.lbl_kaomoji_header.setText(self.tr_str("kaomoji_header"))

        self.input_emoji_search.setPlaceholderText(self.tr_str("emoji_search"))
        self.lbl_combos_header.setText(self.tr_str("combos_header"))
        self.lbl_favs_header.setText(self.tr_str("favs_header"))
        self.lbl_favs_empty.setText(self.tr_str("favs_empty"))

        self._refresh_font_cards_preview()
        self._on_editor_text_changed()
