{
    description = "Flashcards flake";

    inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    };

    outputs = { nixpkgs, ... }:
    let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    in
    {
        devShells.${system}.default = pkgs.mkShell {
            packages = [
                pkgs.python314
                pkgs.uv
            ];
            shellHook = ''
                source ~/.bashrc
                cd ..
                uv sync
                if [ -d .venv ]; then
                    source .venv/bin/activate
                fi
                tput setaf 2
                echo "Happy hacking!"
                tput sgr0
            '';
        };
    };
}
