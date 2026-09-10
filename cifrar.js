#!/usr/bin/env node
/*
  cifrar.js — mete el contenido de secreto/ dentro de sitio/index.html, cifrado.

  Uso (desde la carpeta regalo-daniela):
      node cifrar.js

  Qué hace:
    - Lee secreto/claves.json, secreto/contenido.html y secreto/privado.html.
    - Genera una llave aleatoria por bloque y cifra el HTML con AES-256-GCM.
    - Esa llave se "envuelve" una vez por cada clave válida (PBKDF2-SHA256,
      200.000 iteraciones), así puede haber varias claves de entrada.
    - Escribe el resultado en los <script type="application/json"> de
      sitio/index.html. El texto original NO queda en el sitio.

  Sin la clave correcta, lo que hay en index.html es ruido: ni "ver código
  fuente" ni quitar el candado con las herramientas del navegador sirven.
  Requiere Node 19 o superior (tiene crypto.subtle incorporado).
*/
const fs = require('fs');
const path = require('path');
const { webcrypto } = require('crypto');
const subtle = webcrypto.subtle;

const ROOT = __dirname;
const ITER = 200000;
const enc = new TextEncoder();
const norm = s => s.trim().toLowerCase().replace(/\s+/g, ' ');   // igual que en la página
const b64 = buf => Buffer.from(buf).toString('base64');

async function deriveKey(password, salt) {
  const base = await subtle.importKey('raw', enc.encode(password), 'PBKDF2', false, ['deriveKey']);
  return subtle.deriveKey(
    { name: 'PBKDF2', salt, iterations: ITER, hash: 'SHA-256' },
    base, { name: 'AES-GCM', length: 256 }, false, ['encrypt']);
}

async function seal(text, passwords) {
  const key = webcrypto.getRandomValues(new Uint8Array(32));
  const iv = webcrypto.getRandomValues(new Uint8Array(12));
  const contentKey = await subtle.importKey('raw', key, 'AES-GCM', false, ['encrypt']);
  const ct = await subtle.encrypt({ name: 'AES-GCM', iv }, contentKey, enc.encode(text));
  const wraps = [];
  for (const pw of passwords) {
    const salt = webcrypto.getRandomValues(new Uint8Array(16));
    const wiv = webcrypto.getRandomValues(new Uint8Array(12));
    const kek = await deriveKey(norm(pw), salt);
    const wct = await subtle.encrypt({ name: 'AES-GCM', iv: wiv }, kek, key);
    wraps.push({ salt: b64(salt), iv: b64(wiv), ct: b64(wct) });
  }
  return JSON.stringify({ iter: ITER, iv: b64(iv), ct: b64(ct), wraps });
}

function putBlob(html, id, json) {
  const re = new RegExp(`(<script type="application/json" id="${id}">)[\\s\\S]*?(</script>)`);
  if (!re.test(html)) throw new Error(`No encuentro <script id="${id}"> en sitio/index.html`);
  return html.replace(re, `$1${json}$2`);
}

(async () => {
  const claves = JSON.parse(fs.readFileSync(path.join(ROOT, 'secreto/claves.json'), 'utf8'));
  const contenido = fs.readFileSync(path.join(ROOT, 'secreto/contenido.html'), 'utf8');
  const privado = fs.readFileSync(path.join(ROOT, 'secreto/privado.html'), 'utf8');
  if (!claves.principal?.length || !claves.privada?.length) throw new Error('claves.json necesita "principal" y "privada" con al menos una clave');

  const indexPath = path.join(ROOT, 'sitio/index.html');
  let html = fs.readFileSync(indexPath, 'utf8');
  html = putBlob(html, 'blob-main', await seal(contenido, claves.principal));
  html = putBlob(html, 'blob-private', await seal(privado, claves.privada));
  fs.writeFileSync(indexPath, html);

  // comprobación: ningún fragmento del texto original quedó en el sitio
  const muestra = contenido.match(/<p[^>]*>([^<]{20,})</)?.[1];
  if (muestra && html.includes(muestra)) throw new Error('El texto quedó sin cifrar; revisa el archivo');

  console.log('Listo: sitio/index.html actualizado con el contenido cifrado.');
  console.log(`  claves de entrada: ${claves.principal.length} · claves privadas: ${claves.privada.length}`);
  console.log('  Recuerda: la carpeta secreto/ NUNCA se sube a Netlify.');
})().catch(e => { console.error('Error:', e.message); process.exit(1); });
