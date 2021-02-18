FROM tensorflow/tfx:0.26.0

# ENV CUDA_VERSION 11.0
# ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
# ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64
# ENV NVIDIA_VISIBLE_DEVICES all
# ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
# ENV NVIDIA_REQUIRE_CUDA "cuda=11.0 brand=tesla,driver>=418,driver<419 brand=tesla,driver>=440,driver<441 driver>=450,driver<451"
# ENV CUDNN_VERSION 8.0.5.39
# ENV TF_FORCE_GPU_ALLOW_GROWTH true
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     ca-certificates apt-transport-https gnupg-curl && \
#     NVIDIA_GPGKEY_SUM=d1be581509378368edeec8c1eb2958702feedf3bc3d17011adbf24efacce4ab5 && \
#     NVIDIA_GPGKEY_FPR=ae09fe4bbd223a84b2ccfce3f60f4b3d7fa2af80 && \
#     apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub && \
#     apt-key adv --export --no-emit-version -a $NVIDIA_GPGKEY_FPR | tail -n +5 > cudasign.pub && \
#     echo "$NVIDIA_GPGKEY_SUM  cudasign.pub" | sha256sum -c --strict - && rm cudasign.pub && \
#     echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/cuda.list && \
#     echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list && \
#     apt-get update && apt-get install -y --no-install-recommends \
#     cuda-cudart-11-0 \
#     cuda-compat-11-0 \
#     cuda-libraries-11-0 \
#     libnpp-11-0 \
#     cuda-nvtx-11-0 \
#     libcublas-11-0 \
#     libcusparse-11-0 \
#     libcudnn8=$CUDNN_VERSION-1+cuda11.0 \
#     cuda-cupti-11-0 \
#     && ln -s cuda-11.0 /usr/local/cuda && \
#     echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf \
#     && echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf && \
#     apt-get purge --auto-remove -y gnupg-curl && \
#     apt-mark hold libcublas-11-2 && \
#     apt-mark hold libcudnn8 && \
#     rm -rf /var/lib/apt/lists/*
# RUN pip install tensorflow-gpu==2.4
# RUN pip install tensorflow-text tensorflow_ranking 

WORKDIR /pipeline
COPY ./ ./
ENV PYTHONPATH="/pipeline:${PYTHONPATH}"
RUN pip install tensorflow-text tensorflow_ranking 
# ENTRYPOINT ["python3.7", "/tfx/tfx/scripts/run_executor.py"]