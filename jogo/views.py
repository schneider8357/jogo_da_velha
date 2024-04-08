from django.shortcuts import render

# X == 1, O == 2
estados_jogos = {
    1: {"players": ["fulano", "beltrano"], "proximo": 1, "board": [None, None, None, None, None, None, None, None, None]},
}

def index(request):
    return render(request, "index.html")


def jogo_da_velha(request):
    estado = estados_jogos[1]
    tile_clicado = request.GET.get("tile")
    if tile_clicado:
        print(f"{tile_clicado=}")
        estado["board"][int(tile_clicado)-1] = "X" if estado["proximo"] == 1 else "O"
        estado["proximo"] = 2 if estado["proximo"] == 1 else 1
    return render(request, "jogo_da_velha.html", context={
        "jogador1": estado["players"][0],
        "jogador2": estado["players"][1],
        "proximo": estado["proximo"],
        "board": estado["board"]})
