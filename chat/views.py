from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from channels.layers import get_channel_layer
from chat.models import *

channel_layer = get_channel_layer()
# Create your views here.


def index(request):
   
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


from asgiref.sync import sync_to_async

@sync_to_async
def dbQueries():

    data = users.objects.all().values('id','name')
    finalarray = list()
    for j in data:
        finalarray.append({'id':j['id'],'name':j['name']})
    
    return finalarray



async def trigger(request):
   
    data = await dbQueries()

    await channel_layer.group_send("notification_hey", {
        "type":"notification_message",
        "message":"hello safdar",
        "data":data

    })
    return JsonResponse({'status':True,'message':"trigger"})
