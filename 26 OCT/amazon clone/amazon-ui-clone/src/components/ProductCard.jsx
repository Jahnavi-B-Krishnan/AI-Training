import { Star } from "lucide-react";
import { useCart } from "../context/CartContext";

const money = (amount) =>
  new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0
  }).format(amount);

export default function ProductCard({ product }) {
  const { addToCart } = useCart();

  const discount = Math.round(
    (1 - product.price / product.oldPrice) * 100
  );

  return (
    <article className="product-card">
      
        <div className="product-image" style={{ backgroundColor: product.color || "#fff" }}>
        <img
            src={product.image}
            alt={product.title}
            loading="lazy"
            onError={(e) => {
            e.currentTarget.style.display = "none";
            }}
        />
        </div>

      <div className="product-info">
        <div className="category">{product.category}</div>

        <h3>{product.title}</h3>

        <div className="rating">
          {product.rating}
          <Star size={13} fill="currentColor" />
        </div>

        <div className="price">
          <strong>{money(product.price)}</strong>
          <del>{money(product.oldPrice)}</del>
        </div>

        <p className="discount">{discount}% off</p>

        <p className="delivery">
          FREE delivery <strong>Tomorrow</strong>
        </p>

        <button
          className="add-button"
          onClick={() => addToCart(product)}
        >
          Add to Cart
        </button>
      </div>
    </article>
  );
}