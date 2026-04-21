"""
main_window.py — builds and manages the main application window and all user interactions.

Caesar Cipher — Version 3.0
"""
import tkinter as tk
from tkinter import ttk, messagebox

from constants import (BG, CARD, DIVIDER, TEXT_LT, TEXT_DIM,
                       HDR_TOP, HDR_BOT, ACCENT_LT,
                       BTN_ENC, BTN_DEC, BTN_SEC, BTN_CLR, BTN_EXT,
                       FONT_TXT, FONT_BTN, FONT_BTNL,
                       CHAR_LIMIT, WARN_AT, SHIFT_MIN, SHIFT_MAX)
from cipher import caesar_cipher
from widgets import GlossyButton, _adjust, show_toast
from help_window import show_help


class MainWindow:
    """Encapsulates the entire main application window."""

    def __init__(self, root, start_mode):
        self.root       = root
        self.start_mode = start_mode

        # Undo buffer — stores previous plain text state
        self._undo_stack = []

        self._build_styles()
        self._build_header()
        self._build_toolbar()
        self._build_body()
        self._build_footer()

        root.after(100, self._focus_for_mode)

    # ══════════════════════════════════════════════════════════════════════════
    #  STYLES
    # ══════════════════════════════════════════════════════════════════════════
    def _build_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.TSpinbox",
                        fieldbackground=CARD, background=CARD,
                        foreground="#ffffff", insertcolor=TEXT_LT,
                        relief="flat", font=("Segoe UI", 17, "bold"),
                        arrowcolor="#ffffff", arrowsize=20,
                        borderwidth=0, padding=4)
        style.map("Dark.TSpinbox", fieldbackground=[("readonly", CARD)])

    # ══════════════════════════════════════════════════════════════════════════
    #  HEADER
    # ══════════════════════════════════════════════════════════════════════════
    def _build_header(self):
        self._hdr = tk.Canvas(self.root, height=68, bg=BG, highlightthickness=0)
        self._hdr.pack(fill="x")
        self._hdr.bind("<Configure>", self._draw_header)
        self.root.after(50, self._draw_header)

    def _draw_header(self, e=None):
        c = self._hdr
        c.delete("all")
        cw = c.winfo_width() or 720
        c.create_rectangle(0,  0, cw, 34, fill=HDR_TOP, outline="")
        c.create_rectangle(0, 34, cw, 68, fill=HDR_BOT, outline="")
        c.create_line(0, 34, cw, 34, fill=_adjust(HDR_TOP, +30), width=1)
        c.create_text(cw//2, 22, text="CAESAR CIPHER",
                      fill="white", font=("Segoe UI", 20, "bold"), anchor="center")
        c.create_text(cw//2, 52, text="encrypt  ·  send  ·  decrypt",
                      fill=_adjust(HDR_TOP, +60), font=("Segoe UI", 9, "italic"),
                      anchor="center")

    # ══════════════════════════════════════════════════════════════════════════
    #  TOOLBAR
    # ══════════════════════════════════════════════════════════════════════════
    def _build_toolbar(self):
        bar = tk.Frame(self.root, bg=DIVIDER, pady=10)
        bar.pack(fill="x")
        bar.columnconfigure(0, weight=1)
        bar.columnconfigure(1, weight=0)
        bar.columnconfigure(2, weight=1)

        # Left spacer
        tk.Frame(bar, bg=DIVIDER).grid(row=0, column=0, sticky="ew")

        # Centre: shift key block
        centre = tk.Frame(bar, bg=DIVIDER)
        centre.grid(row=0, column=1)

        tk.Label(centre, text="SHIFT KEY:", bg=DIVIDER, fg="#ffffff",
                 font=("Segoe UI", 14, "bold")).pack()

        self.shift_var = tk.StringVar(value="0")
        # Validate: only allow integers within range while typing
        vcmd = (self.root.register(self._validate_shift), "%P")
        self._spinbox = ttk.Spinbox(centre, from_=SHIFT_MIN, to=SHIFT_MAX,
                                    textvariable=self.shift_var,
                                    width=5, style="Dark.TSpinbox", wrap=True,
                                    font=("Segoe UI", 17, "bold"),
                                    validate="key", validatecommand=vcmd)
        self._spinbox.pack(ipady=6)

        tk.Label(centre, text="\u2190 Share this number with your recipient \u2192",
                 bg=DIVIDER, fg=TEXT_LT, font=("Segoe UI", 10, "bold")).pack(pady=(2, 0))

        # Right: action buttons
        btn_frame = tk.Frame(bar, bg=DIVIDER)
        btn_frame.grid(row=0, column=2, sticky="e", padx=(0, 14))

        GlossyButton(btn_frame, text="?  Help",
                     command=lambda: show_help(self.root),
                     base_color=BTN_SEC, width=88, height=30, font=FONT_BTN
                     ).pack(side="left", padx=4)

        GlossyButton(btn_frame, text="\u2715  Clear",
                     command=self._clear_all,
                     base_color=BTN_CLR, width=88, height=30, font=FONT_BTN
                     ).pack(side="left", padx=4)

        GlossyButton(btn_frame, text="\u23fb  Exit",
                     command=self.root.destroy,
                     base_color=BTN_EXT, width=88, height=30, font=FONT_BTN
                     ).pack(side="left", padx=(4, 0))

    def _validate_shift(self, value):
        """Allow blank, minus sign alone, or any integer while typing."""
        if value in ("", "-"):
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False

    # ══════════════════════════════════════════════════════════════════════════
    #  BODY
    # ══════════════════════════════════════════════════════════════════════════
    def _build_body(self):
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=14, pady=12)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(2, weight=1)
        body.rowconfigure(0, weight=1)

        self._build_left(body)
        tk.Frame(body, bg=DIVIDER, width=2).grid(row=0, column=1, sticky="ns", padx=8)
        self._build_right(body)

    def _card(self, parent):
        return tk.Frame(parent, bg=CARD,
                        highlightbackground=DIVIDER, highlightthickness=1)

    # ── Left panel ────────────────────────────────────────────────────────────
    def _build_left(self, body):
        lw = tk.Frame(body, bg=BG)
        lw.grid(row=0, column=0, sticky="nsew")
        lw.rowconfigure(1, weight=1)
        lw.columnconfigure(0, weight=1)

        tk.Label(lw, text="\U0001f524  PLAIN TEXT", bg=BG, fg=TEXT_LT,
                 font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="ew", pady=(0, 4))

        lc = self._card(lw)
        lc.grid(row=1, column=0, sticky="nsew")
        lc.rowconfigure(0, weight=1)
        lc.columnconfigure(0, weight=1)

        self.input_text = tk.Text(lc, font=FONT_TXT, bg=CARD, fg=TEXT_LT,
                                  insertbackground=ACCENT_LT, relief="flat", bd=0,
                                  wrap="word", padx=10, pady=8)
        self.input_text.grid(row=0, column=0, sticky="nsew")
        self.input_text.bind("<KeyRelease>", self._on_plain_key)

        self.plain_counter = tk.Label(lw, text=f"0 / {CHAR_LIMIT}",
                                      bg=BG, fg=TEXT_DIM,
                                      font=("Segoe UI", 8), anchor="e")
        self.plain_counter.grid(row=2, column=0, sticky="ew", pady=(4, 0))

        lbr = tk.Frame(lw, bg=BG)
        lbr.grid(row=3, column=0, sticky="ew", pady=(6, 0))
        lbr.columnconfigure(0, weight=1)

        GlossyButton(lbr, text="\U0001f512  ENCRYPT \u2192",
                     command=self._do_encrypt,
                     base_color=BTN_ENC, width=175, height=40, font=FONT_BTNL
                     ).grid(row=0, column=0, sticky="ew", padx=(0, 6))

        GlossyButton(lbr, text="\U0001f4cb  Copy",
                     command=self._copy_encrypted,
                     base_color=BTN_SEC, width=100, height=40, font=FONT_BTN
                     ).grid(row=0, column=1)

        # Undo button — restores last plain text state
        GlossyButton(lbr, text="\u21a9  Undo",
                     command=self._undo,
                     base_color=BTN_SEC, width=80, height=40, font=FONT_BTN
                     ).grid(row=0, column=2, padx=(6, 0))

    # ── Right panel ───────────────────────────────────────────────────────────
    def _build_right(self, body):
        rw = tk.Frame(body, bg=BG)
        rw.grid(row=0, column=2, sticky="nsew")
        rw.rowconfigure(1, weight=1)
        rw.columnconfigure(0, weight=1)

        tk.Label(rw, text="\U0001f510  CYPHER TEXT", bg=BG, fg=TEXT_LT,
                 font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="ew", pady=(0, 4))

        rc = self._card(rw)
        rc.grid(row=1, column=0, sticky="nsew")
        rc.rowconfigure(0, weight=1)
        rc.columnconfigure(0, weight=1)

        self.output_text = tk.Text(rc, font=FONT_TXT, bg=CARD, fg=ACCENT_LT,
                                   relief="flat", bd=0, wrap="word", padx=10, pady=8,
                                   state="disabled", insertwidth=2)
        self.output_text.grid(row=0, column=0, sticky="nsew")

        self.cypher_counter = tk.Label(rw, text=f"0 / {CHAR_LIMIT}",
                                       bg=BG, fg=TEXT_DIM,
                                       font=("Segoe UI", 8), anchor="e")
        self.cypher_counter.grid(row=2, column=0, sticky="ew", pady=(4, 0))

        rbr = tk.Frame(rw, bg=BG)
        rbr.grid(row=3, column=0, sticky="ew", pady=(6, 0))
        rbr.columnconfigure(1, weight=1)

        GlossyButton(rbr, text="\U0001f4c4  Paste",
                     command=self._paste_message,
                     base_color=BTN_SEC, width=100, height=40, font=FONT_BTN
                     ).grid(row=0, column=0, padx=(0, 6))

        GlossyButton(rbr, text="\u2190 DECRYPT \U0001f513",
                     command=self._do_decrypt,
                     base_color=BTN_DEC, width=175, height=40, font=FONT_BTNL
                     ).grid(row=0, column=1, sticky="ew")

    # ══════════════════════════════════════════════════════════════════════════
    #  FOOTER
    # ══════════════════════════════════════════════════════════════════════════
    def _build_footer(self):
        tk.Label(self.root,
                 text="Letters, symbols, digits & spaces are all shifted by the key.",
                 bg=BG, fg=TEXT_LT, font=("Segoe UI", 10)).pack(pady=(2, 8))

    # ══════════════════════════════════════════════════════════════════════════
    #  VALIDATION HELPERS
    # ══════════════════════════════════════════════════════════════════════════
    def _get_shift(self, action="encrypt"):
        """Return the validated shift integer, or None on failure."""
        try:
            shift = int(self.shift_var.get())
        except ValueError:
            messagebox.showerror("Invalid Key", "Shift key must be a whole number.")
            return None
        if shift == 0:
            verb = "encrypting" if action == "encrypt" else "decrypting"
            messagebox.showwarning(
                "No Shift Value Set",
                f"Please set a Caesar Shift value before {verb}.\n\n"
                f"Choose any value between {SHIFT_MIN} and -1, or 1 and {SHIFT_MAX}\n"
                f"using the up/down arrows next to the Shift Key."
            )
            return None
        if not (SHIFT_MIN <= shift <= SHIFT_MAX):
            messagebox.showerror(
                "Shift Key Out of Range",
                f"The Shift Key must be between {SHIFT_MIN} and {SHIFT_MAX}.\n"
                f"You entered: {shift}"
            )
            return None
        return shift

    def _counter_colour(self, count):
        return "#ff6b6b" if count >= WARN_AT else TEXT_DIM

    def _update_plain_counter(self, count):
        self.plain_counter.config(text=f"{count} / {CHAR_LIMIT}",
                                  fg=self._counter_colour(count))

    def _update_cypher_counter(self, count):
        self.cypher_counter.config(text=f"{count} / {CHAR_LIMIT}",
                                   fg=self._counter_colour(count))

    # ══════════════════════════════════════════════════════════════════════════
    #  KEYSTROKE HANDLER
    # ══════════════════════════════════════════════════════════════════════════
    def _on_plain_key(self, event=None):
        content = self.input_text.get("1.0", "end-1c")
        count = len(content)
        if count > CHAR_LIMIT:
            self.input_text.delete(f"1.0+{CHAR_LIMIT}c", tk.END)
            count = CHAR_LIMIT
        self._update_plain_counter(count)

    # ══════════════════════════════════════════════════════════════════════════
    #  ACTIONS
    # ══════════════════════════════════════════════════════════════════════════
    def _do_encrypt(self):
        message = self.input_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("No Message", "Please enter a message to encrypt.")
            return
        shift = self._get_shift(action="encrypt")
        if shift is None:
            return
        result = caesar_cipher(message, shift, encrypt=True)
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", result)
        self.output_text.config(state="disabled")
        self._update_cypher_counter(len(result))

    def _do_decrypt(self):
        message = self.output_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("No Message",
                                   "Please enter or encrypt some cypher text first.")
            return
        shift = self._get_shift(action="decrypt")
        if shift is None:
            return
        # Confirm if plain text already has content
        existing = self.input_text.get("1.0", tk.END).strip()
        if existing:
            if not messagebox.askyesno(
                "Overwrite Plain Text?",
                "The Plain Text box already has content.\n"
                "Decrypting will replace it. Continue?"
            ):
                return
        # Save undo state before overwriting
        self._push_undo(existing)
        result = caesar_cipher(message, shift, encrypt=False)
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", result)
        self._update_plain_counter(len(result))

    def _copy_encrypted(self):
        content = self.output_text.get("1.0", tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            show_toast(self.root, "\u2713  Copied to clipboard!")
        else:
            messagebox.showinfo("Nothing to Copy", "Encrypt a message first.")

    def _paste_message(self):
        try:
            text = self.root.clipboard_get()
        except tk.TclError:
            messagebox.showinfo("Nothing to Paste", "The clipboard is empty.")
            return
        existing = self.output_text.get("1.0", tk.END).strip()
        if existing:
            if not messagebox.askyesno(
                "Overwrite Cypher Text?",
                "The Cypher Text box already has content.\n"
                "Pasting will replace it. Continue?"
            ):
                return
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", text)
        self._update_cypher_counter(len(text.strip()))

    def _clear_all(self):
        # Save undo state before clearing
        existing = self.input_text.get("1.0", tk.END).strip()
        if existing:
            self._push_undo(existing)
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.shift_var.set("0")
        self._update_plain_counter(0)
        self._update_cypher_counter(0)

    # ══════════════════════════════════════════════════════════════════════════
    #  UNDO
    # ══════════════════════════════════════════════════════════════════════════
    def _push_undo(self, text):
        """Save text to the undo stack (max 10 levels)."""
        if text:
            self._undo_stack.append(text)
            if len(self._undo_stack) > 10:
                self._undo_stack.pop(0)

    def _undo(self):
        if not self._undo_stack:
            messagebox.showinfo("Nothing to Undo", "No previous plain text to restore.")
            return
        previous = self._undo_stack.pop()
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", previous)
        self._update_plain_counter(len(previous))

    # ══════════════════════════════════════════════════════════════════════════
    #  FOCUS
    # ══════════════════════════════════════════════════════════════════════════
    def _focus_for_mode(self):
        if self.start_mode == "encrypt":
            self.input_text.focus_set()
        else:
            self.output_text.config(state="normal")
            self.output_text.update_idletasks()
            self.output_text.focus_set()
            self.output_text.mark_set("insert", "1.0")
