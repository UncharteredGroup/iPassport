# iPassport frontend

React + Vite PWA: guided application steps with camera capture, verification
feedback, and the final application package.

## Run

```bash
npm install
npm run dev
```

The app expects the backend at `VITE_API_BASE` (default http://localhost:8000).

## Steps

1. Application type + agentic guide chat
2. National ID capture (segmentation overlay + extracted fields)
3. Selfie + liveness
4. Passport photo validation
5. Payment stub + package generation + status tracker
