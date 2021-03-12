from rest_framework.views import APIView
from rest_framework import viewsets, filters
from api import models, permissions, forms
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from jsonfield import JSONField
#from text_classification.predict_text import predict
from threading import Thread 
from rest_framework.authtoken.models import Token
#from image_classification.predict_image import classify_image
from Pcos.pcos_predict import predict_PCOS

class StartThread(Thread):
    def __init__(self, group = None, target = None, name = None, args = (), kwargs = {}, Verbose = None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self):
        Thread.join(self)
        return self._return

class DeveloperProfileViewSet(viewsets.ModelViewSet):
    serializer_class = forms.DeveloperProfileForm
    queryset = models.DeveloperProfile.objects.all()
    permission_classes = (permissions.UpdateDeveloperProfile,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_backends = ('name', 'email', 'organisation')
    def perform_create(self, form):
        form.save()
    def make_create(self, request):
        form = self.serializer_class(data = request.data, context={'request': request})
        if form.is_valid():
            email = form.validated_data['email']
            name = form.validated_data['name']
            organisation = form.validated_data['organisation']
            t1 = StartThread(target = self.perform_create, args = (form,))
            t1.setDaemon(True)
            t1.start()
            return Response({
                'message': "New user is sucessfully created",
                'email': email,
                'name': name,
                'organisation': organisation
            })
        else:
            return Response(
                form.errors,
                status = status.HTTP_400_BAD_REQUEST,
            )
    def create(self, request):
        t = StartThread(target = self.make_create, args = (request,))
        t.setDaemon(True)
        t.start()
        new_response = t.join()
        return new_response

class DeveloperLoginApiView(ObtainAuthToken):
    serializer_class = forms.AccessTokenForm
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    def make_post(self, request):
        form = self.serializer_class(data = request.data, context={'request': request})
        if form.is_valid():
            developer = form.validated_data['user']
            token, check = Token.objects.get_or_create(user = developer)
            return Response({
                'token': token.key,
                'is_staff': developer.is_staff,
                'first_time_generated': check 
            })
        else:
            return Response(
                form.errors,
                status = status.HTTP_400_BAD_REQUEST,
            )
    def post(self, request):
        t = StartThread(target = self.make_post, args = (request,))
        t.setDaemon(True)
        t.start()
        new_response = t.join()
        return new_response

class PCOSViewSet(viewsets.ModelViewSet):
    serializer_class = forms.PCOSForm
    queryset = models.PCOSModel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnReport, IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_backends = ('timing', 'developer_profile', "age", "Chin", "Cheeks", "Lips", "Breast", "Arms", "Thigh", "Exercise", "Eat", "PCOS", "BMI", "Weight", "Period", "Concieve", "Skin", "Hairthin", "Patch", "Tired", "Mood", "Can", "City")

    def perform_create(self, form, report = None):
        form.save(developer_profile = self.request.user, report = report)

    def make_create(self, request):
        form = self.serializer_class(data = request.data)
        if form.is_valid():
            age = form.validated_data["age"]
            Chin = form.validated_data["Chin"]
            Cheeks = form.validated_data["Cheeks"]
            Lips = form.validated_data["Lips"]
            Breast = form.validated_data["Breast"]
            Arms = form.validated_data["Arms"]
            Thigh = form.validated_data["Thigh"]
            Exercise = form.validated_data["Exercise"]
            Eat = form.validated_data["Eat"]
            PCOS = form.validated_data["PCOS"]
            BMI = form.validated_data["BMI"]
            Weight = form.validated_data["Weight"]
            Period = form.validated_data["Period"]
            Concieve = form.validated_data["Concieve"]
            Skin = form.validated_data["Skin"]
            Hairthin = form.validated_data["Hairthin"]
            Patch = form.validated_data["Patch"]
            Tired = form.validated_data["Tired"]
            Mood = form.validated_data["Mood"]
            Can = form.validated_data["Can"]
            City = form.validated_data["City"]
            #t1 = StartThread(target = predict, args = (data,))
            #t1.setDaemon(True)
            #t1.start()
            report = predict_PCOS(age,Chin,Cheeks,Lips,Breast,Arms,Thigh,Exercise,Eat,PCOS,BMI,Weight,Period,Concieve,Skin,Hairthin,Patch,Tired,Mood,Can,City)
            t2 = StartThread(target = self.perform_create, args = (form, report,))
            t2.setDaemon(True)
            t2.start()
            return Response({'report': report})
        else:
            return Response(
                form.errors,
                status = status.HTTP_400_BAD_REQUEST,
            )
    def create(self, request):
        t = StartThread(target = self.make_create, args = (request,))
        t.setDaemon(True)
        t.start()
        new_response = t.join()
        return new_response
        
# class ImageReportViewSet(viewsets.ModelViewSet):
#     serializer_class = forms.ImageReportForm
#     queryset = models.ImageReportModel.objects.all()
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (permissions.UpdateOwnReport, IsAuthenticatedOrReadOnly,)
#     filter_backends = (filters.SearchFilter,)
#     search_backends = ('timing', 'developer_profile',)

#     def perform_create(self, form, report = None):
#         form.save(developer_profile = self.request.user, report = report)
    
#     def make_create(self, request):
#         form = self.serializer_class(data = request.data)
#         if form.is_valid():
#             #print(data)
#             report = {}
#             # t2 = StartThread(target = self.perform_create, args = (form, report,))
#             # t2.setDaemon(True)
#             # t2.start()
#             self.perform_create(form, report)
#             data = data = form.validated_data['parsed_image']
#             #t1 = StartThread(target = classify_image, args = (data,))
#             #t1.setDaemon(True)
#             #t1.start()
#             report = classify_image(data)
#             t2 = StartThread(target = self.perform_create, args = (form, report,))
#             t2.setDaemon(True)
#             t2.start()
#             return Response({'report': report})
#         else:
#             return Response(
#                 form.errors,
#                 status = status.HTTP_400_BAD_REQUEST,
#             )
#     def create(self, request):
#         t = StartThread(target = self.make_create, args = (request,))
#         t.setDaemon(True)
#         t.start()
#         new_response = t.join()
#         return new_response

# class VideoReportViewSet(viewsets.ModelViewSet):
#     serializer_class = forms.VideoReportForm
#     queryset = models.VideoReportModel.objects.all()
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (permissions.UpdateOwnReport, IsAuthenticatedOrReadOnly,)
#     filter_backends = (filters.SearchFilter,)
#     search_backends = ('timing', 'developer_profile',)

#     def perform_create(self, form, report = None):
#         form.save(developer_profile = self.request.user, report = report)
    
#     def make_create(self, request):
#         form = self.serializer_class(data = request.data)
#         if form.is_valid():
#             data = form.validated_data['parsed_video']
#             t1 = StartThread(target = predict, args = (data,))
#             t1.setDaemon(True)
#             t1.start()
#             report = t1.join()
#             t2 = StartThread(target = self.perform_create, args = (form, report,))
#             t2.setDaemon(True)
#             t2.start()
#             return Response({'report': report})
#         else:
#             return Response(
#                 form.errors,
#                 status = status.HTTP_400_BAD_REQUEST,
#             )
#     def create(self, request):
#         t = StartThread(target = self.make_create, args = (request,))
#         t.setDaemon(True)
#         t.start()
#         new_response = t.join()
#         return new_response