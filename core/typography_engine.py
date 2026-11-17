"""
core/typography_engine.py
─────────────────────────
Motor de transformación tipográfica Unicode para MediaHub-FontFamily.
Soporta:
- Más de 30 familias tipográficas Unicode (Góticas, Caligráficas, Serif, Sans,
  Burbujas, Bloques, Versalitas, Vaporwave, Invertido, Glitch, Decoradas).
- Reversión inteligente (normalización de glifos Unicode a ASCII base) para
  poder cambiar de una fuente Unicode a otra sin perder el texto.
- Soporte completo para acentos del español y la letra 'ñ' mediante marcas
  diacríticas combinadas Unicode.
- Modo de escritura en vivo (transformación carácter por carácter) y decoradores.
"""

from __future__ import annotations

ASCII_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ASCII_LOWER = "abcdefghijklmnopqrstuvwxyz"
ASCII_DIGITS = "0123456789"
ASCII_ALL = ASCII_UPPER + ASCII_LOWER + ASCII_DIGITS

# Mapa de caracteres acentuados españoles a (letra_base, marca_combinante_unicode)
ACCENT_DECOMPOSE: dict[str, tuple[str, str]] = {
    "á": ("a", "\u0301"),
    "é": ("e", "\u0301"),
    "í": ("i", "\u0301"),
    "ó": ("o", "\u0301"),
    "ú": ("u", "\u0301"),
    "Á": ("A", "\u0301"),
    "É": ("E", "\u0301"),
    "Í": ("I", "\u0301"),
    "Ó": ("O", "\u0301"),
    "Ú": ("U", "\u0301"),
    "ñ": ("n", "\u0303"),
    "Ñ": ("N", "\u0303"),
    "ü": ("u", "\u0308"),
    "Ü": ("U", "\u0308"),
}

# Marcas combinantes para decoración o limpieza
COMBINING_MARKS = {
    "\u0301",  # Acute accent
    "\u0303",  # Tilde
    "\u0308",  # Diaeresis
    "\u0336",  # Strikethrough
    "\u0332",  # Low line (Underline)
    "\u0333",  # Double low line
    "\u0338",  # Long solidus overlay (Slash)
    "\u0334",  # Tilde overlay
    "\u030a",  # Ring above
    "\u0324",  # Diaeresis below
    "\u035b",  # Zigzag above
}


def _make_table(upper_str: str, lower_str: str, digits_str: str = ASCII_DIGITS) -> dict[str, str]:
    u_list = list(upper_str)
    l_list = list(lower_str)
    d_list = list(digits_str)
    mapping: dict[str, str] = {}
    for i, ch in enumerate(ASCII_UPPER):
        if i < len(u_list):
            mapping[ch] = u_list[i]
    for i, ch in enumerate(ASCII_LOWER):
        if i < len(l_list):
            mapping[ch] = l_list[i]
    for i, ch in enumerate(ASCII_DIGITS):
        if i < len(d_list):
            mapping[ch] = d_list[i]
    return mapping


# ─────────────────────────────────────────────────────────────────────────────
#  Tablas de Mapeo de Glifos Unicode
# ─────────────────────────────────────────────────────────────────────────────

FONT_TABLES: dict[str, dict[str, str]] = {
    "fraktur": _make_table(
        "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ",
        "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷",
        "0123456789",
    ),
    "fraktur_bold": _make_table(
        "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅",
        "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟",
        "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗",
    ),
    "script_bold": _make_table(
        "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩",
        "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃",
        "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗",
    ),
    "script_light": _make_table(
        "𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵",
        "𝒶𝒷𝒸𝒹ℯ𝒻ℊℎ𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏",
        "0123456789",
    ),
    "serif_bold": _make_table(
        "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙",
        "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
        "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗",
    ),
    "serif_italic": _make_table(
        "𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍",
        "𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧",
        "0123456789",
    ),
    "serif_bold_italic": _make_table(
        "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁",
        "𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛",
        "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗",
    ),
    "double_struck": _make_table(
        "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ",
        "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫",
        "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡",
    ),
    "sans_bold": _make_table(
        "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭",
        "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇",
        "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵",
    ),
    "sans_italic": _make_table(
        "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡",
        "𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻",
        "0123456789",
    ),
    "sans_bold_italic": _make_table(
        "𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕",
        "𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯",
        "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵",
    ),
    "monospace": _make_table(
        "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉",
        "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣",
        "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿",
    ),
    "small_caps": _make_table(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ",
        "0123456789",
    ),
    "fullwidth": _make_table(
        "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ",
        "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ",
        "０１２３４５６７８９",
    ),
    "circled": _make_table(
        "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ",
        "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
        "⓪①②③④⑤⑥⑦⑧⑨",
    ),
    "negative_circled": _make_table(
        "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩",
        "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩",
        "⓿➊➋➌➍➎➏➐➑➒",
    ),
    "squared": _make_table(
        "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉",
        "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉",
        "0123456789",
    ),
    "negative_squared": _make_table(
        "🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉",
        "🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉",
        "0123456789",
    ),
    "parenthesized": _make_table(
        "⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵",
        "⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵",
        "⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽",
    ),
    "superscript": _make_table(
        "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻ",
        "ᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖᑫʳˢᵗᵘᵛʷˣʸᶻ",
        "⁰¹²³⁴⁵⁶⁷⁸⁹",
    ),
    "upside_down": _make_table(
        "∀ᙠƆᗡƎℲ⅁HIſʞ˥WNOԀÒᴚS⊥∩ΛMX⅄Z",
        "ɐqɔpǝɟƃɥıɾʞןɯuodbɹsʇnʌʍxʎz",
        "0ƖᄅƐㄣϛ9ㄥ86",
    ),
    "sorcerer": _make_table(
        "卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙",
        "卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙",
        "0123456789",
    ),
    "runic_nordic": _make_table(
        "Ѧ฿₵ĐɆ₣₲ĦƗJ₭ŁΜ₦Ø₱QŘŞŦɄV₩Ӿ¥Ƶ",
        "αв¢∂єfgнιנкℓмησρqяѕтυνωχуz",
        "0123456789",
    ),
}

