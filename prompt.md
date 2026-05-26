# Prompt

## Context and Role

As a Full-Stack JavaScript Developer specializing in realtime collaborative web applications, you are responsible for designing and implementing a complete production-ready project named **LinkPad**. LinkPad must be a lightweight realtime collaborative notes application where users can quickly create or join a temporary shared room and type together live without accounts, passwords, databases, or complicated setup.

The application should be built for real-world short-session collaboration such as classrooms, college study groups, workshops, meetings, orientations, hackathons, clubs, and small team discussions. The experience should feel simple, useful, and direct: a user enters their name, creates or joins a room with a short code, shares the code or invite link, and everyone in the room edits one shared note in real time.

The final solution must include a complete frontend, backend, PWA shell, optional desktop wrapper, deployment configuration, and clear documentation. The codebase should be easy to run, easy to inspect, and suitable for submission as a full project.

## Objective

Develop a complete full-stack realtime collaborative notes application that:

- Allows users to enter a display name before joining.
- Allows users to create a temporary shared room.
- Generates a short readable room code for each room.
- Allows other users to join using the room code.
- Synchronizes one shared note live between all users in a room.
- Shows connected user count and participant indicators.
- Shows who is currently typing.
- Provides an invite link and QR code for same-WiFi phone/laptop joining.
- Works locally on one machine and across devices on the same WiFi or hotspot.
- Can also be deployed as a public Node.js web app.
- Includes an optional Electron desktop wrapper for local LAN hosting.
- Avoids authentication, permanent database storage, dashboards, payments, and unrelated features.

## Product Scope Requirements

LinkPad must focus on temporary realtime writing sessions.

The application must include:

- A landing/home screen for creating or joining a session.
- A room/editor screen for shared note collaboration.
- Realtime note updates using Socket.IO.
- Realtime participant presence.
- Realtime typing indicators.
- A LAN invite link generated from the host machine network address.
- A QR code for quick joining from phones.
- Helpful connection and error states.
- README documentation explaining setup, local usage, LAN usage, and deployment.

The application must not include:

- User accounts or login.
- Password-protected rooms.
- Persistent database storage for notes.
- Rich text editing.
- Chat messages.
- File uploads.
- Project dashboards.
- Payment features.
- Admin panels.
- AI features.
- Any external API dependency beyond normal npm packages.

## Technology Stack

Use the following:

### Frontend

- React
- Vite
- Tailwind CSS
- Socket.IO Client
- QR code generation package
- Service worker and web manifest for a small PWA shell

### Backend

- Node.js
- Express
- Socket.IO
- CORS
- In-memory room storage
- Environment variable support for port and client origin

### Desktop Wrapper

- Electron
- Electron Builder for Windows installer configuration

### Deployment

- Render-compatible configuration
- Root-level scripts for install, build, start, desktop mode, and render build

## UI Requirements

The UI must be modern, clean, responsive, and practical.

The application must include:

- A dark visual theme with readable contrast.
- Clear app branding for LinkPad.
- A responsive layout for mobile, tablet, and desktop.
- Accessible labels for form fields.
- Semantic HTML where appropriate.
- Buttons with disabled states while actions are unavailable.
- Error messages that are understandable to normal users.
- Controls that remain usable on small screens.

The UI should not feel like a generic generated demo. It should feel like a small real product that someone could use in a classroom, study session, or workshop.

## Home Screen Requirements

The home screen must include:

- LinkPad name or logo.
- A short product description.
- Socket connection status.
- Name input field.
- Create Session button.
- Join Session room-code input.
- Join Session button.
- Error message area.

The name input must:

- Be required before creating or joining a room.
- Trim unnecessary whitespace.
- Limit the display name length.
- Allow normal human names.

The room-code input must:

- Accept only alphanumeric characters.
- Convert letters to uppercase.
- Limit room code length to four characters.
- Pre-fill from the `room` query parameter if present in the URL.
- Show a helpful validation error if the room code is invalid.

## Editor Screen Requirements

The editor screen must include:

- LinkPad branding.
- Current room code.
- Copy Room Code button.
- Connected/disconnected status.
- Online user count.
- Participant dots or participant labels.
- Invite panel.
- LAN invite link.
- Copy invite link button.
- QR code for the invite link.
- Typing indicator.
- Leave button.
- Large shared textarea.

The shared textarea must:

