icl_example={
    "boolqa":"""Question: Were Scott Derrickson and Ed Wood of the same nationality?
Thought: Who is Scott Derrickson?
Answer: Scott Derrickson is an **American** director, screenwriter and producer.
Thought: Who is Ed Wood?
Answer: Ed Wood was an **American*** filmmaker.
Thought: I have got all the information. Both Scott Derrickson and Ed Wood are **American**.
Answer: FINISH[True]

Question: Are more people today related to Genghis Khan than Julius Caesar?
Thought: How many children does Julius Caesar has?
Answer:  Julius Caesar had **three children**.
Thought: How many children does Genghis Khan has?
Answer: Genghis Khan had **sixteen children**
Thought: I have got all the information. Genghis Khan had sixteen children while Julius Caesar only had three children. People today related to Genghis Khan more than Julius Caesar
Answer: FINISH[True]

Question: Is Steve Carell's character on The Office portrayed as one with tremendous leadership skills?
Thought: Who is Steve Carell's character on The Office?
Answer: Steve Carell plays Michael Scott on The Office.
Thought: Does Michael Scott has powerful leadership skills? in `The Office`.
Answer: Michael Scott is a clueless and naive character that is not meant to be seen as effective in his job as General Manager.
Thought: I have got all the information. Steve Carell plays Michael Scott on The Office and Michael Scott does not have tremendous leadership skills.
Answer: FINISH[False]

Question: Was Martin Luther same sect as Martin Luther King Jr.?
Thought: What sect did Martin Luther belong to?
Answer: Martin Luther was a seminal figure in the Protestant Reformation and thus belonged to the Protestant sect of Christianity.
Thought: What sect did Martin Luther King Jr. belong to?
Answer: Martin Luther King Jr. was a Baptist minister, thus he belonged to the Baptist sect of Christianity.
Thought: I have got all the information. Martin Luther was a Protestant and Martin Luther King Jr. was a Baptist.
Answer: FINISH[False]""",
    "musique":"""Question: Where do Greyhound buses leave from in the city where Arna Selznick's employer is headquartered?
Thought: Who is the employer of Arna Selznick?
Answer: The employer of Arna Selznick is Nelvana since he directed Nelvana's 1985 animated film The Care Bears Movie.
Thought: Nelvana is an animation studio and entertainment company. Where is the headquarters of Nelvana?
Answer: The headquarters of Nelvana is in Toronto.
Thought: Where do Greyhound buses leave from Toronto?
Answer: Greyhound buses leave from **Toronto Coach Terminal**
Thought: the employer of Arna Selznick is Nelvana. Nelvana's headquartered is in Toronto. Greyhound leave from **Toronto Coach Terminal**
Answer: FINISH[Toronto Coach Terminal]

Question: Which county does Lloyd Dane's birthplace belong to?
Thought: What is the Lloyd Dane's birthplace?
Answer: Lloyd Dane's birthplace is Eldon.
Thought: Eldon is a city. Which country does Eldon belong to?
Answer: Eldon belongs to Miller County.
Thought: Lloyd Dane's birthplace is Eldon. Eldon belongs to Miller County.
Answer: FINISH[Miller County]

Question: Who wrote \"Turn Me On\" by the performer of \"Happy Pills\"?
Thought: Happy Pills is an song from American. Who is the performer of "Happy Pills"?
Answer: the performer of Happy Pills is Norah Jones.
Thought: Turn Me On is a song. Who wrote "Turn Me On" performed by Norah Jones?
Answer: **John D. Loudermilk** wrote: "Turn Me On".
Thought: The performer of "Happy Pills" is **Norah Jones**. **John D. Loudermilk** wrote the `Turn Me On` by Norah Jones.
Answer: FINISH[John D. Loudermil]

Question: Who did the screenwriter for Good Will Hunting play in Dazed and Confused?
Thought: Who is the screenwriter of Good Will Hunting?
Answer: the screenwriter of Good Will Hunting is Ben Affleck.
Thought: who did Ben Affleck play in "Dazed and Confused"?
Answer: Ben Affleck plays Fred O'Bannion in "Dazed and Confused"
Thought: **Ben Affleck** is the screenwriter of Good Will Hunting. Ben Affleck plays **Fred O'Bannion** in `Dazed and Confused`.
Answer: FINISH[Fred O'Bannion]""",
    "hotpot":"""Question: Which magazine was started first, Arthur's Magazine or First for Women?
<Thought> When Arthur's Magazine started?
<Answer> Arthur's Magazine was an American literary periodical published in Philadelphia, which started in **19th (1844)**.
<Thought> When First for Women started?
<Answer> "First for Women" is a well-known women's magazine that covers topics such as health, beauty, fitness, food, and lifestyle. It started in **1989**.
<Thought> Which one started first?
<Answer> Finish[Arthur's Magazine]

Question: Who was the captain of the only battleship to provide gunfire support during the Vietnam War?
<Thought> Who was the captain of the battleship that provided gunfire support during the Vietnam War?
<Answer> Rear Adm. J. (October 23, 1924 – November 4, 2007) was notable as the captain of the battleship USS "New Jersey" during that ship's deployment to the Vietnam War in 1968. 
<Thought> I have got all the information. And **Rear Adm. J.** is the captain providing gunfire support during the Vietnam War?`
Answer 2: FINISH[Rear Adm. J.]

Question: How old is the female main protagonist of Catching Fire? 
<Thought> What is the Catching Fire?
<Answer> Catching Fire is the second book in "The Hunger Games trilogy" written by Suzanne Collins.  It is written in the voice of **Katniss Everdeen**,
<Thought> How old is Katniss Everdeen in Catching Fire book?
<Answer> Katniss Everdeen in Catching Fire book is **16 years old**
<Thought> FireKatniss Everdeen, the female main protagonist of Catching, is FireKatniss Everdeen and she is **16** years old.
<Answer> FINISH[16]

Question: What is one of the stars of The Newcomers known for?
<Thought> Who are the stars in Newcomers?
<Answer> **Chris Evans** is one of the stars in the Newcomers.
<Thought> What is the Chris Evans known for?
<Answer> Chris Evans is known for **superhero roles as the Marvel Comics**
<Thought> I have got all the information. Chris Evans is a star in Newcomers, who is known for **superhero roles as the Marvel Comics**
<Answer> FINISH[Superhero roles as the Marvel Comics]

Question: Billy Preston is an American college basketball player for a team that competes in what?
<Thought> Billy Preston is an American college basketball player. What does Billy Preston play for?
<Answer> Billy Preston is an American college basketball player for the **Kansas Jayhawks**.
<Thought> What does the Kansas Jayhawks compete for?
<Answer> Kansas Jayhawks competes for the **Big 12 Conference**
<Thought> I have got all the information. Billy Preston play for Kansas Jayhawks, and Kansas Jayhawks competes for the **Big 12 Conference**
<Answer> FINISH[The Big 12 Conference]""",

'multihotpot1':"""Question: Are North Marion High School (Oregon) and Seoul High School both located in the same country?
Thought: Which country is North Marion High School (Oregon) located in?
Answer: North Marion High School (Oregon) is located in **United States**.
Thought: Which country is Seoul High School located in?
Answer: Seoul High School is located in **South Korea**.
Thought: Seoul High School is located in South Korea while North Marion High School (Oregon) is located in the United States. They are not in the same country.
Answer: FINISH[No]

Question: Does Jon Wertheim have the same nationality as Jon L. Mills
Thought: what is Jon Wertheim's nationality?
Answer: Jon Wertheim's country of citizenship is American.
Thought: what is Jon L. Mills's nationality?
Answer: Jon L. Mills's nationality is American
Thought: Both Jon Wertheim and Jon L. Mills are American.
Answer: FINISH[yes]

Question: Which film came out first, Blind Shaft or The Mask Of Fu Manchu?
Thought: When was the film Blind Shaft released?
Answer: Blind Shaft was released in **2003**
Thought: When was the film The Mask Of Fu Manchu released?
Answer: The Mask of Fu Manchu was released in **1932**, which is earlier than Blind Shaft.
Thought: The film Mask Of Fu Manchu came out in 1932 while The film Blind Shaft came out in 2003. The Mask of Fu Manchu came out first.
Answer: FINISH[The Mask of Fu Manchu]

Question: When did John V, Prince Of Anhalt-Zerbst's father die?
Thought: Who is the father of John V, Prince Of Anhalt-Zerbst?
Answer:  **Ernest I, Prince of Anhalt-Dessau** is the father of John V, Prince Of Anhalt-Zerbst.
Thought: when did John V, Prince Of Anhalt-Zerbst die?
Answer: Ernest I, Prince of Anhalt-Dessau died in **1516**.
Thought: Ernest I, Prince of Anhalt-Dessau is the father of John V, Prince Of Anhalt-Zerbst, and he died in 1516
Answer: FINISH[1516]

Question: Where was the director of the film Ronnie Rocket born?
Thought: Who is the director of the film Ronnie Rocket?
Answer: **David Lynch** is the director of Ronnie Rocket
Thought: David Lynch is the director. Where was David Lynch born?
Answer: **Missoula, Montana** is the birthplace of David Lynch.
Thought: David Lynch is the director of Ronnie Rocket. He was born in Missoula, Montana.
Answer: FINISH[Missoula, Montana]""",
'multihotpot': """Question: Are North Marion High School (Oregon) and Seoul High School both located in the same country? (yes or no)
Thought: Which country is North Marion High School (Oregon) located in?
Answer: North Marion High School (Oregon) is located in **United States**.
Thought: Which country is Seoul High School located in?
Answer: Seoul High School is located in **South Korea**.
Thought: Seoul High School is located in South Korea while North Marion High School (Oregon) is located in the United States. They are not in the same country.
Answer: FINISH[No]

Question: Which film came out first, Blind Shaft or The Mask Of Fu Manchu?
Thought: When was the film Blind Shaft released?
Answer: Blind Shaft was released in **2003**
Thought: When was the film The Mask Of Fu Manchu released?
Answer: The Mask of Fu Manchu was released in **1932**, which is earlier than Blind Shaft.
Thought: The film Mask Of Fu Manchu came out in 1932 while The film Blind Shaft came out in 2003. The Mask of Fu Manchu came out first.
Answer: FINISH[The Mask of Fu Manchu]

Question: Which film has the director died earlier, Poker In Bed or The Machine To Kill Bad People?
Thought: Who is the director of 'Poker In Bed'
Answer: the director of 'Poker In Bed' is Giuliano Carnimeo.
Thought: Giuliano Carnimeo is the director of Poker In Bed. When did the Giuliano Carnimeo die?
Answer: Giuliano Carnimeo die in 10 September 2016.
Thought: Who is the director of The Machine To Kill Bad People?
Answer: the director of 'The Machine To Kill Bad People' is Roberto Rossellini.
Thought: Roberto Rossellini is the director of 'The Machine To Kill Bad People'. when did the Roberto Rossellini die?
Answer: Roberto Rossellini die in 3 June 1977.
Thought: Poker In Bed's director (die in 10 September 2016) earlier than the director of The Machine To Kill Bad People (die in 3 June 1977).
Answer: FINISH[The Machine To Kill Bad People]"""
}

