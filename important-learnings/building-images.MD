### Build, Tag, and Publish an Image
---

- Building images - the process of building an image based on a Dockerfile
- Tagging images - the process of giving an image a name, which also determines where the image can be distributed
- Publishing images - the process to distribute or share the newly created image using a container registry


---

### Building Images

Most often, images are built using a Dockerfile. The most basic docker build command might look like the following:

``` shell
docker build .
```

The final `.` in the command provides the path or URL to the build context. At this location, the builder will find the Dockerfile and other referenced files.

When you run a build, the builder pulls the base image, if needed, and then runs the instructions specified in the Dockerfile.

With the previous command, the image will have no name, but the output will provide the ID of the image. As an example, the previous command might produce the following output:
</br>

``` docker
docker build .
[+] Building 3.5s (11/11) FINISHED                                              docker:desktop-linux
 => [internal] load build definition from Dockerfile                                            0.0s
 => => transferring dockerfile: 308B                                                            0.0s
 => [internal] load metadata for docker.io/library/python:3.12                                  0.0s
 => [internal] load .dockerignore                                                               0.0s
 => => transferring context: 2B                                                                 0.0s
 => [1/6] FROM docker.io/library/python:3.12                                                    0.0s
 => [internal] load build context                                                               0.0s
 => => transferring context: 123B                                                               0.0s
 => [2/6] WORKDIR /usr/local/app                                                                0.0s
 => [3/6] RUN useradd app                                                                       0.1s
 => [4/6] COPY ./requirements.txt ./requirements.txt                                            0.0s
 => [5/6] RUN pip install --no-cache-dir --upgrade -r requirements.txt                          3.2s
 => [6/6] COPY ./app ./app                                                                      0.0s
 => exporting to image                                                                          0.1s
 => => exporting layers                                                                         0.1s
 => => writing image sha256:9924dfd9350407b3df01d1a0e1033b1e543523ce7d5d5e2c83a724480ebe8f00    0.0s

```

With the previous output, you could start a container by using the referenced image:

``` docker
docker run sha256:9924dfd9350407b3df01d1a0e1033b1e543523ce7d5d5e2c83a724480ebe8f00
```

That name certainly isn't memorable, which is where tagging becomes useful.

---

### Tagging Images

Tagging images is the method to provide an image with a memorable name. However, there is a structure to the name of an image. A full image name has the following structure:

``` docker
[HOST[:PORT_NUMBER]/]PATH[:TAG]
```
`HOST`: The optional registry hostname where the image is located. If no host is specified, Docker's public registry at `docker.io` is used by default.
`PORT_NUMBER`: The registry port number if a hostname is provided
`PATH`: The path of the image, consisting of slash-separated components. For Docker Hub, the format follows `[NAMESPACE/]REPOSITORY`, where namespace is either a user's or organization's name. If no namespace is specified, `library` is used, which is the namespace for Docker Official Images.
`TAG`: A custom, human-readable identifier that's typically used to identify different versions or variants of an image. If no tag is specified, `latest` is used by default.

To tag an image during a build, add the -t or --tag flag:


``` docker build -t my-username/my-image .```


If you've already built an image, you can add another tag to the image by using the docker image tag  command:


``` docker image tag my-username/my-image another-username/another-image:v1 ```

---

### Publishing Images

Once you have an image built and tagged, you're ready to push it to a registry. To do so, use the docker push  command:

```
docker push my-username/my-image

```


> ⓘ Requiring authentication

Before you're able to push an image to a repository, you will need to be authenticated. To do so, simply use the docker login  command.

---

#### Summary 

✅ In simple terms:
“You create something (build it), give it a name (tag it), and upload it (push/publish) so that you or others can use it — just like pushing code to GitHub.”

🔁 Docker vs GitHub (side by side):

   
| **Action**         | **GitHub**                   | **Docker**                                |
|-------------------|------------------------------|--------------------------------------------|
| Create            | Write code                   | Build an image from a Dockerfile           |
| Name it           | Name your repository         | Tag your image (e.g., `my-app:latest`)     |
| Upload it         | `git push`                   | `docker push`                              |
| Share or reuse    | Clone or pull the repo       | Pull and run the image in a container      |


Docker images are like deployable snapshots of your app, and Docker Hub is like GitHub for containers.


