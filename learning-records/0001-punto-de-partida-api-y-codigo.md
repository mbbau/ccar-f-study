# Punto de partida: fundamentos de la Messages API y nivel de código

Matías llega con el modelo mental de OpenAI (creía que `content` era un JSON con `choices`) y no conocía dónde va el `system` ni que la API es stateless; sí sabía que las tools las ejecuta el código de la aplicación. Es especialista en datos, no desarrollador: entiende qué pide un ejercicio de código pero no llega a escribir un loop agéntico completo desde cero.

**Evidence:** diagnóstico de 4 preguntas del 28/9 (3 sin saber o incorrectas, 1 correcta). En el Lab 01 el autocompletado le generó la solución y necesitó guía paso a paso para depurarla; resolvió solo el bug del `import` y ubicar el `while` a partir de pistas.

**Implications:** no asumir fundamentos por experiencia con otros SDKs; comparar con OpenAI funciona como puente. Labs en escalones (leer y predecir → completar huecos → escribir entero opcional), con el autocompletado desactivado. Evaluar la fecha del examen con el repaso del Día 10.
