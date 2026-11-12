import { Link, useNavigate } from "react-router-dom";
import Header from "../components/Header";
import { useCart } from "../context/CartContext";

const money = (amount) =>
  new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0
  }).format(amount);

export default function Cart() {
  const {
    cart,
    changeQuantity,
    removeFromCart,
    subtotal,
    cartCount
  } = useCart();

  const navigate = useNavigate();

  return (
    <>
      <Header />

      <main className="page-wrap">
        <section className="cart-panel">
          <h1>Shopping Cart</h1>

          {cart.length === 0 ? (
            <div className="empty-cart">
              <span>🛒</span>
              <h2>Your cart is empty</h2>
              <p>Discover something you'll love.</p>

              <Link to="/" className="primary-button">
                Continue shopping
              </Link>
            </div>
          ) : (
            <>
              {cart.map((item) => (
                <div className="cart-item" key={item.id}>
                  <div
                    className="cart-art"
                    style={{ background: item.color }}
                  >
                    {item.emoji}
                  </div>

                  <div className="cart-item-info">
                    <h3>{item.title}</h3>
                    <p className="stock">In stock</p>

                    <div className="quantity">
                      <button
                        onClick={() =>
                          changeQuantity(item.id, -1)
                        }
                      >
                        −
                      </button>

                      <strong>{item.quantity}</strong>

                      <button
                        onClick={() =>
                          changeQuantity(item.id, 1)
                        }
                      >
                        +
                      </button>

                      <button
                        className="remove"
                        onClick={() =>
                          removeFromCart(item.id)
                        }
                      >
                        Delete
                      </button>
                    </div>
                  </div>

                  <strong className="cart-price">
                    {money(item.price * item.quantity)}
                  </strong>
                </div>
              ))}

              <div className="subtotal-line">
                Subtotal ({cartCount} items):{" "}
                <strong>{money(subtotal)}</strong>
              </div>

              <button
                className="primary-button"
                onClick={() =>
                  navigate("/login?next=checkout")
                }
              >
                Proceed to Payment
              </button>
            </>
          )}
        </section>
      </main>
    </>
  );
}