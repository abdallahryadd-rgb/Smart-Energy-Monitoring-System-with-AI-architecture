// ==========================================
// Smart Industrial Energy Monitor - Arduino Node
// ==========================================

float p1_now = 100.0, p1_t1 = 95.0, p1_t2 = 90.0;
float p2_now = 150.0, p2_t1 = 145.0, p2_t2 = 140.0;
float p3_now = 120.0, p3_t1 = 115.0, p3_t2 = 110.0;

void setup() {
  Serial.begin(9600);
  while (!Serial); 
  
  Serial.println("--- Industrial Energy Node Initialized ---");
}

void loop() {
  p1_now += random(-2, 3);
  p2_now += random(-3, 4);
  p3_now += random(-2, 2);


  Serial.print("P1: ");
  Serial.print(p1_now); Serial.print(", ");
  Serial.print(p1_t1);  Serial.print(", ");
  Serial.print(p1_t2);
  Serial.println();

  Serial.print("P2: ");
  Serial.print(p2_now); Serial.print(", ");
  Serial.print(p2_t1);  Serial.print(", ");
  Serial.print(p2_t2);
  Serial.println();

  Serial.print("P3: ");
  Serial.print(p3_now); Serial.print(", ");
  Serial.print(p3_t1);  Serial.print(", ");
  Serial.print(p3_t2);
  Serial.println();

  Serial.println("----------------------------------------");


  p1_t2 = p1_t1; p1_t1 = p1_now;
  p2_t2 = p2_t1; p2_t1 = p2_now;
  p3_t2 = p3_t1; p3_t1 = p3_now;

  delay(2000);
}
