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
			1:KeepAllArticlesFilter(),
			2:ArticlesDueFilter(),
			3:OverdueArticlesFilter(),
			4:ArticlesDueTomorrowFilter(),
			5:ArticlesDueTenDaysFilter(),
			6:AlreadyReadArticlesFilter(),
		}	

		@staticmethod
		def items():
			return ArticleFilters.Filters.items()

		@staticmethod
		def contains(filter_id):
			return filter_id is not None and filter_id in ArticleFilters.Filters

		@staticmethod
		def get_filter(filter_id):
			if not ArticleFilters.contains(filter_id):
				raise KeyError('Unknown filter_id \'%s\'.' % filter_id)

			return ArticleFilters.Filters[filter_id]

		@staticmethod
		def get_filter_id(filter_name):
			if filter_name is None:
				return 1 #default in config

			filter = next(ifilter(lambda (key, value): value.name() == filter_name, ArticleFilters.Filters.items()), None)
			if filter is None:
				return 1 #default in config
			(key, value) = filter
			return key
