import imp
from rest_framework.response import Response  
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import User
from django.conf import settings
import boto3

import zipfile
from io import StringIO, BytesIO
import datetime
import botocore

s3 = boto3.resource(
    service_name='s3',
    region_name=settings.AWS_S3_REGION_NAME,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)
def one_download(user):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    file_name = '%s-files-%s.zip' % (bucket_name, user)
    print(f"Saving into zip {file_name}")

    zf = zipfile.ZipFile(file_name, 'w')

    bucket = s3.Bucket(bucket_name)
    try:
        for obj in bucket.objects.all():
            if obj.key.split('/')[2]=='avi@gmil.com':
                print("value",obj.key)
                data = s3.Bucket(bucket_name).Object(obj.key).get()
                zf.writestr(obj.key, data.get('Body').read())
    except botocore.exceptions.ClientError as resperror:
        print ("Error - does bucket exist?", str(resperror))
        print ("Please remove possible empty zip: ", file_name)
    zf.close()
class Download_image(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        print(user)
        one_download(user)
        return Response({'data':'Zip file downloaded'})