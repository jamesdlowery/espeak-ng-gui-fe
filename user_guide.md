# espeak-ng GUI Front-End — User Guide

**Version:** v20260406l  
**Application:** `espeak-ng_gui_fe`  
**Last updated:** 2026-04-06

---

## Table of Contents

1. [Overview](#1-overview)
2. [Prerequisites](#2-prerequisites)
   - 2.1 [Installing espeak-ng](#21-installing-espeak-ng)
   - 2.2 [Python and Tkinter](#22-python-and-tkinter)
3. [Starting the Program](#3-starting-the-program)
4. [The Interface at a Glance](#4-the-interface-at-a-glance)
5. [Voice Selection](#5-voice-selection)
6. [Entering Text](#6-entering-text)
7. [Presets](#7-presets)
   - 7.1 [What Presets Do](#71-what-presets-do)
   - 7.2 [Available Presets](#72-available-presets)
   - 7.3 [A Note on Accuracy](#73-a-note-on-accuracy)
8. [The Parameter Sliders](#8-the-parameter-sliders)
   - 8.1 [Speed](#81-speed)
   - 8.2 [Pitch](#82-pitch)
   - 8.3 [Amplitude](#83-amplitude)
   - 8.4 [Word Gap](#84-word-gap)
9. [The Buttons](#9-the-buttons)
   - 9.1 [▶ SPEAK](#91--speak)
   - 9.2 [■ STOP](#92--stop)
   - 9.3 [💾 SAVE WAV](#93--save-wav)
   - 9.4 [✕ CLEAR](#94--clear)
10. [The Status Bar](#10-the-status-bar)
11. [Typical Workflows](#11-typical-workflows)
    - 11.1 [Quick speech test](#111-quick-speech-test)
    - 11.2 [Trying a sci-fi voice preset](#112-trying-a-sci-fi-voice-preset)
    - 11.3 [Saving speech to a WAV file](#113-saving-speech-to-a-wav-file)
    - 11.4 [Finding your own voice settings](#114-finding-your-own-voice-settings)
12. [Troubleshooting](#12-troubleshooting)
13. [File Naming Convention](#13-file-naming-convention)

---

## 1. Overview

The **espeak-ng GUI Front-End** is a graphical interface for the
[espeak-ng](https://github.com/espeak-ng/espeak-ng) text-to-speech engine.
Instead of typing command-line arguments, you use drop-down menus and sliders
to control how espeak-ng speaks your text — and you can hear the result
immediately or save it as a WAV audio file.

The program requires `espeak-ng` to be installed on your system. It does not
replace espeak-ng; it sits in front of it.

---

## 2. Prerequisites

### 2.1 Installing espeak-ng

The GUI will show an error dialog and refuse to start if `espeak-ng` is not
found on your system PATH. Install it first using the command for your
platform:

| Platform | Command |
|---|---|
| Debian / Ubuntu / Linux Mint | `sudo apt install espeak-ng` |
| Fedora / RHEL / CentOS | `sudo dnf install espeak-ng` |
| Arch Linux / Manjaro | `sudo pacman -S espeak-ng` |
| macOS (Homebrew) | `brew install espeak-ng` |
| Windows | Download from [espeak-ng releases](https://github.com/espeak-ng/espeak-ng/releases) and run the installer |

After installation, verify it works by opening a terminal and running:

```bash
espeak-ng "Hello, world."
```

You should hear speech. If you do, the GUI will work.

### 2.2 Python and Tkinter

- **Python 3.8 or later** is required.
- **Tkinter** is part of the Python standard library and is included
  automatically on most platforms. If it is missing (some minimal Linux
  installs omit it), install it with:

  ```bash
  sudo apt install python3-tk        # Debian / Ubuntu
  sudo dnf install python3-tkinter   # Fedora
  ```

No additional Python packages need to be installed with `pip`.

---

## 3. Starting the Program

Open a terminal, navigate to the folder containing the script, and run:

```bash
python3 espeak-ng_gui_fe_v20260406l.py
```

On Windows you can also double-click the `.py` file if Python is associated
with `.py` files in your system settings.

If `espeak-ng` is not found, an error dialog will appear explaining how to
install it, and the program will exit.

---

## 4. The Interface at a Glance

```
┌─────────────────────────────────────────────────────────────────┐
│  ◈  espeak-ng TTS Console  v20260406l    text-to-speech interface│  ← Header
├─────────────────────────────────────────────────────────────────┤
│  VOICE                                                           │
│  [ English_(America) [en-us]                                ▼ ] │  ← Voice selector
├──────────────────────────────────┬──────────────────────────────┤
│  INPUT TEXT                      │  PRESET                      │
│                                  │  [ — Select Preset —     ▼ ] │
│  (text area)                     │  ───────────────────────────  │
│                                  │  SPEED  (wpm)          175   │
│                                  │  [slider]                    │
│                                  │  PITCH  (0–99)          50   │
│                                  │  [slider]                    │
│                                  │  AMPLITUDE  (0–200)    100   │
│                                  │  [slider]                    │
│                                  │  WORD GAP  (ms×10)      10   │
│                                  │  [slider]                    │
├──────────────────────────────────┴──────────────────────────────┤
│  [ ▶ SPEAK ]  [ ■ STOP ]  [ 💾 SAVE WAV ]          [ ✕ CLEAR ] │  ← Buttons
├─────────────────────────────────────────────────────────────────┤
│  Ready.                                                          │  ← Status bar
└─────────────────────────────────────────────────────────────────┘
```

The window is resizable. Dragging the edges makes the text input area and
settings panel grow accordingly.

---

## 5. Voice Selection

The **VOICE** dropdown at the top of the window lists every voice installed
with your copy of espeak-ng. The list is populated automatically at startup
by running `espeak-ng --voices` in the background.

- Voices are shown with their full name and language code, for example:
  `English_(America) [en-us]`, `French_(France) [fr]`, `Deutsch [de]`.
- **`English_(America) [en-us]`** is selected by default when the program
  first opens.
- Click the dropdown to scroll through all available voices. The list is
  sorted alphabetically by voice name.
- You can change the voice at any time — even during playback the new voice
  will take effect on the next **SPEAK**.

> **Tip:** The number and names of voices depends entirely on what is
> installed with your copy of espeak-ng. Installing additional espeak-ng
> language packs will add more entries to this list the next time you start
> the program.

---

## 6. Entering Text

Click anywhere in the large **INPUT TEXT** area on the left and type or paste
the text you want to speak. There is no length limit imposed by the GUI,
though very long texts will take longer to synthesize.

- Standard cut (`Ctrl+X`), copy (`Ctrl+C`), and paste (`Ctrl+V`) work in
  the text area.
- Line breaks are preserved and affect phrasing and pauses.
- The text area starts with a short sample sentence. Simply select all and
  type to replace it.

---

## 7. Presets

### 7.1 What Presets Do

The **PRESET** dropdown in the right settings panel lets you load a named
set of Speed, Pitch, Amplitude, and Word Gap values with a single click.
When you select a preset, all four sliders update immediately.

Presets do **not** change the selected Voice — language selection remains
under your control in the VOICE dropdown.

After loading a preset you can still adjust the sliders freely to fine-tune
the result.

### 7.2 Available Presets

| Preset | Speed | Pitch | Amplitude | Word Gap | Inspired by |
|---|:-:|:-:|:-:|:-:|---|
| Default (Normal) | 175 | 50 | 100 | 10 | Standard espeak-ng defaults |
| Cylon Centurion (BSG 1978) | 105 | 12 | 95 | 22 | *Battlestar Galactica* (1978) |
| WOPR / Joshua (WarGames) | 130 | 22 | 90 | 18 | *WarGames* (1983) |
| HAL 9000 (2001) | 140 | 38 | 85 | 14 | *2001: A Space Odyssey* (1968) |
| Dalek (Doctor Who) | 110 | 15 | 120 | 20 | *Doctor Who* |
| GLaDOS (Portal) | 150 | 65 | 95 | 12 | *Portal* / *Portal 2* |
| JARVIS / FRIDAY (Marvel) | 180 | 55 | 100 | 8 | *Iron Man* / *Avengers* |
| Terminator (T-800) | 120 | 18 | 110 | 22 | *The Terminator* (1984) |
| Speak & Spell (classic) | 90 | 72 | 130 | 25 | TI Speak & Spell (1978) |
| SAL 9000 (2010) | 145 | 42 | 88 | 13 | *2010: The Year We Make Contact* (1984) |
| Mother / MU-TH-UR (Alien) | 125 | 30 | 80 | 16 | *Alien* (1979) |
| MAX (Flight of Navigator) | 160 | 80 | 105 | 10 | *Flight of the Navigator* (1986) |
| KITT (Knight Rider) | 170 | 48 | 100 | 9 | *Knight Rider* (1982) |
| Slow & Ominous | 80 | 10 | 100 | 30 | General-purpose effect |
| Fast & Frantic | 350 | 60 | 120 | 3 | General-purpose effect |
| Chipmunk | 250 | 99 | 110 | 5 | General-purpose effect |
| Deep & Slow | 95 | 5 | 95 | 20 | General-purpose effect |

### 7.3 A Note on Accuracy

These presets are **approximations** of the acoustic character of each voice,
not exact reproductions. Many of the original fictional voices were created
with hardware that espeak-ng's formant synthesis cannot replicate. For
example, the 1978 Cylon Centurion voice was produced using an **ARP 2500
modular synthesizer** fed through an **EMS Vocoder 1000** — a complex analog
signal chain. The preset captures the spirit (slow, very low-pitched,
deliberate) rather than the exact timbre. Use the sliders to refine any
preset to your liking.

---

## 8. The Parameter Sliders

All four sliders are in the right-hand settings panel. The current numeric
value is displayed to the right of each slider and updates as you drag.

### 8.1 Speed

**Range:** 60 – 450 words per minute  
**Default:** 175 wpm

Controls how fast espeak-ng speaks. The default of 175 wpm is a natural
conversational pace for English. Values below 120 sound slow and deliberate;
values above 300 become difficult to understand.

### 8.2 Pitch

**Range:** 0 – 99  
**Default:** 50

Controls the base pitch (tone) of the voice. Lower values produce a deeper,
more robotic sound. Higher values produce a higher-pitched, more excitable
sound. Pitch interacts with the selected voice — some voices have a naturally
higher or lower register.

### 8.3 Amplitude

**Range:** 0 – 200  
**Default:** 100

Controls the volume of the synthesized speech relative to the system audio
level. 100 is the standard level. Values above 100 increase volume; values
below decrease it. Note that very high values (above ~160) may cause
distortion on some audio hardware.

### 8.4 Word Gap

**Range:** 0 – 100 (units of 10 ms at default speed)  
**Default:** 10

Inserts a pause between each word. The unit is 10 milliseconds at the default
speed of 175 wpm (the actual pause duration scales with speed). A value of 0
produces no extra gap; higher values give speech a more halting, deliberate
quality — useful for robotic voice effects.

---

## 9. The Buttons

### 9.1 ▶ SPEAK

Sends the current text to espeak-ng with the selected voice and slider
settings, and plays it through your system audio output. Synthesis runs in
a background thread so the interface remains usable during playback.

The button is disabled (greyed out) while speech is in progress, and
re-enables automatically when playback finishes.

If espeak-ng reports an error (for example, an unrecognised voice code),
an error dialog will appear with the message from espeak-ng.

### 9.2 ■ STOP

Immediately terminates any speech currently in progress. The **▶ SPEAK**
button re-enables straight away.

### 9.3 💾 SAVE WAV

Opens a **Save As** dialog so you can choose a filename and location. The
program then runs espeak-ng with the current settings and writes the output
as a standard `.wav` audio file instead of playing it through the speakers.

WAV files can be opened in any audio editor (Audacity, etc.) or media
player, and are suitable for further processing or embedding in other
projects.

### 9.4 ✕ CLEAR

Clears all text from the input area. This cannot be undone, so use with
care. The voice, preset, and slider settings are not affected.

---

## 10. The Status Bar

The narrow bar at the very bottom of the window shows the current state of
the program:

| Message | Meaning |
|---|---|
| `Ready.` | Waiting for input |
| `Speaking…` | Playback is in progress |
| `Done.` | Playback finished normally |
| `Stopped.` | Playback was interrupted by **■ STOP** |
| `Preset loaded: <name>` | A preset was applied successfully |
| `Saved → <filename>` | A WAV file was saved successfully |
| `Save failed.` | espeak-ng returned an error during WAV save |
| `No text to speak.` | **▶ SPEAK** was clicked with an empty text area |
| `No text to save.` | **💾 SAVE WAV** was clicked with an empty text area |
| `Cleared.` | The text area was cleared |
| `Error.` | An unexpected error occurred (see the dialog that appeared) |

---

## 11. Typical Workflows

### 11.1 Quick speech test

1. Leave the Voice set to `English_(America) [en-us]`.
2. Delete the sample text and type your own.
3. Click **▶ SPEAK**.

### 11.2 Trying a sci-fi voice preset

1. Select a Voice — for most presets `English_(America) [en-us]` works well.
2. Open the **PRESET** dropdown and choose, for example,
   `WOPR / Joshua (WarGames)`.
3. The sliders update automatically.
4. Type a suitably dramatic message in the text area.
5. Click **▶ SPEAK**.
6. Adjust any slider if you want to push the effect further, then
   click **▶ SPEAK** again.

### 11.3 Saving speech to a WAV file

1. Select your Voice and set your parameters (or choose a preset).
2. Type the text you want to record.
3. Click **💾 SAVE WAV**.
4. Choose a folder and filename in the dialog that appears, then click Save.
5. The status bar will confirm `Saved → yourfile.wav` when complete.

### 11.4 Finding your own voice settings

1. Start with **Default (Normal)** as your baseline or choose the closest
   preset as a starting point.
2. Adjust **Speed** first — this has the biggest effect on character.
3. Then lower **Pitch** for a deeper/robotic quality, or raise it for a
   higher/excitable quality.
4. Use **Word Gap** to add deliberateness or urgency.
5. Adjust **Amplitude** last if the volume feels wrong.
6. Click **▶ SPEAK** after each change to audition the result.

---

## 12. Troubleshooting

**The program won't start and shows an error about espeak-ng.**  
espeak-ng is not installed or is not on your system PATH. Install it using
the command for your platform listed in [Section 2.1](#21-installing-espeak-ng),
then try again.

**The VOICE dropdown is empty or shows only one entry.**  
The `espeak-ng --voices` command returned no usable output. Verify that
espeak-ng is working correctly by running `espeak-ng --voices` in a terminal.
If that command itself produces no output, your espeak-ng installation may be
incomplete.

**I click ▶ SPEAK but hear nothing.**  
Check that your system audio is not muted and that the default audio output
device is working. Try running `espeak-ng "test"` directly in a terminal to
confirm espeak-ng itself can produce audio outside the GUI.

**The speech sounds wrong after selecting a preset.**  
Presets are approximations. The sliders remain editable after a preset is
loaded — adjust Speed, Pitch, Amplitude, and Word Gap until the result
sounds right for your system and voice.

**Saving a WAV file fails.**  
An error dialog will appear with the message from espeak-ng. The most common
cause is a path permission problem (trying to save to a location you do not
have write access to). Choose a different save location, such as your home
folder or Desktop.

**The window opens but the VOICE field looks blank.**  
This is a display issue where the text color matches the background. It
should not occur in v20260406h or later. If you see it, update to the latest
version of the script.

---

## 13. File Naming Convention

Each release of the script follows this naming pattern:

```
espeak-ng_gui_fe_vYYYYMMDDx.py
```

| Part | Meaning | Example |
|---|---|---|
| `espeak-ng_gui_fe` | Application name (GUI Front-End) | — |
| `v` | Version prefix | — |
| `YYYYMMDD` | Release date (ISO 8601) | `20260406` = April 6, 2026 |
| `x` | Revision letter within that date | `l` = twelfth revision |

If you have multiple versions of the file, the one with the latest date and
latest letter is the most current. Always use the latest version unless you
have a specific reason to stay on an older one.
