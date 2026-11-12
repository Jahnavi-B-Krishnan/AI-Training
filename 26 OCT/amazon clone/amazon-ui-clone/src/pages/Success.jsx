import { Link, useLocation } from "react-router-dom";
import { PackageCheck } from "lucide-react";

const money = (amount) =>
  new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0
  }).format(amount);

export default function Success() {
  const location = useLocation();
  const total = location.state?.total;

  return (
    <main className="success-page">
      <Link to="/" className="login-logo">
        shop<span>zone</span><small>.in</small>
      </Link>

      <section className="success-card">
        <div className="success-check">✓</div>

        <p className="eyebrow">ORDER CONFIRMED</p>

        <h1>Order placed successfully!</h1>

        <p>
          Thank you for shopping with ShopZone.
          Your demo order has been confirmed.
        </p>

        {total != null && (
          <div className="order-total">
            <span>Order total</span>
            <strong>{money(total)}</strong>
          </div>
        )}

        <div className="success-details">
          <PackageCheck size={24} />

          <div>
            <strong>What's next?</strong>
            <p>
              Your order has been confirmed in this demo.
              A real store would send you an order confirmation.
            </p>
          </div>
        </div>

        <Link to="/" className="primary-button full">
          Continue shopping
        </Link>

        <p className="demo-disclaimer">
          No real payment was processed.
        </p>
      </section>
    </main>
  );
}