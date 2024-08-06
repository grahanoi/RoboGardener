FROM osrf/ros:humble-desktop-full

# Install additional packages
RUN apt-get update && apt-get install -y \
    nano \
    vim \
    sudo \
    python3-colcon-common-extensions \
    bash-completion \
    python3-argcomplete \
    && rm -rf /var/lib/apt/lists/*

# Arguments for user creation
ARG USERNAME=ros
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create a non-root user with sudo privileges
RUN groupadd --gid $USER_GID $USERNAME \
  && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
  && mkdir /home/$USERNAME/.config \
  && chown $USER_UID:$USER_GID /home/$USERNAME/.config \
  && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
  && chmod 0440 /etc/sudoers.d/$USERNAME

# Set working user to ros (uncomment as needed)
#USER root

# Copy the entrypoint script and bashrc
COPY entrypoint.sh /entrypoint.sh
COPY bashrc /home/${USERNAME}/.bashrc

# Ensure the entrypoint script is executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint and default command
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]