-- Exercise 2: SQL
-- ======================
-- This exercise has three levels. Complete as far as you can.
--
-- To test your queries, run:
--   python exercises/run_sql.py
--
-- This will execute each query against an in-memory SQLite database
-- loaded with the sample data from data/schema.sql.


-- ============================================================
-- BASE LEVEL — Simple queries
-- ============================================================

-- Query 1: List all employees sorted by name alphabetically.
-- Expected columns: name, salary, hire_date

SELECT name, salary, hire_date from employees ORDER BY name ASC;

-- Query 2: List all employees with their department name.
-- (Hint: you need to JOIN two tables)
-- Expected columns: employee_name, department_name

SELECT e.name AS employee_name, d.name AS department_name FROM employees e JOIN departments d ON e.department_id = d.id;

-- Query 3: Count how many employees are in each department.
-- Expected columns: department_name, employee_count

SELECT d.name AS department_name, COUNT(e.id) AS employee_count FROM departments d JOIN employees e ON e.department_id = d.id GROUP BY department_name;

-- ============================================================
-- STANDARD LEVEL — JOINs, aggregations, filtering
-- ============================================================

-- Query 4: Find the top 3 departments by average salary.
-- Expected columns: department_name, avg_salary

SELECT d.name AS department_name, AVG(e.salary) AS avg_salary FROM departments d JOIN employees e ON e.department_id = d.id GROUP BY department_name ORDER BY avg_salary DESC LIMIT 3;

-- Query 5: Find departments where the total employee salary exceeds the department budget.
-- Expected columns: department_name, total_salary, budget

SELECT d.name AS department_name, SUM(e.salary) AS total_salary, d.budget AS budget FROM departments d JOIN employees e ON d.id = e.department_id GROUP BY department_name, budget HAVING total_salary > budget;

-- Query 6: Count the number of active projects per department,
--          including departments with zero active projects.
-- Expected columns: department_name, active_project_count

SELECT d.name AS department_name, COUNT(p.id) AS active_project_count FROM departments d LEFT JOIN projects p ON d.id = p.department_id AND status = 'active' GROUP BY department_name;

-- ============================================================
-- ADVANCED LEVEL — Subqueries, complex logic
-- ============================================================

-- Query 7: Find employees who were hired in the last 12 months and work in departments
--          with at least one completed project.
-- Expected columns: employee_name, department_name, hire_date



-- Query 8: Rank departments by their "project success rate"
--          (completed projects / total projects). Exclude departments with no projects.
-- Expected columns: department_name, total_projects, completed_projects, success_rate



-- Query 9: For each department, find the employee with the highest salary.
--          If multiple employees tie, show all of them.
-- Expected columns: department_name, employee_name, salary


