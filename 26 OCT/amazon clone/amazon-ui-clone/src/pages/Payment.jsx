import { Link, useNavigate } from "react-router-dom";
import { ShieldCheck } from "lucide-react";
import { useCart } from "../context/CartContext";

const money = (amount) =>
  new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0
  }).format(amount);

export default function Payment() {
  const { cart, subtotal, clearCart, cartCount } = useCart();
  const navigate = useNavigate();

  function handlePayment() {
    if (cart.length === 0) {
      navigate("/cart");
      return;
    }

    const orderTotal = subtotal;

    // Demo only: no real payment is processed.
    clearCart();

    navigate("/success", {
      state: { total: orderTotal }
    });
  }

  return (
    <main className="login-page">
      <Link to="/" className="login-logo">
        shop<span>zone</span><small>.in</small>
      </Link>

      <section className="login-card payment-card">
        <h1>Payment</h1>

        <p className="login-intro">
          Review your order before confirming.
        </p>

        {cart.length === 0 ? (
          <>
            <p>Your cart is empty.</p>

            <Link to="/" className="primary-button full">
              Continue shopping
            </Link>
          </>
        ) : (
          <>
            <div className="payment-items">
              {cart.map((item) => (
                <div className="payment-item" key={item.id}>
                  <span>
                    {item.emoji} {item.title} × {item.quantity}
                  </span>

                  <strong>
                    {money(item.price * item.quantity)}
                  </strong>
                </div>
              ))}
            </div>

            <div className="order-total">
              <span>Items ({cartCount})</span>
              <strong>{money(subtotal)}</strong>
            </div>

            <div className="order-total">
              <span>Delivery</span>
              <strong>FREE</strong>
            </div>

            <div className="order-total">
              <span>Total payable</span>
              <strong>{money(subtotal)}</strong>
            </div>

            <div className="demo-tip">
              <ShieldCheck size={20} />

              <p>
                Demo checkout only. No card details are
                collected and no real payment is processed.
              </p>
            </div>

            <button
              className="primary-button full"
              onClick={handlePayment}
            >
              Confirm Demo Payment
            </button>

            <Link to="/cart" className="secondary-button full">
              Back to Cart
            </Link>
          </>
        )}
      </section>
    </main>
  );
}