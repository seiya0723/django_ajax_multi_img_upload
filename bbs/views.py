from django.shortcuts import render


#TODO:ここでDRF仕様のビュークラスと通常のビュークラスを切り替え
#from django.views import View
from rest_framework.views import APIView as View

from django.http.response import JsonResponse
from django.template.loader import render_to_string

from .models import Topic
from .forms import TopicForm,TopicImageForm


class IndexView(View):

    def get(self, request, *args, **kwargs):

        topics  = Topic.objects.all()
        context = { "topics":topics }

        return render(request,"bbs/index.html",context)

    def post(self, request, *args, **kwargs):

        data    = { "error":True }
        form    = TopicForm(request.POST)

        #ここでコメントを保存
        if not form.is_valid():
            print("Validation Error")
            return JsonResponse(data)

        topic   = form.save()


        #ここで複数指定した画像を追記。
        images  = request.FILES.getlist("image")

        for image in images:

            upload_image_file   = { "image":image }
            upload_image_name   = { "topic":topic.id,"image":str(image) }

            form    = TopicImageForm(upload_image_name,upload_image_file)

            if form.is_valid():
                print("バリデーションOK")
                form.save()
            else:
                print("バリデーションNG")
                print(form.errors)




        context             = {}
        context["topics"]   = Topic.objects.all()

        data["error"]       = False
        data["content"]     = render_to_string("bbs/content.html",context,request)

        return JsonResponse(data)

    def delete(self, request, *args, **kwargs):
        
        data    = { "error":True }

        if "pk" not in kwargs:
            return JsonResponse(data)

        topic   = Topic.objects.filter(id=kwargs["pk"]).first()

        if not topic:
            return JsonResponse(data)

        topic.delete()

        context             = {}
        context["topics"]   = Topic.objects.all()

        data["error"]       = False
        data["content"]     = render_to_string("bbs/content.html",context,request)

        return JsonResponse(data)

index   = IndexView.as_view()



