x = [];
seno_esc = [];
coseno_esc = [];
i = 0.0;

while i <= 360.0 do
  rad = (i * 3.14159) / 180;
  s = sin(rad);
  c = cos(rad);

  x = x + [i];
  seno_esc = seno_esc + [s * 10 + 10];
  coseno_esc = coseno_esc + [c * 10 + 10];

  i = i + 5.0;
done;

plot(x, seno_esc);
plot(x, coseno_esc);

