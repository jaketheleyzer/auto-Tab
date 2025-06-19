NOTE_NAMES = ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B']

def hz_to_note_name(frequency):
    if frequency <= 0:
        return None
    import numpy as np
    A4 = 440
    semitones = int(round(12 * np.log2(frequency / A4)))
    note_index = (semitones + 9) % 12
    octave = 4 + ((semitones + 9) // 12)
    return f"{NOTE_NAMES[note_index]}{octave}"
