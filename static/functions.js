function fetchData() {
    fetch("/data")
        .then(response => response.json())
        .then(data => {
            const marqueeElement = document.getElementById("ticker-marquee");
            marqueeElement.innerHTML = ""; // Clear previous data
            data.forEach(stock => {
                const symbolSpan = document.createElement("span");
                symbolSpan.classList.add("symbol");
                symbolSpan.textContent = `${stock.Name.toUpperCase()} : ${stock.LTP}`;

                const trendSpan = document.createElement("span");
                if (parseFloat(stock.LTP) > parseFloat(stock.Previous_Close)) {
                    trendSpan.style.color = "green";
                    trendSpan.textContent = "▲";
                } else if (parseFloat(stock.LTP) < parseFloat(stock.Previous_Close)) {
                    trendSpan.style.color = "red";
                    trendSpan.textContent = "▼";
                } else {
                    trendSpan.textContent = "↔";
                }

                symbolSpan.appendChild(trendSpan);
                marqueeElement.appendChild(symbolSpan);
            });
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
}

function addItem() {
    var name = document.getElementById("name").value;
    var code = document.getElementById("code").value;

    fetch('/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name, code: code })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Show a popup message
        document.getElementById("name").value = "";
        document.getElementById("code").value = "";
        updateItemList(); // Update the item list dynamically
        fetchData(); // Fetch updated stock data
    })
    .catch(error => console.error('Error:', error));
}

function updateItemList() {
    fetch("/stock_list")
        .then(response => response.json())
        .then(data => {
            const itemList = document.getElementById("item-list");
            itemList.innerHTML = ""; // Clear the current list

            // Rebuild the list with the updated data
            data.forEach(item => {
                const listItem = document.createElement("li");
                listItem.textContent = `${item.code} ${item.name} - `;
                const deleteButton = document.createElement("button");
                deleteButton.textContent = "Delete";
                deleteButton.onclick = function() {
                    deleteItem(item.id);
                };
                listItem.appendChild(deleteButton);
                itemList.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error("Error updating item list:", error);
        });
}

function deleteItem(id) {
    if (confirm("Are you sure you want to delete this item?")) {
        fetch(`/delete/${id}`, { method: 'GET' })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                updateItemList(); // Update the item list dynamically
            })
            .catch(error => console.error('Error:', error));
    }
}

// Initial fetch to populate the item list and stock data
updateItemList();
fetchData();
