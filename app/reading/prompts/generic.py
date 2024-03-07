generate_prompt = """
Instruction:
Based on the SAT questions and selected passage provided by the user, 
Generate an {category} SAT-style question and answer set following the criteria below.
Ensure each generated example adheres to these conditions.

1. make sure the question is relevant to the selected passage.
2. make sure the question is relevant to the SAT exam.

{example_question}

Selected Passage from {source_title}:
``` 
{selected_passage}
```

Ouput Format in json:
{format_instructions}

New Question:
"""