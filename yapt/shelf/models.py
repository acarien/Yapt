from django.db import models
from datetime import date, timedelta

# Duration
class Duration(models.Model):
	name = models.CharField(max_length=100, unique=True)
	numberDays = models.PositiveIntegerField(null=True, blank=True)
	date = models.DateField(null=True, blank=True)

	def getEndDate(self):
		today = date.today()
		if self.numberDays is None:
			if self.date is None:
				raise ValueError('Date or NumberDays must have a value')
			else:
				return date(today.year, self.date.month, self.date.day)	
		else:
			return today + timedelta(self.numberDays);
			
	def __unicode__(self):
		return self.name

# Article
class Article(models.Model):
	title = models.CharField(max_length=200)
	url = models.URLField(max_length=200, unique=True)
	creationDate = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
	endDate = models.DateField(null=True)
	hasBeenRead = models.BooleanField(default=False)

	def __unicode__(self):
		return self.title
