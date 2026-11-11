Microsoft Foundry
1. Create a new microsoft foundry
2. inside the new foundry create a new agent
3. give the agent the name according to task
4. give it instructions and upload a files with required rules
5. add guardrail if needed
6. test it in the Foundry playground with relevant questions

Integrate with PyCharm
1. create a new python project 
2. create a requirements.txt file and add the required libraries for the project ( pip install -r requirements.txt   )
3. create a .env file with foundry project endpoint and foundry agent name
3. create a main.py and write code to run the agent in terminal
4. test the agent in the terminal by asking relevant questions

Integrate with redis(Docker)
1. update the main.py code with fastapi 
2. add redis url in.env file
3. then run the following command:
docker run -d --name employee-redis -p 127.0.0.1:6379:6379 -v employee_redis_data:/data redis:7-alpine redis-server --appendonly yes                   
exec employee-redis redis-cli ping
python -m uvicorn main:app --reload   
4. then open http://127.0.0.1:8000/docs?utm_source=chatgpt.com#/default url and text out GET and POST
5. run this command: docker exec -it employee-redis redis-cli
   127.0.0.1:6379> KEYS employee:*
and ensure the steps are being shown