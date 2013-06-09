from itertools import ifilter
from shelf.models import Article, Duration
from datetime import date, timedelta

class KeepAllArticlesFilter:	
	def get_articles(self):
		return Article.objects.all()
	
	@staticmethod
	def name():
		return 'all'

	def __str__(self):
		return 'All'

class OverdueArticlesFilter:
	def get_articles(self):
		return Article.objects.filter(endDate__lt=date.today(), hasBeenRead=False)

	@staticmethod
	def name():
		return 'overdue'

	def __str__(self):
		return 'Overdue'

class ArticlesDueTomorrowFilter:
	def get_articles(self):
		tomorrow = date.today() + timedelta(days=1)
		return Article.objects.filter(endDate__lte=tomorrow, hasBeenRead=False)

	@staticmethod
	def name():
		return 'dueTomorrow'

	def __str__(self):
		return 'Due tomorrow'

class ArticlesDueTenDaysFilter:
	def get_articles(self):
		days = date.today() + timedelta(days=10)
		return Article.objects.filter(endDate__lte=days, hasBeenRead=False)

	@staticmethod
	def name():
		return 'due10Days'

	def __str__(self):
		return 'Due in 10 days'

class ArticlesDueFilter:
	def get_articles(self):
		return Article.objects.filter(endDate__isnull=False, hasBeenRead=False)

	@staticmethod
	def name():
		return 'withDeadLine'

	def __str__(self):
		return 'With deadline'

class AlreadyReadArticlesFilter:
	def get_articles(self):		
		return Article.objects.filter(hasBeenRead=True)

	@staticmethod
	def name():
		return 'alreadyRead'

	def __str__(self):
		return 'Already read'

class ArticleFilters:
		Filters = {
			KeepAllArticlesFilter.name():KeepAllArticlesFilter(),
			ArticlesDueFilter.name():ArticlesDueFilter(),
			OverdueArticlesFilter.name():OverdueArticlesFilter(),
			ArticlesDueTomorrowFilter.name():ArticlesDueTomorrowFilter(),
			ArticlesDueTenDaysFilter.name():ArticlesDueTenDaysFilter(),
			AlreadyReadArticlesFilter.name():AlreadyReadArticlesFilter(),
		}	

		@staticmethod
		def items():
			return ArticleFilters.Filters.items()

		@staticmethod
		def contains(filter_name):
			return filter_name is not None and filter_name in ArticleFilters.Filters

		@staticmethod
		def get_filter(filter_name):
			if not ArticleFilters.contains(filter_name):
				raise KeyError('Unknown filter_name \'%s\'.' % filter_name)

			return ArticleFilters.Filters[filter_name]
