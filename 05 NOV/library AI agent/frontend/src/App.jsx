
import { useState } from "react";
import {
  Send,
  Bot,
  User,
  BookOpen,
  Sparkles,
  LoaderCircle,
  CheckCircle,
  XCircle,
  Library
} from "lucide-react";

import "./App.css";

const API = "http://localhost:8000";

function App() {

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hello! I'm Libra AI. I can help you search for books and make reservations. What are you looking for today?"
    }
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [pending, setPending] = useState(null);

  async function sendMessage(text = input) {

    if (!text.trim() || loading) return;

    setMessages(prev => [
      ...prev,
      { role: "user", text }
    ]);

    setInput("");
    setLoading(true);

    try {

      const response = await fetch(`${API}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: text
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong");
      }

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          text: data.reply,
          tools: data.tools_used
        }
      ]);

      setPending(data.pending_reservation);

    } catch (error) {

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          text: "Error: " + error.message
        }
      ]);

    } finally {
      setLoading(false);
    }
  }


  async function handleReservation(confirmed) {

    if (!pending || loading) return;

    setLoading(true);

    try {

      const response = await fetch(
        `${API}/confirm-reservation`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            book_id: pending.book_id,
            customer_name: pending.customer_name,
            confirmed: confirmed
          })
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Reservation failed");
      }

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          text: data.status === "success"
            ? `Reservation confirmed! Your reservation ID is ${data.reservation.reservation_id}. ${data.reservation.book_title} has been reserved for ${data.reservation.customer_name}.`
            : data.message
        }
      ]);

      setPending(null);

    } catch (error) {

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          text: "Error: " + error.message
        }
      ]);

    } finally {
      setLoading(false);
    }
  }


  const suggestions = [
    "Find books related to Python",
    "Show artificial intelligence books",
    "Is Python Crash Course available?",
    "Reserve Python Crash Course for Ahmed"
  ];


  return (

    <div className="app">

      {/* Sidebar */}

      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">
            <Library size={25} />
          </div>

          <div>
            <h2>Libra AI</h2>
            <span>Smart Library Assistant</span>
          </div>
        </div>

        <button
          className="new-chat"
          onClick={() => {
            setMessages([
              {
                role: "assistant",
                text: "Hello! I'm Libra AI. What would you like to find today?"
              }
            ]);
            setPending(null);
          }}
        >
          + New Conversation
        </button>

        <div className="sidebar-section">
          <p>QUICK ACTIONS</p>

          {suggestions.map((item, index) => (
            <button
              key={index}
              className="suggestion"
              onClick={() => sendMessage(item)}
              disabled={loading}
            >
              <BookOpen size={16} />
              {item}
            </button>
          ))}
        </div>

        <div className="sidebar-bottom">
          <div className="online-dot"></div>
          AI Assistant Ready
        </div>

      </aside>


      {/* Main Chat */}

      <main className="main">

        <header className="topbar">

          <div>
            <h3>Library Assistant</h3>
            <p>Search, discover and reserve books</p>
          </div>

          <div className="status">
            <span></span> Online
          </div>

        </header>


        <section className="chat-area">

          {messages.map((message, index) => (

            <div
              key={index}
              className={`message ${message.role}`}
            >

              <div className="avatar">
                {message.role === "assistant"
                  ? <Bot size={20} />
                  : <User size={20} />
                }
              </div>

              <div className="message-content">

                <div className="message-name">
                  {message.role === "assistant"
                    ? "Libra AI"
                    : "You"}
                </div>

                <div className="message-bubble">
                  {message.text}
                </div>

                {message.tools?.length > 0 && (

                  <div className="tool-info">
                    <Sparkles size={14} />

                    Tools used: {[
                      ...new Set(message.tools)
                    ].join(", ")}

                  </div>

                )}

              </div>

            </div>

          ))}


          {loading && (

            <div className="loading">
              <LoaderCircle className="spin" size={20} />
              Libra AI is thinking...
            </div>

          )}


          {pending && (

            <div className="confirmation-card">

              <h3>
                <BookOpen size={20} />
                Confirm Reservation
              </h3>

              <p>
                Would you like to reserve
                <strong> {pending.book_title}</strong>?
              </p>

              <div className="reservation-details">
                <p>
                  Customer: {pending.customer_name}
                </p>

                <p>
                  Book ID: {pending.book_id}
                </p>

                <p>
                  Available copies: {pending.available_copies}
                </p>
              </div>

              <div className="confirmation-actions">

                <button
                  className="confirm-btn"
                  onClick={() => handleReservation(true)}
                  disabled={loading}
                >
                  <CheckCircle size={17} />
                  Confirm
                </button>

                <button
                  className="cancel-btn"
                  onClick={() => handleReservation(false)}
                  disabled={loading}
                >
                  <XCircle size={17} />
                  Cancel
                </button>

              </div>

            </div>

          )}

        </section>


        {/* Input */}

        <footer className="input-area">

          <div className="input-box">

            <input
              type="text"
              placeholder="Ask me to find or reserve a book..."
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => {
                if (e.key === "Enter") sendMessage();
              }}
              disabled={loading || !!pending}
            />

            <button
              onClick={() => sendMessage()}
              disabled={loading || !input.trim() || !!pending}
            >
              <Send size={19} />
            </button>

          </div>

          <p>
            <Sparkles size={13} />
            Powered by OpenRouter AI
          </p>

        </footer>

      </main>

    </div>

  );
}

export default App;
