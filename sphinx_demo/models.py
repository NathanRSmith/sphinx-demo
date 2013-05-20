from django.db import models
from django.utils import timezone
import datetime


class Poll(models.Model):
    """This is a model for polls with multiple :py:class:`sphinx_demo.models.Choice`.
    """

    question = models.CharField(max_length=200)         #: The question text
    pub_date = models.DateTimeField('date published')   #: The publication date to make this poll available

    def __unicode__(self):
        return self.question

    def was_published_recently(self):
        """Checks to see if the published date is less than a day prior to "now".
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date < now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """This is a model for choices associated with :py:class:`sphinx_demo.models.Poll`.
    """
    poll = models.ForeignKey(Poll)                  #: Choice for :py:class:`sphinx_demo.models.Poll`
    choice_text = models.CharField(max_length=200)  #: Text for a choice
    votes = models.IntegerField(default=0)          #: How many votes this choice has received

    def __unicode__(self):
        return self.choice_text