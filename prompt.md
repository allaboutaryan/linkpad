# Prompt

Build a complete project called **LinkPad**, a lightweight realtime collaborative notes app for small groups. The app should let a user enter their name, create a short room code, share that room code with others, and edit one shared note together in real time. It should work without user accounts, without a database, and without any external AI or third-party API dependency beyond normal npm packages.

The solution must include a React + Vite frontend, a Node.js + Express backend, Socket.IO realtime communication, and an optional Electron desktop wrapper for local LAN hosting. The frontend should have a simple home screen where users can create or join a room, and an editor screen where users can see the room code, connected participants, typing status, invite link, QR code, and the shared note area. The backend should manage rooms in memory, create readable 4-character room codes, sync note updates, broadcast participant lists, show typing users, expose a `/health` endpoint, expose `/api/network` for LAN invite links, and remove empty rooms after a delay.

Keep the implementation practical and focused. Do not add authentication, persistent database storage, chat history, payments, dashboards, or unrelated features. The main goal is quick temporary collaboration for classrooms, workshops, meetings, study groups, and same-WiFi sessions. The UI should feel clean, dark, responsive, and usable on laptops and phones, with clear error messages when a socket disconnects or a room code is invalid.

Use these constraints while writing the code:

- **Clarity:** Name files, functions, events, and states in a way that makes the room flow easy to understand.
- **Completeness:** Include all files needed to run the client, server, PWA shell, Electron wrapper, and deployment setup.
- **Adherence:** Stay within the local-first realtime notes idea and avoid adding unrelated product scope.
- **Efficiency:** Use in-memory room state, concise Socket.IO events, and normal Vite/React build commands.
- **Repetitiveness:** Avoid circular explanations and duplicate code paths where a helper function can keep behavior simple.
- **Human likeness:** Write user-facing text like a real small product, not like a generated demo.
- **Accuracy:** Make sure the commands, dependencies, ports, file paths, and event names match the actual code.

The final repository should be easy to run with `npm run install:all`, `npm run build`, and `npm start`. It should also include clear README documentation for local development, LAN usage, Render deployment, and the difference between online hosting and offline LAN mode.
