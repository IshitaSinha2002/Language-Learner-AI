<h1>Language Learning Engine</h1>

<p>
  A personalized language learning workflow built using LangChain, LangGraph, and an LLM.
  The system generates lessons and quizzes, evaluates learner performance, maintains learning
  history, and adapts future lessons based on previous results.
</p>

<h2>Overview</h2>

<p>
  Language Learning Engine is a workflow-based AI application designed to simulate a personalized
  language tutor.
</p>

<p>
  Unlike a simple LLM chatbot that treats every interaction independently, this system maintains
  persistent learner state. Each learning session contributes to the learner's history, allowing
  the workflow to determine whether the learner should revise a topic or progress to the next one.
</p>

<p>
  The project demonstrates how LangGraph can be used to build stateful, adaptive workflows with
  human-in-the-loop interaction.
</p>

<h2>Key Features</h2>

<ul>
  <li>Personalized lessons based on language and learner level</li>
  <li>LLM-generated language lessons</li>
  <li>Structured quiz generation using Pydantic models</li>
  <li>Human-in-the-loop quiz interaction using LangGraph interrupts</li>
  <li>Automatic quiz evaluation and score calculation</li>
  <li>Learning history maintained across sessions</li>
  <li>Adaptive topic selection based on learner performance</li>
  <li>Persistent learner data stored in JSON</li>
  <li>LangGraph checkpointing for workflow state</li>
</ul>

<h2>Workflow</h2>

<pre>
START
  |
  v
Load Learner
  |
  v
Analyze Progress
  |
  v
Generate Lesson
  |
  v
Generate Quiz
  |
  v
Collect Learner Answers
  |
  v
Evaluate Answers
  |
  v
Update Progress
  |
  v
Choose Next Topic
  |
  v
Save Learner
  |
  v
END
</pre>

<h2>Adaptive Learning</h2>

<p>
  The workflow uses the learner's quiz performance to determine what happens next.
</p>

<pre>
Score &lt; 70%
    |
    v
Repeat Current Topic
    |
    v
Targeted Revision

Score &gt;= 70%
    |
    v
Mark Topic as Mastered
    |
    v
Move to Next Topic
</pre>

<p>
  This allows the system to adapt future sessions instead of treating every learning session
  independently.
</p>

<h2>Persistent State</h2>

<p>
  Learner information is stored in <code>data/learners.json</code>.
</p>

<pre>
{
    "learners": {
        "Ishita": {
            "target_language": "German",
            "learner_level": "0",
            "current_topic": "Basic Vocabulary",
            "weaknesses": [],
            "mastered_topics": [],
            "learning_history": [],
            "next_topic": "Basic Vocabulary"
        }
    }
}
</pre>

<p>
  When the same learner starts the application again, their previous progress is loaded and used
  by the workflow.
</p>

<h2>LangGraph State</h2>

<p>
  The shared workflow state contains information such as:
</p>

<pre>
learner_name
target_language
learner_level
current_topic
lesson
quiz
answers
score
weaknesses
mastered_topics
learning_history
next_topic
</pre>

<p>
  Each workflow node reads the relevant state and returns updates that are passed to subsequent
  nodes.
</p>

<h2>Project Structure</h2>

<pre>
Language Learner/
|
├── app/
│   ├── __init__.py
│   ├── state.py
│   ├── nodes.py
│   ├── graph.py
│   └── prompts.py
|
├── data/
│   └── learners.json
|
├── main.py
├── requirements.txt
├── .env
└── .gitignore
</pre>

<h2>Components</h2>

<h3>State</h3>

<p>
  <code>state.py</code> defines the shared <code>LearningState</code> used throughout the
  LangGraph workflow.
</p>

<h3>Nodes</h3>

<p>
  <code>nodes.py</code> contains the individual workflow operations:
</p>

<ul>
  <li><code>load_learner()</code> loads existing learner information</li>
  <li><code>analyze_progress()</code> determines the current learning topic</li>
  <li><code>generate_lesson()</code> generates a personalized lesson using the LLM</li>
  <li><code>generate_quiz()</code> creates a structured five-question quiz</li>
  <li><code>collect_answers()</code> pauses the workflow and waits for learner input</li>
  <li><code>evaluate_answers()</code> calculates the learner's score</li>
  <li><code>update_progress()</code> updates learning history and mastered topics</li>
  <li><code>choose_next_topic()</code> determines the next topic</li>
  <li><code>save_learner()</code> persists the updated learner state</li>
</ul>

<h3>Graph</h3>

<p>
  <code>graph.py</code> connects the nodes into a LangGraph workflow and uses a checkpointer to
  maintain workflow execution state.
</p>

<h3>Prompts</h3>

<p>
  <code>prompts.py</code> contains the prompts used for lesson and quiz generation.
</p>

<h3>Main Application</h3>

