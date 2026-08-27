import { Link } from "react-router-dom";
import EmptyState from "../components/EmptyState";

export default function NotFound() {
  return (
    <div className="page">
      <EmptyState
        title="This page was lost to the sea"
        description="The record you're looking for doesn't exist."
      />
      <p style={{ textAlign: "center", marginTop: "1rem" }}>
        <Link to="/" className="detail__back">
          &larr; Return to the archive
        </Link>
      </p>
    </div>
  );
}
