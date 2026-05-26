"""
Golden response for the LinkPad project.

This file keeps the important project code in one place so a checker or reviewer
can inspect the expected implementation without opening every folder manually.
Run it with Python if you want to recreate the code files into an output folder:

    python golden_response.py restored_linkpad
"""

from pathlib import Path
import sys


FILES = {
    "package.json": r'''{
  "name": "linkpad",
  "version": "0.1.0",
  "private": true,
  "description": "Local-first realtime collaborative notes with room codes, participant dots, and typing indicators.",
  "scripts": {
    "install:all": "npm install --prefix server && npm install --prefix client",
    "build": "npm run build --prefix client",
    "dev:server": "npm run dev --prefix server",
    "dev:client": "npm run dev --prefix client -- --host 0.0.0.0",
    "desktop": "npm run build && electron .",
    "desktop:dist": "npm run build && electron-builder --win nsis",
    "start": "npm start --prefix server",
    "render-build": "npm run install:all && npm run build"
  },
  "main": "electron/main.cjs",
  "build": {
    "appId": "com.linkpad.local",
    "productName": "LinkPad",
    "files": [
      "electron/**/*",
      "server/**/*",
      "client/dist/**/*",
      "package.json"
    ],
    "directories": {
      "output": "release"
    },
    "win": {
      "signAndEditExecutable": false
    }
  },
  "engines": {
    "node": ">=20"
  },
  "devDependencies": {
    "electron": "^42.2.0",
    "electron-builder": "^26.8.1"
  }
}
''',
    "render.yaml": r'''services:
  - type: web
    name: linkpad
    env: node
    plan: free
    buildCommand: npm run render-build
    startCommand: npm start
    autoDeploy: true
''',
    "client/package.json": r'''{
  "name": "linkpad-client",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview --host 0.0.0.0"
  },
  "dependencies": {
    "@vitejs/plugin-react": "^4.3.1",
    "qrcode": "^1.5.4",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "socket.io-client": "^4.7.5",
    "vite": "^5.3.4"
  },
  "devDependencies": {
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.39",
    "tailwindcss": "^3.4.6"
  }
}
''',
    "client/index.html": r'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#09090b" />
    <link rel="manifest" href="/manifest.webmanifest" />
    <title>LinkPad</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
''',
    "client/vite.config.js": r'''import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173
  }
});
''',
    "client/postcss.config.js": r'''export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {}
  }
};
''',
    "client/tailwind.config.js": r'''/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"]
      }
    }
  },
  plugins: []
};
''',
    "client/public/manifest.webmanifest": r'''{
  "name": "LinkPad",
  "short_name": "LinkPad",
  "description": "Realtime collaborative notes for local networks and lightweight remote sessions.",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "background_color": "#09090b",
  "theme_color": "#09090b",
  "icons": [
    {
      "src": "/icon.svg",
      "sizes": "any",
      "type": "image/svg+xml",
      "purpose": "any maskable"
    }
  ]
}
''',
    "client/public/icon.svg": r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="96" fill="#09090b"/>
  <rect x="96" y="96" width="320" height="320" rx="48" fill="#0e7490" opacity="0.28"/>
  <path d="M164 143h58v184h126v43H164V143z" fill="#67e8f9"/>
</svg>
''',
    "client/public/sw.js": r'''const CACHE_NAME = "linkpad-shell-v1";
const APP_SHELL = ["/", "/manifest.webmanifest", "/icon.svg"];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key)))
      )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const request = event.request;

  if (request.method !== "GET") {
    return;
  }

  const url = new URL(request.url);

  if (url.pathname.startsWith("/socket.io")) {
    return;
  }

  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request).catch(() => caches.match("/"))
    );
    return;
  }

  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }

      return fetch(request).then((networkResponse) => {
        if (url.origin === self.location.origin && networkResponse.ok) {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, responseClone));
        }

        return networkResponse;
      });
    })
  );
});
''',
    "client/src/main.jsx": r'''import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./styles.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch(() => {
      // LinkPad still works without the service worker.
    });
  });
}
''',
    "client/src/styles.css": r'''@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  color-scheme: dark;
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
  background: #09090b;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-width: 320px;
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(103, 232, 249, 0.12), transparent 30rem),
    #09090b;
}

button,
input,
textarea {
  font: inherit;
}

textarea::selection,
input::selection {
  background: rgba(103, 232, 249, 0.35);
}
''',
    "client/src/lib/socket.js": r'''import { io } from "socket.io-client";

const isViteDevServer = window.location.port === "5173";
const serverUrl =
  import.meta.env.VITE_SOCKET_URL ||
  (isViteDevServer
    ? `${window.location.protocol}//${window.location.hostname}:4000`
    : window.location.origin);

export const socket = io(serverUrl, {
  autoConnect: true,
  transports: ["websocket", "polling"]
});
''',
    "client/src/App.jsx": r'''import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { socket } from "./lib/socket.js";
import HomePage from "./pages/HomePage.jsx";
import EditorPage from "./pages/EditorPage.jsx";

const INITIAL_STATUS = socket.connected ? "connected" : "disconnected";
const TYPING_STOP_DELAY = 1200;
const REQUEST_TIMEOUT = 8000;

export default function App() {
  const [view, setView] = useState("home");
  const [roomCode, setRoomCode] = useState("");
  const [note, setNote] = useState("");
  const [usersCount, setUsersCount] = useState(0);
  const [users, setUsers] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const [typingUsers, setTypingUsers] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState(INITIAL_STATUS);
  const [error, setError] = useState("");
  const [isBusy, setIsBusy] = useState(false);
  const latestRoomCode = useRef("");
  const currentUserRef = useRef(null);
  const displayNameRef = useRef("");
  const typingTimeoutRef = useRef(null);

  useEffect(() => {
    function handleConnect() {
      setConnectionStatus("connected");

      if (!latestRoomCode.current || !displayNameRef.current) {
        return;
      }

      socket.timeout(REQUEST_TIMEOUT).emit(
        "join-room",
        { roomCode: latestRoomCode.current, name: displayNameRef.current },
        (requestError, response) => {
          if (requestError || !response?.ok) {
            setError("Reconnected, but could not rejoin the room. Create a new room if needed.");
            return;
          }

          currentUserRef.current = response.currentUser;
          setCurrentUser(response.currentUser);
          setNote(response.note);
          setUsers(response.users || []);
          setUsersCount(response.usersCount);
        }
      );
    }

    function handleDisconnect() {
      setConnectionStatus("disconnected");
    }

    function handleNoteSync(payload) {
      if (payload.roomCode !== latestRoomCode.current) {
        return;
      }

      setNote(payload.note);
    }

    function handleRoomUsers(payload) {
      if (payload.roomCode !== latestRoomCode.current) {
        return;
      }

      setUsers(payload.users || []);
      setUsersCount(payload.usersCount);
    }

    function handleTypingUsers(payload) {
      if (payload.roomCode !== latestRoomCode.current) {
        return;
      }

      setTypingUsers(
        (payload.users || []).filter((user) => user.id !== currentUserRef.current?.id)
      );
    }

    socket.on("connect", handleConnect);
    socket.on("disconnect", handleDisconnect);
    socket.on("note-sync", handleNoteSync);
    socket.on("room-users", handleRoomUsers);
    socket.on("typing-users", handleTypingUsers);

    return () => {
      window.clearTimeout(typingTimeoutRef.current);
      socket.off("connect", handleConnect);
      socket.off("disconnect", handleDisconnect);
      socket.off("note-sync", handleNoteSync);
      socket.off("room-users", handleRoomUsers);
      socket.off("typing-users", handleTypingUsers);
    };
  }, []);

  const createSession = useCallback((name) => {
    setError("");
    setIsBusy(true);
    displayNameRef.current = name;

    if (!socket.connected) {
      setIsBusy(false);
      setError("Socket is disconnected. Refresh the page and try again.");
      return;
    }

    socket.timeout(REQUEST_TIMEOUT).emit("create-room", { name }, (requestError, response) => {
      setIsBusy(false);

      if (requestError) {
        setError("Server did not respond. Wait a few seconds and try again.");
        return;
      }

      if (!response?.ok) {
        setError(response?.error || "Could not create a room.");
        return;
      }

      latestRoomCode.current = response.roomCode;
      currentUserRef.current = response.currentUser;
      setRoomCode(response.roomCode);
      setNote(response.note);
      setCurrentUser(response.currentUser);
      setUsers(response.users || []);
      setUsersCount(response.usersCount);
      setView("editor");
    });
  }, []);

  const joinSession = useCallback((requestedRoomCode, name) => {
    setError("");
    const cleanRoomCode = requestedRoomCode.trim().toUpperCase();

    if (cleanRoomCode.length !== 4) {
      setError("Room code must be exactly 4 characters.");
      return;
    }

    setIsBusy(true);
    displayNameRef.current = name;

    if (!socket.connected) {
      setIsBusy(false);
      setError("Socket is disconnected. Refresh the page and try again.");
      return;
    }

    socket.timeout(REQUEST_TIMEOUT).emit(
      "join-room",
      { roomCode: cleanRoomCode, name },
      (requestError, response) => {
        setIsBusy(false);

        if (requestError) {
          setError("Server did not respond. Check the room code and try again.");
          return;
        }

        if (!response?.ok) {
          setError(response?.error || "Could not join that room.");
          return;
        }

        latestRoomCode.current = response.roomCode;
        currentUserRef.current = response.currentUser;
        setRoomCode(response.roomCode);
        setNote(response.note);
        setCurrentUser(response.currentUser);
        setUsers(response.users || []);
        setUsersCount(response.usersCount);
        setView("editor");
      }
    );
  }, []);

  const updateNote = useCallback(
    (nextNote) => {
      setNote(nextNote);

      if (!roomCode) {
        return;
      }

      socket.emit("note-update", {
        roomCode,
        note: nextNote
      });

      socket.emit("typing-update", {
        roomCode,
        isTyping: true
      });

      window.clearTimeout(typingTimeoutRef.current);
      typingTimeoutRef.current = window.setTimeout(() => {
        socket.emit("typing-update", {
          roomCode,
          isTyping: false
        });
      }, TYPING_STOP_DELAY);
    },
    [roomCode]
  );

  const leaveRoom = useCallback(() => {
    window.location.reload();
  }, []);

  const appState = useMemo(
    () => ({
      roomCode,
      note,
      users,
      currentUser,
      typingUsers,
      usersCount,
      connectionStatus,
      error,
      isBusy
    }),
    [roomCode, note, users, currentUser, typingUsers, usersCount, connectionStatus, error, isBusy]
  );

  if (view === "editor") {
    return (
      <EditorPage
        state={appState}
        onNoteChange={updateNote}
        onLeaveRoom={leaveRoom}
      />
    );
  }

  return (
    <HomePage
      state={appState}
      onCreateSession={createSession}
      onJoinSession={joinSession}
    />
  );
}
''',
    "client/src/pages/HomePage.jsx": r'''import { useState } from "react";
import StatusPill from "../components/StatusPill.jsx";

export default function HomePage({ state, onCreateSession, onJoinSession }) {
  const [name, setName] = useState("");
  const [roomCode, setRoomCode] = useState(() => {
    const params = new URLSearchParams(window.location.search);
    return (params.get("room") || "").replace(/[^a-z0-9]/gi, "").toUpperCase().slice(0, 4);
  });
  const hasName = name.trim().length > 0;
  const cleanRoomCode = roomCode.trim().toUpperCase();
  const canCreate = hasName && !state.isBusy;
  const canJoin = hasName && cleanRoomCode.length > 0 && !state.isBusy;

  function handleSubmit(event) {
    event.preventDefault();

    if (!canJoin) {
      return;
    }

    onJoinSession(cleanRoomCode, name);
  }

  function handleCreateSession() {
    if (!canCreate) {
      return;
    }

    onCreateSession(name);
  }

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-50">
      <section className="mx-auto flex min-h-screen w-full max-w-5xl flex-col px-5 py-6 sm:px-8">
        <header className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-lg border border-cyan-300/25 bg-cyan-300/10 text-lg font-semibold text-cyan-200">
              L
            </div>
            <div>
              <h1 className="text-xl font-semibold tracking-normal">LinkPad</h1>
              <p className="text-sm text-zinc-400">Local realtime notes</p>
            </div>
          </div>
          <StatusPill status={state.connectionStatus} />
        </header>

        <div className="flex flex-1 items-center py-12">
          <div className="grid w-full gap-8 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
            <div className="max-w-2xl">
              <p className="mb-4 text-sm font-medium uppercase text-cyan-200">
                Same WiFi. Shared note. No sign-in.
              </p>
              <h2 className="text-4xl font-semibold tracking-normal text-white sm:text-6xl">
                Start a live note in seconds.
              </h2>
              <p className="mt-5 max-w-xl text-lg leading-8 text-zinc-300">
                Create a room, share the code, and everyone nearby can type together instantly over the local network.
              </p>
            </div>

            <div className="rounded-lg border border-zinc-800 bg-zinc-900/80 p-5 shadow-2xl shadow-cyan-950/20">
              <div className="mb-4 space-y-2">
                <label className="block text-sm font-medium text-zinc-300" htmlFor="name">
                  Your name
                </label>
                <input
                  id="name"
                  value={name}
                  onChange={(event) => setName(event.target.value)}
                  maxLength={24}
                  placeholder="Arya"
                  className="h-12 w-full rounded-md border border-zinc-700 bg-zinc-950 px-4 text-base text-white outline-none transition placeholder:text-zinc-700 focus:border-cyan-300"
                />
              </div>

              <button
                type="button"
                onClick={handleCreateSession}
                disabled={!canCreate}
                className="h-12 w-full rounded-md bg-cyan-300 px-4 text-sm font-semibold text-zinc-950 transition hover:bg-cyan-200 focus:outline-none focus:ring-2 focus:ring-cyan-200 focus:ring-offset-2 focus:ring-offset-zinc-950 disabled:cursor-not-allowed disabled:opacity-40"
              >
                {state.isBusy ? "Please wait..." : "Create Session"}
              </button>

              <div className="my-5 flex items-center gap-3 text-xs uppercase text-zinc-500">
                <div className="h-px flex-1 bg-zinc-800" />
                or join
                <div className="h-px flex-1 bg-zinc-800" />
              </div>

              <form onSubmit={handleSubmit} className="space-y-3">
                <label className="block text-sm font-medium text-zinc-300" htmlFor="roomCode">
                  Room code
                </label>
                <input
                  id="roomCode"
                  value={roomCode}
                  onChange={(event) =>
                    setRoomCode(event.target.value.replace(/[^a-z0-9]/gi, "").toUpperCase())
                  }
                  maxLength={4}
                  placeholder="X7K2"
                  className="h-12 w-full rounded-md border border-zinc-700 bg-zinc-950 px-4 text-center text-xl font-semibold uppercase tracking-[0.25em] text-white outline-none transition placeholder:text-zinc-700 focus:border-cyan-300"
                />
                <button
                  type="submit"
                  disabled={!canJoin}
                  className="h-12 w-full rounded-md border border-zinc-700 px-4 text-sm font-semibold text-zinc-100 transition hover:border-cyan-300 hover:text-cyan-100 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  {state.isBusy ? "Joining..." : "Join Session"}
                </button>
              </form>

              {state.error ? (
                <p className="mt-4 rounded-md border border-red-400/30 bg-red-400/10 px-3 py-2 text-sm text-red-100">
                  {state.error}
                </p>
              ) : null}
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
''',
    "client/src/pages/EditorPage.jsx": r'''import { useState } from "react";
import InvitePanel from "../components/InvitePanel.jsx";
import ParticipantDots from "../components/ParticipantDots.jsx";
import StatusPill from "../components/StatusPill.jsx";
import TypingIndicator from "../components/TypingIndicator.jsx";

export default function EditorPage({ state, onNoteChange, onLeaveRoom }) {
  const [copied, setCopied] = useState(false);

  async function copyRoomCode() {
    await navigator.clipboard.writeText(state.roomCode);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1400);
  }

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-50">
      <section className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-4 py-4 sm:px-6">
        <header className="flex flex-col gap-3 border-b border-zinc-800 pb-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-lg border border-cyan-300/25 bg-cyan-300/10 text-lg font-semibold text-cyan-200">
              L
            </div>
            <div>
              <h1 className="text-lg font-semibold">LinkPad</h1>
              <p className="text-sm text-zinc-400">Room {state.roomCode}</p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <StatusPill status={state.connectionStatus} />
            <ParticipantDots users={state.users} />
            <div className="rounded-md border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm text-zinc-300">
              {state.usersCount} online
            </div>
            <button
              type="button"
              onClick={copyRoomCode}
              className="rounded-md border border-zinc-700 px-3 py-2 text-sm font-medium text-zinc-100 transition hover:border-cyan-300 hover:text-cyan-100"
            >
              {copied ? "Copied" : "Copy Code"}
            </button>
            <button
              type="button"
              onClick={onLeaveRoom}
              className="rounded-md border border-zinc-800 px-3 py-2 text-sm font-medium text-zinc-400 transition hover:border-zinc-600 hover:text-zinc-100"
            >
              Leave
            </button>
          </div>
        </header>

        <div className="flex min-h-0 flex-1 flex-col py-4">
          <InvitePanel roomCode={state.roomCode} />
          <TypingIndicator users={state.typingUsers} />
          <textarea
            value={state.note}
            onChange={(event) => onNoteChange(event.target.value)}
            spellCheck="true"
            placeholder="Start typing. Everyone in this room will see updates live..."
            className="min-h-[70vh] flex-1 resize-none rounded-lg border border-zinc-800 bg-zinc-900/80 p-5 text-base leading-7 text-zinc-100 outline-none transition placeholder:text-zinc-600 focus:border-cyan-300 sm:text-lg"
          />
        </div>
      </section>
    </main>
  );
}
''',
    "client/src/components/InvitePanel.jsx": r'''import { useEffect, useMemo, useState } from "react";
import QRCode from "qrcode";

export default function InvitePanel({ roomCode }) {
  const [networkInfo, setNetworkInfo] = useState(null);
  const [qrCode, setQrCode] = useState("");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    let isMounted = true;

    fetch("/api/network")
      .then((response) => response.json())
      .then((data) => {
        if (isMounted) {
          setNetworkInfo(data);
        }
      })
      .catch(() => {
        if (isMounted) {
          setNetworkInfo(null);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const inviteUrl = useMemo(() => {
    const preferredBaseUrl = networkInfo?.lanUrls?.[0] || window.location.origin;
    return `${preferredBaseUrl}?room=${roomCode}`;
  }, [networkInfo, roomCode]);

  useEffect(() => {
    QRCode.toDataURL(inviteUrl, {
      margin: 1,
      width: 180,
      color: {
        dark: "#09090b",
        light: "#ffffff"
      }
    })
      .then(setQrCode)
      .catch(() => setQrCode(""));
  }, [inviteUrl]);

  async function copyInviteLink() {
    await navigator.clipboard.writeText(inviteUrl);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1400);
  }

  return (
    <div className="mb-4 grid gap-4 rounded-lg border border-cyan-300/20 bg-cyan-300/10 p-4 md:grid-cols-[1fr_auto] md:items-center">
      <div>
        <p className="text-xs font-medium uppercase text-cyan-200">Room Code</p>
        <p className="mt-1 text-3xl font-semibold tracking-[0.25em] text-white">{roomCode}</p>
        <p className="mt-3 break-all text-sm text-zinc-300">{inviteUrl}</p>
        <button
          type="button"
          onClick={copyInviteLink}
          className="mt-3 h-11 rounded-md bg-cyan-300 px-4 text-sm font-semibold text-zinc-950 transition hover:bg-cyan-200"
        >
          {copied ? "Copied" : "Copy Phone Invite Link"}
        </button>
      </div>
      {qrCode ? (
        <img
          src={qrCode}
          alt="Phone invite QR code"
          className="h-36 w-36 rounded-md bg-white p-2"
        />
      ) : null}
    </div>
  );
}
''',
    "client/src/components/ParticipantDots.jsx": r'''export default function ParticipantDots({ users }) {
  if (!users.length) {
    return null;
  }

  return (
    <div className="flex max-w-full flex-wrap items-center gap-2">
      {users.map((user) => (
        <div
          key={user.id}
          className="inline-flex items-center gap-2 rounded-md border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm text-zinc-200"
          title={user.name}
        >
          <span
            className="h-2.5 w-2.5 rounded-full shadow-[0_0_12px_currentColor]"
            style={{ backgroundColor: user.color, color: user.color }}
          />
          <span className="max-w-24 truncate">{user.name}</span>
        </div>
      ))}
    </div>
  );
}
''',
    "client/src/components/StatusPill.jsx": r'''export default function StatusPill({ status }) {
  const isConnected = status === "connected";

  return (
    <div
      className={[
        "inline-flex items-center gap-2 rounded-md border px-3 py-2 text-sm font-medium",
        isConnected
          ? "border-emerald-300/25 bg-emerald-300/10 text-emerald-200"
          : "border-red-300/25 bg-red-300/10 text-red-200"
      ].join(" ")}
    >
      <span
        className={[
          "h-2 w-2 rounded-full",
          isConnected ? "bg-emerald-300" : "bg-red-300"
        ].join(" ")}
      />
      {isConnected ? "Connected" : "Disconnected"}
    </div>
  );
}
''',
    "client/src/components/TypingIndicator.jsx": r'''export default function TypingIndicator({ users }) {
  if (!users.length) {
    return <div className="h-6" aria-live="polite" />;
  }

  const names = users.map((user) => user.name);
  const message =
    names.length === 1
      ? `${names[0]} is typing...`
      : `${names.slice(0, 2).join(", ")}${names.length > 2 ? ` +${names.length - 2}` : ""} are typing...`;

  return (
    <div className="flex h-6 items-center gap-2 text-sm text-zinc-400" aria-live="polite">
      <div className="flex -space-x-1">
        {users.slice(0, 3).map((user) => (
          <span
            key={user.id}
            className="h-2.5 w-2.5 rounded-full ring-2 ring-zinc-950"
            style={{ backgroundColor: user.color }}
          />
        ))}
      </div>
      <span>{message}</span>
    </div>
  );
}
''',
    "server/package.json": r'''{
  "name": "linkpad-server",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "node --watch src/index.js",
    "start": "node src/index.js"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "express": "^4.19.2",
    "socket.io": "^4.7.5"
  },
  "devDependencies": {}
}
''',
    "server/src/index.js": r'''import express from "express";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import cors from "cors";
import { Server } from "socket.io";

const PORT = process.env.PORT || 4000;
const CLIENT_ORIGIN = process.env.CLIENT_ORIGIN || "*";
const ROOM_CODE_LENGTH = 4;
const ROOM_CHARACTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
const EMPTY_ROOM_TTL_MS = 1000 * 60 * 60;
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const clientDistPath = path.resolve(__dirname, "../../client/dist");
const USER_COLORS = [
  "#67e8f9",
  "#a7f3d0",
  "#fde68a",
  "#f9a8d4",
  "#c4b5fd",
  "#fdba74",
  "#93c5fd",
  "#fca5a5"
];

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: CLIENT_ORIGIN,
    methods: ["GET", "POST"]
  }
});

const rooms = new Map();

app.use(cors({ origin: CLIENT_ORIGIN }));
app.use(express.json());
app.use(express.static(clientDistPath));

app.get("/health", (_req, res) => {
  res.json({
    ok: true,
    app: "LinkPad",
    rooms: rooms.size
  });
});

app.get("/api/network", (_req, res) => {
  const addresses = getLocalIPv4Addresses();

  res.json({
    port: Number(PORT),
    localUrl: `http://localhost:${PORT}`,
    lanUrls: addresses.map((address) => `http://${address}:${PORT}`)
  });
});

app.get("*", (_req, res) => {
  res.sendFile(path.join(clientDistPath, "index.html"));
});

io.on("connection", (socket) => {
  socket.data.roomCode = null;
  socket.data.user = createGuestUser(socket.id);

  socket.on("create-room", (payload, callback) => {
    socket.data.user = createUser(socket.id, payload?.name);

    const roomCode = createUniqueRoomCode();

    rooms.set(roomCode, {
      note: "",
      users: new Map(),
      typingUsers: new Set(),
      emptyRoomTimer: null
    });

    joinRoom(socket, roomCode);

    callback?.({
      ok: true,
      roomCode,
      note: "",
      currentUser: getRoomUser(roomCode, socket.id),
      users: getRoomUsers(roomCode),
      usersCount: getUsersCount(roomCode)
    });
  });

  socket.on("join-room", (payload, callback) => {
    const normalizedRoomCode = normalizeRoomCode(payload?.roomCode);
    const room = rooms.get(normalizedRoomCode);

    socket.data.user = createUser(socket.id, payload?.name);

    if (!room) {
      callback?.({
        ok: false,
        error: "Room not found. Check the code and try again."
      });
      return;
    }

    joinRoom(socket, normalizedRoomCode);

    callback?.({
      ok: true,
      roomCode: normalizedRoomCode,
      note: room.note,
      currentUser: getRoomUser(normalizedRoomCode, socket.id),
      users: getRoomUsers(normalizedRoomCode),
      usersCount: getUsersCount(normalizedRoomCode)
    });
  });

  socket.on("note-update", ({ roomCode, note }) => {
    const normalizedRoomCode = normalizeRoomCode(roomCode);
    const room = rooms.get(normalizedRoomCode);

    if (!room || socket.data.roomCode !== normalizedRoomCode) {
      return;
    }

    room.note = typeof note === "string" ? note : "";

    socket.to(normalizedRoomCode).emit("note-sync", {
      roomCode: normalizedRoomCode,
      note: room.note
    });
  });

  socket.on("typing-update", ({ roomCode, isTyping }) => {
    const normalizedRoomCode = normalizeRoomCode(roomCode);
    const room = rooms.get(normalizedRoomCode);

    if (!room || socket.data.roomCode !== normalizedRoomCode) {
      return;
    }

    if (isTyping) {
      room.typingUsers.add(socket.id);
    } else {
      room.typingUsers.delete(socket.id);
    }

    emitTypingUsers(normalizedRoomCode);
  });

  socket.on("disconnect", () => {
    leaveCurrentRoom(socket);
  });
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`LinkPad server running on http://localhost:${PORT}`);
  getLocalIPv4Addresses().forEach((address) => {
    console.log(`Local network: http://${address}:${PORT}`);
  });
});

function joinRoom(socket, roomCode) {
  leaveCurrentRoom(socket);

  const room = rooms.get(roomCode);
  if (!room) {
    return;
  }

  socket.join(roomCode);
  socket.data.roomCode = roomCode;
  clearEmptyRoomTimer(room);
  room.users.set(socket.id, {
    ...socket.data.user,
    color: pickRoomColor(room)
  });

  emitRoomUsers(roomCode);
}

function leaveCurrentRoom(socket) {
  const roomCode = socket.data.roomCode;
  if (!roomCode) {
    return;
  }

  const room = rooms.get(roomCode);
  if (room) {
    room.users.delete(socket.id);
    room.typingUsers.delete(socket.id);

    if (room.users.size === 0) {
      scheduleEmptyRoomCleanup(roomCode, room);
    } else {
      emitRoomUsers(roomCode);
      emitTypingUsers(roomCode);
    }
  }

  socket.leave(roomCode);
  socket.data.roomCode = null;
}

function emitRoomUsers(roomCode) {
  io.to(roomCode).emit("room-users", {
    roomCode,
    users: getRoomUsers(roomCode),
    usersCount: getUsersCount(roomCode)
  });
}

function scheduleEmptyRoomCleanup(roomCode, room) {
  clearEmptyRoomTimer(room);

  room.emptyRoomTimer = setTimeout(() => {
    const latestRoom = rooms.get(roomCode);

    if (latestRoom && latestRoom.users.size === 0) {
      rooms.delete(roomCode);
    }
  }, EMPTY_ROOM_TTL_MS);
}

function clearEmptyRoomTimer(room) {
  if (!room.emptyRoomTimer) {
    return;
  }

  clearTimeout(room.emptyRoomTimer);
  room.emptyRoomTimer = null;
}

function getUsersCount(roomCode) {
  return rooms.get(roomCode)?.users.size ?? 0;
}

function getRoomUsers(roomCode) {
  return Array.from(rooms.get(roomCode)?.users.values() ?? []);
}

function getRoomUser(roomCode, socketId) {
  return rooms.get(roomCode)?.users.get(socketId) ?? null;
}

function emitTypingUsers(roomCode) {
  const room = rooms.get(roomCode);
  const users = Array.from(room?.typingUsers ?? [])
    .map((socketId) => room.users.get(socketId))
    .filter(Boolean);

  io.to(roomCode).emit("typing-users", {
    roomCode,
    users
  });
}

function createUniqueRoomCode() {
  let roomCode = createRoomCode();

  while (rooms.has(roomCode)) {
    roomCode = createRoomCode();
  }

  return roomCode;
}

function createRoomCode() {
  let code = "";

  for (let index = 0; index < ROOM_CODE_LENGTH; index += 1) {
    const characterIndex = Math.floor(Math.random() * ROOM_CHARACTERS.length);
    code += ROOM_CHARACTERS[characterIndex];
  }

  return code;
}

function normalizeRoomCode(roomCode) {
  return String(roomCode || "")
    .trim()
    .toUpperCase();
}

function getLocalIPv4Addresses() {
  return Object.values(os.networkInterfaces())
    .flat()
    .filter((network) => network?.family === "IPv4" && !network.internal)
    .map((network) => network.address);
}

function createGuestUser(socketId) {
  return createUser(socketId);
}

function createUser(socketId, name) {
  const shortId = socketId.replace(/\W/g, "").slice(0, 4).toUpperCase();
  const cleanName = sanitizeName(name);

  return {
    id: socketId,
    name: cleanName || `Guest ${shortId || Math.floor(Math.random() * 900 + 100)}`,
    color: USER_COLORS[0]
  };
}

function sanitizeName(name) {
  return String(name || "")
    .trim()
    .replace(/\s+/g, " ")
    .slice(0, 24);
}

function pickRoomColor(room) {
  const usedColors = new Set(Array.from(room.users.values()).map((user) => user.color));
  const availableColor = USER_COLORS.find((color) => !usedColors.has(color));

  if (availableColor) {
    return availableColor;
  }

  return USER_COLORS[room.users.size % USER_COLORS.length];
}
''',
    "electron/main.cjs": r'''const { app, BrowserWindow, dialog, shell } = require("electron");
const http = require("node:http");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const ROOT_DIR = path.resolve(__dirname, "..");
const SERVER_URL = "http://localhost:4000";

async function startServer() {
  process.env.NODE_ENV = "production";
  process.env.PORT = "4000";

  const serverEntry = pathToFileURL(path.join(ROOT_DIR, "server", "src", "index.js")).href;
  await import(serverEntry);
}

function waitForServer(retries = 40) {
  return new Promise((resolve, reject) => {
    function check() {
      http
        .get(`${SERVER_URL}/health`, (response) => {
          response.resume();
          resolve();
        })
        .on("error", () => {
          retries -= 1;

          if (retries <= 0) {
            reject(new Error("LinkPad server did not start."));
            return;
          }

          setTimeout(check, 250);
        });
    }

    check();
  });
}

async function createWindow() {
  try {
    await startServer();
    await waitForServer();
  } catch (error) {
    dialog.showErrorBox("Could not start LinkPad", error.message);
    app.quit();
    return;
  }

  const window = new BrowserWindow({
    width: 1180,
    height: 820,
    minWidth: 860,
    minHeight: 620,
    backgroundColor: "#09090b",
    title: "LinkPad",
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  window.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: "deny" };
  });

  await window.loadURL(SERVER_URL);
}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  app.quit();
});

app.on("before-quit", () => {
  app.isQuitting = true;
});
''',
}


def restore(destination: Path) -> None:
  for name, content in FILES.items():
    target = destination / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
  output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("restored_linkpad")
  restore(output_dir)
  print(f"Restored {len(FILES)} files into {output_dir}")
