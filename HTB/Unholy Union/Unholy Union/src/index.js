const express = require("express");
const path = require("path");
const mysql = require("mysql2/promise");
const app = express();

// Create a MySQL connection pool
const pool = mysql.createPool({
  host: "127.0.0.1",
  user: "user",
  password: "user_password",
  database: "halloween_invetory",
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});

app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content-Type, Accept",
  );
  next();
});

app.use(express.static(path.join(__dirname, "public")));

app.get("/", async (req, res) => {
  const query = req.query.query ? req.query.query : "";
  let results = { status: null, message: null };

  res.sendFile(path.join(__dirname, "views", "index.html"));
});

app.get("/search", async (req, res) => {
  const query = req.query.query ? req.query.query : "";
  let results = { status: null, message: null };

  try {
    let sqlQuery;

    if (query === "") {
      sqlQuery = "SELECT * FROM inventory";
    } else {
      sqlQuery = `SELECT * FROM inventory WHERE name LIKE '%${query}%'`;
    }

    const [rows] = await pool.query(sqlQuery);
    results.status = "success";
    results.message = rows;
  } catch (err) {
    console.error("Error executing query:", err.stack);
    results.status = "failed";
    results.message = err.message;
  }

  return res.json(results);
});

app.use((req, res) => {
  res.sendFile(path.join(__dirname, "views", "404.html"));
});

app.listen(3000, () => {
  console.log(`Proxy server is running on http://localhost:3000`);
});
