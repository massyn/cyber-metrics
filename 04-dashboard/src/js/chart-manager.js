/**
 * Chart Manager Module
 * Handles Chart.js chart creation and updates
 */

class ChartManager {
    constructor() {
        this.chart = null;
        this.chartCanvas = document.getElementById('overview-chart');
        this.chartContainer = document.getElementById('chart-container');
        this.noDataMessage = document.getElementById('no-data-message');
        
        // Chart configuration
        this.chartConfig = {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'Compliance Score',
                    data: [],
                    backgroundColor: 'rgba(13, 110, 253, 0.8)', // Bootstrap primary blue
                    borderColor: 'rgba(13, 110, 253, 1)',
                    borderWidth: 1
                }, {
                    label: 'SLO Target',
                    data: [],
                    type: 'line',
                    borderColor: 'rgba(25, 135, 84, 1)', // Bootstrap success green
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0,
                    pointHoverRadius: 0
                }, {
                    label: 'SLO Minimum',
                    data: [],
                    type: 'line',
                    borderColor: 'rgba(255, 193, 7, 1)', // Bootstrap warning amber
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0,
                    pointHoverRadius: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                plugins: {
                    title: {
                        display: false
                    },
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    label += (context.parsed.y * 100).toFixed(1) + '%';
                                }
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Date'
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Compliance Score (%)'
                        },
                        min: 0,
                        max: 1.0,
                        ticks: {
                            callback: function(value) {
                                return (value * 100) + '%';
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                }
            }
        };
    }

    /**
     * Process summary data for chart display
     * @param {Array} summaryData - Raw summary data
     * @param {Object} filters - Applied filters
     * @returns {Object} Processed chart data
     */
    processChartData(summaryData, filters = {}) {
        if (!summaryData || !Array.isArray(summaryData)) {
            return null;
        }

        try {
            // Apply filters to data
            let filteredData = window.dataLoader.applyFilters(summaryData, filters);
            
            if (filteredData.length === 0) {
                console.log('No data after filtering');
                return null;
            }

            // Filter for records with weight > 0 (matching SQL WHERE clause)
            filteredData = filteredData.filter(item => 
                item.weight && parseFloat(item.weight) > 0
            );

            if (filteredData.length === 0) {
                console.log('No data with weight > 0');
                return null;
            }

            // Group by datestamp and calculate aggregated metrics
            const groupedData = this.groupByDatestamp(filteredData);
            
            // Sort by datestamp
            const sortedDates = Object.keys(groupedData).sort();
            
            if (sortedDates.length === 0) {
                return null;
            }

            // Process data for chart
            const chartData = {
                labels: sortedDates.map(date => this.formatDateForChart(date)),
                scores: [],
                slos: [],
                sloMins: []
            };

            sortedDates.forEach(date => {
                const dayData = groupedData[date];
                chartData.scores.push(dayData.score);
                chartData.slos.push(dayData.slo);
                chartData.sloMins.push(dayData.sloMin);
            });

            return chartData;

        } catch (error) {
            console.error('Error processing chart data:', error);
            return null;
        }
    }

    /**
     * Group data by datestamp and calculate weighted averages
     * @param {Array} data - Filtered data array
     * @returns {Object} Grouped data by datestamp
     */
    groupByDatestamp(data) {
        const grouped = {};

        data.forEach(item => {
            const date = item.datestamp;
            if (!grouped[date]) {
                grouped[date] = {
                    scoreWeight: 0,
                    sloWeight: 0,
                    sloMinWeight: 0,
                    totalWeight: 0
                };
            }

            const weight = parseFloat(item.weight) || 0;
            const totalok = parseFloat(item.totalok) || 0;
            const total = parseFloat(item.total) || 1; // Avoid division by zero
            const slo = parseFloat(item.slo) || 0;
            const sloMin = parseFloat(item.slo_min) || 0;

            // Calculate weighted contributions (matching SQL logic)
            const scoreWeight = (totalok / total) * weight;
            const sloWeightContrib = slo * weight;
            const sloMinWeightContrib = sloMin * weight;

            grouped[date].scoreWeight += scoreWeight;
            grouped[date].sloWeight += sloWeightContrib;
            grouped[date].sloMinWeight += sloMinWeightContrib;
            grouped[date].totalWeight += weight;
        });

        // Calculate final averages
        Object.keys(grouped).forEach(date => {
            const dayData = grouped[date];
            if (dayData.totalWeight > 0) {
                dayData.score = dayData.scoreWeight / dayData.totalWeight;
                dayData.slo = dayData.sloWeight / dayData.totalWeight;
                dayData.sloMin = dayData.sloMinWeight / dayData.totalWeight;
            } else {
                dayData.score = 0;
                dayData.slo = 0;
                dayData.sloMin = 0;
            }
        });

        return grouped;
    }

    /**
     * Format date for chart display (abbreviated format)
     * @param {string} dateString - Date in YYYY-MM-DD format
     * @returns {string} Formatted date string
     */
    formatDateForChart(dateString) {
        try {
            const date = new Date(dateString + 'T00:00:00'); // Add time to avoid timezone issues
            const options = { month: 'short', day: 'numeric' };
            return date.toLocaleDateString('en-US', options);
        } catch (error) {
            console.error('Error formatting date:', dateString, error);
            return dateString;
        }
    }

    /**
     * Update or create the chart
     * @param {Array} summaryData - Summary data array
     * @param {Object} filters - Applied filters
     */
    updateChart(summaryData, filters = {}) {
        const chartData = this.processChartData(summaryData, filters);
        
        if (!chartData) {
            this.showNoData();
            return;
        }

        this.hideNoData();

        // Update chart data
        this.chartConfig.data.labels = chartData.labels;
        this.chartConfig.data.datasets[0].data = chartData.scores;
        this.chartConfig.data.datasets[1].data = chartData.slos;
        this.chartConfig.data.datasets[2].data = chartData.sloMins;

        if (this.chart) {
            // Update existing chart
            this.chart.update('active');
        } else {
            // Create new chart
            this.createChart();
        }

        console.log(`Chart updated with ${chartData.labels.length} data points`);
    }

    /**
     * Create the Chart.js chart
     */
    createChart() {
        if (this.chart) {
            this.chart.destroy();
        }

        try {
            const ctx = this.chartCanvas.getContext('2d');
            this.chart = new Chart(ctx, this.chartConfig);
            console.log('Chart created successfully');
        } catch (error) {
            console.error('Error creating chart:', error);
            this.showNoData();
        }
    }

    /**
     * Show no data message
     */
    showNoData() {
        this.chartCanvas.style.display = 'none';
        this.noDataMessage.style.display = 'flex';
        
        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
        }
    }

    /**
     * Hide no data message
     */
    hideNoData() {
        this.chartCanvas.style.display = 'block';
        this.noDataMessage.style.display = 'none';
    }

    /**
     * Destroy the chart instance
     */
    destroy() {
        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
        }
    }

    /**
     * Resize chart (useful for responsive behavior)
     */
    resize() {
        if (this.chart) {
            this.chart.resize();
        }
    }

    /**
     * Get the latest overall scores for overview cards
     * @param {Array} summaryData - Summary data array
     * @param {Object} filters - Applied filters
     * @returns {Object|null} Latest overall scores or null if no data
     */
    getLatestOverallScores(summaryData, filters = {}) {
        if (!summaryData || !Array.isArray(summaryData)) {
            return null;
        }

        try {
            // Apply filters to data
            let filteredData = window.dataLoader.applyFilters(summaryData, filters);
            
            if (filteredData.length === 0) {
                return null;
            }

            // Filter for records with weight > 0
            filteredData = filteredData.filter(item => 
                item.weight && parseFloat(item.weight) > 0
            );

            if (filteredData.length === 0) {
                return null;
            }

            // Get latest datestamp
            const latestDate = window.dataLoader.getLatestDatestamp(filteredData);
            if (!latestDate) {
                return null;
            }

            // Filter to latest date only
            const latestData = filteredData.filter(item => item.datestamp === latestDate);

            // Calculate weighted averages for latest date
            let scoreWeight = 0;
            let sloWeight = 0;
            let sloMinWeight = 0;
            let totalWeight = 0;

            latestData.forEach(item => {
                const weight = parseFloat(item.weight) || 0;
                const totalok = parseFloat(item.totalok) || 0;
                const total = parseFloat(item.total) || 1;
                const slo = parseFloat(item.slo) || 0;
                const sloMin = parseFloat(item.slo_min) || 0;

                scoreWeight += (totalok / total) * weight;
                sloWeight += slo * weight;
                sloMinWeight += sloMin * weight;
                totalWeight += weight;
            });

            if (totalWeight === 0) {
                return null;
            }

            return {
                overallScore: scoreWeight / totalWeight,
                averageSlo: sloWeight / totalWeight,
                averageSloMin: sloMinWeight / totalWeight,
                datestamp: latestDate
            };

        } catch (error) {
            console.error('Error calculating latest overall scores:', error);
            return null;
        }
    }

    /**
     * Get chart statistics
     * @returns {Object} Chart statistics
     */
    getChartStats() {
        if (!this.chart || !this.chart.data.datasets[0].data.length) {
            return null;
        }

        const scores = this.chart.data.datasets[0].data;
        const slos = this.chart.data.datasets[1].data;
        const sloMins = this.chart.data.datasets[2].data;

        return {
            dataPoints: scores.length,
            averageScore: scores.reduce((a, b) => a + b, 0) / scores.length,
            minScore: Math.min(...scores),
            maxScore: Math.max(...scores),
            averageSLO: slos.length > 0 ? slos.reduce((a, b) => a + b, 0) / slos.length : 0,
            averageSLOMin: sloMins.length > 0 ? sloMins.reduce((a, b) => a + b, 0) / sloMins.length : 0
        };
    }
}

// Create global instance
window.chartManager = new ChartManager();