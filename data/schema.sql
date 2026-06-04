-- Schema for Exercise 2
-- Run this to create the tables in SQLite or PostgreSQL

CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    budget DECIMAL(12,2)
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    hire_date DATE,
    salary DECIMAL(10,2)
);

CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    start_date DATE,
    end_date DATE,
    status TEXT CHECK(status IN ('active', 'completed', 'cancelled'))
);

-- Sample data

INSERT INTO departments (id, name, budget) VALUES
(1, 'Engineering', 500000.00),
(2, 'Marketing', 200000.00),
(3, 'Sales', 300000.00),
(4, 'HR', 150000.00),
(5, 'Data Science', 400000.00),
(6, 'Finance', 250000.00);

INSERT INTO employees (id, name, department_id, hire_date, salary) VALUES
(1, 'Alice Mueller', 1, '2022-03-15', 85000.00),
(2, 'Bob Schmidt', 1, '2023-06-01', 78000.00),
(3, 'Clara Fischer', 2, '2021-09-10', 65000.00),
(4, 'David Weber', 3, '2023-11-20', 72000.00),
(5, 'Elena Braun', 1, '2024-01-10', 90000.00),
(6, 'Frank Huber', 5, '2022-07-01', 95000.00),
(7, 'Greta Wolf', 5, '2023-08-15', 88000.00),
(8, 'Hans Richter', 4, '2020-01-05', 60000.00),
(9, 'Irene Koch', 3, '2024-04-01', 68000.00),
(10, 'Jan Bauer', 2, '2023-12-01', 62000.00),
(11, 'Katrin Vogel', 6, '2022-05-20', 75000.00),
(12, 'Leon Schreiber', 1, '2025-08-01', 82000.00),
(13, 'Maria Neumann', 5, '2025-09-15', 91000.00),
(14, 'Nils Hartmann', 3, '2025-10-01', 70000.00),
(15, 'Olga Peters', 6, '2021-11-01', 73000.00),
(16, 'Paul Zimmermann', 1, '2024-06-15', 80000.00),
(17, 'Rita Schwarz', 2, '2025-11-01', 64000.00);

INSERT INTO projects (id, name, department_id, start_date, end_date, status) VALUES
(1, 'Platform Redesign', 1, '2024-01-01', '2024-06-30', 'completed'),
(2, 'Mobile App v2', 1, '2024-07-01', NULL, 'active'),
(3, 'Brand Campaign', 2, '2024-03-01', '2024-05-31', 'completed'),
(4, 'CRM Migration', 3, '2024-06-01', NULL, 'active'),
(5, 'ML Pipeline', 5, '2024-02-01', '2024-08-31', 'completed'),
(6, 'Recruitment Portal', 4, '2024-04-01', '2024-07-15', 'cancelled'),
(7, 'Data Warehouse', 5, '2024-09-01', NULL, 'active'),
(8, 'Sales Automation', 3, '2024-10-01', '2025-02-28', 'completed'),
(9, 'API Gateway', 1, '2025-01-01', NULL, 'active'),
(10, 'Customer Insights', 5, '2025-03-01', NULL, 'active');
