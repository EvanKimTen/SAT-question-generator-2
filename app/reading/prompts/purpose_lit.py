generate_prompt = """
Instruction:
Generate {category} SAT-style reading comprehension passage, question, and answer set that meets the following criteria:

Selected Passage from {source_title}: 
{selected_passage} 

Conditions:
1. Source of the passage excerpt: use only the provided selected_passage.

2. Length: Each passage excerpt should be at least 50 words long.

3. Formatting: Depending on the source of the passage, follow these formats:

   - Poem: "The following text is from (Author)'s (year) poem "Poem Name." Include a background sentence if necessary to understand the passage, but ensure it's not an answer choice.
   
   - Short Story: "The following text is from (Author)'s (year) short story "Short Story Name." Include a background sentence if necessary.
   
   - Play: "The following text is from (Author)'s (year) play $\\textit{{Play Name}}$. Include a background sentence if necessary.
   
   - Novel: "The following text is from (Author)'s (year) novel $\\textit{{Novel Name}}$. Include a background sentence if necessary.

4. Symbols: Replace any em dash in the passage with “$\\text{{\\textemdash}}$”.

5. Names and Titles: If a passage, question, or answer choices mention a scientific name or title of a book, novel, play, film, artwork, periodical, database, or website, enclose that name or title in $\\textit{{}}$.

6. Quotation Marks: Use double quotation marks around the titles of articles, essays, chapters, poems, short stories, web pages, songs, or speeches mentioned in the passage, question, or answer choices.

7. Question: Each question should be: “Which choice best states the main purpose of the text?”

8. Answer Choices: Supply four answer choices, formatted like the example passages. Only one answer should correctly describe the purpose of the passage.

9. Answer Choices Content: Among the answer choices, two should be clearly incorrect (and such incorrect answer choices typically introduce information not directly addressed in the passage), one should be plausible but not supported by the text (and such incorrect answer choice typically shifts or blurs the purpose of a text by emphasizing details that aren't a central focus), and one should be the correct answer that accurately states the overall purpose of the passage excerpt. 

10. Correct Answer and Explanation: State the correct answer by its corresponding letter (e.g., "Correct Answer: A") and explain why it is correct. Also, provide reasons why the other three answers are incorrect. For the explanation, make sure to provide a detailed explanation for the correct answer explaining why it correctly captures the overall purpose of the text and provide a succinct explanation for the wrong answers, clearly pointing out the wrong aspects.

11. The letter of the correct answer should be randomly assigned from A to D. Not all passages generated should have identical letters as the correct answer.

12. Prompt Order: Follow this order for each set: passage number, passage instruction (if any), passage, question, answer choices, correct answer (letter only), and explanation.

13. Clarity: Ensure clarity in all prompts and answers.

14. Originality: Avoid reusing the same passages. Use literary works unfamiliar to American readers.

{example_question}


Ouput Format:
{format_instructions}

Include the generated text and question in problem_str.
There are only two problem types: 'Multiple Choice', 'Short Answer'
You must not include double quote(") within the value json output.

New Question:

"""
