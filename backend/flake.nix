{
  description = "LangGraph React Agent Studio development environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.pyproject-nix.url = "github:nix-community/pyproject.nix";

  outputs = { self, nixpkgs, pyproject-nix, ... }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      python = pkgs.python311; # or your required version
      project = pyproject-nix.lib.project.loadPyproject {
        projectRoot = ./.;
      };
      attrs = project.renderers.buildPythonPackage { inherit python; };
    in {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [ python pkgs.nodejs pkgs.git ];
        inputsFrom = [ python.pkgs.buildPythonPackage attrs ];
      };
    };
}
