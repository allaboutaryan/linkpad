import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { socket } from "./lib/socket.js";
import HomePage from "./pages/HomePage.jsx";
import EditorPage from "./pages/EditorPage.jsx";

const INITIAL_STATUS = socket.connected ? "connected" : "disconnected";
const TYPING_STOP_DELAY = 1200;

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
  const latestRoomCode = useRef("");
  const currentUserRef = useRef(null);
  const typingTimeoutRef = useRef(null);

  useEffect(() => {
    function handleConnect() {
      setConnectionStatus("connected");
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

    socket.emit("create-room", { name }, (response) => {
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

    socket.emit("join-room", { roomCode: requestedRoomCode, name }, (response) => {
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
    });
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
      error
    }),
    [roomCode, note, users, currentUser, typingUsers, usersCount, connectionStatus, error]
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