# Mapa inverso global: cualquier glifo estilizado -> carácter ASCII original
REVERSE_GLYPH_MAP: dict[str, str] = {}
for _font_id, _table in FONT_TABLES.items():
    for _ascii_ch, _uni_ch in _table.items():
        if _uni_ch not in ASCII_ALL and _uni_ch not in REVERSE_GLYPH_MAP:
            REVERSE_GLYPH_MAP[_uni_ch] = _ascii_ch


# ─────────────────────────────────────────────────────────────────────────────
#  Catálogo de Definiciones de Fuentes (30 estilos)
# ─────────────────────────────────────────────────────────────────────────────

FONT_STYLES: list[dict] = [
    {
        "id": "normal",
        "name_es": "Estándar (Sin filtro)",
        "name_en": "Standard (Plain Text)",
        "category": "all",
        "badge": "BASE",
        "type": "normal",
    },
    {
        "id": "fraktur",
        "name_es": "Gótico Clásico (Fraktur)",
        "name_en": "Classic Gothic (Fraktur)",
        "category": "gothic",
        "badge": "GÓTICO",
        "type": "table",
        "table": "fraktur",
    },
    {
        "id": "fraktur_bold",
        "name_es": "Gótico Real Negrita",
        "name_en": "Royal Bold Fraktur",
        "category": "gothic",
        "badge": "MEDIEVAL",
        "type": "table",
        "table": "fraktur_bold",
    },
    {
        "id": "script_bold",
        "name_es": "Caligrafía Imperial",
        "name_en": "Imperial Bold Script",
        "category": "script",
        "badge": "CURSIVA",
        "type": "table",
        "table": "script_bold",
    },
    {
        "id": "script_light",
        "name_es": "Pluma Fina (Script)",
        "name_en": "Fine Feather Script",
        "category": "script",
        "badge": "FINA",
        "type": "table",
        "table": "script_light",
    },
    {
        "id": "serif_bold",
        "name_es": "Editorial Serif Negrita",
        "name_en": "Editorial Bold Serif",
        "category": "serif",
        "badge": "EDITORIAL",
        "type": "table",
        "table": "serif_bold",
    },
    {
        "id": "serif_italic",
        "name_es": "Vogue Itálica",
        "name_en": "Vogue Serif Italic",
        "category": "serif",
        "badge": "REVISTA",
        "type": "table",
        "table": "serif_italic",
    },
    {
        "id": "serif_bold_italic",
        "name_es": "Serif Dramática",
        "name_en": "Bold Italic Serif",
        "category": "serif",
        "badge": " ÉNFASIS",
        "type": "table",
        "table": "serif_bold_italic",
    },
    {
        "id": "double_struck",
        "name_es": "Doble Trazo (Pizarra)",
        "name_en": "Double Struck (Blackboard)",
        "category": "serif",
        "badge": "DOBLE",
        "type": "table",
        "table": "double_struck",
    },
    {
        "id": "sans_bold",
        "name_es": "Moderna Sans Bold",
        "name_en": "Modern Sans Bold",
        "category": "sans",
        "badge": "MODERNA",
        "type": "table",
        "table": "sans_bold",
    },
    {
        "id": "sans_italic",
        "name_es": "Sans Oblicua Limpia",
        "name_en": "Clean Sans Italic",
        "category": "sans",
        "badge": "CLEAN",
        "type": "table",
        "table": "sans_italic",
    },
    {
        "id": "sans_bold_italic",
        "name_es": "Sans Dinámica Turbo",
        "name_en": "Dynamic Bold Italic Sans",
        "category": "sans",
        "badge": "IMPACTO",
        "type": "table",
        "table": "sans_bold_italic",
    },
    {
        "id": "monospace",
        "name_es": "Máquina de Escribir (Mono)",
        "name_en": "Typewriter Monospace",
        "category": "sans",
        "badge": "TYPEWRITER",
        "type": "table",
        "table": "monospace",
    },
    {
        "id": "small_caps",
        "name_es": "Versalitas (Small Caps)",
        "name_en": "Aesthetic Small Caps",
        "category": "sans",
        "badge": "VERSALITA",
        "type": "table",
        "table": "small_caps",
    },
    {
        "id": "fullwidth",
        "name_es": "Vaporwave Espaciado",
        "name_en": "Vaporwave Fullwidth",
        "category": "boxed",
        "badge": "AESTHETIC",
        "type": "table",
        "table": "fullwidth",
    },
    {
        "id": "circled",
        "name_es": "Burbujas Claras",
        "name_en": "Circled Bubbles",
        "category": "boxed",
        "badge": "CÍRCULOS",
        "type": "table",
        "table": "circled",
    },
    {
        "id": "negative_circled",
        "name_es": "Esferas Tinta Negra",
        "name_en": "Dark Ink Spheres",
        "category": "boxed",
        "badge": "ESFERAS",
        "type": "table",
        "table": "negative_circled",
    },
    {
        "id": "squared",
        "name_es": "Teclas Mecánicas",
        "name_en": "Mechanical Keycaps",
        "category": "boxed",
        "badge": "TECLAS",
        "type": "table",
        "table": "squared",
    },
    {
        "id": "negative_squared",
        "name_es": "Bloques Sólidos",
        "name_en": "Solid Blocks",
        "category": "boxed",
        "badge": "BLOQUES",
        "type": "table",
        "table": "negative_squared",
    },
    {
        "id": "parenthesized",
        "name_es": "Cápsulas Paréntesis",
        "name_en": "Parenthesized Capsules",
        "category": "boxed",
        "badge": "CÁPSULAS",
        "type": "table",
        "table": "parenthesized",
    },
    {
        "id": "superscript",
        "name_es": "Superíndice Flotante",
        "name_en": "Tiny Superscript",
        "category": "decorated",
        "badge": "MINI",
        "type": "table",
        "table": "superscript",
    },
    {
        "id": "sorcerer",
        "name_es": "Katakana Gamer (Kanji Style)",
        "name_en": "Katakana Gamer Style",
        "category": "gothic",
        "badge": "GAMER",
        "type": "table",
        "table": "sorcerer",
    },
    {
        "id": "runic_nordic",
        "name_es": "Rúnico Ciberpank",
        "name_en": "Cyber Runic Mix",
        "category": "gothic",
        "badge": "CYBER",
        "type": "table",
        "table": "runic_nordic",
    },
    {
        "id": "upside_down",
        "name_es": "Mundo del Revés (Invertido)",
        "name_en": "Upside Down",
        "category": "decorated",
        "badge": "FLIP",
        "type": "table",
        "table": "upside_down",
    },
    {
        "id": "strikethrough",
        "name_es": "Censurado / Tachado",
        "name_en": "Strikethrough",
        "category": "decorated",
        "badge": "TACHADO",
        "type": "combining",
        "mark": "\u0336",
    },
    {
        "id": "underline",
        "name_es": "Trazo Subrayado",
        "name_en": "Single Underline",
        "category": "decorated",
        "badge": "SUBRAYADO",
        "type": "combining",
        "mark": "\u0332",
    },
    {
        "id": "double_underline",
        "name_es": "Doble Riel Subrayado",
        "name_en": "Double Underline",
        "category": "decorated",
        "badge": "DOBLE LÍNEA",
        "type": "combining",
        "mark": "\u0333",
    },
    {
        "id": "slash",
        "name_es": "Corte Diagonal",
        "name_en": "Slashed Overlay",
        "category": "decorated",
        "badge": "SLASH",
        "type": "combining",
        "mark": "\u0338",
    },
    {
        "id": "zalgo_soft",
        "name_es": "Distorsión Etérea (Glitch)",
        "name_en": "Ethereal Glitch (Soft Zalgo)",
        "category": "decorated",
        "badge": "GLITCH",
        "type": "zalgo",
    },
    {
        "id": "gothic_royal",
        "name_es": "Blasón Gótico (Con Marco)",
        "name_en": "Royal Gothic Crest",
        "category": "gothic",
        "badge": "BLASÓN",
        "type": "framed",
        "table": "fraktur_bold",
        "prefix": "꧁༺ ",
        "suffix": " ༻꧂",
    },
    {
        "id": "sparkle_script",
        "name_es": "Caligrafía Estelar",
        "name_en": "Starlight Script",
        "category": "script",
        "badge": "ESTELAR",
        "type": "framed",
        "table": "script_bold",
        "prefix": "✧･ﾟ: * ",
        "suffix": " *:･ﾟ✧",
    },
]

