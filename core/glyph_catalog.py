"""
core/glyph_catalog.py
─────────────────────
Bóveda de Caracteres Invisibles, Símbolos Especiales, Marcos Decorativos,
Kaomojis, Divisores Estéticos y Emojis para MediaHub-FontFamily.
"""

from __future__ import annotations

# ─────────────────────────────────────────────────────────────────────────────
#  1. Laboratorio de Caracteres Invisibles (Espacios Especiales)
# ─────────────────────────────────────────────────────────────────────────────

INVISIBLE_CHARACTERS: list[dict] = [
    {
        "id": "hangul_filler",
        "char": "\u3164",
        "code": "U+3164",
        "xray_tag": "[ㅤU+3164]",
        "name_es": "Espacio Invisible Rey (Hangul Filler)",
        "name_en": "King Invisible Space (Hangul Filler)",
        "badge": "NICKS & JUEGOS",
        "desc_es": "El carácter invisible más famoso. No es eliminado por filtros de texto: ideal para Nicks vacíos en Free Fire, Discord, Steam y mensajes en blanco en WhatsApp.",
        "desc_en": "The most popular non-collapsing blank glyph. Ideal for blank nicknames in games, Discord, Steam, and empty WhatsApp messages.",
    },
    {
        "id": "braille_blank",
        "char": "\u2800",
        "code": "U+2800",
        "xray_tag": "[⠀U+2800]",
        "name_es": "Vacío Braille (Bio de Instagram & TikTok)",
        "name_en": "Braille Pattern Blank (IG & TikTok Bios)",
        "badge": "BIOS & REDES",
        "desc_es": "Mantiene saltos de línea limpios y centrados en biografías de Instagram, TikTok y X sin que la plataforma borre los espacios.",
        "desc_en": "Preserves clean line breaks and centered text in Instagram, TikTok, and X bios without collapsing.",
    },
    {
        "id": "zwsp",
        "char": "\u200b",
        "code": "U+200B",
        "xray_tag": "[·U+200B]",
        "name_es": "Espacio de Ancho Cero (Zero-Width Space)",
        "name_en": "Zero-Width Space (ZWSP)",
        "badge": "ANCHO CERO",
        "desc_es": "Un carácter 100% invisible que no ocupa espacio visual. Perfecto para insertar entre letras y evitar que un texto active enlaces o menciones automáticas.",
        "desc_en": "Takes zero visual width. Insert between letters to prevent auto-linking or bypass word filters invisibly.",
    },
    {
        "id": "zwnj",
        "char": "\u200c",
        "code": "U+200C",
        "xray_tag": "[∣U+200C]",
        "name_es": "Separador de Glifos (Zero-Width Non-Joiner)",
        "name_en": "Zero-Width Non-Joiner (ZWNJ)",
        "badge": "SEPARADOR",
        "desc_es": "Impide que dos caracteres o ligaduras adyacentes se unan sin añadir separación visible entre ellos.",
        "desc_en": "Prevents adjacent characters or ligatures from joining together without adding visible spacing.",
    },
    {
        "id": "ideographic_space",
        "char": "\u3000",
        "code": "U+3000",
        "xray_tag": "[　U+3000]",
        "name_es": "Espacio Ideográfico Ancho (Fullwidth)",
        "name_en": "Wide Ideographic Space (Fullwidth)",
        "badge": "ESTÉTICO",
        "desc_es": "Espacio japonés de doble ancho para sangrías editoriales y textos estilo Vaporwave / Aesthetic.",
        "desc_en": "Double-width Japanese space for editorial indentation and Vaporwave / Aesthetic layouts.",
    },
    {
        "id": "hair_space",
        "char": "\u200a",
        "code": "U+200A",
        "xray_tag": "[ hair]",
        "name_es": "Micro-Espacio de Cabello (Hair Space)",
        "name_en": "Typographic Hair Space",
        "badge": "EDITORIAL",
        "desc_es": "El espacio visible más fino de Unicode. Separa símbolos pegados a las letras con elegancia tipográfica.",
        "desc_en": "The thinnest visible space in Unicode. Adds delicate breathing room around symbols and punctuation.",
    },
]

INVISIBLE_CHARS_SET = {item["char"]: item["xray_tag"] for item in INVISIBLE_CHARACTERS}


# ─────────────────────────────────────────────────────────────────────────────
#  2. Bóveda de Símbolos Especiales (Categorizados)
# ─────────────────────────────────────────────────────────────────────────────

