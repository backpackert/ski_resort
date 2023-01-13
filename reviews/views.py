from django.shortcuts import render, redirect
from django.views import generic
from .models import Review
from rest_framework.views import APIView
from django.contrib.sites.shortcuts import get_current_site
from .forms import ReviewForm
from .serializers import ReviewsSerializer
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated


class ReviewCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewsSerializer
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'create_review.html'

    def post(self, request):
        review = request.data.get('review', {})
        serializer = self.serializer_class(data=review)
        # serializer.is_valid(raise_exception=True)
        # review = serializer.save()
        if serializer.is_valid(raise_exception=True):
            review = serializer.save()
        return Response({"success": "Review '{}' created successfully".format(review.brief)})
        # return Response(serializer.data, status=201)

        # return redirect('review_list')

    # def delete(self, request, pk):
    #     # Get object with this pk
    #     article = get_object_or_404(Article.objects.all(), pk=pk)
    #     article.delete()
    #     return Response({
    #         "message": "Article with id `{}` has been deleted.".format(pk)
    #     }, status=204)


class ReviewListView(generic.ListView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'review_list.html'
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer


# def create_review(request):
#     error = ''
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         else:
#             error = 'Incorrect form'
#
#     form = ReviewForm()
#     data = {
#         'form': form,
#         'error': error
#     }
#
#     return render(request, 'reviews/create_review.html', data)



