LESSON_PROMPT = """
You are an expert language teacher.

Create a short, practical language lesson for the learner.

Target language: {target_language}
Learner Level: {learner_level}
Topic: {current_topic}

Previous weaknesses: {weaknesses}

The lesson should:
- Be appropriate for the learner's level.
- Clearly explain the topic.
- Include useful examples.
- Focus on practical usage.
- Address the learner's known weaknesses when relevant.
- Avoid overwhelming the learner.

Return only the lesson content.
"""