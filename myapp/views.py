from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.http import HttpResponse
import openai
# Create your views here.

OPENAI_API_KEY = "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"

def generate_response(request):
  # Create an OpenAI client
  print("hi")
  openai.api_key = OPENAI_API_KEY

  # Get the prompt from the request
  prompt = request.POST.get("prompt")

  # Send a request to the OpenAI API to generate a response
  response = openai.Completion.create(
    prompt=prompt,
    model="text-davinci-002",
    max_tokens=1024,
  )

  # Get the generated response from the OpenAI API
  generated_response = response.choices[0].text

  # Return the generated response as a JSON object
  return JsonResponse({"response": generated_response})

def index(request):
    return render(request,'index.html')

def fun404(request):
    return render(request, '404.html')

def about(request):
    return render(request, 'about.html')

def category(request):
    return render(request, 'category.html')

def contact(request):
    return render(request, 'contact.html')

def jobdetail(request):
    return render(request,'job-detail.html')

def joblist(request):
    return render(request,'job-list.html')

def testimonial(request):
    return render(request,'testimonial.html')

def chat(request):
    return render(request,'chat.html')

def resume(request):
    return render(request,"resume.html")

def login(request):
    return render(request,"login.html")