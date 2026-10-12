import React, { useState, useEffect, useRef, forwardRef } from 'react';
import { WebSocketMessage, BoundingBox, ViewportSnapshot } from '../types';

interface LiveViewportProps {
  ws: WebSocket | null;
  onFrame?: (frame: ViewportSnapshot) => void;
  onThought?: (thought: any) => void;
  onAction?: (action: any) => void;
  onSessionUpdate?: (session: any) => void;
  children?: React.ReactNode;
}

export const LiveViewport = forwardRef<HTMLDivElement, LiveViewportProps>(
  ({ ws, onFrame, onThought, onAction, onSessionUpdate, children }, ref) => {
    const [frame, setFrame] = useState<ViewportSnapshot | null>(null);
    const [boxes, setBoxes] = useState<BoundingBox[]>([]);
    const [connected, setConnected] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [frameCount, setFrameCount] = useState(0);
    const [fps, setFps] = useState(0);
    const lastFrameTime = useRef<number>(0);
    const frameCountRef = useRef(0);
    const fpsInterval = useRef<NodeJS.Timeout | null>(null);

    useEffect(() => {
      if (!ws) return;

      const handleMessage = (event: MessageEvent) => {
        try {
          const msg: WebSocketMessage = JSON.parse(event.data);
          switch (msg.type) {
            case 'viewport':
              setFrame(msg.payload as ViewportSnapshot);
              setBoxes(msg.payload.boundingBoxes || []);
              onFrame?.(msg.payload);
              frameCountRef.current++;
              break;
            case 'thought':
              onThought?.(msg.payload);
              break;
            case 'action':
              onAction?.(msg.payload);
              break;
            case 'session_update':
              onSessionUpdate?.(msg.payload);
              break;
            case 'error':
              setError(msg.payload as string);
              break;
            default:
              console.log('Unknown message type:', msg.type);
          }
        } catch (err) {
          console.error('Error parsing WebSocket message:', err);
        }
      };

      const handleOpen = () => {
        setConnected(true);
        setError(null);
      };

      const handleClose = () => {
        setConnected(false);
      };

      ws.addEventListener('message', handleMessage);
      ws.addEventListener('open', handleOpen);
      ws.addEventListener('close', handleClose);

      // FPS calculation
      fpsInterval.current = setInterval(() => {
        setFps(frameCountRef.current);
        frameCountRef.current = 0;
      }, 1000);

      return () => {
        ws.removeEventListener('message', handleMessage);
        ws.removeEventListener('open', handleOpen);
        ws.removeEventListener('close', handleClose);
        if (fpsInterval.current) clearInterval(fpsInterval.current);
      };
    }, [ws, onFrame, onThought, onAction, onSessionUpdate]);

    return (
      <div ref={ref} className="relative w-full h-full">
        {frame && (
          <img
            src={frame.frameBase64}
            alt="Browser viewport"
            className="w-full h-full object-cover rounded-lg"
          />
        )}
        {boxes.map((box, idx) => (
          <div
            key={idx}
            className="absolute border-2 border-cyan-400 rounded pointer-events-none"
            style={{
              left: `${box.x}px`,
              top: `${box.y}px`,
              width: `${box.width}px`,
              height: `${box.height}px`,
              boxShadow: '0 0 10px rgba(0, 240, 255, 0.5)',
            }}
          >
            {box.isInteractive && (
              <span className="absolute -top-5 left-0 text-xs bg-cyan-500 text-white px-1 rounded">
                {box.tagName}
              </span>
            )}
          </div>
        ))}
        <div className="absolute top-2 left-2 flex items-center gap-2">
          <span
            className={`w-3 h-3 rounded-full ${connected ? 'bg-green-500' : 'bg-red-500'}`}
          />
          <span className="text-xs text-white">
            {connected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
        {fps > 0 && (
          <div className="absolute top-2 right-2 text-xs text-white">
            {fps} fps
          </div>
        )}
        {children}
      </div>
    );
  }
);

LiveViewport.displayName = 'LiveViewport';