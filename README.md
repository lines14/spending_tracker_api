# spending_tracker_api
Purchases spending tracker based on FastAPI with SQLAlchemy, Alembic, Pydantic and Redis cache.<br> Processed with Ruff and Dockerized with Github Actions CI.<br><br>
Local start:<br>
docker compose up --build --force-recreate --watch<br> 
Allowed commands inside container:<br> 
source ~/.bashrc, then:<br> 
migrate,  
seed all,  
currencies:update
