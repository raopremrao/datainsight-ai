document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('uploadForm');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const errorMessageDiv = document.getElementById('error-message');

    let barChart = null;
    let pieChart = null;

    uploadForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        loadingDiv.style.display = 'block';
        resultsDiv.style.display = 'none';
        errorMessageDiv.style.display = 'none';

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error || 'Server error'); });
            }
            return response.json();
        })
        .then(data => {
            loadingDiv.style.display = 'none';
            
            if (data.error) {
                showError(data.error);
                return;
            }
            
            resultsDiv.style.display = 'block';
            document.getElementById('aiInsights').innerText = data.ai_insights;
            
            // Destroy old charts if they exist
            if(barChart) barChart.destroy();
            if(pieChart) pieChart.destroy();
            
            const barChartContainer = document.getElementById('barChartContainer');
            const pieChartContainer = document.getElementById('pieChartContainer');

            // Handle Bar Chart
            if (data.chart_data.bar_chart_data) {
                barChartContainer.style.display = 'block';
                const barCtx = document.getElementById('barChart').getContext('2d');
                barChart = new Chart(barCtx, {
                    type: 'bar',
                    data: {
                        labels: data.chart_data.bar_chart_data.labels,
                        datasets: [{
                            label: data.chart_data.bar_chart_data.title,
                            data: data.chart_data.bar_chart_data.data,
                            backgroundColor: 'rgba(54, 162, 235, 0.6)'
                        }]
                    }
                });
            } else {
                 barChartContainer.style.display = 'none';
            }

            // Handle Pie Chart
            if (data.chart_data.pie_chart_data) {
                pieChartContainer.style.display = 'block';
                const pieCtx = document.getElementById('pieChart').getContext('2d');
                pieChart = new Chart(pieCtx, {
                    type: 'pie',
                    data: {
                        labels: data.chart_data.pie_chart_data.labels,
                        datasets: [{
                            label: data.chart_data.pie_chart_data.title,
                            data: data.chart_data.pie_chart_data.data
                        }]
                    }
                });
            } else {
                pieChartContainer.style.display = 'none';
            }

        })
        .catch(error => {
            loadingDiv.style.display = 'none';
            showError(error.message);
        });
    });

    function showError(message) {
        errorMessageDiv.innerText = message;
        errorMessageDiv.style.display = 'block';
    }
});