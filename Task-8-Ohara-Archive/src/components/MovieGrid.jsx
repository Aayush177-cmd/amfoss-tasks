import MovieCard from "./MovieCard";
import Loader from "./Loader";
import EmptyState from "./EmptyState";

export default function MovieGrid({
  movies,
  loading,
  error,
  emptyTitle = "No records found",
  emptyDescription = "Try another search term.",
}) {
  if (loading) return <Loader />;

  if (error) {
    return (
      <EmptyState
        title="The archive is unreachable"
        description={error}
      />
    );
  }

  if (!movies || movies.length === 0) {
    return <EmptyState title={emptyTitle} description={emptyDescription} />;
  }

  return (
    <div className="grid">
      {movies.map((movie) => (
        <MovieCard key={movie.id} movie={movie} />
      ))}
    </div>
  );
}
