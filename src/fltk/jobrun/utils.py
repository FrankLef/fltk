from pathlib import Path
import winsound

dir_path = Path(__file__).resolve().parent
SUCCESS_WAV = "kids-cartoon-close-bells-2256.wav"


def ring_success() -> None:
    sound_file = str(dir_path.joinpath(SUCCESS_WAV))
    winsound.PlaySound(sound_file, flags=winsound.SND_FILENAME)
    # winsound.MessageBeep(winsound.MB_ICONASTERISK)
    # winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    # winsound.Beep(440, 500)


def ring_error() -> None:
    winsound.MessageBeep(winsound.MB_ICONHAND)
    # winsound.Beep(440, 500)
