from django.shortcuts import render, redirect, reverse,  get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import BookModelForm
from .models import Book
# 1. form없이 걍 2. form객체생성후(6장) 3. DjangoGenericView 이용 4. GenericView 상속(7장)
book_list = ListView.as_view(model=Book) # Listview 제너릭뷰 
# def book_list(request):
#   book_list = Book.objects.all()
#   return render(request,
#                 'book/book_list.html',
#                 {'book_list':book_list},
                  #  'object_list':

class BookcreateView(CreateView):
  model = Book
  fields = ['title','author','publisher','sales']
  def form_valid(self, form): # 유효성 검사 성공후 자동 호출
        book = form.save(commit=False)
        book.ip = self.request.META['REMOTE_ADDR']
        book.save()
        return redirect(book) 
book_new = BookcreateView.as_view()


book_new1 = CreateView.as_view(model=Book, # as_view가 book_new1을 알아서 만들어줌 / 모델이름 필드 추가 필요
                              fields = ['title','author','publisher','sales']) 


# book_new = CreateView.as_view()
def book_new1(request): # GET:template / POST:파라미터 변수를 받아 db에 save() -> book:list
  if request.method == 'POST':
    # title = request.POST['title']
    # author = request.POST['author']
    # publisher = request.POST['publisher']
    # sales = int(request.POST['sales'])
    # ip = request.META['REMOTE_ADDR'] # 요청한 client의 ip
    # book = Book(title=title, author=author, publisher=publisher, sales=sales, ip=ip)
    # book.save()
    # return redirect(book) # book.get_absolute_url의 return값이 자동생성
    form = BookModelForm(request.POST)
    # print('★ ', form.is_valid()) # 유효성 검증 결과
    # print('유효성 검사 결과 : ', form.cleaned_data) # 유효성 검증 결과
    if form.is_valid() : # 유효성 검사 
        # book = Book(**form.cleaned_data)
        # book.ip = request.META['REMOTE_ADDR'] #  요청한 client의 ip 지정하기위해 사용
        book = form.save(False)
        book.ip = request.META('REMOTE_ADDR')  #  요청한 client의 ip 지정하기위해 사용
        book.save()
        return redirect(book)
    # else:
    #   return render(request, 'book/book_form.html', {'form':form})
  elif request.method == 'GET':
    form = BookModelForm()
    return render(request, 'book/book_form.html',{'form':form})

book_edit = UpdateView.as_view(model=Book,
                              fields = ['title','author','publisher','sales']) 


def book_edit1(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
      form = BookModelForm(request.POST, instance=book) # 데이터베이스에서 그대로 가져오고 싶을때, instance=book  안하면 null로 
      if form.is_valid():
        book = form.save() # ip 수정 안 함, 수정 하려면 아래 3줄 처럼 
        # book = form.svae(False)
        # book.ip = request.META['REMOTE_ADDR']
        # book.save()
        return redirect(book)
    elif request.method == 'GET':
      form = BookModelForm(instance=book)
    return render(request, 'book/book_form.html', {'form':form})

book_delete = DeleteView.as_view(model=Book,
                                # template_name = "~", 
                                success_url = reverse_lazy("book:list"))

def book_delete1(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
      book.delete()
      return redirect(book)
    elif request.method == 'GET':
      return render(request, 'book/book_confirm_delete.html', {'object':book})