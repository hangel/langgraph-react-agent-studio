{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    pyproject-nix.url = "github:nix-community/pyproject.nix";
  };

  outputs = { self, nixpkgs, pyproject-nix, ... }:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
      project = pyproject-nix.lib.project.loadPyproject {
        projectRoot = ./frontend;
      };
      python = pkgs.python311;
      attrs = project.renderers.buildPythonPackage { inherit python; };
    in {
      packages.x86_64-linux.default = python.pkgs.buildPythonPackage attrs;
      devShells.x86_64-linux.default = pkgs.mkShell {
        buildInputs = [ python pkgs.nodejs ];
        inputsFrom = [ python.pkgs.buildPythonPackage attrs ];
      };
    };
}
