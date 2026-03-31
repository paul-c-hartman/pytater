# Pytater

*Offline Speech to Text for Linux.*

> [!IMPORTANT]
> This project is a fork of [ideasman42's Nerd Dictation](https://github.com/ideasman42/nerd-dictation)--where the original is a script meant for easy hacking, this is a full-fledged Python package, meant to provide vastly simpler setup and a Python API on top of the original CLI.

See [demo video](https://www.youtube.com/watch?v=T7sR-4DFhpQ) (from ideasman42).

This is a utility that provides simple access speech to text for using in Linux
without being tied to a desktop environment, using the excellent [VOSK-API](https://github.com/alphacep/vosk-api).

_**Simple to set up**_  
   &nbsp;&nbsp;&nbsp;Pytater can be installed with a single command from PyPi.  
_**Configurable**_  
   &nbsp;&nbsp;&nbsp;Configure pytater using config files, environment variables, or the Python API (partially complete).  
_**Zero Overhead**_  
   &nbsp;&nbsp;&nbsp;As pytater is activated manually, there are no background processes.

## Usage

It is suggested to bind begin/end/cancel to shortcut keys.

```sh
pytater begin
```
```sh
pytater end
```

For details on how this can be used, see:
`pytater --help` and `pytater begin --help`.

## Features

Specific features include:

### Numbers as Digits
Optional conversion from numbers to digits.

So `Three million five hundred and sixty second` becomes `3,000,562nd`.

A series of numbers (such as reciting a phone number) is also supported.

So `Two four six eight` becomes `2,468`.

### Time Out
Optionally end speech to text early when no speech is detected for a given number of seconds.
(without an explicit call to `end` which is otherwise required).

### Output Type
Output can simulate keystroke events (default) or simply print to the standard output.

## User configuration
TODO: fill in this section

## Suspend/Resume
Initial load time can be an issue for users on slower systems or with some of the larger language-models. In this case, suspend/resume can be useful. While suspended, all data is kept in memory and the process is stopped. Audio recording is stopped and restarted on resume.

See `pytater begin --help` for details on how to access these options.

## Dependencies

- Python 3.6.2 (or newer).
- An audio recording utility (`parec` by default).
- An input simulation utility (`xdotool` by default). (This is not necessary if all you're doing is printing dictated words to the terminal.)

### Audio Recording Utilities

You may select one of the following tools.

- `parec` command for recording from pulse-audio.
- `sox` command as alternative, see the guide: [Using sox with pytater](readme-sox.md).
- `pw-cat` command for recording from pipewire.

### Input Simulation Utilities

You may select one of the following input simulation utilities.

- [xdotool](https://github.com/jordansissel/xdotool) command to simulate input in X11.
- [ydotool](https://github.com/ReimuNotMoe/ydotool) command to simulate input anywhere (X11/Wayland/TTYs).
  See the setup guide: [Using ydotool with pytater](readme-ydotool.md).
- [dotool](https://git.sr.ht/~geb/dotool) command to simulate input anywhere (X11/Wayland/TTYs).
- [wtype](https://github.com/atx/wtype) to simulate input in Wayland".

## Install

With pip (not recommended, as this will install it globally):

```sh
pip3 install pytater
```

Or alternatively, using [uv](https://github.com/astral-sh/uv) or [pipx](https://pipx.pypa.io/stable/):

```sh
uv tool install pytater
# or:
pipx install pytater
# This will add a `pytater` command to your PATH
```

Then download a model. The complete list of models is available [here](https://alphacephei.com/vosk/models). To do this:

```sh
pytater download # to download the default model, or:
pytater download --model large
# Or by URL:
pytater download --model "https://alphacephei.com/path/to/model"
```

To test dictation:

```sh
pytater begin &
# Start speaking.
pytater end
```

- Reminder that it's up to you to bind begin/end/cancel to actions you can easily access (typically key shortcuts).

## Details

- Typing in results will **never** press enter/return.
- Recording and speech to text is performed in parallel.

## Examples

Store the result of speech to text as a variable in the shell:

```sh
SPEECH="$(pytater begin --timeout=1.0 --output=STDOUT)"
```

## Limitations

- Text from VOSK is all lower-case. While the user configuration can be used to set the case of common words like `I`, this isn't very convenient.
- For some users the delay in start up may be noticeable on systems with slower hard disks especially when running for the 1st time (a cold start). This is a limitation with the choice not to use a service that runs in the background. Recording begins before any the speech-to-text components are loaded to mitigate this problem.

## Roadmap

- Complete and documented API (partially complete)
- Proper extension support using [entry points](https://setuptools.pypa.io/en/latest/userguide/entry_point.html)
- Reimplement certain features as post-processors
  - General solution to capitalize words (proper nouns for example)
- Proper logging system
- Processing of audio files in addition to live audio
- Support Windows & macOS
