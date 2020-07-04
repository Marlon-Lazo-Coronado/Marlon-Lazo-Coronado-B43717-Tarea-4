# Marlon-Lazo-Coronado-B43717-Tarea-4

Solución de la tarea #4 del curso Modelos Probabilisticos de señales y Sistemas.

Primero se desea mencionar que esta tarea se ha resuelto usando como base la solucion propuesta por el profesor Fabian Abarca para un problema similar de OOK en: https://github.com/fabianabarca/mpss/blob/master/Py8.ipynb. De hecho, el codigo es ensencialmente el mismo pero adaptado a BPSK porlo que la mayor parte del contenido intelectual de esta solucion es de su pertenencia.

Todas las graficas generadas se encuentran en la carpeta Graficas de este mismo repositorio. Se prefiere la revision del codigo ya que ahi esta todo debidamente comentado, ademas que no se tiene la costumbre de presentar resultados en el READMI por lo que puede ser poco estetico.


Punto 1. Crear un esquema de modulación BPSK para los bits presentados. Esto implica asignar una forma de onda sinusoidal normalizada (amplitud unitaria) para cada bit y luego una concatenación de todas estas formas de onda.

Para este y los demas apartados se tomaron 50 puntos de muestreo en vez de 10,000 a como se indica en el teorema del muestro de Nyquist ya que tarda mucho la simulacion y no genera errores para los SNR que se solicita.

Se establecieron parametros tales como la frecuencia de la portadora, el periodo de la señal, los puntos de muestro y la frecuencia de los bits y de aqui se generaron las señales portadoras de 1=sen y 0=-sen, tal y como se muestra en el siguiente enlace:
https://user-images.githubusercontent.com/65795065/86503820-01f3dd00-bd6f-11ea-9dc1-dce00ee46554.png

Una vez asignada una forma de onda para cada simbolo se procede a concatinar todaslas ondas para generar la señal tranmitida, tal y como se muestra en el siguiente fracmento de codigo:

    #Creamos la señal modulada
    for k,bit in enumerate(bits):
        if bit==1:
            señal[k*p:(k+1)*p]=seno_1
        else:
            señal[k*p:(k+1)*p]=seno_0

Generando la señal que transmitida:https://user-images.githubusercontent.com/65795065/86504430-58fcb080-bd75-11ea-87ca-2356f8809129.png



Punto 2.  Calcular la potencia promedio de la señal modulada generada.

Este punto es sencillo, basta con seguir las formaluas explicadas en el Py.8 por lo que se genera el siguiente fracmento de código:
    #Potencia instantanea
    dW=señal**2
    #Potencia promedio
    W=integrate.trapz(dW,ts)/((len(datos)+1)*T)
    print('La potencia promedio es: ', W )

En donde la unica diferencia esta en que los ceros si portan energia por lo que se obtiene una energia total de 0.49W. Para 50 puntos de muestreo.




Puntp 3. Simular un canal ruidoso del tipo AWGN (ruido aditivo blanco gaussiano) con una relación señal a ruido (SNR) desde -2 hasta 3 dB.

Para esta parte se realizo un bucle en el que se genera un vectro con los sigmas desde SMR=-3 hasta SMR=3, se ha calculado un alor de mas para poder hacer una mejor grafica en elpunto 6. Ademas en el mismo bucle se ha hecho la impresion de 6 graficas para las diferentes intensidades de potencia de ruido.

    SNR=0
    Vector_SNR=[]   #Inicializamos vectores
    Vector_sigma=[]
    
    for i in range(-3,4): # El enunciado dice de -2 a 3, yo tomo de -3 a 3 para tener mas puntos el la grafica del punto 6.
        SNR=i #Valormaximo
        #DesViacion estandar del ruido sigma
        sigma=(W/(10**(SNR/10)))**(1/2)
        #print('La potencia del ruido es: ',sigma)
    
        # Ahora vamos a generar el ruido (Potencia=sigma^2), np.random(media,potencia, forma)  
        ruido=np.random.normal(0,sigma, señal.shape)
        Vector_sigma.append(sigma)#Guardamos los valores de sigma 
        Vector_SNR.append(SNR)# Guardamos el vector de SNR para el punto 6
   
        
        #Creamos la señal recibida
        Rx=señal+ruido

        #Graficamos el ultimo ruido en 10 periodos de simbolo
        plt.plot(Rx[0:10*p])
        plt.xlabel('Tiempo(ms)')
        plt.ylabel('Amplitud')
        plt.title('Señal Recibida con sigma=%s' %sigma)
        #plt.legend(loc=1)
        plt.show()
        print('\nPara SNR de -3 a 3, la potencia del ruido sigma es: ',Vector_sigma)
    
 Por lo que se obtiene una serie de graficas con la señal recibida despues de pasar por el canal ruidoso, a continuacion se presenta la grafica en la que se aprecia la mayor cantidad de ruido. https://user-images.githubusercontent.com/65795065/86504697-10df8d00-bd79-11ea-91b5-67221a3ef799.png

