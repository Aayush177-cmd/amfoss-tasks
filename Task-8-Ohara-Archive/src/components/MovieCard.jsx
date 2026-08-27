import { Link } from "react-router-dom";
import { IMG_BASE } from "../api/tmdb";
import { useWatchlist } from "../context/WatchlistContext";

function recordNumber(id) {
  return `No. ${String(id).padStart(6, "0")}`;
}

function year(dateStr) {
  return dateStr ? dateStr.slice(0, 4) : "—";
}

export default function MovieCard({ movie }) {
  const { isSaved, toggleEntry } = useWatchlist();
  const saved = isSaved(movie.id);

  const handleToggle = (event) => {
    event.preventDefault();
    event.stopPropagation();
    toggleEntry(movie);
  };

  return (
    <Link to={`/film/${movie.id}`} className="card" data-saved={saved}>
      <span className="card__record">{recordNumber(movie.id)}</span>
      <div className="card__frame">
        {movie.poster_path ? (
          <img
            className="card__poster"
            src={`${IMG_BASE}${movie.poster_path}`}
            alt={`Poster for ${movie.title}`}
            loading="lazy"
          />
        ) : (
          <div className="card__poster card__poster--blank">No Plate</div>
        )}
        <button
          type="button"
          className="card__seal"
          onClick={handleToggle}
          aria-pressed={saved}
          aria-label={saved ? `Remove ${movie.title} from archive` : `Add ${movie.title} to archive`}
          title={saved ? "Remove from archive" : "Add to archive"}
        >
          {saved ? "✓" : "+"}
        </button>
      </div>
      <div className="card__body">
        <h3 className="card__title">{movie.title}</h3>
        <div className="card__meta">
          <span>{year(movie.release_date)}</span>
          <span className="card__rating">
            &#9733; {movie.vote_average ? movie.vote_average.toFixed(1) : "—"}
          </span>
        </div>
      </div>
    </Link>
  );
}
