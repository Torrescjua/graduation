# Regalo para Daniela — guía rápida

## 1. Cómo editar el contenido

Abre `index.html` con cualquier editor de texto (Notas, VS Code, etc.) y busca estos puntos:

- **Contraseña de entrada**: en la parte de abajo del archivo busca `CONFIG.mainPasswords`. Ahí están las palabras que abren la página (por ahora: `daniela` y `dany`). Puedes agregar o cambiar las que quieras, escritas en minúscula.
- **Contraseña de la sección privada**: `CONFIG.innerPasswords` (por ahora: `dany kyss godt`). No importan mayúsculas ni espacios de más, el sistema los ignora.
- **Fecha del contador "tiempo juntos"**: `CONFIG.startDate`. Está puesta como `new Date(2023, 1, 14, ...)` — el `1` es el mes (0 = enero, 1 = febrero, etc.) así que ese `14` es el día exacto. Ajústalo a la fecha real que quieras usar.
- **Línea de tiempo**: busca el comentario `<!-- LÍNEA DE TIEMPO -->`. Cada bloque `.timeline-item` tiene una fecha (`.timeline-date`) y un texto (`.timeline-text`). Puedes agregar, quitar o editar los que quieras copiando el mismo formato.
- **La carta**: busca `<!-- CARTA -->` y reemplaza el texto dentro de `.letter-body` por el que tú quieras. Los saltos de línea se respetan tal cual los escribas.
- **Sección privada**: el texto está en `.inner-msg`, dentro de `#inner-content`. Cámbialo por lo que quieras decirle ahí, sin que nadie más lo vea.

## 2. Fotos y videos del regalo

Las fotos y videos ya están enumerados y preparados para la página dentro de `fotos/`:

- Galería pública: `foto-001.jpg` a `foto-076.jpg`.
- Videos: `video-001.mp4` a `video-024.mp4` / `.mov`.
- Los originales permanecen en `fotos/Photos-1-001/`. Las fotos HEIC fueron convertidas a JPG para asegurar que se vean en navegadores y en Netlify.

No necesitas tocar el código: todas las fotos y videos enumerados aparecen automáticamente. Si agregas más material, actualiza `galleryCount` o la lista `videoFiles` en `CONFIG` (arriba de `index.html`).

También puedes usar el botón **“Agregar fotos”** dentro de la página. Las fotos se guardan en el navegador desde el que las agregaste y se mantienen al volver a abrir la página allí. Para que aparezcan para todas las personas que visiten el sitio, colócalas igualmente en `fotos/`, enuméralas y vuelve a publicar la carpeta en Netlify.

## 3. Recursos para animaciones

En `recursos-animaciones/` puedes subir imágenes decorativas o ilustraciones que quieras incorporar a futuras animaciones visuales. Esta carpeta no modifica la página automáticamente.

Consejo: comprime las fotos antes (por ejemplo con [squoosh.app](https://squoosh.app)) para que la página cargue rápido — con que cada foto pese menos de 1-2 MB va perfecto.

## 3. Cómo publicarla gratis con su nombre en la URL (Netlify)

Netlify es gratis, no pide tarjeta y te da un enlace tipo `https://daniela-y-juan.netlify.app` (tú eliges el nombre).

1. Entra a [app.netlify.com](https://app.netlify.com) y crea una cuenta gratis (con tu correo o con GitHub/Google).
2. Ya adentro, busca el botón **"Add new site" → "Deploy manually"**.
3. Arrastra toda la carpeta `regalo-daniela` (la que contiene `index.html` y `fotos/`) al recuadro que dice "Drag and drop your site folder here". En unos segundos queda publicada con una URL aleatoria.
4. Para ponerle su nombre: entra al sitio recién creado → **"Site configuration" → "Change site name"** → escribe algo como `daniela-y-juan` o `paradaniela` (debe estar disponible, sin espacios ni tildes) → Guardar.
5. Tu URL final quedará como `https://ese-nombre.netlify.app`. Ese es el link que le compartes a Daniela.

Para actualizar la página en el futuro (si cambias fotos o textos), vuelve a "Deploys" en ese mismo sitio y arrastra la carpeta actualizada otra vez — Netlify la reemplaza sin cambiar la URL.

### Alternativa: GitHub Pages
El proyecto ya incluye un flujo automático de GitHub Pages. Tras subirlo a la rama `main`, en el repositorio abre **Settings → Pages** y selecciona **GitHub Actions** como fuente. Cada cambio enviado a `main` publicará el sitio en `https://torrescjua.github.io/graduation/`.

## 4. Antes de enviarle el link

- Ábrela tú primero (doble clic en `index.html`) para revisar que todo se vea y lea como quieres.
- Recuerda decirle a Daniela la palabra clave de entrada de otra forma (en persona, por mensaje, etc.) — la página no la muestra en ningún lado.
