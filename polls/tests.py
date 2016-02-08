import datetime
from django.utils import timezone
from .models import Question
from django.test import TestCase
from django.core.urlresolvers import reverse

# Create your tests here.

def create_question(question_text, days):
    """

    :param question_text: Text of question to be created.
    :param days: Offset days (positive or negative)
    :return: Question object with a time offset for testing.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,
                                   pub_date=time)


class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, the user should be told.
        :return:
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls have been published.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_index_view_displays_questions_in_the_past(self):
        """
        Questions older than a day shouldn't display on the index.
        :return:
        """
        create_question(question_text="Past Question.",days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past Question.>']
                                 )
    def test_index_view_with_a_future_question(self):
        """
        Questions published in the future shouldn't show on the index.
        :return:
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response,
                            "No polls have been published.",
                            status_code=200)
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_index_view_with_a_past_and_future_question_display_only_past(self):
        create_question(question_text="Future Question.", days=30)
        create_question(question_text="Past Question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past Question.>'])

    def test_index_view_with_two_past_questions(self):
        create_question(question_text="Past Question 1.", days=-30)
        create_question(question_text="Past Question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past Question 2.>',
                                  '<Question: Past Question 1.>'])

class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_future_question(self):
        """
        Detail view of a question with a pub_date in the future should return 404.
        """
        future_question = create_question(question_text="Future question.", days=5)
        response = self.client.get(reverse('polls:detail',
                                   args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_with_past_question(self):
        """
        Detail view of a question with a pub_date in the past should display properly (200 OK).

        """
        past_question = create_question(question_text="Past question.", days=-5)
        response = self.client.get(reverse('polls:detail',
                                   args=(past_question.id,)))
        self.assertContains(response,
                            past_question.question_text,
                            status_code=200)

class ResultsIndexDetailTests(TestCase):
    def test_with_question_from_future(self):
        """
        Results should only be shown for polls that have already been published.

        """
        future_question = create_question(question_text="Future Question.", days=30)
        response = self.client.get(reverse('polls:results',
                                           args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_question_has_choices(self):
        """
        Questions with zero choices shouldn't be displayed.

        """


class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently should return false for dates whose pub_date is in the future. Duh.
        Create a datetime object 30 days from now.
        Create a question object with pub_date as 30 days from now.
        Assert that if you asked whether it was published recently, the answer should be False.

        """

        time = timezone.now() + datetime.timedelta(days=30)

        future_question = Question(pub_date=time)

        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """

        was_published_recently() should return False whose pub_date is older than a day.
        Create a datetime object for 30 days ago.
        Create a question with that date as pub_date.
        Method should return False.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(),False)

    def test_was_published_recently_with_actual_recent_pub_date(self):
        """
        was_published_recently() should return True for actually recent questions.
        Create a time an hour ago.
        Create a question dated at that time.
        Should return true.
        :return:
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        new_question = Question(pub_date=time)
        self.assertEqual(new_question.was_published_recently(), True)

