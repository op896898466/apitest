from rest_framework import serializers

from .models import DebugTalks


class DebugTalksSerializer(serializers.ModelSerializer):
    """
    DebugTalks序列化器
    """

    class Meta:
        model = DebugTalks
        exclude = ('create_time', 'update_time', "is_delete")

        extra_kwargs = {
            'debugtalk': {
                'write_only': True
            }
        }
