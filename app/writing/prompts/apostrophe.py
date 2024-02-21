generate_prompt = """
Generate one SAT-style question that require an understanding of the use of apostrophes. 


For instance:
\"
Passage:
\"Literary agents estimate that more than half of all nonfiction books credited to a celebrity or other public figure are in fact written by ghostwriters, professional authors who are paid to write other ______ but whose names never appear on book covers.\"

Question: 
Fill in the blank with the correct phrase:

A) people's stories
B) peoples story's
C) peoples stories
D) people's story's

Correct Answer: 
A) people's stories

Explanation:
The correct form is \"people's stories\" because the stories belong to other people. The word \"people\" is the plural of \"person\", so \"peoples\" is incorrect. The apostrophe in \"people's\" indicates possession, which is needed here because the stories belong to other people.

Passage:
\"Cheng Dang and her colleagues at the University of Washington recently ran simulations to determine the extent to which individual snow ______ affects the amount of light reflecting off a snowy surface.\"

Question: 
Fill in the blank with the correct phrase:

A) grain's physical properties'
B) grains' physical properties
C) grains' physical property's
D) grains physical properties

Correct Answer: 
B) grains' physical properties

Explanation:
The correct form is \"grains' physical properties\" because we are talking about the properties of separate snow grains, which is indicated by the term \"individual\" in the passage. The apostrophe in \"grains'\" indicates possession, showing that the properties belong to the grains. There's no need for an apostrophe after \"properties\".

Passage:
\"In his groundbreaking book $\textit{{Bengali Harlem and the Lost Histories of South Asian America}}$, Vivek Bald uses newspaper articles, census records, ships' logs, and memoirs to tell the ______ who made New York City their home in the early twentieth century.\"

Question: 
Fill in the blank with the correct phrase:

A) story's of the South Asian immigrants
B) story's of the South Asian immigrants'
C) stories of the South Asian immigrants
D) stories' of the South Asian immigrant's

Correct Answer: 
C) stories of the South Asian immigrants

Explanation:
The correct form is \"stories of the South Asian immigrants\". The word \"of\" indicates possession here, so no apostrophe is needed. We're talking about multiple stories of multiple immigrants, so \"stories\" and \"immigrants\" should both be plural. 


Passage:
\"In Death Valley National Park's Racetrack Playa, a flat, dry lakebed, are 162 rocks$\text{{\textemdash}}$some weighing less than a pound but others almost 700 pounds$\text{{\textemdash}}$that move periodically from place to place, seemingly of their own volition. Racetrack-like trails in the ______ mysterious migration.\"

Question: 
Fill in the blank with the correct phrase:

A) playas sediment mark the rock's
B) playa's sediment mark the rocks
C) playa's sediment mark the rocks'
D) playas' sediment mark the rocks'

Correct Answer: 
C) playa's sediment mark the rocks'

Explanation: 
The correct form is \"playa's sediment mark the rocks'\". There are two separate possessions in this sentence: the sediment of the playa, and the migration of the rocks. The word \"playa's\" indicates the sediment belongs to the playa, and the word \"rocks'\" indicates the migration belongs to the rocks.

{example_question}
\"


Use the following guidelines:

- Each question must have four answer choices.
- The answer choices should be phrases composed of at least two words.
- At least one of the answer choices should not contain an apostrophe.
- For the rest of the choices, the apostrophes should appear either at the end of the first or the last word, or both.
- The first and last words of the answer choices should include both the singular and plural forms of the same noun.
- For phrases with two consecutive words that both could have an apostrophe (like \"people's stories\"), the correct answer will only have an apostrophe on the first word, never the second.


The aim of these questions is to test the student's ability to understand the number and possession of nouns based on the context of the passage. They need to decide if the passage is discussing a single or multiple number of a certain noun, and whether something belongs to something else.

Bear in mind that the word \"of\" also indicates possession and in that case, no apostrophe is needed. Also, if the passage is not discussing possession, none of the words should have an apostrophe.

Ouput Format:
{format_instructions}

New Question:
"""