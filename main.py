import os
import librosa
import crepe
from utils.pitch_detection_crepe import extract_notes_crepe
from utils.tab_generator import generate_tabs
import numpy as np

print("Autotab is running. Type 'exit' to quit.")

while True:
    filename = input("Enter audio file name (without or with extension), or type 'exit' to quit: ").strip()
    if filename.lower() == 'exit':
        break

    # Try extensions if none provided
    base = os.path.splitext(filename)[0]
    possible_extensions = ['', '.wav', '.m4a', '.mp3']
    filepath = None
    for ext in possible_extensions:
        test_path = f'samples/{base}{ext}'
        if os.path.exists(test_path):
            filepath = test_path
            break

    if not filepath:
        print(f"❌ File '{filename}' not found in 'samples/'")
        continue

    try:
        y, sr = librosa.load(filepath, sr=16000)
        print(f"Audio duration: {len(y) / sr:.2f} seconds")
        print("Audio loaded at 16000 Hz\n")

        # Run CREPE
        times, freqs, confidences, _ = crepe.predict(y, sr, step_size=10, center=False, viterbi=True)

        print(f"CREPE sample output:")
        print(f"  First 5 times: {times[:5]}")
        print(f"  First 5 freqs: {freqs[:5]}")
        print(f"  First 5 confs: {confidences[:5]}")
        print(f"  Max conf: {max(confidences):.2f}, Min conf: {min(confidences):.2f}")



        # Pass results to note extractor
        filtered_notes = extract_notes_crepe(times, freqs, confidences)

        # Print results
       # print("\nFiltered stable notes:")
        #for start, end, note, conf in filtered_notes:
         #   print(f"{start:.2f}s to {end:.2f}s: {note} ({conf}%)")

        if not filtered_notes:
            print("⚠️ No stable notes detected — try adjusting thresholds or check input quality.")

        generate_tabs(filtered_notes)



    except Exception as e:
        print(f"❌ Failed to load '{filename}': {e}")
