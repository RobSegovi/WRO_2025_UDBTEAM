#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

int pinServo = 10;
float y;
int theta = 0;

LiquidCrystal_I2C lcd(0x27,16,2); 

// -- Motor --
int M1 = 4;
int M2 = 3;
int PWM = 2;

// --- tiempo ---  
long tiempo = 3000;
long tiempoactual = 0;

// --- Variables de comunicación ---
String inputString = "";
bool stringComplete = false;

// --- Variables Py ---
int indicador = 6;   // 0 = nada, 1 = verde, 2 = rojo, 3 = naranjaDer, 4 = azulIzq, 5 = pared.
long posX = 0;        // coordenada eje X
long area = 0;        // área del objeto
int guardar = 0;      //guardar indicador

void setup() 
{
  origen(0);
  pinMode(pinServo, OUTPUT);
  lcd.init();
  lcd.backlight();

  for(int i = 2; i < 5; i++)
  {
    pinMode(i, OUTPUT);
  }

  Serial.begin(9600);

}
void loop()
{
  lectura();
  if(indicador == 0)//no ve nada, entonces avanza.
  {
    origen(0);
    avanzar(255);
  }
  else if(indicador == 3)//color naranja, entonces girar a la derecha.
  {
    guardar = indicador;
    derecha(2);
    delay(3000);
  }
  else if(indicador == 4)//color azul, entonces girar a la izquierda
  {
    guardar = indicador;
    izquierda(2);
    delay(3000);
  }
  else if(indicador == 5)//pared, entonces retroceder y girar
  {
    retroceder(255);
    delay(1500);
    if(guardar == 3)//girar a la derecha
    {
      derecha(2);
      delay(3000);
    }
    else if(guardar == 4)//girar a la izquierda
    {
      izquierda(2);
      delay(3000);
    }
  }
}

// --- Funciones de movimiento ---
void avanzar(int fast) 
{
  analogWrite(PWM, fast);
  digitalWrite(M1, HIGH);
  digitalWrite(M2, LOW);
}

void retroceder(int fast) 
{
  analogWrite(PWM, fast);
  digitalWrite(M1, LOW);
  digitalWrite(M2, HIGH);
}

void detener() 
{
  digitalWrite(M1, LOW);
  digitalWrite(M2, LOW);
}

void izquierda(int i)
{
  if(i == 1) theta=85;
  else if(i == 2) theta=85;

  for(int hz = 0; hz <= 50; hz++)
  {
    Serial.println(theta);
    y = ((theta*2000.0)/180.0) + 500;
    digitalWrite(pinServo, HIGH);
    delayMicroseconds(y);
    digitalWrite(pinServo, LOW);
    delayMicroseconds(2000 - y);
  }
}

void derecha(int j)
{
  if(j == 1) theta=59;
  else if(j == 2) theta=59;

  for(int hz = 0; hz <= 50; hz++)
  {
    Serial.println(theta);
    y = ((theta*2000.0)/180.0) + 500;
    digitalWrite(pinServo, HIGH);
    delayMicroseconds(y);
    digitalWrite(pinServo, LOW);
    delayMicroseconds(2000 - y);
  }
}

void origen(int k)
{
  if(k == 0)theta=72; //origen real.
  else if(k == 1)theta=72; //origen izquierda.
  //else if(k == 2)theta=80; //origen derecha.
  
  for(int hz = 0; hz <= 50; hz++)
  {
    Serial.println(theta);
    y = ((theta*2000.0)/180.0) + 500;
    digitalWrite(pinServo, HIGH);
    delayMicroseconds(y);
    digitalWrite(pinServo, LOW);
    delayMicroseconds(2000 - y);
  }
}

// --- Lectura de datos desde la Raspberry ---
void lectura()
{
  if (stringComplete) 
  {
    stringComplete = false;

    // Separar por comas
    int firstComma = inputString.indexOf(',');
    int secondComma = inputString.indexOf(',', firstComma + 1);

    if (firstComma > 0 && secondComma > 0) 
    {
      // Extraer las 3 partes
      String indicadorStr = inputString.substring(0, firstComma);
      String xStr = inputString.substring(firstComma + 1, secondComma);
      String areaStr = inputString.substring(secondComma + 1);

      // Convertir a enteros
      indicador = indicadorStr.toInt();
      posX = xStr.toInt();
      area = areaStr.toInt();
      delay(20);

      // Mostrar en pantalla
      String LCDP = "i:" + String(indicador) + " X:" + String(posX);
      String Area = "Area: " + String(area);
      lcd.setCursor(2,0);
      lcd.print(" ");
      lcd.setCursor(6,0);
      lcd.print("        ");
      lcd.setCursor(0,0);
      lcd.print(LCDP);
      lcd.setCursor(5, 1);
      lcd.print("                ");
      lcd.setCursor(0, 1);
      lcd.print(Area);
    }
    inputString = ""; // limpiar para el siguiente mensaje
  }
}

// --- Captura de datos entrantes por Serial ---
void serialEvent() 
{
  while (Serial.available()) 
  {
    char inChar = (char)Serial.read();
    if (inChar == '\n') // fin del mensaje
    {       
      stringComplete = true;
    } 
    else 
    {
      inputString += inChar;
    }
  }
}