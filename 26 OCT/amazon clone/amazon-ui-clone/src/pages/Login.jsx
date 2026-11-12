import { Link, useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();
  const location = useLocation();

  const checkout =
    new URLSearchParams(location.search).get("next") ===
    "checkout";

  function handleLogin(e) {
    e.preventDefault();

    const validEmail =
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

    const validPassword = password.trim().length >= 4;

    if (!validEmail || !validPassword) {
      navigate("/404", {
        state: {
          message:
            "Invalid login details. Please check your email and password."
        }
      });

      return;
    }

    if (checkout) {
      navigate("/payment");
    } else {
      navigate("/");
    }
  }

  return (
    <main className="login-page">
      <Link to="/" className="login-logo">
        shop<span>zone</span><small>.in</small>
      </Link>

      <section className="login-card">
        <h1>Sign in</h1>

        <p className="login-intro">
          {checkout
            ? "Sign in to continue to payment."
            : "Welcome to ShopZone."}
        </p>

        <form onSubmit={handleLogin}>
          <label htmlFor="email">Email address</label>

          <input
            id="email"
            type="text"
            inputMode="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label htmlFor="password">Password</label>

          <input
            id="password"
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button
            type="submit"
            className="primary-button full"
          >
            {checkout ? "Sign in to continue" : "Sign in"}
          </button>
        </form>

        <p className="terms">
          This is a demo login. No real account is created.
        </p>

        <Link to="/" className="secondary-button full">
          Back to shopping
        </Link>

        <div className="demo-tip">
          <strong>Demo credentials</strong>
          <p>
            Use any valid email and a password with at
            least four characters.
          </p>
        </div>
      </section>
    </main>
  );
}