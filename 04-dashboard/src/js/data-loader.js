/**
 * Data Loader Module
 * Handles loading and caching of JSON data files
 */

class DataLoader {
    constructor() {
        this.cacheExpiration = 60 * 60 * 1000; // 1 hour in milliseconds
        this.cache = new Map();
    }

    /**
     * Load JSON data with caching
     * @param {string} fileName - Name of the JSON file (summary.json or detail.json)
     * @returns {Promise<Object|null>} Parsed JSON data or null if error
     */
    async loadData(fileName) {
        const cacheKey = fileName;
        const now = Date.now();

        // Check if we have cached data that's still valid
        if (this.cache.has(cacheKey)) {
            const cachedData = this.cache.get(cacheKey);
            if (now - cachedData.timestamp < this.cacheExpiration) {
                console.log(`Using cached data for ${fileName}`);
                return cachedData.data;
            } else {
                console.log(`Cache expired for ${fileName}, reloading...`);
                this.cache.delete(cacheKey);
            }
        }

        try {
            const response = await fetch(`json/${fileName}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Cache the data with timestamp
            this.cache.set(cacheKey, {
                data: data,
                timestamp: now
            });

            console.log(`Loaded and cached ${fileName}`);
            return data;

        } catch (error) {
            console.error(`Error loading ${fileName}:`, error);
            return null;
        }
    }

    /**
     * Load summary data specifically
     * @returns {Promise<Array|null>} Summary data array or null
     */
    async loadSummaryData() {
        return await this.loadData('summary.json');
    }

    /**
     * Load detail data specifically
     * @returns {Promise<Array|null>} Detail data array or null
     */
    async loadDetailData() {
        return await this.loadData('detail.json');
    }

    /**
     * Get unique values from a field in the data
     * @param {Array} data - The data array
     * @param {string} field - The field name to extract unique values from
     * @returns {Array} Array of unique values
     */
    getUniqueValues(data, field) {
        if (!data || !Array.isArray(data)) {
            return [];
        }

        const values = data.map(item => item[field])
            .filter(value => value !== null && value !== undefined);

        const uniqueValues = [...new Set(values)];

        return uniqueValues.sort();
    }

    /**
     * Get the latest datestamp from the data
     * @param {Array} data - The data array
     * @returns {string|null} Latest datestamp or null
     */
    getLatestDatestamp(data) {
        if (!data || !Array.isArray(data)) {
            return null;
        }

        const datestamps = data.map(item => item.datestamp)
            .filter(date => date !== null && date !== undefined);

        if (datestamps.length === 0) {
            return null;
        }

        return datestamps.sort().pop();
    }

    /**
     * Filter data by latest datestamp only
     * @param {Array} data - The data array
     * @returns {Array} Filtered data with only latest datestamp
     */
    getLatestData(data) {
        if (!data || !Array.isArray(data)) {
            return [];
        }

        const latestDate = this.getLatestDatestamp(data);
        if (!latestDate) {
            return [];
        }

        return data.filter(item => item.datestamp === latestDate);
    }

    /**
     * Apply filters to data
     * @param {Array} data - The data array
     * @param {Object} filters - Filter object with business_unit, team, location strings
     * @returns {Array} Filtered data
     */
    applyFilters(data, filters) {
        if (!data || !Array.isArray(data)) {
            return [];
        }

        return data.filter(item => {
            // Check business_unit filter
            if (filters.business_unit && filters.business_unit !== '') {
                if (item.business_unit !== filters.business_unit) {
                    return false;
                }
            }

            // Check team filter
            if (filters.team && filters.team !== '') {
                if (item.team !== filters.team) {
                    return false;
                }
            }

            // Check location filter
            if (filters.location && filters.location !== '') {
                if (item.location !== filters.location) {
                    return false;
                }
            }

            return true;
        });
    }

    /**
     * Clear all cached data
     */
    clearCache() {
        this.cache.clear();
        console.log('Cache cleared');
    }

    /**
     * Get cache statistics
     * @returns {Object} Cache statistics
     */
    getCacheStats() {
        const stats = {
            size: this.cache.size,
            items: []
        };

        this.cache.forEach((value, key) => {
            const age = Date.now() - value.timestamp;
            const remaining = Math.max(0, this.cacheExpiration - age);
            
            stats.items.push({
                key: key,
                age: age,
                remaining: remaining,
                expired: remaining === 0
            });
        });

        return stats;
    }
}

// Create global instance
window.dataLoader = new DataLoader();