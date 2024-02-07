generate_prompt = """
Please generate an SAT-style verb-tense type question. The question should include a short passage context, with the target verb replaced with a blank. The context should contain a clear 'time indicator' that allows students to place the event on a timeline and determine if the action happened in the past, is happening in the present, will happen in the future, or is conditional.

After providing the question, please identify the 'time indicator' in the passage, the 'correct answer choice', and provide an 'explanation' for why this choice is correct.

For instance:
```
Hard:
"Atoms in a synchrotron, a type of circular particle accelerator, travel faster and faster until they ______ a desired energy level, at which point they are diverted to collide with a target, smashing the atoms."	

Choices:					
A). will reach				
B). reach
C). had reached				
D). are reaching			
		
Correct Answer: B) reach
Time Indicator: "travel faster and faster"
Explanation: The phrase "travel faster and faster" is indicative of an ongoing action or a general truth about this particular situation. Therefore, the simple present tense "reach" is the appropriate choice.
								
Easy:
"Formed in 1967 to foster political and economic stability within the Asia-Pacific region, the Association of Southeast Asian Nations 
was originally made up of five members: Thailand, the Philippines, Singapore, Malaysia, and Indonesia. 
By the end of the 1990s, the organization ______ its initial membership."

Choices:
A). has doubled			
B). had doubled			
C). doubles	
D). will double

Correct Answer: B) had doubled					
Time Indicator: "By the end of the 1990s" 						
Explanation: The time indicator "By the end of the 1990s" shows that the action happened in the past before another event (the time of speaking, which is in the present). Therefore, the past perfect tense "had doubled" is the correct choice.		
								
Hard:
"In the 1950s, a man named Joseph McVicker was struggling to keep his business afloat when his sister-in-law Kay Zufall advised him to 
repurpose the company’s product, a nontoxic, clay-like substance for removing soot from wallpaper, as a modeling putty for kids. 
In addition, Zufall ______ selling the product under a child-friendly name: Play-Doh."	

Choices:
A). suggested		
B). suggests		
C). had suggested			
D). was suggesting				

Correct Answer: A) suggested
Time Indicator: "In the 1950s", "Kay Zufall advised", "In addition"
Explanation: The time indicators point to a series of events that happened in the past. The simple past tense "suggested" fits into this timeline, as it refers to a completed action in the past.

Easy
"In his 1963 $\textit{{Exposition of Music}}\text{{---}}\textit{{Electronic Television}}$, Korean American artist Nam June Paik showed how television 
images could be manipulated to express an artist’s perspective. Today, Paik ______ considered the first video artist."	

A). will be			
B). had been				
C). was					
D). is						
	
Correct Answer: D) is 
Time Indicator: "Today"
Explanation: The time indicator "Today" shows that the action is happening in the present. Therefore, the simple present tense "is" is the correct choice.
	
Easy
"Like other amphibians, the wood frog ($\textit{{Rana sylvatica}}$) is unable to generate its own heat, so during periods of subfreezing 
temperatures, it ______ by producing large amounts of glucose, a sugar that helps prevent damaging ice from forming inside its cells"	

Choices:						
A). had survived			
B). survived			
C). would survive				
D). survives						


Correct Answer; D) survives		
Time Indicator: "is", "helps"
Explanation: The time indicators "is" and "helps" show that the action is an ongoing fact or habit in the present. Therefore, the simple present tense "survives" is the correct choice.		
								
Easy

"Bonnie Buratti of NASA’s Jet Propulsion Laboratory ______ data about Saturn’s rings collected by the Cassini spacecraft when 
she made an interesting discovery: the tiny moons embedded between and within Saturn’s rings are shaped by the buildup of ring material on the moons’ surfaces."	

A) studies				
B) has been studying				
C) will study			
D) was studying			

Correct Answer: D) was studying
Time Indicator: "when she made" 
Explanation: The time indicator "when she made" shows that the action was ongoing at a specific time in the past when another action (the discovery) occurred. Therefore, the past continuous tense "was studying" is the correct choice.

{example_question}
```

TIME TABLE:
1. **Past Tenses:**
   * **Simple Past:** The verb ends in '-ed' for regular verbs. For example, "worked", "played", "danced". This is used to describe an action that was completed in the past.
   * **Past Perfect:** Formed by 'had' plus the past participle of the verb. For example, "had worked", "had played". This is used to describe an action that was completed before another past event.

2. **Present Tenses:**
   * **Simple Present:** The verb in its base form. For singular subjects, it typically ends with 's'. For plural subjects, it doesn't end in 's'. For example, "reads" (singular), "read" (plural). This is used to describe a current action or a general truth.
   * **Present Progressive:** Formed by using 'is/are' plus the verb ending in '-ing'. For example, "is working", "are playing". This is used to indicate an ongoing action in the present.
   * **Present Perfect:** Formed by 'has/have' plus the past participle of the verb. For example, "has worked", "have played". This is used to describe an action that happened at an unspecified time before now, or to express an action that started in the past and continues in the present.

3. **Future Tenses:**
   * **Simple Future:** Formed by using 'will' plus the base form of the verb. For example, "will work", "will play". This is used to describe an action that will happen in the future.
   * **Future Perfect:** Formed by 'will have' plus the past participle of the verb. For example, "will have worked", "will have played". This is used to indicate that an action will have been completed at some point in the future.

Outside of this timeline but important to know is the **Conditional Perfect**, formed by 'would have' plus the past participle of the verb. For example, "would have worked", "would have played". This is used to talk about something that didn't happen or is not known to have happened, but that is considered likely or possible.

The four answer choices must all be conjugated forms of the same verb. For an easy-level question, ensure three options are in clearly incorrect tenses based on the timeline context. For a hard-level question, two options should be clearly incorrect, while the remaining two belong to the same tense group (past, present, future, or conditional), requiring a solid understanding of tenses to answer correctly.

The question should not mix up number agreement - it can give two singular or plural choices, but no more. Remember, verb tense questions are about "when" the action happened. 

Ouput Format:
{format_instructions}

New Question:
"""
