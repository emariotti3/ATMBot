FROM python:2.7-slim

ENV TOKEN "667720183:AAGKnQxLDRbrHfGFw21G0Z2TuLndc-1tkTY"
ENV GOOGLE_API_KEY "..."

# Copy the current directory contents into the container at /app
COPY . src/* /dataset/cajeros-automaticos/* ./
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r ./requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run bot.py when the container launches
CMD python bot.py ${TOKEN} ${GOOGLE_API_KEY}
