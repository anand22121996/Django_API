from django.shortcuts import render
from .models import Article
from .serializers import ArticleSerializer
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication,TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.

# Generic APIViews
# List & Create - PK not required
class LCArticleAPI(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, 
                    mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    #authentication_classes = [TokenAuthentication]
    authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    def get(self, request, *args, **kwargs):
        return self.list(request,*args, **kwargs)

    def post(self, request,*args, **kwargs):
        return self.create(request,*args, **kwargs)

#Retrieve Update & Delete - PK required
class RUDArticleAPI(generics.GenericAPIView, mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, mixins.DestroyModelMixin):   
    #authentication_classes = [TokenAuthentication]
    authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]


    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request,*args, **kwargs)
    
    def put(self, request,*args, **kwargs):
        return self.update(request,*args, **kwargs)
    
    def delete(self, request,*args, **kwargs):
        return self.destroy(request,*args, **kwargs)

# Class based apiview
class ArticleAPIView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

class ArticleDetail(APIView):
    def get_object(self,id):
        try:
            return Article.objects.get(id=id)
        
        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    def put(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# function based apiview
@api_view(['POST','GET'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT','GET','DELETE'])
def article_detail(request,pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)