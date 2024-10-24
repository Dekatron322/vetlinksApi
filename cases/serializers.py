from rest_framework import serializers
from .models import Case, LaboratoryReport, Comment

class LaboratoryReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaboratoryReport
        fields = ['report_title', 'report_details', 'created_at']

class CaseSerializer(serializers.ModelSerializer):
    laboratory_reports = serializers.SerializerMethodField()  # Define a method to fetch lab reports

    class Meta:
        model = Case
        fields = [
            'id',
            'category', 
            'case_title', 
            'image', 
            'signalment_and_history', 
            'clinical_examination', 
            'clinical_findings', 
            'differential_diagnoses', 
            'tentative_diagnoses', 
            'management', 
            'diagnostic_plan', 
            'advice_to_clients', 
            'assistants',
            'laboratory_reports'  # Include lab reports in the case serializer
        ]
    
    # Method to return laboratory reports
    def get_laboratory_reports(self, obj):
        reports = LaboratoryReport.objects.filter(case=obj)  # Filter lab reports for this case
        return LaboratoryReportSerializer(reports, many=True).data



class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'case', 'app_user', 'comment_text', 'parent', 'created_at', 'replies']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []