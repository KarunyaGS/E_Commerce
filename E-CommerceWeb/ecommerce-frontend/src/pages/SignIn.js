import React, { useState } from "react";
import { postJSON } from "../api";
import { useNavigate, Link } from "react-router-dom";

export default function SignIn({ onAuth }) {
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const { ok, status, data } = await postJSON("/api/login/", form);

      if (ok && data.access) {
        // Store JWT tokens
        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);
        localStorage.setItem("authUser", data.user.username);
        if (onAuth) onAuth({ username: data.user.username });
        navigate("/");
      } else {
        setError((data && data.detail) ? data.detail : "Invalid email or password");
      }
    } catch (err) {
      setError("Network error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6 col-lg-4">
          <div className="card">
            <div className="card-header bg-success text-white text-center">
              <div className="card-body p-4">
                <h3 className="card-title text-center mb-4">Sign In to Happy Shoppy Categories</h3>
              </div>
            </div>
            <div className="card-body">
              {error && (
                <div className="alert alert-danger" role="alert">
                  {error}
                </div>
              )}
              
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="email" className="form-label">Email Address</label>
                  <input 
                    id="email"
                    name="email" 
                    type="email"
                    className="form-control" 
                    placeholder="Enter your email" 
                    value={form.email} 
                    onChange={handleChange} 
                    required 
                  />
                </div>

                <div className="mb-4">
                  <label htmlFor="password" className="form-label">Password</label>
                  <input 
                    id="password"
                    name="password" 
                    type="password" 
                    className="form-control" 
                    placeholder="Enter your password" 
                    value={form.password} 
                    onChange={handleChange} 
                    required 
                  />
                </div>

                <button 
                  className="btn btn-success w-100 mb-3" 
                  type="submit" 
                  disabled={loading}
                >
                  {loading ? "Signing in..." : "Sign In"}
                </button>
              </form>

              <div className="text-center">
                <p className="mb-0 text-muted">
                  Don't have an account? 
                  <Link to="/signup" className="text-success text-decoration-none ms-1">
                    Sign Up
                  </Link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}







// import React, { useState } from "react";

// function SignIn() {
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");

//   const handleSubmit = (e) => {
//     e.preventDefault();
//     console.log("Sign-in:", email, password);
//     // Later: validate with Django and get JWT token
//   };

//   return (
//     <div className="container mt-5" style={{ maxWidth: "400px" }}>
//       <h3 className="text-center mb-4">Sign In</h3>
//       <form onSubmit={handleSubmit}>
//         <input
//           type="email"
//           placeholder="Email"
//           className="form-control mb-3"
//           onChange={(e) => setEmail(e.target.value)}
//           required
//         />
//         <input
//           type="password"
//           placeholder="Password"
//           className="form-control mb-3"
//           onChange={(e) => setPassword(e.target.value)}
//           required
//         />
//         <button type="submit" className="btn btn-success w-100">
//           Sign In
//         </button>
//       </form>
//     </div>
//   );
// }

// export default SignIn;
