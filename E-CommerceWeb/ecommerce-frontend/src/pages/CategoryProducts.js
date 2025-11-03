import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getJSON } from "../api";

const CategoryProducts = () => {
  const { id } = useParams();
  const [products, setProducts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const productsPerPage = 5;

  useEffect(() => {
    getJSON(`/api/products/?ct_id=${id}`)
      .then(({ ok, data, status }) => {
        if (!ok) {
          console.error("Error fetching products:", status, data);
          return;
        }
        if (data.results && Array.isArray(data.results)) {
          setProducts(data.results);
        } else if (Array.isArray(data)) {
          setProducts(data);
        }
      })
      .catch((err) => console.error("Error fetching products:", err));
  }, [id]);

  // Pagination logic
  const indexOfLast = currentPage * productsPerPage;
  const indexOfFirst = indexOfLast - productsPerPage;
  const currentProducts = products.slice(indexOfFirst, indexOfLast);

//   return (
//     <div className="p-6 text-center">
//       <h1 className="text-2xl font-bold mb-4">Products</h1>
//       <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
//         {currentProducts.map((p) => (
//           <div
//             key={p.pdt_id}
//             className="border rounded-lg shadow-md p-4 bg-white"
//           >
//             <h2 className="font-semibold text-lg">{p.pdt_name}</h2>
//             <p>MRP: ₹{p.pdt_mrp}</p>
//             <p>Discount Price: ₹{p.pdt_dis_price}</p>
//             <p>Quantity: {p.pdt_qty}</p>
//           </div>
//         ))}
//       </div>

//       {/* Pagination buttons */}
//       <div className="mt-4">
//         {Array.from({ length: Math.ceil(products.length / productsPerPage) }).map(
//           (_, i) => (
//             <button
//               key={i}
//               onClick={() => setCurrentPage(i + 1)}
//               className={`px-3 py-1 mx-1 border rounded ${
//                 currentPage === i + 1
//                   ? "bg-blue-500 text-white"
//                   : "bg-white text-blue-500"
//               }`}
//             >
//               {i + 1}
//             </button>
//           )
//         )}
//       </div>
//     </div>
//   );
return (
  <div className="container py-5 text-center">
    <h1 className="fw-bold mb-5">Products</h1>

    {/* Product grid layout */}
    <div className="row row-cols-2 row-cols-md-3 row-cols-lg-4 g-4 justify-content-center">
      {currentProducts.map((p) => (
        <div className="col" key={p.pdt_id}>
          <div
            className="card border-0 shadow-sm h-100"
            style={{
              borderRadius: "15px",
              cursor: "pointer",
              transition: "all 0.3s ease-in-out",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-6px)";
              e.currentTarget.style.boxShadow = "0 8px 20px rgba(0,0,0,0.15)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow = "0 4px 10px rgba(0,0,0,0.1)";
            }}
          >
            <div className="card-body text-center">
              <h5 className="card-title text-primary fw-bold">{p.pdt_name}</h5>
              <p className="card-text text-muted small mb-1">
                <strong>MRP:</strong> ₹{p.pdt_mrp}
              </p>
              <p className="card-text text-success small mb-1">
                <strong>Discount:</strong> ₹{p.pdt_dis_price}
              </p>
              <p className="card-text text-secondary small">
                <strong>Qty:</strong> {p.pdt_qty}
              </p>
            </div>
          </div>
        </div>
      ))}
    </div>

    {/* Pagination buttons */}
    <div className="mt-4">
      {Array.from({ length: Math.ceil(products.length / productsPerPage) }).map(
        (_, i) => (
          <button
            key={i}
            onClick={() => setCurrentPage(i + 1)}
            className={`btn btn-sm mx-1 ${
              currentPage === i + 1
                ? "btn-primary text-white"
                : "btn-outline-primary"
            }`}
          >
            {i + 1}
          </button>
        )
      )}
    </div>
  </div>
);

};

export default CategoryProducts;
