export default function SearchBar({ value, onChange, size = "default" }) {
  return (
    <div className={`dial dial--${size}`}>
      <span className="dial__glyph" aria-hidden="true">&#8981;</span>
      <input
        type="text"
        className="dial__input"
        placeholder="Search the archive by title…"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        aria-label="Search movies"
      />
      {value && (
        <button
          type="button"
          className="dial__clear"
          onClick={() => onChange("")}
          aria-label="Clear search"
        >
          &times;
        </button>
      )}
    </div>
  );
}
