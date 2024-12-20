from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    ContentSerializer,
    VoteSerializer,
    UserRegistrationSerializer,
    ContentDetailSerializer,
)
from .models import Content, Vote
from .pagination import ContentPagination


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateContentAPIView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ContentSerializer
    queryset = Content.objects.all()


class ContentsListAPIView(APIView):
    pagination_class = ContentPagination

    def get(self, request):
        last_id = request.GET.get("last_id", None)
        contents_query = Content.objects.all().order_by("-created_at")

        if last_id:
            contents_query = contents_query.filter(id__gt=last_id)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(contents_query, request)

        serialized_data = ContentSerializer(result_page, many=True)

        return paginator.get_paginated_response(serialized_data.data)


class VoteCreateUpdateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            content_id = serializer.validated_data["content"].id
            score = serializer.validated_data["score"]
            user = request.user

            existing_vote = Vote.objects.filter(
                content_id=content_id, user=user
            ).first()

            if existing_vote:
                existing_vote.score = score
                existing_vote.save()
                return Response(
                    {"message": "Vote updated successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                Vote.objects.create(
                    content_id=content_id,
                    user=user,
                    score=score,
                )
                return Response(
                    {"message": "Vote added successfully."},
                    status=status.HTTP_201_CREATED,
                )
        print("was not valid")
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ContentDetailAPIView(RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Content.objects.all()
    serializer_class = ContentDetailSerializer
    lookup_field = "pk"

    def get_serializer_context(self):
        user = self.request.user
        if not user.is_authenticated:
            user_id = None
        else:
            user_id = user.id
        return {"user_id": user_id}
