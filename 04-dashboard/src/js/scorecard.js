/**
 * Scorecard Module
 * Handles scorecard table rendering and data processing
 */

class ScorecardManager {
    constructor() {
        this.tableBody = document.getElementById('scorecard-table-body');
        this.noDataMessage = document.getElementById('scorecard-no-data-message');
        this.tableContainer = document.getElementById('scorecard-table-container');
        this.lastUpdatedElement = document.getElementById('scorecard-last-updated');
        
        this.currentData = null;
        this.currentFilters = {};
        this.sortColumn = 'title';
        this.sortDirection = 'asc';
        
        this.initializeSorting();
    }

    /**
     * Initialize table sorting functionality
     */
    initializeSorting() {
        // Add event listeners to sortable headers
        const sortableHeaders = document.querySelectorAll('#scorecard-table .sortable');
        
        sortableHeaders.forEach(header => {
            header.addEventListener('click', () => {
                const sortField = header.dataset.sort;
                this.handleSort(sortField);
            });
        });
    }

    /**
     * Handle column sorting
     * @param {string} column - Column to sort by
     */
    handleSort(column) {
        if (this.sortColumn === column) {
            // Toggle direction if same column
            this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            // New column, default to ascending
            this.sortColumn = column;
            this.sortDirection = 'asc';
        }
        
        // Update sort indicators
        this.updateSortIndicators();
        
        // Re-render table with current data
        if (this.currentData) {
            const sortedData = this.sortData(this.currentData);
            this.renderTableRows(sortedData);
            
            // Re-initialize sparklines after sorting
            this.initializeSparklines();
        }
    }

    /**
     * Update visual sort indicators
     */
    updateSortIndicators() {
        // Clear all sort classes
        const sortableHeaders = document.querySelectorAll('#scorecard-table .sortable');
        sortableHeaders.forEach(header => {
            header.classList.remove('sort-asc', 'sort-desc');
        });
        
        // Add sort class to active column
        const activeHeader = document.querySelector(`#scorecard-table .sortable[data-sort="${this.sortColumn}"]`);
        if (activeHeader) {
            activeHeader.classList.add(`sort-${this.sortDirection}`);
        }
    }

    /**
     * Sort data array based on current sort settings
     * @param {Array} data - Data to sort
     * @returns {Array} Sorted data
     */
    sortData(data) {
        return [...data].sort((a, b) => {
            let aValue, bValue;
            
            if (this.sortColumn === 'title') {
                aValue = a.title.toLowerCase();
                bValue = b.title.toLowerCase();
            } else if (this.sortColumn === 'score') {
                aValue = a.currentScore;
                bValue = b.currentScore;
            }
            
            let comparison = 0;
            if (aValue > bValue) {
                comparison = 1;
            } else if (aValue < bValue) {
                comparison = -1;
            }
            
            return this.sortDirection === 'desc' ? -comparison : comparison;
        });
    }

    /**
     * Load and render scorecard data
     * @param {Object} filters - Current filter selections
     */
    async loadScorecard(filters = {}) {
        try {
            this.currentFilters = filters;
            
            // Load summary data
            const summaryData = await window.dataLoader.loadSummaryData();
            
            if (!summaryData || summaryData.length === 0) {
                this.showNoData();
                return;
            }

            // Process and render the data
            this.processAndRenderData(summaryData);
            
        } catch (error) {
            console.error('Error loading scorecard:', error);
            this.showNoData();
        }
    }

    /**
     * Process summary data and render scorecard table
     * @param {Array} summaryData - Raw summary data
     */
    processAndRenderData(summaryData) {
        // Apply filters to the data
        const filteredData = window.dataLoader.applyFilters(summaryData, this.currentFilters);
        
        if (filteredData.length === 0) {
            this.showNoData();
            return;
        }

        // Get latest datestamp
        const latestDate = window.dataLoader.getLatestDatestamp(filteredData);
        
        // Get current scores (latest datestamp only)
        const currentScores = this.calculateCurrentScores(filteredData, latestDate);
        
        // Get historical scores for sparklines
        const historicalScores = this.calculateHistoricalScores(filteredData);
        
        // Store current data for sorting
        this.currentData = currentScores;
        this.historicalData = historicalScores;
        
        // Render the table
        this.renderTable(currentScores, historicalScores);
        
        // Initialize sparklines after table is rendered
        this.initializeSparklines();
        
        // Update last updated timestamp
        this.updateLastUpdated(latestDate);
        
        this.showTable();
    }

