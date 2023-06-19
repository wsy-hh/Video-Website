from django.shortcuts import render
from django.views import generic
from .models import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.hashers import check_password
import jwt
from datetime import datetime, timedelta
from rest_framework.parsers import FileUploadParser
import time
import os
import json
from rest_framework import status
from django.core.paginator import Paginator, InvalidPage
import hashlib
from django.conf import settings
import base64
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt


def md5_encrypt(string):
    # 创建MD5哈希对象
    md5_hash = hashlib.md5()
    
    # 将字符串转换为字节类型，并计算其哈希值
    md5_hash.update(string.encode('utf-8'))
    
    # 获取哈希值的十六进制表示
    encrypted_string = md5_hash.hexdigest()
    
    return encrypted_string


def generate_jwt_token(user_id):
    # 设置过期时间为 1 小时
    expire_time = datetime.utcnow() + timedelta(hours=1)
    # 构建 JWT 载荷
    payload = {
        'user_id': user_id,
        'exp': expire_time
    }
    # 生成 JWT 令牌
    token = jwt.encode(payload, 'secret_key', algorithm='HS256')
    return token


def get_user_id_from_token(token):
    decoded_token = jwt.decode(token, 'secret_key', algorithms=['HS256'])
    user_id = decoded_token.get('user_id')
    return user_id


def encrypt_password(password):
    md5_hash = hashlib.md5()
    md5_hash.update(password.encode('utf-8'))
    encrypted_password = md5_hash.hexdigest()
    return encrypted_password


class LoginAPIView(APIView):
    def post(self, request):
        if request.method == 'POST':
            email = request.data['email']
            password = encrypt_password(request.data['password'])
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'message': 'Invalid credentials'}, status=201)
            # 验证密码
            if password == user.pwd:
                # 登录成功，生成并返回登录令牌
                # 可以使用 JWT 库生成令牌
                token = generate_jwt_token(user.id)
                return Response({'token': token, 'message': "Login successful!", 'code': 200, 'nickname': user.nickname}, status=200)
            else:
                return Response({'message': 'Wrong password.'}, status=200)
        else:
            return Response({'message': 'Please using POST method.'}, status=400)

        serializer = UserSerializer(data=request.data)


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # 创建新用户
            return Response({'message': 'User registered successfully.', "code": 200}, status=200)
        else:
            return Response(serializer.errors, status=400)




class FileUploadView(APIView):
    def post(self, request, format=None):
        # try:
        #     token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        #     user_id = get_user_id_from_token(token)
        # except Exception:
        #     return Response({'error': 'Invalid Token'}, status=400)
        file_obj = request.FILES['file']
        file_name = file_obj.name
        file_ext = os.path.splitext(file_name)[1]
        file_name = md5_encrypt(str(time.time())) + file_ext
        path = os.path.join(settings.BASE_DIR, 'static', 'video', file_name)
        print(file_name)
        if(file_ext == ".mp4"):
            file = File.objects.create(path="video/"+file_name)
            file.save()
        else:
            picture = Picture.objects.create(path="video/"+file_name)
            picture.save()
        with open(path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)        
        return Response({'message': 'File uploaded successfully','code': 200, 'file_name': "video/"+file_name}, status=200)

class GetVideoDetailView(APIView):
    def get(self, request, format=None):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        video = Video.objects.get(pk=request.data['video'])
        print(type(video))
        serializer = VideoSerializer(instance=video)
        print(serializer.data)
        if serializer.data is not None:
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)


class GetVideoList(APIView):
    def post(self, request, format=None):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        keyword = request.data['keyword'] if 'keyword' in request.data else ''
        page = request.data['page'] if 'page' in request.data else 1

        # 进行关键词查询
        videos = Video.objects.filter(title__icontains=keyword)

        # 对查询结果进行分页
        paginator = Paginator(videos, 10)  # 每页显示10个结果
        try:
            page_videos = paginator.page(page)
        except InvalidPage:
            return Response({'message': 'Invalid page number.'}, status=400)

        # 序列化分页后的结果
        serializer = VideoSerializer(page_videos, many=True)

        # 返回序列化数据和分页信息
        response_data = {
            'results': serializer.data,
            'page': page_videos.number,
            'total_pages': paginator.num_pages,
            'total_results': paginator.count
        }
        return Response(response_data, status=200)


