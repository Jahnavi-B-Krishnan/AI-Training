import { Link, useLocation, useNavigate } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

export default function NotFound() {
  const location = useLocation();
  const navigate = useNavigate();

  const message =
    location.state?.message ||
    "We couldn't find the page you're looking for.";

  return (
    <main className="error-page">
      <Link to="/" className="login-logo">
        shop<span>zone</span><small>.in</small>
      </Link>

      <section className="error-content">
        <h1>404</h1>

        <h2>Oops! Something went wrong.</h2>

        <p>{message}</p>

        <div className="error-actions">
          <button
            className="secondary-button"
            onClick={() => navigate(-1)}
          >
            <ArrowLeft size={16} />
            Go back
          </button>

          <Link to="/login" className="primary-button">
            Try signing in again
          </Link>

          <Link to="/" className="text-link">
            Back to home
          </Link>
        </div>
      </section>
    </main>
  );
}