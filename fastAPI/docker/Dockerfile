FROM public.ecr.aws/lambda/python:3.11
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.7.1 /lambda-adapter /opt/extensions/lambda-adapter

WORKDIR /app

# 依存関係のインストールなど
COPY ./api /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# GOOGLE SECRETbn
COPY  ./service-account.json /app/service-account.json

#環境変数. RUN のあと環境変数は失われるので無意味
COPY ./.env.docker /app/.env
#RUN export $(cat /app/.env | xargs )
#RUN . /app/.env.sh

ENTRYPOINT ["uvicorn"]
CMD [ "main:app", "--host", "0.0.0.0", "--port", "5050" , "--env-file", "/app/.env"]
