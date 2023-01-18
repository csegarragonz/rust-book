FROM csegarragonz/dotfiles:0.2.0 as dotfiles
FROM ubuntu:22.04

SHELL ["/bin/bash", "-c"]
ENV RUST_DOCKER="on"

# APT dependencies
RUN apt update \
    && apt upgrade -y \
    && apt install -y \
        build-essential \
        curl \
        git \
        python3-dev \
        python3-pip \
        python3-venv

# Install latest rust and rust-analyser
RUN curl --proto '=https' --tlsv1.3 https://sh.rustup.rs -sSf | sh -s -- -y \
    && curl -L \
        https://github.com/rust-lang/rust-analyzer/releases/latest/download/rust-analyzer-x86_64-unknown-linux-gnu.gz \
        | gunzip -c - > /usr/bin/rust-analyzer \
    && chmod +x /usr/bin/rust-analyzer

# Get the source code
RUN git clone https://github.com/csegarragonz/rust-book /rust-book \
    && cd /rust-book \
    && ./bin/create_venv.sh

# Prepare development environment
COPY --from=dotfiles /neovim/build/bin/nvim /usr/bin/nvim
COPY --from=dotfiles /usr/local/share/nvim /usr/local/share/nvim
RUN git clone https://github.com/csegarragonz/dotfiles ~/dotfiles \
    && curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
        https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim \
    && mkdir -p ~/.config/nvim/ \
    && ln -s ~/dotfiles/nvim/init.vim ~/.config/nvim/init.vim \
    && ln -s ~/dotfiles/nvim/after ~/.config/nvim/ \
    && ln -s ~/dotfiles/nvim/syntax ~/.config/nvim/ \
    && nvim +PlugInstall +qa \
    && nvim +PlugUpdate +qa \
    && ln -sf ~/dotfiles/bash/.bashrc ~/.bashrc \
    && ln -sf ~/dotfiles/bash/.bash_profile ~/.bash_profile \
    && ln -sf ~/dotfiles/bash/.bash_aliases ~/.bash_aliases \
    && echo ". /rust-book/bin/workon.sh" >> ~/.bashrc

WORKDIR /rust-book
CMD ["/bin/bash", "-l"]
