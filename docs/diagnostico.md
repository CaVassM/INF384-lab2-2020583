# 1.1 -> Fallas del Pipeline

- Como primer error, es el hecho de que los jobs se encuentren independientes.
  Es decir, el job de publicar no depende del job validar; por tanto, cualquier cambio u commit
  que se envíe y no pase las pruebas, pasarán al 2do step sin garantizar su calidad.
- Como segundo error, se muestra que descarga nuevamente el repositorio, obteniendo así en su totalidad 
  como dos repositorios redundantes, los cuales no se puede garantizar su reproducibilidad al haber sido ejecutados en diferentes
  tiempos, pues puede que las librerías hayan cambiado con el tiempos
- Como tercer error, se realiza instalación de librerías por medio de un requirements en ambos ambientes, mas
  no se utiliza el lock que se encuentra implementado en el repositorio. Grave puesto que el lock sí garantiza
  reproducibilidad entre las versiones.
- Como cuarto error, no se cachea las librerías, pues no se encuentra instanciado el valor cache en ninguno de los dos 
  jobs.

  
# 1.2 -> Defectos que explican la duración
- Considero lo que genera demoras son las instalaciones de las librerías. Si bien se reducen (ej_1 con un tiempo de 46 seg,
  mientras que los restantes de 33 seg, esto debido al caché), el indicar a la máquina en verificar e instalar nuevamente 
  los paquetes requeridos para el proyecto, actualizar no solo el gestor sino también estas librerías, son las que generan
  retardo. Con lock podría reducirse pues sería una versión fija e inmutable al reproducir el pipeline más veces.

# 1.3 -> Vinculo con su caso  


# 1.4 -> Metrica DORA

# 1.5 -> Proxy
