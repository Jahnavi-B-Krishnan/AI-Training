
import { useRegistration } from "../context/RegistrationContext";

function Registrations() {
  const {
    events,
    registrations,
    cancelRegistration
  } = useRegistration();

  function handleCancel(registration) {
    const confirmCancel = window.confirm(
      "Are you sure you want to cancel this registration?"
    );

    if (confirmCancel) {
      cancelRegistration(registration.id);
    }
  }

  return (
    <div>
      <h1>Registrations</h1>

      <p className="page-description">
        View and manage all event registrations.
      </p>

      {registrations.length === 0 ? (
        <p className="empty-message">
          No registrations have been made yet.
        </p>
      ) : (

        <div className="registration-list">

          {registrations.map((registration) => {

            const event = events.find(
              (item) => item.id === registration.eventId
            );

            return (
              <div
                className="registration-card"
                key={registration.id}
              >

                <h3>{registration.name}</h3>

                <p>
                  <strong>Email:</strong> {registration.email}
                </p>

                <p>
                  <strong>Event:</strong> {event?.title}
                </p>

                <p>
                  <strong>Event Date:</strong> {event?.date}
                </p>

                <button
                  className="cancel-button"
                  onClick={() => handleCancel(registration)}
                >
                  Cancel Registration
                </button>

              </div>
            );
          })}

        </div>
      )}

    </div>
  );
}

export default Registrations;
