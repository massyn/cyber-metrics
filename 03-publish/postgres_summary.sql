-- Create the summary table
CREATE TABLE IF NOT EXISTS summary
(
    total double precision,
    totalok double precision,
    metric_id text,
    title text,
    slo double precision,
    slo_min double precision,
    weight double precision,
    category text,
    datestamp date,
    business_unit text,
    team text,
    location text
);

-- Remove the old data that will be replaced in case another run is needed
DELETE FROM summary
WHERE (metric_id, datestamp) IN (
    SELECT DISTINCT
        d.metric_id,
        CAST(d.datestamp AS date) AS datestamp
    FROM
        detail AS d
);

-- Insert the new data based on the detail data that has already been loaded
INSERT INTO summary (
    metric_id,
    title,
    datestamp,
    slo,
    slo_min,
    weight,
    category,
    business_unit,
    team,
    location,
    total,
    totalok
)
SELECT
    d.metric_id,
    d.title,
    CAST(d.datestamp AS date) AS datestamp,
    d.slo,
    d.slo_min,
    d.weight,
    d.category,
    d.business_unit,
    d.team,
    d.location,
    COUNT(d.compliance) AS total,
    SUM(d.compliance) AS totalok
FROM
    detail AS d
GROUP BY
    d.metric_id,
    d.title,
    d.datestamp,
    d.slo,
    d.slo_min,
    d.weight,
    d.category,
    d.business_unit,
    d.team,
    d.location;

-- Create the view that will be used to display the summary data.  It will only show the last 12 months of data,
-- or less if there is not enough data to fill 12 months.  The data will be evenly spaced out over the last year.  The schema is
-- the same as the summary table.  The view will be used to display the data in the dashboard, thus reducing the total
-- volume of data that needs to be loaded, improving performance and reducing the amount of data that needs to be stored.
CREATE OR REPLACE VIEW v_summary AS
WITH available_dates AS (
    SELECT DISTINCT datestamp
    FROM summary
    WHERE datestamp >= (CURRENT_DATE - interval '1 year')
    ORDER BY datestamp
),

row_numbered_dates AS (
    SELECT
        datestamp,
        ROW_NUMBER() OVER (ORDER BY datestamp) AS row_num,
        COUNT(*) OVER () AS total_rows
    FROM available_dates
),

selected_dates AS (
    SELECT datestamp
    FROM row_numbered_dates
    WHERE
        row_num = total_rows -- Always include the latest date
        OR row_num = 1 -- Always include the earliest date
        -- Evenly distribute other dates
        OR row_num % (CEIL(total_rows / 12.0)) = 0
    ORDER BY datestamp
    LIMIT 12
)

SELECT s.*
FROM
    summary AS s
INNER JOIN selected_dates AS d ON s.datestamp = d.datestamp
ORDER BY datestamp;
