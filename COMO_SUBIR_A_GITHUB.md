# 🚀 Cómo subir OptiBottle a GitHub y activar GitHub Pages

Esta guía te lleva de cero a tener tu proyecto en línea con su propia página web. **Tiempo estimado: 20-30 minutos.**

---

## 📝 Paso 1: Crear cuenta en GitHub (si no tienes)

1. Ve a [github.com](https://github.com)
2. Haz clic en **Sign up** (esquina superior derecha)
3. Llena tus datos. Usa tu correo escolar si quieres.
4. Verifica tu correo

> 💡 **Tip:** Elige un username que se vea profesional, lo verás en la URL del proyecto. Ej: `juanperez` mejor que `xXgamer_69Xx`.

---

## 📁 Paso 2: Crear el repositorio

1. Una vez logueado, haz clic en el botón **+** arriba a la derecha → **New repository**
2. Llena el formulario:
   - **Repository name:** `optibottle`
   - **Description:** `Sistema de información para optimización de producción de botellas plásticas - PIA Sistemas de Información`
   - **Visibility:** ✅ **Public** (público — necesario para GitHub Pages gratis)
   - ⚠️ **NO marques** "Add a README file" (ya tienes uno)
   - ⚠️ **NO agregues** .gitignore ni license desde aquí
3. Clic en **Create repository**

Te llevará a una página con instrucciones. Déjala abierta y pasa al siguiente paso.

---

## 💻 Paso 3: Subir tu proyecto (elige UNA opción)

### 🟢 Opción A — La más fácil: arrastrar y soltar (sin terminal)

1. En la página de tu repo nuevo, busca el link que dice: **"uploading an existing file"**
2. **Descomprime** tu archivo `optibottle_codigo_fuente.zip` en tu computadora
3. Abre la carpeta `optibottle` que se creó
4. **Selecciona TODOS los archivos y carpetas que están adentro** (Ctrl+A)
5. Arrástralos a la página de GitHub (donde dice "drag files here")
6. Abajo, en "Commit changes":
   - Mensaje: `Subida inicial del proyecto OptiBottle`
   - Clic en **Commit changes**

✅ ¡Listo! Tu código ya está en GitHub.

### 🔵 Opción B — Con Git desde la terminal (más pro)

```bash
# 1. Descomprime el ZIP y entra a la carpeta
cd optibottle

# 2. Inicializa Git
git init
git branch -M main

# 3. Conecta con tu repo (reemplaza TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/optibottle.git

# 4. Agrega y sube los archivos
git add .
git commit -m "Subida inicial del proyecto OptiBottle"
git push -u origin main
```

> Si te pide credenciales, GitHub ya no acepta tu contraseña normal. Necesitas un **Personal Access Token**. Para el PIA es más fácil la Opción A.

---

## 🌐 Paso 4: Activar GitHub Pages (la página web)

1. En tu repositorio, haz clic en la pestaña **Settings** (arriba a la derecha)
2. En el menú de la izquierda, busca y haz clic en **Pages**
3. En la sección **Build and deployment**:
   - **Source:** `Deploy from a branch`
   - **Branch:** Selecciona `main` y luego la carpeta `/docs` (¡importante!)
   - Clic en **Save**
4. Espera 1-2 minutos. Recarga la página de Settings → Pages.
5. Aparecerá un mensaje verde con tu URL:
   ```
   ✅ Your site is live at https://TU_USUARIO.github.io/optibottle/
   ```

---

## 🎨 Paso 5: Personalizar (opcional pero recomendado)

### Actualiza los links de GitHub en la página

Edita el archivo `docs/index.html`:
- Busca `https://github.com/` (aparece 2 veces)
- Reemplaza con: `https://github.com/TU_USUARIO/optibottle`

### Actualiza el README

Edita `README.md`:
- Reemplaza `TU_USUARIO` con tu username real (aparece varias veces)

### Para editar archivos directo desde GitHub:
1. Abre el archivo en GitHub
2. Clic en el ícono del lápiz ✏️ (arriba a la derecha)
3. Haz los cambios
4. Abajo: **Commit changes**

---

## ✅ Paso 6: Verifica que todo funciona

Abre tu sitio: `https://TU_USUARIO.github.io/optibottle/`

Deberías ver:
- ✅ La landing page con el dashboard mockup
- ✅ Las secciones de problema/solución, módulos
- ✅ Los 3 manuales con botones "Ver" y "Descargar"
- ✅ Al hacer clic en "Ver", se abre el PDF en el navegador

---

## 📤 ¿Qué entregar al profesor?

Tienes **dos opciones** según cómo le guste recibir las cosas:

### Si quiere archivos sueltos (lo normal):
- Los 3 PDFs (Manual Técnico, Manual de Usuario, Guion)
- El ZIP del código
- El video que grabaste
- **El link a tu repositorio de GitHub** (esto es lo que suma puntos extra)

### Si todo en uno:
- Solo el **link a tu GitHub Pages**: `https://TU_USUARIO.github.io/optibottle/`
  - Desde ahí se puede ver y descargar todo

---

## 🆘 Problemas comunes

### "404 - Page not found" al abrir mi GitHub Pages
- Asegúrate de haber seleccionado la carpeta `/docs` y no `/root` en Settings → Pages
- Espera 5 minutos, a veces tarda en publicarse la primera vez

### Los PDFs no se ven en el visor
- Algunos navegadores móviles bloquean PDFs incrustados. El botón "Descargar PDF" siempre funcionará.

### Subí el código pero no veo la carpeta `docs`
- Asegúrate de haber subido TODOS los archivos del proyecto, incluyendo carpetas ocultas

### Quiero cambiar algo después de subirlo
- Edita el archivo directo desde GitHub (ícono del lápiz) y guarda los cambios
- GitHub Pages se actualiza automáticamente en 1-2 minutos

---

## 🎯 Tips para impresionar al profe

1. **Pin el repo** en tu perfil de GitHub (botón "Pin" en el repo). Así aparece destacado.
2. **Agrega una descripción** al repo (engranaje arriba a la derecha).
3. **Incluye el link de GitHub Pages** en la "About" section del repo.
4. Al entregar, menciona: *"El proyecto está versionado en GitHub y tiene página web propia con GitHub Pages."* — Eso ya te separa del 90% de los equipos.

---

**¡Listo! Cualquier duda, vuelve a este archivo. 🚀**
