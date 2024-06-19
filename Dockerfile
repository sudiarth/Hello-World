FROM python:alpine as release

# Install component
RUN apk add --no-cache wget gcompat tzdata

# Set the timezone to Makassar
ENV TZ=Asia/Makassar

WORKDIR /app

EXPOSE 80

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "app.py" ]
