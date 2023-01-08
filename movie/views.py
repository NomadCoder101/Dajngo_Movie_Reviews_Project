from django.shortcuts import render ,HttpResponse

from django.shortcuts import get_object_or_404,redirect

from movie.models import Movie, Review

from .forms import ReviewForm

from django.contrib.auth.decorators import login_required



# Create your views here.

def home1(request):

    searchTerm = request.GET.get('searchMovie')
    movies = Movie.objects.all()
    

    return render(request,'movie/home.html',{'searchTerm':searchTerm,
                                            'movies':movies})



def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'movie/home.html',{'searchTerm':searchTerm, 'movies': movies})


def detail(request, movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    reviews = Review.objects.filter(movie = movie)
    return render(request, 'movie/detail.html', {'movie':movie,'reviews':reviews})

def about(request):
    return render(request, 'movie/about.html',{})


def signup(request):
    email = request.GET.get('email')
    return render(request, 'movie/signup.html', {'email':email})


@login_required
def createreview(request, movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    if request.method == 'GET':
        return render(request, 'movie/createreview.html',{'form':ReviewForm(), 'movie':movie})
    else:
        try:

            form = ReviewForm(request.POST)
            newReview = form.save(commit=False)
            newReview.user = request.user
            newReview.movie = movie
            newReview.save()
            return redirect('movie:detail',newReview.movie.id)
        except ValueError:
            return render(request,'movie/createreview.html',{'form':ReviewForm(),'error':'bad data passed in'})


@login_required
def updatereview(request, review_id):
    review = get_object_or_404(Review,pk=review_id,user=request.user)

    if request.method == 'GET':
        form = ReviewForm(instance=review)
        return render(request, 'movie/updatereview.html',{'review': review,'form':form})
    else:
        try:
            form = ReviewForm(request.POST,instance=review)
            form.save()
            return redirect('movie:detail', review.movie.id)
        except ValueError:
            return render(request,'movie/updatereview.html',{'review': review,'form':form,'error':'Bad data in form'})


@login_required
def deletereview(request, review_id):
    review = get_object_or_404(Review, pk=review_id,
    user=request.user)
    review.delete()
    return redirect('movie:detail', review.movie.id)