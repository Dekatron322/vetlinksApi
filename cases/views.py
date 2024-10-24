from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Case
from .serializers import CaseSerializer, LaboratoryReportSerializer, CommentSerializer
from drf_yasg.utils import swagger_auto_schema
from django.views.decorators.csrf import csrf_exempt

@swagger_auto_schema(method='get', responses={200: CaseSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can view all cases
def list_all_cases(request):
    """
    Retrieve all cases in the system.
    """
    cases = Case.objects.all()  # Fetch all cases from the database
    serializer = CaseSerializer(cases, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Create Case Endpoint
@swagger_auto_schema(method='post', request_body=CaseSerializer)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_case(request):
    """
    Create a new case associated with the authenticated user.
    """
    user = request.user
    serializer = CaseSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(app_user=user)  # assuming app_user is a foreign key to the user model
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List User's Cases Endpoint
@swagger_auto_schema(method='get', responses={200: CaseSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_cases(request):
    """
    Retrieve all cases associated with the authenticated user.
    """
    user = request.user
    cases = Case.objects.filter(app_user=user)
    serializer = CaseSerializer(cases, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Update Case Endpoint
@swagger_auto_schema(method='put', request_body=CaseSerializer, responses={200: CaseSerializer()})
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_case(request, case_id):
    """
    Update an existing case by its ID.
    """
    try:
        case = Case.objects.get(pk=case_id, app_user=request.user)
    except Case.DoesNotExist:
        return Response({'error': 'Case not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CaseSerializer(case, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete Case Endpoint
@swagger_auto_schema(method='delete', responses={204: 'No Content'})
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_case(request, case_id):
    """
    Delete a specific case by its ID.
    """
    try:
        case = Case.objects.get(pk=case_id, app_user=request.user)
    except Case.DoesNotExist:
        return Response({'error': 'Case not found'}, status=status.HTTP_404_NOT_FOUND)

    case.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Get Case Detail by ID
@swagger_auto_schema(method='get', responses={200: CaseSerializer()})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_case_detail(request, case_id):
    """
    Retrieve details of a specific case by its ID.
    """
    try:
        case = Case.objects.get(pk=case_id, app_user=request.user)
    except Case.DoesNotExist:
        return Response({'error': 'Case not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CaseSerializer(case)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(method='post', request_body=LaboratoryReportSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_laboratory_report(request, case_id):
    """
    Add a laboratory report to a specific case.
    """
    try:
        case = Case.objects.get(pk=case_id, app_user=request.user)
    except Case.DoesNotExist:
        return Response({'error': 'Case not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LaboratoryReportSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(case=case)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: CaseSerializer()})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_case_detail(request, case_id):
    """
    Retrieve details of a specific case by its ID.
    """
    try:
        # Temporarily remove filtering by `app_user=request.user` to check if the case exists.
        case = Case.objects.get(pk=case_id)
    except Case.DoesNotExist:
        return Response({'error': 'Case not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CaseSerializer(case)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Create Case Endpoint
@swagger_auto_schema(method='post', request_body=CommentSerializer)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, case_id):
    """
    Add a comment to a specific case.
    """
    try:
        case = Case.objects.get(pk=case_id)
    except Case.DoesNotExist:
        return Response({'error': 'Case not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(app_user=request.user, case=case)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List comments for a specific case
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_comments(request, case_id):
    """
    Retrieve all comments associated with a specific case.
    """
    try:
        case = Case.objects.get(pk=case_id)
    except Case.DoesNotExist:
        return Response({'error': 'Case not found'}, status=status.HTTP_404_NOT_FOUND)

    comments = Comment.objects.filter(case=case)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_replies(request, comment_id):
    """
    Retrieve all replies associated with a specific comment.
    """
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    replies = Comment.objects.filter(parent=comment)
    serializer = CommentSerializer(replies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)