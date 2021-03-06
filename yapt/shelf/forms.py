#-*- coding: utf-8 -*-
from django import forms
from shelf.models import Article, Duration
from shelf.articleFilters import *
from django.forms import extras
from django.forms.util import flatatt
import datetime

class ArticleForm(forms.ModelForm):
	duration = forms.ModelChoiceField(queryset=Duration.objects.all(), required=False)

	class Meta:
		model = Article
		fields = ['url', 'title', 'duration']

class SelectEditArticleForm(forms.Form):
	articles = forms.ModelChoiceField(queryset=Article.objects.all().extra(select={'lower_title':'lower(title)'}).order_by('lower_title'))	

class EditArticleForm(forms.ModelForm):
	id = forms.CharField(widget=forms.HiddenInput)

	def __init__(self, *args, **kwargs):
		super(EditArticleForm, self).__init__(*args, **kwargs)
		self.fields['hasBeenRead'].label = "Has been read"
		self.fields['endDate'].label = "End date"
		self.fields['endDate'].required = False
	
	def clean(self):
		cleaned_data = super(EditArticleForm, self).clean()
		article_id = cleaned_data['id']
		try:
			article = Article.objects.get(id=int(article_id))
			endDate = self.cleaned_data['endDate']
			cleaned_data['creationDate'] = article.creationDate
			if ((article.endDate is not None and endDate != article.endDate) or (article.endDate is None)) and endDate is not None and endDate < datetime.date.today():
				self._errors["endDate"] = self.error_class([u"End date cannot be in the past."])					
		except Article.DoesNotExist:
			raise forms.ValidationError(u"Article does not exist.")					

		return cleaned_data

	class Meta:
		model = Article

class DurationAdminForm(forms.ModelForm):
	class Meta:
		model = Duration

	def clean(self):
		cleaned_data = super(DurationAdminForm, self).clean()
		numberDays = cleaned_data.get('numberDays')
		date = cleaned_data.get('date')
		if numberDays is None and date is None:
			raise forms.ValidationError("NumberDays and Date cannot be both empty.")
		return cleaned_data

class SearchForm(forms.Form):
	filterChoices = (ArticleFilters.items())
	filter = forms.ChoiceField(choices=filterChoices)
	urlTitle = forms.CharField(max_length=400, label='Url/Title', required=False)
	paging = forms.CharField(widget=forms.HiddenInput, required=False)

	def clean_filter(self):
		filter_name = self.cleaned_data['filter']
		if filter_name is None:
			raise forms.ValidationError("Filter has not a valid value.")

		if not ArticleFilters.contains(filter_name):
			raise forms.ValidationError("Filter has not a valid value.")

		return filter_name
