import React from "react";
import { Link } from "react-router-dom";

const Welcome = () => {
  return (
    <div className="d-flex flex-column align-items-center justify-content-center" style={{ height: "80vh" }}>
      <h1 className="mb-4">WELCOME!</h1>
      <h3 className="mb-4">To Happy Shoppy</h3>
      <div>
        <Link to="/signin" className="btn btn-outline-success mx-2 px-4">Sign In</Link>
        <Link to="/signup" className="btn btn-outline-primary px-4">Sign Up</Link>
      </div>
    </div>
  );
};

export default Welcome;
