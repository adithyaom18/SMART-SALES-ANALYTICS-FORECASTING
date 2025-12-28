fetch("/evaluation")
    .then(response => response.json())
    .then(data => {

        const ctx = document.getElementById("evaluationChart").getContext("2d");

        new Chart(ctx, {
            type: "line",
            data: {
                labels: data.dates,
                datasets: [
                    {
                        label: "Historical Sales",
                        data: data.actual_sales,
                        borderWidth: 2
                    },
                    {
                        label: "Forecasted Trend",
                        data: data.predicted_sales,
                        borderWidth: 2
                    }
                ]
            }
        });
    });
