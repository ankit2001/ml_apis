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
from Cervical_Cancer.predict_cervical import predict_cervical
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
        
class CervicalViewSet(viewsets.ModelViewSet):
    serializer_class = forms.CervicalForm
    queryset = models.CervicalModel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnReport, IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_backends = ('timing', 'developer_profile', "age", "no_of_sexual_parteners", "age_of_first_intercourse", "no_of_pregnancies", "smokes", "smokes_packs", "hormonal_contraceptives", "intra_uterine", "STDS", "any_std", "condylomatosis", "cervical_condylomatosis", "vaginal", "vulvo_perineal", "syphilis", "pelvic", "genital", "molluscum", "AIDS", "HIV", "hepatitis", "HPV", "diagnosis_std", "cancer", "neoplasis", "diagnosis_hpv")

    def perform_create(self, form, report = None):
        form.save(developer_profile = self.request.user, report = report)

    def make_create(self, request):
        form = self.serializer_class(data = request.data)
        if form.is_valid():
            age = form.validated_data["age"]
            no_of_sexual_parteners = form.validated_data["no_of_sexual_parteners"]
            age_of_first_intercourse = form.validated_data["age_of_first_intercourse"]
            no_of_pregnancies = form.validated_data["no_of_pregnancies"]
            smokes = form.validated_data["smokes"]
            smokes_packs = form.validated_data["smokes_packs"]
            hormonal_contraceptives = form.validated_data["hormonal_contraceptives"]
            intra_uterine = form.validated_data["intra_uterine"]
            STDS = form.validated_data["STDS"]
            any_std = form.validated_data["any_std"]
            condylomatosis = form.validated_data["condylomatosis"]
            cervical_condylomatosis = form.validated_data["cervical_condylomatosis"]
            vaginal = form.validated_data["vaginal"]
            vulvo_perineal = form.validated_data["vulvo_perineal"]
            syphilis = form.validated_data["syphilis"]
            pelvic = form.validated_data["pelvic"]
            genital = form.validated_data["genital"]
            molluscum = form.validated_data["molluscum"]
            AIDS = form.validated_data["AIDS"]
            HIV = form.validated_data["HIV"]
            hepatitis = form.validated_data["hepatitis"]
            HPV = form.validated_data["HPV"]
            diagnosis_std = form.validated_data["diagnosis_std"]
            cancer = form.validated_data["cancer"]
            neoplasis = form.validated_data["neoplasis"]
            diagnosis_hpv = form.validated_data["diagnosis_hpv"]
            #t1 = StartThread(target = predict, args = (data,))
            #t1.setDaemon(True)
            #t1.start()
            report = predict_cervical(age, no_of_sexual_parteners, age_of_first_intercourse, no_of_pregnancies, smokes, smokes_packs, hormonal_contraceptives, intra_uterine, STDS, any_std, condylomatosis, cervical_condylomatosis, vaginal, vulvo_perineal, syphilis, pelvic, genital, molluscum, AIDS, HIV, hepatitis, HPV, diagnosis_std, cancer, neoplasis, diagnosis_hpv)
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

class BreastCancerViewSet(viewsets.ModelViewSet):
    serializer_class = forms.BreastCancerForm
    queryset = models.BreastCancerModel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnReport, IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_backends = ('timing', 'developer_profile',)

    def perform_create(self, form, report = None):
        form.save(developer_profile = self.request.user, report = report)
    
    def make_create(self, request):
        form = self.serializer_class(data = request.data)
        if form.is_valid():
            #print(data)
            report = {}
            # t2 = StartThread(target = self.perform_create, args = (form, report,))
            # t2.setDaemon(True)
            # t2.start()
            self.perform_create(form, report)
            data = form.validated_data['parsed_image']
            #t1 = StartThread(target = classify_image, args = (data,))
            #t1.setDaemon(True)
            #t1.start()
            from Breast_Cancer.predict_breast_cancer import predict_breast_cancer
            report = predict_breast_cancer(data)
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