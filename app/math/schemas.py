from pydantic import BaseModel, conint, Field
from enum import Enum
from typing import Optional, List
from app.core.schema import QuestionType


class Category(str, Enum):
    ALGEBRA = "Algebra"
    GEOMETRY = "Geometry"
    CALCULUS = "Calculus"
    QUADRATIC_EQUATION = "Quadratic Equation"


class MajorCategory(str, Enum):
    LINEAR_EQUATIONS = "Linear Equations"
    LINEAR_FUNCTION = "Linear Function"
    SYSTEM_OF_EQUATIONS = "System of Equations"
    ABSOLUTE_VALUE = "Absolute Value"
    SOLVING_INEQUALITIES = "Solving Inequalities"
    GRAPHING_INEQUALITIES = "Graphing Inequalities"
    EXPONENTIAL_EQUATIONS = "Exponential Equations"
    EXPONENTIAL_FUNCTION = "Exponential Function"
    RADICAL_EQUATION_AND_FUNCTION = "Radical Equation and Function"
    COMPLEX_NUMBERS = "Complex Numbers"
    QUADRATIC_EQUATION = "Quadratic Equation"
    QUADRATIC_FUNCTION = "Quadratic Function"
    POLYNOMIAL_EQUATION = "Polynomial Equation"
    POLYNOMIAL_FUNCTION = "Polynomial Function"
    RATIONAL_EQUATION = "Rational Equation"
    RATIONAL_FUNCTION = "Rational Function"
    FUNCTIONS = "Functions"
    TRANSFORMATION = "Transformation"
    RATIO_RATE_PROPORTION = "Ratio, Rate, and Proportion"
    PERCENTAGE = "Percentage"
    PROBABILITY = "Probability"
    STATISTICS = "Statistics"
    ANGLES_TRIANGLES_POLYGONS = "Angles, Triangles, and Polygons"
    CIRCLE = "Circle"
    CONGRUENCE_SIMILARITY_TRIANGLES = "Congruence and Similarity of Triangles"
    POLYGON_CIRCLE_EQUATION = "Polygon in Plane / Circle Equation"
    VOLUME_SURFACE_AREA = "Volume (feat. Surface Area)"
    TRIGONOMETRIC_RATIO = "Trigonometric Ratio"


class LinearEquationsSubCategory(str, Enum):
    ONE_VARIABLE = "One Variable"
    WRITING_EQUATION = "Writing the Linear Equation"
    INTERPRETING_EQUATION = "Interpreting the Linear Equation"
    THREE_TYPES_SOLUTION = "Three Types of Solution"
    FUNCTION_NOTATION = "Function Notation"
    SOLVING_FOR_Y = "Solving for y"


class LinearFunctionSubCategory(str, Enum):
    SLOPE = "Slope"
    INTERCEPTS = "Intercepts"
    LINEAR_FUNCTION = "Linear Function"
    PARALLEL_PERPENDICULAR_LINES = "Parallel and Perpendicular Lines"
    LINES_AND_EQUATIONS = "Lines and Equations"
    LINEAR_EQUATION_WITH_GRAPH_CHART = "Linear Equation with Graph and Chart"
    INTERPRETING_LINEAR_EQUATIONS = "Interpreting Linear Equations"


class SystemOfEquationsSubCategory(str, Enum):
    STANDARD_FORM = "Standard Form"
    SLOPE_INTERCEPT_FORM = "Slope-Intercept Form"
    GRAPH = "Graph"
    SOLVING_THE_SYSTEM = "Solving the System of Linear Equations"


class AbsoluteValueSubCategory(str, Enum):
    DEFINITION = "Definition of Absolute Value"
    SOLVING_ABSOLUTE_VALUE_EQUATION = "Solving the Absolute Value Equation"
    ABSOLUTE_VALUE_FUNCTION = "Absolute Value Function"


class SolvingInequalitiesSubCategory(str, Enum):
    LINEAR_INEQUALITIES = "Linear Inequalities"
    COMPOUND_INEQUALITIES = "Compound Inequalities"
    ABSOLUTE_VALUE_INEQUALITIES = "Absolute Value Inequalities"
    WRITING_INEQUALITIES = "Writing Inequalities"


class GraphingInequalitiesSubCategory(str, Enum):
    LINEAR_INEQUALITIES = "Linear Inequalities"


class ExponentialEquationsSubCategory(str, Enum):
    EXPONENTIAL_PROPERTIES = "Exponential Properties"
    SOLVING_EXPONENTIAL_EQUATIONS = "Solving Exponential Equations"
    EXPONENTIAL_RELATIONSHIPS = "Exponential Relationships"


class ExponentialFunctionSubCategory(str, Enum):
    EXPONENTIAL_FUNCTION = "Exponential Function"
    INCREASING_DECREASING_RELATIONSHIP = "Increasing or Decreasing Relationship"