- Update local state immediately when the user types.
- Emit note updates to the server.
- Receive note updates from other users.
- Keep the writing area large and comfortable.
- Support browser spellcheck.

## Realtime Collaboration Requirements

Implement realtime communication using Socket.IO.

The client must emit and handle events for:

- Creating rooms.
- Joining rooms.
- Updating notes.
- Receiving note syncs.
- Updating typing status.
- Receiving typing users.
- Receiving room user lists.
- Handling socket connect and disconnect states.

The backend must manage Socket.IO rooms so that updates are scoped only to the correct room. A user typing in one room must never update another room.

## Backend API Requirements

The backend must run on port `4000` by default.

The backend must listen on:

```text
0.0.0.0
```

This is required so other devices on the same local network can connect.

The backend must expose:

### `GET /health`

Returns structured JSON containing:

- `ok: true`
- App name
- Current room count

### `GET /api/network`

Returns structured JSON containing:

- Server port
- Localhost URL
- LAN URLs for non-internal IPv4 addresses

This endpoint is required so the frontend can generate useful same-WiFi invite links.

## Socket Event Requirements

Implement the following server-side Socket.IO events:

### `create-room`

When triggered:

- Sanitize the submitted display name.
- Generate a unique four-character room code.
- Create a new in-memory room.
- Add the current socket as a room participant.
- Return the room code, empty note, current user, users list, and user count.

### `join-room`

When triggered:

- Normalize the room code.
- Sanitize the submitted display name.
- Check whether the room exists.
- Return a structured error if the room does not exist.
- Join the socket to the room if it exists.
- Return the current note, current user, users list, and user count.

### `note-update`

When triggered:

- Confirm the socket belongs to the submitted room.
- Sanitize the note value as a string.
- Update the room's in-memory note.
- Broadcast the note to every other socket in that room.

### `typing-update`

When triggered:

- Confirm the socket belongs to the submitted room.
- Add or remove the socket from the room typing set.
- Broadcast the updated typing users list.

### `disconnect`

When triggered:

- Remove the socket from its current room.
- Remove the socket from the typing set.
- Update the participant list.
- Schedule room cleanup if the room becomes empty.

## Room Management Requirements

Room data must be stored in memory.

Each room must store:

- Current note text.
- Connected users map.
- Typing users set.
- Empty-room cleanup timer.

Room codes must:

- Be exactly four characters long.
- Use uppercase readable characters.
- Avoid confusing characters where reasonable.
- Be unique among active rooms.

Empty rooms must:

- Not remain forever.
- Be removed after a reasonable delay.
- Cancel cleanup if a user rejoins before the cleanup timer finishes.

## User Data Requirements

Each user object should include:

- Socket ID.
- Display name.
- Assigned color.

Display names must:

- Be trimmed.
- Collapse repeated whitespace.
- Be limited to a safe length.
- Fall back to a guest name if blank.

User colors must:

- Come from a small readable color palette.
- Prefer unused colors in the room.
- Reuse colors only when needed.

## Error Handling Requirements

The frontend must handle:

- Socket disconnected state.
- Server timeout during create room.
- Server timeout during join room.
- Invalid room code length.
- Room not found.
- Failed reconnect/rejoin attempt.

The backend must handle:

- Missing or invalid payload values.
- Attempts to update rooms the socket has not joined.
- Unknown room codes.
- Socket disconnects.
- Empty-room cleanup.

All errors returned to the client must be structured and user-friendly.

## Reconnection Requirements

The client must track the latest joined room code and display name.

If the socket reconnects after a disconnect:

- Attempt to rejoin the last active room.
- Restore the current user.
- Restore the note.
- Restore the users list.
- Restore the online count.
- Show a useful error if rejoining fails.

## Typing Indicator Requirements

Typing indicators must:

- Emit when the local user types.
- Stop after a short delay when typing pauses.
- Avoid showing the current user as typing to themselves.
- Support one or more users typing.
- Use concise human text.

Example messages:

```text
Arya is typing...
Arya, Neha are typing...
Arya, Neha +1 are typing...
```

## Invite Link and QR Requirements

The editor screen must show an invite panel.

The invite panel must:

- Fetch `/api/network`.
- Prefer a LAN URL if available.
- Fall back to the current browser origin.
- Add the room code as a query parameter.
- Show the generated invite link.
- Provide a copy invite link button.
- Generate a QR code for the invite link.

