# LinkPad Prompt Submission

This repository is arranged for the project submission format. The four main files are:

- `prompt.md` - the final coding prompt written around the seven prompt-quality dimensions.
- `justification.md` - a short human-written explanation of why the prompt is strong.
- `golden_response.py` - the expected LinkPad codebase collected into one runnable Python file.
- `README.md` - this overview file.

## Project Idea

LinkPad is a small realtime collaborative notes app. A user enters their name, creates or joins a short room code, and writes in one shared note with everyone in the same room. It is meant for quick group work in classes, meetings, workshops, study groups, and same-WiFi sessions.

The app uses React, Vite, TailwindCSS, Node.js, Express, Socket.IO, and an optional Electron wrapper. It intentionally avoids login, permanent storage, databases, and extra product features because the goal is fast temporary collaboration.

## How To Read The Submission

Start with `prompt.md` to see the exact instruction used for the coding task. Then read `justification.md` for the reasoning behind the prompt. The full expected code is inside `golden_response.py` as a `FILES` dictionary, and it can recreate the project files if needed.

## Restore The Golden Code

```bash
python golden_response.py restored_linkpad
```

That command writes the stored code files into a folder named `restored_linkpad`.

## Run The Restored App

After restoring the files, run:

```bash
cd restored_linkpad
npm run install:all
npm run build
npm start
```

Then open:

```text
http://localhost:4000
```

For development, the backend can run on port `4000` and the Vite client on port `5173`.
