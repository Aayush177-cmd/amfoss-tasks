import { useEffect, useState } from "react";
import SearchBar from "../components/SearchBar";
import GenreFilter from "../components/GenreFilter";
import MovieGrid from "../components/MovieGrid";
import { useDebounce } from "../hooks/useDebounce";
import {
  discoverByGenre,
  getGenres,
  getTrending,
  searchMovies,
} from "../api/tmdb";

export default function Home() {
  const [query, setQuery] = useState("");
  const debouncedQuery = useDebounce(query, 400);

  const [genres, setGenres] = useState([]);
  const [activeGenre, setActiveGenre] = useState(null);

  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getGenres()
      .then((data) => setGenres(data.genres ?? []))
      .catch(() => setGenres([]));
  }, []);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    const request = debouncedQuery
      ? searchMovies(debouncedQuery)
      : activeGenre
      ? discoverByGenre(activeGenre)
      : getTrending();

    request
      .then((data) => {
        if (!cancelled) setMovies(data.results ?? []);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message ?? "Something went wrong.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [debouncedQuery, activeGenre]);

  const heading = debouncedQuery
    ? `Results for “${debouncedQuery}”`
    : activeGenre
    ? genres.find((g) => g.id === activeGenre)?.name ?? "Records"
    : "Trending This Week";

  return (
    <div className="page">
      <section className="hero">
        <p className="hero__eyebrow">Vol. I — The Public Ledger</p>
        <h1 className="hero__title">
          Every film ever made
          <br />
          begins as a record.
        </h1>
        <p className="hero__sub">
          Search the archive, weigh the evidence, and preserve the titles
          worth remembering in your own collection.
        </p>
        <SearchBar value={query} onChange={setQuery} size="large" />
      </section>

      {!debouncedQuery && (
        <GenreFilter
          genres={genres}
          activeId={activeGenre}
          onSelect={setActiveGenre}
        />
      )}

      <section className="section">
        <div className="section__head">
          <h2>{heading}</h2>
        </div>
        <MovieGrid
          movies={movies}
          loading={loading}
          error={error}
          emptyTitle="No matching records"
          emptyDescription="The archive has no titles under that entry. Try another search."
        />
      </section>
    </div>
  );
}
