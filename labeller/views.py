from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout as django_logout
from django.contrib.auth.decorators import login_required
import requests
import random

from .models import Snippet, Evaluated_Snippet, User
from .forms import SpamForm, YNForm, OpinionForm, Y_OpinionForm, FactForm, Y_FactForm, ProductForm, Y_ProductForm
from .utils import extract_entity, select_snippet_to_evaluate, validate_user, get_inventory_info, delete_previous_label

@login_required
def spam(request):
    validate_user(request.user.id)

    if request.method == 'POST':
        if 'correction_spam' in request.POST:
            return delete_previous_label(Evaluated_Snippet, request.user, 'spam')
        else:
            spam_form = SpamForm(request.POST)
            if spam_form.is_valid():
                snippet_to_evaluate = request.session.get('context')['snippet_to_evaluate']
                if spam_form.data['field'] == 'True':
                    current_snippet = Evaluated_Snippet(evaluator = request.user,
                    snippet = Snippet.objects.get(id=snippet_to_evaluate),
                    entity = Snippet.objects.get(id=snippet_to_evaluate).entity,
                    extracted_span = '',
                    is_spam = True)
                    current_snippet.save()
                    return HttpResponseRedirect('/spam/')

                else:
                    return HttpResponseRedirect('/opinion/')
    else:
        try:
            snippet_to_evaluate = select_snippet_to_evaluate(Snippet, Evaluated_Snippet, request.user)
        except:
            return HttpResponseRedirect('/out_of_samples/')

        span_portions = extract_entity(Snippet.objects.get(id=snippet_to_evaluate).text, 
                                    Snippet.objects.get(id=snippet_to_evaluate).entity)

        
        total_spans, labelled_span_count = get_inventory_info(Snippet, Evaluated_Snippet, request.user)

        context = {'entity': Snippet.objects.get(id=snippet_to_evaluate).entity,
               'span_portions': span_portions,
               'current_count': labelled_span_count, 'total_snippets': total_spans}

        request.session['context'] = {'entity': Snippet.objects.get(id=snippet_to_evaluate).entity,
                                    'span_portions': span_portions, 'snippet_to_evaluate': snippet_to_evaluate,
                                    'current_count': labelled_span_count, 'total_snippets': total_spans}
        spam_form = SpamForm()
        context['spam_form'] = spam_form 
        return render(request, "spam.html", context)

@login_required
def opinion(request):

    validate_user(request.user.id)

    context = request.session.get('context')
    snippet_to_evaluate = request.session.get('context')['snippet_to_evaluate']
    
    if request.method == 'POST':
        if 'correction_opinion' in request.POST:
            f = open("context.txt", "a")
            f.write("\nHere")
            f.close()
            return delete_previous_label(Evaluated_Snippet, request.user, 'opinion')
        else:
            text_form = OpinionForm(request.POST)
            context['text_form'] = text_form
            if text_form.is_valid():
                if (text_form.data['yn_field'] == 'True') and (len(text_form.data['text_field']) > 0):
                    current_snippet = Evaluated_Snippet(evaluator = request.user,
                    snippet = Snippet.objects.get(id=snippet_to_evaluate),
                    entity = Snippet.objects.get(id=snippet_to_evaluate).entity,
                    is_opinion = True,
                    extracted_span = text_form.data['text_field'])
                    current_snippet.save()
                    return HttpResponseRedirect('/spam/')

                elif text_form.data['yn_field'] == 'False':
                    return HttpResponseRedirect('/fact/')

                else:
                    text_form = Y_OpinionForm()
                    context['text_form'] = text_form
                    return render(request, "opinion.html", context)

    else:
        text_form = OpinionForm()
        context['text_form'] = text_form
        return render(request, "opinion.html", context)

@login_required
def fact(request):

    validate_user(request.user.id)

    context = request.session.get('context')
    snippet_to_evaluate = request.session.get('context')['snippet_to_evaluate']

    if request.method == 'POST':
        if 'correction_fact' in request.POST:
            return delete_previous_label(Evaluated_Snippet, request.user, 'fact')
        else:
            text_form = FactForm(request.POST)
            context['text_form'] = text_form
            if text_form.is_valid():
                if (text_form.data['yn_field'] == 'True') and (len(text_form.data['text_field']) > 0):
                    current_snippet = Evaluated_Snippet(evaluator = request.user,
                    snippet = Snippet.objects.get(id=snippet_to_evaluate),
                    entity = Snippet.objects.get(id=snippet_to_evaluate).entity,
                    is_fact = True,
                    extracted_span = text_form.data['text_field'])
                    current_snippet.save()
                    return HttpResponseRedirect('/spam/')

                elif text_form.data['yn_field'] == 'False':
                    return HttpResponseRedirect('/product_mention/')
                else:
                    text_form = Y_FactForm()
                    context['text_form'] = text_form
                    return render(request, "fact.html", context)

    else:
        text_form = FactForm()
        context['text_form'] = text_form
        return render(request, "fact.html", context)

@login_required
def product_mention(request):

    validate_user(request.user.id)

    context = request.session.get('context')
    snippet_to_evaluate = request.session.get('context')['snippet_to_evaluate']

    if request.method == 'POST':
        if 'correction_product_mention' in request.POST:
            return delete_previous_label(Evaluated_Snippet, request.user, 'product_mention')
        else:
            text_form = ProductForm(request.POST)
            context['text_form'] = text_form
            if text_form.is_valid():
                if (text_form.data['yn_field'] == 'True') and (len(text_form.data['text_field']) > 0):
                    current_snippet = Evaluated_Snippet(evaluator = request.user,
                    snippet = Snippet.objects.get(id=snippet_to_evaluate),
                    entity = Snippet.objects.get(id=snippet_to_evaluate).entity,
                    product_mention = True,
                    extracted_span = text_form.data['text_field'])
                    current_snippet.save()
                    return HttpResponseRedirect('/spam/')
            
                elif text_form.data['yn_field'] == 'False':
                    current_snippet = Evaluated_Snippet(evaluator = request.user,
                    snippet = Snippet.objects.get(id=snippet_to_evaluate),
                    entity = Snippet.objects.get(id=snippet_to_evaluate).entity)
                    current_snippet.save()
                    return HttpResponseRedirect('/spam/')
                else:
                    text_form = Y_ProductForm()
                    context['text_form'] = text_form
                    return render(request, "product_mention.html", context)    

    else:
        text_form = ProductForm()
        context['text_form'] = text_form
        return render(request, "product_mention.html", context)

@login_required
def out_of_samples(request):

    validate_user(request.user.id)

    try:
        select_snippet_to_evaluate(Snippet, Evaluated_Snippet, request.user)
        return render(request, "spam.html")
    except:
        if request.method == 'POST':
            return delete_previous_label(Evaluated_Snippet, request.user, 'out_of_samples')
        else:
            return render(request, "out_of_samples.html")

@login_required
def logout(request):
    django_logout (request)
    return render(request, "logout.html")