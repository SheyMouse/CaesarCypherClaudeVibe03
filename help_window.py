"""
help_window.py — help popup and help.txt file reader.

Caesar Cipher — Version 3.0
"""
import tkinter as tk
from tkinter import ttk

from constants import (BG, CARD, DIVIDER, TEXT_LT, TEXT_DIM,
                       HDR_TOP, HDR_BOT, ACCENT_LT, BTN_SEC)
from widgets import GlossyButton, _adjust


# ── Help file loader ──────────────────────────────────────────────────────────
def load_help(path="help.txt"):
    """
    Parse help.txt into (intro, sections).
    sections is a list of (title, [(tag, line), ...]) tuples.
    Tags: 'body' for normal lines, 'example' for [EXAMPLE] lines.
    """
    try:
        with open(path, encoding="utf-8") as f:
            raw = f.read()
    except FileNotFoundError:
        return (
            "help.txt not found. Place it in the same folder as this script.",
            []
        )

    blocks   = raw.split("[SECTION]")
    intro    = blocks[0].strip()
    sections = []

    for block in blocks[1:]:
        lines = block.strip().splitlines()
        title = lines[0].strip()
        points = []
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            if line.startswith("[EXAMPLE]"):
                points.append(("example", line[len("[EXAMPLE]"):].strip()))
            else:
                points.append(("body", line))
        sections.append((title, points))

    return intro, sections


# ── Help popup ────────────────────────────────────────────────────────────────
def show_help(parent):
    """
    Open the help popup centred over `parent`.
    `parent` should be the root window (or any Toplevel to centre over).
    """
    popup = tk.Toplevel(parent)
    popup.title("How to Use")
    popup.configure(bg=BG)
    popup.resizable(True, True)
    popup.grab_set()

    pw, ph = 560, 860
    popup.update_idletasks()
    rx = parent.winfo_x() + (parent.winfo_width()  - pw) // 2
    ry = parent.winfo_y() + (parent.winfo_height() - ph) // 2
    popup.geometry(f"{pw}x{ph}+{rx}+{ry}")
    popup.minsize(400, 320)

    # ── Glossy header ─────────────────────────────────────────────────────────
    hc = tk.Canvas(popup, height=58, bg=BG, highlightthickness=0)
    hc.pack(fill="x")

    def _draw_hdr(e=None):
        hc.delete("all")
        cw = hc.winfo_width() or pw
        hc.create_rectangle(0,  0, cw, 29, fill=HDR_TOP, outline="")
        hc.create_rectangle(0, 29, cw, 58, fill=HDR_BOT, outline="")
        hc.create_line(0, 29, cw, 29, fill=_adjust(HDR_TOP, +30), width=1)
        hc.create_text(cw // 2, 29, text="❓  HOW TO USE",
                       fill="white", font=("Segoe UI", 14, "bold"), anchor="center")

    hc.bind("<Configure>", _draw_hdr)
    popup.after(50, _draw_hdr)

    # ── Scrollable text ───────────────────────────────────────────────────────
    tf = tk.Frame(popup, bg=BG)
    tf.pack(fill="both", expand=True, padx=12, pady=8)

    sb = ttk.Scrollbar(tf, orient="vertical")
    sb.pack(side="right", fill="y")

    txt = tk.Text(tf, bg=CARD, fg=TEXT_LT, font=("Segoe UI", 10),
                  wrap="word", relief="flat", bd=0,
                  padx=18, pady=10, cursor="arrow",
                  yscrollcommand=sb.set)
    txt.pack(side="left", fill="both", expand=True)
    sb.config(command=txt.yview)
    popup.bind("<MouseWheel>",
               lambda e: txt.yview_scroll(int(-1*(e.delta/120)), "units"))

    txt.tag_configure("intro",   font=("Segoe UI", 10, "italic"), foreground=TEXT_LT,
                      lmargin1=10, lmargin2=10, spacing1=4, spacing3=10)
    txt.tag_configure("rule",    font=("Segoe UI", 1), foreground=DIVIDER,
                      background=DIVIDER, spacing3=10)
    txt.tag_configure("heading", font=("Segoe UI", 11, "bold"), foreground=ACCENT_LT,
                      spacing1=14, spacing3=4)
    txt.tag_configure("divider", font=("Segoe UI", 1), foreground="#2a2a4a",
                      background="#2a2a4a", spacing3=4)
    txt.tag_configure("body",    font=("Segoe UI", 10), foreground=TEXT_LT,
                      lmargin1=10, lmargin2=10, spacing1=3, spacing3=3)
    txt.tag_configure("example", font=("Segoe UI", 10, "italic"), foreground=TEXT_DIM,
                      lmargin1=10, lmargin2=10, spacing1=2, spacing3=2)

    intro, sections = load_help()
    txt.insert("end", intro + "\n", "intro")
    txt.insert("end", "─" * 55 + "\n", "rule")

    for i, (title, points) in enumerate(sections):
        txt.insert("end", title + "\n", "heading")
        txt.insert("end", "─" * 55 + "\n", "divider")
        for tag, line in points:
            txt.insert("end", line + "\n", tag)
        if i < len(sections) - 1:
            txt.insert("end", "\n")

    txt.config(state="disabled")

    GlossyButton(popup, text="  Close  ", command=popup.destroy,
                 base_color=BTN_SEC, width=110, height=34).pack(pady=10)
