from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        # model to base serializer from
        model = get_user_model()
        # fields to include in the serializer;
        # converted to and from json when make http post;
        # to make accessible in api
        fields = ('email', 'password', 'name')
        # extra_keywordargs: configure extra settings in model serializer
        # define extra restrictions for field(s) defined
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serialzier for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            # Access the context of request.
            # The view will pass the context into serializer
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        # when override validate function, must return the values;
        # at the end once the validation is successful
        attrs['user'] = user
        return attrs
