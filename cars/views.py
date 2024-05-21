from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, View, TemplateView

from .forms import CustomerForm, LicensePlateInlineFormSet
from .models import Customer


class HomePageView(TemplateView):
    template_name = 'home_template.html'


class ListPlatesView(ListView):
    model = Customer
    template_name = 'list_plates.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return Customer.objects.prefetch_related('license_plates')


class CreateCustomerView(View):
    template_name = 'add_plates.html'

    def get(self, request, *args, **kwargs):
        customer_form = CustomerForm()
        license_plate_formset = LicensePlateInlineFormSet(prefix='plates')
        return render(request, self.template_name, {
            'customer_form': customer_form,
            'license_plate_formset': license_plate_formset
        })

    def post(self, request, *args, **kwargs):
        license_plate_formset = LicensePlateInlineFormSet(
            request.POST, prefix='plates')
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            email = customer_form.cleaned_data['email']
            customer, created = Customer.objects.get_or_create(email=email)
            license_plate_formset = LicensePlateInlineFormSet(
                request.POST, instance=customer, prefix='plates')
            if license_plate_formset.is_valid():
                license_plate_formset.save()
                messages.success(
                    request,
                    'Customer and license plates created successfully.' if created else 'Customer already exists, updated customer license plates.'
                )
                return redirect(reverse_lazy('add_plate'))
            else:
                error_messages = [
                    messages.error(request, value) for obj in license_plate_formset.errors for key, value in obj.items()
                ]
        else:
            messages.error(request, 'Email is not valid.')

        return render(request, self.template_name, {
            'customer_form': customer_form,
            'license_plate_formset': license_plate_formset
        })


class UpdateCustomerView(UpdateView):
    model = Customer
    template_name = 'edit_customer.html'
    form_class = LicensePlateInlineFormSet

    def get_customer(self):
        return get_object_or_404(Customer, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_customer()
        context['customer'] = customer

        if self.request.POST:
            context['license_plate_formset'] = LicensePlateInlineFormSet(
                self.request.POST,
                instance=customer,
                prefix='plates'
            )
        else:
            context['license_plate_formset'] = LicensePlateInlineFormSet(
                instance=customer, prefix='plates')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        license_plate_formset = context['license_plate_formset']
        if license_plate_formset.is_valid():
            license_plate_formset.instance = self.object
            license_plate_formset.save()
            messages.success(
                self.request,
                'License plates updated successfully.'
            )
            return redirect(reverse_lazy('edit_customer', kwargs={'pk': self.object.pk}))
        else:
            error_messages = [
                messages.error(request, value) for obj in license_plate_formset.errors for key, value in obj.items()
            ]
            return self.render_to_response(self.get_context_data(form=license_plate_formset))
