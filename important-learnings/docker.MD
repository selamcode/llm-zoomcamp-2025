Notes are from the official docker documentation and other source

### Containers 

> containers are isolated processes for each of your app's components. Each component - **the frontend React app, the Python API engine, and the database** runs in its own isolated environment, completely isolated from everything else on your machine. 

---

### Docker <img src="images/docker5.svg" width="60"/>

Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly.

##### Here's what makes containers(docker) awesome. 

Containers (Docker) are:

- **Self-contained**. Each container has everything it needs to function with no reliance on any pre-installed dependencies on the host machine.
- **Isolated**. Since containers are run in isolation, they have minimal influence on the host and other containers, increasing the security of your applications.
- **Independent**. Each container is independently managed. Deleting one container won't affect any others.
- **Portable**. Containers can run anywhere! The container that runs on your development machine will work the same way in a data center or anywhere in the cloud!
</br>

---
### Image


</br>

> A container image is a standardized package that includes all of the files, binaries, libraries, and configurations to run a container.

</br>

##### There are two important principles of images:

1. Images are immutable. Once an image is created, it can't be modified. You can only make a new image or add changes on top of it.

2. Container images are composed of layers. Each layer represents a set of file system changes that add, remove, or modify files.

</br>
These two principles let you to extend or add to existing images. For example, if you are building a Python app, you can start from the [Python image](https://hub.docker.com/_/python)  and add additional layers to install your app's dependencies and add your code. This lets you focus on your app, rather than Python itself.

### More On Docker Images and Layers 

Docker images are built in layers, so when you want to update an image (say from version v1 to v2), you:

- Start from the v1 image as the base.

- Add your updates or changes on top as a new layer.

- Save this combined result as a new image, which you can tag as v2.

</br>

This way, v2 contains all of v1’s layers plus the new changes, without duplicating everything. It’s efficient, and you can always roll back or use different versions easily.

</br>

> Updating images is about building new layers on top of existing ones and tagging them as new versions.

</br>

##### Finding images
[Docker Hub](https://hub.docker.com/)  is the default global marketplace for storing and distributing images. 

</br>

---
### Registry



Now that you know what a container image is and how it works, you might wonder - where do you store these images?

Well, you can store your container images on your computer system, but what if you want to share them with your friends or use them on another machine? That's where the image registry comes in.

An image registry is a centralized location for storing and sharing your container images. It can be either public or private. [Docker Hub](https://hub.docker.com/)  is a public registry that anyone can use and is the default registry.

Registry vs. repository
While you're working with registries, you might hear the terms registry and repository as if they're interchangeable. Even though they're related, they're not quite the same thing.

A registry is a centralized location that stores and manages container images, whereas a repository is a collection of related container images within a registry. Think of it as a folder where you organize your images based on projects. Each repository contains one or more container imagereg

![Registry vs.Repository](images/Registry%20vs.Repository.png)

---
### Docker Compose

So far, you’ve worked with single-container apps. But real-world apps often need multiple services—like databases, caches, or message queues.

A best practice is to run one service per container. While you can start multiple containers using docker run, managing networks and connections quickly becomes complex.

That’s why tools like Docker Compose exist—to simplify running and connecting multi-container apps.

##### What is Docker Compose?
> Docker Compose is a tool that lets you define and run multiple Docker containers together using a docker-compose.yml file.

> It helps you describe how different containers should work together—like a web server, a database, and a cache, all in one place.

> 💡 Think of Docker Compose as a project manager for multiple services that need to run together.

Here its's important to understand the how it's different from **Dockerfile**.

### Dockerfile vs Docker Compose

A **Dockerfile** is used to define how to build a single Docker image, specifying the environment, dependencies, and startup commands for one container. In contrast, **Docker Compose** uses a `docker-compose.yml` file to configure and run multiple containers together, allowing you to define how different services (like a web app, database, and cache) interact and start them all with a single command. In short, Dockerfile builds one container, while Docker Compose orchestrates many.

#### 💡 Example 
> 🛠 Dockerfile is like writing the setup instructions for one service, such as a backend API — it tells Docker how to build and run just that piece.

> 🔗 Docker Compose is like a service manager that launches and connects multiple services — like a backend API, a database, and a frontend — making sure they run together in one environment.

##### In short:

> Dockerfile = how to build one service.

> Docker Compose = how to run and connect multiple services as a complete system.

---

### Dockerfile

A Dockerfile is a text-based document that's used to create a container image. It provides instructions to the image builder on the commands to run, files to copy, startup command, and more.

##### As an example, the following Dockerfile would produce a ready-to-run Python application:
``` docker

FROM python:3.12
WORKDIR /usr/local/app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY src ./src
EXPOSE 5000

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

`CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

```

### A Dockerfile typically follows these steps:

- Determine your base image
- Install application dependencies
- Copy in any relevant source code and/or binaries
- Configure the final image


