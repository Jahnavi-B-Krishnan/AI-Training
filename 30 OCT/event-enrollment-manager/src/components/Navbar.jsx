
import { NavLink } from "react-router-dom";

function Navbar() {
  return (
    <header className="navbar">
      <div className="nav-content">

        <h2>Event Enrollment Manager</h2>

        <nav>
          <NavLink to="/" end>
            Events
          </NavLink>

          <NavLink to="/registrations">
            Registrations
          </NavLink>
        </nav>

      </div>
    </header>
  );
}

export default Navbar;
