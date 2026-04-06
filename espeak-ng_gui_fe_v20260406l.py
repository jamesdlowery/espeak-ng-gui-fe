#!/usr/bin/env python3
"""
espeak-ng GUI Front-End
Version: v20260406l
A clean Tkinter interface for the espeak-ng text-to-speech engine.
Requires: espeak-ng installed and on PATH

Changelog:
  v20260406l - Fixed voice names again: diagnostic confirmed that parts[3]
               in --voices output IS the full VoiceName (e.g. "Afrikaans",
               "English_(America)"). Dropped the file-reading approach
               entirely; now uses parts[3] directly. Also fixed parts[4]
               (the file path) as the voice code passed to -v.
  v20260406k - Attempted to restore full voice names by reading voice files
               on disk; failed because voices/lang path does not exist on
               Debian.
  v20260406j - Added Cylon Centurion (BSG 1978) preset.
  v20260406i - Added PRESET dropdown with named robotic/sci-fi voice
               approximations. Selecting a preset loads its speed/pitch/
               amplitude/word-gap values into the sliders automatically.
  v20260406h - Fixed VOICE field appearing blank on startup (white text on
               white background): force foreground/background colors for all
               ttk Combobox states including the initial 'readonly' state.
  v20260406g - Fixed blank VOICE menu: corrected column parsing for
               espeak-ng --voices output; guaranteed en-us default entry
               is always present and pre-selected on startup.
  v20260406f - Default voice on startup is now explicitly English_(America)
               (en-us), matched robustly against the voice code regardless
               of label format.
  v20260406e - Fixed silent playback: pass text as a CLI argument instead of
               via stdin, which espeak-ng handles more reliably. Also surface
               stderr errors in a dialog so failures are visible.
  v20260406d - Fixed crash caused by _style_ttk being merged into
               _fix_combo_width in v20260406c.
  v20260406c - Moved voice selector above the left/right panel split so it
               spans the full window width; dropdown popup sized to the
               longest voice name so all entries are fully readable.
  v20260406b - Widened right settings panel so slider labels are readable.
  v20260406a - Initial release.
"""

__version__ = "v20260406l"
__appname__ = "espeak-ng_gui_fe"

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font as tk_font
import subprocess
import threading
import shutil
import os


# ── Palette ──────────────────────────────────────────────────────────────────
BG        = "#1a1a2e"
SURFACE   = "#16213e"
PANEL     = "#0f3460"
ACCENT    = "#e94560"
ACCENT2   = "#53d8fb"
FG        = "#e0e0e0"
FG_DIM    = "#7a7a9a"
FONT_MONO = ("Courier New", 10)
FONT_UI   = ("Courier New", 9)
FONT_H    = ("Courier New", 13, "bold")

# ── Default voice ─────────────────────────────────────────────────────────────
DEFAULT_VOICE_LABEL = "English_(America) [en-us]"
DEFAULT_VOICE_CODE  = "en-us"

# ── Voice presets ─────────────────────────────────────────────────────────────
# Each entry: "Label": (speed, pitch, amplitude, word_gap)
# Values are community approximations — adjust to taste.
PRESETS = {
    "— Select Preset —":               None,
    "Default (Normal)":                (175,  50, 100, 10),
    "Cylon Centurion (BSG 1978)":      (105,  12,  95, 22),
    "WOPR / Joshua (WarGames)":        (130,  22,  90, 18),
    "HAL 9000 (2001)":                 (140,  38,  85, 14),
    "Dalek (Doctor Who)":              (110,  15, 120, 20),
    "GLaDOS (Portal)":                 (150,  65,  95, 12),
    "JARVIS / FRIDAY (Marvel)":        (180,  55, 100,  8),
    "Terminator (T-800)":              (120,  18, 110, 22),
    "Speak & Spell (classic)":         ( 90,  72, 130, 25),
    "SAL 9000 (2010)":                 (145,  42,  88, 13),
    "Mother / MU-TH-UR (Alien)":      (125,  30,  80, 16),
    "MAX (Flight of Navigator)":       (160,  80, 105, 10),
    "KITT (Knight Rider)":             (170,  48, 100,  9),
    "Slow & Ominous":                  ( 80,  10, 100, 30),
    "Fast & Frantic":                  (350,  60, 120,  3),
    "Chipmunk":                        (250,  99, 110,  5),
    "Deep & Slow":                     ( 95,   5,  95, 20),
}


