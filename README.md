# AulaViva MIDAMA — GitOps S08 y S18

Repositorio de configuración separado de [la aplicación MIDAMA](https://github.com/silvadaniel-mac/equipo-02--MIDAMA). Importación inicial desde el commit de aplicación 309e3e7b71571d77a0fad4d011222b90beed1b5e, validado en [S08 run 45745217466](https://github.com/silvadaniel-mac/equipo-02--MIDAMA/actions/runs/45745217466). La imagen de S08 es ghcr.io/silvadaniel-mac/aulaviva-api@sha256:a39d94c1b0fe023fff112f7e8dc0225c11b11e8ab90feaa72eae983a284ac64e. Ambos overlays comienzan en ese digest como baseline de laboratorio; no implica promoción ni despliegue real a producción. El servicio académico S18 se prueba adicionalmente en el pipeline S10 del repo app, no se declara desplegado aquí.

- base: Deployment no-root, probes, límites y Service.
- overlays/dev y overlays/prod: namespaces separados, 1 y 2 réplicas, respectivamente.
- argocd: AppProject restringido y Applications apuntando a este repositorio.
- CI manifests: render y comprobaciones de ambos ambientes, artefacto descargable.
- CODEOWNERS: propietarios de revisión. Activar protección de main con 2 aprobaciones y check manifests luego de la importación.

## Validación y operación
```sh
kubectl kustomize overlays/dev
kubectl kustomize overlays/prod
```
Para sincronizar en un clúster autorizado con Argo CD instalado, aplicar project.yaml y application-dev.yaml. Antes de usar producción, revisar acceso GHCR, capacidad, secretos, políticas y aprobación del equipo. No aplicar application-prod.yaml en un entorno real solo por realizar el laboratorio. El clúster de Actions es efímero.

## Promoción entre repositorios
La app contiene el workflow S08 y scripts/promote-s08.sh. El propietario debe crear una GitHub App dedicada con Contents y Pull requests read/write, instalada solo en este repo. En el repo app definir GITOPS_REPOSITORY=silvadaniel-mac/equipo-02-gitops, GITOPS_OWNER=silvadaniel-mac, GITOPS_REPO_NAME=equipo-02-gitops, GITOPS_APP_ID (ID de esa app), y secret GITOPS_APP_PRIVATE_KEY. No guardar claves aquí. El workflow abre PR para dev tras push a main. La fusión requiere revisión humana. Producción se promueve por PR separado, después de probar dev.

## Rollback
Crear un PR que restablezca el digest anteriormente validado en el overlay afectado. Revisar CI, aprobar y fusionar; comprobar Synced/Healthy, revisión e imagen desplegada en el clúster autorizado. No editar tags ni forzar pushes.

Estado inicial: configuración importada; la automatización externa y sincronización en clúster externo deben verificarse tras configurar la app y fusionar el PR. No almacenar kubeconfig, contraseñas ni datos de estudiantes.
