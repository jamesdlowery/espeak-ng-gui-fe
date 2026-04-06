# espeak-ng GUI Front-End

A clean, dark-themed Python/Tkinter graphical interface for the
[espeak-ng](https://github.com/espeak-ng/espeak-ng) text-to-speech engine.
Type or paste text, choose a language voice, dial in your parameters, and hit
**Speak** — or save the result as a WAV file.

---

## Screenshot

> *(Add a screenshot here once the app is running — e.g. `docs/screenshot.png`)*

---

## Features

- **Full voice list** — populated automatically from `espeak-ng --voices`,
  showing complete names (e.g. `English_(America) [en-us]`) with
  `English_(America)` pre-selected as the default.
- **Sci-Fi / Robotic Presets** — one-click presets that load Speed, Pitch,
  Amplitude, and Word Gap settings approximating famous fictional computer
  voices:

  | Preset | Inspiration |
  |---|---|
  | Default (Normal) | Standard espeak-ng defaults |
  | Cylon Centurion (BSG 1978) | *Battlestar Galactica* (1978) |
  | WOPR / Joshua (WarGames) | *WarGames* (1983) |
  | HAL 9000 (2001) | *2001: A Space Odyssey* (1968) |
  | Dalek (Doctor Who) | *Doctor Who* |
  | GLaDOS (Portal) | *Portal* / *Portal 2* |
  | JARVIS / FRIDAY (Marvel) | *Iron Man* / *Avengers* |
  | Terminator (T-800) | *The Terminator* (1984) |
  | Speak & Spell (classic) | Texas Instruments Speak & Spell (1978) |
  | SAL 9000 (2010) | *2010: The Year We Make Contact* (1984) |
  | Mother / MU-TH-UR (Alien) | *Alien* (1979) |
  | MAX (Flight of Navigator) | *Flight of the Navigator* (1986) |
  | KITT (Knight Rider) | *Knight Rider* (1982) |
  | Slow & Ominous | — |
  | Fast & Frantic | — |
  | Chipmunk | — |
  | Deep & Slow | — |

- **Manual controls** — independent sliders for:
  - **Speed** (60–450 wpm)
  - **Pitch** (0–99)
  - **Amplitude** (0–200)
  - **Word Gap** (0–100 × 10 ms)
- **▶ Speak** — synthesizes and plays speech in a background thread so the
  UI stays responsive.
- **■ Stop** — terminates playback immediately.
- **💾 Save WAV** — writes the speech to a `.wav` file of your choice.
- **✕ Clear** — clears the text input area.
- **Status bar** — shows current state (Ready / Speaking / Done / errors).
- Graceful startup error if `espeak-ng` is not installed or not on `PATH`.

---

## Requirements

### espeak-ng

This GUI is a front-end only — it requires `espeak-ng` to be installed
separately and available on your system `PATH`.

| Platform | Install command |
|---|---|
| Debian / Ubuntu / Mint | `sudo apt install espeak-ng` |
| Fedora / RHEL | `sudo dnf install espeak-ng` |
| Arch Linux | `sudo pacman -S espeak-ng` |
| macOS (Homebrew) | `brew install espeak-ng` |
| Windows | Download installer from [espeak-ng releases](https://github.com/espeak-ng/espeak-ng/releases) |

### Python

- **Python 3.8 or later**
- **Tkinter** — included in the standard library on most platforms.
  - If missing on Debian/Ubuntu: `sudo apt install python3-tk`

No third-party Python packages are required.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/espeak-ng-gui-fe.git
cd espeak-ng-gui-fe

# Run directly — no install step needed
python3 espeak-ng_gui_fe_v20260406l.py
```

Or just download the single `.py` file and run it.

---

## Usage

1. **Select a Voice** from the full-width dropdown at the top.
   `English_(America) [en-us]` is selected by default.
2. **Optionally select a Preset** from the right panel to load a named
   voice character's parameters.
3. **Adjust sliders** for Speed, Pitch, Amplitude, and Word Gap as desired.
   Presets can be fine-tuned after loading.
4. **Type or paste text** into the input area.
5. Click **▶ SPEAK** to hear the result, or **💾 SAVE WAV** to save it.

---

## File Naming Convention

Releases follow the convention:

```
espeak-ng_gui_fe_vYYYYMMDDx.py
```

where `YYYYMMDD` is the date and `x` is an alphabetic revision letter
(`a`, `b`, `c`, …) for multiple releases on the same day.

---

## Changelog

| Version | Summary |
|---|---|
| v20260406l | Fixed full voice names — `parts[3]` from `--voices` output is the complete VoiceName; dropped unreliable file-reading approach |
| v20260406k | Attempted voice name restoration via on-disk file reading (failed on Debian — path not found) |
| v20260406j | Added **Cylon Centurion (BSG 1978)** preset |
| v20260406i | Added **PRESET** dropdown with 16 named sci-fi / robotic voice approximations |
| v20260406h | Fixed VOICE field appearing blank on first launch (white-on-white text); forced TTK Combobox color states |
| v20260406g | Fixed blank VOICE menu; corrected `--voices` column parsing; guaranteed `en-us` default always present |
| v20260406f | Made `English_(America) [en-us]` the explicit startup default |
| v20260406e | Fixed silent playback — switched from stdin to CLI argument for text; errors now shown in dialog |
| v20260406d | Fixed crash: `_style_ttk` accidentally merged into `_fix_combo_width` in v20260406c |
| v20260406c | Moved VOICE selector to full-width row above left/right split; dropdown popup sized to longest entry |
| v20260406b | Widened right settings panel so slider labels are fully readable |
| v20260406a | Initial release |

---

## Notes on Presets

The preset parameter values are **community approximations** based on the
acoustic character of each fictional voice. None can exactly replicate the
original — for example, the Cylon Centurion voice was created using an
**ARP 2500 synthesizer** fed through an **EMS Vocoder 1000**, a hardware
chain that espeak-ng's formant synthesis cannot reproduce. Presets are a
starting point; the sliders let you tune from there.

---

## License

MIT License — see `LICENSE` for details.

---

## Contributing

Pull requests are welcome. If you have a well-tested preset for a voice not
yet included, feel free to open an issue or PR with the suggested
Speed / Pitch / Amplitude / Word Gap values and the fictional voice's source.
