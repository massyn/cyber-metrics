/**
 * Main Application Module
 * Coordinates all dashboard functionality
 */

class DashboardApp {
    constructor() {
        this.currentSection = 'overview';
        this.summaryData = null;
        this.detailData = null;
        this.isLoading = false;
        this.currentFilters = {};
        
        this.initializeApp();
    }

    /**
     * Initialize the application
     */
    async initializeApp() {
        console.log('Initializing Security Dashboard...');
        
        try {
            // Set up navigation
            this.initializeNavigation();
            
            // Set up filter callbacks
            this.initializeFilters();
            
            // Show loading state
            this.showLoading();
            
            // Load initial data
            await this.loadInitialData();
            
            // Hide loading state
            this.hideLoading();
            
            console.log('Dashboard initialized successfully');
            
        } catch (error) {
            console.error('Error initializing dashboard:', error);
            this.showError('Failed to initialize dashboard. Please refresh the page.');
        }
    }

    /**
     * Initialize navigation functionality
     */
    initializeNavigation() {
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                
                const targetSection = link.getAttribute('href').substring(1); // Remove #
                this.switchSection(targetSection);
            });
        });
        
        // Initialize with overview section
        this.switchSection('overview');
    }

    /**
     * Initialize filter system
     */
    initializeFilters() {
        // Set callback for when filters change
        window.filterManager.setOnFiltersChanged((filters) => {
            this.onFiltersChanged(filters);
        });
    }

    /**
     * Load initial data
     */
    async loadInitialData() {
        try {
            console.log('Loading summary data...');
            
            // Load summary data
            this.summaryData = await window.dataLoader.loadSummaryData();
            
            if (!this.summaryData) {
                throw new Error('Failed to load summary data');
            }
            
            console.log(`Loaded ${this.summaryData.length} summary records`);
            
            // Populate filters
            await window.filterManager.populateFilters(this.summaryData);
            
            // Update chart with initial data
            this.updateOverviewChart();
            
            // Update overview cards
            this.updateOverviewCards();
            
            // Update last updated timestamp
            this.updateLastUpdatedTime();
            
        } catch (error) {
            console.error('Error loading initial data:', error);
            this.showDataError();
        }
    }

    /**
     * Handle filter changes
     * @param {Object} filters - Applied filters
     */
    onFiltersChanged(filters) {
        console.log('Filters changed:', filters);
        
        // Store filters globally for persistence across sections
        this.currentFilters = filters;
        
        if (this.currentSection === 'overview') {
            this.updateOverviewChart(filters);
            this.updateOverviewCards(filters);
        } else if (this.currentSection === 'scorecard') {
            this.updateScorecard(filters);
        } else if (this.currentSection === 'detail') {
            // Update detail view if it's currently active
            if (window.detailManager && window.detailManager.currentMetric) {
                window.detailManager.updateFilters(filters);
            }
        }
    }

    /**
     * Update overview chart with current data and filters
     * @param {Object} filters - Optional filters to apply
     */
    updateOverviewChart(filters = null) {
        if (!this.summaryData) {
            window.chartManager.showNoData();
            return;
        }
        
        try {
            const activeFilters = filters || this.currentFilters || window.filterManager.getCurrentFilters();
            window.chartManager.updateChart(this.summaryData, activeFilters);
            
            // Log chart statistics
            const stats = window.chartManager.getChartStats();
            if (stats) {
                console.log(`Chart updated: ${stats.dataPoints} points, avg score: ${(stats.averageScore * 100).toFixed(1)}%`);
            }
            
        } catch (error) {
            console.error('Error updating overview chart:', error);
            window.chartManager.showNoData();
        }
    }

    /**
     * Update overview cards with current data and filters
     * @param {Object} filters - Optional filters to apply
     */
    updateOverviewCards(filters = null) {
        if (!this.summaryData) {
            this.showOverviewCardsError();
            return;
        }
        
        try {
            const activeFilters = filters || this.currentFilters || window.filterManager.getCurrentFilters();
            const overallScores = window.chartManager.getLatestOverallScores(this.summaryData, activeFilters);
            
            if (overallScores) {
                this.populateOverviewCards(overallScores);
                console.log('Overview cards updated with latest scores');
            } else {
                this.showOverviewCardsError();
            }
            
        } catch (error) {
            console.error('Error updating overview cards:', error);
            this.showOverviewCardsError();
        }
    }

    /**
     * Populate overview cards with calculated scores
     * @param {Object} scores - Overall scores object
     */
    populateOverviewCards(scores) {
        // Update score badge
        const scoreBadge = document.getElementById('overview-score-badge');
        if (scoreBadge) {
            const scorePercentage = (scores.overallScore * 100).toFixed(1) + '%';
            const badgeClass = this.getScoreColorClass(scores.overallScore, scores.averageSlo, scores.averageSloMin);
            scoreBadge.className = `badge fs-6 ${badgeClass}`;
            scoreBadge.textContent = scorePercentage;
        }
        
        // Update SLO values
        const sloValue = document.getElementById('overview-slo-value');
        if (sloValue) {
            sloValue.textContent = (scores.averageSlo * 100).toFixed(1) + '%';
        }
        
        const sloMinValue = document.getElementById('overview-slo-min-value');
        if (sloMinValue) {
            sloMinValue.textContent = (scores.averageSloMin * 100).toFixed(1) + '%';
        }
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
     * Show error state for overview cards
     */
    showOverviewCardsError() {
        const scoreBadge = document.getElementById('overview-score-badge');
        if (scoreBadge) {
            scoreBadge.className = 'badge fs-6 bg-secondary';
            scoreBadge.textContent = 'No Data';
        }
        
        const sloValue = document.getElementById('overview-slo-value');
        if (sloValue) {
            sloValue.textContent = '-';
        }
        
        const sloMinValue = document.getElementById('overview-slo-min-value');
        if (sloMinValue) {
            sloMinValue.textContent = '-';
        }
    }

    /**
     * Update scorecard with current data and filters
     * @param {Object} filters - Optional filters to apply
     */
    updateScorecard(filters = null) {
        if (!this.summaryData) {
            window.scorecardManager.showNoData();
            return;
        }
        
        try {
            const activeFilters = filters || this.currentFilters || window.filterManager.getCurrentFilters();
            window.scorecardManager.loadScorecard(activeFilters);
            
            console.log('Scorecard updated with filters:', activeFilters);
            
        } catch (error) {
            console.error('Error updating scorecard:', error);
            window.scorecardManager.showNoData();
        }
    }

    /**
     * Switch between dashboard sections
     * @param {string} sectionName - Name of section to show
     */
    switchSection(sectionName) {
        // Hide all sections
        const sections = document.querySelectorAll('.content-section');
        sections.forEach(section => {
            section.style.display = 'none';
        });
        
        // Show target section
        const targetSection = document.getElementById(`${sectionName}-section`);
        if (targetSection) {
            targetSection.style.display = 'block';
        }
        
        // Update navigation
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.classList.remove('active');
        });
        
        const activeLink = document.getElementById(`nav-${sectionName}`);
        if (activeLink) {
            activeLink.classList.add('active');
        }
        
        this.currentSection = sectionName;
        
        // Handle section-specific logic
        if (sectionName === 'overview' && this.summaryData) {
            // Refresh chart and cards when switching to overview with current filters
            setTimeout(() => {
                window.chartManager.resize();
                this.updateOverviewChart(this.currentFilters);
                this.updateOverviewCards(this.currentFilters);
            }, 100);
        } else if (sectionName === 'scorecard' && this.summaryData) {
            // Load scorecard when switching to scorecard with current filters
            setTimeout(() => {
                this.updateScorecard(this.currentFilters);
            }, 100);
        } else if (sectionName === 'detail') {
            // Detail view is handled by detailManager directly
            // No additional action needed here
        }
        
        console.log(`Switched to ${sectionName} section`);
    }

    /**
     * Show loading state
     */
    showLoading() {
        this.isLoading = true;
        
        // Add loading class to main elements
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.classList.add('loading');
        }
        
        // Show loading in last updated
        const lastUpdated = document.getElementById('last-updated');
        if (lastUpdated) {
            lastUpdated.textContent = 'Loading...';
        }
    }

    /**
     * Hide loading state
     */
    hideLoading() {
        this.isLoading = false;
        
        // Remove loading class
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.classList.remove('loading');
        }
    }

    /**
     * Show data error state
     */
    showDataError() {
        // Show no data message in chart
        window.chartManager.showNoData();
        
        // Update last updated with error
        const lastUpdated = document.getElementById('last-updated');
        if (lastUpdated) {
            lastUpdated.textContent = 'Error loading data';
            lastUpdated.classList.add('text-danger');
        }
        
        console.error('Data error state activated');
    }

    /**
     * Show general error message
     * @param {string} message - Error message to display
     */
    showError(message) {
        // You could implement a toast/alert system here
        console.error('Application error:', message);
        alert(message); // Simple fallback
    }

    /**
     * Update last updated timestamp
     */
    updateLastUpdatedTime() {
        const lastUpdated = document.getElementById('last-updated');
        if (!lastUpdated) return;
        
        try {
            if (this.summaryData && this.summaryData.length > 0) {
                const latestDate = window.dataLoader.getLatestDatestamp(this.summaryData);
                if (latestDate) {
                    const date = new Date(latestDate + 'T00:00:00');
                    const formattedDate = date.toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric'
                    });
                    lastUpdated.textContent = `Last updated: ${formattedDate}`;
                    lastUpdated.classList.remove('text-danger');
                } else {
                    lastUpdated.textContent = 'Last updated: Unknown';
                }
            }
        } catch (error) {
            console.error('Error updating timestamp:', error);
            lastUpdated.textContent = 'Last updated: Error';
        }
    }

    /**
     * Refresh data (reload from source)
     */
    async refreshData() {
        if (this.isLoading) {
            console.log('Already loading, skipping refresh');
            return;
        }
        
        try {
            this.showLoading();
            
            // Clear cache to force reload
            window.dataLoader.clearCache();
            
            // Reload data
            await this.loadInitialData();
            
            this.hideLoading();
            
            console.log('Data refreshed successfully');
            
        } catch (error) {
            console.error('Error refreshing data:', error);
            this.showError('Failed to refresh data. Please try again.');
            this.hideLoading();
        }
    }

    /**
     * Get current filters
     * @returns {Object} Current filter state
     */
    getCurrentFilters() {
        return this.currentFilters;
    }

    /**
     * Get application status
     * @returns {Object} Application status information
     */
    getStatus() {
        return {
            currentSection: this.currentSection,
            isLoading: this.isLoading,
            hasData: this.summaryData !== null,
            dataRecords: this.summaryData ? this.summaryData.length : 0,
            filters: this.currentFilters,
            chartStats: window.chartManager.getChartStats(),
            cacheStats: window.dataLoader.getCacheStats()
        };
    }
}

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, starting dashboard application...');
    window.dashboardApp = new DashboardApp();
});

// Handle window resize for chart responsiveness
window.addEventListener('resize', () => {
    if (window.chartManager) {
        window.chartManager.resize();
    }
});

// Add keyboard shortcuts
document.addEventListener('keydown', (event) => {
    // Ctrl+R or F5 for refresh
    if ((event.ctrlKey && event.key === 'r') || event.key === 'F5') {
        event.preventDefault();
        if (window.dashboardApp) {
            window.dashboardApp.refreshData();
        }
    }
    
    // Escape to clear filters
    if (event.key === 'Escape') {
        if (window.filterManager) {
            window.filterManager.clearAllFilters();
        }
    }
});