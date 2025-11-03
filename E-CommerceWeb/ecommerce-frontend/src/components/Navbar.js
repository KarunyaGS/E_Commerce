import React from "react";
import { Link, useNavigate } from "react-router-dom";

function Navbar({ user, setUser, searchTerm, setSearchTerm, onSearch }) {
const navigate = useNavigate();

const logout = () => {
localStorage.removeItem("isAuthenticated");
localStorage.removeItem("authUser");
setUser(null);
navigate("/");
};

return (
<nav className="navbar navbar-light bg-light px-3 shadow-sm d-flex justify-content-between align-items-center">
{/* LEFT SIDE */}
<div className="d-flex align-items-center">
<Link to="/" className="navbar-brand fw-bold text-primary me-3">
Happy Shoppy Categories
</Link>

    <>
      {user && (
        <Link
          to="/all-products"
          className="btn btn-outline-secondary btn-sm me-3"
        >
          View All Products
        </Link>
      )}

      <div className="input-group input-group-sm" style={{ width: "300px" }}>
        <input
          type="text"
          className="form-control form-control-sm"
          placeholder="Search electronics, clothing, laptops under 40000..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && onSearch()}
          title="Try: electronics, cloth, mobile phones, laptops under 50000"
        />
        <button className="btn btn-primary" onClick={onSearch}>
          🔍 Search
        </button>
      </div>
    </>
  </div>

  {/* RIGHT SIDE */}
  <div className="d-flex align-items-center">
    {user ? (
      <>
        <span className="me-3 text-muted">Hi, {user.username}</span>
        <button
          className="btn btn-outline-danger btn-sm"
          onClick={logout}
        >
          Logout
        </button>
      </>
    ) : (
      <>
        <Link to="/signin" className="btn btn-outline-success btn-sm mx-1">
          Sign In
        </Link>
        <Link to="/signup" className="btn btn-outline-primary btn-sm">
          Sign Up
        </Link>
      </>
    )}
  </div>
</nav>
);
}

export default Navbar;