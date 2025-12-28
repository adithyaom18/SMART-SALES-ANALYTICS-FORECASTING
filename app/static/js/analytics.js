fetch("/analytics-data")
    .then(response => response.json())
    .then(data => {

        /* ----------------------------
           Monthly Sales Trend (Always)
        ----------------------------- */
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

        /* ----------------------------
           Region-wise Sales (Optional)
        ----------------------------- */
        if (data.region) {
            new Chart(document.getElementById("regionSalesChart"), {
                type: "doughnut",
                data: {
                    labels: data.region.labels,
                    datasets: [{
                        data: data.region.sales
                    }]
                }
            });
        } else {
            document.getElementById("regionSalesChart")
                .parentElement
                .insertAdjacentHTML(
                    "beforeend",
                    "<p class='text-muted text-center mt-3'>Region data not available</p>"
                );
        }

        /* ----------------------------
           Category-wise Sales (Optional)
        ----------------------------- */
        if (data.category) {
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
        } else {
            document.getElementById("categorySalesChart")
                .parentElement
                .insertAdjacentHTML(
                    "beforeend",
                    "<p class='text-muted text-center mt-3'>Category data not available</p>"
                );
        }

        /* ----------------------------
           Hide Loading Spinner
        ----------------------------- */
        document.getElementById("loadingSpinner").style.display = "none";

    })
    .catch(error => {
        console.error("Error loading analytics data:", error);
    });