GENERATION_SYSTEM="""Given an input query, please think step by step through an iterative self-ask process."""
#
GENERATION_USER=""""You need to decompose a complex question into several sub-questions step by step and give an answer to each sub-query, until finishing it with a final answer.
Specifically, please take care of your output format:
1. Each decomposed sub-query should start with a <Thought>.
2. Each answer should start with a <Answer>.
3. The final answer should be wrapped with FINISH[...].



Here are some examples, and you should follow the same format:

{icl_example}

Starting below, please complete the following question answering trajectory following the above format,

Question: {query}
"""

BOOL_GENERATION_USER=""""Please judge the question step by step by interleaving Thought and Answer.
- Thought: in the Thought step, you should reason about the current situation and formulate a sub-question. Your Thought process should aim to formulate as simple and specific a question as possible, which should include a clear description of the key entities’ features.
- Answer: in the Answer step, you should answer the sub-question proposed in the Thought step.

## Format
Starting below, you must follow the following format:

Question: a complex question
Thought: The first sub-question
Answer: the first sub-question.
... (the Thought and Answer steps can repeat N times)
Thought: the final thought
Answer: FINISH[your final answer, i.e., True/False]

## Note:
1. It is better NOT TO use pronouns in Thought, but to use the corresponding results obtained previously. For example, instead of “What is the most popular movie directed by this person”, you should output “Get the most popular movie directed by Martin Scorsese”.
2. Please ensure the answer in the Answer step is clear without any ambiguity. For example, the pronouns, e.g., it, them, and his, are not allowed since these words rely on specific context.
3. Your final answer should be True or False. `True` indicates the question is right while the `False` indicates the question is wrong.

Here are some examples:

{icl_example}

Question: {query}
"""

GROUNDING_SYSTEM="""First, read the reference paragraphs and extract the corresponding sentence to answer the question. Then compare your solution to the student's answer and evaluate if the student's answer is correct or not. Don't decide if the student's answer is correct until you have extracted the sentence yourself."""

GROUNDING_USER="""Here are some paragraphs, and each paragraph is identified by a numeric identifier, e.g., []. 
{doc}

Starting below, you should follow this format:
Question: the given question
Student's answer: the answer provided by a student
Extracted sentence: the sentence extracted from the above paragraphs. You must include the citation of the paragraph from which the sentence is taken by ending with corresponding numeric identifier, e.g., [].  If no paragraph is cited, you should **not give** the identifier.
The student's answer is Ture or False: just give "True" or "False". If the paragraphs do not contain the answer, please give a 'True'

Begin and complete the following content!
Question: {question}
Student's answer: {answer}
"""
