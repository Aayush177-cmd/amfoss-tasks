const API_KEY = import.meta.env.VITE_TMDB_API_KEY;
const BASE_URL = "https://api.themoviedb.org/3";

export const IMG_BASE = "https://image.tmdb.org/t/p/w500";
export const IMG_BASE_LARGE = "https://image.tmdb.org/t/p/w780";
export const BACKDROP_BASE = "https://image.tmdb.org/t/p/original";

class TmdbError extends Error {}

async function request(path, params = {}) {
  if (!API_KEY) {
    throw new TmdbError(
      "Missing TMDB API key. Add VITE_TMDB_API_KEY to your .env file."
    );
  }

  const url = new URL(`${BASE_URL}${path}`);
  url.searchParams.set("api_key", API_KEY);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.set(key, value);
    }
  });

  const res = await fetch(url.toString());
  if (!res.ok) {
    throw new TmdbError(`TMDB request failed (${res.status})`);
  }
  return res.json();
}

export function getTrending(timeWindow = "week", page = 1) {
  return request(`/trending/movie/${timeWindow}`, { page });
}

export function getPopular(page = 1) {
  return request("/movie/popular", { page });
}

export function getTopRated(page = 1) {
  return request("/movie/top_rated", { page });
}

export function discoverByGenre(genreId, page = 1) {
  return request("/discover/movie", {
    with_genres: genreId,
    page,
    sort_by: "popularity.desc",
  });
}

export function searchMovies(query, page = 1) {
  return request("/search/movie", { query, page, include_adult: false });
}

export function getMovieDetails(id) {
  return request(`/movie/${id}`, {
    append_to_response: "credits,videos,recommendations",
  });
}

export function getGenres() {
  return request("/genre/movie/list");
}

export { TmdbError };
