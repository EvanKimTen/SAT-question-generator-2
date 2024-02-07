generate_prompt = """
Generate a SAT-style Accomplishing a Goal question, by using the following steps:

1. Clearly define the goal in the question. For example, "The student wants to ...".

2. Consider the components of the goal when formulating the question. This could be emphasizing a difference or similarity between two things, making or supporting a generalization about a type or kind, providing an example of something, comparing or contrasting two things, specifying a reason or explaining an advantage, disadvantage or process.

3. When creating answer choices, ensure all information is derived from bullet points of the given passage. Be aware that among the four answer choices, two should be evidently incorrect, one should seem correct but is actually wrong, and only one should be the correct answer.

4. The correct answer must address all components of the goal. Any answer that only partially meets the criteria should be deemed incorrect.

5. In the question and answer choices, replace any scientific names, titles, etc., with suitable placeholders.

6. For clarity, the question should be followed by the answer choices, the correct answer, and a clear explanation as to why it is correct. All prompts should be clear, and answers should be provided with clarity.

7. Remember that the main objective of the goal question is to test the ability to use information from the bullet points to accomplish a certain goal, as defined in the question.

Remember, the main goal is to formulate a question that will test a student's ability to use information from a passage to accomplish a specific goal. This includes understanding the goal, identifying the components of the goal, and selecting the answer choice that fully accomplishes the goal.

For instance:

"
While researching a topic, a student has taken the following notes:
$\\ \bullet$Bharati Mukherjee was an Indian-born author of novels and short stories.
$\\ \bullet$She published the novel $Textit{{The Holder of the World}}$ in 1993.
$\\ \bullet$A central character in the novel is a woman living in twentieth-century United
States.
$\\ \bullet$Another central character is a woman living in seventeenth-century India.

The student wants to introduce the novel $Textit{{The Holder of the World}}$ to an audience already familiar with Bharati Mukherjee. Which choice most effectively uses relevant information from the notes to accomplish this goal?

A) Bharati Mukherjee’s settings include both twentieth-century United States and seventeenth-century India.
B) In addition to her novel $Textit{{The Holder of the World}}$, which was published in 1993, Indian-born author Bharati Mukherjee wrote other novels and short stories.
C) Bharati Mukherjee’s novel $Textit{{The Holder of the World}}$ centers around two women, one living in twentieth-century United States and the other in seventeenth-century India.
D) $Textit{{The Holder of the World}}$ was not the only novel written by Indian-born author Bharati Mukherjee.

{example_question}
"

Order your new question as: passage, question, answer choices, correct answer, and explanation. Make sure the prompts and answers are clear and straightforward. Don't reuse passages already employed for this type of question.

Ouput Format:
{format_instructions}

New Question:
"""
