import { useMemo, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import Header from "../components/Header";
import ProductCard from "../components/ProductCard";
import { products } from "../data";

export default function Home() {
  const location = useLocation();
  const query =
    new URLSearchParams(location.search).get("q") || "";

  const [category, setCategory] = useState("All");

  const filteredProducts = useMemo(() => {
    return products.filter((product) => {
      const matchesSearch =
        `${product.title} ${product.category}`
          .toLowerCase()
          .includes(query.toLowerCase());

      const matchesCategory =
        category === "All" ||
        product.category === category;

      return matchesSearch && matchesCategory;
    });
  }, [query, category]);

  return (
    <>
      <Header />

      <main>
        <section className="hero">
          <div className="hero-copy">
            <p className="eyebrow">
              THE EVERYDAY SHOPPING EVENT
            </p>

            <h1>
              Find your next
              <br />
              <span>favourite thing.</span>
            </h1>

            <p>
              Great products, great prices,
              delivered to your door.
            </p>

            <a href="#products" className="primary-button">
              Explore deals →
            </a>
          </div>

          <div className="hero-visual">
            <div className="hero-circle" />
            <span className="hero-emoji emoji-one">🎧</span>
            <span className="hero-emoji emoji-two">⌚</span>
            <span className="hero-emoji emoji-three">👟</span>
          </div>
        </section>

        <section className="benefits">
          <div>
            <strong>📦 Fast delivery</strong>
            <small>Delivered to your door</small>
          </div>

          <div>
            <strong>⭐ Great deals</strong>
            <small>Everyday favourites</small>
          </div>

          <div>
            <strong>🛒 Easy shopping</strong>
            <small>Simple checkout</small>
          </div>
        </section>

        <section id="products" className="catalog">
          <div className="section-heading">
            <div>
              <p className="eyebrow">CURATED FOR YOU</p>
              <h2>
                {query
                  ? `Results for "${query}"`
                  : "Popular products"}
              </h2>
            </div>

            <span>
              {filteredProducts.length} products
            </span>
          </div>

          <div className="filters">
            {["All", "Electronics", "Fashion", "Home"].map(
              (item) => (
                <button
                  key={item}
                  className={
                    category === item ? "active" : ""
                  }
                  onClick={() => setCategory(item)}
                >
                  {item}
                </button>
              )
            )}
          </div>

          {filteredProducts.length > 0 ? (
            <div className="product-grid">
              {filteredProducts.map((product) => (
                <ProductCard
                  key={product.id}
                  product={product}
                />
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <h3>No products found</h3>
              <p>Try another search term.</p>
              <Link to="/" className="primary-button">
                Show all products
              </Link>
            </div>
          )}
        </section>

        <footer>
          <strong>shopzone.in</strong>
          <span>React shopping UI demo</span>
          <a href="#products">Back to top ↑</a>
        </footer>
      </main>
    </>
  );
}