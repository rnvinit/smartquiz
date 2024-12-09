from django.core.management.base import BaseCommand
from quiz.models import Question, Choice

class Command(BaseCommand):
    help = 'Adds initial questions to the database'

    def handle(self, *args, **kwargs):
        questions = [
            {
                'text': 'What is the capital of France?',
                'choices': [
                    ('Paris', True),
                    ('London', False),
                    ('Berlin', False),
                    ('Madrid', False),
                ],
                'difficulty': 1,
            },
            {
                'text': 'Which planet is known as the Red Planet?',
                'choices': [
                    ('Mars', True),
                    ('Venus', False),
                    ('Jupiter', False),
                    ('Saturn', False),
                ],
                'difficulty': 1,
            },
            {
                'text': 'What is the largest mammal in the world?',
                'choices': [
                    ('Blue Whale', True),
                    ('African Elephant', False),
                    ('Giraffe', False),
                    ('Hippopotamus', False),
                ],
                'difficulty': 2,
            },
            {
                'text': 'Who painted the Mona Lisa?',
                'choices': [
                    ('Leonardo da Vinci', True),
                    ('Pablo Picasso', False),
                    ('Vincent van Gogh', False),
                    ('Michelangelo', False),
                ],
                'difficulty': 2,
            },
            {
                'text': 'What is the chemical symbol for gold?',
                'choices': [
                    ('Au', True),
                    ('Ag', False),
                    ('Fe', False),
                    ('Cu', False),
                ],
                'difficulty': 3,
            },
        ]

        for question_data in questions:
            question = Question.objects.create(text=question_data['text'], difficulty=question_data['difficulty'])
            for choice_text, is_correct in question_data['choices']:
                Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)

        self.stdout.write(self.style.SUCCESS('Successfully added initial questions'))