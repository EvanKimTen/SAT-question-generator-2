generate_prompt = """
Instruction:
Generate {category} SAT-style reading comprehension passage, question, and answer set that meets the following criteria:

Selected Passage from {source_title}: 
{selected_passage}

1. Source of the passage excerpt: use only the provided selected_passage.

2. Length: Each passage excerpt should contain a minimum of 50 words.

3. Formatting: Adjust the introductory instruction to suit the type of literature the passage is sourced from:

   - Poem: "The following text is from (Author)'s (year) poem "Poem Title." Add an essential background sentence about the poem if required for comprehension, but not as an answer choice.
   
   - Short Story: "The following text is from (Author)'s (year) short story "Short Story Title." Include a relevant background sentence if necessary.
   
   - Play: "The following text is from (Author)'s (year) play $\\textit{{Play Title}}$. Insert a crucial background sentence about the play if needed.
   
   - Novel: "The following text is from (Author)'s (year) novel $\\textit{{Novel Title}}$. Provide an essential background sentence about the novel if required.

4. Symbols: Replace any em dash found in the passage with “$\\text{{\\textemdash}}$”.

5. Titles & Names: Enclose any mentioned scientific names or titles (books, novels, plays, films, artworks, periodicals, databases, websites) in $\textit{{}}$ in the passage, question, or answer choices.

6. Quotation Marks: Apply double quotation marks to titles (articles, essays, chapters, poems, short stories, web pages, songs, speeches) mentioned in the passage, question, or answer choices.

7. Question: The posed question should be: “Which choice best states the main purpose of the text?”

8. Answer Choices: Supply four answer choices, formatted like the example passages. Only one answer should correctly describe the purpose of the passage.

9. Answer Choices Content: Among the answer choices, two should be clearly incorrect (and such incorrect answer choices typically introduce information not directly addressed in the passage), one should be plausible but not supported by the text (and such incorrect answer choice typically shifts or blurs the purpose of a text by emphasizing details that aren't a central focus), and one should be the correct answer that accurately states the overall purpose of the passage excerpt. 

10. Correct Answer and Explanation: State the correct answer by its corresponding letter (e.g., "Correct Answer: A") and explain why it is correct. Also, provide reasons why the other three answers are incorrect. For the explanation, make sure to provide a detailed explanation for the correct answer explaining why it correctly captures the overall purpose of the text and provide a succinct explanation for the wrong answers, clearly pointing out the wrong aspects.

11. The letter of the correct answer should be randomly assigned from A to D. Not all passages generated should have identical letters as the correct answer.

12. Prompt Order: Each set should be structured as follows: passage number, passage instruction (if available), passage, question, answer choices, correct answer, and explanation.

13. Clarity: Ensure that prompts and answers are clear and easily understandable.

14. Originality: Do not reuse passages. Choose literary works unfamiliar to American readers.

{example_question}


Ouput Format:
{format_instructions}

Include the generated text and question in problem_str.
There are only two problem types: 'Multiple Choice', 'Short Answer'
You must not include double quote(") within the value json output.

"""
