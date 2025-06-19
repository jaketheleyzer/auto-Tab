import numpy as np

STANDARD_TUNING = {
    6: ('E2', 40),
    5: ('A2', 45),
    4: ('D3', 50),
    3: ('G3', 55),
    2: ('B3', 59),
    1: ('E4', 64),
}

NOTE_TO_MIDI = {
    'C': 0, 'C♯': 1, 'D': 2, 'D♯': 3, 'E': 4, 'F': 5,
    'F♯': 6, 'G': 7, 'G♯': 8, 'A': 9, 'A♯': 10, 'B': 11
}


def note_name_to_midi(note):
    name = note[:-1]
    octave = int(note[-1])
    return 12 * (octave + 1) + NOTE_TO_MIDI[name]


def find_all_frets(note):
    midi = note_name_to_midi(note)
    options = []
    for string, (_, base_midi) in STANDARD_TUNING.items():
        fret = midi - base_midi
        if 0 <= fret <= 20:
            options.append((string, fret))
    return options


def movement_penalty(last_string, last_fret, string, fret):
    # No penalty if going between a fret and open string on the same string
    if last_string == string and (last_fret == 0 or fret == 0):
        fret_cost = 0
    else:
        fret_diff = abs(fret - last_fret)
        if fret_diff <= 1:
            fret_cost = 0
        elif fret_diff == 2:
            fret_cost = 0.5
        elif fret_diff == 3:
            fret_cost = 1
        else:
            fret_cost = 1 + ((fret_diff - 3) ** 2) * 0.5  # Quadratic growth

    string_diff = abs(string - last_string)
    string_cost = 0.5 * string_diff  # Linear string switch cost

    return fret_cost + string_cost



def select_best_path(note_sequence):
    import statistics
    paths = [[option] for option in find_all_frets(note_sequence[0][2])]

    for idx in range(1, len(note_sequence)):
        next_note = note_sequence[idx][2]
        next_options = find_all_frets(next_note)
        new_paths = []

        for path in paths:
            last_string, last_fret = path[-1][:2]
            for option in next_options:
                string, fret = option
                cost = movement_penalty(last_string, last_fret, string, fret)
                new_paths.append(path + [(string, fret, cost)])

        # Keep best path per option
        paths = []
        for option in next_options:
            best = None
            best_score = float('inf')
            for p in new_paths:
                if p[-1][:2] == option:
                    total_cost = sum(step[2] for step in p if len(step) == 3)
                    frets = [step[1] for step in p]
                    avg_fret = sum(frets) / len(frets)
                    fret_std = np.std([step[1] for step in path])
                    total_cost += fret_std * 2  # increase multiplier as needed

                    if total_cost < best_score:
                        best = p
                        best_score = total_cost

            if best:
                paths.append(best)

    best_path = min(paths, key=lambda p: (
        sum(step[2] for step in p if len(step) == 3) +
        (statistics.stdev([step[1] for step in p]) if len(p) > 1 else 0)
    ))
    return [step[:2] for step in best_path]


def generate_tabs(filtered_notes):
    print("\nText-Based Tab Notation:")
    best_path = select_best_path(filtered_notes)
    for (start, end, note, conf), (string, fret) in zip(filtered_notes, best_path):
        print(f"{start:.2f}s: {note} → String {string}, Fret {fret}")

    # Build tab lines
    tab_lines = {i: [] for i in range(1, 7)}
    for (_, _, note, _), (string, fret) in zip(filtered_notes, best_path):
        for i in range(1, 7):
            if i == string:
                tab_lines[i].append(f"{fret:>2}")
            else:
                tab_lines[i].append("--")

    # Normalize line lengths
    max_len = max(len(v) for v in tab_lines.values())
    for i in range(1, 7):
        tab_lines[i] += ["--"] * (max_len - len(tab_lines[i]))

    # Print in wrapped blocks
    MAX_COLUMNS = 25
    string_labels = {1: 'E', 2: 'B', 3: 'G', 4: 'D', 5: 'A', 6: 'E'}

    print("\nReadable Tab Output:")
    for chunk_start in range(0, max_len, MAX_COLUMNS):
        chunk_end = chunk_start + MAX_COLUMNS
        for i in range(1, 7):
            line = f"{string_labels[i]} | " + ' '.join(tab_lines[i][chunk_start:chunk_end])
            print(line)
        print()
