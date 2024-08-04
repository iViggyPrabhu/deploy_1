# Use the official Ubuntu 22.04 base image
FROM ubuntu:22.04
ENV http_proxy http://proxy-dmz.intel.com:912
ENV https_proxy http://proxy-dmz.intel.com:912
ENV no_proxy localhost,intel.com,.intel.com,*.intel.com,10.0.0.0/8
ENV DEBIAN_FRONTEND noninteractive

RUN cd /etc/apt/ && \
    touch apt.conf && \
    echo Acquire::http::Proxy "http://proxy-dmz.intel.com:912"; >>/etc/apt/apt.conf && \
    echo Acquire::https::Proxy "http://proxy-dmz.intel.com:912"; >>/etc/apt/apt.conf

RUN apt-get update && \
    apt-get -y install ca-certificates gnupg gnupg1 curl htop openssl tcpdump telnet traceroute zip unzip \
    software-properties-common vim wget build-essential python3-pip openssh-server && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Intel SSL certificate pre-install
RUN mkdir -p /usr/local/share/ca-certificates/intel && \
    cd /usr/local/share/ca-certificates/intel && \
    wget -qO- -O tmp.zip http://certificates.intel.com/repository/certificates/Intel%20Root%20Certificate%20Chain%20Base64.zip && unzip tmp.zip && rm tmp.zip &&\
    wget -qO- -O tmp.zip http://certificates.intel.com/repository/certificates/Public%20Root%20Certificate%20Chain%20Base64.zip && unzip tmp.zip && rm tmp.zip &&\
    wget -qO- -O tmp.zip http://certificates.intel.com/repository/certificates/IntelSHA2RootChain-Base64.zip && unzip tmp.zip && rm tmp.zip &&\
    wget -qO- -O tmp.zip http://certificates.intel.com/repository/certificates/PublicSHA2RootChain-Base64.zip && unzip tmp.zip && rm tmp.zip &&\
    update-ca-certificates


# Update the package lists
RUN apt-get update

# Install Python and pip
RUN apt-get install -y python3 python3-pip

# Install FastAPI and uvicorn
RUN pip3 install fastapi uvicorn

# Copy the app code to the container
COPY app /app

# Set the working directory
WORKDIR /app

# Expose the port on which the server will run
EXPOSE 8000

# Start the FastAPI server using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]