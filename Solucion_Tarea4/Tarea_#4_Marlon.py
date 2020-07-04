#Universidad de Costa Rica 
#Modelos Probabilisticos de Señales y Sistemas
#Marlon Lazo Coronado B43717
#Tarea 4

import pandas as pd
import numpy as np
from scipy import stats
from scipy import signal
from scipy import integrate
import matplotlib.pyplot as plt


def main():

    ############# Punto 1 #########################
    
    datos=pd.read_csv('bits10K.csv', header=0)
    
    #Frecuencia del la portadora
    f=5000 #Hz
    
    #Periodo del simbolo y de la portadora
    T=1/f
    
    #Numero de puntos del muestreo por el teorema de nyquist p = 2f = 10,000 como minimo.
    #Pero para no durar tanto la simulacion lo dejamos en 50 y para generar ruido y gragicar en punto 6.
    p=50
    print('Todo lo demas es con base a 50 puntos de muestreo\n')

    #Tempo de muestro por periodo
    tp=np.linspace(0,T,p)
    #print(tp)

    #Creamos la portadora
    seno_1=np.sin(2*np.pi*f*tp)
    seno_0=-np.sin(2*np.pi*f*tp)

    #Esto es para probar
    plt.plot(tp,seno_1)
    plt.xlabel('Tiempo(ms)')
    plt.ylabel('Amplitud')
    plt.title('Portadora para un 1')
    #plt.legend(loc=1)
    plt.show()

    #Frecuencia de muestreo
    fs=p/T
    
    #len(datos)+1=9999+1=10000
    #Creamos el tiempo en el que se transmite toda la señal, todos los bits
    ts=np.linspace(0,(len(datos)+1)*T,(len(datos)+1)*p)    #Es probable que aya que sumarle 1
    #print(len(datos))

    #Inicializamos el vector de la señal
    señal=np.zeros((len(datos)+1)*p) #cantidad de bits por cantidad de puntos


    #Convertimos el dataframe en numpy array, e insertamos el primer 
    #elemente que por alguna razon se pierde
    temporal1=datos.to_numpy()
    bits = np.insert(temporal1,0, [[0]])      
    #print(len(bits))
    #print(bits)
    

    #Creamos la señal modulada
    for k,bit in enumerate(bits):
        if bit==1:
            señal[k*p:(k+1)*p]=seno_1
        else:
            señal[k*p:(k+1)*p]=seno_0
            
    # El periodo en el que segrafica la señal depende del numero de puntos de muestra
    
    #Graficamos la señal modulada en 10 periodos
    plt.plot(señal[0:10*p])
    plt.xlabel('Tiempo(ms)')
    plt.ylabel('Amplitud')
    plt.title('Señal Transmitida')
    #plt.legend(loc=1)
    plt.show()
    
    
    
    
    
    # Punto 2. Calcular la potencia promedio de la señal enviada.
    
    #Potencia instantanea
    dW=señal**2
    #Potencia promedio
    W=integrate.trapz(dW,ts)/((len(datos)+1)*T)
    print('La potencia promedio es: ', W )
    
    
    
    
    
    
    # Punto 3. Creamos la señal transmitida para diferentes potencias de ruido
    '''
    SNR(dB)=Relacion señal a ruido
    SNR=10Log10(W/Wr)
    W/(10^(SNR/10))=Wr......... sigma=[W/(10^(SNR/10))]^(1/2)
    Wr=sigma^2'''
    
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




    # PUNTO 4: Graficar la densidad espectral de potencia de la señal con el método de Welch (SciPy), antes y después del canal ruidoso.
    
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
    
    
    
    
    
    
    
    ############# PUNTO 5: Demodular y decodificar ################
    Energia=np.sum(seno_1**2)  #Formula de la energia en la señal
    
    #Inicializamos el vector de bits recibidos
    bitsRx=np.zeros(len(bits))
    
    Vector_Ber=[] #Para guardar los BER para cada SNR
    
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
        
    print('\nPara un SNR que va desde -3 a 3 la las tasas de erro de bist (BER) son: ',Vector_Ber)
    
    
    ########### Punto 6. Graficar BER versus SNR. ################
    plt.plot(Vector_SNR,Vector_Ber,'ro') #Graficamos Vector_SNR vs Vector_Ber.
    plt.xlabel('Relacio Señal a Ruido SNR(dB)')
    plt.ylabel('Tasa de Error de bits BER')
    plt.title('SNR vs BER')
    #plt.legend(loc=1)
    plt.show()


main()



###################### Guardamos codigo ##########################

 #Para generar vector de binario tipo numpy.array
 #X=stats.bernoulli(0.5)
 #bits=X.rvs(10)
 #print(type(bits))



#Convertimos el dataframe en numpy array
    #temporal1=datos.to_numpy()
    #bits = np.insert(temporal1,0, [[0]])      
    #print(len(bits))
    #print(len(datos))



    #Otra forma de convertir el dataframe a array
    #datosarray = np.array(datos)



''' #Decodificacion de la señal mediante la deteccion de la energia
    
    for k in range(0,len(bits)): #No estamos usando b, debedia de quita a bits
        Ep=np.sum(Rx[k*p:(k+1)*p]*seno_1)
        
        if Ep>Energia/2:
            bitsRx[k]=1
        else:
            bitsRx[k]=0
    #print(bitsRx)
    
    
    #Contabilizamos la tasa de error
    
    err=np.sum(np.abs(bits-bitsRx))
    
    BER=err/(len(bits))
    
    print('\nPara una potencia de ruido sigma de: ',Vector_sigma[6])
    print('La tasa de error de bits es: ',BER)'''








