import React, { useState } from "react";
import { postJSON } from "../api";
import { useNavigate, Link } from "react-router-dom";

export default function SignUp() {
  const [form, setForm] = useState({ 
    username: "", 
    first_name: "", 
    last_name: "", 
    email: "", 
    password: "", 
    confirm_password: "" 
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const { ok, status, data } = await postJSON("/api/register/", form);
      
      if (ok) {
        // success — optionally show message then redirect to sign-in
        navigate("/signin");
      } else {
        // show server errors (could be validation errors)
        if (typeof data === "object") setError(JSON.stringify(data));
        else setError(data || `Error ${status}`);
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
            <div className="card-header bg-primary text-white text-center">
              <h4 className="mb-0">Create Account</h4>
              <p className="mb-0 mt-1">Join Happy Shoppy today!</p>
            </div>
            <div className="card-body">
              {error && (
                <div className="alert alert-danger" role="alert">
                  {error}
                </div>
              )}
              
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="first_name" className="form-label">First Name</label>
                  <input 
                    id="first_name"
                    name="first_name" 
                    className="form-control" 
                    placeholder="Enter first name" 
                    value={form.first_name} 
                    onChange={handleChange} 
                    required 
                  />
                </div>

                <div className="mb-3">
                  <label htmlFor="last_name" className="form-label">Last Name</label>
                  <input 
                    id="last_name"
                    name="last_name" 
                    className="form-control" 
                    placeholder="Enter last name" 
                    value={form.last_name} 
                    onChange={handleChange} 
                    required 
                  />
                </div>

                <div className="mb-3">
                  <label htmlFor="username" className="form-label">Username</label>
                  <input 
                    id="username"
                    name="username" 
                    className="form-control" 
                    placeholder="Enter username (min 3 characters)" 
                    value={form.username} 
                    onChange={handleChange} 
                    required 
                    minLength="3"
                  />
                </div>

                <div className="mb-3">
                  <label htmlFor="email" className="form-label">Email Address</label>
                  <input 
                    id="email"
                    name="email" 
                    type="email" 
                    className="form-control" 
                    placeholder="example@gmail.com" 
                    value={form.email} 
                    onChange={handleChange} 
                    required 
                  />
                </div>

                <div className="mb-3">
                  <label htmlFor="password" className="form-label">Create Password</label>
                  <input 
                    id="password"
                    name="password" 
                    type="password" 
                    className="form-control" 
                    placeholder="Enter password (min 3 characters)" 
                    value={form.password} 
                    onChange={handleChange} 
                    required 
                    minLength="3"
                  />
                </div>

                <div className="mb-4">
                  <label htmlFor="confirm_password" className="form-label">Confirm Password</label>
                  <input 
                    id="confirm_password"
                    name="confirm_password" 
                    type="password" 
                    className="form-control" 
                    placeholder="Confirm your password" 
                    value={form.confirm_password} 
                    onChange={handleChange} 
                    required 
                    minLength="3"
                  />
                </div>

                <button 
                  type="submit" 
                  className="btn btn-primary w-100 mb-3" 
                  disabled={loading}
                >
                  {loading ? "Creating Account..." : "Create Account"}
                </button>
              </form>

              <div className="text-center">
                <p className="mb-0 text-muted">
                  Already have an account? 
                  <Link to="/signin" className="text-primary text-decoration-none ms-1">
                    Sign In
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

// function SignUp() {
//   const [form, setForm] = useState({
//     firstName: "",
//     lastName: "",
//     email: "",
//     password: "",
//     confirmPassword: "",
//   });

//   const handleChange = (e) => {
//     setForm({ ...form, [e.target.name]: e.target.value });
//   };

//   const handleSubmit = (e) => {
//     e.preventDefault();
//     console.log("Form submitted:", form);
//     // Later: send to Django backend via API
//   };

//   return (
//     <div className="container mt-5" style={{ maxWidth: "400px" }}>
//       <h3 className="text-center mb-4">Sign Up</h3>
//       <form onSubmit={handleSubmit}>
//         <input
//           name="firstName"
//           placeholder="First Name"
//           className="form-control mb-2"
//           onChange={handleChange}
//           required
//         />
//         <input
//           name="lastName"
//           placeholder="Last Name"
//           className="form-control mb-2"
//           onChange={handleChange}
//           required
//         />
//         <input
//           type="email"
//           name="email"
//           placeholder="Email"
//           className="form-control mb-2"
//           onChange={handleChange}
//           required
//         />
//         <input
//           type="password"
//           name="password"
//           placeholder="Password"
//           className="form-control mb-2"
//           onChange={handleChange}
//           required
//         />
//         <input
//           type="password"
//           name="confirmPassword"
//           placeholder="Confirm Password"
//           className="form-control mb-3"
//           onChange={handleChange}
//           required
//         />
//         <button type="submit" className="btn btn-primary w-100">
//           Create Account
//         </button>
//       </form>
//     </div>
//   );
// }

// export default SignUp;
