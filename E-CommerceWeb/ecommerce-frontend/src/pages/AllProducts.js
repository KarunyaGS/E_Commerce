import React, { useEffect, useState } from "react";
import { getJSON } from "../api";

function AllProducts() {
  const [products, setProducts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const productsPerPage = 5;

  useEffect(() => {
    getJSON("/api/products/")
      .then(({ ok, data, status }) => {
        if (!ok) {
          console.error("Error fetching products:", status, data);
          return;
        }
        // Handle both paginated or direct array responses
        const results = data.results || data;
        setProducts(Array.isArray(results) ? results : []);
      })
      .catch((err) => console.error("Error fetching products:", err));
  }, []);

  // Pagination logic
  const totalPages = Math.ceil(products.length / productsPerPage);
  const startIndex = (currentPage - 1) * productsPerPage;
  const currentProducts = products.slice(startIndex, startIndex + productsPerPage);

  const goToFirst = () => setCurrentPage(1);
  const goToLast = () => setCurrentPage(totalPages);
  const goToPrevious = () => setCurrentPage((prev) => Math.max(prev - 1, 1));
  const goToNext = () => setCurrentPage((prev) => Math.min(prev + 1, totalPages));

  return (
    <div className="p-5 text-center">
      <h1 className="text-3xl font-bold mb-5 text-gray-800">All Products</h1>

      {/* Product Grid */}
      <div className="row row-cols-2 row-cols-md-3 row-cols-lg-4 g-4 justify-content-center">
        {currentProducts.map((p) => (
          <div
            key={p.pdt_id}
            className="bg-white shadow-md rounded-xl p-4 w-64 cursor-pointer hover:shadow-lg hover:scale-105 transition-transform"
          >
            <h2 className="fw-bold text-primary mb-2">{p.pdt_name}</h2>
            <p className="mb-1"><strong>MRP:</strong> ₹{p.pdt_mrp}</p>
            <p className="mb-1"><strong>Discount:</strong> ₹{p.pdt_dis_price}</p>
            <p className="mb-1"><strong>Qty:</strong> {p.pdt_qty}</p>
          </div>
        ))}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="d-flex justify-content-center align-items-center mt-4 flex-wrap gap-2">
          <button
            className="btn btn-outline-primary btn-sm"
            onClick={goToFirst}
            disabled={currentPage === 1}
          >
            First
          </button>
          <button
            className="btn btn-outline-primary btn-sm"
            onClick={goToPrevious}
            disabled={currentPage === 1}
          >
            Previous
          </button>

          {/* Numbered Pagination */}
          {Array.from({ length: totalPages })
            .slice(
              Math.max(0, currentPage - 3),
              Math.min(totalPages, currentPage + 2)
            )
            .map((_, i, arr) => {
              const pageNumber = i + 1 + Math.max(0, currentPage - 3);
              return (
                <button
                  key={pageNumber}
                  onClick={() => setCurrentPage(pageNumber)}
                  className={`btn btn-sm ${
                    currentPage === pageNumber
                      ? "btn-primary text-white"
                      : "btn-outline-primary"
                  }`}
                >
                  {pageNumber}
                </button>
              );
            })}

          <button
            className="btn btn-outline-primary btn-sm"
            onClick={goToNext}
            disabled={currentPage === totalPages}
          >
            Next
          </button>
          <button
            className="btn btn-outline-primary btn-sm"
            onClick={goToLast}
            disabled={currentPage === totalPages}
          >
            Last
          </button>
        </div>
      )}
    </div>
  );
}

export default AllProducts;
