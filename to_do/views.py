from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse

# Create your views here.

def index(request):
	if "to_do" not in request.session:

		# create new list
		request.session["to_do"] = []

	return render(request, "to_do/index.html", {
		"to_do": request.session["to_do"]
		})

def add_task(request):

	# check if method is post
	if request.method == "POST":

		# take data from form and save as form
		form = AddTaskForm(request.POST)

		# check if form is valid
		if form.is_valid():

			# isolate the individual inputs 
			task = form.cleaned_data["task"]

			# add task to list of task
			request.session["to_do"] += [task]

			# return user to list of task
			return HttpResponseRedirect(reverse("index"))

		else:
			# if form invalid, re-render to existing page
			return render(request, "to_do/add_task.html", {
				"form": form
				})

	return render(request, "to_do/add_task.html", {
		"form" : AddTaskForm()
		})




class AddTaskForm(forms.Form):
	task = forms.CharField(
		label="New Task",
		min_length=1,)
	start_date = forms.DateField(
		label="Start Date", 
		input_formats=['%Y-%m-%d'], 
		error_messages={'invalid': "Please enter in format YYYY-MM-DD"})
	end_date = forms.DateField(
		label="End Date",
		input_formats=['%Y-%m-%d'],
		error_messages={'invalid': "Please enter in format YYYY-MM-DD"})
	description = forms.CharField(
		label="Task Description",
		required=False)
