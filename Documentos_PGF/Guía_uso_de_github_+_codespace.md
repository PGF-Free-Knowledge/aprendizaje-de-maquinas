# GUÍA PASO A PASO: USO DE GITHUB + CODESPACE

🔹 1. Iniciar trabajo

Ingresa a tu repositorio en GitHub.

Haz clic en el botón verde Code → pestaña Codespaces.

Abre el proyecto con Open in browser.
→ Esto abre tu entorno de trabajo en línea (similar a VS Code, pero dentro del navegador).



🔹 2. Estructura de la pantalla

📁 Explorador (izquierda): muestra carpetas y archivos.

🧾 Editor (centro): donde editas el código o los archivos Markdown.

💬 Terminal (abajo): donde se escriben los comandos git.
Si no está visible → menú View → Terminal o clic en el ícono >_ abajo.


🔹 3. Flujo básico de sincronización
Cada vez que trabajes:

Editar archivos → guarda con Ctrl+S.

Abrir Terminal (abajo) y escribir:

git status


(muestra qué cambió)

Agregar cambios al control de versión:

git add .


Registrar (commit) los cambios:

git commit -m "Descripción breve de lo que hiciste"


Subir cambios al repositorio (GitHub):

git push


✅ Eso guarda tu trabajo en GitHub y lo deja disponible desde cualquier PC.


🔹 4. Cuando trabajes desde otro computador o Codespace

Antes de hacer cualquier cambio:

git pull


Esto descarga los últimos cambios desde GitHub al entorno actual, evitando conflictos.


🔹 5. Si aparece un conflicto

Lee el mensaje en la terminal.

Si ves “both modified” o “merge conflict”, no te preocupes:

Edita o elimina los archivos duplicados (según el caso).

Luego escribe:

git add .
git commit -m "Conflicto resuelto"
git push


Con eso se limpia y sincroniza todo.


🔧 COMANDOS GIT DE USO COMÚN
| Acción            | Comando                   | Descripción breve              |
| ----------------- | ------------------------- | ------------------------------ |
| Ver estado        | `git status`              | Muestra qué archivos cambiaron |
| Agregar archivos  | `git add .`               | Incluye todos los cambios      |
| Registrar cambios | `git commit -m "mensaje"` | Guarda los cambios localmente  |
| Subir a GitHub    | `git push`                | Sube al repositorio remoto     |
| Descargar cambios | `git pull`                | Trae lo más reciente de GitHub |
| Cancelar merge    | `git merge --abort`       | Detiene una fusión con error   |
| Ver historial     | `git log --oneline`       | Muestra los commits recientes  |



🧰 TERMINAL Y VS CODE (equivalencias)
| Herramienta                      | Qué es                                 | Dónde se usa                    |
| -------------------------------- | -------------------------------------- | ------------------------------- |
| **Terminal**                     | Línea de comandos dentro del Codespace | Abajo en la pantalla            |
| **VS Code (Visual Studio Code)** | Editor local (en tu PC)                | Solo si trabajas sin Codespaces |
| **Codespaces**                   | VS Code en la nube (dentro de GitHub)  | Lo que uso ahora                |


No se necesita instalar VS Code localmente, ya que Codespaces tiene todo integrado.

💡 RECOMENDACIÓN DE USO DIARIO

Al comenzar el día:

git pull


Trabaja y guarda (Ctrl + S).

Al terminar:

git add .
git commit -m "avance del día"
git push


Con eso nunca perderé avances ni generaré conflictos.

Gentileza PGF
