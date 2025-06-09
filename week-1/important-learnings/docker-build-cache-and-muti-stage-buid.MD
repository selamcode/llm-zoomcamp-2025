## Build Cache and Multi-Stage Build


##### 🧠 1. What Is Docker Build Cache?

Docker builds your image step by step, layer by layer, from your Dockerfile.

Each instruction (like COPY, RUN, etc.) creates a layer.

Docker caches those layers to avoid rebuilding them if nothing has changed.

</br>

``` dockerfile
🔁 Build Cache in Action:
Dockerfile

FROM node:18

WORKDIR /app

COPY package.json .
RUN npm install         # ⏱ Cached unless package.json changes

COPY . .                # ⏱ Cached unless your code changes

CMD ["node", "app.js"]

```

If you modify just your source code and leave the dependency list unchanged:

- Docker skips the npm install

- Only re-runs the last COPY . . and CMD steps

💡 Result: Rebuild is faster because it uses the cached layers

---

### Multi-Stage Build

Before going to muti-satge build we must understand `Build Time` and `Runtime(Run Time)` in devlopemnt.

###### `Build Time`

- This is when your code is converted into a runnable form.

- In compiled languages (like C, Java), this means compiling source code into binaries or bytecode.

- In interpreted languages (like Python), this means installing dependencies, preparing environment, maybe running scripts to set things up.

- Build time happens once, before the app runs.

- It often requires tools like compilers (gcc), package managers (pip), or bundlers.

###### `Runtime (or Run Time)`

- This is when your app is actually running and serving its purpose.

- The program executes, responding to user input or performing tasks.

- The runtime environment needs the built or prepared files (executables, installed libraries, source code).

- Build tools are usually not needed here — just the final product.

---
### Muti-Stage Build

This is basiclly separating the `build environment` from the final `runtime environment`. 

This is done in the dockerfile.


``` dockerfile

# 🏗 Stage 1: Build stage
# Why? We need a full Python environment and tools like gcc and pip to install packages and turn our app into a binary.
FROM python:3.11-slim AS builder

# Why? Some Python packages (like cryptography or numpy) need a C compiler to be installed, so we install gcc and other tools.
RUN apt-get update && apt-get install -y gcc python3-dev libffi-dev build-essential

# Why? Set our working folder inside the container.
WORKDIR /app

# Why? We copy the list of required Python packages into the container so we can install them before copying the whole code.
COPY requirements.txt .

# Why? We install all Python packages we need to run the app, including PyInstaller which helps us convert Python code to a binary.
RUN pip install pyinstaller
RUN pip install -r requirements.txt

# Why? Now we copy the full source code into the container (after dependencies) to avoid rebuilding if dependencies haven’t changed.
COPY . .

# Why? We use PyInstaller to turn app.py into a single binary so that we don’t need Python or source code in the final image.
RUN pyinstaller --onefile app.py

---

# 🚀 Stage 2: Runtime stage
# Why? This is the lightweight container that will run in production. It only includes what we need to run the binary.

FROM debian:bullseye-slim

# Why? The binary created with PyInstaller still needs some system libraries like libffi or glib to run, so we install them here.
RUN apt-get update && apt-get install -y libffi7 libglib2.0-0 && apt-get clean

# Why? Set the working directory again in this second stage.
WORKDIR /app

# Why? We copy only the compiled binary from the build stage. No Python, no source code, no extra files.
COPY --from=builder /app/dist/app /app/app

# Why? This tells Docker to run the binary when the container starts.
CMD ["./app"]


```

</br>

| Item                           | Present in Build | Present in Runtime | Why Not in Runtime (if excluded)             |
| ------------------------------ | ---------------- | ------------------ | -------------------------------------------- |
| Python Interpreter             | Yes              | Yes                | Needed for app execution                     |
| pip                            | Yes              | No (usually)       | Not needed; dependencies pre-installed       |
| System Build Tools (gcc, make) | Yes              | No                 | Bulky, security risk, only needed to compile |
| Installed Python Packages      | Yes              | Yes                | Needed for app functionality                 |
| App Source Code                | Yes              | Yes                | Needed to run app                            |
| Build Temporary Files          | Yes              | No                 | Waste space, unnecessary for running app     |

</br>

### 🧠 Why Use Multi-Stage Build? (Simple Explanation)

</br>

| Problem Without Multi-Stage        | Multi-Stage Solution                         |
| ---------------------------------- | -------------------------------------------- |
| Big images with unused tools       | 🧹 Only keep what we need in the final image |
| Source code exposed in container   | 🔒 Source code stays in the build stage      |
| Python and pip needed at runtime   | 🪶 Remove them — just run a binary           |
| Security risk from too many layers | 🔐 Smaller, safer runtime image              |
| Slower startup and larger deploys  | 🚀 Fast, light container to ship and start   |
