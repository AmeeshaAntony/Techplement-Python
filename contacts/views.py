from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from .forms import ContactForm
from django.contrib import messages


def home(request):
    return render(request, 'contacts/index.html')
# View to list all contacts
def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, 'contacts/contact_list.html', {'contacts': contacts})

# View to add a new contact
def add_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')  # Assuming you have an email field
        
        try:
            contact = Contact(name=name, phone=phone, email=email)
            contact.save()
            messages.success(request, 'Contact added successfully!')
            return redirect('home')
        except IntegrityError:
            messages.error(request, 'A contact with this email already exists.')
            return render(request, 'contacts/add_contact.html')

    return render(request, 'contacts/add_contact.html')
# View to update an existing contact
def update_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact updated successfully.')
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/update_contact.html', {'form': form})

# View to delete a contact
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact deleted successfully.')
        return redirect('contact_list')
    return render(request, 'contacts/delete_contact.html', {'contact': contact})

def contact_list(request):
    # Use 'contacts/base.html' if needed for Django to find it
    return render(request, 'contacts/base.html')  

def search_contact(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Contact.objects.filter(name__icontains=query) 
    return render(request, 'contacts/search.html', {'results': results, 'query': query})