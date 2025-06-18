libreoffice --version
RUN apt-get update && apt-get install -y libreoffice
libreoffice --headless --convert-to pdf --outdir /app/converted /app/uploads/sample.docx

docker build -t word2pdf .
docker run -p 5005:5005 word2pdf