<p>
  <code>main.py</code> provides the command-line interface for starting a learning session,
  displaying the lesson and quiz, collecting answers, and displaying the final result.
</p>

<h2>Tech Stack</h2>

<table>
  <thead>
    <tr>
      <th>Technology</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Python</td>
      <td>Application development</td>
    </tr>
    <tr>
      <td>LangChain</td>
      <td>LLM integration and prompt orchestration</td>
    </tr>
    <tr>
      <td>LangGraph</td>
      <td>Stateful workflow orchestration</td>
    </tr>
    <tr>
      <td>Groq</td>
      <td>LLM inference</td>
    </tr>
    <tr>
      <td>Llama 3.3 70B Versatile</td>
      <td>Lesson and quiz generation</td>
    </tr>
    <tr>
      <td>Pydantic</td>
      <td>Structured LLM output validation</td>
    </tr>
    <tr>
      <td>JSON</td>
      <td>Persistent learner storage</td>
    </tr>
  </tbody>
</table>

<h2>Human-in-the-Loop</h2>

<p>
  The project uses LangGraph's interrupt mechanism to pause the workflow after generating a quiz.
</p>

<pre>
Generate Quiz
     |
     v
Interrupt Workflow
     |
     v
Learner Answers Questions
     |
     v
Resume Workflow
     |
     v
Evaluate Answers
</pre>

<p>
  This allows the LLM workflow to interact with a real user before continuing execution.
</p>

<h2>Getting Started</h2>

<h3>Prerequisites</h3>

<ul>
  <li>Python 3.12</li>
  <li>Groq API key</li>
  <li>Git</li>
</ul>

<h3>Installation</h3>

<p>Create a virtual environment:</p>

<pre>
py -3.12 -m venv venv
</pre>

<p>Activate the environment on Windows PowerShell:</p>

<pre>
.\venv\Scripts\Activate.ps1
</pre>

<p>Install the dependencies:</p>

<pre>
python -m pip install -r requirements.txt
</pre>

<h3>Environment Variables</h3>

<p>
  Create a <code>.env</code> file in the project root:
</p>

<pre>
GROQ_API_KEY=your_api_key_here
</pre>

<p>
  Do not commit the <code>.env</code> file to GitHub.
</p>

<h3>Run the Application</h3>

<pre>
python main.py
</pre>

<p>The application will ask for:</p>

<pre>
Enter your name:
What language do you want to learn?
What is your current level?
</pre>

<p>
  The system will then generate a lesson, create a quiz, collect the learner's answers,
  calculate the score, update progress, and save the learner state.
</p>

<h2>Example Session</h2>

<pre>
Enter your name: Ishita
What language do you want to learn? German
What is your current level? 0

LESSON

[Generated German lesson]

QUIZ

1. What does 'Hallo' mean in German?
   1. Goodbye
   2. Good night
   3. Hello
   4. How are you?

...

Enter your answers:

Question 1: danke
Question 2: Ich spreche
Question 3: Auf Wiedersehen
Question 4: Good night
Question 5: Danke

RESULT

Score: 40.0%

Areas to improve:
- What does 'Hallo' mean in German?
- How do you introduce yourself in German?
- What is the correct response to 'Danke'?

Next topic: Basic Vocabulary
</pre>

<h2>Learning Workflow Design</h2>

<p>
  The project separates responsibilities between deterministic application logic and
  LLM-based generation.
</p>

<h3>LLM Responsibilities</h3>

<ul>
  <li>Generating lessons</li>
  <li>Generating quizzes</li>
  <li>Adapting educational content to the learner's language and level</li>
</ul>

<h3>Application Responsibilities</h3>

<ul>
  <li>Maintaining workflow state</li>
  <li>Calculating scores</li>
  <li>Managing learner history</li>
  <li>Choosing the next topic</li>
  <li>Persisting learner information</li>
  <li>Managing workflow execution and interruption</li>
</ul>

<p>
  This separation makes the workflow more predictable, maintainable, and easier to extend.
</p>

<h2>Future Improvements</h2>

<ul>
  <li>Use a database instead of JSON for learner persistence</li>
  <li>Generate detailed weakness categories instead of storing incorrect questions</li>
  <li>Use LLM-based evaluation for open-ended language answers</li>
  <li>Track vocabulary and grammar mastery separately</li>
  <li>Add spaced repetition for previously learned concepts</li>
  <li>Add pronunciation practice</li>
  <li>Add conversational learning sessions</li>
  <li>Build a web interface for the learning engine</li>
  <li>Add analytics for long-term learner progress</li>
</ul>

<h2>Project Objective</h2>

<p>
  The primary objective of this project is to demonstrate how LangGraph can be used to build
  a persistent, adaptive AI workflow.
</p>

<p>
  The project combines LLM-powered content generation with deterministic state management,
  human-in-the-loop interaction, conditional learning progression, and persistent learner history.
</p>
