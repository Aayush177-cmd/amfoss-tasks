import { useWatchlist } from "../context/WatchlistContext";
import MovieGrid from "../components/MovieGrid";

export default function Archive() {
  const { entries } = useWatchlist();

  return (
    <div className="page">
      <section className="section-head-block">
        <p className="hero__eyebrow">Vol. II — Personal Collection</p>
        <h1 className="page__title">My Archive</h1>
        <p className="page__sub">
          {entries.length > 0
            ? `${entries.length} title${entries.length === 1 ? "" : "s"} preserved for later viewing.`
            : "Titles you mark for preservation will be catalogued here."}
        </p>
      </section>

      <MovieGrid
        movies={entries}
        loading={false}
        error={null}
        emptyTitle="Your archive is empty"
        emptyDescription="Discover films worth preserving, then seal them into your collection."
      />
    </div>
  );
}
