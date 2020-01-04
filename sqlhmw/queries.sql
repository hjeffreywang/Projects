--1	 List the following details of each employee: employee number, last name, first name, gender, and salary.

select employee.emp_num, last_name, first_name, gender, salary
from employee
inner join employees on employee.emp_num = salary.emp_num;



-- 2	List employees who were hired in 1986.

select * from employee
where extract(year from hire_date)=1986;



-- 3	List the manager of each department with the following information: 
-- 	department number, department name, the manager’s employee number, last name, first name, and start and end employment dates.

select department_manager.dept_num, department.dept_name, department_manager.emp_num, 
	employee.last_name, employee.first_name, employee.hire_date, department_manager.to_date
from department_manager
inner join employee on employee.emp_num = department_manager.emp_num
inner join department on department.dept_num=department_manager.dept_num;


-- 4	List the department of each employee with the following information: employee number, last name, first name, and department name.

select employee.last_name, employee_department.emp_num,  department.dept_name, employee.first_name
from employee_department
inner join employee on employee.emp_num = employee_department.emp_num
inner join department on department.dept_num=employee_department.dept_num;

-- 5	List all employees whose first name is “Hercules” and last names begin with “B.”
select first_name, last_name
from employee
where first_name='Hercules' and last_name like 'B%';


-- 6	List all employees in the Sales department, including their employee number, last name, first name, and department name.

select employee_department.emp_num, last_name, first_name, department.dept_name
from employee_department
inner join employee on employee_department.emp_num=employee.emp_num
inner join department on employee_department.dept_num=department.dept_num
where employee_department.dept_num='d007';



-- 7	List all employees in the Sales and Development departments, including their employee number, last name, first name, and department name.
-- d007 and d005 are the sales and development departments


select employee_department.emp_num, last_name, first_name, department.dept_name
from employee_department
inner join employee on employee_department.emp_num=employee.emp_num
inner join department on employee_department.dept_num=department.dept_num
where employee_department.dept_num='d007' or employee_department.dept_num='d005';



-- 8	In descending order, list the frequency count of employee last names, i.e., how many employees share each last name.

select last_name, count(*) as frequency
from employee
group by last_name
order by frequency desc;