Para encontrar una relacion de la potencia del ruido sigma, ha hecho el procedimiento matematico explicado en el py.8.
    '''
    SNR(dB)=Relacion señal a ruido
    SNR=10Log10(W/Wr)
    W/(10^(SNR/10))=Wr......... sigma=[W/(10^(SNR/10))]^(1/2)
    Wr=sigma^2'''
Los Vlores de sigma se pueden ver al correr el codigo.


Punto 4. Graficar la densidad espectral de potencia de la señal con el método de Welch (SciPy), antes y después del canal ruidoso.

Para graficar  la densidad espectral de potencia de la señal se utilizo el metodo welch, una vez mas esto biene resuelto en el py.8. Esto se hizo para la señal enviada y recibida.

    # Antes del canal ruidoso
    fw, PSD = signal.welch(señal, fs, nperseg=1024)
    plt.figure()
    plt.semilogy(fw, PSD)
    plt.xlabel('Frecuencia / Hz')
    plt.ylabel('Densidad espectral de potencia / V**2/Hz')
    plt.title('Señal Recibida con sigma=0')
    plt.show()
    
    # Después del canal ruidoso
    fw, PSD = signal.welch(Rx, fs, nperseg=1024)
    plt.figure()
    plt.semilogy(fw, PSD)
    plt.xlabel('Frecuencia / Hz')
    plt.ylabel('Densidad espectral de potencia / V**2/Hz')
    plt.title('Señal Recibida con sigma=0.4955')
    plt.show()

Generando como resultado las graficas.

https://user-images.githubusercontent.com/65795065/86504841-b6473080-bd7a-11ea-9b5a-577b39ddc713.png

https://user-images.githubusercontent.com/65795065/86504855-d4ad2c00-bd7a-11ea-970a-6e76189c0349.png


Punto 5. Demodular y decodificar la señal y hacer un conteo de la tasa de error de bits (BER, bit error rate) para cada nivel SNR.

Esta parte tambien se hizo utilizando el ejemplo dado por el profesor y añadiendo un ciclo for para calcular de manera iteratiba las tasas de error de bits y generar un vectos que permita graficar lo solicitado en elpunto 6.

    for n in Vector_sigma: #Vector_sigma es el vector con diferentes sigmas segun los SNR
    
        sigma_t=n
        #print(sigma_t)
        ruido=np.random.normal(0,sigma_t, señal.shape) #Recreamos el ruido para tener diferentes señales recibidas
        #Creamos la señal recibida
        Rx=señal+ruido
    
        for k in range(0,len(bits)): 
       
            Ep=np.sum(Rx[k*p:(k+1)*p]*seno_1)
        
            if Ep>Energia/2:
                bitsRx[k]=1
            else:
                bitsRx[k]=0
    
        #Contabilizamos la tasa de error
        err=np.sum(np.abs(bits-bitsRx))
    
        BER=err/(len(bits))
        Vector_Ber.append(BER)

En esta parte no se generan graficas unicamente tenemos dos vectores bitsRx que contiene los bits decodificados y Vector_Ber que contiene las tasas de error segun el SNR. Estos vectores pueden visualizarse al compilar el .py.



Punto 6. Graficar BER versus SNR.

Aqui solamente se grafican el vector Vector_SNR generado en el punto 5 contra el vector Vector_SNR generado en el punto 3.

    plt.plot(Vector_SNR,Vector_Ber,'ro') #Graficamos Vector_SNR vs Vector_Ber.
    plt.xlabel('Relacio Señal a Ruido SNR(dB)')
    plt.ylabel('Tasa de Error de bits BER')
    plt.title('SNR vs BER')
    #plt.legend(loc=1)
    plt.show()
    
 De aqui se obtiene la siguiente grafica: https://user-images.githubusercontent.com/65795065/86504949-38842480-bd7c-11ea-9a4c-443f9d4e33bb.png   
 En donde se puede ver claramente que la tasa de error ber cae de forma exponencial conforme aumente el SNR.
 
 Nuevamente se prefiere que se haga una revision directamente del .py para una mejor visualizacion de la tarea.













