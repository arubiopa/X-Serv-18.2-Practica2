from django.shortcuts import render
from models import Pages
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

def formulario():
    return ( "<form method='POST'>FORMULARIO:<input type='text'name='valor' value='' /><button type='submit'> Acortar</button></form>")


def imprimourls():
    urloginial = ""
    urlacortada = ""
    resultado = ""
    for url in Pages.objects.all():
        urlacortada = "<a href='http://127.0.0.1:8000/"+ str(url.id) + "'>"+ "http://127.0.0.1:8000/"+str(url.id) + "</a>"
        urloginial = "<a href='" + url.pagina + "'>"+ url.pagina + "</a>"
        resultado = "<p>Pagina: " + str(urloginial) + "</br> URL acortada:"+ str(urlacortada) +"</p>"
    return resultado

@csrf_exempt
def acortaurl(request, recurso):
    cuerpo = request.body
    if request.method == "GET":
        if recurso == "":
            return HttpResponse(formulario() + imprimourls())
        else:
            try:
        		contenido = Pages.objects.get(id=recurso)
        		return HttpResponseRedirect(contenido.pagina)
            except Pages.DoesNotExist:
        		return HttpResponseNotFound("<h1>Pagina no encontrada:</h1><p><a href='http://127.0.0.1:8000'>formulario</a></p>")

    if request.method == "POST":
        resultado = ""
        cuerpo = request.body.split('=')[1]
        if cuerpo.find("http%3A%2F%2F") >=  0:
            cuerpo = cuerpo.split('http%3A%2F%2F')[1]
        cuerpo = "http://" + cuerpo
        if cuerpo == "":
            return HttpResponseNotFound(formulario() + "URL no introducida")
        try:
            contenido = Pages.objects.get(pagina=cuerpo)
            resultado += "URL original: " + cuerpo + " ---->URL ya acortada: " + str(contenido.id)
        except Pages.DoesNotExist:
            pagina = Pages(pagina=cuerpo)
            pagina.save()
            resultado = "<p> Pagina acortada: " + cuerpo + " </p>" + imprimourls()

        return HttpResponse(resultado +"<p><a href='http://127.0.0.1:8000'>formulario</a></p>")
