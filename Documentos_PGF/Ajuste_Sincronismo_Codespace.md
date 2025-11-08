# Resolución de conflicto Git en Codespaces

Este es el registro completo del proceso de resolución de conflicto entre la carpeta `Instrumentos_ELO` y sus archivos duplicados.

---

### 💻 Registro del terminal

```bash
@PGF-Free-Knowledge ➜ /workspaces/aprendizaje-de-maquinas (main) $ git config pull.rebase false
@PGF-Free-Knowledge ➜ /workspaces/aprendizaje-de-maquinas (main) $ git pull
CONFLICT (rename/rename): Documentos_PGF/Instrumentos _ELO/analisis_instruementos.ipynb renamed to ...
...
@PGF-Free-Knowledge ➜ /workspaces/aprendizaje-de-maquinas (main) $ git push
Enumerating objects: 26, done.
...
@PGF-Free-Knowledge ➜ /workspaces/aprendizaje-de-maquinas (main) $

Secuencia de solución - Error de sincronismo

@PGF-Free-Knowledge ➜ /workspaces/aprendizaje-de-maquinas (main) $ git config pull.rebase false
@PGF-Free-Knowledge ➜ /workspaces/aprendizaje-de-maquinas (main) $ git pull
CONFLICT (rename/rename): Documentos_PGF/Instrumentos _ELO/analisis_instruementos.ipynb renamed to Documentos_PGF/Instrumentos_ELO/analisis_instruementos.ipynb in HEAD and to Documentos_PGF/Instrumentos_ELO/analisis_instrumentos.ipynb in 8c60cccf7bc2ab2302a7f2222b814fa411037a75.
CONFLICT (file location): Documentos_PGF/Instrumentos _ELO/analisis_instruementos.ipynb renamed to Documentos_PGF/Instrumentos _ELO/analisis_instrumentos.ipynb in 8c60cccf7bc2ab2302a7f2222b814fa411037a75, inside a directory that was renamed in HEAD, suggesting it should perhaps be moved to Documentos_PGF/Instrumentos_ELO/analisis_instrumentos.ipynb.
CONFLICT (file location): Documentos_PGF/Instrumentos _ELO/documentacion_instrumentos.md added in 8c60cccf7bc2ab2302a7f2222b814fa411037a75 inside a directory that was renamed in HEAD, suggesting it should perhaps be moved to Documentos_PGF/Instrumentos_ELO/documentacion_instrumentos.md.
Automatic merge failed; fix conflicts and then commit the result.
@PGF-Free-Knowledge ➜ /workspaces/aprendizaje-de-maquinas (main) $ git status
On branch main
Your branch and 'origin/main' have diverged,
and have 2 and 15 different commits each, respectively.
  (use "git pull" if you want to integrate the remote branch with yours)

You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Changes to be committed:
        new file:   "Documentos_PGF/Teor\303\255a/Clase 1.pdf"
        new file:   "Documentos_PGF/Teor\303\255a/Clase 2.pdf"
        new file:   "Documentos_PGF/Teor\303\255a/Clase 3.pdf"
        new file:   "Documentos_PGF/Teor\303\255a/Clase 4.pdf"
        new file:   "Documentos_PGF/Teor\303\255a/Clase 5.pdf"
        new file:   Documentos_PGF/Videos/Links Videos Universidad de Chile
        new file:   Documentos_PGF/Videos/Links.md

Unmerged paths:
  (use "git add/rm <file>..." as appropriate to mark resolution)
        both deleted:    Documentos_PGF/Instrumentos _ELO/analisis_instruementos.ipynb
        added by us:     Documentos_PGF/Instrumentos_ELO/analisis_instruementos.ipynb
        added by them:   Documentos_PGF/Instrumentos_ELO/analisis_instrumentos.ipynb
        added by them:   Documentos_PGF/Instrumentos_ELO/documentacion_instrumentos.md

@PGF-Free-Knowledge ➜ /workspaces/aprendizaje-de-maquinas (main) $ git add "Documentos_PGF/Instrumentos_ELO/analisis_instrumentos.ipynb"
git add "Documentos_PGF/Instrumentos_ELO/documentacion_instrumentos.md"
git rm "Documentos_PGF/Instrumentos _ELO/analisis_instruementos.ipynb"
rm 'Documentos_PGF/Instrumentos _ELO/analisis_instruementos.ipynb'
@PGF-Free-Knowledge ➜ /workspaces/aprendizaje-de-maquinas (main) $ git status
On branch main
Your branch and 'origin/main' have diverged,
and have 2 and 15 different commits each, respectively.
  (use "git pull" if you want to integrate the remote branch with yours)

You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Changes to be committed:
        new file:   Documentos_PGF/Instrumentos_ELO/analisis_instrumentos.ipynb
        new file:   Documentos_PGF/Instrumentos_ELO/documentacion_instrumentos.md
        new file:   "Documentos_PGF/Teor\303\255a/Clase 1.pdf"
        new file:   "Documentos_PGF/Teor\303\255a/Clase 2.pdf"
        new file:   "Documentos_PGF/Teor\303\255a/Clase 3.pdf"
        new file:   "Documentos_PGF/Teor\303\255a/Clase 4.pdf"
        new file:   "Documentos_PGF/Teor\303\255a/Clase 5.pdf"
        new file:   Documentos_PGF/Videos/Links Videos Universidad de Chile
        new file:   Documentos_PGF/Videos/Links.md

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        added by us:     Documentos_PGF/Instrumentos_ELO/analisis_instruementos.ipynb

@PGF-Free-Knowledge ➜ /workspaces/aprendizaje-de-maquinas (main) $ git rm "Documentos_PGF/Instrumentos_ELO/analisis_instruementos.ipynb"
rm 'Documentos_PGF/Instrumentos_ELO/analisis_instruementos.ipynb'
@PGF-Free-Knowledge ➜ /workspaces/aprendizaje-de-maquinas (main) $ git status
On branch main
Your branch and 'origin/main' have diverged,
and have 2 and 15 different commits each, respectively.
  (use "git pull" if you want to integrate the remote branch with yours)

All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

Changes to be committed:
        renamed:    Documentos_PGF/Instrumentos_ELO/analisis_instruementos.ipynb -> Documentos_PGF/Instrumentos_ELO/analisis_instrumentos.ipynb
        new file:   Documentos_PGF/Instrumentos_ELO/documentacion_instrumentos.md
        new file:   "Documentos_PGF/Teor\303\255a/Clase 1.pdf"
        new file:   "Documentos_PGF/Teor\303\255a/Clase 2.pdf"
        new file:   "Documentos_PGF/Teor\303\255a/Clase 3.pdf"
        new file:   "Documentos_PGF/Teor\303\255a/Clase 4.pdf"
        new file:   "Documentos_PGF/Teor\303\255a/Clase 5.pdf"
        new file:   Documentos_PGF/Videos/Links Videos Universidad de Chile
        new file:   Documentos_PGF/Videos/Links.md

@PGF-Free-Knowledge ➜ /workspaces/aprendizaje-de-maquinas (main) $ git commit -m "Conflicto resuelto: limpieza de duplicados en Instrumentos_ELO"
[main 40d6f90] Conflicto resuelto: limpieza de duplicados en Instrumentos_ELO
@PGF-Free-Knowledge ➜ /workspaces/aprendizaje-de-maquinas (main) $ git push
Enumerating objects: 26, done.
Counting objects: 100% (26/26), done.
Delta compression using up to 2 threads
Compressing objects: 100% (20/20), done.
Writing objects: 100% (21/21), 1.23 MiB | 6.97 MiB/s, done.
Total 21 (delta 3), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (3/3), done.
To https://github.com/PGF-Free-Knowledge/aprendizaje-de-maquinas
   8c60ccc..40d6f90  main -> main
@PGF-Free-Knowledge ➜ /workspaces/aprendizaje-de-maquinas (main) $
