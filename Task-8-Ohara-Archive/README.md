# Ohara Archive

A movie discovery and watchlist app built with React, styled after the Library
of Ohara — a scholars' archive where every film is treated as a record worth
preserving. Movie data comes from [The Movie Database (TMDB)](https://www.themoviedb.org/).

## Features

- **Discover** — browse trending movies, filter by genre, or search the full
  TMDB catalog with a debounced search bar.
- **Movie detail pages** — poster, backdrop, overview, runtime, rating,
  director, cast, and related recommendations, each on its own route
  ('/film/:id').
- **Personal archive (watchlist)** — add or remove any movie with one click;
  the list persists across sessions via 'localStorage', no backend required.
- **Responsive UI** — works from mobile to desktop, with visible keyboard
  focus states and reduced-motion support.
- **Reusable components** — 'MovieCard', 'MovieGrid', 'SearchBar',
  'GenreFilter', 'Loader', 'EmptyState' are all shared across pages.

## Tech stack

- React 19 + Vite
- React Router for client-side routing
- React Context + 'localStorage' for watchlist persistence (no Redux needed
  for a data set this size)
- Plain CSS with design tokens (CSS custom properties) — no UI framework
- TMDB REST API (v3)

## Project structure


src/
  api/tmdb.js                   # TMDB fetch wrapper (search, trending, details, genres)
  hooks/useDebounce.js          # debounce hook used by search
  context/WatchlistContext.jsx  # watchlist state + localStorage sync
  components/                   # MovieCard, MovieGrid, SearchBar, GenreFilter, Navbar...
  pages/                        # Home, Archive (watchlist), MovieDetail, NotFound
  
## Getting started

1. **Get a free TMDB API key**
   - Create an account at https://www.themoviedb.org/signup
   - Go to Settings → API → request a "Developer" API key (v3 auth)

2. **Clone and install**
   npm install

3. **Add your API key**
   cp .env.example .env
   # then edit .env and paste your key:
   # VITE_TMDB_API_KEY=your_key_here

4. **Run locally**
   
   npm run dev

6. **Build for production**
   
   npm run build
   npm run preview   # sanity-check the production build locally
   

## Deploying

The app is a static Vite build, so any static host works. Two easy options:

### Vercel
1. Push this repo to GitHub.
2. Import it at https://vercel.com/new.
3. Framework preset: **Vite**. Build command 'npm run build', output dir 'dist'.
4. Add an environment variable 'VITE_TMDB_API_KEY' with your TMDB key.
5. Deploy.

### Netlify
1. Push this repo to GitHub.
2. New site from Git at https://app.netlify.com.
3. Build command: 'npm run build', publish directory: 'dist'.
4. Site settings → Environment variables → add 'VITE_TMDB_API_KEY'.
5. Deploy.

> Because 'VITE_TMDB_API_KEY' is a build-time variable, you must set it in
> your host's dashboard (not just your local '.env') before building, or the
> deployed app will show "Missing TMDB API key".

## Notes

This project is not affiliated with or endorsed by TMDB.
