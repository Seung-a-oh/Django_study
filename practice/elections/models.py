from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=10)
    intro = models.TextField()
    area = models.CharField(max_length=15)
    party_num = models.IntegerField(default=0)
    
    # str을 오버라이드, 이 클래스를 어떻게 표현할 지
    def __str__(self):
        return self.name    # name을 대표로 나타내라.

class Poll(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    area = models.CharField(max_length=15)

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True)
    votes = models.IntegerField(default=0)


