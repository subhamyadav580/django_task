from rest_framework import serializers
from accounts.models import User
import string 
import random 

# Returns a random alphanumeric string of length 'length'
def random_key(length):
	key = ''
	for i in range(length):
		key += random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
	return key




class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'age', 'uniqueID', 'picture', 'password', 'password2']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = User(
            email = self.validated_data['email'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            age = self.validated_data['age'],
            picture = self.validated_data['picture'],
        )
        uniqueID = self.validated_data['uniqueID']
        if uniqueID is not None:
            uniqueID = self.validated_data['uniqueID']
            uniqueID_length = len(uniqueID)
            if uniqueID_length == 6 and uniqueID.isalnum():
                account.uniqueID = uniqueID
            else:
                raise serializers.ValidationError({'uniqueID': 'UniqueID must be alphanumeric and of length 6'})

        else:
            uniqueID = random_key(6)
            print(uniqueID)
            account.uniqueID = uniqueID
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password must match'})

        account.set_password(password)
        account.save()

        return account





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email',
                  'first_name', 'last_name', 'age', 'uniqueID', 'picture']