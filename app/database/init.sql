-- Employee information table
CREATE TABLE IF NOT EXISTS employees (
    employee_id VARCHAR(10) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    annual_leave_days INTEGER NOT NULL DEFAULT 0,
    used_leave_days INTEGER NOT NULL DEFAULT 0,

    CHECK (annual_leave_days >= 0),
    CHECK (used_leave_days >= 0),
    CHECK (used_leave_days <= annual_leave_days)
);

-- View to calculate remaining leave balance
CREATE OR REPLACE VIEW employee_leave_balances AS
SELECT
    employee_id,
    full_name,
    department,
    annual_leave_days,
    used_leave_days,
    annual_leave_days - used_leave_days
        AS remaining_leave_days
FROM employees;

-- Insert fictional employee records
INSERT INTO employees (
    employee_id,
    full_name,
    department,
    annual_leave_days,
    used_leave_days
)
VALUES
    ('E101', 'Rahul Sharma', 'Engineering', 20, 12),
    ('E102', 'Priya Mehta', 'Human Resources', 20, 8),
    ('E103', 'Amit Verma', 'Finance', 18, 13),
    ('E104', 'Neha Patel', 'IT Support', 20, 5)
ON CONFLICT (employee_id) DO NOTHING;