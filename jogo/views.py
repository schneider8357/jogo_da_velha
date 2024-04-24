from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from jogo.helpers import venceu
from jogo.models import Jogo, Board



def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return HttpResponse("nao foi possivel realizar login: usuario ou senha incorretos", status_code=401) 

def novo_jogo_da_velha(request):
    jogador1 = get_object_or_404(User, username=request.POST.get("jogador1"))
    jogador2 = get_object_or_404(User, username=request.POST.get("jogador2"))
    novo_jogo = Jogo(
        jogador1=jogador1,
        jogador2=jogador2,
        senha=request.POST.get("senha"),
    )
    novo_jogo.board = Board()
    novo_jogo.board.save()
    novo_jogo.save()
    return redirect(f"/jogo-da-velha/?jogo={novo_jogo.id}")


def jogo_da_velha(request):
    id_jogo = request.POST.get("jogo") or request.GET.get("jogo")
    jogo = get_object_or_404(Jogo, id=id_jogo)
    if not request.POST.get("senha"):
        return render(request, "digite_senha.html", context={"id_jogo": jogo.id})
    board = [
        jogo.board.tile0, jogo.board.tile1, jogo.board.tile2,
        jogo.board.tile3, jogo.board.tile4, jogo.board.tile5,
        jogo.board.tile6, jogo.board.tile7, jogo.board.tile8,
    ]
    tile_clicado = request.POST.get("tile")
    print(f"{board=}, {tile_clicado=} {jogo.venc=}")
    if request.user == jogo.jogador1:
        jogador_clicou = 1
    elif request.user == jogo.jogador2:
        jogador_clicou = 2
    else:
        jogador_clicou = None
    if tile_clicado and jogador_clicou == jogo.proximo and board[int(tile_clicado)-1] is None and not jogo.venc:
        print(f"{tile_clicado=}")
        board[int(tile_clicado)-1] = "X" if jogo.proximo == 1 else "O"
        if (venceu(board[0], board[1], board[2]) or
            venceu(board[3], board[4], board[5]) or
            venceu(board[6], board[7], board[8]) or
            venceu(board[0], board[3], board[6]) or
            venceu(board[1], board[4], board[7]) or
            venceu(board[2], board[5], board[8]) or
            venceu(board[0], board[4], board[8]) or
            venceu(board[2], board[4], board[6])
        ):
            jogo.venc = jogo.proximo
            # TODO salvar estado do board no banco de dados ( e as outras coisas ) 
        jogo.proximo = 2 if jogo.proximo == 1 else 1
        jogo.board.tile0 = board[0]
        jogo.board.tile1 = board[1]
        jogo.board.tile2 = board[2]
        jogo.board.tile3 = board[3]
        jogo.board.tile4 = board[4]
        jogo.board.tile5 = board[5]
        jogo.board.tile6 = board[6]
        jogo.board.tile7 = board[7]
        jogo.board.tile8 = board[8]
        jogo.board.save()
        jogo.save()
        print(board)
    return render(request, "jogo_da_velha.html", context={
        "id_jogo": jogo.id,
        "jogador1": jogo.jogador1,
        "jogador2": jogo.jogador2,
        "proximo": jogo.proximo,
        "board": board,
        "vencedor": jogo.venc,
        "senha": request.POST.get("senha")})

def jogos_anteriores(request):
    jogos = Jogo.objects.all()
    return render(request, "jogos_anteriores.html", context={
        "jogos": jogos
    })