class RadicalEquationFunctionSubCategory(str, Enum):
    RADICAL_EXPRESSION = "Radical Expression"
    RADICAL_EQUATION = "Radical Equation"
    RADICAL_FUNCTION = "Radical Function"


class ComplexNumbersSubCategory(str, Enum):
    IMAGINARY_NUMBER = "Imaginary Number i"
    COMPLEX_CONJUGATE = "Complex Conjugate"


class QuadraticEquationSubCategory(str, Enum):
    FOIL_PRODUCT_MULTIPLYING = "FOIL and Product = Multiplying"
    FACTORING_DIVIDING = "Factoring = Dividing"
    ZERO_PRODUCT_RULES = "Zero Product Rules"
    FINDING_SOLUTIONS_OF_QUADRATIC = "Finding Solutions of Quadratic"
    DISCRIMINANT = "Discriminant"
    RELATION_BETWEEN_COEFFICIENT_SOLUTIONS = (
        "Relation between Coefficient and Solutions"
    )
    SYSTEM_OF_EQUATIONS_QUADRATIC_LINEAR = (
        "System of Equations with Quadratic and Linear"
    )


class QuadraticFunctionSubCategory(str, Enum):
    PARABOLA = "Parabola"
    THREE_FORMS_OF_QUADRATIC_FUNCTIONS = "Three Forms of Quadratic Functions"
    WORD_PROBLEMS_OF_QUADRATIC = "Word Problems of Quadratic"


class PolynomialEquationSubCategory(str, Enum):
    POLYNOMIAL = "Polynomial"
    DIVIDING_POLYNOMIALS = "Dividing Polynomials"
    REMAINDER_THEOREM = "Remainder Theorem"


class PolynomialFunctionSubCategory(str, Enum):
    GRAPH_OF_POLYNOMIAL_FUNCTION = "Graph of Polynomial Function"


class RationalEquationSubCategory(str, Enum):
    SIMPLIFYING_FRACTIONS = "Simplifying the Fractions"
    SOLVE_FOR_VARIABLE = "Solve for the Variable (in terms of)"
    UNDEFINED_VALUE_EXTRANEOUS_SOLUTIONS = "Undefined Value and Extraneous Solutions"


class RationalFunctionSubCategory(str, Enum):
    RATIONAL_FUNCTION = "Rational Function"


class FunctionsSubCategory(str, Enum):
    COMPOSITE_FUNCTION = "Composite Function"
    INTERPRETING_NON_LINEAR = "Interpreting Non-Linear"
    ALL_FUNCTION_GRAPHS_FOR_SAT = "All Function Graphs for SAT"


class TransformationSubCategory(str, Enum):
    TRANSLATION = "Translation"
    REFLECTION = "Reflection"


class RatioRateProportionSubCategory(str, Enum):
    RATIO_RATE = "Ratio and Rate"
    PROPORTION = "Proportion"
    UNIT_CONVERSION = "Unit Conversion"


class PercentageSubCategory(str, Enum):
    PERCENT = "Percent"
    PERCENT_INCREASING_DECREASING = "Percent Increasing and Decreasing"
    WORD_QUESTIONS = "Word Questions"


class ProbabilitySubCategory(str, Enum):
    COUNTING = "Counting"
    PROBABILITY = "Probability"
    CONDITIONAL_PROBABILITY = "Conditional Probability"


class StatisticsSubCategory(str, Enum):
    DATA_REPRESENTATIONS = "Data Representations"
    MEAN_MEDIAN_MODE_OUTLIER = "Mean, Median, and Mode / Outlier"
    RANGE_STANDARD_DEVIATION = "Range and Standard Deviation"
    BOX_WHISKER_PLOTS = "Box and Whisker Plots"
    SCATTER_PLOTS_LINE_OF_BEST_FIT = "Scatter Plots and Line of Best Fit"
    DATA_INFERENCE = "Data Inference"


class AnglesTrianglesPolygonsSubCategory(str, Enum):
    LINES_AND_ANGLES = "Lines and Angles"
    TRIANGLES_AND_POLYGONS = "Triangles and Polygons"
    RIGHT_TRIANGLE = "Right Triangle"
    QUADRILATERAL = "Quadrilateral"


class CircleSubCategory(str, Enum):
    TANGENT_CHORD_INSCRIBED_ANGLES = "Tangent, Chord, Inscribed Angles"
    CIRCLE_SECTOR_PERIMETER_AREA = "Circle, Sector --> Perimeter and Area"


class CongruenceSimilarityTrianglesSubCategory(str, Enum):
    CONGRUENCE_OF_TRIANGLES = "Congruence of Triangles"
    SIMILARITY_OF_TRIANGLES = "Similarity of Triangles"


class PolygonCircleEquationSubCategory(str, Enum):
    POLYGON_IN_PLANE_AND_MIXED = "Polygon in Plane and Mixed"
    CIRCLE_EQUATIONS = "Circle Equations"


