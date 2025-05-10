{
  description="anonymity_api flake";
  inputs = {
    nixpkgs.url = "github:NixOs/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
     devShells.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          python313
          uv
        ];
        shellHook = ''
        '';
      } ;
    }
  );
}

