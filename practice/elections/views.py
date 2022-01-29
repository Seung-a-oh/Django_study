from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .models import Candidate, Poll, Choice
import datetime
from django.db.models import Sum

def index(request):
    # db에서 후보들을 불러온 다음에,
    candidates = Candidate.objects.all()
    # str = ''
    # for candidate in candidates:
    #     str += "<p>{} 기호 {}번({})<br>".format(candidate.name,
    #         candidate.party_num, 
    #         candidate.area)
    #     str += candidate.intro+"</p>"

    # return HttpResponse(str)

    # 그걸 context에 넣어서 
    context = {'candidates':candidates}
    # html 파일로 전달하기
    return render(request, 'elections/index.html', context)


def candidates(request, name):
    candidate = get_object_or_404(Candidate, name=name)
    # try:
    #     candidate = Candidate.objects.get(name = name)
    # except:
    #     raise Http404
    return HttpResponse(candidate.name)

def areas(request, area):
    today = datetime.datetime.now()

    try:
        poll = Poll.objects.get(area = area, 
                start_date__lte=today,  # 투표 기간이 현재 시점보다 이른가
                end_date__gte=today)    # 투표 마감이 현재 시간보다 늦은가 
        candidates = Candidate.objects.filter(area = area) # 앞 area는 candidate, 뒤는 매개변수

    except:
        poll=None
        candidates=None

    # area가 같은 값만 필터링해서 가져와라
    context = {'candidates':candidates,
            'area': area,
            'poll': poll}
    return render(request, 'elections/area.html', context)


def polls(request, poll_id):
    # pk = primary key
    # 받아온 poll_id로 poll객체 불러오기
    poll = Poll.objects.get(pk = poll_id)
    selection = request.POST['choice']

    try: 
        choice = Choice.objects.get(poll_id = poll_id, candidate_id = selection)
        choice.votes += 1
        choice.save()
    except:
        #최초로 투표하는 경우, DB에 저장된 Choice객체가 없기 때문에 Choice를 새로 생성합니다
        choice = Choice(poll_id = poll_id, candidate_id = selection, votes = 1)
        choice.save()
    
    return HttpResponseRedirect("/areas/{}/results".format(poll.area))

def results(request, area):
    candidates = Candidate.objects.filter(area=area)
    polls = Poll.objects.filter(area=area)
    poll_results = []

    for poll in polls:
        result = {}
        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date

        total_votes = Choice.objects.filter(poll_id=poll.id).aggregate(Sum('votes'))
        result['total_votes'] = total_votes['votes__sum']

        rates = []
        for candidate in candidates:
            try:
                choice = Choice.objects.get(poll = poll, candidate = candidate)
                rates.append(round(choice.votes * 100/result['total_votes'], 1))
            except:
                rates.append(0)
        result['rates'] = rates
        poll_results.append(result)
    
    context = {'candidates':candidates, 'area':area, 'poll_results':poll_results}

    return render(request, 'elections/result.html', context)