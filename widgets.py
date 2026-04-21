"""
widgets.py — reusable UI components: GlossyButton, _adjust, show_toast.

Caesar Cipher — Version 3.0
"""
import tkinter as tk


def _adjust(hex_color, amount):
    """Lighten (positive) or darken (negative) a hex colour string."""
    h = hex_color.lstrip("#")
    r, g, b = [int(h[i:i+2], 16) for i in (0, 2, 4)]
    r = max(0, min(255, r + amount))
    g = max(0, min(255, g + amount))
    b = max(0, min(255, b + amount))
    return f"#{r:02x}{g:02x}{b:02x}"


class GlossyButton(tk.Frame):
    """
    A rounded glossy button drawn entirely on an internal Canvas.
    Inherits from Frame so construction is always safe on Windows;
    the Canvas is drawn after_idle to guarantee Tk has registered it.
    """
    def __init__(self, parent, text, command=None,
                 base_color="#2a5298", text_color="#ffffff",
                 width=140, height=36, radius=10,
                 font=("Segoe UI", 10, "bold"), **kwargs):
        bg = parent["bg"]
        super().__init__(parent, bg=bg, width=width, height=height,
                         cursor="hand2", **kwargs)
        self.pack_propagate(False)

        self._text    = text
        self._command = command
        self._base    = base_color
        self._fg      = text_color
        self._btn_w   = width
        self._btn_h   = height
        self._r       = radius
        self._font    = font
        self._hover   = False
        self._pressed = False

        self._canvas = tk.Canvas(self, width=width, height=height,
                                 highlightthickness=0, bd=0,
                                 bg=bg, cursor="hand2")
        self._canvas.pack()

        for widget in (self, self._canvas):
            widget.bind("<Enter>",           self._on_enter)
            widget.bind("<Leave>",           self._on_leave)
            widget.bind("<ButtonPress-1>",   self._on_press)
            widget.bind("<ButtonRelease-1>", self._on_release)

        self._canvas.after_idle(self._redraw)

    # ── Drawing ───────────────────────────────────────────────────────────────
    def _redraw(self):
        c = self._canvas
        c.delete("all")
        w, h, r = self._btn_w, self._btn_h, self._r

        if self._pressed:
            top_col = _adjust(self._base, -25)
            bot_col = _adjust(self._base, -40)
        elif self._hover:
            top_col = _adjust(self._base, +45)
            bot_col = _adjust(self._base, +25)
        else:
            top_col = _adjust(self._base, +30)
            bot_col = self._base

        self._rrect(0, 0, w, h, r, bot_col)
        self._rrect(0, 0, w, h // 2, r, top_col, flat_bottom=True)
        c.create_line(r, 1, w - r, 1, fill=_adjust(top_col, +40), width=1)
        c.create_text(w // 2, h // 2 + (1 if self._pressed else 0),
                      text=self._text, fill=self._fg,
                      font=self._font, anchor="center")

    def _rrect(self, x1, y1, x2, y2, r, color, flat_bottom=False):
        c = self._canvas
        if flat_bottom:
            c.create_rectangle(x1 + r, y1, x2 - r, y2, fill=color, outline="")
            c.create_rectangle(x1, y1 + r, x2, y2,     fill=color, outline="")
            c.create_arc(x1,     y1, x1+2*r, y1+2*r, start=90, extent=90, fill=color, outline="")
            c.create_arc(x2-2*r, y1, x2,     y1+2*r, start=0,  extent=90, fill=color, outline="")
        else:
            c.create_rectangle(x1 + r, y1, x2 - r, y2, fill=color, outline="")
            c.create_rectangle(x1, y1 + r, x2, y2 - r, fill=color, outline="")
            for ax, ay, start in [(x1, y1, 90), (x2-2*r, y1, 0),
                                   (x1, y2-2*r, 180), (x2-2*r, y2-2*r, 270)]:
                c.create_arc(ax, ay, ax+2*r, ay+2*r,
                             start=start, extent=90, fill=color, outline="")

    # ── Events ────────────────────────────────────────────────────────────────
    def _on_enter(self, _):  self._hover = True;  self._redraw()
    def _on_leave(self, _):  self._hover = False; self._pressed = False; self._redraw()
    def _on_press(self, _):  self._pressed = True; self._redraw()
    def _on_release(self, _):
        self._pressed = False
        self._redraw()
        if self._command:
            self._command()

    def set_text(self, text):
        self._text = text
        self._redraw()


def show_toast(root, message="✓ Copied to clipboard!"):
    """
    Display a borderless toast notification that fades in near the
    bottom-right of `root`, holds, then fades out automatically.
    """
    toast = tk.Toplevel(root)
    toast.overrideredirect(True)
    toast.attributes("-topmost", True)
    toast.attributes("-alpha", 0.0)
    toast.configure(bg="#2a3a5a")

    tk.Label(toast, text=message,
             bg="#2a3a5a", fg="#dde0ff",
             font=("Segoe UI", 10, "bold"),
             padx=18, pady=10).pack()

    def position():
        toast.update_idletasks()
        tw = toast.winfo_width()
        th = toast.winfo_height()
        rx = root.winfo_x() + root.winfo_width()  - tw - 20
        ry = root.winfo_y() + root.winfo_height() - th - 50
        toast.geometry(f"+{rx}+{ry}")

    position()

    def fade_in(alpha=0.0):
        alpha = round(alpha + 0.1, 1)
        toast.attributes("-alpha", alpha)
        if alpha < 1.0:
            toast.after(20, lambda: fade_in(alpha))
        else:
            toast.after(1500, fade_out)

    def fade_out(alpha=1.0):
        alpha = round(alpha - 0.1, 1)
        if alpha <= 0:
            toast.destroy()
        else:
            toast.attributes("-alpha", alpha)
            toast.after(40, lambda: fade_out(alpha))

    toast.after(10, fade_in)
