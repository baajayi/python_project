import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('life_exp.sqlite')
cursor = conn.cursor()

# SQL query to find the top 100 countries with the highest average life expectancy
query = """
SELECT 
    e.name AS country,
    le.year,
    le.life_expectancy
FROM life_expectancy le
JOIN entities e ON le.entity_id = e.entity_id
WHERE e.name IN (
    SELECT e.name
    FROM life_expectancy le
    JOIN entities e ON le.entity_id = e.entity_id
    GROUP BY e.name
    ORDER BY AVG(le.life_expectancy) DESC
    LIMIT 100
)
ORDER BY e.name, le.year;
"""

# Execute the query
cursor.execute(query)

# Fetch all rows
rows = cursor.fetchall()

# Close the connection
conn.close()

# Convert rows to a JSON-like list of dictionaries
data = [{'country': row[0], 'year': row[1], 'life_expectancy': row[2]} for row in rows]

# Optionally, print the data to check
with open('gexp.js', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2) # Print first 10 rows to check
