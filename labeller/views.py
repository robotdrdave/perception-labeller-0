from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
import requests
import random

from .models import Snippet, Evaluated_Snippet, User
from .forms import SpamForm, YNForm, OpinionForm, FactForm, ProductForm
from .utils import extract_entity, select_snippet_to_evaluate, validate_user


def spam(request):
    validate_user(request.user.id)

    if request.method == 'POST':
        spam_form = SpamForm(request.POST)
        if spam_form.is_valid():
            snippet_to_evaluate = request.session.get('context')['snippet_to_evaluate']
            if spam_form.data['field'] == 'True':
                Evaluated_Snippet(evaluator = request.user,
                snippet = Snippet.objects.get(id=snippet_to_evaluate),
                is_harmful = False,
                is_opinion = False,
                is_fact = False,
                extracted_span = '',
                is_spam = True).save()
                return HttpResponseRedirect('/spam/')

            else:
                current_snippet = Evaluated_Snippet(evaluator = request.user,
                snippet = Snippet.objects.get(id=snippet_to_evaluate),
                is_harmful = False,
                is_opinion = False,
                is_fact = False,
                extracted_span = '',
                is_spam = False)
                current_snippet.save()
                request.session['current_snippet_id'] = current_snippet.id
                f = open("context.txt", "a")
                f.write('\n' + str(request.session.get('context')))
                f.close()
                return HttpResponseRedirect('/harmful/')
    else:
        try:
            snippet_to_evaluate = select_snippet_to_evaluate(Snippet, Evaluated_Snippet, request.user)
        except:
            return HttpResponseRedirect('/out_of_samples/')

        span_portions = extract_entity(Snippet.objects.get(id=snippet_to_evaluate).text, 
                                    Snippet.objects.get(id=snippet_to_evaluate).entity)

        context = {'entity': Snippet.objects.get(id=snippet_to_evaluate).entity,
               'span_portions': span_portions}

        request.session['context'] = {'entity': Snippet.objects.get(id=snippet_to_evaluate).entity,
                                    'span_portions': span_portions, 'snippet_to_evaluate': snippet_to_evaluate}
        spam_form = SpamForm()
        context['spam_form'] = spam_form 
        return render(request, "spam.html", context)

def harmful(request): 
    validate_user(request.user.id)
    
    context = request.session.get('context')
    f = open("context.txt", "a")
    f.write('\n' + str(context))
    f.close()
    current_snippet = Evaluated_Snippet.objects.get(id=request.session.get('current_snippet_id'))

    if request.method == 'POST':
        harm_form = YNForm(request.POST)
        context['harm_form'] = harm_form
        if harm_form.is_valid():
            if harm_form.data['field'] == 'True':
                current_snippet.is_harmful = True
                current_snippet.save()
            
            else:
                current_snippet.is_harmful = False
                current_snippet.save()
            
            return HttpResponseRedirect('/opinion/')

    else:
        harm_form = YNForm()
        context['harm_form'] = harm_form
        return render(request, "harmful.html", context)

def opinion(request):

    validate_user(request.user.id)

    context = request.session.get('context')
    current_snippet = Evaluated_Snippet.objects.get(id=request.session.get('current_snippet_id'))
    
    if request.method == 'POST':
        text_form = OpinionForm(request.POST)
        context['text_form'] = text_form
        if text_form.is_valid():
            if text_form.data['yn_field'] == 'True':
                current_snippet.is_opinion = True
                current_snippet.extracted_span = text_form.data['text_field']
                current_snippet.save()
                return HttpResponseRedirect('/spam/')

            else:
                current_snippet.is_opinion = False
                current_snippet.save()
                return HttpResponseRedirect('/fact/')

    else:
        text_form = OpinionForm()
        context['text_form'] = text_form
        return render(request, "opinion.html", context)

def fact(request):

    validate_user(request.user.id)

    context = request.session.get('context')
    current_snippet = Evaluated_Snippet.objects.get(id=request.session.get('current_snippet_id'))

    if request.method == 'POST':
        text_form = FactForm(request.POST)
        context['text_form'] = text_form
        if text_form.is_valid():
            if text_form.data['yn_field'] == 'True':
                current_snippet.is_fact = True
                current_snippet.extracted_span = text_form.data['text_field']
                current_snippet.save()
                return HttpResponseRedirect('/spam/')

            else:
                current_snippet.is_fact = False
                current_snippet.save()
                return HttpResponseRedirect('/product_mention/')

    else:
        text_form = FactForm()
        context['text_form'] = text_form
        return render(request, "fact.html", context)

def product_mention(request):

    validate_user(request.user.id)

    context = request.session.get('context')
    current_snippet = Evaluated_Snippet.objects.get(id=request.session.get('current_snippet_id'))

    if request.method == 'POST':
        text_form = ProductForm(request.POST)
        context['text_form'] = text_form
        if text_form.is_valid():
            if text_form.data['yn_field'] == 'True':
                current_snippet.product_mention = True
                current_snippet.extracted_span = text_form.data['text_field']
                current_snippet.save()
            
            else:
                current_snippet.product_mention = False
                current_snippet.save()

            return HttpResponseRedirect('/spam/')

    else:
        text_form = ProductForm()
        context['text_form'] = text_form
        return render(request, "product_mention.html", context)

def out_of_samples(request):

    validate_user(request.user.id)

    try:
        select_snippet_to_evaluate(Snippet, Evaluated_Snippet, request.user)
        return render(request, "spam.html")
    except:
        return render(request, "out_of_samples.html")