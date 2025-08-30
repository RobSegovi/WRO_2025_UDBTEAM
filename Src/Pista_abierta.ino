#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
//retroceso cuadno va a la izquierda es mucho y retroceso cuando va a derecha es muy poco 
//volataje og 6.70
//act 6.50
int pinServo = 10;
float y;
int theta = 0;
int imp=0;
LiquidCrystal_I2C lcd(0x27,16,2); 

// Definir un carácter personalizado (ejemplo: carita feliz)
byte up[8] = 
{
  B00100,
  B01110,
  B11111,
  B00100,
  B00100,
  B00100,
  B01110,
};
byte down[8] = 
{
  B01110,
  B00100,
  B00100,
  B00100,
  B11111,
  B01110,
  B00100,
};

// -- Motor --
int M1 = 4;
int M2 = 3;
int PWM = 2;

// --- tiempo ---  
long tiempo = 3000;
long tiempoactual = 0;
int numdelay = 72;
int numdelayexiz = 30;
int numdelayexde = 40 ;
int retrodelay = 800;
int delaygiz = 2200;
int delaygde = 2200;
// ---Varaibles de velocidad 
int vcorriz = 225;
int vcorrde =225;
int vgiriz = 245;
int vgirde = 245;
int vretro = 255;
int vavan =  200;
// --- Variables de comunicación ---
String inputString = "";
bool stringComplete = false;

