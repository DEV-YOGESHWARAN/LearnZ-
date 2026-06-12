from django.shortcuts import render

def index(request):
    """Serve the main frontend application"""
    return render(request, 'index.html')

def chat(request):
    """Serve the chat interface"""
    return render(request, 'chat.html')