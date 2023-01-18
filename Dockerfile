FROM csegarragonz/dotfiles:0.2.0 as dotfiles
FROM ubuntu:22.04

RUN nvim +PlugInstall +qa \
    && nvim +PlugUpdate +qa

# APT dependencies
RUN apt update \
    && apt upgrade -y \
    && apt install -y \
        curl \
        git

# Install latest rust
RUN curl --proto '=https' --tlsv1.3 https://sh.rustup.rs -sSf | sh -s -- -y

# Get the source code
RUN git clone https://github.com/csegarragonz/rust-book /rust-book

# Prepare development environment
COPY --from=dotfiles /neovim/build/bin/nvim /usr/bin/nvim
COPY --from=dotfiles /usr/local/share/nvim /usr/local/share/nvim
RUN git clone https://github.com/csegarragonz/dotfiles ~/dotfiles
    && curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
        https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim \
    && mkdir -p ~/.config/nvim/ \
    && ln -s ~/dotfiles/nvim/init.vim ~/.config/nvim/init.vim \
    && ln -s ~/dotfiles/nvim/after ~/.config/nvim/ \
    && ln -s ~/dotfiles/nvim/syntax ~/.config/nvim/ \
    && nvim +PlugInstall +qa \
    && nvim +PlugUpdate +qa
    && ln -sf ~/dotfiles/bash/.bashrc ~/.bashrc \
    && ln -sf ~/dotfiles/bash/.bash_profile ~/.bash_profile \
    && ln -sf ~/dotfiles/bash/.bash_aliases ~/.bash_aliases \
    && echo ". /rust-book/bin/workon.sh" >> ~/.bashrc

WORKDIR /rust-book
