
import { useState } from "react";
import EventCard from "../components/EventCard";
import { useRegistration } from "../context/RegistrationContext";

function Events() {
  const {
    events,
    getAvailableSeats,
    addRegistration
  } = useRegistration();

  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All");
  const [selectedEvent, setSelectedEvent] = useState(null);

  const filteredEvents = events.filter((event) => {
    const matchesSearch = event.title
      .toLowerCase()
      .includes(search.toLowerCase());

    const matchesCategory =
      category === "All" || event.category === category;

    return matchesSearch && matchesCategory;
  });

  return (
    <div>
      <h1>Upcoming Events</h1>

      <p className="page-description">
        Browse and register for upcoming events.
      </p>

      <div className="filters">

        <input
          type="text"
          placeholder="Search events..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          <option value="All">All Categories</option>
          <option value="Technology">Technology</option>
          <option value="Arts">Arts</option>
          <option value="Life Skills">Life Skills</option>
        </select>

      </div>

      {filteredEvents.length === 0 ? (
        <p className="empty-message">
          No events found. Try another search or category.
        </p>
      ) : (

        <div className="event-grid">

          {filteredEvents.map((event) => (
            <EventCard
              key={event.id}
              event={event}
              availableSeats={getAvailableSeats(event.id)}
              onRegister={setSelectedEvent}
              showForm={selectedEvent?.id === event.id}
              onClose={() => setSelectedEvent(null)}
              onSubmit={addRegistration}
            />
          ))}

        </div>

      )}

    </div>
  );
}

export default Events;
