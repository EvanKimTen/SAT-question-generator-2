generate_prompt = """

Selected Passage from {source_title}: 
{selected_passage}


Instruction:
First, enclose one of the sentences in the Selected Passage within the “$\\underbar{{}}$” delimeters.
Second, Generate {category} SAT-style reading comprehension passage, question, and answer set 
that meets the following criteria:


1. Source of the passage excerpt: use only the provided selected_passage. Selected Passage must not be used "as-is" since it doesn't contain the underlined sentence.
You should make one sentence as underlined sentence.

2. Passage Length: The passage excerpt should be at least 90 words long.

3. Passage Formatting: The passage should be similar to given example passages and should contain a sentence within {{}} of “$\\underbar{{}}$”. This sentence will be the focus of the comprehension question. If an em dash appears in the passage, replace it with '—'.

4a. Scientific Names and Titles: Any scientific names or titles of books, novels, plays, films, artworks, periodicals, databases, or websites mentioned in the passage, question, or answer choices must be enclosed in $\\textit{{}}$. 

4b. Literary Names and Titles: If the passage, the question or the answer choices mention a title of an article, an essay, a chapter, a poem, a short story, a web page, a song, or a speech name, then there must be double quotation marks around that name (for example, “In My Life” is the title of a song by Beatles). 

5. Question: The question should ask about the **function of the underlined sentence** in the passage. It can follow one of these templates: 
* “Which choice best describes the function of the underlined sentence in the text as a whole?”
* “Which choice best states the function of the underlined sentence in the overall structure of the text?”
* “Which choice best describes the function of the () sentence in the overall structure of the text?”
* “Which choice best describes the function of the underlined portion in the text as a whole?”
* “Which choice best describes the function of the () sentence in the text?” 

The () should be replaced accordingly depending on the order of the sentence in the passage.

6. The Function-Purpose Relation: The question about the function of a particular sentence or text portion should be designed considering the overall purpose of the passage. Consider the author's intent: 
* Why was the text written? 
* What goal does it serve? 
The purpose of the text might be to explain, illustrate, criticize, argue, introduce a concept, or use any active verbs that demonstrate the goals of the author. Reflect on these possible goals while formulating the question. More specifically, remember that the function of an underlined sentence or text portion is about its role within the larger context of the passage. Hence, the question should prompt the reader to consider why this sentence is included and what contribution it makes to the overall passage.

7. Answer Choices: Provide four answer choices. Either two sets of two answer choices should have similar lengths, or three choices should be of similar length. The correct answer can be the longest but no more than 5 words longer than the other choice of similar length.

8. Answer Choices Content: Among the answer choices, two should be clearly incorrect (and such incorrect answer choices typically introduce information not directly addressed in the passage), one should be plausible but not supported by the text (and such incorrect answer choice typically shifts or blurs the purpose of a text by emphasizing details that aren’t a central focus), and one should be the correct answer that accurately states the function of the sentence in the context of the passage. 

9. Correct Answer and Explanation: State the correct answer by its corresponding letter (e.g., "Correct Answer: A") and explain why it is correct. Also, provide reasons why the other three answers are incorrect. For the explanation, make sure to provide a detailed explanation for the correct answer explaining why it correctly captures the overall purpose of the text and provide a succinct explanation for the wrong answers, clearly pointing out the wrong aspects.

10. The letter of the correct answer should be randomly assigned from A to D. Not all passages generated should have identical letters as the correct answer.

For Instance:

Passage:
```
$\\ \\, \\$Some bird species don't raise their own chicks. Instead, adult females lay their eggs in other nests, next to another bird species' own eggs. $/underbar{{Female cuckoos have been seen quickly laying eggs in the nests of other bird species when those birds are out looking for food.}}$ After the eggs hatch, the noncuckoo parents will typically raise the cuckoo chicks as if they were their own offspring, even if the cuckoos look very different from the other chicks.

Question: Which choice best describes the function of the underlined sentence in the text as a whole?
```

A). It introduces a physical feature of female cuckoos that is described later in the text.
B). It describes the appearance of the cuckoo nests mentioned earlier in the text. 
C). It offers a detail about how female cuckoos carry out the behavior discussed in the text.
D). It explains how other birds react to the female cuckoo behavior discussed in the text.

Correct Answer: C
Explanation: Choice C is the best answer because it best describes how the underlined sentence functions in the text as a whole. The first two sentences establish that birds of some species don't raise their own young; instead, they lay their eggs in the nests of birds of other species. The underlined sentence then states that female cuckoo birds engage in this behavior, having been observed specifically laying their eggs in other nests while the other birds are out finding food. According to the text, the cuckoo chicks are then raised by the other birds. Thus, the underlined sentence provides a particular detail about how female cuckoos carry out the behavior of laying eggs for other birds to raise. 
Choice A is incorrect. Rather than mentioning a physical feature of female cuckoos, the underlined sentence introduces a specific behavior of female cuckoos: laying eggs in the nests of birds of other species when the other birds are away. The only reference to physical features is the last sentence's general mention of cuckoo chicks looking different from chicks of other species. Choice B is incorrect because the underlined sentence refers to the nests of birds other than cuckoos and doesn't describe how any nests look, cuckoo or otherwise. Instead, the sentence addresses how female cuckoos use other birds' nests. Choice D is incorrect because the underlined sentence describes only female cuckoo behavior (laying eggs in the nests of birds of other species when the other birds are away); it's the last sentence of the text that addresses the other birds' reaction, indicating that those birds usually raise the cuckoo chicks once they've hatched. 


Passage:
```
A study by a team including finance professor Madhu Veeraraghavan suggests that exposure to sunshine during the workday can lead to overly optimistic behavior. $\\underbar{{Using data spanning from 1994 to 2010 for a set of US companies, the team compared over 29,000 annual earnings forecasts to the actual earnings later reported by those companies.}}$ The team found that the greater the exposure to sunshine at work in the two weeks before a manager submitted an earnings forecast, the more the manager's forecast exceeded what the company actually earned that year.

Question: Which choice best states the function of the underlined sentence in the overall structure of the text?
```

A). To summarize the results of the team's analysis.
B). To present a specific example that illustrates the study's findings.
C). To explain part of the methodology used in the team's study.
D). To call out a challenge the team faced in conducting its analysis.

Correct Answer: C
Explanation: Choice C is the best answer because it best describes how the underlined sentence functions in the text as a whole. The first sentence presents the implications of Veeraraghavan's team's study: sunshine exposure during work hours can cause overly optimistic behavior. The underlined sentence then describes the data the team consulted and how they were used (comparing predictions about earnings to what the companies actually earned), and the final sentence presents what the team found in their examination of the data. Thus, the underlined sentence mainly functions to explain part of the methodology used in the team's study. 

Choice A is incorrect because the underlined sentence explains in part how the team conducted their analysis of the effect of sunshine but doesn't address what the team found; a broad summary is instead given in the other two sentences. Choice B is incorrect because the underlined sentence doesn't present any specific examples from the team's comparisons of 29,000 earnings predictions to actual earnings; it simply explains in part how the team conducted their analysis. Choice D is incorrect because the underlined sentence simply explains in part how the team conducted their analysis; the text never mentions any challenges that the team encountered in their study. 

Passage:
```
$\\underbar{{President Richard Nixon is most famous for his participation in the 1970s Watergate political scandal, a convoluted tale of criminality and eroded ethics involving a constellation of associates such as security operative Jack Caulfield and Attorney General John Mitchell.}}$ But Nixon's legacy is complex: he has been praised for his role in affirming the sovereignty of tribal nations, and he once made an attempt at reforming United States health care policy that is arguably a precursor to the Affordable Care Act, which became law during the Barack Obama administration.		

Which choice best describes the function of the underlined sentence in the text as a whole?	
```


A) It presents an accomplishment of a historical figure whose significance is detailed later in the text.
B) It describes a common perception of a historical figure that is challenged by information presented later in the text.	
C) It states a claim about a historical figure that is supported by evidence later in the text.	
D) It compares the achievements of three historical figures to a fourth that is mentioned later in the text.	Correct Answer: B
Explanation: The underlined sentence introduces President Richard Nixon in a negative light by focusing on his role in the Watergate scandal. However, the text that follows highlights some of Nixon's positive contributions, challenging the initial portrayal. Therefore, the correct answer is B.
Answer A is incorrect because the underlined sentence doesn't present an accomplishment, rather it talks about the infamous Watergate scandal. Answer C is incorrect as the claim about the scandal is not further supported in the text; the text moves on to discuss Nixon's other actions. Answer D is incorrect because the sentence doesn't make a comparison among multiple historical figures.

Passage:
```
In what is now Washington state, the Tulalip Tribes operate the Hibulb Cultural Center. 
$\\underbar{{Relying on traditional knowledge to guide the design of exhibits, this institution presents Tulalip history and culture to the tribes' citizens.}}$ The Comanche Nation, a tribe in Oklahoma, employs a similar strategy in its own cultural center. Both centers contrast with museums that aren't Indigenous-led; when displaying Indigenous artifacts, such museums tend to anticipate mainly non-Indigenous audiences and rely on Euro-centric strategies for designing exhibits.		

Which choice best describes the function of the underlined sentence in the text as a whole?	
```

A) It suggests improvements to a particular tribal cultural center.	
B) It encourages tribal citizens to attend their local cultural center.	
C) It explains how one tribal cultural center differs from other tribal cultural centers.	
D) It provides a basic description of a particular tribal cultural center.					
Correct Answer: D)
Explanation: D is the answer because the underlined sentence in this context provides basic information about the operations of the Hibulb Cultural Center.
Answer A is incorrect as the sentence doesn't suggest any improvements for the cultural center. Answer B is incorrect because the sentence doesn't specifically encourage tribal citizens to attend the center. Answer C is incorrect because the sentence doesn't compare the Hibulb Cultural Center to other tribal cultural centers—it merely describes its approach.
						

Passage:
```
The Museum of Modern Art (MOMA) in New York City has an exhibition of video games that includes $\\textit{{Pac-Man}}$ from 1980, which museum visitors can play on site, and $\\textit{{SimCity 2000}}$ from 1994, which visitors can see only in a video presentation. MOMA claims the video presentations are only for games that would be impractical to display in a playable form, but $\\underbar{{video games are an inherently interactive medium,}}$ a feature that is grossly absent in a video-only presentation.		

Which choice best describes the function of the underlined portion in the text as a whole?	
```

A) It identifies a feature of many video games that is not shared by some of the games included in MOMA's exhibition.	
B) It provides a claim about video games as art that both MOMA and the author accept as true.	
C) It describes a misconception about video games that the author believes is evident in MOMA's choice about which video games to exhibit.	
D)It presents a consideration that the author thinks partly undermines MOMA's approach to exhibiting video games.	

Correct Answer: D)
Explanation: The underlined statement presents a fundamental feature of video games—their interactive nature—and uses this to criticize the Museum of Modern Art's decision to display certain games in a non-interactive format.
Answer A is incorrect because the sentence does not distinguish between games in the exhibition—it generalizes the interactive feature to all video games. Answer B is incorrect because the text suggests the author and MOMA have differing views on exhibiting video games, particularly the non-playable ones. Answer C is incorrect because the sentence is not highlighting a misconception about video games; it is pointing out a conflict between the medium's nature and MOMA's approach.


{example_question}


Ouput Format:
{format_instructions}

Include the generated text and question in problem_str.
There are only two problem types: 'Multiple Choice', 'Short Answer'
You must not include double quote(") within the value json output.


New Question:
"""