class AddVideoView(APIView):
    def post(self, request, format=None):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        user = User.objects.get(pk=user_id)
        # const data = {
        #   file_path: this.file_name,
        #   picture_path: this.picture_path,
        #   introduction: this.form.introduction,
        #   title: this.form.title,
        #   tags: this.checkList
        # }
        file = File.objects.get(path=request.data['file_path'])
        picture = Picture.objects.get(path=request.data['picture_path'])
        video = Video.objects.create(
            title=request.data['title'],
            introduction=request.data['introduction'],
            user=user,
            file=file,
            picture=picture
        )
        labels = request.data['tags']
        for label_name in labels:
            label = Label.objects.get(name=label_name)
            video.labels.add(label)
        video.save()
        return Response({'message': 'Video created successfully.','code':200}, status=200)


class RecommandListView(APIView):
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        recommand = Recommend.objects.all()
        serializer = RecommandSerializer(recommand, many=True)
        return Response(serializer.data)


class BannerListView(APIView):
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        banner = Banner.objects.all()
        serializer = BannerSerializer(banner, many=True)
        return Response(serializer.data)


class LabelListAPIView(APIView):
    def get(self, request):
        # try:
        #     token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        #     user_id = get_user_id_from_token(token)
        # except Exception:
        #     return Response({'error': 'Invalid Token'}, status=400)
        labels = Label.objects.all()
        serializer = LabelSerializer(labels, many=True)
        return Response(serializer.data)


class GetHistoryRecordList(APIView):
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
            print(user_id)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        user = User.objects.get(pk=user_id)
        history_record = HistoryRecord.objects.filter(
            user=user).order_by('-id')
        serializer = HistoryRecordDetailSerializer(history_record, many=True)
        return Response(serializer.data)


class AddHistoryRecord(APIView):
    def post(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
            print(user_id)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        video_id = request.data.get('video_id')
        try:
            user = User.objects.get(pk=user_id)
            video = Video.objects.get(pk=video_id)
        except User.DoesNotExist and Video.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        history_record_data = {'user': user_id, 'video': video_id}
        print(history_record_data)
        serializer = HistoryRecordSerializer(data=history_record_data)
        if serializer.is_valid():
            history_record = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetLableVideoListView(APIView):
    def post(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)

        label_id = request.data['label_id']
        label = Label.objects.get(pk=label_id)
        videos = Video.objects.filter(labels=label)

        serializer = VideoSerializer(videos, many=True)

        return Response(serializer.data)

class UpdateUserInfo(APIView):
     def post(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        user = User.objects.get(pk=user_id)
        avatar = Picture.objects.get(path=request.data['avatar'])
        user.nickname = request.data['nickname']
        user.email = request.data['email']
        user.phone = request.data['phone']
        user.introduction = request.data['introduction']
        user.gender = request.data['gender']
        user.avatar = avatar
        user.save()

        return Response({'message': 'Update successfully.', 'code': 200}, status=200)

class GetUserInfo(APIView):
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        user = User.objects.get(pk=user_id)
        avatoar = user.avatar.path
        data = {
            'nickname': user.nickname,
            'email': user.email,
            'phone': user.phone,
            'introduction': user.introduction,
            'gender': user.gender,
            'avatar': avatoar

        }
        return Response(data)


class getSubscribeStatus(APIView):
    def post(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)

        creator = User.objects.get(email=request.data['email'])

        try:
            subscribe = Subscription.objects.get(
                creator_id=creator.id, user_id=user_id)
            return Response({'status': 1})
        except Subscription.DoesNotExist:
            return Response({'status': 0})


class CancelSubscribe(APIView):
    def post(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        user = User.objects.get(pk=user_id)
        creator = User.objects.get(email=request.data['email'])
        subscribe = Subscription.objects.get(
            creator_id=creator.id, user_id=user_id)
        subscribe.delete()
        return Response({'message': 'Cancel successfully.'}, status=200)


class Subscribe(APIView):
    def post(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)

        user = User.objects.get(pk=user_id)
        creator = User.objects.get(email=request.data['email'])
        subscribe = Subscription.objects.create(
            user_id=user.id,
            creator_id=creator.id
        )
        subscribe.save()
        return Response({'message': 'Subscribe successfully.'}, status=200)


class GetCreatorVideoList(APIView):
    def post(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        creator = User.objects.get(email=request.data['email'])
        videos = Video.objects.filter(user=creator).order_by('?')[:5]
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

class GetUploadVideoList(APIView):
    def post(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        creator = User.objects.get(pk=user_id)
        videos = Video.objects.filter(user=creator)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

class GetSubscribeList(APIView):
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        user = User.objects.get(pk=user_id)
        subscribe = Subscription.objects.filter(user_id=user.id)
        user = User.objects.get(pk=user_id)
        subscriptions = Subscription.objects.filter(user_id=user.id)
        creator_ids = subscriptions.values_list('creator_id', flat=True)
        creators = User.objects.filter(id__in=creator_ids)
        # 处理 creators，将其序列化为需要的格式
        serializer = UserSerializer(creators, many=True)
        return Response(serializer.data)
