#!/usr/bin/python
# -*- coding: utf-8 -*-
import collections

from kamu.opinions.models import Question, Option, Answer, \
    VoteOptionCongruence, QuestionSessionRelevance, QuestionSource
from kamu.opinions.views import LAST_QUESTION_KEY
from kamu.votes.models import Party, Session, Member
from kamu.user_voting import models as user_voting
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from django import forms

from django import template
register = template.Library()

@register.inclusion_tag('opinions/promise_statistics_sidebar.html',
                        takes_context=True)
def promise_statistics_sidebar(context, user, question=None):
    get_party_cong = VoteOptionCongruence.objects.get_party_congruences
    parties = list(get_party_cong(for_user=user, for_question=question))
    # If no congruences found for parties, skip the other queries.
    if not parties:
        return {}

    member_type = ContentType.objects.get_for_model(Member)
    member_votes = user_voting.Vote.objects.filter(user=user,
                                                   content_type=member_type)
    members = []
    for vote in member_votes:
        member = Member.objects.get(pk=vote.object_id)
        get_cong = VoteOptionCongruence.objects.get_member_congruence
        member.congruence = get_cong(member, for_user=user, for_question=question)
        if member.congruence is None:
            continue
        members.append(member)

    return dict(parties=parties, members=members, user=user)

@register.filter
def congruence_to_percentage(share):
    if (share is None):
        return _("N/A")
    try:
        return "%i" % int((share+1)/2.0*100)
    except ValueError:
        return ''

@register.inclusion_tag('opinions/match_session.html', takes_context=True)
def match_session(context, session, question=None, delete=False):
    src_list = QuestionSource.objects.all()
    session = context['request'].session
    args = dict(src_list=src_list, session=session, question=question,
                delete=delete)
    if session and LAST_QUESTION_KEY in session:
        act_que = session[LAST_QUESTION_KEY]
        args['active_question'] = act_que
        que = src_list[1].question_set.all()[0]

    return args

