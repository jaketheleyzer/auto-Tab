# AutoTab

**AutoTab** is an AI-powered tool that listens to monophonic guitar audio and generates optimized tablature in standard tuning (EADGBE).

### Features
- 🎸 Converts audio into guitar tabs
- 🧠 Uses CREPE for pitch detection
- 🎯 Smart fret/string selection to minimize hand movement
- 📉 Penalizes high fret deviation and awkward jumps
- 🔁 Outputs readable and text-based tablature

### How It Works
1. Load `.wav`, `.mp3`, or `.m4a` files into the `/samples` folder.
2. Run the program: `python main.py`
3. Choose a file and let AutoTab analyze it.
4. View suggested fret positions and generated tabs.

### Requirements
- Python 3.10+
- `librosa`, `crepe`, `tensorflow`, `numpy`

### Coming Soon
- Polyphonic support
- Export tabs to Guitar Pro or PDF
- Real-time input

---

### 📦 2. Create a `requirements.txt`

You can generate it with:

```bash
pip freeze > requirements.txt
