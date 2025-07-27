/**
 * Filter Management Module
 * Handles filter UI and state management
 */

class FilterManager {
    constructor() {
        this.currentFilters = {
            business_unit: '',
            team: '',
            location: ''
        };
        
        this.filterElements = {
            business_unit: document.getElementById('business-unit-filter'),
            team: document.getElementById('team-filter'),
            location: document.getElementById('location-filter')
        };
        
        this.clearButton = document.getElementById('clear-filters');
        
        this.onFiltersChanged = null; // Callback function
        
        this.initializeEventListeners();
    }

    /**
     * Initialize event listeners for filter controls
     */
    initializeEventListeners() {
        // Clear filters button
        this.clearButton.addEventListener('click', () => {
            this.clearAllFilters();
        });

        // Auto-apply filters on change
        Object.values(this.filterElements).forEach(element => {
            element.addEventListener('change', () => {
                this.applyFilters();
            });
        });
    }

    /**
     * Populate filter options from data
     * @param {Array} data - Summary data array
     */
    async populateFilters(data) {
        if (!data || !Array.isArray(data)) {
            this.showFilterError();
            return;
        }

        try {
            // Get latest data only for filter options
            const latestData = window.dataLoader.getLatestData(data);
            
            // Populate each filter
            this.populateFilterSelect('business_unit', latestData);
            this.populateFilterSelect('team', latestData);
            this.populateFilterSelect('location', latestData);
            
            console.log('Filters populated successfully');
        } catch (error) {
            console.error('Error populating filters:', error);
            this.showFilterError();
        }
    }

    /**
     * Populate a specific filter select element
     * @param {string} filterType - Type of filter (business_unit, team, location)
     * @param {Array} data - Data to extract unique values from
     */
    populateFilterSelect(filterType, data) {
        const selectElement = this.filterElements[filterType];
        if (!selectElement) return;

        // Get unique values
        const uniqueValues = window.dataLoader.getUniqueValues(data, filterType);
        
        // Clear existing options but keep the "All" option
        const allOptionText = selectElement.options[0].textContent;
        selectElement.innerHTML = '';
        
        // Add "All" option
        const allOption = document.createElement('option');
        allOption.value = '';
        allOption.textContent = allOptionText;
        selectElement.appendChild(allOption);
        
        if (uniqueValues.length === 0) {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = 'No data available';
            option.disabled = true;
            selectElement.appendChild(option);
            return;
        }

        // Add options
        uniqueValues.forEach(value => {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = value;
            selectElement.appendChild(option);
        });

        console.log(`Populated ${filterType} filter with ${uniqueValues.length} options`);
    }

    /**
     * Show error message in filter selects
     */
    showFilterError() {
        Object.entries(this.filterElements).forEach(([filterType, element]) => {
            const labels = {
                business_unit: 'All Business Units',
                team: 'All Teams', 
                location: 'All Locations'
            };
            element.innerHTML = `<option value="">${labels[filterType]}</option><option value="" disabled>Error loading data</option>`;
        });
    }

    /**
     * Apply current filter selections
     */
    applyFilters() {
        // Get selected values from each filter
        this.currentFilters.business_unit = this.getSelectedValue('business_unit');
        this.currentFilters.team = this.getSelectedValue('team');
        this.currentFilters.location = this.getSelectedValue('location');

        console.log('Applied filters:', this.currentFilters);

        // Trigger callback if set
        if (this.onFiltersChanged && typeof this.onFiltersChanged === 'function') {
            this.onFiltersChanged(this.currentFilters);
        }

        // Update UI to show applied state
        this.updateFilterButtonState();
    }

    /**
     * Get selected value from a filter select element
     * @param {string} filterType - Type of filter
     * @returns {string} Selected value
     */
    getSelectedValue(filterType) {
        const selectElement = this.filterElements[filterType];
        if (!selectElement) return '';

        return selectElement.value || '';
    }

    /**
     * Clear all filter selections
     */
    clearAllFilters() {
        // Clear selections in UI (reset to first option - "All")
        Object.values(this.filterElements).forEach(element => {
            element.selectedIndex = 0;
        });

        // Clear current filters
        this.currentFilters = {
            business_unit: '',
            team: '',
            location: ''
        };

        console.log('Cleared all filters');

        // Trigger callback if set
        if (this.onFiltersChanged && typeof this.onFiltersChanged === 'function') {
            this.onFiltersChanged(this.currentFilters);
        }

        // Update UI
        this.updateFilterButtonState();
    }

    /**
     * Update filter button states based on current selections
     */
    updateFilterButtonState() {
        const hasFilters = this.hasActiveFilters();
        
        this.clearButton.disabled = !hasFilters;
    }

    /**
     * Check if any filters are currently active
     * @returns {boolean} True if any filters are active
     */
    hasActiveFilters() {
        return this.currentFilters.business_unit !== '' ||
               this.currentFilters.team !== '' ||
               this.currentFilters.location !== '';
    }

    /**
     * Get current filter state
     * @returns {Object} Current filter object
     */
    getCurrentFilters() {
        return { ...this.currentFilters };
    }

    /**
     * Set callback function for when filters change
     * @param {Function} callback - Function to call when filters change
     */
    setOnFiltersChanged(callback) {
        this.onFiltersChanged = callback;
    }

    /**
     * Programmatically set filter values
     * @param {Object} filters - Filter object with string values
     */
    setFilters(filters) {
        if (!filters) return;

        // Set selections in UI
        if (filters.business_unit !== undefined) {
            this.setSelectValue('business_unit', filters.business_unit);
        }
        if (filters.team !== undefined) {
            this.setSelectValue('team', filters.team);
        }
        if (filters.location !== undefined) {
            this.setSelectValue('location', filters.location);
        }

        // Apply the filters
        this.applyFilters();
    }

    /**
     * Set selected value for a specific filter
     * @param {string} filterType - Type of filter
     * @param {string} value - Value to select
     */
    setSelectValue(filterType, value) {
        const selectElement = this.filterElements[filterType];
        if (!selectElement) return;

        // Set the selected value
        selectElement.value = value || '';
    }

    /**
     * Get filter summary for display
     * @returns {string} Human-readable filter summary
     */
    getFilterSummary() {
        const summaryParts = [];

        if (this.currentFilters.business_unit) {
            summaryParts.push(`Business Unit: ${this.currentFilters.business_unit}`);
        }
        if (this.currentFilters.team) {
            summaryParts.push(`Team: ${this.currentFilters.team}`);
        }
        if (this.currentFilters.location) {
            summaryParts.push(`Location: ${this.currentFilters.location}`);
        }

        return summaryParts.length > 0 ? summaryParts.join(' | ') : 'No filters applied';
    }
}

// Create global instance
window.filterManager = new FilterManager();