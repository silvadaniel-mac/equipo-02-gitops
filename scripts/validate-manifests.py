import re
from pathlib import Path
import yaml

REPO = "https://github.com/silvadaniel-mac/equipo-02-gitops.git"
for env, replicas in (("dev", 1), ("prod", 2)):
    ns = "aulaviva-" + env
    docs = list(yaml.safe_load_all(Path(f"artifacts/{env}.yaml").read_text()))
    by_kind = {d["kind"]: d for d in docs if d}
    assert by_kind["Namespace"]["metadata"]["name"] == ns
    assert set(by_kind) == {"Namespace", "Service", "Deployment"}
    dep = by_kind["Deployment"]
    assert dep["metadata"]["namespace"] == ns
    assert by_kind["Service"]["metadata"]["namespace"] == ns
    assert by_kind["Service"]["spec"]["type"] == "ClusterIP"
    assert dep["spec"]["replicas"] == replicas
    pod = dep["spec"]["template"]["spec"]
    c = pod["containers"][0]
    assert re.fullmatch(r"ghcr\.io/silvadaniel-mac/aulaviva-api@sha256:[0-9a-f]{64}", c["image"])
    assert pod["securityContext"]["runAsNonRoot"] is True
    assert pod["automountServiceAccountToken"] is False
    assert c["securityContext"]["allowPrivilegeEscalation"] is False
    assert c["securityContext"]["readOnlyRootFilesystem"] is True
    assert "ALL" in c["securityContext"]["capabilities"]["drop"]
    assert all(k in c for k in ("readinessProbe", "livenessProbe", "resources"))
    app = yaml.safe_load(Path(f"argocd/application-{env}.yaml").read_text())["spec"]
    assert app["source"]["repoURL"] == REPO
    assert app["source"]["targetRevision"] == "main"
    assert app["source"]["path"] == "overlays/" + env
    assert app["destination"]["namespace"] == ns
    print(f"{env}: manifiestos, digest, namespace y seguridad OK")
project = yaml.safe_load(Path("argocd/project.yaml").read_text())["spec"]
assert project["sourceRepos"] == [REPO]
assert {d["namespace"] for d in project["destinations"]} == {"aulaviva-dev", "aulaviva-prod"}
print("AppProject restringido: OK")
