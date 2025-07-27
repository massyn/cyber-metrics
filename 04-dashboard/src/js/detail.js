/**
 * Detail View Module
 * Handles detailed metric analysis, charts, and evidence tables
 */

class DetailManager {
    constructor() {
        // UI Elements
        this.section = document.getElementById('detail-section');
        this.titleElement = document.getElementById('detail-metric-title');
        this.lastUpdatedElement = document.getElementById('detail-last-updated');
        this.scoreBadge = document.getElementById('detail-score-badge');
        this.sloValue = document.getElementById('detail-slo-value');
        this.sloMinValue = document.getElementById('detail-slo-min-value');
        this.backButton = document.getElementById('back-to-scorecard');
        
        // Chart elements
        this.chartCanvas = document.getElementById('detail-chart');
        this.chartContainer = document.getElementById('detail-chart-container');
        this.noDataMessage = document.getElementById('detail-no-data-message');
        
        // Evidence table elements
        this.evidenceTableBody = document.getElementById('evidence-table-body');
        this.evidenceTableContainer = document.getElementById('evidence-table-container');
        this.evidenceNoDataMessage = document.getElementById('evidence-no-data-message');
        this.evidenceCount = document.getElementById('evidence-count');
        this.pageSizeSelect = document.getElementById('evidence-page-size');
        this.paginationInfo = document.getElementById('evidence-pagination-info');
        this.pagination = document.getElementById('evidence-pagination');
        
        // Data
        this.currentMetric = null;
        this.currentFilters = {};
        this.evidenceData = null;
        this.chart = null;
        
        // Pagination
        this.currentPage = 1;
        this.pageSize = 25;
        this.totalRecords = 0;
        
        // Evidence table sorting
        this.evidenceSortColumn = 'compliance';
        this.evidenceSortDirection = 'asc';
        
        this.initializeEventHandlers();
    }

    /**
     * Update filters and refresh data
     * @param {Object} filters - New filter settings
     */
    async updateFilters(filters) {
        this.currentFilters = filters;
        
        // Refresh both chart and evidence table with new filters
        if (this.currentMetric) {
            await this.loadPerformanceChart();
            await this.loadEvidenceTable();
        }
    }

    /**
     * Initialize event handlers
     */
    initializeEventHandlers() {
        // Back button
        this.backButton.addEventListener('click', () => {
            this.navigateBackToScorecard();
        });
        
        // Page size selector
        this.pageSizeSelect.addEventListener('change', (e) => {
            this.pageSize = parseInt(e.target.value);
            this.currentPage = 1;
            this.renderEvidenceTable();
        });
        
        // Evidence table sorting
        this.initializeEvidenceSorting();
    }

    /**
     * Initialize evidence table sorting functionality
     */
    initializeEvidenceSorting() {
        // Add event listeners to sortable headers
        const sortableHeaders = document.querySelectorAll('#evidence-table .sortable');
        
        sortableHeaders.forEach(header => {
            header.addEventListener('click', () => {
                const sortField = header.dataset.sort;
                this.handleEvidenceSort(sortField);
            });
        });
    }

    /**
     * Handle evidence table column sorting
     * @param {string} column - Column to sort by
     */
    handleEvidenceSort(column) {
        if (this.evidenceSortColumn === column) {
            // Toggle direction if same column
            this.evidenceSortDirection = this.evidenceSortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            // New column, default to ascending
            this.evidenceSortColumn = column;
            this.evidenceSortDirection = 'asc';
        }
        
        // Update sort indicators
        this.updateEvidenceSortIndicators();
        
        // Reset to first page and re-render
        this.currentPage = 1;
        this.renderEvidenceTable();
    }

    /**
     * Update visual sort indicators for evidence table
     */
    updateEvidenceSortIndicators() {
        // Clear all sort classes
        const sortableHeaders = document.querySelectorAll('#evidence-table .sortable');
        sortableHeaders.forEach(header => {
            header.classList.remove('sort-asc', 'sort-desc');
        });
        
        // Add sort class to active column
        const activeHeader = document.querySelector(`#evidence-table .sortable[data-sort="${this.evidenceSortColumn}"]`);
        if (activeHeader) {
            activeHeader.classList.add(`sort-${this.evidenceSortDirection}`);
        }
    }

    /**
     * Show metric detail view
     * @param {Object} metricData - Metric information and filters
     */
    async showMetric(metricData) {
        this.currentMetric = metricData;
        this.currentFilters = metricData.filters || {};
        
        try {
            // Update header information
            this.updateHeader();
            
            // Load and render performance chart
            await this.loadPerformanceChart();
            
            // Load and render evidence table
            await this.loadEvidenceTable();
            
        } catch (error) {
            console.error('Error showing metric detail:', error);
            this.showError();
        }
    }

