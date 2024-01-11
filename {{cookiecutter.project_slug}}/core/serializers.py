from datetime import datetime

from rest_framework import serializers
from rest_framework.fields import FileField
from rest_framework.serializers import ModelSerializer, Serializer, ValidationError

from core.models import Media


class BaseSerializer(Serializer):
    """
    Base serializer class for common functionality and customization.

    This class is intended to be used as a base class for other serializers
    in the project. It provides a central place to include shared logic,
    additional fields, or methods that should be present in multiple serializers.
    Subclasses inheriting from this class can benefit from a consistent structure
    and behavior across the project.

    Example:
    ```
    class CustomSerializer(BaseSerializer):
        # Your custom serializer fields and methods go here
    ```
    """

    ...


class BaseModelSerializer(ModelSerializer):
    """
    Base model serializer class for common functionality and customization.

    This class inherits from Django REST Framework's ModelSerializer and is intended
    to be used as a base class for other model serializers in the project. It provides
    a central place to include shared logic, additional fields, or methods specific
    to model serializers. Subclasses inheriting from this class can benefit from a
    consistent structure and behavior across serializers that deal with Django models.

    Example:
    ```
    class CustomModelSerializer(BaseModelSerializer):
        # Your custom model serializer fields and methods go here
    ```
    """

    ...


class MediaSerializer(BaseModelSerializer):
    """
    Serializer for the Media model.

    This serializer is used to convert Media model instances to JSON representations.
    It inherits from the BaseModelSerializer, providing common functionality for
    handling Django model instances. The Meta class specifies that the serializer
    should be associated with the Media model and include all fields.

    Example:
    ```
    media_instance = Media.objects.get(pk=1)
    serializer = MediaSerializer(media_instance)
    serialized_data = serializer.data
    ```

    Attributes:
    - `model`: Specifies the associated model for the serializer.
    - `fields`: A string indicating that all fields of the associated model should be included.
    """

    class Meta:
        model = Media
        fields = "__all__"

    def validate_media_type(self, value):
        if value not in ["image", "video", "document"]:
            raise ValidationError("Invalid media type.")
        return value

    def create(self, validated_data):
        file_path = validated_data.pop("file_path")
        instance = super().create(validated_data)
        instance.file_path.save(file_path.name, file_path)
        return instance

    def update(self, instance, validated_data):
        file_path = validated_data.pop("file_path", None)
        instance = super().update(instance, validated_data)
        if file_path is not None:
            instance.file_path.save(file_path.name, file_path)
        return instance


class MediaFileField(FileField):
    def to_internal_value(self, data):
        if not data:
            return None

        # Validate file type
        if data.content_type:
            media_type = data.content_type.split("/")[0]
            media_type = "document" if media_type == "text" else media_type

        if media_type not in ["image", "video", "document"]:
            raise serializers.ValidationError("Invalid media type.")

        # Create Media object from file and return its serialized data
        media_serializer = MediaSerializer(data={"file_path": data, "media_type": media_type, "title": data.name})
        media_serializer.is_valid(raise_exception=True)
        return media_serializer.validated_data

    def to_representation(self, value):
        if not value:
            return None
        # Return serialized data of the existing Media object
        media_serializer = MediaSerializer(value)
        return media_serializer.data


class UnixTimestampField(serializers.Field):
    def to_representation(self, value):
        return datetime.fromtimestamp(value / 1000).strftime("%Y-%m-%d %H:%M:%S")

    def to_internal_value(self, data):
        return int(data)
