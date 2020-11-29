from collections import OrderedDict
from django.db.models import Max
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
import random

from finitelycomputable.idtrust_django.models import (
        Interaction, Exchange, Strategy, deviation,
)

def trust_list_display(trust_list):
    return ", ".join(["Trust" if t else "Distrust" for t in trust_list])

def home(request):
    if request.method != 'POST':
        return render(request, 'id_trust/interaction_begin.html', {})
    try:
        user_miscommunication = float(request.POST.get('user_miscommunication'))
    except (ValueError, TypeError):
        user_miscommunication = 0.0
    try:
        foil_miscommunication = float(request.POST.get('foil_miscommunication'))
    except (ValueError, TypeError):
        foil_miscommunication = 0.0
    obj = Interaction.objects.create(
        foil_strategy=random.choice(Strategy.choices)[0],
        user_miscommunication=user_miscommunication,
        foil_miscommunication=foil_miscommunication,
    )
    interact_core(request, obj.pk)
    return redirect(obj)


def effect(intent, miscommunication):
    return intent ^ bool(miscommunication > random.random())


def interact_core(request, pk):
    from django.shortcuts import get_object_or_404
    interaction = get_object_or_404(Interaction, pk=pk)
    foil_intent = Strategy.impl(interaction.foil_strategy)(
            [e.user_effect for e in interaction.exchange_set.all()])
    user_intent = request.POST.get('user_intent')
    if user_intent == 'Trust':
        user_intent = True
    elif user_intent == 'Distrust':
        user_intent = False
    if user_intent in [True, False]:
        interaction.exchange_set.create(
            user_intent=user_intent,
            user_effect=effect(user_intent, interaction.user_miscommunication),
            foil_intent=foil_intent,
            foil_effect=effect(foil_intent, interaction.foil_miscommunication),
        )
    user_guess = request.POST.get('user_guess')
    if user_guess:
        interaction.user_guess = user_guess
        interaction.save()
    user_intent = [j.user_intent for j in interaction.exchange_set.all()]
    user_effect = [j.user_effect for j in interaction.exchange_set.all()]
    foil_intent = [j.foil_intent for j in interaction.exchange_set.all()]
    foil_effect = [j.foil_effect for j in interaction.exchange_set.all()]
    strategy_lists = OrderedDict()
    if len(user_intent):
        for (k, v) in Strategy.choices:
            st = Strategy.impl(k)
            strategy_lists[v] = [deviation(user_intent, foil_intent, st)]
            strategy_lists[v].append(deviation(foil_intent, user_intent, st))
    s_results = [
            "%s: (foil %.1f) (user %.1f)" %
            (k, v[0], v[1]) for (k, v) in strategy_lists.items()]
    score = interaction.score()
    return {
        'interaction': interaction,
        'score': score,
        'user_intent': trust_list_display(user_intent),
        'user_effect': trust_list_display(user_effect),
        'foil_effect': trust_list_display(foil_effect),
        'foil_intent': trust_list_display(foil_intent),
        's_results': s_results,
        'strategies': Strategy,
    }

def interact(request, pk):
    return render(request, 'id_trust/interaction.html',
        interact_core(request, pk))


class ExchangeCreate(CreateView):
    model = Exchange
    fields = ['interaction', 'user_intent']
    template_name = "id_trust/exchange_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context

    def form_valid(self, form):
        interaction = form.instance.interaction
        form.instance.foil_trust = Strategy.impl(
            form.instance.interaction.foil_strategy)(
            [e.user_intent for e in interaction.exchange_set.all()]
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('id_trust:interact',
                       kwargs={'pk': self.object.interaction_id})


class Home(CreateView):
    model = Exchange
    fields = ['user_intent']
    template_name = "id_trust/interaction_begin.html"

    def form_valid(self, form):
        interaction = form.instance.interaction = Interaction.objects.create(
            foil_strategy = random.choice(Strategy.choices)[0]
        )
        form.instance.foil_trust = Strategy.impl(interaction.foil_strategy)(
            [e.user_intent for e in interaction.exchange_set.all()]
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('id_trust:interact',
                       kwargs={'pk': self.object.interaction_id})


class Interact(DetailView):
    template_name = 'id_trust/interaction.html'
    fields = ['choice']
    model = Interaction

    def get_context_data(self, **kwargs):
        context = super(Interact, self).get_context_data(**kwargs)
        context.update(interact_core(self.request, self.object.pk, True))
        return context
