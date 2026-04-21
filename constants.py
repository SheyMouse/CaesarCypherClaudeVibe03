"""
constants.py — application-wide colour palette, fonts and limit constants.

Caesar Cipher — Version 3.0
"""
# ── Palette ───────────────────────────────────────────────────────────────────
BG        = "#12121f"   # near-black page
CARD      = "#1c1c30"   # card panels
DIVIDER   = "#2a2a4a"
TEXT_LT   = "#dde0ff"   # light lavender text
TEXT_DIM  = "#7070a0"   # muted text
HDR_TOP   = "#3a4a9a"   # header gloss top
HDR_BOT   = "#1e2a6a"   # header gloss bottom
ACCENT_LT = "#818cf8"   # bright indigo accent

# ── Button base colours ───────────────────────────────────────────────────────
BTN_ENC  = "#1a4fa0"   # blue   — Encrypt
BTN_DEC  = "#5b21b6"   # purple — Decrypt
BTN_SEC  = "#2a3a5a"   # slate  — Copy / Paste / Help
BTN_CLR  = "#7f1d1d"   # dark red — Clear
BTN_EXT  = "#14532d"   # dark green — Exit

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT_LBL  = ("Segoe UI", 9,  "bold")
FONT_TXT  = ("Segoe UI", 11)
FONT_BTN  = ("Segoe UI", 10, "bold")
FONT_BTNL = ("Segoe UI", 11, "bold")

# ── App limits ────────────────────────────────────────────────────────────────
CHAR_LIMIT  = 1000    # maximum characters in either text panel
WARN_AT     = 900     # counter turns red at this many characters
SHIFT_MIN   = -94
SHIFT_MAX   =  94
