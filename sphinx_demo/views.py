from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from sphinx_demo.models import Choice, Poll


class IndexView(generic.ListView):
    """This is a view that lists the currently available polls.  Limits to the 5 most recent polls.

    .. note:: URLconf name/url: index sphinx_demo/
    """

    template_name = 'sphinx_demo/index.html'    #:
    context_object_name = 'latest_poll_list'    #:

    def get_queryset(self):
        """Return the last five published polls (not including those set to be
        published in the future).
        """
        return Poll.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """Displays details for the specified poll, allowing a user to vote for a particular choice.

    .. note:: URLconf name/url: detail sphinx_demo/<pk>/
    """
    model = Poll                                #: :py:class:`sphinx_demo.models.Poll`
    template_name = 'sphinx_demo/detail.html'   #:

    def get_queryset(self):
        """Excludes any polls that aren't published yet.
        """
        return Poll.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Displays the results for the specified poll.  Vote counts are listed for each choice.

    .. note:: URLconf name/url: results sphinx_demo/<pk>/results/
    """
    model = Poll                                #: :py:class:`sphinx_demo.models.Poll`
    template_name = 'sphinx_demo/results.html'  #:


def vote(request, poll_id):
    """This is a deprecated function-based view.  It processes votes and increments the count for the choice
    that was chosen.  Redirects to :py:class:`sphinx_demo.views.ResultsView`.

    :param request: Standard Django request
    :param poll_id: ID of the poll to be processed.
    :type poll_id: int


    .. todo:: Convert to CBV.

    .. note:: URLconf name/url: vote sphinx_demo/<poll_id>/vote/
    """
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'sphinx_demo/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('sphinx_demo:results', args=(p.id,)))