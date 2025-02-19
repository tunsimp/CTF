function updateQuery() {
  const query = document.getElementById("searchInput").value;
  let sqlQuery;

  // If the query is empty, show the full inventory query
  if (query === "") {
    sqlQuery = "SELECT * FROM inventory";
  } else {
    sqlQuery = `SELECT * FROM inventory WHERE name LIKE '%${query}%'`;
  }

  // Update the SQL query and re-highlight using Prism.js
  const debugQuery = document.getElementById("debugQuery");
  debugQuery.textContent = sqlQuery;
  Prism.highlightElement(debugQuery); // Re-highlight the SQL query
}

async function performQuery() {
  const query = document.querySelector("input").value;
  const container = document.getElementById("resultsContainer");

  // Perform the fetch request with the user's input
  const response = await fetch("/search?query=" + query).then((response) =>
    response.json(),
  );

  console.log(response.message);
  console.log(response.status);

  // Check if the message is empty
  if (
    response.status === "success" &&
    response.message &&
    response.message.length > 0
  ) {
    const results = response.message;
    const table = document.createElement("table");
    table.setAttribute("class", "table table-bordered");
    const tableHeader = document.createElement("tr");

    const headers = Object.keys(results[0]);
    headers.forEach((header) => {
      const th = document.createElement("th");
      th.textContent = header;
      tableHeader.appendChild(th);
    });

    table.appendChild(tableHeader);

    results.forEach((row) => {
      const tableRow = document.createElement("tr");
      headers.forEach((header) => {
        const td = document.createElement("td");
        td.textContent = row[header];
        tableRow.appendChild(td);
      });
      table.appendChild(tableRow);
    });

    container.innerHTML = "";
    container.appendChild(table);
  } else {
    // If the response is empty, display "Cannot find"
    container.innerHTML = `<p class="warning">Cannot find any matching items.</p>`;
  }

  // Update and highlight the SQL query in real-time based on user input
  updateQuery();

  // Highlight the JSON response (output)
  const debugMessage = document.getElementById("debugMessage");
  debugMessage.textContent = JSON.stringify(
    response.message || "No data returned",
    null,
    2,
  );
  Prism.highlightElement(debugMessage); // Re-highlight the JSON output
}

document.addEventListener("DOMContentLoaded", () => {
  updateQuery(); // Highlight the initial query on load
});

const footer = document.getElementById("footer");
const minimize = document.getElementById("minimize");
const expand = document.getElementById("expand");
const fullscreen = document.getElementById("fullscreen");
const maincontent = document.getElementById("main-content");

expand.addEventListener("click", () => {
  footer.style.height = "45%";
  maincontent.style.padding = "0 0 30% 0";
});

minimize.addEventListener("click", () => {
  footer.style.height = "40px";
  maincontent.style.padding = "0";
});

fullscreen.addEventListener("click", () => {
  footer.style.height = "100%";
});