    /**
     * Calculate current scores for latest datestamp
     * @param {Array} data - Filtered summary data
     * @param {string} latestDate - Latest datestamp
     * @returns {Array} Array of metric scores
     */
    calculateCurrentScores(data, latestDate) {
        // Filter to latest date only
        const latestData = data.filter(item => item.datestamp === latestDate);
        
        // Group by title and calculate scores
        const scoresByTitle = {};
        
        latestData.forEach(item => {
            const metricId = item.metric_id;
            
            if (!scoresByTitle[metricId]) {
                scoresByTitle[metricId] = {
                    metric_id: metricId,
                    title: item.title,
                    totalOk: 0,
                    total: 0,
                    slo: item.slo,
                    slo_min: item.slo_min
                };
            }
            
            scoresByTitle[metricId].totalOk += item.totalok;
            scoresByTitle[metricId].total += item.total;
            
            // Use max values for SLO (should be same across records)
            scoresByTitle[metricId].slo = Math.max(scoresByTitle[metricId].slo, item.slo);
            scoresByTitle[metricId].slo_min = Math.max(scoresByTitle[metricId].slo_min, item.slo_min);
        });
        
        // Convert to array and calculate scores
        const results = Object.values(scoresByTitle).map(metric => ({
            metric_id: metric.metric_id,
            title: metric.title,
            currentScore: metric.total > 0 ? metric.totalOk / metric.total : 0,
            slo: metric.slo,
            slo_min: metric.slo_min
        }));
        
        // Sort by title alphabetically
        return results.sort((a, b) => a.title.localeCompare(b.title));
    }

    /**
     * Calculate historical scores for sparklines
     * @param {Array} data - Filtered summary data
     * @returns {Object} Object with title as key and historical scores as value
     */
    calculateHistoricalScores(data) {
        const historicalData = {};
        
        // Group by title and datestamp
        const groupedData = {};
        
        data.forEach(item => {
            const key = `${item.metric_id}|${item.datestamp}`;
            
            if (!groupedData[key]) {
                groupedData[key] = {
                    metric_id: item.metric_id,
                    title: item.title,
                    datestamp: item.datestamp,
                    totalOk: 0,
                    total: 0
                };
            }
            
            groupedData[key].totalOk += item.totalok;
            groupedData[key].total += item.total;
        });
        
        // Calculate scores and group by metric_id (but use title as key for display)
        Object.values(groupedData).forEach(item => {
            if (!historicalData[item.title]) {
                historicalData[item.title] = [];
            }
            
            historicalData[item.title].push({
                datestamp: item.datestamp,
                score: item.total > 0 ? item.totalOk / item.total : 0
            });
        });
        
        // Sort each title's data by datestamp
        Object.keys(historicalData).forEach(title => {
            historicalData[title].sort((a, b) => a.datestamp.localeCompare(b.datestamp));
        });
        
        return historicalData;
    }

    /**
     * Render the scorecard table
     * @param {Array} currentScores - Current scores data
     * @param {Object} historicalScores - Historical scores for sparklines
     */
    renderTable(currentScores, historicalScores) {
        // Sort the data first
        const sortedData = this.sortData(currentScores);
        
        // Render table rows
        this.renderTableRows(sortedData, historicalScores);
        
        // Update sort indicators
        this.updateSortIndicators();
    }

