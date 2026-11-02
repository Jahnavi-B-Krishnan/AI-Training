
import RegistrationForm from "./RegistrationForm";

function EventCard({
  event,
  availableSeats,
  onRegister,
  showForm,
  onClose,
  onSubmit
}) {
  const isFull = availableSeats === 0;

  return (
    <div className="event-card">

      <p className="category">{event.category}</p>

      <h3>{event.title}</h3>

      <p><strong>Event ID:</strong> {event.id}</p>
      <p><strong>Date:</strong> {event.date}</p>
      <p><strong>Time:</strong> {event.time}</p>
      <p><strong>Total Seats:</strong> {event.capacity}</p>
      <p><strong>Available Seats:</strong> {availableSeats}</p>

      <button
        onClick={() => onRegister(event)}
        disabled={isFull}
      >
        {isFull ? "Fully Booked" : "Register"}
      </button>

      {showForm && (
        <RegistrationForm
          event={event}
          onClose={onClose}
          onSubmit={onSubmit}
        />
      )}

    </div>
  );
}

export default EventCard;
