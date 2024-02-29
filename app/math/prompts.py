math_generate_prompt = """
    Your task is to generate one similar sat math question given format, catgory, question_type, and category-related example question.
    
    first major catgory: {major_one_category}
    second major category: {major_two_category}
    third major category: {major_three_category}
    question_type: {question_type}
    example question: {example_question}
    output format:{format_instructions}

    similar question:
"""

math_solve_prompt = """
    Following is SAT Math word question.

    EXAMPLE_QUESTION:
    "
    {example_question}
    "
    QUESTION_TYPE:
    "
    {question_type}
    "

    First, analyze the question to figure out useful information for solving the question.
    Second, using the reult of the first step, solve it step-by-step with explanation.
    If question_TYPE is MULTIPLE_CHOICE, with a solution you just derived, make 3 more similar but wrong answer choices.
    If question_TYPE is SHORT_ANSWER, leave answer choices empty.
    Finally, return the result as the following format.

    "
    {format_instructions}
    "
"""

sympy_translation_prompt = """
Translate a math question into a symbolic expression that can be solved using Python's sympy library. 
You must explicitly define symbols before using them. 

**Examples**

Question: Solve for x in the equation 2*x + 3 = 15.

Sympy Expression:
```text
# Define the variable
x = symbols('x')

# Define the expression
expression = Eq(2*x + 3, 15)

# Solve the expression
output = solve(expression)
```
```output
[6]
```
Answer: x = 6

Question: In the $xy$-plane, a line with equation $2y=c$ for some constant $c$ intersects a parabola at exactly one point. If the parabola has equation $y=-2x^2+9x$, what is the value of $c$?

Sympy Expression:
```text
# Define the variables
x, y, c = symbols('x y c')

# Define the equations
equation_parabola = Eq(y, -2*x**2 + 9*x)
equation_line = Eq(2*y, c)

# Equate the two equations to find the intersection point(s)
intersection = solve((equation_parabola, equation_line), (x, y))

# The discriminant of the quadratic equation is zero
discriminant = (9)**2 - 4*(-2)*(-y)
y_value = solve(Eq(discriminant, 0), y)[0]

# Substitute y into the line's equation to find c
c_value = solve(equation_line.subs(y, y_value), c)[0]
output = c_value
```
```output
[81/4]
```
Answer: c = 81/4

Question: Question: What is the value of 19*5**4?

Sympy Expression:
```text
# Define the variable 
x = symbols('x')

# Define the expression
expression = 19*x**4

# Substitute x = 5 into the expression
output = expression.subs(x, 5)
```
```output
[11875]
```
Answer: x = 11875

Question: 
$y=2x^2-21x+64 
$y=3x+a
In the given system of equations, $a$ is a constant. The graphs of the equations in the given system intersect at exactly one point, $(x, y)$, in the $xy$-plane. What is the value of $x$?

Sympy Expression:
```text
# define the variables
x, a = symbols('x a')

# Calculate the constants for the quadratic equation
b = -24
c = 64 - a

# The discriminant of the quadratic equation is zero
discriminant = b**2 - 4*2*c

# Find the value of a for which the discriminant is zero
a_value = solve(Eq(discriminant, 0), a)[0]

# Substitute a_value in the equation to find the quadratic equation and its roots
equation = Eq(2*x**2 + b*x + c.subs(a, a_value), 0)
x_values = solve(equation, x)
output = x_values
```
```output
[6]
```
Answer: x = 6

Question: What is the solution for the quadratic equation x^2 - 3x + 2 = 0?

Sympy Expression:
```text
# Define the variable 
x = symbols('x')

# Define the equation
expression = Eq(x**2 - 3*x + 2, 0)

# Solve the equation
output = solve(expression)
```
```output
[1, 2]
```
Answer: x = 1, 2

Question: Solve the system of equations y = 2x + 3 and y = 3x + 1.

Sympy Expression:
```text
# Define the variables
x, y = symbols('x y')

# Define the equations
eq1 = Eq(y, 2*x + 3)
eq2 = Eq(y, 3*x + 1)

# Solve the system of equations
output = solve((eq1,eq2), (x, y))
```
```output
{{x: 2, y: 7}}
```
Answer: x = 2, y = 7


Question: $\\frac{{55}}{{x+6}}=x$ What is the positive solution to the given equation?

Sympy Expression:
```text
# Define the variable
x = symbols('x')

# Define the equation
equation = Eq(55/(x + 6), x)

# Solve the equation
output = solve(equation, x)
```
```output
[-11, 5]
```
Answer: x = -11, x = 5.


Question: {question}

{format_instructions}
"""


sympy_solved_question_prompt = """
Given question, python sympy code that solves the question, and the result of the code,
Finalize the exact answer that directly answer the question with explanation.

Question: 
```
{question}
```
Sympy Expression:
```
{sympy_expression}
```


Excute Result:
```
{output}
```

"
{format_instructions}
"

Answer with explanation:
"""
