from django.shortcuts import render
from django.http import HttpResponse
from .models import Candidate, Poll, Choice
import datetime

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

def areas(request, area):
    today = datetime.datetime.now()

    try:
        poll = Poll.objects.get(area = area, 
        start_date__lte=today,  # 투표 기간이 현재 시점보다 이른가
        end_date__gte=today)    # 투표 마감이 현재 시간보다 늦은가 
    except:
        poll=None
        candidate=None

    # area가 같은 값만 필터링해서 가져와라
    candidate = Candidate.objects.filter(area = area) # 앞 area는 candidate, 뒤는 매개변수
    context = {'candidates':candidate,
    'area': area,
    'poll': poll}
    return render(request, 'elections/area.html', context)

def polls(request, poll_id):
    # pk = primary key
    poll = Poll.objects.get(pk = poll_id)
    selection = request.POST['choice']

    try: 
        choice = Choice.objects.get(poll_id = poll.id, candidate_id = selection)
        choice.votes += 1
        choice.save()
    except:
        #최초로 투표하는 경우, DB에 저장된 Choice객체가 없기 때문에 Choice를 새로 생성합니다
        choice = Choice(poll_id = poll.id, candidate_id = selection, votes = 1)
        choice.save()
    
    return HttpResponse(selection)

# def polls(request, poll):
#     poll2 = Poll.objects.get(pk = poll)
#     selection = request.POST['choice']

#     try: 
#         choice = Choice.objects.get(poll = poll2, candidate = selection)
#         choice.votes += 1
#         choice.save()
#     except:
#         #최초로 투표하는 경우, DB에 저장된 Choice객체가 없기 때문에 Choice를 새로 생성합니다
#         choice = Choice(poll = poll2, candidate = selection, votes = 1)
#         choice.save()
    
#     return HttpResponse(selection)