#!/usr/bin/env python3
"""
espeak-ng GUI Front-End
Version: v20260406f
A clean Tkinter interface for the espeak-ng text-to-speech engine.
Requires: espeak-ng installed and on PATH

Changelog:
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

__version__ = "v20260406f"
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
    """Return list of (display_name, lang_code) tuples from espeak-ng --voices.

    espeak-ng --voices columns:
      Pty  Lang  Age/Gender  VoiceName  File  [Other languages...]
      e.g.:
       5  en-us  M  english-us  en/en-us
    We build the label as "VoiceName  [Lang]" so it is human-readable.
    """
    try:
        result = subprocess.run(
            ["espeak-ng", "--voices"],
            capture_output=True, text=True, timeout=5
        )
        voices = []
        for line in result.stdout.splitlines()[1:]:   # skip header
            parts = line.split()
            if len(parts) >= 5:
                lang      = parts[1]   # e.g. "en-us"
                voicename = parts[3]   # e.g. "english-us"
                label     = f"{voicename}  [{lang}]"
                voices.append((label, lang))
        voices.sort(key=lambda x: x[0])
        return voices if voices else [("english-us  [en-us]", "en-us")]
    except Exception:
        return [("english-us  [en-us]", "en-us")]


class EspeakGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"espeak-ng  //  TTS Console  [{__version__}]")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self.root.minsize(780, 500)

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
            (v[0] for v in self.voices if v[1] == "en-us"),
            next((v[0] for v in self.voices if v[1].startswith("en")), voice_names[0])
        )
        self.voice_combo.set(default)
        self.voice_combo.pack(fill="x")
        # After the window is drawn, size the combobox to fit the longest entry
        self.root.after(100, self._fix_combo_width)

        # ── Left/right split ──
        split = tk.Frame(body, bg=BG)
        split.pack(fill="both", expand=True)

        # Left: text input
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

        # Right: settings panel
        right = tk.Frame(split, bg=SURFACE, padx=14, pady=14, width=320)
        right.pack(side="right", fill="y", padx=(14, 0))
        right.pack_propagate(False)

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
        style.configure("TCombobox",
                        fieldbackground=PANEL, background=PANEL,
                        foreground=FG, selectbackground=ACCENT,
                        arrowcolor=ACCENT2)
        style.configure("TScale",
                        background=BG, troughcolor=PANEL,
                        sliderlength=14, sliderrelief="flat")
        style.map("TScale", background=[("active", ACCENT2)])

    def _fix_combo_width(self):
        """Size the combobox widget to fit the longest voice name."""
        try:
            font = tk_font.Font(font=self.voice_combo["font"])
            voice_names = [v[0] for v in self.voices]
            max_px = max(font.measure(n) for n in voice_names) + 20
            char_width = font.measure("0") or 7
            self.voice_combo["width"] = max(max_px // char_width, 30)
        except Exception:
            pass  # Non-critical — widget already fills its row with fill="x"

    def _get_voice_code(self):
        label = self.voice_var.get()
        for disp, code in self.voices:
            if disp == label:
                return code
        return "en-us"

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
        cmd.append(text)   # text as final positional argument
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
                if self._speak_proc.returncode not in (0, -15):  # -15 = SIGTERM (stop)
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
            result = subprocess.run(
                cmd, capture_output=True, timeout=60
            )
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