FONT_STYLES_BY_ID: dict[str, dict] = {f["id"]: f for f in FONT_STYLES}


class TypographyEngine:
    """Motor estático de conversión y manipulación de fuentes Unicode."""

    @staticmethod
    def normalize_to_plain(text: str) -> str:
        """
        Convierte cualquier texto previamente estilizado con fuentes Unicode
        de vuelta a caracteres legibles estándar (conservando acentos, emojis y símbolos).
        """
        out: list[str] = []
        i = 0
        n = len(text)
        while i < n:
            ch = text[i]
            base = REVERSE_GLYPH_MAP.get(ch, ch)
            # Revisar si el siguiente carácter es tilde o acento combinante
            if i + 1 < n and text[i + 1] in ("\u0301", "\u0303", "\u0308"):
                mark = text[i + 1]
                recomposed = None
                for acc_ch, (b_ch, m_ch) in ACCENT_DECOMPOSE.items():
                    if b_ch == base and m_ch == mark:
                        recomposed = acc_ch
                        break
                if recomposed:
                    out.append(recomposed)
                    i += 2
                    continue
            # Ignorar marcas de tachado/subrayado decorativas al limpiar
            if ch in ("\u0336", "\u0332", "\u0333", "\u0338", "\u0334", "\u030a", "\u0324", "\u035b"):
                i += 1
                continue
            out.append(base)
            i += 1
        return "".join(out)

    @staticmethod
    def transform_char(ch: str, style_id: str) -> str:
        """
        Transforma un único carácter al estilo `style_id`.
        Ideal para el modo de escritura en tiempo real en el lienzo.
        """
        if not ch or style_id == "normal":
            return ch

        style = FONT_STYLES_BY_ID.get(style_id)
        if not style:
            return ch

        stype = style.get("type", "table")

        # Si el carácter viene acentuado (ej. á, ñ), descomponer base + diacrítico
        if ch in ACCENT_DECOMPOSE:
            base_ch, accent_mark = ACCENT_DECOMPOSE[ch]
            styled_base = TypographyEngine._map_single_ascii(base_ch, style)
            return styled_base + accent_mark

        # Si ya era un glifo de otra fuente Unicode, normalizar primero
        plain_ch = REVERSE_GLYPH_MAP.get(ch, ch)

        if stype in ("table", "framed"):
            return TypographyEngine._map_single_ascii(plain_ch, style)
        elif stype == "combining":
            mark = style.get("mark", "\u0336")
            if plain_ch.strip():
                return plain_ch + mark
            return plain_ch
        elif stype == "zalgo":
            if plain_ch.strip():
                return plain_ch + "\u0334\u030a"
            return plain_ch
        return ch

    @staticmethod
    def _map_single_ascii(ch: str, style: dict) -> str:
        table_name = style.get("table", "")
        table = FONT_TABLES.get(table_name, {})
        return table.get(ch, ch)

    @staticmethod
    def transform_text(text: str, style_id: str) -> str:
        """
        Transforma una cadena completa al estilo `style_id`.
        Si el texto ya tenía otra fuente Unicode, lo normaliza primero.
        """
        if not text:
            return ""
        if style_id == "normal":
            return TypographyEngine.normalize_to_plain(text)

        style = FONT_STYLES_BY_ID.get(style_id)
        if not style:
            return text

        plain = TypographyEngine.normalize_to_plain(text)
        stype = style.get("type", "table")

        if stype == "upside_down" or style_id == "upside_down":
            # El modo invertido invierte también el orden de los caracteres por línea
            lines = plain.split("\n")
            flipped_lines = []
            for line in lines:
                chars = [TypographyEngine.transform_char(c, "upside_down") for c in reversed(line)]
                flipped_lines.append("".join(chars))
            return "\n".join(flipped_lines)

        transformed = "".join(TypographyEngine.transform_char(c, style_id) for c in plain)

        if stype == "framed":
            prefix = style.get("prefix", "")
            suffix = style.get("suffix", "")
            return f"{prefix}{transformed}{suffix}"

        return transformed

    @staticmethod
    def apply_combining_mark(text: str, mark: str) -> str:
        """Aplica una marca combinante (tachado, subrayado, slash) sobre cualquier texto sin perder su fuente actual."""
        out = []
        for ch in text:
            if ch in ("\n", "\r", " ", "\t") or ch in COMBINING_MARKS:
                out.append(ch)
            else:
                out.append(ch + mark)
        return "".join(out)
