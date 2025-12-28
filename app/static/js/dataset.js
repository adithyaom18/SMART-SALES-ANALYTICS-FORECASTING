fetch("/active-dataset")
    .then(res => res.json())
    .then(data => {
        document.getElementById("datasetBadge").innerText =
            "📂 " + data.name;
    });
