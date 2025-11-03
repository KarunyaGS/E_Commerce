import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getJSON } from "../api";

const Home = () => {
  const [categories, setCategories] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    getJSON("/api/categories/")
      .then(({ ok, data, status }) => {
        if (!ok) {
          console.error("Error fetching categories:", status, data);
          return;
        }
        if (data.results && Array.isArray(data.results)) {
          setCategories(data.results);
        } else if (Array.isArray(data)) {
          setCategories(data);
        }
      })
      .catch((err) => console.error("Error fetching categories:", err));
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <main className="flex-grow px-8 py-10">
        <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
          Happy Shoppy Categories
        </h1>

        {/* Category Grid */}
        <div className="row row-cols-2 row-cols-md-3 row-cols-lg-4 g-4 justify-content-center">
          {categories.map((cat) => (
            <div className="col" key={cat.ct_id}>
              <div
                onClick={() => navigate(`/category/${cat.ct_id}`)}
                className="card border-0 shadow-sm text-center h-100 category-card"
                style={{
                  borderRadius: "15px",
                  cursor: "pointer",
                  transition: "all 0.3s ease-in-out",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "translateY(-6px)";
                  e.currentTarget.style.boxShadow =
                    "0 8px 20px rgba(0,0,0,0.15)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "translateY(0)";
                  e.currentTarget.style.boxShadow =
                    "0 4px 10px rgba(0,0,0,0.1)";
                }}
              >
                <div className="card-body">
                  <h5 className="card-title text-primary fw-bold">
                    {cat.ct_name}
                  </h5>
                  <p className="card-text text-muted small">
                    {cat.ct_description}
                  </p>
                  <p className="text-secondary small mt-2">
                    Updated on:{" "}
                    {new Date(cat.ct_date).toLocaleDateString("en-GB")}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>

      <footer className="bg-gray-100 text-center py-3 text-sm text-gray-500 border-t">
        © {new Date().getFullYear()} Happy Shoppy Categories | Contact
      </footer>
    </div>
  );
};

export default Home;
