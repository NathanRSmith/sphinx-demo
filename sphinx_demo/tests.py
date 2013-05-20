import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from sphinx_demo.models import Poll


class PollMethodTests(TestCase):
    """Tests the :py:class:`sphinx_demo.models.Poll` methods.
    """

    def test_was_published_recently_with_future_poll(self):
        """Tests that :py:meth:`sphinx_demo.models.Poll.was_published_recently` should return False for polls whose
        pub_date is in the future
        """
        future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        """Tests that :py:meth:`sphinx_demo.models.Poll.was_published_recently` should return False for polls whose pub_date
        is older than 1 day
        """
        old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=30))
        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        """Tests that :py:meth:`sphinx_demo.models.Poll.was_published_recently` should return True for polls whose pub_date
        is within the last day
        """
        recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(recent_poll.was_published_recently(), True)


def create_poll(question, days):
    """Creates a poll with the given `question` published the given number of
    `days` offset to now (negative for polls published in the past,
    positive for polls that have yet to be published).

    :param question: The question for the poll
    :type question: str
    :param days: How many days in the future to be published
    :type days: int
    :returns: The newly created poll.
    :rtype: :py:class:`sphinx_demo.models.Poll` object.
    """
    return Poll.objects.create(question=question,
        pub_date=timezone.now() + datetime.timedelta(days=days))


class PollViewTests(TestCase):
    """Tests the views.
    """
    def test_index_view_with_no_polls(self):
        """Tests :py:class:`sphinx_demo.views.IndexView` that if no polls exist,
        an appropriate message should be displayed.
        """
        response = self.client.get(reverse('sphinx_demo:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_a_past_poll(self):
        """Tests :py:class:`sphinx_demo.views.IndexView` that polls with a pub_date in
        the past should be displayed on the index page.
        """
        create_poll(question="Past poll.", days=-30)
        response = self.client.get(reverse('sphinx_demo:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past poll.>']
        )

    def test_index_view_with_a_future_poll(self):
        """Tests :py:class:`sphinx_demo.views.IndexView` that polls with a pub_date
        in the future should not be displayed on the index page.
        """
        create_poll(question="Future poll.", days=30)
        response = self.client.get(reverse('sphinx_demo:index'))
        self.assertContains(response, "No polls are available.", status_code=200)
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_future_poll_and_past_poll(self):
        """Tests :py:class:`sphinx_demo.views.IndexView` that even if both past
        and future polls exist, only past polls should be displayed.
        """
        create_poll(question="Past poll.", days=-30)
        create_poll(question="Future poll.", days=30)
        response = self.client.get(reverse('sphinx_demo:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past poll.>']
        )

    def test_index_view_with_two_past_polls(self):
        """Tests :py:class:`sphinx_demo.views.IndexView` that the polls index page may display multiple polls.
        """
        create_poll(question="Past poll 1.", days=-30)
        create_poll(question="Past poll 2.", days=-5)
        response = self.client.get(reverse('sphinx_demo:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
             ['<Poll: Past poll 2.>', '<Poll: Past poll 1.>']
        )


class PollIndexDetailTests(TestCase):
    """Tests :py:class:`sphinx_demo.views.DetailView`
    """
    def test_detail_view_with_a_future_poll(self):
        """The detail view of a poll with a pub_date in the future should
        return a 404 not found.
        """
        future_poll = create_poll(question='Future poll.', days=5)
        response = self.client.get(reverse('sphinx_demo:detail', args=(future_poll.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_poll(self):
        """The detail view of a poll with a pub_date in the past should display
        the poll's question.
        """
        past_poll = create_poll(question='Past Poll.', days=-5)
        response = self.client.get(reverse('sphinx_demo:detail', args=(past_poll.id,)))
        self.assertContains(response, past_poll.question, status_code=200)