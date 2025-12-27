let chart;

function loadForecast(months) {
    fetch(`/forecast?months=${months}`)
        .then(response => response.json())
        .then(data => {

            const ctx = document.getElementById("forecastChart").getContext("2d");

            if (chart) {
                chart.destroy();
            }

            chart = new Chart(ctx, {
                type: "line",
                data: {
                    labels: data.dates,
                    datasets: [{
                        label: "Predicted Sales",
                        data: data.predicted_sales,
                        borderWidth: 2
                    }]
                }
            });
        });
}

document.getElementById("monthsSelect").addEventListener("change", function () {
    loadForecast(this.value);
});

// Load default (3 months)
loadForecast(3);
