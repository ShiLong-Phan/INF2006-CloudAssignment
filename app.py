from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import statistics
from decimal import Decimal

app = Flask(__name__)
CORS(app) # This handles the "CORS" security requirement locally

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="inf2006"
    )

def decimal_to_float(obj):
    """Convert Decimal objects to float for JSON serialization"""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {key: decimal_to_float(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_float(item) for item in obj]
    return obj

# 1. DESCRIPTIVE STATISTICS ENDPOINTS

@app.route('/analytics/descriptive_stats')
def descriptive_stats():
    """Get descriptive statistics for salary and employment data"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    year = request.args.get('year', 2023)
    university = request.args.get('university', '')
    
    # Base query
    query = """
        SELECT 
            AVG(e.gross_monthly_mean) as avg_salary,
            MIN(e.gross_monthly_mean) as min_salary,
            MAX(e.gross_monthly_mean) as max_salary,
            STDDEV(e.gross_monthly_mean) as salary_std,
            AVG(e.employment_rate_overall) as avg_employment_rate,
            MIN(e.employment_rate_overall) as min_employment_rate,
            MAX(e.employment_rate_overall) as max_employment_rate,
            STDDEV(e.employment_rate_overall) as employment_rate_std
        FROM employment_outcomes e
        JOIN degrees d ON e.degree_id = d.degree_id
        JOIN schools s ON d.school_id = s.school_id
        JOIN universities u ON s.university_id = u.university_id
        WHERE e.year = %s AND e.gross_monthly_mean IS NOT NULL
    """
    
    params = [year]
    
    # Add university filter if specified
    if university:
        query += " AND u.university_name = %s"
        params.append(university)
    
    cursor.execute(query, params)
    data = cursor.fetchone()
    conn.close()
    
    return jsonify(decimal_to_float(data))

@app.route('/analytics/salary_distribution/<int:year>')
def salary_distribution(year):
    """Get salary distribution by ranges for histogram"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            CASE 
                WHEN gross_monthly_mean < 3000 THEN '< $3,000'
                WHEN gross_monthly_mean < 4000 THEN '$3,000 - $4,000'
                WHEN gross_monthly_mean < 5000 THEN '$4,000 - $5,000'
                WHEN gross_monthly_mean < 6000 THEN '$5,000 - $6,000'
                WHEN gross_monthly_mean < 7000 THEN '$6,000 - $7,000'
                ELSE '≥ $7,000'
            END as salary_range,
            COUNT(*) as count
        FROM employment_outcomes e
        WHERE e.year = %s AND gross_monthly_mean IS NOT NULL
        GROUP BY salary_range
        ORDER BY MIN(gross_monthly_mean)
    """
    
    cursor.execute(query, (year,))
    data = cursor.fetchall()
    conn.close()
    
    return jsonify(decimal_to_float(data))

# 2. GROUP-BY ANALYSIS ENDPOINTS

@app.route('/analytics/university_comparison')
def university_comparison():
    """Compare universities by average salary and employment rate"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    year = request.args.get('year', 2023)
    
    query = """
        SELECT 
            u.university_name,
            AVG(e.gross_monthly_mean) as avg_salary,
            AVG(e.employment_rate_overall) as avg_employment_rate,
            COUNT(*) as program_count
        FROM employment_outcomes e
        JOIN degrees d ON e.degree_id = d.degree_id
        JOIN schools s ON d.school_id = s.school_id
        JOIN universities u ON s.university_id = u.university_id
        WHERE e.year = %s
        GROUP BY u.university_name
        ORDER BY avg_salary DESC
    """
    
    cursor.execute(query, (year,))
    data = cursor.fetchall()
    conn.close()
    
    return jsonify(decimal_to_float(data))

@app.route('/analytics/school_performance/<university_name>')
def school_performance(university_name):
    """Get school performance within a university"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    year = request.args.get('year', 2023)
    
    query = """
        SELECT 
            s.name as school_name,
            AVG(e.gross_monthly_mean) as avg_salary,
            AVG(e.employment_rate_overall) as avg_employment_rate,
            COUNT(*) as program_count
        FROM employment_outcomes e
        JOIN degrees d ON e.degree_id = d.degree_id
        JOIN schools s ON d.school_id = s.school_id
        JOIN universities u ON s.university_id = u.university_id
        WHERE u.university_name = %s AND e.year = %s
        GROUP BY s.name
        ORDER BY avg_salary DESC
    """
    
    cursor.execute(query, (university_name, year))
    data = cursor.fetchall()
    conn.close()
    
    return jsonify(decimal_to_float(data))

# 3. TIME-SERIES ANALYSIS ENDPOINTS

@app.route('/analytics/salary_trends')
def salary_trends():
    """Get salary trends over time by university"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            u.university_name,
            e.year,
            AVG(e.gross_monthly_mean) as avg_salary
        FROM employment_outcomes e
        JOIN degrees d ON e.degree_id = d.degree_id
        JOIN schools s ON d.school_id = s.school_id
        JOIN universities u ON s.university_id = u.university_id
        GROUP BY u.university_name, e.year
        ORDER BY u.university_name, e.year
    """
    
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    
    return jsonify(decimal_to_float(data))


# 4. COMPARATIVE ANALYSIS ENDPOINTS

@app.route('/analytics/year_comparison/<int:year1>/<int:year2>')
def year_comparison(year1, year2):
    """Compare statistics between two years"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            u.university_name,
            AVG(CASE WHEN e.year = %s THEN e.gross_monthly_mean END) as salary_year1,
            AVG(CASE WHEN e.year = %s THEN e.gross_monthly_mean END) as salary_year2,
            AVG(CASE WHEN e.year = %s THEN e.employment_rate_overall END) as employment_year1,
            AVG(CASE WHEN e.year = %s THEN e.employment_rate_overall END) as employment_year2
        FROM employment_outcomes e
        JOIN degrees d ON e.degree_id = d.degree_id
        JOIN schools s ON d.school_id = s.school_id
        JOIN universities u ON s.university_id = u.university_id
        WHERE e.year IN (%s, %s)
        GROUP BY u.university_name
        HAVING salary_year1 IS NOT NULL AND salary_year2 IS NOT NULL
        ORDER BY u.university_name
    """
    
    cursor.execute(query, (year1, year2, year1, year2, year1, year2))
    data = cursor.fetchall()
    conn.close()
    
    return jsonify(decimal_to_float(data))

@app.route('/analytics/top_performing_programs')
def top_performing_programs():
    """Get top performing programs by salary and employment rate"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    year = request.args.get('year', 2023)
    limit = request.args.get('limit', 10)
    university = request.args.get('university', '')
    
    # Base query
    query = """
        SELECT 
            u.university_name,
            s.name as school_name,
            d.name as degree_name,
            e.gross_monthly_mean as salary,
            e.employment_rate_overall as employment_rate,
            (e.gross_monthly_mean * 0.6 + e.employment_rate_overall * 50) as performance_score
        FROM employment_outcomes e
        JOIN degrees d ON e.degree_id = d.degree_id
        JOIN schools s ON d.school_id = s.school_id
        JOIN universities u ON s.university_id = u.university_id
        WHERE e.year = %s
    """
    
    params = [year]
    
    # Add university filter if specified
    if university:
        query += " AND u.university_name = %s"
        params.append(university)
    
    query += " ORDER BY performance_score DESC LIMIT %s"
    params.append(int(limit))
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    
    return jsonify(decimal_to_float(data))

# 5. STATISTICAL PROJECTIONS ENDPOINTS

@app.route('/analytics/salary_projection/<university_name>')
def salary_projection(university_name):
    """Simple linear trend projection for salary"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            e.year,
            AVG(e.gross_monthly_mean) as avg_salary
        FROM employment_outcomes e
        JOIN degrees d ON e.degree_id = d.degree_id
        JOIN schools s ON d.school_id = s.school_id
        JOIN universities u ON s.university_id = u.university_id
        WHERE u.university_name = %s
        GROUP BY e.year
        ORDER BY e.year
    """
    
    cursor.execute(query, (university_name,))
    data = cursor.fetchall()
    conn.close()
    
    # Simple linear regression for projection
    if len(data) >= 2:
        years = [row['year'] for row in data]
        salaries = [float(row['avg_salary']) for row in data]
        
        # Calculate linear trend
        n = len(years)
        sum_x = sum(years)
        sum_y = sum(salaries)
        sum_xy = sum(x * y for x, y in zip(years, salaries))
        sum_x2 = sum(x * x for x in years)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        intercept = (sum_y - slope * sum_x) / n
        
        # Project next 2 years
        last_year = max(years)
        projections = []
        for i in range(1, 3):
            proj_year = last_year + i
            proj_salary = slope * proj_year + intercept
            projections.append({
                'year': proj_year,
                'projected_salary': round(proj_salary, 2)
            })
        
        return jsonify({
            'historical_data': decimal_to_float(data),
            'projections': projections,
            'trend_slope': round(slope, 2)
        })
    
    return jsonify({'historical_data': decimal_to_float(data), 'projections': []})

# 6. UTILITY ENDPOINTS

@app.route('/analytics/universities')
def get_universities():
    """Get list of all universities"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT university_name FROM universities ORDER BY university_name")
        universities = [row[0] for row in cursor.fetchall()]
        print(f"Available universities: {universities}")
        conn.close()
        
        return jsonify(universities)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": "Database connection failed", "message": str(err)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500

@app.route('/analytics/degrees/<university_name>')
def get_degrees(university_name):
    """Get list of degree programs for a specific university"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # First, let's check what universities exist
    cursor.execute("SELECT DISTINCT university_name FROM universities ORDER BY university_name")
    all_universities = [row[0] for row in cursor.fetchall()]
    print(f"Available universities: {all_universities}")
    print(f"Requested university: '{university_name}'")
    
    query = """
        SELECT DISTINCT d.name as degree_name 
        FROM degrees d
        JOIN schools s ON d.school_id = s.school_id
        JOIN universities u ON s.university_id = u.university_id 
        WHERE u.university_name = %s 
        ORDER BY d.name
    """
    cursor.execute(query, (university_name,))
    degrees = [row[0] for row in cursor.fetchall()]
    print(f"Found {len(degrees)} degree programs for university '{university_name}': {degrees}")
    conn.close()
    
    return jsonify(degrees)

@app.route('/analytics/debug/university-degrees')
def debug_university_degrees():
    """Debug endpoint to see university-degree relationships"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            u.university_id,
            u.university_name,
            s.school_id,
            s.name as school_name,
            d.degree_id,
            d.name as degree_name
        FROM universities u
        LEFT JOIN schools s ON u.university_id = s.university_id
        LEFT JOIN degrees d ON s.school_id = d.school_id
        ORDER BY u.university_name, s.name, d.name
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    
    return jsonify(data)

@app.route('/analytics/years')
def get_years():
    """Get list of all available years"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT year FROM years ORDER BY year")
    years = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(years)

@app.route('/test')
def test():
    """Simple test endpoint that doesn't require database"""
    return jsonify({"status": "Flask server is running!", "message": "Database endpoints may require MySQL to be running"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)