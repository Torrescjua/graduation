# Regalo para Daniela — guía rápida

## Cómo está organizada la carpeta

```
regalo-daniela/
├─ sitio/               ← carpeta que publica GitHub Pages
│  ├─ index.html        (diseño + contenido cifrado; no se edita a mano, salvo CONFIG)
│  ├─ retrato.webp      (foto de la portada)
│  ├─ favicon.svg
│  └─ fotos/            (se completa al publicar desde fotos.enc)
├─ fotos/               ← medios locales; no se guardan en Git sin cifrar
├─ fotos.enc            ← archivo cifrado que usa GitHub Actions
├─ secreto/             ← NUNCA se sube. Aquí editas los textos y las claves
│  ├─ contenido.html    (hero, contador, logros, carta, estructura de capítulos)
│  ├─ privado.html      (la rosa eterna y el mensaje del capítulo privado)
│  └─ claves.json       (claves de entrada y clave privada)
├─ cifrar.js            ← mete secreto/ dentro de sitio/index.html, cifrado
├─ organizar_fotos.py   ← renombra y comprime tus fotos hacia fotos/
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

Esta protección aplica al sitio publicado, no al repositorio fuente: `secreto/`
y `cifrar.js` siguen versionados. Mantén privado el repositorio; si alguna vez
fue público, borrar esos archivos en un commit nuevo no elimina su historial.

Las fotos y videos se guardan cifrados en `fotos.enc` dentro del repositorio.
GitHub Actions los descifra durante la publicación y los copia a `sitio/fotos/`.
En el sitio publicado, los archivos multimedia pueden abrirse si alguien conoce
su URL directa; el candado privado solo controla su aparición en la página, no
es una barrera de acceso al archivo.

## Cómo editar textos o claves

1. Edita `secreto/contenido.html` (o `privado.html`, o `claves.json`).
2. En una terminal, dentro de `regalo-daniela/`:
   ```
   node cifrar.js
   ```
   (necesita Node 19 o más nuevo: `node -v` para comprobar).
3. Sube los cambios a `main`; GitHub Pages publicará `sitio/` automáticamente.

Nunca publiques `secreto/` ni `cifrar.js`: GitHub Pages publica solo `sitio/`.

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
`sitio/index.html`, en el bloque `CONFIG` del final. Para fotos privadas, agrega
el nombre a `privateFiles` (por ejemplo `privado-001.jpeg`); no hace falta editar
`secreto/privado.html`, que ya contiene el mosaico privado. Copia el archivo con
ese nombre en `fotos/` antes de volver a cifrar los medios.

## Las fotos

```
python organizar_fotos.py /ruta/a/tu/carpeta/con/todas/las/fotos
```

Copia (nunca mueve ni borra el original) las fotos y videos a
`fotos/`, renombrados en orden cronológico, y las comprime si tienes
Pillow (`pip install pillow`). Si el número no es 76/24, te imprime el
bloque `CONFIG` para pegar en `sitio/index.html`.

Después de agregar o cambiar medios, vuelve a cifrar el archivo que se publica:

```powershell
$pass = Read-Host "Clave de medios" -AsSecureString
.\tools\protect-media.ps1 -Passphrase $pass
Remove-Variable pass
```

Escribe la clave en el prompt seguro; no la guardes en el comando ni en el
repositorio. GitHub Actions necesita esa misma clave como secreto
`MEDIA_PASSPHRASE`.

Mientras no estén, la página no se rompe: el mosaico muestra un aviso y los
videos que faltan no aparecen.

## Publicar con GitHub Pages

1. En GitHub, configura el secreto del repositorio `MEDIA_PASSPHRASE` con la
  clave usada para cifrar `fotos.enc`.
2. En **Settings → Pages**, elige **GitHub Actions** como origen.
3. Sube los cambios a la rama `main`; la acción descifra los medios, prepara
  `sitio/` y publica solo esa carpeta.

La URL se muestra en **Settings → Pages**. Para Netlify manual, primero hay que
preparar `sitio/fotos/` con los medios descifrados, igual que hace la acción.

## Antes de mandarle el enlace

- Corre `node cifrar.js` después del último cambio de texto y abre
  `sitio/index.html` para comprobar la página.
- Dile la contraseña por otro medio. Las pistas del candado las escribiste
  tú; si te parecen demasiado directas, cámbialas en `sitio/index.html`
  (buscar "Pista") y en `secreto/contenido.html` (capítulo 06).
- Los videos deben ser `.mp4`.