    /**
     * Update header section with metric information
     */
    updateHeader() {
        if (!this.currentMetric) return;
        
        // Update title
        this.titleElement.textContent = this.currentMetric.title;
        
        // Update score badge
        const scorePercentage = (this.currentMetric.currentScore * 100).toFixed(1) + '%';
        const badgeClass = this.getScoreColorClass(
            this.currentMetric.currentScore,
            this.currentMetric.slo,
            this.currentMetric.slo_min
        );
        this.scoreBadge.className = `badge fs-6 ${badgeClass}`;
        this.scoreBadge.textContent = scorePercentage;
        
        // Update SLO values
        this.sloValue.textContent = (this.currentMetric.slo * 100).toFixed(1) + '%';
        this.sloMinValue.textContent = (this.currentMetric.slo_min * 100).toFixed(1) + '%';
    }

    /**
     * Load and render performance chart
     */
    async loadPerformanceChart() {
        try {
            // Load summary data
            const summaryData = await window.dataLoader.loadSummaryData();
            
            if (!summaryData || summaryData.length === 0) {
                this.showChartNoData();
                return;
            }
            
            // Filter data for this metric and apply filters
            const metricData = summaryData.filter(item => 
                item.metric_id === this.currentMetric.metric_id
            );
            
            const filteredData = window.dataLoader.applyFilters(metricData, this.currentFilters);
            
            if (filteredData.length === 0) {
                this.showChartNoData();
                return;
            }
            
            // Process data for chart
            const chartData = this.processChartData(filteredData);
            
            // Render chart
            this.renderChart(chartData);
            
            // Update last updated time
            this.updateLastUpdated(chartData);
            
        } catch (error) {
            console.error('Error loading performance chart:', error);
            this.showChartNoData();
        }
    }

    /**
     * Process summary data for chart display
     * @param {Array} data - Filtered summary data for this metric
     * @returns {Object} Chart data object
     */
    processChartData(data) {
        // Group by datestamp and calculate scores
        const groupedData = {};
        
        data.forEach(item => {
            const datestamp = item.datestamp;
            
            if (!groupedData[datestamp]) {
                groupedData[datestamp] = {
                    datestamp: datestamp,
                    totalOk: 0,
                    total: 0,
                    slo: item.slo,
                    slo_min: item.slo_min
                };
            }
            
            groupedData[datestamp].totalOk += item.totalok;
            groupedData[datestamp].total += item.total;
            
            // Use max values for SLO (should be consistent)
            groupedData[datestamp].slo = Math.max(groupedData[datestamp].slo, item.slo);
            groupedData[datestamp].slo_min = Math.max(groupedData[datestamp].slo_min, item.slo_min);
        });
        
        // Convert to array and calculate scores
        const results = Object.values(groupedData).map(item => ({
            datestamp: item.datestamp,
            score: item.total > 0 ? item.totalOk / item.total : 0,
            slo: item.slo,
            slo_min: item.slo_min
        }));
        
        // Sort by datestamp
        results.sort((a, b) => a.datestamp.localeCompare(b.datestamp));
        
        return {
            data: results,
            latestDate: results.length > 0 ? results[results.length - 1].datestamp : null
        };
    }

