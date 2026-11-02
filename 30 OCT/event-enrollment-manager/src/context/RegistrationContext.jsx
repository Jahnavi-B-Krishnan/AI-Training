
import { createContext, useContext, useEffect, useState } from "react";

const RegistrationContext = createContext();

const initialEvents = [
  {
    id: "EV101",
    title: "Intro to Cloud Computing",
    category: "Technology",
    date: "10 Nov 2026",
    time: "10:00",
    capacity: 4
  },
  {
    id: "EV102",
    title: "Creative Writing Lab",
    category: "Arts",
    date: "12 Nov 2026",
    time: "14:00",
    capacity: 3
  },
  {
    id: "EV103",
    title: "Data Visualization Basics",
    category: "Technology",
    date: "14 Nov 2026",
    time: "11:00",
    capacity: 5
  },
  {
    id: "EV104",
    title: "Personal Finance Essentials",
    category: "Life Skills",
    date: "16 Nov 2026",
    time: "16:00",
    capacity: 4
  },
  {
    id: "EV105",
    title: "Public Speaking Practice",
    category: "Life Skills",
    date: "18 Nov 2026",
    time: "10:30",
    capacity: 3
  },
  {
    id: "EV106",
    title: "Digital Illustration Studio",
    category: "Arts",
    date: "20 Nov 2026",
    time: "13:00",
    capacity: 2
  }
];

export function RegistrationProvider({ children }) {

  const [registrations, setRegistrations] = useState(() => {
    const savedData = localStorage.getItem("eventRegistrations");

    return savedData ? JSON.parse(savedData) : [];
  });

  useEffect(() => {
    localStorage.setItem(
      "eventRegistrations",
      JSON.stringify(registrations)
    );
  }, [registrations]);

  function addRegistration(registration) {

    const selectedEvent = initialEvents.find(
      (event) => event.id === registration.eventId
    );

    if (!selectedEvent) {
      return {
        success: false,
        message: "Event not found."
      };
    }

    const activeRegistrations = registrations.filter(
      (item) => item.eventId === registration.eventId
    );

    if (activeRegistrations.length >= selectedEvent.capacity) {
      return {
        success: false,
        message: "This event is fully booked."
      };
    }

    const emailExists = registrations.some(
      (item) =>
        item.eventId === registration.eventId &&
        item.email.trim().toLowerCase() ===
          registration.email.trim().toLowerCase()
    );

    if (emailExists) {
      return {
        success: false,
        message: "This email is already registered for this event."
      };
    }

    const newRegistration = {
      id: Date.now().toString(),
      eventId: registration.eventId,
      name: registration.name.trim(),
      email: registration.email.trim().toLowerCase()
    };

    setRegistrations((previousRegistrations) => [
      ...previousRegistrations,
      newRegistration
    ]);

    return {
      success: true,
      message: "Registration successful!"
    };
  }

  function cancelRegistration(registrationId) {
    setRegistrations((previousRegistrations) =>
      previousRegistrations.filter(
        (item) => item.id !== registrationId
      )
    );
  }

  function getAvailableSeats(eventId) {

    const selectedEvent = initialEvents.find(
      (event) => event.id === eventId
    );

    if (!selectedEvent) {
      return 0;
    }

    const registeredCount = registrations.filter(
      (item) => item.eventId === eventId
    ).length;

    return selectedEvent.capacity - registeredCount;
  }

  return (
    <RegistrationContext.Provider
      value={{
        events: initialEvents,
        registrations,
        addRegistration,
        cancelRegistration,
        getAvailableSeats
      }}
    >
      {children}
    </RegistrationContext.Provider>
  );
}

export function useRegistration() {
  return useContext(RegistrationContext);
}
