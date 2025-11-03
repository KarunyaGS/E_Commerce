// src/pages/SearchResults.js
import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { getJSON } from "../api";

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

function SearchResults() {
  const query = useQuery();
  const location = useLocation();
  const searchTerm = query.get("q") || "";
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchEngine, setSearchEngine] = useState("api");
  const [searchStats, setSearchStats] = useState(null);

  useEffect(() => {
    // Check if we have direct Elasticsearch results from navigation state
    if (location.state?.results) {
      const { results, query, searchEngine: engine } = location.state;
      setProducts(results.products || []);
      setSearchEngine(engine || "elasticsearch-direct");
      setSearchStats({
        total: results.total,
        took: results.took,
        engine: engine
      });
      return;
    }

    // Fallback to API search
    if (!searchTerm) return;

    setLoading(true);
    setError(null);
    setSearchEngine("api");

    getJSON(`/api/search/?q=${encodeURIComponent(searchTerm)}`)
      .then(({ ok, data, status }) => {
        if (!ok) throw new Error(typeof data === "string" ? data : `Error ${status}`);
        setProducts(data.products || []);
        setSearchEngine(data.using || "api");
        setSearchStats({
          total: data.total || data.products?.length || 0,
          engine: data.using || "api"
        });
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [searchTerm, location.state]);

  return (
    <div className="container mt-4">
      <h4 className="mb-3">
        Search Results for: <span className="text-primary">{searchTerm}</span>
      </h4>

      {loading && (
        <div className="text-center my-5">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-2">Searching products...</p>
        </div>
      )}
      
      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}

      {!loading && !error && products.length === 0 && (
        <div className="alert alert-info" role="alert">
          <h5>No products found for "{searchTerm}"</h5>
          <p>Try searching with different keywords or check the spelling.</p>
        </div>
      )}

      {/* Products section - Only show products */}
      {!loading && products.length > 0 && (
        <>
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h5 className="mb-0">Found {products.length} product(s)</h5>
            <div className="d-flex flex-column align-items-end">
              {/* <span className={`badge ${searchEngine.includes('elasticsearch') ? 'bg-success' : 'bg-secondary'}`}>
                {searchEngine === 'elasticsearch-direct' ? '🚀 Direct Elasticsearch' : 
                 searchEngine === 'elasticsearch' ? '⚡ Elasticsearch API' : 
                 '🔍 Database Search'}
              </span> */}
              {searchStats?.took && (
                <small className="text-muted mt-1">
                  Search took {searchStats.took}ms
                </small>
              )}
            </div>
          </div>
          <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 row-cols-xl-4 g-4">
            {products.map((product) => (
              <div className="col" key={product.pdt_id}>
                <div className="card h-100 border shadow-sm">
                  <div className="card-body">
                    <h5 className="card-title text-primary">
                      {product.pdt_name}
                    </h5>
                    {product.category && (
                      <span className="badge bg-secondary mb-2">
                        {product.category}
                      </span>
                    )}
                    <div className="d-flex justify-content-between align-items-center">
                      <div>
                        {product.pdt_mrp && product.pdt_mrp !== product.pdt_dis_price && (
                          <p className="card-text text-muted text-decoration-line-through mb-0">
                            ₹{product.pdt_mrp}
                          </p>
                        )}
                        <p className="card-text text-success fw-bold fs-5 mb-0">
                          ₹{product.pdt_dis_price}
                        </p>
                      </div>
                      {product.score && (
                        <small className="text-muted">
                          Score: {product.score.toFixed(2)}
                        </small>
                      )}
                    </div>
                    {product.pdt_qty !== undefined && (
                      <small className="text-muted">
                        Stock: {product.pdt_qty > 0 ? `${product.pdt_qty} available` : 'Out of stock'}
                      </small>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default SearchResults;