SYMBOL_CATEGORIES: list[dict] = [
    {
        "id": "stars",
        "name_es": "✦ Estrellas, Astros & Destellos",
        "name_en": "✦ Stars, Celestial & Sparkles",
        "symbols": [
            "✦", "✧", "★", "☆", "✩", "✪", "✫", "✬", "✭", "✮", "✯", "✰",
            "⁂", "⁎", "⁑", "☸", "❂", "✵", "✶", "✷", "✸", "✹", "✺", "✻",
            "✼", "✽", "✾", "✿", "❀", "❁", "❃", "❇", "❈", "❉", "❊", "❋",
            "☽", "☾", "☼", "☀", "☁", "☂", "☃", "☄", "⚡", "❄", "❅", "❆",
        ],
    },
    {
        "id": "frames",
        "name_es": "༺ Corchetes, Alas & Ornamentos",
        "name_en": "༺ Brackets, Wings & Ornaments",
        "symbols": [
            "༺", "༻", "꧁", "꧂", "⸼", "⸽", "『", "』", "【", "】", "〖", "〗",
            "〘", "〙", "〚", "〛", "⌈", "⌉", "⌊", "⌋", "⟬", "⟭", "⟪", "⟫",
            "⟮", "⟯", "«", "»", "‹", "›", "⟨", "⟩", "︵", "︶", "︷", "︸",
            "︹", "︺", "︻", "︼", "︽", "︾", "︿", "﹀", "﹁", "﹂", "﹃", "﹄",
        ],
    },
    {
        "id": "hearts_flora",
        "name_es": "❦ Corazones, Rosas & Realeza",
        "name_en": "❦ Hearts, Flora & Royalty",
        "symbols": [
            "♡", "♥", "❥", "❣", "❦", "❧", "☙", "⚜", "⚘", "☘", "❀", "❁",
            "♔", "♕", "♖", "♗", "♘", "♙", "♚", "♛", "♜", "♝", "♞", "♟",
            "♠", "♢", "♣", "♤", "♦", "♧", "✞", "✟", "✠", "✡", "☥", "☦",
            "☧", "☨", "☩", "☪", "☫", "☬", "☭", "☮", "☯", "☸", " crowned"[0:0] or "♛", "♚",
        ],
    },
    {
        "id": "arrows",
        "name_es": "➔ Flechas, Punteros & Rutas",
        "name_en": "➔ Arrows, Pointers & Paths",
        "symbols": [
            "➔", "➙", "➛", "➜", "➝", "➞", "➟", "➠", "➡", "➢", "➣", "➤",
            "➥", "➦", "➧", "➨", "➳", "➵", "➸", "➺", "➻", "➼", "➽", "➾",
            "←", "↑", "→", "↓", "↔", "↕", "↖", "↗", "↘", "↙", "⇐", "⇑",
            "⇒", "⇓", "⇔", "⟿", "⟶", "⟹", "⟺", "↺", "↻", "⟲", "⟳", "↳",
        ],
    },
    {
        "id": "music_retro",
        "name_es": "♪ Música, Teclas Mac & Símbolos Retro",
        "name_en": "♪ Music, Keycaps & Retro Tech",
        "symbols": [
            "♪", "♫", "♬", "♩", "♭", "♮", "♯", "𝄞", "𝄢", "⌘", "⌥", "⌃",
            "⇧", "⇪", "⌫", "⌦", "⏎", "⎋", "⇥", "⇤", "", "⊞", "⚙", "⚔",
            "⚖", "⚗", "⚘", "⚜", "⚠", "⚡", "☢", "☣", "☤", "♻", "♾", "⌖",
            "⌚", "⌛", "✉", "✎", "✏", "✐", "✑", "✒", "✓", "✔", "✕", "✖",
        ],
    },
    {
        "id": "math_currency",
        "name_es": "∞ Matemática, Griego & Divisas",
        "name_en": "∞ Math, Greek & Currencies",
        "symbols": [
            "∞", "≈", "≠", "≡", "≤", "≥", "±", "∓", "×", "÷", "√", "∛",
            "∑", "∏", "∫", "∬", "∮", "∂", "∆", "∇", "∈", "∉", "∩", "∪",
            "α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "λ", "μ", "π", "ρ",
            "σ", "τ", "φ", "χ", "ψ", "ω", "Ω", "€", "£", "¥", "₿", "¢",
        ],
    },
    {
        "id": "lines_blocks",
        "name_es": "═ Cajas, Bordes & Geometría",
        "name_en": "═ Box Drawing & Geometry",
        "symbols": [
            "─", "━", "│", "┃", "┄", "┅", "┈", "┉", "═", "║", "╔", "╗",
            "╚", "╝", "╠", "╣", "╦", "╩", "╬", "╭", "╮", "╯", "╰", "╱",
            "╲", "╳", "░", "▒", "▓", "█", "▄", "▀", "■", "□", "▪", "▫",
            "▲", "△", "▶", "▷", "▼", "▽", "◀", "◁", "◆", "◇", "◈", "◉",
        ],
    },
    {
        "id": "superscripts_rare",
        "name_es": "™ Índices, Fracciones & Sellos Raros",
        "name_en": "™ Fractions, Numbers & Rare Seals",
        "symbols": [
            "™", "©", "®", "℗", "℠", "№", "℃", "℉", "°", "‰", "‱", "§",
            "¶", "†", "‡", "•", "‣", "․", "‥", "…", "※", "‽", "⁂", "⁋",
            "½", "⅓", "⅔", "¼", "¾", "⅕", "⅖", "⅗", "⅘", "⅙", "⅚", "⅛",
            "Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ", "Ⅹ", "Ⅺ", "Ⅻ",
        ],
    },
]


