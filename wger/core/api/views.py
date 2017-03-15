# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.
import re

from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route


from wger.core.models import (
    UserProfile,
    Language,
    DaysOfWeek,
    License,
    RepetitionUnit,
    WeightUnit)
from wger.core.api.serializers import (
    UsernameSerializer,
    UserRegistrationSerializer,
    LanguageSerializer,
    DaysOfWeekSerializer,
    LicenseSerializer,
    RepetitionUnitSerializer,
    WeightUnitSerializer
)
from wger.core.api.serializers import UserprofileSerializer
from wger.core.models import Language
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, \
    TokenAuthentication
from wger.utils.permissions import UpdateOnlyPermission, WgerPermission
from django.utils import translation
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from wger.config.models import GymConfig


class RegisterUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows login and registration of users
    """
    serializer_class = UserRegistrationSerializer
    http_method_names = ['post']
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        # Creates a user and assign them a default gym

        # validates email address
        if request.data.get('email'):
            email_format = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
            if not re.match(email_format, request.data.get('email')):
                raise serializers.ValidationError("Invalid email format")

        user = User(username=request.data['username'], email=request.data.get('email', None))
        # Hashes user's password
        user.password = make_password(request.data['password'])
        # Handles case for when the user already exists
        try:
            user.save()
        except IntegrityError:
            content = {"message": "User already exists"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Sets the language for the user
        language = Language.objects.get(short_name=translation.get_language())
        user.userprofile.notification_language = language

        # Sets default gym, if needed
        gym_config = GymConfig.objects.get(pk=1)
        if gym_config.default_gym:
            user.userprofile.gym = gym_config.default_gym

            # Creates gym user configuration object
            config = GymUserConfig()
            config.gym = gym_config.default_gym
            config.user = user
            config.save()

        user.userprofile.save()

        serializer = UserRegistrationSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for workout objects
    """
    is_private = True
    serializer_class = UserprofileSerializer
    permission_classes = (WgerPermission, UpdateOnlyPermission)
    ordering_fields = '__all__'

    def get_queryset(self):
        """
        Only allow access to appropriate objects
        """
        return UserProfile.objects.filter(user=self.request.user)

    def get_owner_objects(self):
        """
        Return objects to check for ownership permission
        """
        return [(User, 'user')]

    @detail_route()
    def username(self, request, pk):
        """
        Return the username
        """

        user = self.get_object().user
        return Response(UsernameSerializer(user).data)


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for workout objects
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    ordering_fields = '__all__'
    filter_fields = ('full_name',
                     'short_name')


class DaysOfWeekViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for workout objects
    """
    queryset = DaysOfWeek.objects.all()
    serializer_class = DaysOfWeekSerializer
    ordering_fields = '__all__'
    filter_fields = ('day_of_week', )


class LicenseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for workout objects
    """
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    ordering_fields = '__all__'
    filter_fields = ('full_name',
                     'short_name',
                     'url')


class RepetitionUnitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for repetition units objects
    """
    queryset = RepetitionUnit.objects.all()
    serializer_class = RepetitionUnitSerializer
    ordering_fields = '__all__'
    filter_fields = ('name', )


class WeightUnitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for weight units objects
    """
    queryset = WeightUnit.objects.all()
    serializer_class = WeightUnitSerializer
    ordering_fields = '__all__'
    filter_fields = ('name', )
