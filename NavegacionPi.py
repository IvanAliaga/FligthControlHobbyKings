from RPIO import PWM
import time

#Constantes
PULSE_WIDTH_INCREMENT_GRANULARITY_US_KK = 1
AUX_ON                                  = 2018
AUX_OFF                                 = 1015
PIN_AILERON                             = 24    #Verde
PIN_ELEVATOR                            = 17    #Amarillo
PIN_THROTTLE                            = 25    #Rojo
PIN_RUDDER                              = 22    #Azul
PIN_AUXILIARY                           = 18    #Morado
AILERON_US_KK_DEFAULT                   = 1500  #Valor max es 1900 y valor min es 1100
ELEVATOR_US_KK_DEFAULT                  = 1500  #Valor max es 1900 y valor min es 1100
THROTTLE_US_KK_DEFAULT                  = 1100  #Valor max es 2400 y valor min es 1100
RUDDER_US_KK_DEFAULT                    = 1500  #Valor max es 1900 y valor min es 1100
#Outputs
aileron = PWM.Servo(0, PWM.SUBCYCLE_TIME_US_DEFAULT, PULSE_WIDTH_INCREMENT_GRANULARITY_US_KK)
elevator = PWM.Servo(0, PWM.SUBCYCLE_TIME_US_DEFAULT, PULSE_WIDTH_INCREMENT_GRANULARITY_US_KK)
throttle = PWM.Servo(0, PWM.SUBCYCLE_TIME_US_DEFAULT, PULSE_WIDTH_INCREMENT_GRANULARITY_US_KK)
rudder = PWM.Servo(0, PWM.SUBCYCLE_TIME_US_DEFAULT, PULSE_WIDTH_INCREMENT_GRANULARITY_US_KK)
auxiliary = PWM.Servo(0, PWM.SUBCYCLE_TIME_US_DEFAULT, PULSE_WIDTH_INCREMENT_GRANULARITY_US_KK)

class NavegacionPi():
      def __init__(self):
         aileron.set_servo(PIN_AILERON, AILERON_US_KK_DEFAULT)
         time.sleep(0.5)#(0.00001)
         elevator.set_servo(PIN_ELEVATOR, ELEVATOR_US_KK_DEFAULT)
         time.sleep(0.5)
         throttle.set_servo(PIN_THROTTLE, THROTTLE_US_KK_DEFAULT)
         time.sleep(0.5)
         rudder.set_servo(PIN_RUDDER, RUDDER_US_KK_DEFAULT)
         time.sleep(0.5)
         self.auxiliary_bool(True)
         time.sleep(0.5)
         print("Pulso inicializado")
         print("Cargando ..")
         time.sleep(1)
         print("Cargando ...")
         time.sleep(1)  
         print("Navegacion Pi listo")
       
      def auxiliary_bool(self, condicion):
          if condicion:
            auxiliary.set_servo(PIN_AUXILIARY, AUX_ON)
          else:
            auxiliary.set_servo(PIN_AUXILIARY, AUX_OFF)
     
      def arm_model(self):
          rudder.set_servo(PIN_RUDDER, 1100)
          time.sleep(2)
          rudder.set_servo(PIN_RUDDER, RUDDER_US_KK_DEFAULT)
          print("Modelo armado y listo para volar")
          time.sleep(1)

      def disarm_model(self):
          rudder.set_servo(PIN_AUXILIARY, 1900)
          time.sleep(2)
          rudder.set_servo(PIN_AUXILIARY, RUDDER_US_KK_DEFAULT)
          print("Modelo desarmado")
          time.sleep(1)
     
      def full_throttle(self):
          throttle.set_servo(PIN_THROTTLE, 2390)
     
      def idle_throttle(self):
          throttle.set_servo(PIN_THROTTLE, RUDDER_US_KK_DEFAULT)
      
      def get_value(self, data = "", separator = "", index = 0):
          found = 0
          str_index = [0, -1]  
          max_index = len(data)-1
          for i in range(0, max_index+1):
             if found <= index:
               if data[i] == separator or i == max_index:
                 found = found + 1
                 str_index[0] = str_index[1] + 1
                 if i == max_index:
                    str_index[1] = i + 1
                 else:
                    str_index[1] = i
          if found > index:
             return data[str_index[0]:str_index[1]]
          else:
             return ""
       
      def stop(self):
          throttle.stop_servo(PIN_THROTTLE)
          rudder.stop_servo(PIN_RUDDER)
          aileron.stop_servo(PIN_AILERON)
          elevator.stop_servo(PIN_ELEVATOR)
          auxiliary.stop_servo(PIN_AUXILIARY)

      def send_data(self, data):
          time.sleep(0.001)
          word1 = self.get_value(data, "_", 0)
          word2 = self.get_value(data, "_", 1)
          
          #if word1 == "+":
          #   self.full_throttle()
          #elif word == "-":
          #   self.idle_throttle() 	
          if word1 == "TH":
             throttle.set_servo(PIN_THROTTLE, int(word2))
             time.sleep(0.4)
             print("Throttle speed :" + str(word2))  
          elif word1 == "RD":
             rudder.set_servo(PIN_RUDDER, int(word2))
             time.sleep(0.4)
             print("Rudder:" + str(word2))
          elif word1 == "AI":
             aileron.set_servo(PIN_AILERON, int(word2))
             time.sleep(0.4)
             print("Aileron :" + str(word2))
          elif word1 == "EL":
             elevator.set_servo(PIN_ELEVATOR, int(word2))
             time.sleep(0.4)
             print("Elevator :" + str(word2))
          elif word1 == "AUX":
             if word2 == "ON":
                self.auxiliary_bool(True)
                time.sleep(0.4)
                print("Self-Level is ON")
             elif word2 == "OFF":
                self.auxiliary_bool(False)
                time.sleep(0.4)
                print("Self-Level is OFF")
          elif word1 == "ARM":
             self.arm_model()
             time.sleep(0.4)
          elif word1 == "DARM":
             self.disarm_model()
             time.sleep(0.4)
          time.sleep(0.001)