class VolumeSurfaceAreaSubCategory(str, Enum):
    PRISMS = "Prisms"
    CYLINDERS_SPHERES = "Cylinders and Spheres"
    PYRAMIDS_CONES = "Pyramids and Cones"


class TrigonometricRatioSubCategory(str, Enum):
    TRIGONOMETRIC_RATIOS = "Trigonometric Ratios"
    DEGREE_AND_RADIAN = "Degree and Radian"
    UNIT_CIRCLE_TRIGONOMETRY = "Unit Circle and Trigonometry"


subcategory_data = {
    MajorCategory.LINEAR_EQUATIONS: list(LinearEquationsSubCategory),
    MajorCategory.LINEAR_FUNCTION: list(LinearFunctionSubCategory),
    MajorCategory.SYSTEM_OF_EQUATIONS: list(SystemOfEquationsSubCategory),
    MajorCategory.ABSOLUTE_VALUE: list(AbsoluteValueSubCategory),
    MajorCategory.SOLVING_INEQUALITIES: list(SolvingInequalitiesSubCategory),
    MajorCategory.GRAPHING_INEQUALITIES: list(GraphingInequalitiesSubCategory),
    MajorCategory.EXPONENTIAL_EQUATIONS: list(ExponentialEquationsSubCategory),
    MajorCategory.EXPONENTIAL_FUNCTION: list(ExponentialFunctionSubCategory),
    MajorCategory.RADICAL_EQUATION_AND_FUNCTION: list(
        RadicalEquationFunctionSubCategory
    ),
    MajorCategory.COMPLEX_NUMBERS: list(ComplexNumbersSubCategory),
    MajorCategory.QUADRATIC_EQUATION: list(QuadraticEquationSubCategory),
    MajorCategory.QUADRATIC_FUNCTION: list(QuadraticFunctionSubCategory),
    MajorCategory.POLYNOMIAL_EQUATION: list(PolynomialEquationSubCategory),
    MajorCategory.POLYNOMIAL_FUNCTION: list(PolynomialFunctionSubCategory),
    MajorCategory.RATIONAL_EQUATION: list(RationalEquationSubCategory),
    MajorCategory.RATIONAL_FUNCTION: list(RationalFunctionSubCategory),
    MajorCategory.FUNCTIONS: list(FunctionsSubCategory),
    MajorCategory.TRANSFORMATION: list(TransformationSubCategory),
    MajorCategory.RATIO_RATE_PROPORTION: list(RatioRateProportionSubCategory),
    MajorCategory.PERCENTAGE: list(PercentageSubCategory),
    MajorCategory.PROBABILITY: list(ProbabilitySubCategory),
    MajorCategory.STATISTICS: list(StatisticsSubCategory),
    MajorCategory.ANGLES_TRIANGLES_POLYGONS: list(AnglesTrianglesPolygonsSubCategory),
    MajorCategory.CIRCLE: list(CircleSubCategory),
    MajorCategory.CONGRUENCE_SIMILARITY_TRIANGLES: list(
        CongruenceSimilarityTrianglesSubCategory
    ),
    MajorCategory.POLYGON_CIRCLE_EQUATION: list(PolygonCircleEquationSubCategory),
    MajorCategory.VOLUME_SURFACE_AREA: list(VolumeSurfaceAreaSubCategory),
    MajorCategory.TRIGONOMETRIC_RATIO: list(TrigonometricRatioSubCategory),
}


class GenerateSimilarQuestionRequest(BaseModel):
    category_ids: List[str] = Field(..., max_items=3)
    question_type: QuestionType
    question_count: conint(ge=1, le=5) = Field(example=1)


class GenerateProblemSetRequest(BaseModel):
    category_ids: List[str] = Field(..., max_items=3)
    question_count: conint(ge=1, le=5) = Field(example=1)


class GeneratedQuestion(BaseModel):
    id: int
    question: str
    explanation: str


class SolutionWithChoices(BaseModel):
    choice_a: Optional[str]
    choice_b: Optional[str]
    choice_c: Optional[str]
    choice_d: Optional[str]
    answer: Optional[str]
    solution: Optional[str]


class CompleteGeneratedQuestion(BaseModel):
    question: str
    explanation: Optional[str]
    choice_a: Optional[str]
    choice_b: Optional[str]
    choice_c: Optional[str]
    choice_d: Optional[str]
    answer: Optional[str]


class CompleteProblemSet(BaseModel):
    id: int
    name: str = Field(default="New Problem Set")
    is_full_test: bool


class SolveQuestionSympyRequest(BaseModel):
    question: str


class SympyTranslation(BaseModel):
    question: str
    sympy_expression: str


class SympySolvedQuestion(BaseModel):
    sympy_expression: str
    correct_answer: str
    explanation: str
