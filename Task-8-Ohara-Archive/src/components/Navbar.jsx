import { NavLink } from "react-router-dom";
import { useWatchlist } from "../context/WatchlistContext";

export default function Navbar() {
  const { entries } = useWatchlist();

  return (
    <header className="nav">
      <div className="nav__inner">
        <NavLink to="/" className="nav__brand">
          <span className="nav__mark" aria-hidden="true">&#9737;</span>
          <span className="nav__wordmark">
            Ohara <em>Archive</em>
          </span>
        </NavLink>
        <nav className="nav__links">
          <NavLink to="/" end className="nav__link">
            Discover
          </NavLink>
          <NavLink to="/archive" className="nav__link">
            My Archive
            {entries.length > 0 && (
              <span className="nav__count">{entries.length}</span>
            )}
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
