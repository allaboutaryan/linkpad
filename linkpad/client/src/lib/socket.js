import { io } from "socket.io-client";

const serverUrl = import.meta.env.VITE_SOCKET_URL || `${window.location.protocol}//${window.location.hostname}:4000`;

export const socket = io(serverUrl, {
  autoConnect: true,
  transports: ["websocket", "polling"]
});

