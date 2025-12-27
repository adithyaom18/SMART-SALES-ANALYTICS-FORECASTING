fetch("/analytics-data")
    .then(response => response.json())
    .then(data => {

        // Monthly Sales Trend
        new Chart(document.getElementById("monthlySalesChart"), {
            type: "line",
            data: {
                labels: data.monthly.dates,
                datasets: [{
                    label: "Monthly Sales",
                    data: data.monthly.sales,
                    borderWidth: 2,
                    fill: false
                }]
            }
        });

        // Region Sales
        new Chart(document.getElementById("regionSalesChart"), {
            type: "doughnut",
            data: {
                labels: data.region.labels,
                datasets: [{
                    data: data.region.sales
                }]
            }
        });

        // Category Sales
        new Chart(document.getElementById("categorySalesChart"), {
            type: "bar",
            data: {
                labels: data.category.labels,
                datasets: [{
                    label: "Sales",
                    data: data.category.sales
                }]
            }
        });

    });
