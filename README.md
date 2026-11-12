# spending_tracker_api
Purchases spending tracker based on FastAPI with SQLAlchemy, Alembic, Pydantic and Redis cache.<br> Processed with Ruff and Dockerized with Github Actions CI.<br><br>
Start:
docker compose up --build --force-recreate --watch<br><br>  
After start do inside container:  
source ~/.bashrc,  
migrate,  
seed all,  
currencies:update
