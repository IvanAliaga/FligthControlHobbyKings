#!/usr/bin/python
'''
Created on 05/06/2014

@author: ivanaliaga
'''
import time
import serial


arduino = serial.Serial()
arduino.port = '/dev/ttyACM0'
arduino.baudrate = 9600

class Navegacion():

      #arduino = serial.Serial()
      #arduino.port = '/dev/ttyACM0'
      #arduino.baudrate = 9600
      
      def abrir_puerto(self):
          if(arduino.isOpen()):
             print("Puerto serial abierto")
          else:
             try:
                arduino.open()
	        print("Cargando.")
                time.sleep(1)
                print("Cargando..")
                time.sleep(2)
                print("Cargando...")
                print("Conexion Exitosa! :-)")
	     except Exception, e:
                arduino.close()
                print("Oops! Algo salio mal " + str(e))

      def cerrar_puerto(self):
          if(arduino.isOpen()):
             arduino.close()
          else:
             print("Puerto serial cerrado")
      
      def control(self, pitch='', roll='', yaw=''):
          lista = [pitch, roll, yaw]
          try:
             arduino.flushInput()
             arduino.flushOutput()
             if(arduino.isOpen()):
	        for elemento in lista:
                   arduino.write(elemento)
                   time.sleep(0.5)
                   print("Envio exitoso control " + str(elemento)) 
             else:
                print("No se puede abrir el puerto serial")
          except Exception, e1:
              arduino.close()
              print("Error comunicando...: " + str(e1))
     
      def aceleracion(self, throttle=''):          
	  try:
             arduino.flushInput()
             arduino.flushOutput()
             if(arduino.isOpen()):
                arduino.write(throttle)
                time.sleep(0.5)
                print("Envio exitoso : Throttle " + str(throttle))
             else:
                print("No se puede abrir el puerto serial")
          except Exception, e1:
              print("Error comunicando...: " + str(e1))
    
      def auxiliar(self, aux=''):
          try:
             arduino.flushInput()
             arduino.flushOutput()
             if(arduino.isOpen()):
                arduino.write(aux)
                time.sleep(0.5)
                print("Envio exitoso : Aux " + str(aux))
             else:
                print("No se puede abrir el puerto serial")
          except Exception, e1:
              print("Error comunicando...: " + str(e1))

      def estado(self, state=''):
          try:
             arduino.flushInput()
             arduino.flushOutput()
             if(arduino.isOpen()):
                arduino.write(state)
                time.sleep(0.5)
                print("Envio exitoso : State " + str(state))
             else:
                print("No se puede abrir el puerto serial")
          except Exception, e1:
              print("Error comunicando...: " + str(e1))

