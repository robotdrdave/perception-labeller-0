import re
import random
from .models import User
from django.http import HttpResponseRedirect

def extract_entity(span, entity):
    locations = [m.start() for m in re.finditer(entity.lower(), span.lower())]
    isolated_span_portions = []
    previous_index = 0
    for entity_mention in locations:
        isolated_span_portions.append(span[previous_index:entity_mention])
        isolated_span_portions.append(span[entity_mention:entity_mention+len(entity)])
        previous_index = entity_mention + len(entity)
    isolated_span_portions.append(span[previous_index:])
    return isolated_span_portions

def select_snippet_to_evaluate(Snippet, Evaluated_Snippet, user):
    snippets = set([s_id.id for s_id in Snippet.objects.all()])
    evaluated_snippets = set([s.snippet.id for s in Evaluated_Snippet.objects.all() if s.evaluator == user])
    return random.choice(list(snippets.difference(evaluated_snippets)))

def validate_user(user_id):
    if user_id not in [user.id for user in User.objects.all()]:
        return HttpResponseRedirect('/accounts/login')
