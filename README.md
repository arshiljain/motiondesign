# Ash — Interaction & Experimental Systems

Portfolio of Ash, Interaction Designer & Creative Technologist. An infinite spatial canvas featuring 28 tactile design experiments, micro-instruments, physical interactions, and generative systems.

## ✨ Features

- **Infinite Canvas & Physics**: Fluid pan, pinch, drag navigation, and optical lens boundary distortion shaders.
- **Embedded Audio Engine**: Web Audio API harp synthesizer responding to pointer proximity and gestures.
- **28 Interactive Case Studies**: Detailed modal sheets, typography specifications, kinematic previews, and toolchains.
- **Rich Media**: High-definition video screen recordings and poster frames for every study.
- **Search & Categorization**: Multi-tier instant search and Roman-numeral category filter dock.
- **Glassmorphism Interface**: Responsive bottom floating dock, custom vector typography, and dark/light adaptive assets.

---

## 🚀 How to Run

Because modern browsers enforce security policies on `fetch()` from `file://` protocol, serve the project over HTTP:

### Option 1: Python Server (Recommended)
Includes static file serving with correct MIME types and native `/api/search` routing:
```bash
python server.py
```
Open in browser: **[http://localhost:3000](http://localhost:3000)**

### Option 2: Node / NPM
```bash
npm start
# or
npx serve .
```

---

## 📁 Project Structure

```text
├── index.html              # Main HTML, CSS, interactive canvas engine, and Web Audio harp
├── projects.json           # All 28 project definitions and metadata
├── server.py               # Local server with static serving & search API handling
├── package.json            # NPM configuration and scripts
├── apple-touch-icon.png    # Apple touch icon
├── favicon.svg             # Clean vector favicon
├── favicon-32.png          # 32x32 light favicon
├── favicon-32-dark.png     # 32x32 dark favicon
└── images/                 # Complete media assets
    ├── 01.jpg .. 28.jpg    # Project preview posters
    └── 01.mp4 .. 28.mp4    # Project screen recordings
```
