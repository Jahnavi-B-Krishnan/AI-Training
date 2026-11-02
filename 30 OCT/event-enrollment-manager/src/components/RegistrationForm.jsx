
import { useState } from "react";

function RegistrationForm({ event, onClose, onSubmit }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");

  function handleSubmit(e) {
    e.preventDefault();

    if (!name.trim() || !email.trim()) {
      setError("Please enter both your name and email.");
      return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(email.trim())) {
      setError("Please enter a valid email address.");
      return;
    }

    const result = onSubmit({
      eventId: event.id,
      name,
      email
    });

    if (!result.success) {
      setError(result.message);
      return;
    }

    alert("Registration successful!");
    onClose();
  }

  return (
    <div className="form-panel">

      <h3>Register for {event.title}</h3>

      <form onSubmit={handleSubmit}>

        <label>Full Name</label>

        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Enter your full name"
        />

        <label>Email Address</label>

        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
        />

        {error && (
          <p className="error-message">{error}</p>
        )}

        <div className="form-buttons">

          <button type="submit">
            Submit Registration
          </button>

          <button
            type="button"
            className="secondary-button"
            onClick={onClose}
          >
            Close
          </button>

        </div>

      </form>

    </div>
  );
}

export default RegistrationForm;