def check_espeak():
    if not shutil.which("espeak-ng"):
        messagebox.showerror(
            "espeak-ng not found",
            "espeak-ng is not installed or not on your PATH.\n\n"
            "Install it with:\n"
            "  Linux:   sudo apt install espeak-ng\n"
            "  macOS:   brew install espeak-ng\n"
            "  Windows: https://github.com/espeak-ng/espeak-ng/releases"
        )
        return False
    return True


def get_voices():
    """Return sorted list of (display_label, voice_code) tuples.

    espeak-ng --voices columns (confirmed on Debian 1.52.0):
      Pty  Language  Age/Gender  VoiceName           File         Other
      ' 5  en-us     --/M        English_(America)   gmw/en-us'

      parts[1] = lang code    e.g. "en-us"
      parts[3] = full name    e.g. "English_(America)"   ← display label
      parts[4] = file path    e.g. "gmw/en-us"           ← passed to -v

    Label is built as "English_(America) [en-us]" to match the original style.
    The en-us entry is always present so the combobox is never empty.
    """
    fallback = [(DEFAULT_VOICE_LABEL, DEFAULT_VOICE_CODE)]
    try:
        result = subprocess.run(
            ["espeak-ng", "--voices"],
            capture_output=True, text=True, timeout=5
        )
        voices = []
        for line in result.stdout.splitlines()[1:]:
            parts = line.split()
            if len(parts) < 5:
                continue
            lang      = parts[1]   # e.g. "en-us"
            full_name = parts[3]   # e.g. "English_(America)"
            file_path = parts[4]   # e.g. "gmw/en-us"  — passed to espeak-ng -v
            label = f"{full_name} [{lang}]"
            voices.append((label, file_path))   # store file_path as the voice code

        if not voices:
            return fallback

        voices.sort(key=lambda x: x[0])

        # Ensure en-us is always present
        if not any(DEFAULT_VOICE_CODE in code for _, code in voices):
            voices.insert(0, (DEFAULT_VOICE_LABEL, DEFAULT_VOICE_CODE))

        return voices

    except Exception:
        return fallback


class EspeakGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"espeak-ng  //  TTS Console  [{__version__}]")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self.root.minsize(780, 520)

        self._speak_proc = None
        self._speaking   = False

        self.voices = get_voices()
        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── UI Construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        self._style_ttk()

        # ── Header ──
        hdr = tk.Frame(self.root, bg=PANEL, pady=8)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"◈  espeak-ng TTS Console  {__version__}",
                 font=FONT_H, bg=PANEL, fg=ACCENT2).pack(side="left", padx=16)
        tk.Label(hdr, text="text-to-speech interface",
                 font=FONT_UI, bg=PANEL, fg=FG_DIM).pack(side="left")

        # ── Main area ──
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=16, pady=12)

        # ── Voice selector — full-width row above the left/right split ──
        voice_row = tk.Frame(body, bg=BG)
        voice_row.pack(fill="x", pady=(0, 10))
        self._section(voice_row, "VOICE")
        self.voice_var = tk.StringVar()
        voice_names = [v[0] for v in self.voices]
        self.voice_combo = ttk.Combobox(
            voice_row, textvariable=self.voice_var,
            values=voice_names, state="readonly", font=FONT_UI
        )
        default = next(
            (v[0] for v in self.voices if v[1] == DEFAULT_VOICE_CODE),
            self.voices[0][0]
        )
        self.voice_combo.set(default)
        self.voice_combo.pack(fill="x")
        self.root.after(100, self._fix_combo_width)

        # ── Left/right split ──
        split = tk.Frame(body, bg=BG)
        split.pack(fill="both", expand=True)

        # ── Left: text input ──
        left = tk.Frame(split, bg=BG)
        left.pack(side="left", fill="both", expand=True)

        self._section(left, "INPUT TEXT")
        self.text_box = tk.Text(
            left, height=12, wrap="word",
            bg=SURFACE, fg=FG, insertbackground=ACCENT2,
            font=FONT_MONO, relief="flat", padx=8, pady=8,
            selectbackground=PANEL, selectforeground=FG
        )
        self.text_box.pack(fill="both", expand=True, pady=(0, 10))
        self.text_box.insert("1.0", "Hello! I am espeak-ng, your text-to-speech engine.")

        # ── Right: settings panel ──
        right = tk.Frame(split, bg=SURFACE, padx=14, pady=14, width=320)
        right.pack(side="right", fill="y", padx=(14, 0))
        right.pack_propagate(False)

        # PRESET dropdown
        self._section(right, "PRESET")
        self.preset_var = tk.StringVar(value="— Select Preset —")
        preset_names = list(PRESETS.keys())
        self.preset_combo = ttk.Combobox(
            right, textvariable=self.preset_var,
            values=preset_names, state="readonly", font=FONT_UI
        )
        self.preset_combo.pack(fill="x", pady=(0, 10))
        self.preset_combo.bind("<<ComboboxSelected>>", self._apply_preset)

        # Divider
        tk.Frame(right, bg=PANEL, height=1).pack(fill="x", pady=(0, 6))

        # Sliders
        self._section(right, "SPEED  (wpm)")
        self.speed_var = tk.IntVar(value=175)
        self._slider(right, self.speed_var, 60, 450)

        self._section(right, "PITCH  (0–99)")
        self.pitch_var = tk.IntVar(value=50)
        self._slider(right, self.pitch_var, 0, 99)

        self._section(right, "AMPLITUDE  (0–200)")
        self.amp_var = tk.IntVar(value=100)
        self._slider(right, self.amp_var, 0, 200)

        self._section(right, "WORD GAP  (ms×10)")
        self.gap_var = tk.IntVar(value=10)
        self._slider(right, self.gap_var, 0, 100)

        # ── Status bar ──
        self.status_var = tk.StringVar(value="Ready.")
        status = tk.Frame(self.root, bg=PANEL, pady=4)
        status.pack(fill="x", side="bottom")
        self.status_lbl = tk.Label(
            status, textvariable=self.status_var,
            font=FONT_UI, bg=PANEL, fg=FG_DIM, anchor="w"
        )
        self.status_lbl.pack(side="left", padx=12)

        # ── Button bar ──
        btn_bar = tk.Frame(self.root, bg=BG, pady=8)
        btn_bar.pack(fill="x", padx=16, side="bottom")

        self.speak_btn = self._btn(btn_bar, "▶  SPEAK",  self._speak,   ACCENT)
        self.speak_btn.pack(side="left", padx=(0, 8))

        self.stop_btn = self._btn(btn_bar, "■  STOP",    self._stop,    "#444466")
        self.stop_btn.pack(side="left", padx=(0, 8))

        self._btn(btn_bar, "💾  SAVE WAV", self._save_wav, PANEL).pack(side="left")
        self._btn(btn_bar, "✕  CLEAR",    self._clear,    "#333355").pack(side="right")

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _section(self, parent, label):
        tk.Label(parent, text=label, font=("Courier New", 8, "bold"),
                 bg=parent["bg"], fg=ACCENT).pack(anchor="w", pady=(6, 1))

    def _slider(self, parent, var, from_, to):
        row = tk.Frame(parent, bg=parent["bg"])
        row.pack(fill="x", pady=(0, 6))
        tk.Label(row, textvariable=var, width=4,
                 font=FONT_UI, bg=parent["bg"], fg=ACCENT2).pack(side="right")
        ttk.Scale(row, from_=from_, to=to, orient="horizontal",
                  variable=var).pack(side="left", fill="x", expand=True)

    def _btn(self, parent, text, cmd, color):
        return tk.Button(
            parent, text=text, command=cmd,
            bg=color, fg=FG, activebackground=ACCENT2, activeforeground=BG,
            font=("Courier New", 10, "bold"), relief="flat",
            padx=14, pady=6, cursor="hand2", bd=0
        )

    def _style_ttk(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Force Combobox field colors in every possible state so the text is
        # always visible — including on first render before any interaction.
        style.configure("TCombobox",
                        fieldbackground=PANEL,
                        background=PANEL,
                        foreground=FG,
                        selectforeground=FG,
                        selectbackground=PANEL,
                        insertcolor=FG,
                        arrowcolor=ACCENT2,
                        bordercolor=PANEL,
                        lightcolor=PANEL,
                        darkcolor=PANEL)
        style.map("TCombobox",
                  fieldbackground=[("readonly", PANEL),
                                   ("disabled", SURFACE),
                                   ("active",   PANEL),
                                   ("focus",    PANEL),
                                   ("!focus",   PANEL)],
                  foreground=[("readonly", FG),
                              ("disabled", FG_DIM),
                              ("active",   FG),
                              ("focus",    FG),
                              ("!focus",   FG)],
                  selectforeground=[("readonly", FG),
                                    ("focus",    FG),
                                    ("!focus",   FG)],
                  selectbackground=[("readonly", PANEL),
                                    ("focus",    PANEL),
                                    ("!focus",   PANEL)],
                  background=[("active", PANEL),
                              ("pressed", PANEL)])

        style.configure("TScale",
                        background=BG, troughcolor=PANEL,
                        sliderlength=14, sliderrelief="flat")
        style.map("TScale", background=[("active", ACCENT2)])

    def _fix_combo_width(self):
        """Size the voice combobox to fit the longest voice name."""
        try:
            font = tk_font.Font(font=self.voice_combo["font"])
            voice_names = [v[0] for v in self.voices]
            max_px = max(font.measure(n) for n in voice_names) + 20
            char_width = font.measure("0") or 7
            self.voice_combo["width"] = max(max_px // char_width, 30)
        except Exception:
            pass

    def _apply_preset(self, event=None):
        """Load the selected preset's parameters into the sliders."""
        name = self.preset_var.get()
        params = PRESETS.get(name)
        if params is None:
            return   # "— Select Preset —" or unknown key
        speed, pitch, amp, gap = params
        self.speed_var.set(speed)
        self.pitch_var.set(pitch)
        self.amp_var.set(amp)
        self.gap_var.set(gap)
        self._set_status(f"Preset loaded: {name}", ACCENT2)

    def _get_voice_code(self):
        label = self.voice_var.get()
        for disp, code in self.voices:
            if disp == label:
                return code
        return DEFAULT_VOICE_CODE

    def _build_cmd(self, text, outfile=None):
        """Build the espeak-ng command. Text is passed as a CLI argument."""
        cmd = [
            "espeak-ng",
            "-v", self._get_voice_code(),
            "-s", str(self.speed_var.get()),
            "-p", str(self.pitch_var.get()),
            "-a", str(self.amp_var.get()),
            "-g", str(self.gap_var.get()),
        ]
        if outfile:
            cmd += ["-w", outfile]
        cmd.append(text)
        return cmd

    def _set_status(self, msg, color=FG_DIM):
        self.status_var.set(msg)
        self.status_lbl.configure(fg=color)

    # ── Actions ───────────────────────────────────────────────────────────────

    def _speak(self):
        if self._speaking:
            self._stop()
        text = self.text_box.get("1.0", "end").strip()
        if not text:
            self._set_status("No text to speak.", ACCENT)
            return
        self._speaking = True
        self._set_status("Speaking…", ACCENT2)
        self.speak_btn.configure(state="disabled")

        def run():
            try:
                cmd = self._build_cmd(text)
                self._speak_proc = subprocess.Popen(
                    cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
                )
                _, err = self._speak_proc.communicate()
                if self._speak_proc.returncode not in (0, -15):
                    err_msg = err.decode().strip() if err else "Unknown error"
                    self.root.after(0, lambda: messagebox.showerror(
                        "espeak-ng error", err_msg))
            except FileNotFoundError:
                self.root.after(0, lambda: messagebox.showerror(
                    "Error", "espeak-ng not found on PATH."))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            finally:
                self._speaking = False
                self._speak_proc = None
                self.root.after(0, lambda: self.speak_btn.configure(state="normal"))
                self.root.after(0, lambda: self._set_status("Done.", FG_DIM))

        threading.Thread(target=run, daemon=True).start()

    def _stop(self):
        if self._speak_proc:
            try:
                self._speak_proc.terminate()
            except Exception:
                pass
        self._speaking = False
        self._set_status("Stopped.", FG_DIM)
        self.speak_btn.configure(state="normal")

    def _save_wav(self):
        text = self.text_box.get("1.0", "end").strip()
        if not text:
            self._set_status("No text to save.", ACCENT)
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV audio", "*.wav"), ("All files", "*.*")],
            title="Save speech as WAV"
        )
        if not path:
            return
        self._set_status("Saving WAV…", ACCENT2)
        try:
            cmd = self._build_cmd(text, outfile=path)
            result = subprocess.run(cmd, capture_output=True, timeout=60)
            if result.returncode == 0:
                self._set_status(f"Saved → {os.path.basename(path)}", ACCENT2)
                messagebox.showinfo("Saved", f"WAV file saved:\n{path}")
            else:
                self._set_status("Save failed.", ACCENT)
                messagebox.showerror("Error", result.stderr.decode())
        except Exception as e:
            self._set_status("Error.", ACCENT)
            messagebox.showerror("Error", str(e))

    def _clear(self):
        self.text_box.delete("1.0", "end")
        self._set_status("Cleared.", FG_DIM)

    def _on_close(self):
        self._stop()
        self.root.destroy()


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    root = tk.Tk()
    if not check_espeak():
        root.destroy()
        return
    app = EspeakGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
