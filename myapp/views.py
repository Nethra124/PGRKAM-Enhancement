from django.contrib.auth import authenticate,logout,get_user_model
from django.contrib.auth import login as lg
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
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
    if request.user.is_authenticated:
        return render(request,'index.html')
    return render(request,'index1.html')

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
    if request.method=="POST":
        try:
            request.POST["name"]
            User=get_user_model()
            user=User.objects.create_user(username=request.POST["email"].lower(),password=request.POST["pass"])
            user.save()
            user.email=request.POST["email"].lower()
            user.first_name=request.POST["name"]
            user.save()
            user=authenticate(username=request.POST["Username"].lower(),password=request.POST["Password1"])
            lg(request,user)
            return HttpResponseRedirect(reverse("index"))
        except:
            if(request.POST['email']=="" or request.POST['pass']==""):
                return render(request,"login2.html",{
                    "message": "Please enter your credentials"
                })
            user=authenticate(username=request.POST['email'],password=request.POST['pass'])
            if user:
                lg(request,user)
                return HttpResponseRedirect(reverse("index"))
            else:
                
                return render(request,"login2.html",{
                    "message": "Wrong credentials, retry!"
                })
    return render(request,"login.html")

def resume1(request):
    return render(request, "resume1.html")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def profile2(request):
    return render(request,"profile2.html")

def edit_profile(request):
    return render(request,"edit_profile.html")

def resumeanalysis(request):
    return render(request,"resumeanalysis.html")

