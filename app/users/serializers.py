from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from core import models
from rest_framework import serializers
import re
from django.core.validators import RegexValidator

def controlla_stringa(value):
    """ check is not empty """
    msg=""
    if len(value.replace(" ","")) == 0:
        msg = _('Campo {} deve essere compilato')

    """ check is only alphabetic """
    p = re.compile('[0-9]+')
    if p.search(value):
        msg = _("Campo {} deve essere compilato")

    return msg

def controlla_numero(value):
    msg = ""
    p = re.compile('[0-9]+').search(value)
    if p:
        if value != re.compile('[0-9]+').search(value).group():
            msg = _("campo {} deve contoneere solo numeri")
    return msg


def normalize_stringa(value):

    """ Normalize with first capital letter nd the rest lower """
    # values = value.strip()
    value=value.lower()
    l_values = value.split(" ")
    l_values = [i for i in l_values if len(i)>0]
    value = ""
    for i in l_values:
        li = list(i)
        li[0] = li[0].upper()
        if value == "":
            value = "".join(li)
        else:
            value = value + " " + "".join(li)
    return value


class ProvinciaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Provincia
        fields = ('id', 'nome')
        read_only_fields = ('id', 'nome')


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the user object"""

    class Meta:
        model = get_user_model()
        # fields = ('email', 'password', 'nome','cognome')
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """ create a new user with encrypted password and return it """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """ Update a user, settings the password correctly and return it """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user authentication object """
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='ValidationError')

        attrs['user'] = user
        return attrs
#
class UserDetailSerializer(serializers.ModelSerializer):
    """ serializers with all the users data """

    class Meta:
        model = models.User
        fields = ('nome','cognome', 'telefono',
                  'indirizzo', 'citta', 'provincia_ita',
                  'provincia_estero', 'stato', 'stato_estero',
                  )

    def validate_cognome(self, value):
       """ check cognome does exists """
       value = value.strip()
       msg_error = controlla_stringa(value)
       if msg_error != "":
           raise serializers.ValidationError(msg_error.format(_('Cognome')))
       """ normalize field """
       value = normalize_stringa(value)

       return value

    def validate_nome(self, value):
        value = value.strip()
        """ check nome does exists """
        msg_error = controlla_stringa(value)
        if msg_error != "":
            raise serializers.ValidationError(msg_error.format(_('Nome')))
        """ normalize field """
        value = normalize_stringa(value)
        return value

    def validate_telefono(self, value):
        """ valdidate telefono only number """
        """ allow + if first """
        piu = False
        value = value.strip()
        lv = list(value)
        if lv[0] == '+':
            lv.pop(0)
            num_tel = "".join(lv)
            piu = True
        else:
            num_tel = value
        msg = controlla_numero(num_tel)

        if len(msg)>0:
            raise serializers.ValidationError(msg.format(_('Telefono')))

        if piu == True:
            num_tel = '+' + num_tel

        return value

    def validate_indirizzo(self, value):
        """ check if indirizzo is filled"""
        value = value.strip()
        if not value:
            raise serializers.ValidationError(_('Indirizzo non inserito'))
        value = value.lower()

        return value

    def validate_citta(self, value):
        """ check cognome does exists """
        value = value.strip()
        msg_error = controlla_stringa(value)
        if msg_error != "":
            raise serializers.ValidationError(msg_error.format(_('Citta')))
        """ normalize field """
        value = normalize_stringa(value)

        return value

    def validate_stato_estero(self, value):
        """ check cognome does exists """
        value = value.strip()
        if len(value)>0:
            msg_error = controlla_stringa(value)
            if msg_error != "":
                raise serializers.ValidationError(msg_error.format('Stato Estero'))
                """ normalize field """
            value = normalize_stringa(value)

        return value

    def validate_provincia_ita(self, value):
        return value

    def validate(self, data):
        """ check if the important field are present """
        field_list = ['nome','cognome', 'telefono',
                  'indirizzo', 'citta', 'stato']
        location_fields = ['stato', 'stato_estero', 'provincia_estero']

        msg_error = []
        for f in field_list:
            if f not in data:
                msg_error.append ("campo {} mancante".format(f))

        for f in location_fields:
            if f not in data:
                msg_error.append ("campo {} mancante".format(f))
            else:
                if data[f] is not None:
                    data[f] = data[f].strip()

        if len(msg_error) > 0:
            raise serializers.ValidationError(msg_error)

        """ check if provincia is coherent with country """

        # if (data['provincia_ita'] is not None) and \
        #    (data['provincia_estero'] is not None or \
        #     len(data['provincia_estero'])!=0):
        #    print (data)
        #    raise serializers.ValidationError(_(
        #         "Selezionare solo una proivincia in base allo stato"))

        if data['stato'] == 'I' and data['provincia_ita'] is None:
            raise serializers.ValidationError(
                "Selezionare la provincia italiana")
        if data['stato'] == 'E' and (len(data['provincia_estero'])==0 or \
            len(data['stato_estero'])==0):
            raise serializers.ValidationError(_(
                "Inserire la provincia/contea paese estero"))
        return data
