generate_prompt = """
Subject-Verb agreement is about the number agreement between the subject and the conjugated verb form.

Example Questions: 
```
The classic children’s board game Chutes and Ladders is a version of an ancient Nepalese game, Paramapada Sopanapata. 
In both games, players encounter “good” or “bad” spaces while traveling along a path; landing on one of the good spaces ______ a player to skip ahead and arrive closer to the end goal.

Subject: Landing on one of the good spaces (Singular)
Verb: allows (Singular)

Answer Choices Format: 
3 plural vs. 1 singular

Answer Choices:
A) allows - singular 
B) are allowing - plural
C) have allowed - plural
D) allow - plural

Correct Answer:
A) allows 

When writing $\textit{{The Other Black Girl}}$ (2021), novelist Zakiya Dalila Harris drew on her own experiences working at a publishing office. 
The award-winning book is Harris’s first novel, but her writing ______ honored before. 
At the age of twelve, she entered a contest to have a story published in $\textit{{American Girl}}$ magazine$\text{{---}}$and won.

Subject: Her writing (singular)
Verb: has been (singular)

Answer Choices Format: 
3 plural vs. 1 singular

Answer Choices:
A) were - plural
B) have been - plural
C) has been - singular
D) are - plural

Correct Answer:
C) has been

Professional American football player Fred Cox invented one of the world’s most popular toys. In the 1970s, 
he came up with the idea for the Nerf football, which ______ of the harder and heavier regulation football.

Answer Choices Format: 
3 plural vs. 1 singular

Answer Choices:
A) were a smaller, foam version - plural
B) are smaller, foam versions - plural 
C) were smaller, foam versions - plural
D) is a smaller, foam version - singular

Correct Answer:
D) is a smaller, foam version

Subject: the idea for the Nerf football (singular)
Verb: is a smaller, foam versions (signular)


{example_question}
```

Output Conditions:
* singular answer choice form MUST END in "s"
* plural answer choice form NO "s" at the end
* for each answer choice, write "singular" for singular and "plural" for plural
* Only one "______" is allowed.

Output Format:
```
Question: {{newly generated passage}}

Subject: {{subject in question}}

Verb: {{verb follows the subject}}

Answer Choices Format: 
{{3 singluar vs 1 plural answer choices | 3 plural vs. 1 singular answer choices}}

Answer Choices: {{four answer choices (3 singluar vs 1 plural answer choices | 3 plural vs. 1 singular answer choice)}}

Correct Answer: {{correct answer}}
```

The answer choices, regardless of tense, must have 3 singular and 1 plural form
or 3 plural and 1 singular form.


Ouput Format:
{format_instructions}


New Question (follow the output format above):
"""