    /**
     * Render the performance chart
     * @param {Object} chartData - Processed chart data
     */
    renderChart(chartData) {
        const ctx = this.chartCanvas.getContext('2d');
        
        // Destroy existing chart
        if (this.chart) {
            this.chart.destroy();
        }
        
        // Prepare data for Chart.js
        const labels = chartData.data.map(item => {
            const date = new Date(item.datestamp);
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        });
        
        const scores = chartData.data.map(item => (item.score * 100));
        const sloLine = chartData.data.map(item => (item.slo * 100));
        const sloMinLine = chartData.data.map(item => (item.slo_min * 100));
        
        // Create chart
        this.chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Score',
                        data: scores,
                        backgroundColor: 'rgba(54, 162, 235, 0.6)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1,
                        type: 'bar'
                    },
                    {
                        label: 'SLO Target',
                        data: sloLine,
                        borderColor: 'rgba(40, 167, 69, 1)',
                        backgroundColor: 'transparent',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        type: 'line',
                        pointRadius: 0,
                        fill: false
                    },
                    {
                        label: 'SLO Minimum',
                        data: sloMinLine,
                        borderColor: 'rgba(255, 193, 7, 1)',
                        backgroundColor: 'transparent',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        type: 'line',
                        pointRadius: 0,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Compliance Score (%)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.parsed.y.toFixed(1) + '%';
                            }
                        }
                    }
                }
            }
        });
        
        // Show chart container
        this.chartContainer.style.display = 'block';
        this.noDataMessage.style.display = 'none';
    }

    /**
     * Load and render evidence table
     */
    async loadEvidenceTable() {
        try {
            // Load detail data
            this.evidenceData = await window.dataLoader.loadDetailData();
            
            if (!this.evidenceData || this.evidenceData.length === 0) {
                this.showEvidenceNoData();
                return;
            }
            
            // Filter data for this metric and apply organizational filters
            const filteredData = this.filterEvidenceData();
            
            if (filteredData.length === 0) {
                this.showEvidenceNoData();
                return;
            }
            
            this.totalRecords = filteredData.length;
            this.currentPage = 1;
            
            // Render table
            this.renderEvidenceTable(filteredData);
            
        } catch (error) {
            console.error('Error loading evidence table:', error);
            this.showEvidenceNoData();
        }
    }

    /**
     * Filter evidence data based on current metric and filters
     * @returns {Array} Filtered evidence data
     */
    filterEvidenceData() {
        if (!this.evidenceData) return [];
        
        // Filter by metric_id
        let filtered = this.evidenceData.filter(item => 
            item.metric_id === this.currentMetric.metric_id
        );
        
        // Apply organizational filters
        filtered = window.dataLoader.applyFilters(filtered, this.currentFilters);
        
        // Apply sorting
        filtered = this.sortEvidenceData(filtered);
        
        return filtered;
    }

    /**
     * Sort evidence data based on current sort settings
     * @param {Array} data - Data to sort
     * @returns {Array} Sorted data
     */
    sortEvidenceData(data) {
        return [...data].sort((a, b) => {
            let aValue, bValue;
            
            if (this.evidenceSortColumn === 'resource') {
                aValue = a.resource.toLowerCase();
                bValue = b.resource.toLowerCase();
            } else if (this.evidenceSortColumn === 'detail') {
                aValue = a.detail.toLowerCase();
                bValue = b.detail.toLowerCase();
            } else if (this.evidenceSortColumn === 'compliance') {
                aValue = a.compliance;
                bValue = b.compliance;
            }
            
            let comparison = 0;
            if (aValue > bValue) {
                comparison = 1;
            } else if (aValue < bValue) {
                comparison = -1;
            }
            
            return this.evidenceSortDirection === 'desc' ? -comparison : comparison;
        });
    }

    /**
     * Render evidence table with pagination
     * @param {Array} data - Optional filtered data, otherwise uses current filtered data
     */
    renderEvidenceTable(data = null) {
        const filteredData = data || this.filterEvidenceData();
        
        // Calculate pagination
        const startIndex = (this.currentPage - 1) * this.pageSize;
        const endIndex = startIndex + this.pageSize;
        const pageData = filteredData.slice(startIndex, endIndex);
        
        // Clear table body
        this.evidenceTableBody.innerHTML = '';
        
        // Render rows
        pageData.forEach(item => {
            const row = document.createElement('tr');
            
            // Resource column
            const resourceCell = document.createElement('td');
            resourceCell.textContent = item.resource;
            row.appendChild(resourceCell);
            
            // Detail column
            const detailCell = document.createElement('td');
            detailCell.textContent = item.detail;
            detailCell.style.maxWidth = '400px';
            detailCell.style.overflow = 'hidden';
            detailCell.style.textOverflow = 'ellipsis';
            detailCell.style.whiteSpace = 'nowrap';
            detailCell.title = item.detail; // Full text on hover
            row.appendChild(detailCell);
            
            // Compliance column
            const complianceCell = document.createElement('td');
            const complianceBadge = this.createComplianceBadge(item.compliance);
            complianceCell.appendChild(complianceBadge);
            row.appendChild(complianceCell);
            
            this.evidenceTableBody.appendChild(row);
        });
        
        // Update sort indicators
        this.updateEvidenceSortIndicators();
        
        // Update count and pagination
        this.updateEvidenceCount(filteredData.length);
        this.updatePagination(filteredData.length);
        
        // Show table
        this.evidenceTableContainer.style.display = 'block';
        this.evidenceNoDataMessage.style.display = 'none';
    }

    /**
     * Create compliance badge element
     * @param {number} compliance - Compliance value (0, 1, or decimal)
     * @returns {HTMLElement} Badge element
     */
    createComplianceBadge(compliance) {
        const badge = document.createElement('span');
        badge.classList.add('badge');
        
        if (compliance === 1) {
            badge.classList.add('bg-success');
            badge.textContent = 'Compliant';
        } else if (compliance === 0) {
            badge.classList.add('bg-danger');
            badge.textContent = 'Non-Compliant';
        } else {
            badge.classList.add('bg-warning', 'text-dark');
            badge.textContent = `Partial (${(compliance * 100).toFixed(1)}%)`;
        }
        
        return badge;
    }

    /**
     * Update evidence count display
     * @param {number} totalCount - Total number of evidence records
     */
    updateEvidenceCount(totalCount) {
        this.evidenceCount.textContent = `${totalCount} record${totalCount === 1 ? '' : 's'}`;
    }

    /**
     * Update pagination controls
     * @param {number} totalCount - Total number of records
     */
    updatePagination(totalCount) {
        const totalPages = Math.ceil(totalCount / this.pageSize);
        
        // Update pagination info
        const startRecord = totalCount > 0 ? (this.currentPage - 1) * this.pageSize + 1 : 0;
        const endRecord = Math.min(this.currentPage * this.pageSize, totalCount);
        this.paginationInfo.textContent = `Showing ${startRecord}-${endRecord} of ${totalCount}`;
        
        // Clear pagination
        this.pagination.innerHTML = '';
        
        if (totalPages <= 1) {
            return; // Don't show pagination for single page
        }
        
        // Previous button
        const prevItem = document.createElement('li');
        prevItem.classList.add('page-item');
        if (this.currentPage === 1) {
            prevItem.classList.add('disabled');
        }
        const prevLink = document.createElement('a');
        prevLink.classList.add('page-link');
        prevLink.href = '#';
        prevLink.textContent = 'Previous';
        prevLink.addEventListener('click', (e) => {
            e.preventDefault();
            if (this.currentPage > 1) {
                this.currentPage--;
                this.renderEvidenceTable();
            }
        });
        prevItem.appendChild(prevLink);
        this.pagination.appendChild(prevItem);
        
        // Page numbers (show max 5 pages around current)
        const startPage = Math.max(1, this.currentPage - 2);
        const endPage = Math.min(totalPages, this.currentPage + 2);
        
        for (let i = startPage; i <= endPage; i++) {
            const pageItem = document.createElement('li');
            pageItem.classList.add('page-item');
            if (i === this.currentPage) {
                pageItem.classList.add('active');
            }
            
            const pageLink = document.createElement('a');
            pageLink.classList.add('page-link');
            pageLink.href = '#';
            pageLink.textContent = i;
            pageLink.addEventListener('click', (e) => {
                e.preventDefault();
                this.currentPage = i;
                this.renderEvidenceTable();
            });
            
            pageItem.appendChild(pageLink);
            this.pagination.appendChild(pageItem);
        }
        
        // Next button
        const nextItem = document.createElement('li');
        nextItem.classList.add('page-item');
        if (this.currentPage === totalPages) {
            nextItem.classList.add('disabled');
        }
        const nextLink = document.createElement('a');
        nextLink.classList.add('page-link');
        nextLink.href = '#';
        nextLink.textContent = 'Next';
        nextLink.addEventListener('click', (e) => {
            e.preventDefault();
            if (this.currentPage < totalPages) {
                this.currentPage++;
                this.renderEvidenceTable();
            }
        });
        nextItem.appendChild(nextLink);
        this.pagination.appendChild(nextItem);
    }

    /**
     * Get Bootstrap color class based on score and SLO thresholds
     * @param {number} score - Current score (0-1)
     * @param {number} slo - SLO target (0-1)
     * @param {number} slo_min - SLO minimum (0-1)
     * @returns {string} Bootstrap badge class
     */
    getScoreColorClass(score, slo, slo_min) {
        if (score >= slo) {
            return 'bg-success';
        } else if (score >= slo_min) {
            return 'bg-warning';
        } else {
            return 'bg-danger';
        }
    }

    /**
     * Update last updated timestamp
     * @param {Object} chartData - Chart data with latest date
     */
    updateLastUpdated(chartData) {
        if (chartData && chartData.latestDate) {
            const date = new Date(chartData.latestDate);
            this.lastUpdatedElement.textContent = `Last updated: ${date.toLocaleDateString()}`;
        }
    }

    /**
     * Navigate back to scorecard view
     */
    navigateBackToScorecard() {
        if (window.dashboardApp) {
            window.dashboardApp.switchSection('scorecard');
        }
    }

    /**
     * Show chart no data message
     */
    showChartNoData() {
        this.chartContainer.style.display = 'none';
        this.noDataMessage.style.display = 'block';
    }

    /**
     * Show evidence table no data message
     */
    showEvidenceNoData() {
        this.evidenceTableContainer.style.display = 'none';
        this.evidenceNoDataMessage.style.display = 'block';
        this.evidenceCount.textContent = '0 records';
        this.paginationInfo.textContent = 'No records to display';
        this.pagination.innerHTML = '';
    }

    /**
     * Show general error state
     */
    showError() {
        this.showChartNoData();
        this.showEvidenceNoData();
        this.lastUpdatedElement.textContent = 'Error loading data';
    }
}

// Create global instance
window.detailManager = new DetailManager();