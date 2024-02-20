generate_prompt = """
Instruction:
Based on the SAT questions provided by the user, 
Generate an {category} SAT-style question and answer set following the criteria below.
Ensure each generated example adheres to these conditions.

Conditions:
1. Source of the passage excerpt: use only the provided selected_passage. Enclose one of the sentences in the selected_passage within the “$\\underbar{{}}$”

2. Passage Excerpt Length: The actual passage excerpt (the portion of text directly sourced from a literary work) must be at least 80 words long for a poem. Other types of passage excerpt must be at least 90 words long.

3. Passage Formatting: The passage should be similar to given example passages and should contain a sentence within {{}} of “$\\underbar{{}}$”. This sentence will be the focus of the comprehension question. If an em dash appears in the passage, replace it with '—'.

4a. Scientific Names and Titles: Any scientific names or titles of books, novels, plays, films, artworks, periodicals, databases, or websites mentioned in the passage, question, or answer choices must be enclosed in $\\textit{{}}$. 

4b. Literary Names and Titles: If the passage, the question or the answer choices mention a title of an article, an essay, a chapter, a poem, a short story, a web page, a song, or a speech name, then there must be double quotation marks around that name (for example, “In My Life” is the title of a song by Beatles). 

5. Introduce the passage in the following format: "The following text is from (Author)'s (year) (passage type) "Title." Provide one additional sentence about the context that does not overlap with answer choices if the information in the passage excerpt isn’t enough to understand the context of the excerpt.

6. Question: The question should ask about the **function of the underlined sentence** in the passage. It can follow one of these templates: 
“Which choice best describes the function of the underlined sentence in the text as a whole?”
“Which choice best states the function of the underlined sentence in the overall structure of the text?”
“Which choice best describes the function of the () sentence in the overall structure of the text?”
“Which choice best describes the function of the underlined portion in the text as a whole?”
“Which choice best describes the function of the () sentence in the text?” 

The () should be replaced accordingly depending on the order of the sentence in the passage.

7. The Function-Purpose Relation: The question about the function of a particular sentence or text portion should be designed considering the overall purpose of the passage. Consider the author's intent: 
Why was the text written? 
What goal does it serve? 
The purpose of the text might be to explain, illustrate, criticize, argue, introduce a concept, or use any active verbs that demonstrate the goals of the author. Reflect on these possible goals while formulating the question. More specifically, remember that the function of an underlined sentence or text portion is about its role within the larger context of the passage. Hence, the question should prompt the reader to consider why this sentence is included and what contribution it makes to the overall passage.


8. Answer Choices: Provide four answer choices. Either two sets of two answer choices should have similar lengths, or three choices should be of similar length. The correct answer can be the longest but no more than 5 words longer than the other choice of similar length. The letter of the correct answer should be randomly assigned from A to D. Not all passages generated should have identical letters as the correct answer.


9. Answer Choices Content: Among the answer choices, two should be clearly incorrect (and such incorrect answer choices typically introduce information not directly addressed in the passage), one should be plausible but not supported by the text, and one should be the correct answer that accurately states the role of the underlined text in the context of the passage. 

10. Correct Answer and Explanation: State the correct answer by its corresponding letter (e.g., "Correct Answer: A") and explain why it is correct. Also, provide reasons why the other three answers are incorrect. For the explanation, make sure to provide a detailed explanation for the correct answer explaining why it correctly captures the overall purpose of the text and provide a succinct explanation for the wrong answers, clearly pointing out the wrong aspects. Refer to the explanation of the questions provided by the user to help generate the explanation.

11. Prompt Order: Generate the prompt in the following order: the passage, the question, the answer choices, the correct answer (letter only, e.g., “Correct Answer: A”), and the explanation.

For Instance:

Example 1.

passage:
The following text is from Charlotte Forten Grimke's 1888 poem “At Newport.”
$\\ \\, \\$Oh, deep delight to watch the gladsome waves
$\\$Exultant leap upon the rugged rocks; 
$\\ \\underbar{{Ever repulsed, yet ever rushing on $\\text{{\\textemdash}}$ 
$\\ \\underbar{{$Filled with a life that will not know defeat;}}$ 
$\\$To see the glorious hues of sky and sea.
$\\$The distant snowy sails, glide spirit like,$\\$ Into an unknown world, to feel the sweet
$\\$Enchantment of the sea thrill all the soul,
$\\$Clearing the clouded brain, making the heart
$\\$Leap joyous as it own bright, singing waves!

Question: Which choice best describes the function of the underlined portion in the text as a whole?

Answer Choices:
A). It portrays the surroundings as an imposing and intimidating scene.
B). It characterizes the sea's waves as a relentless and enduring force
C). It conveys the speaker's ambivalence about the natural world.
D). It draws a contrast between the sea's waves and the speaker's thoughts.

Correct Answer: B
Explanation: Choice B is the best answer because it most accurately describes how the underlined portion functions in the text as a whole. The text presents the speaker's experience of viewing the sea. In the underlined portion, the speaker focuses on the idea that the waves hitting rocks on the shore are a relentless and enduring force: they are constantly pushed back (“ever repulsed”) but always return (“ever rushing on”), as though they have an energy that can't be overcome (“a life that will not know defeat”). 
Choice A is incorrect. Although the underlined portion characterizes the waves as a relentless force (always “repulsed” but still “rushing on” and never being defeated), the speaker doesn't suggest that the surroundings are intimidating. Instead, the speaker presents the scene in a positive way, describing the “deep delight” of the “gladsome,” or cheerful, waves and feeling “the heart / Leap joyous” while viewing the sea. Choice C is incorrect because the underlined portion doesn't suggest that the speaker is ambivalent, or has mixed feelings about, the natural world. Instead, it presents a single view of one part of the immediate surroundings: the speaker characterizes the sea's waves as an unstoppable force, since they are constantly pushed back but always return (“ever repulsed, yet ever rushing on”). Choice D is incorrect. Although the text later suggests the speaker's view of her own thoughts by referring to a “clouded brain” and a heart that leaps joyously, this reference neither occurs within the underlined portion nor establishes a clear contrast with the relentless determination of the waves. The underlined portion addresses only the speaker's view of the waves and doesn't suggest what her own thoughts might be.


Example 2. 

passage:
The following text is adapted from Zora Neale Hurston's 1921 short story $\\textit{{John Redding Goes to Sea}}$. John is a child who lives in a town in the woods.

$\\ \\, \\$Perhaps ten-year-old John was puzzling to the folk there in the Florida woods for he was an imaginative child and fond of day-dreams. 
The St. John River flowed a scarce three hundred feet from his back door. On its banks at this point grow numerous palms, luxuriant magnolias and bay trees. 
On the bosom of the stream float millions of delicately colored hyacinths. $\\underbar{{[John Redding] loved to wander down to the water's edge, and, casting in dry twigs, watch them sail away down stream to Jacksonville, the sea, the wide world and [he] wanted to follow them.}}$

Question: Which choice best describes the function of the underlined sentence in the text as a whole?

Answer Choices:
A). It provides an extended description of a location that John likes to visit.
B). It reveals that some residents of John's town are confused by his behavior.
C). It illustrates the uniqueness of John's imagination compared to the imaginations of other children.
D). It suggests that John longs to experience a larger life outside the Florida woods.

Correct Answer: D
Explanation: Choice D is the best answer because it accurately describes how the underlined sentence functions in the text as a whole. The text establishes that John has a strong imagination and then goes on to describe the St. John River near John's home in the Florida woods. The underlined sentence depicts John sending twigs sailing down the river while he imagines them reaching “Jacksonville, the sea, the wide world,” where he wishes he could follow. This suggests that John longs to expand his life experiences beyond the Florida woods. 
Choice A is incorrect because the second and third sentences of the text provide an extended description of the riverbank where John likes to go, whereas the underlined sentence describes what John does at that location. Choice B is incorrect because the first sentence of the text suggests that John's behavior “was puzzling” to others around him, whereas the underlined sentence concerns the content of John's imaginings. Choice C is incorrect because the underlined sentence elaborates on John's imagination but doesn't mention any other children to whom John could be compared.


Example 3.

passage:
The following text is from Edith Wharton's 1905 novel $\\textit{{The House of Mirth}}$. Lily Bart and a companion are walking through a park.

$\\ \\, \\$Lily had no real intimacy with nature, but she had a passion for the appropriate and could be keenly sensitive to a scene 
which was the fitting background of her own sensations. “$\\underbar{{The landscape outspread below her seemed an enlargement of her present mood,
and she found something of herself in its calmness, its breadth, its long free reaches.}}$” 
On the nearer slopes the sugar-maples wavered like pyres of light; lower down was a massing of grey orchards, and here and there the lingering green of an oak-grove.

Question: Which choice best describes the function of the underlined sentence in the text as a whole?

Answer Choices:
A). It creates a detailed image of the physical setting of the scene.
B). It establishes that a character is experiencing an internal conflict.
C). It makes an assertion that the next sentence then expands on.
D). It illustrates an idea that is introduced in the previous sentence.

Correct  Answer: D
Explanation: Choice D is the best answer because it best describes how the underlined sentence functions in the text as a whole. The first sentence of the text establishes that Lily can be “keenly sensitive to” scenes that serve as a “fitting background” for her feelings—that is, she's very aware of when a setting seems to reflect her mood. The next sentence, which is underlined, then demonstrates this awareness: Lily views the landscape she's in as a large-scale reflection of her current mood, identifying with elements such as its calmness. Thus, the function of the underlined sentence is to illustrate an idea introduced in the previous sentence. 
Choice A is incorrect because the underlined sentence describes the scene only in very general terms, referring to its calmness, breadth, and long stretches of land. It's the next sentence that adds specific details about colors, light, and various trees nearby. Choice B is incorrect because nothing in the underlined sentence suggests that Lily is experiencing an internal conflict. In fact, the sentence indicates that Lily thinks the landscape reflects her own feeling of calmness. Choice C is incorrect because the only assertion in the underlined sentence is that Lily feels that broad aspects of the landscape, such as its calmness, reflect her current mood, and that assertion isn't expanded on in the next sentence. Instead, the next sentence describes specific details of the scene without connecting them to Lily's feelings.


Example 4.

passage:
The following text is adapted from $\\textit{{Indian Boyhood,}}$ a 1902 memoir by Ohiyesa (Charles A. Eastman), a Santee Dakota writer. In the text, Ohiyesa recalls how the women in his tribe harvested maple syrup during his childhood.
$\\ \\, \\$Now the women began to test the trees$\\text{{---}}$moving leisurely among them, axe in hand, and striking a single quick blow, to see if the sap would appear. $\\underbar{{The trees, like people, have their individual characters: some were ready to yield up their life-blood, while others were more reluctant.}}$ Now one of the birchen basins was set under each tree, and a hardwood chip driven deep into the cut which the axe had made. From the corners of this chip$\\text{{---}}$at first drop by drop, then more freely$\\text{{---}}$the sap trickled into the little dishes.

Question: Which choice best describes the function of the underlined sentence in the text as a whole?

Answer Choices:
A). It portrays the range of personality traits displayed by the women as they work.
B). It foregrounds the beneficial relationship between humans and maple trees. 
C). It demonstrates how human behavior can be influenced by the natural environment.
D). It elaborates on an aspect of the maple trees that the women evaluate.

Correct: D
Explanation: Choice D is the best answer because it best describes the function of the underlined sentence in the text's overall portrayal of how the women in Ohiyesa's tribe harvested maple syrup. The text states that the women used an axe to strike the maple trees in order to find out which ones would produce sap. The underlined sentence compares the trees to people, with the sap described as the trees' “life-blood.” Some of the trees are ready to give out their sap, while others are unwilling to do so. Using personification, the sentence provides greater detail about the aspect of the maple trees—their potential to give sap—that the women are evaluating. 
Choice A is incorrect because the personalities of the women are not discussed in the text. Although the underlined sentence does mention “individual characters,” this reference is not to the women in the text but rather to the maple trees, which the sentence compares to people with individual character traits. Choice B is incorrect because the underlined sentence focuses on the trees' willingness or refusal to yield sap, not on the beneficial relationship between the women and the trees. Additionally, although the text does suggest that the women and their tribe benefit from the maple trees since the trees allow the women to harvest syrup, there is nothing in the text to suggest that the trees benefit from this relationship in turn. Choice C is incorrect because the underlined sentence is comparing maple trees to humans, not addressing the influence of the natural environment on how the actual humans in the text, the women, behave.


{example_question}

Ouput Format:
{format_instructions}

New Question:
"""
