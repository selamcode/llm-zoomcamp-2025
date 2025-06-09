### 1. Publishing and Exposing Ports

- What: Letting your container talk to the outside world by opening network ports.

- Why: So you can access apps inside containers (like a web server) from your computer or other devices.

- Example: Mapping container port 80 to your computer’s port 8080 lets you visit localhost:8080 to see the app.

### 2. Overriding Container Defaults
- What: Changing what a container does when it starts.

- Why: To customize or run different commands instead of the default one baked into the image.

- Example: Running a container’s shell (bash) instead of its default app.

### 3. Persisting Container Data
- What: Saving data created inside a container so it’s not lost when the container stops or is removed.

- Why: Containers are temporary by nature — without persistence, all data inside disappears.

- Example: Using Docker volumes or bind mounts to save a database’s files on your computer.

### 4. Sharing Local Files with Containers
- What: Letting containers use files from your local machine.

- Why: For easy code editing, config sharing, or testing without rebuilding images.

- Example: Mounting your app folder into the container so changes appear instantly inside.

### 5. Multi-Container Applications
- What: Running multiple containers together to form a complete app (like web server + database).

- Why: Separates responsibilities, making apps modular, scalable, and easier to manage.

- Example: Using Docker Compose to start a web app container and a database container at the same time.

