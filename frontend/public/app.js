fetch("/api/postgres_test")
    .then(r => r.json())
    .then(data => {
        document.getElementById("output").innerText =
            JSON.stringify(data, null, 2);
    });
