import { io, Socket } from "socket.io-client";

let _socketInstance: Socket | null = null;

export const getSocket = (): Socket => {
  if (!_socketInstance) {
    _socketInstance = io((import.meta as any).env?.VITE_BACKEND_URL || "http://localhost:3001", {
      transports: ["websocket"],
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    });
  }
  return _socketInstance;
};

export const socket: Socket = getSocket();
