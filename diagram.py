from diagrams import Diagram, Cluster, Edge
from diagrams.azure.compute import FunctionApps
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.container import Docker
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet
from diagrams.k8s.compute import Pod
from diagrams.k8s.group import Namespace
from diagrams.generic.database import SQL
from diagrams.generic.compute import Rack

with Diagram("JobGenie System Architecture", show=False):
    user = User("Admin/User")
    
    with Cluster("Frontend"):
        frontend = Server("Django Admin")
    
    with Cluster("Backend"):
        backend = Server("Django")
        
    with Cluster("Tarefas Agendadas"):
        celery = Rack("Celery or Azure Logic Apps")
        redis = SQL("Redis")
    
    with Cluster("Banco de Dados"):
        db = PostgreSQL("PostgreSQL")
    
    with Cluster("Integração de IA"):
        ia = Internet("GPT/Claude")
    
    with Cluster("Plataforma de Execução"):
        azure_functions = FunctionApps("Azure Functions")
        
    with Cluster("Orquestração e Deploy"):
        k8s = Namespace("Kubernetes")
        docker = Docker("Docker")
        gh_actions = GithubActions("CI/CD")
    
    user >> Edge(color="black") >> frontend
    frontend >> Edge(color="black") >> backend
    backend >> Edge(color="blue") >> db
    backend >> Edge(color="blue") >> celery
    celery >> Edge(color="blue") >> redis
    backend >> Edge(color="blue") >> azure_functions
    backend >> Edge(color="blue") >> ia
    backend >> Edge(color="blue") >> k8s
    k8s >> Edge(color="blue") >> docker
    docker >> Edge(color="blue") >> gh_actions
