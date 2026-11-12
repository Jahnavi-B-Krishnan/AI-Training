import { Link, useNavigate } from "react-router-dom";
import { Search, ShoppingCart, MapPin } from "lucide-react";
import { useState } from "react";
import { useCart } from "../context/CartContext";

export default function Header() {
  const [search, setSearch] = useState("");
  const { cartCount } = useCart();
  const navigate = useNavigate();

  function handleSearch(e) {
    e.preventDefault();
    navigate(`/?q=${encodeURIComponent(search.trim())}`);
  }

  return (
    <>
      <header className="topbar">
        <Link to="/" className="brand">
          shop<span>zone</span><small>.in</small>
        </Link>

        <div className="deliver">
          <MapPin size={17} />
          <div>
            <small>Deliver to</small>
            <strong>India</strong>
          </div>
        </div>

        <form className="searchbar" onSubmit={handleSearch}>
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search ShopZone"
            aria-label="Search products"
          />
          <button type="submit" aria-label="Search">
            <Search size={21} />
          </button>
        </form>

        <Link to="/login" className="account-link">
          <small>Hello, sign in</small>
          <strong>Account & Lists</strong>
        </Link>

        <Link to="/cart" className="cart-link">
          <span className="cart-count">{cartCount}</span>
          <ShoppingCart size={27} />
          <strong>Cart</strong>
        </Link>
      </header>

      <nav className="subnav">
        <Link to="/">All</Link>
        <a href="/#products">Today's Deals</a>
        <a href="/#products">Electronics</a>
        <a href="/#products">Fashion</a>
        <a href="/#products">Home & Kitchen</a>
      </nav>
    </>
  );
}