from django.shortcuts import render, redirect
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
# Create your views here.

def unlikey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    return redirect("board:detail", bpk)

def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(request.user)
    return redirect("board:detail", bpk)

def index(request):
    cate = request.GET.get("cate", "")
    kw = request.GET.get("kw","")
    pg = request.GET.get("page", 1)
    
    
    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            from acc.models import User
            try:
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none()
        elif cate == "con":
            b = Board.objects.filter(content__contains=kw)
    else:
        b = Board.objects.all()
        
    s = b.count()

    pag = Paginator(b, 2)
    obj = pag.get_page(pg)
    context = {
        "bset" : obj,
        "cate" : cate,
        "kw" : kw,
        "s":s
    }
    return render(request, "board/index.html", context)


def dreply(request, bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if r.replyer == request.user:
        r.delete()
    else:
        pass # 혼내줘야댐
    return redirect("board:detail", bpk)

def creply(request, bpk):
    b = Board.objects.get(id=bpk)
    c = request.POST.get("con")
    Reply(b=b, comment=c, replyer=request.user).save()
    return redirect("board:detail", bpk)


def update(request, bpk):
    b = Board.objects.get(id=bpk)
    
    if b.writer != request.user:
        return redirect("board:index")

    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        b.subject , b.content = s,c
        b.save()
        return redirect("board:detail", bpk)
    context = {
        "b" : b
    }
    return render(request, "board/update.html", context)


def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        Board(subject=s, content=c, pubdate=timezone.now(), writer=request.user).save()
        return redirect("board:index")
    return render(request, "board/create.html")



def delete(request, bpk):
    b = Board.objects.get(id=bpk)
    if b.writer == request.user:
        b.delete()
    else:
        pass # 혼내줘야함
    return redirect("board:index")

def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()

    context = {
        "b" : b,
        "rset" : r
    }
    return render(request, "board/detail.html", context)
