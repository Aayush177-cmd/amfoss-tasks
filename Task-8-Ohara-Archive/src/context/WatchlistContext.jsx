import { createContext, useContext, useEffect, useMemo, useState } from "react";

const STORAGE_KEY = "ohara-archive:watchlist";
const WatchlistContext = createContext(null);

function readStoredWatchlist() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export function WatchlistProvider({ children }) {
  const [entries, setEntries] = useState(readStoredWatchlist);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
  }, [entries]);

  const value = useMemo(() => {
    const isSaved = (id) => entries.some((entry) => entry.id === id);

    const addEntry = (movie) => {
      setEntries((prev) =>
        prev.some((entry) => entry.id === movie.id) ? prev : [
          {
            id: movie.id,
            title: movie.title,
            poster_path: movie.poster_path,
            release_date: movie.release_date,
            vote_average: movie.vote_average,
            savedAt: Date.now(),
          },
          ...prev,
        ]
      );
    };

    const removeEntry = (id) => {
      setEntries((prev) => prev.filter((entry) => entry.id !== id));
    };

    const toggleEntry = (movie) => {
      if (isSaved(movie.id)) {
        removeEntry(movie.id);
      } else {
        addEntry(movie);
      }
    };

    return { entries, isSaved, addEntry, removeEntry, toggleEntry };
  }, [entries]);

  return (
    <WatchlistContext.Provider value={value}>
      {children}
    </WatchlistContext.Provider>
  );
}

export function useWatchlist() {
  const ctx = useContext(WatchlistContext);
  if (!ctx) {
    throw new Error("useWatchlist must be used within a WatchlistProvider");
  }
  return ctx;
}
