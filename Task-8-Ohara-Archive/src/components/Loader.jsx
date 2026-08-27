export default function Loader({ label = "Retrieving records" }) {
  return (
    <div className="loader" role="status">
      <span className="loader__mark" aria-hidden="true" />
      <span className="loader__label">{label}&hellip;</span>
    </div>
  );
}
