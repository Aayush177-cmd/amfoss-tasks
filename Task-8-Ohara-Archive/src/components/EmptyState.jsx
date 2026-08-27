export default function EmptyState({ title, description }) {
  return (
    <div className="empty-state">
      <span className="empty-state__seal" aria-hidden="true">
        &#10058;
      </span>
      <h3>{title}</h3>
      {description && <p>{description}</p>}
    </div>
  );
}