Example invite link:

```text
http://192.168.0.100:4000?room=ABCD
```

## PWA Requirements

Include a lightweight PWA shell.

The project must include:

- `manifest.webmanifest`
- SVG app icon
- Service worker
- Service worker registration in the frontend entry file

The service worker must:

- Cache basic app shell files.
- Clean old caches during activation.
- Avoid caching Socket.IO requests.
- Provide a navigation fallback to `/` when appropriate.

The documentation must clearly explain that the PWA shell does not make live collaboration work without the server.

## Electron Requirements

Include an optional Electron desktop wrapper.

The Electron app must:

- Start the production Node server.
- Wait for `/health` to respond.
- Open `http://localhost:4000`.
- Use a secure BrowserWindow configuration.
- Enable context isolation.
- Disable node integration.
- Open external links in the system browser.
- Show an error dialog if the server fails to start.

The root package must include:

- `desktop` script
- `desktop:dist` script
- Electron Builder configuration

## Folder Structure Requirements

The final project must contain:

```text
client/
client/public/
client/src/
client/src/components/
client/src/lib/
client/src/pages/
server/
server/src/
electron/
docs/
README.md
package.json
package-lock.json
render.yaml
.gitignore
```

The important source files must include:

```text
client/src/App.jsx
client/src/main.jsx
client/src/styles.css
client/src/lib/socket.js
client/src/pages/HomePage.jsx
client/src/pages/EditorPage.jsx
client/src/components/InvitePanel.jsx
client/src/components/ParticipantDots.jsx
client/src/components/StatusPill.jsx
client/src/components/TypingIndicator.jsx
server/src/index.js
electron/main.cjs
docs/OFFLINE_LAN_ARCHITECTURE.md
```

## README Documentation Requirements

The README must document:

- Project overview.
- Why LinkPad exists.
- Feature list.
- Tech stack.
- Folder structure.
- Local installation.
- Build command.
- Start command.
- Development mode.
- Same-WiFi usage.
- Desktop host app usage.
- Render deployment steps.
- Difference between Render mode and Offline LAN mode.
- Production limitations.
- Future improvement ideas.

The README must include these commands:

```bash
npm run install:all
npm run build
npm start
```

The README must explain that GitHub Pages is not enough because this project requires a Node.js Socket.IO server.

## Performance Requirements

The application must:

- Keep the frontend bundle reasonable.
- Avoid unnecessary dependencies.
- Use simple React state instead of heavy state libraries.
- Avoid expensive re-renders where possible.
- Use timeout-based typing updates instead of emitting excessive status changes.
- Use Socket.IO rooms to avoid broadcasting to unrelated users.
- Clean up socket listeners when React components unmount.
- Clean up empty rooms on the backend.

## Accessibility Requirements

The application must:

- Use semantic HTML where practical.
- Provide labels for inputs.
- Use readable text contrast.
- Keep buttons keyboard-accessible.
- Avoid hiding critical information only in color.
- Use useful alt text for the QR code image.
- Keep form interactions understandable on mobile and desktop.

## Security and Data Handling Requirements

The project does not require login or permanent storage, but it must still handle user input carefully.

The backend must:

- Sanitize display names.
- Normalize room codes.
- Accept note values safely as strings.
- Ignore room updates from sockets that are not in the room.
- Avoid exposing unnecessary server data.

The frontend must:

- Limit display-name length.
- Limit room-code input length.
- Avoid rendering unsafe HTML from users.
- Treat notes as plain text inside a textarea.

## Deployment Requirements

Include a `render.yaml` file suitable for Render deployment.

Render configuration must include:

- Node environment.
- Free plan compatibility.
- Build command.
- Start command.
- Auto deploy enabled.

The root package must include:

```bash
npm run render-build
```

This command must install dependencies for the server and client, then build the frontend.

## Output Requirements

The final output must be a complete runnable LinkPad project.

After setup, the reviewer must be able to:

- Install dependencies.
- Build the client.
- Start the server.
- Open the app at `http://localhost:4000`.
- Create a room.
- Join the room from another browser tab or device.
- Type in the shared note.
- See realtime note updates.
- See connected participants.
- See typing indicators.
- Copy the room code.
- Use the invite link.
- Scan the QR code.
- Understand local, LAN, desktop, and Render usage from the README.

