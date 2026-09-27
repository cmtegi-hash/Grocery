# Lista de mercado

Dos partes:

- **`pc_app.py`** — app de Streamlit que corres en tu PC para administrar
  el catálogo y la lista activa, y sincronizar a GitHub.
- **`docs/`** — la PWA que abres desde el iPhone. Solo lee la lista y
  permite marcar/desmarcar ítems como comprados (guardado en el propio
  teléfono).

## 1. Crear el repositorio en GitHub

1. Crea un repositorio nuevo en GitHub (puede ser público).
2. Sube el contenido de esta carpeta tal cual (incluyendo `docs/` y `data/`).

## 2. Activar GitHub Pages

1. En el repositorio, ve a **Settings → Pages**.
2. En "Source", elige la rama `main` y la carpeta `/docs`.
3. Guarda. GitHub te dará una URL, algo como:
   `https://tu-usuario.github.io/tu-repo/`

## 3. Conectar la PWA con tu archivo de datos

Abre `docs/index.html` y busca esta línea cerca del inicio del `<script>`:

```js
const JSON_URL = "https://raw.githubusercontent.com/TU-USUARIO/TU-REPO/main/data/lista_mercado.json";
```

Reemplaza `TU-USUARIO` y `TU-REPO` por los tuyos. Guarda y vuelve a subir
el cambio a GitHub.

## 4. Correr la app de la PC

```bash
pip install -r requirements.txt
streamlit run pc_app.py
```

Esto abre la app en tu navegador. Cada vez que agregues ítems o quites
los que ya compraste, se guarda en `data/lista_mercado.json`. Al
presionar **"Sincronizar al iPhone"**, la app hace automáticamente
`git add`, `git commit` y `git push` de ese archivo.

> Nota: para que el botón de sincronizar funcione, la carpeta del
> proyecto debe ser un repositorio git ya conectado a GitHub (con
> `git remote add origin ...` configurado y tus credenciales guardadas,
> por ejemplo con un token o SSH). Si el push automático falla, la app
> te avisa y puedes subirlo tú mismo con los mismos comandos.

## 5. Instalar la PWA en el iPhone

1. Abre en Safari la URL de GitHub Pages del paso 2.
2. Toca el ícono de compartir → **"Agregar a inicio"**.
3. Listo — se abre como una app, con su propio ícono.

## Cómo funciona el día a día

- **En la PC**: agregas ítems nuevos (o los seleccionas del catálogo si
  ya los habías comprado antes), y quitas los que ya compraste.
- **Sincronizas** antes de salir de casa.
- **En el iPhone**: abres la app, tocas "Actualizar" para traer lo más
  reciente, y marcas cada ítem conforme lo pones en el carrito — esto
  funciona sin internet una vez que la lista se descargó.
- **De vuelta en casa**: en la PC, quitas de la lista activa lo que sí
  compraste. Lo que no encontraste se queda ahí para la próxima vez.
