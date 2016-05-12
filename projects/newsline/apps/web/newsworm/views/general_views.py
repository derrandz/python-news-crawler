from django.shortcuts import render

# Here goes the general views.
# Specific use views are listed below ./views directory

def home(request):
	return render(request, "home.html", {})
