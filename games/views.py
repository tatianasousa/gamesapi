"""
Book: Building RESTful Python Web Services
Chapter 2: Working with class based views and hyperlinked APIs in Django
Author: Gaston C. Hillar - Twitter.com/gastonhillar
Publisher: Packt Publishing Ltd. - http://www.packtpub.com
"""
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Game
from games.serializers import GameSerializer

@api_view(['GET', 'POST'])
def game_list(request):

    games = Game.objects.all()
    games_serializer = GameSerializer(games, many=True)
    tam = len(games_serializer.data)

    nomes = []
    i = tam - 1
    for nome in games_serializer.data:
        nome = games_serializer.data[i]['name']
        nomes.append(nome)
        i = i - 1

    if request.method == 'GET':
        
        return Response(games_serializer.data)
    elif request.method == 'POST':
        game_serializer = GameSerializer(data=request.data)
        if game_serializer.is_valid():
            if (game_serializer.validated_data['name'] in nomes):
                return Response("O Jogo já existe!")
            
            game_serializer.save()
            return Response(game_serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

@api_view(['GET', 'PUT', 'DELETE'])
def game_detail(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    games = Game.objects.all()
    games_serializer = GameSerializer(games, many=True)
    tam = len(games_serializer.data)

    nomes = []
    i = tam - 1
    for nome in games_serializer.data:
        nome = games_serializer.data[i]['name']
        nomes.append(nome)
        i = i - 1

    if request.method == 'GET':
        game_serializer = GameSerializer(game)
        return Response(game_serializer.data)
    elif request.method == 'PUT':
        game_serializer = GameSerializer(game, data=request.data)
        if game_serializer.is_valid():
            if (game_serializer.validated_data['name'] in nomes):
                return Response("Já existe jogo com esse nome!")
            game_serializer.save()
            return Response(game_serializer.data)
        return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if game.played == True:
            return Response("O jogo não pode ser excluído!")
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)