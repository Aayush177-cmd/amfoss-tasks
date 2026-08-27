export default function GenreFilter({ genres, activeId, onSelect }) {
  if (!genres || genres.length === 0) return null;

  return (
    <div className="chips" role="tablist" aria-label="Filter by classification">
      <button
        type="button"
        className="chip"
        data-active={!activeId}
        onClick={() => onSelect(null)}
      >
        All Records
      </button>
      {genres.map((genre) => (
        <button
          type="button"
          key={genre.id}
          className="chip"
          data-active={activeId === genre.id}
          onClick={() => onSelect(genre.id)}
        >
          {genre.name}
        </button>
      ))}
    </div>
  );
}
