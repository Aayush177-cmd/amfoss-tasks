import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  BACKDROP_BASE,
  IMG_BASE_LARGE,
  getMovieDetails,
} from "../api/tmdb";
import { useWatchlist } from "../context/WatchlistContext";
import Loader from "../components/Loader";
import EmptyState from "../components/EmptyState";
import MovieGrid from "../components/MovieGrid";

function formatRuntime(minutes) {
  if (!minutes) return "Unknown length";
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return `${h}h ${m}m`;
}

export default function MovieDetail() {
  const { id } = useParams();
  const { isSaved, toggleEntry } = useWatchlist();

  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    setMovie(null);

    getMovieDetails(id)
      .then((data) => {
        if (!cancelled) setMovie(data);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message ?? "Could not load this record.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [id]);

  if (loading) return <Loader label="Unsealing record" />;
  if (error || !movie) {
    return (
      <EmptyState
        title="Record not found"
        description={error ?? "This title could not be retrieved from the archive."}
      />
    );
  }

  const saved = isSaved(movie.id);
  const director = movie.credits?.crew?.find((c) => c.job === "Director");
  const cast = movie.credits?.cast?.slice(0, 8) ?? [];
  const recommendations = movie.recommendations?.results?.slice(0, 6) ?? [];

  return (
    <div className="detail">
      {movie.backdrop_path && (
        <div
          className="detail__backdrop"
          style={{
            backgroundImage: `linear-gradient(180deg, rgba(15,17,23,0.35) 0%, var(--ink) 92%), url(${BACKDROP_BASE}${movie.backdrop_path})`,
          }}
        />
      )}

      <div className="detail__content page">
        <Link to="/" className="detail__back">
          &larr; Back to the archive
        </Link>

        <div className="detail__grid">
          <div className="detail__poster-wrap">
            {movie.poster_path ? (
              <img
                className="detail__poster"
                src={`${IMG_BASE_LARGE}${movie.poster_path}`}
                alt={`Poster for ${movie.title}`}
              />
            ) : (
              <div className="detail__poster detail__poster--blank">No Plate</div>
            )}
          </div>

          <div className="detail__info">
            <p className="hero__eyebrow">
              No. {String(movie.id).padStart(6, "0")}
              {movie.release_date ? ` · Filed ${movie.release_date.slice(0, 4)}` : ""}
            </p>
            <h1 className="detail__title">{movie.title}</h1>
            {movie.tagline && <p className="detail__tagline">&ldquo;{movie.tagline}&rdquo;</p>}

            <div className="detail__meta">
              <span>&#9733; {movie.vote_average?.toFixed(1) ?? "—"} / 10</span>
              <span>{formatRuntime(movie.runtime)}</span>
              <span>{movie.status}</span>
              {director && <span>Dir. {director.name}</span>}
            </div>

            {movie.genres?.length > 0 && (
              <div className="detail__genres">
                {movie.genres.map((g) => (
                  <span key={g.id} className="tag">
                    {g.name}
                  </span>
                ))}
              </div>
            )}

            <p className="detail__overview">{movie.overview || "No record of this synopsis remains."}</p>

            <button
              type="button"
              className="btn btn--seal"
              data-active={saved}
              onClick={() => toggleEntry(movie)}
            >
              {saved ? "✓ Preserved in your archive" : "+ Add to your archive"}
            </button>

            {cast.length > 0 && (
              <div className="detail__cast">
                <h3>Cast on Record</h3>
                <div className="detail__cast-list">
                  {cast.map((member) => (
                    <span key={member.cast_id ?? member.credit_id} className="cast-chip">
                      {member.name}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {recommendations.length > 0 && (
          <section className="section">
            <div className="section__head">
              <h2>Related Records</h2>
            </div>
            <MovieGrid movies={recommendations} loading={false} error={null} />
          </section>
        )}
      </div>
    </div>
  );
}
