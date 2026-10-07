# Criterios de revisión: tipo de problema, no rol de la medida

En el Lab 03 Matías llegó a 17/17, pero escribir criterios explícitos le costó más que reconocerlos en un quiz (6/6 en la lección). Sus primeros `NO_REPORTAR` describían el *rol* de una medida (placeholder, formato condicional) en lugar del *tipo de hallazgo* a omitir (estilo, nombres). Su primer criterio de performance ("todo lo que implique joins") era tan amplio que habría generado falsos positivos en casi todo el modelo. Y agregó un ejemplo few-shot de "reportar" que ningún criterio cubría. Las tres cosas se resolvieron con la pregunta "¿qué haría Claude con esta medida concreta?".

**Evidence:** lab 03, 7/10: 13/17 → 15 → 16 → 17 en cuatro iteraciones; necesitó la palabra "engañoso" dada explícitamente. El fix del promedio ponderado: propuso `AVERAGEX(precio*m3/m3)` (se cancela) y no llegó solo a `DIVIDE(SUMX(...), SUM(m3))`; prefiere validar DAX contra un modelo real.

**Implications:** reconocer ≠ producir. En los próximos labs de prompts (Día 04 extracción, Día 15 distractores) pedirle que *escriba* criterios y ejemplos y probarlos con el escenario "sos Claude, te llega esta entrada". Reforzar la regla: criterios y ejemplos tienen que contar la misma historia. No evaluar DAX en el aire: si un lab lo necesita, dar la fórmula o un modelo real.
