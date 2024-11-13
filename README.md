pip install SQLAlchemy   
pip install alembic  
alembic init alembic  
pip install pymssql  
pip install pyodbc  


alembic revision --autogenerate -m "Initial migration from SQL schema"   
alembic upgrade head  


pip install "fastapi[standard]"   
