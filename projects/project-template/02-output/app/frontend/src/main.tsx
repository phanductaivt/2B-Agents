import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

type Ticket = {
  id: string;
  passengerName: string;
  route: string;
  travelDate: string;
  departureDate: string;
  fareAmount: number;
  status: string;
};

type Quote = {
  ticketId: string;
  newTravelDate: string;
  fareDifference: number;
  changeFee: number;
  totalDue: number;
  paymentRequired: boolean;
};

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8000";

function App() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [ticketId, setTicketId] = useState("");
  const [newDate, setNewDate] = useState("2026-06-07");
  const [quote, setQuote] = useState<Quote | null>(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const selectedTicket = tickets.find((ticket) => ticket.id === ticketId);

  useEffect(() => {
    fetch(`${API_BASE}/tickets`)
      .then((response) => response.json())
      .then((items: Ticket[]) => {
        setTickets(items);
        setTicketId(items[0]?.id ?? "");
      })
      .catch(() => setMessage("Unable to load tickets. Check that the backend is running."));
  }, []);

  async function requestQuote() {
    setLoading(true);
    setMessage("");
    setQuote(null);
    const response = await fetch(`${API_BASE}/tickets/${ticketId}/change-quote`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ new_travel_date: newDate })
    });
    const body = await response.json();
    setLoading(false);
    if (!response.ok) {
      setMessage(body.detail?.message ?? "Unable to quote this date change.");
      return;
    }
    setQuote(body);
  }

  async function confirmChange() {
    setLoading(true);
    setMessage("");
    const response = await fetch(`${API_BASE}/tickets/${ticketId}/confirm-change`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ new_travel_date: newDate, payment_confirmed: true })
    });
    const body = await response.json();
    setLoading(false);
    if (!response.ok) {
      setMessage(body.detail?.message ?? "Unable to confirm this change.");
      return;
    }
    setMessage(`Ticket ${body.ticketId} changed. Confirmation sent.`);
  }

  return (
    <main className="shell">
      <section className="panel">
        <div>
          <p className="eyebrow">Self-service travel tools</p>
          <h1>Ticket date change</h1>
          <p className="summary">
            Select a confirmed ticket, choose a new date, review fees, then confirm the change.
          </p>
        </div>

        <label>
          Ticket
          <select value={ticketId} onChange={(event) => setTicketId(event.target.value)}>
            {tickets.map((ticket) => (
              <option key={ticket.id} value={ticket.id}>
                {ticket.id} - {ticket.route}
              </option>
            ))}
          </select>
        </label>

        {selectedTicket && (
          <div className="ticket">
            <span>{selectedTicket.passengerName}</span>
            <strong>{selectedTicket.route}</strong>
            <span>Current date: {selectedTicket.travelDate}</span>
            <span>Status: {selectedTicket.status}</span>
          </div>
        )}

        <label>
          New travel date
          <input value={newDate} onChange={(event) => setNewDate(event.target.value)} type="date" />
        </label>

        <div className="actions">
          <button onClick={requestQuote} disabled={!ticketId || loading}>
            View fee
          </button>
          <button onClick={confirmChange} disabled={!quote || loading}>
            Confirm and pay
          </button>
        </div>

        {quote && (
          <div className="quote">
            <div>
              <span>Fare difference</span>
              <strong>${quote.fareDifference}</strong>
            </div>
            <div>
              <span>Change fee</span>
              <strong>${quote.changeFee}</strong>
            </div>
            <div>
              <span>Total due</span>
              <strong>${quote.totalDue}</strong>
            </div>
          </div>
        )}

        {message && <p className="message">{message}</p>}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
