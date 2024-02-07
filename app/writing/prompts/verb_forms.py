generate_prompt = """
Please generate a SAT-style question involving the use of different verb forms including base, infinitive, present participle, past tense, past participle, and gerund. 
Each question should provide four possible answers, one of which is correct. 
The questions should range from easy to hard difficulty and include a detailed explanation for the correct answer. 
Please be sure to cover a wide range of topics and contexts, just like on the actual SAT exam.

In your questions, make sure to include examples that require the understanding of:

The main verb that needs to be conjugated in accordance with the subject and tense (Finite Verb).
Non-finite verbs such as infinitives, gerunds, or participles that don't change according to the subject.
The use of verbs to indicate purpose, the act of doing something, or as part of a verb group.
The questions should also include one infinitive form and one -ing form in the four answer choices. Provide a mix of action, happening, and state of being verb examples. 
For additional complexity, make sure some sentences require students to correctly identify the verb form from a sentence where the subject and main verb are placed far apart from each other.

For instance:
```

Hard	
"In 1966, Emmett Ashford became the first African American to umpire a Major League Baseball game. 
His energetic gestures announcing when a player had struck out and his habit of barreling after a hit ball 
to see if it would land out of ______ transform the traditionally solemn umpire role into a dynamic one."							

"difficult because
the subject (in orange)
and the main verb 
""helped"" placed far apart 
from each other"		


A). bounds helped						
B). bounds, helping						
C). bounds that helped						
D). bounds to help						
								

Correct Answer: A) bounds helped 
			
Easy	
"A member of the Cherokee Nation, Mary Golda Ross is renowned for her contributions to 
NASA’s Planetary Flight Handbook, which ______ detailed mathematical guidance for missions to Mars and Venus."		


A). provided		need a finite verb to properly form the "which" clause				
B). having provided						
C). to provide						
D). providing						
						

Correct Answer: A) provided		


Easy	

"In winter, the diets of Japanese macaques, also known as snow monkeys, are influenced more by food availability than by 
food preference. Although the monkeys prefer to eat vegetation and land-dwelling invertebrates, those food sources may 
become unavailable because of extensive snow and ice cover, ______ the monkeys to hunt for marine animals in any 
streams that have not frozen over."			

A). forces						
B). to force						
C). forcing		a present participle phrase = additional detail				
D). forced						
						
Correct Answer: C) forcing 					
								
easy	
"In the historical novel $\textit{{The Surrender Tree}}$, Cuban American author Margarita Engle uses poetry 
rather than prose ______ the true story of Cuban folk hero Rosa La Bayamesa."	

A). tells						
B). told						
C). is telling						
D). to tell		purpose of using poetry over prose is to to tell the true story				


Correct Answer: D) to tell 	

easy	

"For thousands of years, people in the Americas ______ the bottle gourd, a large bitter fruit with a thick rind, to make bottles, 
other types of containers, and even musical instruments. Oddly, there is no evidence that any type of bottle gourd is native 
to the Western Hemisphere; either the fruit or its seeds must have somehow been carried from Asia or Africa."

A). to use						
B). have used		need a conjugated main verb to form a proper sentence				
C). having used						
D). using						


Correct Answer: B) have used  	


easy	
"To survive when water is scarce, embryos inside African turquoise killifish eggs ______ a dormant state known as diapause.
In this state, embryonic development is paused for as long as two years—longer than the life span of an adult killifish."	

A). enter		need a conjugated main verb to form a proper sentence				
B). to enter						
C). having entered						
D). entering						
								

Correct Answer: A) enter


Hard	

"A model created by biologist Luis Valente predicts that the rate of speciation—the rate at which new species form—on an 
isolated island located approximately 5,000 kilometers from the nearest mainland ______ triple the rate of speciation 
on an island only 500 kilometers from the mainland."							

"a single word 
determines 
the correct answer"		

A). being						
B). to be		"if the sentence said ""Luis Valente predicts the rate of specifiation"",then B would be right because we don't need another main verb"				
C). to have been						
D). will be		"BUT the word ""that"" indicates a start of another complete thought and therefore we need a proper finite verb form"				

Correct Answer: D) will be  						
								
Easy	

"In 1637, the price of tulips skyrocketed in Amsterdam, with single bulbs of rare varieties selling for up to the equivalent of 
$200,000 in today’s US dollars. Some historians ______ that this “tulip mania” was the first historical instance of an asset
bubble, which occurs when investors drive prices to highs not supported by actual demand."

A). claiming						
B). claim		need a conjugated main verb to form a proper sentence				
C). having claimed						
D). to claim						
								
Correct Answer: B) claim 	


Easy	

"Even though bats prefer very sweet nectar, the plants that attract them have evolved to produce nectar that is only 
moderately sweet. A recent study ______ why: making sugar is energy-intensive, and it is more advantageous for 
plants to make a large amount of low- sugar nectar than a small amount of high-sugar nectar."	

A). explains		need a conjugated main verb to form a proper sentence				
B). explaining						
C). having explained						
D). to explain						


Correct Answer: A) explains


Hard	

"Working from an earlier discovery of Charpentier’s, chemists Emmanuelle Charpentier and Jennifer Doudna—winners of 
the 2020 Nobel Prize in Chemistry—re-created and then reprogrammed the so-called “genetic scissors” of a species of 
DNA-cleaving bacteria ______ a tool that is revolutionizing the field of gene technology."						

Note:
"having more words make it difficult to understand the main  message of the sentence which impacts one's
ability to see if the sentence already has a main verb or not"		

A) to forge		"purpose of recreating and reprogramming the ""genetic scissors"" is to forge a revolutionizing tool"			
B) forging					
C) forged					
D) and forging					

Correct Answer: A) to forge

{example_question}
```


Finally, for each question, provide the correct answer and a brief explanation of why this answer is correct based on the verb form rules.

Ouput Format:
{format_instructions}

New Question: 
"""
