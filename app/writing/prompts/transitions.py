generate_prompt = """
Please generate one SAT-style question that test the understanding of transition words or phrases in sentences. The question should cover one of three formats:

- Format A: {{Transition}}, {{_____________}}. (most common)
- Format B: {{______}}, {{Transition}}, {{________}}. (less common)
- Format C: {{_________________}}, {{Transition}}. (rare, but possible)

The correct answer and the distractors should be clearly distinct in their meaning and usage. No two options should convey the same idea, as this could potentially lead to multiple correct answers.

The question should include clear textual clues both before and after the blank space(s) to help in determining the correct transition word or phrase.

The question should focus on three types of transitions:

1. Continue (add information, give examples, define, emphasize, or compare)
2. Contradict (contrast)
3. Cause & Effect (chronological sequence)

The question should provide four answer options, one of which is correct, and cover a variety of topics and contexts similar to the actual SAT exam. Finally, provide the correct answer and a brief explanation of why this answer is correct based on the context and the role of transition words or phrases.

{example_question}
"


Ouput Format:
{format_instructions}

New Question:
"""
