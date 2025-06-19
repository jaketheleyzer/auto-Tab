import math
import numpy as np


def freq_to_note_name(freq):
    """Convert frequency (Hz) to the closest note name (e.g., A4, C♯3)"""
    if freq <= 0:
        return None
    A4 = 440.0
    NOTES = ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B']
    semitones = int(round(12 * np.log2(freq / A4)))
    note_index = (semitones + 9) % 12
    octave = 4 + ((semitones + 9) // 12)
    return f"{NOTES[note_index]}{octave}"


def extract_notes_crepe(times, freqs, confidences):
    notes = []
    prev_note = None
    start_time = None
    confs = []

    for i in range(len(freqs)):
        freq = freqs[i]
        conf = confidences[i]
        time = times[i]

        if freq == 0 or conf < 0.01:
            note = None
        else:
            note = freq_to_note_name(freq)

        if note == prev_note:
            confs.append(conf * 100)
        else:
            if prev_note is not None:
                end_time = time
                duration = end_time - start_time
                avg_conf = sum(confs) / len(confs)
                notes.append((start_time, end_time, prev_note, duration, avg_conf))

            prev_note = note
            start_time = time
            confs = [conf * 100] if note else []

    # Add the last note
    if prev_note is not None and confs:
        end_time = times[-1]
        duration = end_time - start_time
        avg_conf = sum(confs) / len(confs)
        notes.append((start_time, end_time, prev_note, duration, avg_conf))

    # Apply filters
    min_duration = 0.04
    min_avg_conf = 45

    filtered = []
    for start, end, note, duration, avg_conf in notes:
        boosted_conf = avg_conf * (0.5 + duration)
        if duration >= min_duration and boosted_conf >= 50:
            percent_conf = round(boosted_conf, 2)
            filtered.append((start, end, note, percent_conf))

    return filtered