# ─────────────────────────────────────────────────────────────────────────────
#  3. Marcos Envolventes, Divisores & Kaomojis
# ─────────────────────────────────────────────────────────────────────────────

TEXT_WRAPPERS: list[dict] = [
    {"name": "Alas Imperiales", "prefix": "꧁༺ ", "suffix": " ༻꧂"},
    {"name": "Corchete Japonés", "prefix": "『 ", "suffix": " 』"},
    {"name": "Sello Pesado", "prefix": "【 ", "suffix": " 】"},
    {"name": "Destello Lunar", "prefix": "✧･ﾟ: * ", "suffix": " *:･ﾟ✧"},
    {"name": "Corona Real", "prefix": "♛ ", "suffix": " ♛"},
    {"name": "Ciber Espadas", "prefix": "⚔️ ━━ ", "suffix": " ━━ ⚔️"},
    {"name": "Encaje Floral", "prefix": "✿•┈• ", "suffix": " •┈•✿"},
    {"name": "Francotirador Gamer", "prefix": "▄︻デ ", "suffix": " ══━一"},
    {"name": "Estrella Polar", "prefix": "─── ･ ｡ﾟ☆: *.☽ ", "suffix": " ☾.* :☆ﾟ. ───"},
    {"name": "Doble Diamante", "prefix": "❖ ── ✦ ", "suffix": " ✦ ── ❖"},
    {"name": "Cinta Gótica", "prefix": "⸼ ۫ ּ ִ ۫ ּ ", "suffix": " ּ ۫ ִ ּ ۫ ⸼"},
    {"name": "Cámara VHS", "prefix": "｢ REC ● ", "suffix": " ｣"},
]

AESTHETIC_DIVIDERS: list[str] = [
    "─── ･ ｡ﾟ☆: *.☽ .* :☆ﾟ. ───",
    "•❅──────✧❅✦❅✧──────❅•",
    "╔═══*.·:·.☽✧    ✦    ✧☾.·:·.*═══╗",
    "╚═══*.·:·.☽✧    ✦    ✧☾.·:·.*═══╝",
    "─── ❖ ── ✦ ──『 ✦ 』── ✦ ── ❖ ───",
    "✿°•∘ɷ∘•°✿ ... ✿°•∘ɷ∘•°✿",
    "━━━✦❘༻༺❘✦━━━",
    "⋅•⋅⊰∙∘☽༓☾∘∙⊱⋅•⋅",
    "█▓▒▒░░░ ✦ ░░░▒▒▓█",
    "╰── ⋅ ⋅ ── ✩ ── ⋅ ⋅ ──╯",
    "✦•┈๑⋅⋯ ⋯⋅๑┈•✦",
    "♫♪.ılılıll|̲̅̅●̲̅̅|̲̅̅=̲̅̅|̲̅̅●̲̅̅|llılılı.♫♪",
]

