# @appi.get("/logout")
# async def logout(request: Request):
#     response = RedirectResponse(url="/", status_code=302)
#     response.delete_cookie(key="token")
#     response.delete_cookie(key="token_type")
#     return response



# from fastapi import FastAPI, HTTPException
# import requests

# app = FastAPI()

# @app.get("/grafica")
# async def obtener_grafica():
#     #esta funcion le envia el id a la api que va a generar el grafico la api de el puerto 80  
#     # Hacer una solicitud GET a la API en el puerto 8080 para obtener la gráfica
    
#     try:
#         response = requests.post("http://localhost:8080/obtener_id")
#         response = requests.get("http://localhost:8080/obtener_grafica")
#         response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa
#         grafica = response.content  # Obtener el contenido de la respuesta (la imagen de la gráfica)
#     except requests.RequestException as e:
#         raise HTTPException(status_code=500, detail="Error al obtener la gráfica de la API en el puerto 8080")

#     # Renderizar el HTML con la gráfica insertada
#     html_con_grafica = f"""
#     <html>
#     <head>
#         <title>Gráfica</title>
#     </head>
#     <body>
#         <h1>Gráfica</h1>
#         <img src="data:image/png;base64,{grafica.decode('utf-8')}" alt="Gráfica generada">
#     </body>
#     </html>
#     """

#     return HTMLResponse(content=html_con_grafica, status_code=200)
