generate_prompt = """
Please generate a series of SAT-style questions that test the concept of parallel structure in sentences. These questions should require the understanding of consistent verb, adjective, or noun forms in a list of two or more items in a sentence.

In each question, provide four possible answers, one of which is correct. The difficulty of the questions should range from easy to hard, and they should cover a variety of topics and contexts similar to the actual SAT exam. Make sure to provide an answer choice with "-ed" form verb to test students' understanding of this specific rule.

The questions should follow the existing format in the passage. Each question should contain a list of two items, and the correct answer should maintain the same verb form as the first item in the list. For instance, if the first item uses a base form of a verb, the second item should also be in the base form.


For instance:
```
"In order to prevent non-native fish species from moving freely between the Mediterranean and Red Seas, marine biologist Bella Galil has proposed that a saline lock system be installed along the Suez Canal in Egypt’s Great Bitter Lakes. The lock would increase the salinity of the lakes and ______ a natural barrier of water most marine creatures would be unable to cross."

A). creates
B). create
C). creating
D). created

The correct answer is B) create, because the verb should maintain the same base form as the first item "increase" in the list.


"The International Space Station is equipped with a variety of systems that enable astronauts to satisfy their daily needs while in orbit. These systems include a water reclamation system, a waste disposal system, and ______."

A). a food storage device
B). a food storing device
C). storing food
D). stored food

The correct answer is A) a food storage device, because the verb form "storing" should maintain the same form as the verb "reclamation" and "disposal" in the list.


"The new exercise program for the office staff consists of running in the morning, stretching in the afternoon, and ______."

A). lifting weights
B). lift weights
C). lifting weight
D). lifted weights

The correct answer is A) lifting weights, because the verb should maintain the same form as the first item in the list, which is "running".


"The new strategy for the company includes increasing productivity, cutting costs, and ______."

A). hire new staff
B). hiring new staff
C). hires new staff
D). hire new staffs

The correct answer is B) hiring new staff, because the verb should maintain the same form as the first item in the list, which is "increasing".

{example_question}
```

Finally, for each question, provide the correct answer and a brief explanation of why this answer is correct based on the rules of parallel structure.

Ouput Format:
{format_instructions}


New Question:
"""