KAOMOJI_CATEGORIES: list[dict] = [
    {
        "name_es": "✨ Felices, Magia & Estrellas",
        "name_en": "✨ Happy, Magic & Sparkles",
        "items": [
            "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧",
            "(づ｡◕‿‿◕｡)づ",
            "(✿◠‿◠)",
            "(★^O^★)",
            "╰(*´︶`*)╯",
            "(ﾉ´ヮ`)ﾉ*: ･ﾟ",
            "✧◝(⁰▿⁰)◜✧",
            "(๑>ᴗ<๑)",
            "(≧◡≦) ♡",
            "⸜(｡˃ ᵕ ˂ )⸝♡",
        ],
    },
    {
        "name_es": "🔥 Actitud, Acción & Mesas",
        "name_en": "🔥 Attitude, Action & Table Flip",
        "items": [
            "(╯°□°）╯︵ ┻━┻",
            "┬─┬ノ( º _ ºノ)",
            "(▀̿Ĺ̯▀̿ ̿)",
            "(ง'̀-'́)ง",
            "(⌐■_■)",
            "ᕦ(ò_óˇ)ᕤ",
            "(╬ Ò﹏Ó)",
            "¯\\_(ツ)_/¯",
            "(¬‿¬)",
            "( •_•)>⌐■-■",
        ],
    },
    {
        "name_es": "🐾 Criaturas, Gatos & Relax",
        "name_en": "🐾 Cute Creatures & Chill",
        "items": [
            "(=^･ω･^=)",
            "ʕ•́ᴥ•̀ʔっ",
            "૮ ˶ᵔ ᵕ ᵔ˶ ა",
            "(V)(°,,,,°)(V)",
            "₍ᐢ. .ᐢ₎",
            "(-_-) zzz",
            "( ´ ▽ ` )ﾉ",
            "(づ￣ ³￣)づ",
            "(⁄ ⁄•⁄ω⁄•⁄ ⁄)",
            "(⊙_⊙)",
        ],
    },
]


# ─────────────────────────────────────────────────────────────────────────────
#  4. Estudio de Emojis & Combos Estéticos
# ─────────────────────────────────────────────────────────────────────────────

AESTHETIC_EMOJI_COMBOS: list[dict] = [
    {"combo": "✨🌙🦋", "label": "Noche Mística"},
    {"combo": "👑🔥⚡", "label": "Rey Competitivo"},
    {"combo": "🎧💜🌌", "label": "Lo-Fi Midnight"},
    {"combo": "🥀🖤⛓️", "label": "Dark Grunge"},
    {"combo": "🌸🍡🍵", "label": "Sakura Café"},
    {"combo": "🎮👾🕹️", "label": "Arcade Pro"},
    {"combo": "☕📖🍂", "label": "Editorial Otoño"},
    {"combo": "💎❄️⚔️", "label": "Filo Helado"},
    {"combo": "🕯️📜🖋️", "label": "Poeta Clásico"},
    {"combo": "🚀🪐☄️", "label": "Odisea Espacial"},
    {"combo": "🍀🌿🐸", "label": "Bosque Zen"},
    {"combo": "🩸🦇🕸️", "label": "Vampiro Gótico"},
]

