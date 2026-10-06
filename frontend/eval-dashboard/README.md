# Eval Dashboard

React + Vite dashboard for the GenAI Eval Engine.

## What It Does

- Register and log in with the FastAPI backend.
- Submit model outputs for evaluation.
- Poll run status until scoring completes.
- Review run history and detailed scoring reasoning.
- Edit or delete runs owned by the signed-in user.

## Local Development

```bash
npm install
npm run dev
```

The app expects the backend API at `http://localhost:8000/api/v1` by default.
Update `src/services/api.js` if the backend runs elsewhere.

## Checks

```bash
npm run lint
npm run build
```

Keep the React hook lint rules enabled. The dashboard initializes async data
inside effects and keeps run edit state local to `RunDetail`.
