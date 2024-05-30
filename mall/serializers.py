from rest_framework import serializers
from .models import Stuff, PostImage


class PostImageSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(use_url=True)

    class Meta:
        model = PostImage
        fields = ['image']


class PostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    # 게시글에 등록된 이미지들 가지고 오기
    def get_images(self, obj):
        image = obj.image.all()
        return PostImageSerializer(instance=image, many=True, context=self.context).data

    class Meta:
        model = Stuff
        fields = '__all__'

    def create(self, validated_data):
        instance = Stuff.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            PostImage.objects.create(post=instance, image=image_data)
        return instance
