--Create Tables
--Import data csvs
--Attach Foreign Keys


CREATE TABLE "Employee" (
  "id" SERIAL,
  "emp_num" INT UNIQUE PRIMARY KEY NOT NULL,
  "birth_date" DATE NOT NULL,
  "first_name" VARCHAR(20) NOT NULL,
  "last_name" VARCHAR(20) NOT NULL,
  "gender" CHAR(1) NOT NULL,
  "hire_date" DATE NOT NULL
);

CREATE TABLE "Department" (
  "id" SERIAL,
  "dept_num" CHAR(10) UNIQUE PRIMARY KEY NOT NULL,
  "dept_name" VARCHAR(23) NOT NULL
);

CREATE TABLE "Title" (
  "id" SERIAL,
  "emp_num" INT NOT NULL,
  "title" VARCHAR(30) NOT NULL,
  "from_date" DATE NOT NULL,
  "to_date" DATE NOT NULL
);

CREATE TABLE "Employee_Department" (
  "id" SERIAL,
  "emp_num" INT NOT NULL,
  "dept_num" VARCHAR(4) NOT NULL,
  "from_date" DATE NOT NULL,
  "to_date" DATE NOT NULL
);

CREATE TABLE "Department_Manager" (
  "id" SERIAL,
  "dept_num" VARCHAR(10) NOT NULL,
  "emp_num" INT NOT NULL,
  "from_date" DATE NOT NULL,
  "to_date" DATE NOT NULL
);

CREATE TABLE "Salary" (
  "id" SERIAL,
  "emp_num" INT NOT NULL,
  "salary" INT NOT NULL,
  "from_date" DATE NOT NULL,
  "to_date" DATE NOT NULL
);

ALTER TABLE "Employee_Department" ADD FOREIGN KEY ("emp_num") REFERENCES "Employee" ("emp_num");

ALTER TABLE "Employee_Department" ADD FOREIGN KEY ("dept_num") REFERENCES "Department" ("dept_num");

ALTER TABLE "Department_Manager" ADD FOREIGN KEY ("dept_num") REFERENCES "Department" ("dept_num");

ALTER TABLE "Department_Manager" ADD FOREIGN KEY ("emp_num") REFERENCES "Employee" ("emp_num");

ALTER TABLE "Salary" ADD FOREIGN KEY ("emp_num") REFERENCES "Employee" ("emp_num");

ALTER TABLE "Title" ADD FOREIGN KEY ("emp_num") REFERENCES "Employee" ("emp_num");