    /**
     * Render table rows with given data
     * @param {Array} data - Sorted scorecard data
     * @param {Object} historicalScores - Historical scores for sparklines (optional)
     */
    renderTableRows(data, historicalScores = null) {
        this.tableBody.innerHTML = '';
        
        // Use stored historical data if not provided
        const histData = historicalScores || this.historicalData || {};
        
        data.forEach(metric => {
            const row = document.createElement('tr');
            row.style.cursor = 'pointer';
            row.classList.add('metric-row');
            
            // Add click handler for row navigation
            row.addEventListener('click', () => {
                this.navigateToDetail(metric);
            });
            
            // Title column
            const titleCell = document.createElement('td');
            titleCell.textContent = metric.title;
            row.appendChild(titleCell);
            
            // Current Score column with color coding
            const scoreCell = document.createElement('td');
            const scorePercentage = (metric.currentScore * 100).toFixed(1) + '%';
            scoreCell.innerHTML = `<span class="badge ${this.getScoreColorClass(metric.currentScore, metric.slo, metric.slo_min)}">${scorePercentage}</span>`;
            row.appendChild(scoreCell);
            
            // Trend column
            const trendCell = document.createElement('td');
            const sparklineData = histData[metric.title] || [];
            trendCell.innerHTML = this.createSparklineHtml(sparklineData);
            row.appendChild(trendCell);
            
            this.tableBody.appendChild(row);
        });
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
            return 'bg-success'; // Green
        } else if (score >= slo_min) {
            return 'bg-warning'; // Yellow
        } else {
            return 'bg-danger'; // Red
        }
    }

    /**
     * Create sparkline visualization
     * @param {Array} data - Historical score data
     * @returns {string} HTML for sparkline
     */
    createSparklineHtml(data) {
        if (!data || data.length < 2) {
            return '<span class="text-muted">No trend data</span>';
        }
        
        const sparklineId = `sparkline-${Math.random().toString(36).substr(2, 9)}`;
        const values = data.map(d => (d.score * 100).toFixed(1));
        
        const firstScore = data[0].score;
        const lastScore = data[data.length - 1].score;
        const difference = lastScore - firstScore;
        
        let trendClass = 'text-secondary';
        let trendIcon = '→';
        let sparklineColor = '#6c757d';
        
        if (difference > 0.01) { // Improving by more than 1%
            trendClass = 'text-success';
            trendIcon = '↗';
            sparklineColor = '#198754';
        } else if (difference < -0.01) { // Declining by more than 1%
            trendClass = 'text-danger';
            trendIcon = '↘';
            sparklineColor = '#dc3545';
        }
        
        // Create container with both sparkline and trend indicator
        return `
            <div class="d-flex align-items-center">
                <span id="${sparklineId}" class="sparkline me-2" data-values="${values.join(',')}" data-color="${sparklineColor}"></span>
                <span class="${trendClass} small">${trendIcon}</span>
            </div>
        `;
    }

    /**
     * Initialize sparklines after table rendering
     */
    initializeSparklines() {
        // Use a simple canvas-based sparkline implementation
        const sparklineElements = this.tableBody.querySelectorAll('.sparkline');
        
        sparklineElements.forEach(element => {
            const values = element.dataset.values.split(',').map(v => parseFloat(v));
            const color = element.dataset.color || '#6c757d';
            
            this.createCanvasSparkline(element, values, color);
        });
    }

    /**
     * Create a canvas-based sparkline
     * @param {Element} container - Container element
     * @param {Array} values - Data values
     * @param {string} color - Line color
     */
    createCanvasSparkline(container, values, color) {
        if (!values || values.length < 2) return;
        
        const canvas = document.createElement('canvas');
        canvas.width = 60;
        canvas.height = 20;
        canvas.style.verticalAlign = 'middle';
        
        const ctx = canvas.getContext('2d');
        
        // Calculate dimensions
        const width = canvas.width;
        const height = canvas.height;
        const padding = 2;
        const drawWidth = width - (padding * 2);
        const drawHeight = height - (padding * 2);
        
        // Find min/max values
        const minValue = Math.min(...values);
        const maxValue = Math.max(...values);
        const range = maxValue - minValue || 1; // Avoid division by zero
        
        // Draw the sparkline
        ctx.strokeStyle = color;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        
        values.forEach((value, index) => {
            const x = padding + (index / (values.length - 1)) * drawWidth;
            const y = padding + drawHeight - ((value - minValue) / range) * drawHeight;
            
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        
        ctx.stroke();
        
        // Clear container and add canvas
        container.innerHTML = '';
        container.appendChild(canvas);
    }

    /**
     * Show the table and hide no data message
     */
    showTable() {
        this.tableContainer.style.display = 'block';
        this.noDataMessage.style.display = 'none';
    }

    /**
     * Show no data message and hide table
     */
    showNoData() {
        this.tableContainer.style.display = 'none';
        this.noDataMessage.style.display = 'block';
    }

    /**
     * Update the last updated timestamp
     * @param {string} datestamp - Latest datestamp
     */
    updateLastUpdated(datestamp) {
        if (this.lastUpdatedElement && datestamp) {
            const date = new Date(datestamp);
            this.lastUpdatedElement.textContent = `Last updated: ${date.toLocaleDateString()}`;
        }
    }

    /**
     * Navigate to detail view for a specific metric
     * @param {Object} metric - Metric data to show in detail view
     */
    navigateToDetail(metric) {
        console.log('Navigating to detail view for metric:', metric.metric_id, '-', metric.title);
        
        // Store metric info for detail view - use metric_id for data consistency
        const metricData = {
            metric_id: metric.metric_id,
            title: metric.title,
            currentScore: metric.currentScore,
            slo: metric.slo,
            slo_min: metric.slo_min,
            filters: this.currentFilters
        };
        
        // Use the detail manager to show the metric
        if (window.detailManager) {
            window.detailManager.showMetric(metricData);
        }
        
        // Switch to detail section
        if (window.dashboardApp) {
            window.dashboardApp.switchSection('detail');
        }
    }

    /**
     * Refresh scorecard with current filters
     */
    refresh() {
        this.loadScorecard(this.currentFilters);
    }
}

// Create global instance
window.scorecardManager = new ScorecardManager();