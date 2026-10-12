/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: '#0a0f1d',
          card: '#121a29',
          border: '#1e293b',
          neonCyan: '#00f0ff',
          neonPink: '#ff007f',
          neonGreen: '#00ff66',
          neonYellow: '#ffcc00',
          darker: '#050811',
        }
      },
      boxShadow: {
        neon: '0 0 15px rgba(0, 240, 255, 0.3)',
        neonPink: '0 0 15px rgba(255, 0, 127, 0.3)',
        neonGreen: '0 0 15px rgba(0, 255, 102, 0.3)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'scanline': 'scanline 8s linear infinite',
      },
      keyframes: {
        scanline: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(1000%)' },
        }
      }
    },
  },
  plugins: [],
}