EMOJI_CATEGORIES: list[dict] = [
    {
        "id": "faces",
        "name_es": "😀 Rostros & Expresiones",
        "name_en": "😀 Faces & Expressions",
        "emojis": [
            ("😀", "sonrisa feliz"), ("😎", "gafas cool"), ("🤩", "estrellas ojos"),
            ("🥳", "fiesta"), ("😏", "picaro"), ("🥹", "emocionado"),
            ("😭", "llorar"), ("😤", "orgullo"), ("🤯", "mente explosiva"),
            ("🥶", "frio hielo"), ("🥵", "calor"), ("😈", "diablo morado"),
            ("💀", "calavera"), ("👻", "fantasma"), ("👽", "alien"),
            ("🤖", "robot"), ("🎃", "calabaza"), ("🎭", "mascaras teatro"),
            ("🫠", "derritiendose"), ("🫡", "saludo respeto"), ("🤫", "silencio"),
            ("🤔", "pensando"), ("😴", "dormir"), ("😇", "angel"),
        ],
    },
    {
        "id": "aesthetic",
        "name_es": "✨ Brillos, Corazones & Fuego",
        "name_en": "✨ Sparkles, Hearts & Fire",
        "emojis": [
            ("✨", "brillos chispas"), ("🔥", "fuego llama"), ("⚡", "rayo trueno"),
            ("💫", "estrella fugaz"), ("🌟", "estrella brillante"), ("🌙", "luna"),
            ("☀️", "sol"), ("🌈", "arcoiris"), ("☁️", "nube"),
            ("❄️", "copo nieve"), ("💧", "gota agua"), ("🌊", "ola mar"),
            ("❤️", "corazon rojo"), ("🖤", "corazon negro"), ("🤍", "corazon blanco"),
            ("💜", "corazon morado"), ("💙", "corazon azul"), ("💚", "corazon verde"),
            ("💛", "corazon amarillo"), ("🩷", "corazon rosa"), ("❤️‍🔥", "corazon fuego"),
            ("💔", "corazon roto"), ("💯", "cien puntos"), ("💥", "explosion"),
        ],
    },
    {
        "id": "hands",
        "name_es": "🙌 Manos, Gestos & Corona",
        "name_en": "🙌 Hands, Gestures & Royalty",
        "emojis": [
            ("👋", "hola mano"), ("👌", "ok perfecto"), ("✌️", "paz victoria"),
            ("🤞", "dedos cruzados"), ("🫰", "corazon coreano"), ("🤟", "rock"),
            ("🤘", "cuernos metal"), ("🤙", "llamame"), ("👈", "izquierda"),
            ("👉", "derecha"), ("👆", "arriba"), ("👇", "abajo"),
            ("👍", "like bien"), ("👎", "dislike"), ("✊", "puno"),
            ("👊", "golpe puno"), ("👏", "aplausos"), ("🙌", "manos arriba"),
            ("🫶", "manos corazon"), ("🤝", "apreton manos"), ("🙏", "gracias rezar"),
            ("✍️", "escribiendo pluma"), ("💪", "fuerza brazo"), ("👑", "corona rey"),
        ],
    },
    {
        "id": "gaming_objects",
        "name_es": "🎮 Gaming, Arte & Escritura",
        "name_en": "🎮 Gaming, Art & Writing",
        "emojis": [
            ("🎮", "control juego"), ("🕹️", "joystick arcade"), ("👾", "monstruo pixel"),
            ("🎧", "audifonos"), ("🎤", "microfono"), ("🎸", "guitarra"),
            ("🎹", "piano"), ("🎨", "paleta arte"), ("🖋️", "pluma fuente"),
            ("✒️", "punta pluma"), ("📜", "pergamino"), ("📖", "libro abierto"),
            ("⚔️", "espadas cruzadas"), ("🛡️", "escudo"), ("🏹", "arco flecha"),
            ("💣", "bomba"), ("💎", "diamante"), ("🏆", "trofeo copa"),
            ("🥇", "medalla oro"), ("🎯", "diana"), ("🎲", "dado"),
            ("♟️", "peon ajedrez"), ("🔮", "bola cristal"), ("🧿", "amuleto nazar"),
        ],
    },
    {
        "id": "nature",
        "name_es": "🦋 Naturaleza, Flores & Criaturas",
        "name_en": "🦋 Nature, Flowers & Creatures",
        "emojis": [
            ("🦋", "mariposa"), ("🥀", "rosa marchita"), ("🌹", "rosa roja"),
            ("🌸", "flor cerezo sakura"), ("🌺", "hibisco"), ("🌻", "girasol"),
            ("🌼", "margarita"), ("🌷", "tulipan"), ("🍀", "trebol suerte"),
            ("🌿", "hierba hoja"), ("🍂", "hojas otono"), ("🍄", "hongo seta"),
            ("🐉", "dragon"), ("🦅", "aguila"), ("🦉", "buho"),
            ("🦇", "murcielago"), ("🐺", "lobo"), ("🦊", "zorro"),
            ("🐱", "gato"), ("🐶", "perro"), ("🐼", "panda"),
            ("🐍", "serpiente"), ("🕷️", "arana"), ("🦈", "tiburon"),
        ],
    },
    {
        "id": "food_badges",
        "name_es": "☕ Café, Postres & Sellos",
        "name_en": "☕ Coffee, Treats & Badges",
        "emojis": [
            ("☕", "cafe taza"), ("🍵", "te matcha"), ("🧋", "boba bubble tea"),
            ("🍷", "copa vino"), ("🍸", "coctel"), ("🍓", "fresa"),
            ("🍒", "cerezas"), ("🍑", "durazno"), ("🍋", "limon"),
            ("🍕", "pizza"), ("🍔", "hamburguesa"), ("🍣", "sushi"),
            ("🍜", "ramen"), ("🍡", "dango"), ("🍰", "pastel"),
            ("🍩", "dona"), ("🍪", "galleta"), ("🍫", "chocolate"),
            ("✅", "check verde"), ("☑️", "check caja"), ("❌", "cruz roja"),
            ("⚠️", "alerta"), ("🚫", "prohibido"), ("♾️", "infinito"),
        ],
    },
]
