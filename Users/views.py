from django.shortcuts import render

# Create your views here.


from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.views import APIView
from Users.serializers import UserSerializer, GroupSerializer
from rest_framework.response import Response
from django.http import Http404, HttpResponse, JsonResponse
import json
from Users.delegatealloc import *

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class DelegateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class DelegateAlloc(APIView):

    def post(self, request):
        pollData = request.data
        print pollData
        delegateResults = self.delegate_alloc(pollData)
        #jsonResult = json.loads(delegateResults)
        return JsonResponse(delegateResults, safe=False)

    def get(self, request):
        return JsonResponse("Delegate GET response", safe=False)

    def delegate_alloc(self, allPolls):
        votes = Delegates()
        delswon=[]
        for state in statemap:
            if state in allPolls:
                state_polls={}
                for loc in allPolls:   # can be either state (VA) or CD, ie MNCD3
                    if state in loc:
                        state_polls[loc]=allPolls[loc]
                # print state, delegaterule[state]
                # find all the polls matching StateCD
                delswon.append(votes.alloc_delegates(state, delegaterule[state], allPolls[state],
                                delegatecdrule[state],  state_polls))
            print "done with", state
        '''
        Sum = {i:0 for i in cand_list}
        for stateres in delswon:
            for result in stateres:
                for cand in stateres[result]:
                    Sum[cand] += int(stateres[result][cand])
        '''
        print delswon
        #print "SEC primary result total:", Sum
        return delswon
