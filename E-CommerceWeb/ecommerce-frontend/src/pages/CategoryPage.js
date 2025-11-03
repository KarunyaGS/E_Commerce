import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function CategoryPage() {
  const { ct_id } = useParams();
  const [products, setProducts] = useState([]);
  const [next, setNext] = useState(null);
  const [prev, setPrev] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/products/?ct=${ct_id}`)
      .then(res => res.json())
      .then(data => {
        setProducts(data.results);
        setNext(data.next);
        setPrev(data.previous);
      })
      .catch(err => console.error(err));
  }, [ct_id]);

  const fetchPage = (url) => {
    fetch(url)
      .then(res => res.json())
      .then(data => {
        setProducts(data.results);
        setNext(data.next);
        setPrev(data.previous);
      });
  };

  return (
    <div style={{ textAlign: "center", marginTop: "30px" }}>
      <h2>Products in Category {ct_id}</h2>
      <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "15px", marginTop: "20px" }}>
        {products.map(p => (
          <div key={p.pdt_id} style={{ border: "1px solid gray", borderRadius: "10px", padding: "10px", width: "200px" }}>
            <h4>{p.pdt_name}</h4>
            <p>MRP: ₹{p.pdt_mrp}</p>
            <p>Discount Price: ₹{p.pdt_dis_price}</p>
            <p>Quantity: {p.pdt_qty}</p>
          </div>
        ))}
      </div>
      <div style={{ marginTop: "20px" }}>
        {prev && <button onClick={() => fetchPage(prev)} style={{ marginRight: "10px" }}>Previous</button>}
        {next && <button onClick={() => fetchPage(next)}>Next</button>}
      </div>
    </div>
  );
}

export default CategoryPage;
