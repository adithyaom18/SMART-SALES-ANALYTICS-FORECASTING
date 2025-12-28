fetch("/kpis")
    .then(res => res.json())
    .then(data => {

        const kpiContainer = document.getElementById("kpiCards");

        const growthArrow = data.growth_pct >= 0 ? "↑" : "↓";
        const growthClass = data.growth_pct >= 0 ? "text-success" : "text-danger";

        kpiContainer.innerHTML = `
            <div class="col-md-3">
                <div class="card kpi-card shadow-sm">
                    <div class="card-body text-center">
                        <div class="kpi-icon">💰</div>
                        <h6>Total Sales</h6>
                        <h4 class="kpi-value">₹ ${data.total_sales}</h4>
                    </div>
                </div>
            </div>

            <div class="col-md-3">
                <div class="card kpi-card shadow-sm">
                    <div class="card-body text-center">
                        <div class="kpi-icon">📊</div>
                        <h6>Avg Monthly</h6>
                        <h4 class="kpi-value">₹ ${data.avg_monthly_sales}</h4>
                    </div>
                </div>
            </div>

            <div class="col-md-3">
                <div class="card kpi-card shadow-sm">
                    <div class="card-body text-center">
                        <div class="kpi-icon">🏆</div>
                        <h6>Peak Month</h6>
                        <h4 class="kpi-value">${data.peak_month}</h4>
                    </div>
                </div>
            </div>

            <div class="col-md-3">
                <div class="card kpi-card shadow-sm">
                    <div class="card-body text-center">
                        <div class="kpi-icon">📈</div>
                        <h6>Growth (MoM)</h6>
                        <h4 class="kpi-value ${growthClass}">
                            ${growthArrow} ${data.growth_pct}%
                        </h4>
                    </div>
                </div>
            </div>

            <div class="col-md-12 mt-3">
                <div class="card kpi-card shadow-sm">
                    <div class="card-body text-center">
                        <div class="kpi-icon">🗓️</div>
                        <h6>Data Coverage</h6>
                        <h4 class="kpi-value">${data.data_coverage} Months</h4>
                    </div>
                </div>
            </div>
        `;

        // ✅ Hide loading spinner after KPIs are rendered
        document.getElementById("loadingSpinner").style.display = "none";
    })
    .catch(error => {
        console.error("Error loading KPI data:", error);
    });