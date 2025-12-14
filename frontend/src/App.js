import { useState } from "react";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState(null);
  const [sweets, setSweets] = useState([]);
  const [isAdmin, setIsAdmin] = useState(false);
  const [searchName, setSearchName] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [newName, setNewName] = useState("");
  const [newCategory, setNewCategory] = useState("");
  const [newPrice, setNewPrice] = useState("");
  const [newQuantity, setNewQuantity] = useState("");



  const handleLogin = async () => {
  const response = await fetch("http://localhost:8000/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();
  setToken(data.access_token);

  // fetch /me to know if admin
  const meResponse = await fetch("http://localhost:8000/api/me", {
    headers: {
      Authorization: `Bearer ${data.access_token}`,
    },
  });

  const meData = await meResponse.json();
  setIsAdmin(meData.is_admin);
};


  const fetchSweets = async () => {
    const response = await fetch("http://localhost:8000/api/sweets", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const data = await response.json();
    setSweets(data);
  };

  const createSweet = async () => {
  await fetch("http://localhost:8000/api/sweets", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      name: newName,
      category: newCategory,
      price: Number(newPrice),
      quantity: Number(newQuantity),
    }),
  });

  setNewName("");
  setNewCategory("");
  setNewPrice("");
  setNewQuantity("");

    fetchSweets();
  };

  const purchaseSweet = async (sweetId) => {
    await fetch(
      `http://localhost:8000/api/sweets/${sweetId}/purchase`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    fetchSweets();
  };

const updateSweet = async (sweet) => {
  await fetch(`http://localhost:8000/api/sweets/${sweet.id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      name: sweet.name,
      category: sweet.category,
      price: sweet.price + 1,
      quantity: sweet.quantity,
    }),
  });

  fetchSweets();
};

  const deleteSweet = async (sweetId) => {
  await fetch(`http://localhost:8000/api/sweets/${sweetId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  fetchSweets();
};


const restockSweet = async (sweetId) => {
  try {
    const response = await fetch(
      `http://localhost:8000/api/sweets/${sweetId}/restock?quantity=5`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error("Restock failed");
    }

    fetchSweets(); // refresh list
  } catch (err) {
    console.error("Restock error:", err);
  }
};

const searchSweets = async () => {
  try {
    const response = await fetch(
      `http://localhost:8000/api/sweets/search?name=${searchName}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await response.json();
    setSweets(data);
  } catch (err) {
    console.error("Search failed:", err);
  }
};

const searchByPrice = async () => {
  const response = await fetch(
    `http://localhost:8000/api/sweets/search?min_price=${minPrice}&max_price=${maxPrice}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await response.json();
  setSweets(data);
};


  return (
    <div style={{ padding: "40px", maxWidth: "500px", margin: "auto" }}>
      <h2>Sweet Shop</h2>

      {!token && (
        <>
          <input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ width: "100%", marginBottom: "8px" }}
          />
          <input
            placeholder="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: "100%", marginBottom: "8px" }}
          />
          <button onClick={handleLogin} style={{ width: "100%" }}>
            Login
          </button>
        </>
      )}

      {token && (
        <>

<input
  placeholder="Search sweet by name"
  value={searchName}
  onChange={(e) => setSearchName(e.target.value)}
  style={{ width: "100%", marginTop: "20px" }}
/>

<button onClick={searchSweets} style={{ width: "100%", marginTop: "8px" }}>
  Search
</button>


          <button onClick={fetchSweets} style={{ marginTop: "20px" }}>
            Load Sweets
          </button>
<input
  placeholder="Min price"
  value={minPrice}
  onChange={(e) => setMinPrice(e.target.value)}
  style={{ width: "100%", marginTop: "8px" }}
/>

<input
  placeholder="Max price"
  value={maxPrice}
  onChange={(e) => setMaxPrice(e.target.value)}
  style={{ width: "100%", marginTop: "8px" }}
/>

<button onClick={searchByPrice} style={{ width: "100%", marginTop: "8px" }}>
  Search by Price
</button>

{isAdmin && (
  <div style={{ border: "1px solid #ccc", padding: "10px", marginTop: "20px" }}>
    <h3>Add New Sweet</h3>

    <input
      placeholder="Name"
      value={newName}
      onChange={(e) => setNewName(e.target.value)}
      style={{ width: "100%", marginBottom: "6px" }}
    />

    <input
      placeholder="Category"
      value={newCategory}
      onChange={(e) => setNewCategory(e.target.value)}
      style={{ width: "100%", marginBottom: "6px" }}
    />

    <input
      placeholder="Price"
      type="number"
      value={newPrice}
      onChange={(e) => setNewPrice(e.target.value)}
      style={{ width: "100%", marginBottom: "6px" }}
    />

    <input
      placeholder="Quantity"
      type="number"
      value={newQuantity}
      onChange={(e) => setNewQuantity(e.target.value)}
      style={{ width: "100%", marginBottom: "6px" }}
    />

    <button onClick={createSweet} style={{ width: "100%" }}>
      Add Sweet
    </button>
  </div>
)}



          {sweets.map((sweet) => (
            <div
              key={sweet.id}
              style={{
                border: "1px solid #ccc",
                padding: "10px",
                marginTop: "10px",
              }}
            >
              <h3>{sweet.name}</h3>
              <p>Category: {sweet.category}</p>
              <p>Price: {sweet.price}</p>
              <p>Quantity: {sweet.quantity}</p>

              <button
                onClick={() => purchaseSweet(sweet.id)}
                disabled={sweet.quantity === 0}
              >
                Purchase
              </button>

{isAdmin && (
  <div style={{ marginTop: "8px" }}>
    <button
  onClick={() => updateSweet(sweet)}
  style={{ width: "100%" }}
>
  Increase Price (+1)
</button>
  </div>
)}


{isAdmin && (
  <button
    onClick={() => deleteSweet(sweet.id)}
    style={{
      marginTop: "6px",
      backgroundColor: "red",
      color: "white",
      width: "100%",
    }}
  >
    Delete
  </button>
)}

{isAdmin && (
  <button
    onClick={() => restockSweet(sweet.id)}
    style={{
      marginTop: "6px",
      backgroundColor: "green",
      color: "white",
      width: "100%",
    }}
  >
    Restock +5
  </button>
)}


            </div>
          ))}
        </>
      )}
    </div>
  );
}

export default App;
