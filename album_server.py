from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        albums_quantity = len(album_names)
        result = "<h2>У артиста {} нашлось {} альбомов:</h2> <br>".format(artist, albums_quantity)
        result += "<ol><li>"
        result += "<li>".join(album_names)
        result += "</ol>"
    return result

@route("/albums", method="POST")
def artist():
    getyear=request.forms.get("year")
    getartist=request.forms.get("artist")
    getgenre=request.forms.get("genre")
    getalbum=request.forms.get("album")
    findalbum_list = album.findalbum(getalbum)
    try:
        # Проверяем год на число, провоцируем ошибку, которую обрабатываем
        getyearint = int(getyear)
        if findalbum_list:
            message = "Альбом {} уже есть в базе".format(getalbum)
            result = HTTPError(409, message)
        else:
            album.newartist(getyear, getartist, getgenre, getalbum)
            result = "<h3>В базу добавлен альбом {} артиста {}</h3>".format(getalbum, getartist)
        return result
    except ValueError as v_error:
        message = "Ошибка {}. Введенные данные {} не являются годом".format(v_error, getyear)
        result = HTTPError(409, message)
        return result
    

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)