from django.shortcuts import render, redirect, HttpResponse, get_object_or_404

from jogo.helpers import venceu
from jogo.models import Jogo, Board

# # X == 1, O == 2
# estados_jogos = {
#     1: {
#         "players": ["fulano", "beltrano"], 
#         "proximo": 1, 
#         "board": [
#             None, None, None, 
#             None, None, None, 
#             None, None, None
#         ],
#         "vencedor": None,
#     },
# }

def index(request):
    return render(request, "index.html")

def novo_jogo_da_velha(request):
    novo_jogo = Jogo(jogador1=request.GET.get("jogador1"), jogador2=request.GET.get("jogador2"))
    novo_jogo.board = Board()
    novo_jogo.board.save()
    novo_jogo.save()
    return redirect(f"/jogo-da-velha/?jogo={novo_jogo.id}")


def jogo_da_velha(request):
    jogo = get_object_or_404(Jogo, id=request.GET.get("jogo"))
    board = [
        jogo.board.tile0, jogo.board.tile1, jogo.board.tile2,
        jogo.board.tile3, jogo.board.tile4, jogo.board.tile5,
        jogo.board.tile6, jogo.board.tile7, jogo.board.tile8,
    ]
    tile_clicado = request.GET.get("tile")
    if tile_clicado and board[int(tile_clicado)-1] is None and jogo.venc is None:
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
    jogo.save()
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
    return render(request, "jogo_da_velha.html", context={
        "id_jogo": jogo.id,
        "jogador1": jogo.jogador1,
        "jogador2": jogo.jogador2,
        "proximo": jogo.proximo,
        "board": board,
        "vencedor": jogo.venc})
