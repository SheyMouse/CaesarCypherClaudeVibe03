# 🔐 Caesar Cipher

A desktop encryption tool built with Python and tkinter, implementing the classic Caesar Cipher — extended beyond the standard alphabet to cover the full range of printable ASCII characters including symbols, digits, punctuation and spaces.

---

## A Brief History

The Caesar Cipher is one of the oldest and simplest encryption techniques known to exist. It takes its name from Julius Caesar, who used it in his private correspondence around 58 BC to protect military communications from enemies who might intercept his messages. The Roman historian Suetonius documented its use, noting that Caesar would shift each letter of the alphabet by three positions — so **A** became **D**, **B** became **E**, and so on.

Despite its simplicity, the cipher was reportedly effective at the time, as many of Caesar's enemies were illiterate and those who weren't had no familiarity with cryptography. The technique was later adapted by Augustus Caesar, who used a shift of one, and it continued to see use in various forms throughout the medieval period.

Today the Caesar Cipher is considered trivially breakable — there are only 25 possible shifts to try — but it remains one of the most important ciphers in history. It laid the groundwork for more sophisticated substitution ciphers, and it is still widely used as an introduction to the principles of cryptography and information security.

This app extends the classical Caesar Cipher beyond letters to encompass the full printable ASCII character set, making it significantly harder to crack by eye.

---

## Features

- Encrypts and decrypts **letters, symbols, digits, punctuation and spaces**
- Extended shift range of **-94 to 94** covering the full printable ASCII pool
- **1,000 character limit** with a live character counter that warns as you approach the limit
- **Mode-selection splash screen** on launch — choose Encrypt or Decrypt before you begin
- **Web 2.0 dark-mode UI** with glossy custom buttons and smooth hover effects
- **Toast notification** on copy — a subtle fade-in/fade-out confirmation
- **Editable help file** (`help.txt`) — update the help content without touching any Python
- Fully **modular codebase** — clean separation of concerns across six focused modules

---

## Requirements

- Python **3.8** or later
- No third-party packages — uses the Python standard library only (`tkinter`, `ttk`)

---

## How to Run

1. Place all project files in the same folder
2. Open a terminal in that folder and run:

```bash
python caesar_cipher.py
```

3. Choose **Encrypt** or **Decrypt** from the splash screen
4. Set a Shift Key value (any non-zero number from -94 to 94)
5. Type or paste your message and click the action button

---

## How the Cipher Works

Each character in your message is shifted along its character pool by the Shift Key value:

| Character type | Shift pool | Example (Shift Key: 3) |
|---|---|---|
| Uppercase letters | A – Z (26 chars) | `A` → `D`   `Z` → `C` |
| Lowercase letters | a – z (26 chars) | `a` → `d`   `z` → `c` |
| Symbols, digits, spaces | Full printable ASCII (95 chars) | `!` → `$`   `?` → `B` |

The shift wraps around within its pool, so no character is ever lost. To decrypt, the recipient uses the same Shift Key in reverse.

> ⚠️ Both sender and recipient **must** use the same Shift Key to communicate successfully.

---

## Project Structure

```
caesar_cipher/
│
├── caesar_cipher.py   ← Entry point — run this to launch the app
├── splash.py          ← Mode-selection splash screen
├── help_window.py     ← Help popup and help.txt file reader
├── widgets.py         ← GlossyButton widget and colour utilities
├── cipher.py          ← Core encryption and decryption logic
├── constants.py       ← Colour palette and font definitions
│
├── help.txt           ← Help content (plain text, edit freely)
├── requirements.txt   ← Dependency declaration (stdlib only)
└── README.md          ← This file
```

### Module Dependencies

```
caesar_cipher.py  →  constants, cipher, widgets, help_window, splash
splash.py         →  constants, widgets, help_window
help_window.py    →  constants, widgets
widgets.py        →  tkinter only
cipher.py         →  pure Python, no imports
constants.py      →  pure Python, no imports
```

---

## Editing the Help Content

Open `help.txt` in any text editor. The format is straightforward:

- The **opening block** (before any `[SECTION]` tag) is the intro paragraph
- `[SECTION] Your Title` starts a new section with a styled heading
- `[EXAMPLE] Some text` renders in a dimmed italic style — use for cipher examples
- Any other line renders as normal body text

Changes take effect immediately the next time the Help window is opened — no restart required.

---

## Shift Key Guidelines

- The Shift Key accepts any value from **-94 to +94**.
- A shift of **0** is not permitted as it would leave the message unchanged.
- Any value outside this range is rejected with an error.

---

## Limitations

- The Caesar Cipher is **not secure** by modern cryptographic standards. It should not be used to protect sensitive information.
- The 1,000 character limit is intentional — this tool is designed for short messages.
- The Shift Key is essentially a shared password. Anyone who knows it can decrypt the message in seconds.

---

## License

This project is released for educational and personal use.
