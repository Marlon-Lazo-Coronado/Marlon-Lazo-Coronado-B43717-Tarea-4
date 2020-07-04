# Marlon-Lazo-Coronado-B43717-Tarea-4

Solución de la tarea #4 del curso Modelos Probabilisticos de señales y Sistemas.

Primero se desea mencionar que esta tarea se ha resuelto usando como base la solucion propuesta por el profesor Fabian Abarca para un problema similar de OOK en: https://github.com/fabianabarca/mpss/blob/master/Py8.ipynb. De hecho, el codigo es ensencialmente el mismo pero adaptado a BPSK porlo que la mayor parte del contenido intelectual de esta solucion es de su pertenencia.

Todas las graficas generadas se encuentran en la carpeta Graficas de este mismo repositorio.


Punto 1. Crear un esquema de modulación BPSK para los bits presentados. Esto implica asignar una forma de onda sinusoidal normalizada (amplitud unitaria) para cada bit y luego una concatenación de todas estas formas de onda.

Para este y los demas apartados se tomaron 50 puntos de muestreo en vez de 10,000 a como se indica en el teorema del muestro de Nyquist ya que tarda mucho la simulacion y no genera errores para los SNR que se solicita.

Se establecieron parametros tales como la frecuencia de la portadora, el periodo de la señal, los puntos de muestro y la frecuencia de los bits y de aqui se generaron las señales portadoras de 1 y 0, tal y como se muestra en el siguiente enlace:
https://user-images.githubusercontent.com/65795065/86503820-01f3dd00-bd6f-11ea-9dc1-dce00ee46554.png

Una vez asignada una forma de onda para cada simbolo se procede a concatinar todaslas ondas para generar la señal tranmitida, tal y como se muestra en el siguiente fracmento de codigo:

    #Creamos la señal modulada
    for k,bit in enumerate(bits):
        if bit==1:
            señal[k*p:(k+1)*p]=seno_1
        else:
            señal[k*p:(k+1)*p]=seno_0

0bteniendo como resultado la grafica que se encuentra en: https://github.com/Marlon-Lazo-Coronado/Marlon-Lazo-Coronado-B43717-Tarea-4/blob/master/Solucion_Tarea4/Graficas/2_Se%C3%B1al_Embiada.png
