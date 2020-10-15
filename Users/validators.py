from django.core.exceptions import ValidationError


def validate_file_size(value):
    file_size = value.size

    if file_size > 10485760:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value


def validate_image_size(value):
    file_size = value.size
    if file_size > 10485760:
        return False
    else:
        return True


def validate_video_size(value):
    file_size = value.size
    if file_size > 10485760:
        return False
    else:
        return True
