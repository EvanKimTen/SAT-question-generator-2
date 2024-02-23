FUNCTION_CATEGORY_PREPROCESS_PROMPT = """
Given the document content provided, select the 3~4 sentences passage excerpt (the portion of text directly sourced from a literary work) 
that at least 80 words long for a poem. Other types of passage excerpt must be at least 90 words long.

I need you to revise this passage with the following criteria:

1. Include a key sentence that will be underscored, like this: $\\underbar{{}}$”. This sentence will be used to create a comprehension question later. Choose a sentence that is important to the overall meaning of the passage.
2. If there are any instances of an em dash in the passage (this symbol: -), please replace it with an '—' instead.

Please edit the passage accordingly and provide me with the revised version.
Passage 
{passage}
"""