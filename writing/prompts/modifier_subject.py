generate_prompt = """
Create a SAT-style practice passage with a particular focus on the modifier-subject category. 
One sentence in the passage should include a modifier and a subject clause.

Components:

'Modifier' - A participle phrase that directly describes the subject. This should either be in the present participle (-ing) form or the past participle (-ed/-en/-t/-n) form, and be followed by a comma.
'Subject Clause' - A clause containing the subject, which should be more extended than the 'Subject'.
'Subject' - A noun within the subject clause, described by the modifier.

Guidelines:

* Place the modifier right before the subject clause, separated by a comma.
* Replace the subject clause with '______' in the full sentence.
* Label each part of the sentence clearly.

Use the following format for the practice question:

Category: Modifier-Subject

Example Questions:
```
<Passage>
Based on genetic evidence, archaeologists have generally agreed that reindeer domestication began in the eleventh century CE. 
However, since uncovering fragments of a 2,000-year-old reindeer training harness in northern Siberia, ____ may have begun much earlier.

<Answer Choices>
A). researcher Robert Losey has argued that domestication
B). researcher Robert Losey’s argument is that domestication
C). domestication, researcher Robert Losey has argued,
D). the argument researcher Robert Losey has made is that domestication

<Modifier>
"since uncovering fragments of a 2,000-year-old reindeer training harness in northern Siberia,"
<Subject Clause>
"researcher Robert Losey has argued that domestication"
<Subject>
"researcher Robert Losey"


<Passage>
In assessing the films of Japanese director Akira Kurosawa, ____ have missed his equally deep engagement with Japanese artistic traditions such as Noh theater.

<Answer Choices>
A). many critics have focused on Kurosawa’s use of Western literary sources but
B). Kurosawa’s use of Western literary sources has been the focus of many critics, who
C). there are many critics who have focused on Kurosawa’s use of Western literary sources, but they
D). the focus of many critics has been on Kurosawa’s use of Western literary sources; they

<Modifier>
"In assessing the films of Japanese director Akira Kurosawa"
<Subject Clause>
"many critics have focused on Kurosawa’s use of Western literary sources but"
<Subject>
"many critics"

<Passage>
African American Percy Julian was a scientist and entrepreneur whose work helped people around the world to see. 
Named in 1999 as one of the greatest achievements by a US chemist in the past hundred years, ____ led to the first mass-produced treatment for glaucoma.

<Answer Choices>
A). Julian synthesized the alkaloid physostigmine in 1935; it
B). in 1935 Julian synthesized the alkaloid physostigmine, which
C). Julian’s 1935 synthesis of the alkaloid physostigmine
D). the alkaloid physostigmine was synthesized by Julian in 1935 and

<Modifier>
"Named in 1999 as one of the greatest achievements by a US chemist in the past hundred years"
<Subject Clause>
"Julian’s 1935 synthesis of the alkaloid physostigmine"
<Subject>
"Julian’s 1935 synthesis"

<Passage>
In 2016, engineer Vanessa Galvez oversaw the installation of 164 bioswales, vegetated channels designed to absorb and divert stormwater, 
along the streets of Queens, New York. By reducing the runoff flowing into city sewers, ______

<Answer Choices>
A) the mitigation of both street flooding and the resulting pollution of nearby waterways has been achieved by bioswales.
B) the bioswales have mitigated both street flooding and the resulting pollution of nearby waterways.
C) the bioswales’ mitigation of both street flooding and the resulting pollution of nearby waterways has been achieved.
D) both street flooding and the resulting pollution of nearby waterways have been mitigated by bioswales.


<Modifier>
"By reducing the runoff flowing into city sewers,"
<Subject Clause>
"the bioswales have mitigated both street flooding and the resulting pollution of nearby waterways."
<Subject>
"the bioswales"

<Passage>
Compared to that of alumina glass, ______ silica glass atoms are so far apart that they are unable to re-form bonds after being separated.

<Answer Choices>
A) silica glass is at a significant disadvantage due to its more dispersed atomic arrangement:
B) silica glass has a more dispersed atomic arrangement, resulting in a significant disadvantage:
C) a significant disadvantage of silica glass is that its atomic arrangement is more dispersed:
D) silica glass’s atomic arrangement is more dispersed, resulting in a significant disadvantage:


<Modifier>
"Compared to that of alumina glass,"
<Subject Clause>
"silica glass’s atomic arrangement is more dispersed, resulting in a significant disadvantage:"
<Subject>
"silica glass’s atomic arrangement"

{example_question}
```

Ouput Format:
{format_instructions}

Now, craft a similar question for practice:
"""
