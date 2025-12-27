fetch("/kpis")
    .then(response => response.json())
    .then(data => {

        const kpiContainer = document.getElementById("kpiCards");

        kpiContainer.innerHTML = `
            <div class="col-md-3">
                <div class="card shadow-sm border-0">
                    <div class="card-body">
                        <h6 class="text-muted">Total Sales</h6>
                        <h4 class="fw-bold text-primary">$${data.total_sales.toLocaleString()}</h4>
                    </div>
                </div>
            </div>

            <div class="col-md-3">
                <div class="card shadow-sm border-0">
                    <div class="card-body">
                        <h6 class="text-muted">Avg Monthly Sales</h6>
                        <h4 class="fw-bold text-success">$${data.avg_monthly_sales.toLocaleString()}</h4>
                    </div>
                </div>
            </div>

            <div class="col-md-3">
                <div class="card shadow-sm border-0">
                    <div class="card-body">
                        <h6 class="text-muted">Best Category</h6>
                        <h4 class="fw-bold text-warning">${data.best_category}</h4>
                    </div>
                </div>
            </div>

            <div class="col-md-3">
                <div class="card shadow-sm border-0">
                    <div class="card-body">
                        <h6 class="text-muted">Peak Month</h6>
                        <h4 class="fw-bold text-danger">${data.peak_month}</h4>
                    </div>
                </div>
            </div>
        `;
    });
