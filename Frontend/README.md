<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# Frontend (Vue + Vite)

Apple-inspired IdeaStream UI rebuilt with Vue 3, Vite, and Tailwind (CDN). Two routes:
- `/` Homepage with hero + top-3 hottest ideas
- `/board` Full board with add form, voting, and detail modal

## Quickstart
1) Install deps: `npm install`
2) Run dev server: `npm run dev` (defaults to http://localhost:3000)
3) Build for prod: `npm run build`

## Notes
- Styling via Tailwind CDN in `index.html` plus custom utility classes.
- State is shared via `composables/useTodos.ts` (todos, voting, add-new).
- New idea form lives on `/board` only; votes are toggleable once per user (in-memory).