// --- Variables Py ---
int indicador =0 ;   // 0 = nada, 1 = verde, 2 = rojo, 3 = naranjaDer, 4 = azulIzq, 5 = pared, 6 = correcion derecha, 7 = correcion izquierda.
long posX = 0;        // coordenada eje X
long area = 0;        // área del objeto
int guardar = 0;      //guardar indicador
int color = 0;
// --- milis const ---
unsigned long  tanterior = 0;
unsigned long esperadecor = 500;
unsigned long esperadecorder = 620;
unsigned long tinicio = 0;
bool prim = true;
bool corregir = false;
void setup() 
{
  origen(0);
  pinMode(pinServo, OUTPUT);
  lcd.init();
  lcd.backlight();
  lcd.createChar(0, up);
  lcd.createChar(1, down);
  delay(10);
  lcd.print("c:");
  for(int i = 2; i < 5; i++)
  {
    pinMode(i, OUTPUT);
  }

  Serial.begin(9600);
  digitalWrite(M1, LOW);
  digitalWrite(M2, LOW);

}
void loop()
{

  lectura();
  //avanzar 
  
  inicio: 
  if(posX==1) {
    color=1;
    lcd.setCursor(10,1);
    lcd.print("     ");
    lcd.setCursor(10,1);
    lcd.print("c:azul");
  }
  else if (posX==2){
    color=2;
        lcd.setCursor(10,1);
    lcd.print("     ");
    lcd.setCursor(10,1);
    lcd.print("c:naran");
  }

  if(indicador == 1)
  {
    pantalla(1);
    if (guardar == 2) // anterioriormente corriegio a la derecha
    {
      /*/izquierda(75, vcorriz, 10);//(angulo,velocidad,delay)
      for (int i=0 ; i<=numdelay; i++)
      {
       lectura();
       if(indicador== 4 || indicador == 5) goto inicio;
       delay(10);
      }/*/
    }
    else if (guardar == 3)//anteriormente corrigio a la izquierda
    {
     /*/ derecha(50, vcorrde, 10);//(angulo,velocidad,delay)
      for (int i=0 ; i<=numdelay; i++)
      {
       lectura();
       if(indicador== 4 || indicador == 5) goto inicio;
       delay(10);
      }/*/
    }
    else if(guardar == 5 )//girar a la derecha
    {
      origen(2);
    }
    else if( guardar == 4 )//girar a la izquierda
    {
      origen(1);
    }
    else origen(0);
    if(imp==0)
    {
      avanzar(245);
      delay(100);
      imp =1;
    }else
    {
    avanzar(vavan);
    guardar = indicador;
    }
    
    
  }
  else if(indicador == 2)//corregir a la derecha
  {
    unsigned long tactual = millis();  
    if(prim == true)
    {
      tinicio =  millis();
      prim = false;
    }
    if((tactual - tinicio) >= esperadecorder)
    {
      izquierda(75, vcorriz, 10);//(angulo,velocidad,delay)
      for (int i=0 ; i<=numdelayexde; i++)
      {
       lectura();
       if(indicador !=2)
        {
         prim =true;
         goto inicio;
        }
       delay(10);
      }


      prim =true;
      
      
    }
    pantalla(5);
    derecha(40, vcorrde, 0);//(angulo,velocidad,delay)
    guardar = indicador;
  }
  else if(indicador == 3)//correcion izquierda
  {
   
    unsigned long tactual = millis();  
    if(prim == true)
    {
      tinicio =  millis();
      prim = false;
    }
    if(tactual-tinicio >= esperadecor)
    {
      derecha(50, vcorriz, 300);//(angulo,velocidad,delay)
      for (int i=0 ; i<=numdelayexiz; i++)
      {
       lectura();
       if(indicador !=3)
        {
         prim =true;
         goto inicio;
        }
       delay(10);
      }

      prim =true;
      
      
    }
    pantalla(6);
    izquierda(71, vcorriz, 0);//(angulo,velocidad,delay)
    guardar = indicador;

  }
  //girar  a la izquierda
  else if(indicador == 4)//color azul
  {
    pantalla(4);
    izquierda(90, vgiriz, delaygiz);//(angulo,velocidad,delay)
    guardar = indicador;
    color = 1;
    lcd.setCursor(10,1);
    lcd.print("     ");
    lcd.setCursor(10,1);
    lcd.print("c:azul");
    
  }
  //girar a la derecha derecha
  else if(indicador == 5)//color naranja
  {
    pantalla(3);
    derecha(40, vgirde, delaygde);//(angulo,velocidad,delay)
    guardar = indicador;
    color = 2;
    lcd.setCursor(10,1);
    lcd.print("     ");
    lcd.setCursor(10,1);
    lcd.print("c:naran");
  }
   else if(indicador == 6)//pared, entonces retroceder y girar
  {
    pantalla(2); 
    if(guardar == 5 || color == 2)//girar a la derecha
    {
      Servo(90);// girar a la izquierda para movernos a la derecha
      retroceder(vretro);
      delay(retrodelay);
      //derecha(40, 225, 1500);//(angulo,velocidad,delay)
    }
    else if(guardar == 4 || color == 1)//girar a la izquierda
    {
      Servo(40);
      retroceder(vretro);
      delay(retrodelay);
      //izquierda(90, 225, 1500);//(angulo,velocidad,delay)
      
    }
    guardar = indicador;
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

void izquierda(int ang, int vel, int re)
{
  Servo(ang); //centro 
  avanzar(vel);
  delay(re);
}

void derecha(int ang, int vel, int re)
{
  Servo(ang); //centro 
  avanzar(vel);
  delay(re);

}

void origen(int k)
{
  if(k == 0) theta=66; //origen real.
  else if(k == 1) theta=68; //origen izquierda. viene de la izquierda
  else if(k == 2) theta=70; //origen derecha. viende de la izquierda
  Servo(theta);

}

// --- Servo sin libreria---
void Servo(float theta)
{
  for(int hz = 0; hz <= 50; hz++)
  {
    y = ((theta*2000.0)/180.0) + 500.0;
    digitalWrite(pinServo, HIGH);
    delayMicroseconds(y);
    digitalWrite(pinServo, LOW);
    delayMicroseconds(2000.0 - y);
    
  }
}

// --- LCD ---
void pantalla(int tv)
{
  if(tv == 1)
  {
    lcd.setCursor(0,0);
    lcd.write((byte)0);
    lcd.write((byte)0);
    lcd.write((byte)0);
    lcd.write((byte)0); 
    lcd.setCursor(0,1);
    lcd.write((byte)0);
    lcd.write((byte)0);
    lcd.write((byte)0);
    lcd.write((byte)0); 
  }
  else if(tv == 2)
  {
    lcd.setCursor(0,0);
    lcd.write((byte)1);
    lcd.write((byte)1);
    lcd.write((byte)1);
    lcd.write((byte)1); 
    lcd.setCursor(0,1);
    lcd.write((byte)1);
    lcd.write((byte)1);
    lcd.write((byte)1);
    lcd.write((byte)1);
  }
  else if(tv == 3)
  {
    lcd.setCursor(0,0);
    lcd.print(">>>>");
    lcd.setCursor(0,1);
    lcd.print(">>>>");
  }
  else if(tv == 4)
  {
    lcd.setCursor(0,0);
    lcd.print("<<<<");
    lcd.setCursor(0,1);
    lcd.print("<<<<");
  }
   else if(tv == 5)
  {
    lcd.setCursor(0,0);
    lcd.print("-->>");
    lcd.setCursor(0,1);
    lcd.print("-->>");
  }
    else if(tv == 6)
  {
    lcd.setCursor(0,0);
    lcd.print("<<--");
    lcd.setCursor(0,1);
    lcd.print("<<--");
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
      //delay(20);
      String LCDP0 = "i:" + String(indicador);

      

      lcd.setCursor(10,0);
      lcd.print(LCDP0);
      
     
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