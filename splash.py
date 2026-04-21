"""
splash.py — mode-selection splash screen shown on launch.

Caesar Cipher — Version 3.0
"""
import tkinter as tk

from constants import (BG, CARD, DIVIDER, TEXT_LT, TEXT_DIM,
                       HDR_TOP, HDR_BOT, BTN_ENC, BTN_DEC, BTN_SEC, BTN_EXT)
from widgets import GlossyButton, _adjust
from help_window import show_help


VERSION = "3.0"


def show_entry_dialogue(root):
    """
    Display the mode-selection splash screen.
    Returns 'encrypt', 'decrypt', or 'exit'.
    """
    chosen = tk.StringVar(value="")

    splash = tk.Toplevel(root)
    splash.title("Caesar Cipher")
    splash.configure(bg=BG)
    splash.resizable(False, False)
    splash.grab_set()
    splash.focus_force()

    sw, sh = 480, 680
    splash.update_idletasks()
    sx = (splash.winfo_screenwidth()  - sw) // 2
    sy = (splash.winfo_screenheight() - sh) // 2
    splash.geometry(f"{sw}x{sh}+{sx}+{sy}")

    # Version label — bottom right corner
    def _place_version(e=None):
        lbl.place(x=sw - 6, y=sh - 6, anchor="se")
    lbl = tk.Label(splash, text=f"v{VERSION}",
                   bg=BG, fg=TEXT_DIM, font=("Segoe UI", 8))
    splash.bind("<Configure>", _place_version)
    splash.after(60, _place_version)

    def on_close():
        chosen.set("exit")
        splash.destroy()
    splash.protocol("WM_DELETE_WINDOW", on_close)

    # ── Glossy header ─────────────────────────────────────────────────────────
    hc = tk.Canvas(splash, height=80, bg=BG, highlightthickness=0)
    hc.pack(fill="x")

    def draw_splash_header(e=None):
        hc.delete("all")
        cw = hc.winfo_width() or sw
        hc.create_rectangle(0,  0, cw, 40, fill=HDR_TOP, outline="")
        hc.create_rectangle(0, 40, cw, 80, fill=HDR_BOT, outline="")
        hc.create_line(0, 40, cw, 40, fill=_adjust(HDR_TOP, +30), width=1)
        hc.create_text(cw // 2, 24, text="CAESAR CIPHER",
                       fill="white", font=("Segoe UI", 20, "bold"), anchor="center")
        hc.create_text(cw // 2, 60, text="encrypt  ·  send  ·  decrypt",
                       fill=_adjust(HDR_TOP, +60), font=("Segoe UI", 9, "italic"),
                       anchor="center")

    hc.bind("<Configure>", draw_splash_header)
    splash.after(50, draw_splash_header)

    # ── Prompt ────────────────────────────────────────────────────────────────
    tk.Label(splash, text="Are you encrypting or decrypting a message?",
             bg=BG, fg=TEXT_LT,
             font=("Segoe UI", 13, "bold")).pack(pady=(28, 6))

    tk.Label(splash, text="Choose a mode to get started.",
             bg=BG, fg=TEXT_DIM,
             font=("Segoe UI", 9)).pack(pady=(0, 30))

    # ── Mode cards ────────────────────────────────────────────────────────────
    btn_row = tk.Frame(splash, bg=BG)
    btn_row.pack()

    def pick(mode):
        chosen.set(mode)
        splash.destroy()

    def make_mode_card(parent, icon, title, subtitle, btn_label, base_col, mode):
        """
        A single Canvas acting as a fully clickable card — no child widgets
        so every pixel responds to hover/click events.
        """
        CW, CH = 175, 200
        BRAD   = 10
        BH, BY = 34, 152

        hover   = [False]
        pressed = [False]

        c = tk.Canvas(parent, width=CW, height=CH,
                      highlightthickness=1,
                      highlightbackground=DIVIDER,
                      bg=CARD, cursor="hand2")

        def draw(hov=False, prs=False):
            c.delete("all")
            c.create_rectangle(0, 0, CW, CH, fill=CARD, outline="")
            if hov:
                c.create_rectangle(0, 0, CW, CH,
                                   fill=_adjust(base_col, -30), outline="")
            c.create_text(CW // 2, 44,  text=icon,     font=("Segoe UI", 28),        fill=TEXT_LT, anchor="center")
            c.create_text(CW // 2, 88,  text=title,    font=("Segoe UI", 11, "bold"), fill=TEXT_LT, anchor="center")
            c.create_text(CW // 2, 110, text=subtitle, font=("Segoe UI", 8),          fill=TEXT_DIM, anchor="center")

            bx1, bx2 = 12, CW - 12
            by1, by2 = BY, BY + BH
            r = BRAD

            if prs:
                bt = _adjust(base_col, -25); bb = _adjust(base_col, -40)
            elif hov:
                bt = _adjust(base_col, +45); bb = _adjust(base_col, +25)
            else:
                bt = _adjust(base_col, +30); bb = base_col

            for ax, ay, start in [(bx1, by1, 90), (bx2-2*r, by1, 0),
                                   (bx1, by2-2*r, 180), (bx2-2*r, by2-2*r, 270)]:
                c.create_arc(ax, ay, ax+2*r, ay+2*r,
                             start=start, extent=90, fill=bb, outline="")
            c.create_rectangle(bx1+r, by1, bx2-r, by2, fill=bb, outline="")
            c.create_rectangle(bx1, by1+r, bx2, by2-r, fill=bb, outline="")

            mid = (by1 + by2) // 2
            for ax, ay, start in [(bx1, by1, 90), (bx2-2*r, by1, 0)]:
                c.create_arc(ax, ay, ax+2*r, ay+2*r,
                             start=start, extent=90, fill=bt, outline="")
            c.create_rectangle(bx1+r, by1, bx2-r, mid, fill=bt, outline="")
            c.create_rectangle(bx1, by1+r, bx2, mid,    fill=bt, outline="")
            c.create_line(bx1+r, by1+1, bx2-r, by1+1,
                          fill=_adjust(bt, +40), width=1)
            c.create_text((bx1+bx2)//2, (by1+by2)//2 + (1 if prs else 0),
                          text=btn_label, fill="white",
                          font=("Segoe UI", 10, "bold"), anchor="center")

        def on_enter(_):   hover[0] = True;  draw(hov=True,  prs=pressed[0])
        def on_leave(_):   hover[0] = False; pressed[0] = False; draw()
        def on_press(_):   pressed[0] = True; draw(hov=True, prs=True)
        def on_release(_):
            pressed[0] = False
            draw(hov=hover[0])
            pick(mode)

        c.bind("<Enter>",           on_enter)
        c.bind("<Leave>",           on_leave)
        c.bind("<ButtonPress-1>",   on_press)
        c.bind("<ButtonRelease-1>", on_release)
        c.after_idle(draw)
        return c

    make_mode_card(btn_row,
                   icon="🔒", title="ENCRYPT", subtitle="Write a secret message",
                   btn_label="Start Encrypting", base_col=BTN_ENC,
                   mode="encrypt").pack(side="left", padx=18)

    make_mode_card(btn_row,
                   icon="🔓", title="DECRYPT", subtitle="Read a secret message",
                   btn_label="Start Decrypting", base_col=BTN_DEC,
                   mode="decrypt").pack(side="left", padx=18)

    # ── Footer: help row + note ───────────────────────────────────────────────
    footer = tk.Frame(splash, bg=BG)
    footer.pack(pady=(22, 0))

    tk.Label(footer, text="New to Caesar Cipher?",
             bg=BG, fg=TEXT_DIM, font=("Segoe UI", 9)).pack(side="left", padx=(0, 8))

    def open_splash_help():
        splash.grab_release()
        show_help(splash)
        splash.grab_set()

    GlossyButton(footer, text="?  How it Works", command=open_splash_help,
                 base_color=BTN_SEC, width=130, height=28,
                 font=("Segoe UI", 9, "bold")).pack(side="left")

    tk.Label(splash, text="You can switch modes at any time using the buttons in the app.",
             bg=BG, fg=TEXT_DIM, font=("Segoe UI", 8)).pack(pady=(10, 0))

    GlossyButton(splash, text="⏻  Exit", command=on_close,
                 base_color=BTN_EXT, width=100, height=30,
                 font=("Segoe UI", 9, "bold")).pack(pady=(16, 0))

    root.wait_window(splash)
    return chosen.get()
