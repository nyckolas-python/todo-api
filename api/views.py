import django_filters.rest_framework as filters

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework.generics import CreateAPIView, \
    ListCreateAPIView, RetrieveUpdateDestroyAPIView

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from api.serializers import UserSerializer, TaskSerializer, TaskSerializerExecutor, \
    TaskImagesSerializer, UserRegisterSerializer
from api.models import Task, Image
from api.permissions import IsOwner, IsExecutor
from api.servises import is_task_executor, is_task_owner

# Create your views here.
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def user_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'format', \
            'username': 'username', 'password': 'password'})
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid data'})

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=HTTP_200_OK)


class RegisterUserView(CreateAPIView):
    """
    Registration View
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data["email"]
            username = serializer.data["username"]
            password = serializer.data["password"]

            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            token = Token.objects.create(user=user)
            return Response(
                {
                    "user": f"{user.username}",
                    "token": f"{token}",
                },
                status=HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CreateUserWithoutValidationView(CreateAPIView):
    """
    Create user without validation View
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class TaskListView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['status']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsExecutor | IsOwner, )
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_permissions(self):
        if self.request.method == 'PUT' and is_task_executor(self.request):                
            return [IsExecutor(),]

        return [IsOwner(),]

    def get_queryset(self):
        return (
            Task.objects.filter(id=self.kwargs.get("pk", None))
            .prefetch_related("executors")
            .select_related("user")
        )
    
    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT' and is_task_executor(self.request):
            serializer_class = TaskSerializerExecutor

        return serializer_class


class CreateImagesView(CreateAPIView):

    serializer_class = TaskImagesSerializer
    queryset = Image.objects.all()

    def post(self, request, *args, **kwargs):
        if not is_task_owner(request):
            raise PermissionDenied({"detail": "You don't have permission to access"})

        return super().post(request, *args, **kwargs)
