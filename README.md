# Regalo para Daniela — guía rápida

## Cómo está organizada la carpeta

```
regalo-daniela/
├─ sitio/               ← LA ÚNICA carpeta que se sube a Netlify
│  ├─ index.html        (diseño + contenido cifrado; no se edita a mano, salvo CONFIG)
│  ├─ retrato.webp      (foto de la portada)
│  ├─ favicon.svg
│  └─ fotos/            (foto-001.jpg … y video-001.mp4 …)
├─ secreto/             ← NUNCA se sube. Aquí editas los textos y las claves
│  ├─ contenido.html    (hero, contador, logros, carta, estructura de capítulos)
│  ├─ privado.html      (la rosa eterna y el mensaje del capítulo privado)
│  └─ claves.json       (claves de entrada y clave privada)
├─ cifrar.js            ← mete secreto/ dentro de sitio/index.html, cifrado
├─ organizar_fotos.py   ← renombra y comprime tus fotos hacia sitio/fotos/
└─ README.md
```

## Seguridad: por qué ya nadie puede entrar sin la clave

Antes, la carta, el mensaje privado y las dos claves estaban escritas tal
cual dentro del HTML: cualquiera con el enlace podía abrir "ver código
fuente" y leerlo todo sin contraseña. Ahora **el contenido va cifrado**
(AES-256-GCM, con la llave derivada de la clave mediante PBKDF2). En
`sitio/index.html` solo hay ruido; la clave correcta lo descifra en el
navegador de quien la escribe, y la clave equivocada no descifra nada.
Quitar el candado con las herramientas del navegador tampoco sirve: detrás
no hay nada que mostrar.

Cada bloque tiene su propia llave: la clave de entrada abre la página y
la clave privada abre el capítulo 06. Puede haber varias claves de entrada
(hoy: `daniela` y `dany`); no importan mayúsculas ni espacios de más.

Lo único que sigue sin cifrar son las **fotos y videos** dentro de
`sitio/fotos/`: alguien que adivine el nombre exacto del archivo (por
ejemplo `…/fotos/foto-001.jpg`) podría abrirlo directo. Los nombres no se
listan en ningún lado y el enlace es privado, así que en la práctica solo
lo vería quien ya tiene el sitio; si quieres cerrar también esa puerta,
se puede cifrar las fotos igual que los textos, dímelo.

## Cómo editar textos o claves

1. Edita `secreto/contenido.html` (o `privado.html`, o `claves.json`).
2. En una terminal, dentro de `regalo-daniela/`:
   ```
   node cifrar.js
   ```
   (necesita Node 19 o más nuevo: `node -v` para comprobar).
3. Vuelve a subir la carpeta `sitio/` a Netlify.

Nunca subas `secreto/` ni `cifrar.js`: solo la carpeta `sitio/`.

**La carta** va por hojas. Cada `<div class="page">` es una hoja; agrega o
quita las que quieras y la numeración se ajusta sola. Ahora la hoja toma el
alto de la página que se está leyendo (cambia con suavidad al pasar), así
que las páginas no tienen por qué ser del mismo largo. Escribe cada párrafo
en una línea larga sin cortarla a mano.

**Los logros** (capítulo 02) se editan en `contenido.html`, bloque por
bloque (`.when` = título, `.what` = detalle). Daniela además puede agregar
los suyos desde la página; esos quedan guardados solo en su navegador.

**El retrato** es `sitio/retrato.webp`; reemplázalo por otro con el mismo
nombre (cuadrado, 700×700 o más). Si falta, la portada sigue funcionando.

**Fecha del contador y lista de fotos/videos**: es lo único que se edita en
`sitio/index.html`, en el bloque `CONFIG` del final.

## Las fotos

```
python3 organizar_fotos.py /ruta/a/tu/carpeta/con/todas/las/fotos
```

Copia (nunca mueve ni borra el original) las fotos y videos a
`sitio/fotos/`, renombrados en orden cronológico, y las comprime si tienes
Pillow (`pip install pillow`). Si el número no es 76/24, te imprime el
bloque `CONFIG` para pegar en `sitio/index.html`.

Mientras no estén, la página no se rompe: el mosaico muestra un aviso y los
videos que faltan no aparecen.

## Publicar gratis con su nombre en la URL (Netlify)

1. [app.netlify.com](https://app.netlify.com) → cuenta gratis.
2. **Add new site → Deploy manually**.
3. Arrastra la carpeta **`sitio/`** (solo esa) al recuadro.
4. **Site configuration → Change site name** → por ejemplo `daniela-grado`.
5. Queda en `https://daniela-grado.netlify.app`.

Para actualizar: **Deploys** → arrastrar `sitio/` otra vez. La URL no cambia.

## Antes de mandarle el enlace

- Corre `node cifrar.js` después del último cambio de texto y ábrela tú
  (doble clic en `sitio/index.html`) con las fotos puestas.
- Dile la contraseña por otro medio. Las pistas del candado las escribiste
  tú; si te parecen demasiado directas, cámbialas en `sitio/index.html`
  (buscar "Pista") y en `secreto/contenido.html` (capítulo 06).
- Los videos deben ser `.mp4`.
